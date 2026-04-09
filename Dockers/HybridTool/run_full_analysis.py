#!/usr/bin/env python3
"""
Standalone full-analysis script for ECS Fargate Task

Environment variables:
- JOB_ID: Job identifier (used in S3 filename)
- PFD_GOAL: Target PFD value
- CONFIDENCE_GOAL: Target confidence level
- FAILURES: Observed number of failures
- S3_BUCKET: S3 bucket name for results
- AWS_REGION: AWS region
- PRIOR_TRACE_S3_KEY: (optional) S3 key of pre-computed prior trace (.nc)
                      If provided, skips run_composite_model and loads trace from S3.

Output:
- Uploads JSON file to S3: s3://{S3_BUCKET}/results/full-analysis-{JOB_ID}.json
"""

import os
import math
from typing import Dict, Any

from task_common import (
    get_base_config,
    validate_base_config,
    print_base_config,
    run_task,
    load_trace_from_s3,
)

from bbn_inference.sensitivity_analysis import (
    get_number_of_required_demand,
    filter_outsiders,
    get_confidence,
    demand_model_func,
)
from bbn_inference.runners.composite_model import run_composite_model
from bbn_inference.bbn_utils import run_sampling


def get_job_config() -> Dict[str, Any]:
    """Read and validate environment variables (Full Analysis specific)"""
    config = get_base_config()
    
    # Add Full Analysis specific environment variables
    config["CONFIDENCE_GOAL"] = float(os.environ.get("CONFIDENCE_GOAL", "0"))
    
    # FAILURES: required, must be provided (0 is a valid value, but None is not)
    failures_str = os.environ.get("FAILURES")
    if failures_str is None:
        raise ValueError("FAILURES environment variable is required")
    config["FAILURES"] = int(failures_str)
    
    # DEMAND_REQUIRED: required for full_analysis (must be provided from sensitivity analysis)
    demand_required_str = os.environ.get("DEMAND_REQUIRED")
    if demand_required_str is not None and demand_required_str.strip() != "":
        config["DEMAND_REQUIRED"] = int(demand_required_str)
    else:
        config["DEMAND_REQUIRED"] = None
    
    # Base validation
    validate_base_config(config)
    
    # Full Analysis specific validation
    if config["CONFIDENCE_GOAL"] <= 0:
        raise ValueError("CONFIDENCE_GOAL must be a positive number")
    if config["FAILURES"] < 0:
        raise ValueError("FAILURES must be non-negative")
    
    config["PRIOR_TRACE_S3_KEY"] = os.environ.get("PRIOR_TRACE_S3_KEY")

    # Print configuration
    print_base_config(config)
    print(f"[CONFIG] CONFIDENCE_GOAL: {config['CONFIDENCE_GOAL']}")
    print(f"[CONFIG] FAILURES: {config['FAILURES']}")
    if config["DEMAND_REQUIRED"] is not None:
        print(f"[CONFIG] DEMAND_REQUIRED: {config['DEMAND_REQUIRED']} (reusing from sensitivity analysis)")
    else:
        print(f"[CONFIG] DEMAND_REQUIRED: not provided (required - will raise error)")
    print(f"[CONFIG] DRAWS: {config['DRAWS']}")
    print(f"[CONFIG] TUNE: {config['TUNE']}")
    print(f"[CONFIG] CHAINS: {config['CHAINS']}")
    print(f"[CONFIG] THIN: {config['THIN']}")
    if config["PRIOR_TRACE_S3_KEY"]:
        print(f"[CONFIG] PRIOR_TRACE_S3_KEY: {config['PRIOR_TRACE_S3_KEY']}")

    return config


