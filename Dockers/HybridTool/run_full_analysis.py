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

Output:
- Uploads JSON file to S3: s3://{S3_BUCKET}/results/full-analysis-{JOB_ID}.json
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
    get_number_of_required_demand,
    filter_outsiders,
    get_confidence,
    demand_model_func,
)
from bbn_inference.examples.example_for_composite_model import run_example_for_composite_model
from bbn_inference.bbn_utils import run_sampling


def get_job_config() -> Dict[str, Any]:
    """Read and validate environment variables (Full Analysis specific)"""
    config = get_base_config()
    
    # Add Full Analysis specific environment variables
    config["CONFIDENCE_GOAL"] = float(os.environ.get("CONFIDENCE_GOAL", "0"))
    config["FAILURES"] = int(os.environ.get("FAILURES", "0"))
    
    # Base validation
    validate_base_config(config)
    
    # Full Analysis specific validation
    if config["CONFIDENCE_GOAL"] <= 0:
        raise ValueError("CONFIDENCE_GOAL must be a positive number")
    if config["FAILURES"] < 0:
        raise ValueError("FAILURES must be non-negative")
    
    # Print configuration
    print_base_config(config)
    print(f"[CONFIG] CONFIDENCE_GOAL: {config['CONFIDENCE_GOAL']}")
    print(f"[CONFIG] FAILURES: {config['FAILURES']}")
    
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
    
    # 1. Generate trace (Prior)
    print("\n[STEP 1] Generating composite model trace...")
    trace = run_example_for_composite_model(bbn_data)
    print("[STEP 1] Trace generation completed")

    # 2. Sensitivity Analysis: calculate required demand and Prior metrics
    print("\n[STEP 2] Running sensitivity analysis...")
    demand_required = get_number_of_required_demand(
        trace, pfd_goal=pfd_goal, confidence_goal=confidence_goal
    )
    
    # Trace preprocessing for PFD update
    filtered_pfd_trace = filter_outsiders(trace.posterior["PFD"])
    prior_mean = trace.posterior["PFD"].mean().item()
    prior_conf = get_confidence(data=trace.posterior["PFD"], goal=pfd_goal)
    
    print(f"[STEP 2] Required number of tests: {int(demand_required)}")
    print(f"[STEP 2] Prior mean: {prior_mean}")
    print(f"[STEP 2] Prior confidence @goal: {prior_conf}")
    
    # 3. Full Analysis: iterate through demand_list and sample
    print("\n[STEP 3] Running iterative full analysis with demand list...")
    # Calculate demand list
    demand_list = list(range(500, int(demand_required) + 500, 500))
    pfd_output = []
    last_conf = None
    
    for idx, demand in enumerate(demand_list, 1):
        print(f"[STEP 3] Processing demand {idx}/{len(demand_list)}: {demand}")
        
        # Build demand model and run sampling
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
        
        # Store results as [demand (str), mean PFD (float)]
        pfd_output.append([str(demand), updated_mean])
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
            "pfd": result_metrics["pfd_output"],
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
