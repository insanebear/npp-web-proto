#!/usr/bin/env python3
"""
ECS Fargate Task: Update PFD

Environment variables:
- JOB_ID: Job identifier
- PFD_GOAL: Target PFD value
- DEMAND: Number of tests
- FAILURES: Observed number of failures
- FORECAST_TESTS: (optional, default 0 = skip) Number of upcoming tests for the
                  posterior predictive failure forecast
- S3_BUCKET: S3 bucket name for results
- AWS_REGION: AWS region

Output:
- Uploads JSON to S3: s3://{S3_BUCKET}/results/update-pfd-{JOB_ID}.json
"""

import os
from typing import Dict, Any

from task_common import (
    get_base_config,
    validate_base_config,
    print_base_config,
    run_task,
)

from bbn_inference.sensitivity_analysis import (
    filter_outsiders,
    get_confidence,
    demand_model_func,
)
from bbn_inference.runners.composite_model import run_composite_model
from bbn_inference.bbn_utils import run_sampling, get_future_failure_prob


def get_job_config() -> Dict[str, Any]:
    """Read and validate environment variables (Update PFD specific)"""
    config = get_base_config()
    
    # Add Update PFD specific environment variables
    config["DEMAND"] = int(os.environ.get("DEMAND", "0"))
    config["FAILURES"] = int(os.environ.get("FAILURES", "0"))
    # Upcoming tests for the posterior predictive forecast (0 = skip)
    config["FORECAST_TESTS"] = int(os.environ.get("FORECAST_TESTS", "0"))

    # Base validation
    validate_base_config(config)

    # Update PFD specific validation
    if config["DEMAND"] <= 0:
        raise ValueError("DEMAND must be a positive number")
    if config["FAILURES"] < 0:
        raise ValueError("FAILURES must be non-negative")
    if config["FAILURES"] > config["DEMAND"]:
        raise ValueError("failures cannot exceed demand")
    if not (0 <= config["FORECAST_TESTS"] <= 10_000_000):
        raise ValueError("FORECAST_TESTS must be between 0 and 10,000,000")

    # Print configuration
    print_base_config(config)
    print(f"[CONFIG] DEMAND: {config['DEMAND']}")
    print(f"[CONFIG] FAILURES: {config['FAILURES']}")
    print(f"[CONFIG] FORECAST_TESTS: {config['FORECAST_TESTS']}")
    print(f"[CONFIG] DRAWS: {config['DRAWS']}")
    print(f"[CONFIG] TUNE: {config['TUNE']}")
    print(f"[CONFIG] CHAINS: {config['CHAINS']}")
    print(f"[CONFIG] THIN: {config['THIN']}")
    
    return config


def calculate_pfd_metrics(config: Dict[str, Any], bbn_data: Any) -> Dict[str, float]:
    """Calculate PFD metrics"""
    pfd_goal = config["PFD_GOAL"]
    demand = config["DEMAND"]
    failures = config["FAILURES"]
    draws = config["DRAWS"]
    tune = config["TUNE"]
    chains = config["CHAINS"]
    thin = config["THIN"]
    
    # 1. Generate trace (Prior)
    print("\n[STEP 1] Generating composite model trace...")
    trace = run_composite_model(bbn_data, draws=draws, tune=tune, chains=chains, thin=thin)
    print("[STEP 1] Trace generation completed")
    
    # 2. Trace preprocessing and Prior metrics
    filtered_pfd_trace = filter_outsiders(trace.posterior["PFD"])
    prior_mean = trace.posterior["PFD"].mean().item()
    before_conf = get_confidence(data=trace.posterior["PFD"], goal=pfd_goal)
    
    print(f"[STEP 2] Prior mean: {prior_mean}")
    print(f"[STEP 2] Prior confidence @goal: {before_conf}")
    
    # 3. PFD update (sampling - Posterior)
    print("\n[STEP 3] Running PFD update sampling...")
    model = demand_model_func(
        demand=demand,
        observed_failures=failures,
        pfd_trace=filtered_pfd_trace,
    )
    updated_trace = run_sampling(model, draws=draws, tune=tune, chains=chains, thin=thin)
    
    updated_pfd_mean = updated_trace.posterior["pfd_prior"].mean().item()
    updated_conf = get_confidence(
        data=updated_trace.posterior["pfd_prior"], goal=pfd_goal
    )

    print(f"[STEP 3] Updated PFD mean: {updated_pfd_mean}")
    print(f"[STEP 3] Updated confidence @goal: {updated_conf}")

    # Posterior predictive forecast: chance of seeing a failure in the upcoming tests
    forecast_tests = config["FORECAST_TESTS"]
    future_failure_prob = None
    if forecast_tests > 0:
        future_failure_prob = get_future_failure_prob(
            updated_trace.posterior["pfd_prior"], forecast_tests
        )
        print(f"[STEP 3] P(>=1 failure in next {forecast_tests} tests): {future_failure_prob:.4f}")

    return {
        "updated_pfd": updated_pfd_mean,
        "updated_confidence": updated_conf,
        "prior_mean": prior_mean,
        "prior_confidence": before_conf,
        "forecast_tests": forecast_tests,
        "future_failure_prob": future_failure_prob,
    }


def build_result_json(
    config: Dict[str, Any], 
    result_metrics: Dict[str, float], 
    bbn_input_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Build result JSON"""
    return {
        "message": "PFD updated",
        "data": result_metrics,
        "bbn_input": bbn_input_info,
    }


def build_completion_payload(
    config: Dict[str, Any], 
    result_metrics: Dict[str, float], 
    s3_location: str
) -> Dict[str, Any]:
    """Build completion payload"""
    payload = {
        "status": "completed",
        "job_id": config["JOB_ID"],
        "updated_pfd": result_metrics["updated_pfd"],
        "updated_confidence": result_metrics["updated_confidence"]
    }
    if config["TEST_OUTPUT_DIR"]:
        payload["local_path"] = s3_location
    else:
        payload["s3_location"] = f"s3://{config['S3_BUCKET']}/{s3_location}"
    return payload


def get_test_mode_dummy(config: Dict[str, Any]) -> Dict[str, float]:
    """Generate dummy data for test mode"""
    return {
        "updated_pfd": 99999.0,
        "updated_confidence": 99999.0,
        "prior_mean": config["PFD_GOAL"],
        "prior_confidence": 0.95,
        "forecast_tests": config["FORECAST_TESTS"],
        "future_failure_prob": 99999.0 if config["FORECAST_TESTS"] > 0 else None,
    }


def main():
    """Main execution function"""
    run_task(
        task_name="Update PFD",
        get_config_func=get_job_config,
        run_analysis_func=calculate_pfd_metrics,
        build_result_json_func=build_result_json,
        build_completion_payload_func=build_completion_payload,
        s3_key_prefix="full/update-pfd",
        test_mode_dummy_func=get_test_mode_dummy,
    )


if __name__ == "__main__":
    main()