def run_full_analysis(config: Dict[str, Any], bbn_data: Any) -> Dict[str, Any]:
    """Run Full Analysis"""
    pfd_goal = config["PFD_GOAL"]
    confidence_goal = config["CONFIDENCE_GOAL"]
    failures = config["FAILURES"]
    draws = config["DRAWS"]
    tune = config["TUNE"]
    chains = config["CHAINS"]
    thin = config["THIN"]
    
    # 1. Get trace (Prior): load from S3 if available, otherwise compute
    prior_trace_s3_key = config.get("PRIOR_TRACE_S3_KEY")
    if prior_trace_s3_key:
        print(f"\n[STEP 1] Loading pre-computed trace from S3: {prior_trace_s3_key}")
        trace = load_trace_from_s3(config, prior_trace_s3_key)
        print("[STEP 1] Trace loaded from S3")
    else:
        print("\n[STEP 1] Generating composite model trace...")
        trace = run_composite_model(bbn_data, draws=draws, tune=tune, chains=chains, thin=thin)
    print("[STEP 1] Trace generation completed")

    # 2. Sensitivity Analysis: reuse required demand from sensitivity analysis
    print("\n[STEP 2] Using demand_required from sensitivity analysis...")
    
    # DEMAND_REQUIRED must be provided (validated by frontend)
    demand_required_provided = config.get("DEMAND_REQUIRED")
    if demand_required_provided is None:
        raise ValueError("DEMAND_REQUIRED must be provided. Please run Sensitivity Analysis first.")
    
    # Reuse value from sensitivity analysis (apply ceil for consistency)
    demand_required = int(math.ceil(float(demand_required_provided)))
    print(f"[STEP 2] Using provided demand_required: {demand_required} (from sensitivity analysis)")
    
    # Trace preprocessing for PFD update
    filtered_pfd_trace = filter_outsiders(trace.posterior["PFD"])
    prior_mean = trace.posterior["PFD"].mean().item()
    prior_conf = get_confidence(data=trace.posterior["PFD"], goal=pfd_goal)
    
    print(f"[STEP 2] Required number of tests: {demand_required}")
    print(f"[STEP 2] Prior mean: {prior_mean}")
    print(f"[STEP 2] Prior confidence @goal: {prior_conf}")
    
    # 3. Full Analysis: update PFD at required demand only
    print("\n[STEP 3] Running PFD update at required demand...")
    demand = demand_required
    print(f"[STEP 3] Processing demand: {demand}")

    model = demand_model_func(
        demand=demand,
        observed_failures=failures,
        pfd_trace=filtered_pfd_trace
    )
    updated_trace = run_sampling(model, draws=draws, tune=tune, chains=chains, thin=thin)

    updated_mean = updated_trace.posterior["pfd_prior"].mean().item()
    last_conf = get_confidence(
        data=updated_trace.posterior["pfd_prior"], goal=pfd_goal
    )

    pfd_output = [[str(demand), updated_mean]]
    print(f"[STEP 3] Demand={demand} -> PFD={updated_mean:.5g}, Confidence={last_conf:.4f}")

    return {
        "demand_required": int(demand_required),
        "prior_mean": prior_mean,
        "prior_confidence": prior_conf,
        "pfd_output": pfd_output,
        "final_confidence": last_conf
    }


def build_result_json(
    config: Dict[str, Any], 
    result_metrics: Dict[str, Any], 
    bbn_input_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Build result JSON"""
    return {
        "input": {
            "parameter": {
                "test_count": result_metrics["demand_required"],
                "target": config["PFD_GOAL"],
                "prior": {
                    "distribution": "trace",
                    "mean": result_metrics["prior_mean"],
                    "confidence": result_metrics["prior_confidence"],
                },
                "observed_failures": config["FAILURES"],
            },
            "bbn_input": bbn_input_info,
        },
        "output": {
            "mean_posterior_pfd": result_metrics["pfd_output"],
            "confidence": result_metrics["final_confidence"],
        },
    }


def build_completion_payload(
    config: Dict[str, Any], 
    result_metrics: Dict[str, Any], 
    s3_location: str
) -> Dict[str, Any]:
    """Build completion payload"""
    payload = {
        "status": "completed",
        "job_id": config["JOB_ID"],
        "demand_required": result_metrics["demand_required"],
        "final_confidence": result_metrics["final_confidence"]
    }
    if config["TEST_OUTPUT_DIR"]:
        payload["local_path"] = s3_location
    else:
        payload["s3_location"] = f"s3://{config['S3_BUCKET']}/{s3_location}"
    return payload


def get_test_mode_dummy(config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate dummy data for test mode"""
    demand_required = 99999
    return {
        "demand_required": demand_required,
        "prior_mean": config["PFD_GOAL"],
        "prior_confidence": config["CONFIDENCE_GOAL"],
        "pfd_output": [["100", 99999], ["200", 99999]],  # Dummy output structure
        "final_confidence": 99999.0
    }


def main():
    """Main execution function"""
    run_task(
        task_name="Full Analysis",
        get_config_func=get_job_config,
        run_analysis_func=run_full_analysis,
        build_result_json_func=build_result_json,
        build_completion_payload_func=build_completion_payload,
        s3_key_prefix="full-analysis",
        test_mode_dummy_func=get_test_mode_dummy,
    )


if __name__ == "__main__":
    main()
