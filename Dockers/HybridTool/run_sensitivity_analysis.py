#!/usr/bin/env python3
"""
ECS Fargate Task: Sensitivity Analysis

Environment variables:
- JOB_ID: Job identifier
- PFD_GOAL: Target PFD value
- CONFIDENCE_GOAL: Target confidence level
- S3_BUCKET: S3 bucket name for results
- AWS_REGION: AWS region

Output:
- Uploads JSON to S3: s3://{S3_BUCKET}/results/sensitivity-analysis-{JOB_ID}.json
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
    get_confidence,
)
from bbn_inference.examples.example_for_composite_model import run_example_for_composite_model


def get_job_config() -> Dict[str, Any]:
    """Read and validate environment variables (Sensitivity Analysis specific)"""
    config = get_base_config()
    
    # Add Sensitivity Analysis specific environment variables
    config["CONFIDENCE_GOAL"] = float(os.environ.get("CONFIDENCE_GOAL", "0"))
    
    # Base validation
    validate_base_config(config)
    
    # Sensitivity Analysis specific validation
    if config["CONFIDENCE_GOAL"] <= 0:
        raise ValueError("CONFIDENCE_GOAL must be a positive number")
    if config["CONFIDENCE_GOAL"] > 1.0:
        raise ValueError("CONFIDENCE_GOAL must be between 0 and 1 (e.g., 0.95)")
    
    # Print configuration
    print_base_config(config)
    print(f"[CONFIG] CONFIDENCE_GOAL: {config['CONFIDENCE_GOAL']}")
    print(f"[CONFIG] DRAWS: {config['DRAWS']}")
    print(f"[CONFIG] TUNE: {config['TUNE']}")
    print(f"[CONFIG] CHAINS: {config['CHAINS']}")
    print(f"[CONFIG] THIN: {config['THIN']}")
    
    return config


def run_sensitivity_analysis(config: Dict[str, Any], bbn_data: Any) -> Dict[str, Any]:
    """Run Sensitivity Analysis"""
    pfd_goal = config["PFD_GOAL"]
    confidence_goal = config["CONFIDENCE_GOAL"]
    draws = config["DRAWS"]
    tune = config["TUNE"]
    chains = config["CHAINS"]
    thin = config["THIN"]
    
    # 1. Generate trace (Prior)
    print("\n[STEP 1] Generating composite model trace...")
    trace = run_example_for_composite_model(bbn_data, draws=draws, tune=tune, chains=chains, thin=thin)
    print("[STEP 1] Trace generation completed")

    # 2. Sensitivity Analysis & Prior Metrics
    print("\n[STEP 2] Running sensitivity analysis...")
    
    # Calculate required demand
    num_tests = get_number_of_required_demand(
        trace, pfd_goal=pfd_goal, confidence_goal=confidence_goal,
        draws=draws, tune=tune, chains=chains, thin=thin
    )
    
    # Calculate Prior PFD metrics (for context)
    prior_mean = trace.posterior["PFD"].mean().item()
    prior_conf = get_confidence(data=trace.posterior["PFD"], goal=pfd_goal)
    
    print(f"[STEP 2] Required number of tests: {int(num_tests)}")
    print(f"[STEP 2] Prior mean: {prior_mean}")
    print(f"[STEP 2] Prior confidence @goal: {prior_conf}")
    
    return {
        "num_tests": int(num_tests),
        "prior_mean": prior_mean,
        "prior_confidence": prior_conf,
    }


def build_result_json(
    config: Dict[str, Any], 
    result_metrics: Dict[str, Any], 
    bbn_input_info: Dict[str, Any]
) -> Dict[str, Any]:
    """Build result JSON"""
    return {
        "message": "Sensitivity analysis complete",
        "data": result_metrics,
        "bbn_input": bbn_input_info,
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
        "num_tests": result_metrics["num_tests"]
    }
    if config["TEST_OUTPUT_DIR"]:
        payload["local_path"] = s3_location
    else:
        payload["s3_location"] = f"s3://{config['S3_BUCKET']}/{s3_location}"
    return payload


def get_test_mode_dummy(config: Dict[str, Any]) -> Dict[str, Any]:
    """Generate dummy data for test mode"""
    num_tests = 99999
    return {
        "num_tests": num_tests,
        "prior_mean": config["PFD_GOAL"],
        "prior_confidence": config["CONFIDENCE_GOAL"],
    }


def main():
    """Main execution function"""
    run_task(
        task_name="Sensitivity Analysis",
        get_config_func=get_job_config,
        run_analysis_func=run_sensitivity_analysis,
        build_result_json_func=build_result_json,
        build_completion_payload_func=build_completion_payload,
        s3_key_prefix="sensitivity-analysis",
        test_mode_dummy_func=get_test_mode_dummy,
    )


if __name__ == "__main__":
    main()
