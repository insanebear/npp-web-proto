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
import sys
import json
from pathlib import Path
import boto3
from typing import Dict, Any, Tuple, Optional

sys.path.insert(0, '/app/server')

from bbn_inference.sensitivity_analysis import (
    get_number_of_required_demand,
    filter_outsiders,
    get_confidence,
)
from bbn_inference.examples.example_for_composite_model import run_example_for_composite_model
from bbn_input_loader import load_bayesian_data_from_env


# Get job configuration from environment variables
def get_job_config() -> Dict[str, Any]:
    # Read environment variables
    config = {
        "JOB_ID": os.environ.get("JOB_ID"),
        "PFD_GOAL": float(os.environ.get("PFD_GOAL", "0")),
        "CONFIDENCE_GOAL": float(os.environ.get("CONFIDENCE_GOAL", "0")),
        "S3_BUCKET": os.environ.get("S3_BUCKET"),
        "AWS_REGION": os.environ.get("AWS_REGION", "ap-northeast-2"),
        "TEST_MODE": os.environ.get("TEST_MODE", "false").lower() == "true",
        "TEST_OUTPUT_DIR": os.environ.get("TEST_OUTPUT_DIR"),
        "BBN_INPUT_PATH": os.environ.get("BBN_INPUT_PATH"),
        "BBN_INPUT_BUCKET": os.environ.get("BBN_INPUT_BUCKET"),
        "JOBS_TABLE_NAME": os.environ.get("JOBS_TABLE_NAME"),
    }
    
    if config["TEST_MODE"] and not config["TEST_OUTPUT_DIR"]:
        config["TEST_OUTPUT_DIR"] = os.path.join("tempDoc", "hybrid-tool-test")

    # Validation
    if not config["JOB_ID"]:
        raise ValueError("JOB_ID environment variable is required")
    if not config["S3_BUCKET"]:
        raise ValueError("S3_BUCKET environment variable is required")
    if config["PFD_GOAL"] <= 0 or config["CONFIDENCE_GOAL"] <= 0:
        raise ValueError("PFD_GOAL and CONFIDENCE_GOAL must be positive numbers")
    if config["CONFIDENCE_GOAL"] > 1.0:
        raise ValueError("CONFIDENCE_GOAL must be between 0 and 1 (e.g., 0.95)")

    print(f"[CONFIG] JOB_ID: {config['JOB_ID']}")
    print(f"[CONFIG] PFD_GOAL: {config['PFD_GOAL']}")
    print(f"[CONFIG] CONFIDENCE_GOAL: {config['CONFIDENCE_GOAL']}")
    print(f"[CONFIG] S3_BUCKET: {config['S3_BUCKET']}")
    print(f"[CONFIG] BBN_INPUT_PATH: {config['BBN_INPUT_PATH'] or 'default (nrc_report_data)'}")
    if config['BBN_INPUT_BUCKET']:
        print(f"[CONFIG] BBN_INPUT_BUCKET: {config['BBN_INPUT_BUCKET']}")

    return config

# Update job status in DynamoDB
def update_job_status(
    dynamodb_client: Any, 
    config: Dict[str, Any], 
    status: str, 
    s3_key: Optional[str] = None, 
    error_msg: Optional[str] = None
) -> None:
    jobs_table_name = config['JOBS_TABLE_NAME']
    job_id = config['JOB_ID']
    
    if not jobs_table_name or not dynamodb_client:
        return

    update_expression = 'SET jobStatus = :s'
    expression_attribute_values = {':s': {'S': status}}
    
    if status == 'COMPLETED' and s3_key:
        update_expression += ', resultsPath = :p'
        expression_attribute_values[':p'] = {'S': s3_key}
    elif status == 'FAILED' and error_msg:
        update_expression += ', errorMessage = :e'
        # considering DynamoDB characters limit
        expression_attribute_values[':e'] = {'S': error_msg[:500]}
    
    try:
        dynamodb_client.update_item(
            TableName=jobs_table_name,
            Key={'jobId': {'S': job_id}},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values
        )
        print(f"[DynamoDB] Job status updated to {status}: {job_id}")
    except Exception as e:
        print(f"[WARNING] Failed to update DynamoDB status to {status}: {str(e)}")

def load_bbn_data_and_info(config: Dict[str, Any]) -> Tuple[Any, Dict[str, Any]]:
    bbn_input_path = config["BBN_INPUT_PATH"]
    bbn_input_bucket = config["BBN_INPUT_BUCKET"]
    
    print(f"[DEBUG] Loading BBN data from: path={bbn_input_path}, bucket={bbn_input_bucket}")
    
    bbn_data = load_bayesian_data_from_env(
        bbn_input_path,
        bbn_input_bucket,
    )
    
    print(f"[DEBUG] BBN data loaded successfully. Complexity={bbn_data.complexity}")
    
    # Determine BBN input source for result metadata
    bbn_input_info = {}
    if bbn_input_path and bbn_input_bucket:
        bbn_input_info = {
            "source": "s3",
            "bucket": bbn_input_bucket,
            "key": bbn_input_path
        }
    elif bbn_input_path:
        bbn_input_info = {"source": "local", "path": bbn_input_path}
    else:
        bbn_input_info = {"source": "default", "description": "NRC report data (default)"}
        
    return bbn_data, bbn_input_info

def run_sensitivity_analysis(config: Dict[str, Any], bbn_data: Any) -> Dict[str, Any]:
    pfd_goal = config["PFD_GOAL"]
    confidence_goal = config["CONFIDENCE_GOAL"]
    
    # 1. Generate trace (Prior)
    print("\n[STEP 1] Generating composite model trace...")
    trace = run_example_for_composite_model(bbn_data)
    print("[STEP 1] Trace generation completed")

    # 2. Sensitivity Analysis & Prior Metrics
    print("\n[STEP 2] Running sensitivity analysis...")
    
    # Calculate required demand
    num_tests = get_number_of_required_demand(
        trace, pfd_goal=pfd_goal, confidence_goal=confidence_goal
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

def upload_results_to_s3(
    config: Dict[str, Any], 
    result_metrics: Dict[str, Any], 
    bbn_input_info: Dict[str, Any]
) -> str:
    job_id = config["JOB_ID"]
    s3_bucket = config["S3_BUCKET"]
    aws_region = config["AWS_REGION"]
    test_output_dir = config["TEST_OUTPUT_DIR"]
    
    # Build result JSON
    result_json = {
        "message": "Sensitivity analysis complete",
        "data": result_metrics,
        "bbn_input": bbn_input_info,
    }

    # Upload to S3/Local
    print("\n[STEP 3] Uploading results...")
    s3_key = f"results/sensitivity-analysis-{job_id}.json"
    
    if test_output_dir:
        output_path = Path(test_output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        local_file = output_path / s3_key.replace("/", "_") 
        local_file.write_text(json.dumps(result_json, indent=2), encoding="utf-8")
        print(f"[TEST MODE] Results saved locally to {local_file}")
        return str(local_file)
    else:
        s3_client = boto3.client('s3', region_name=aws_region)
        s3_client.put_object(
            Bucket=s3_bucket,
            Key=s3_key,
            Body=json.dumps(result_json, indent=2),
            ContentType="application/json"
        )
        print(f"[STEP 3] Results uploaded to s3://{s3_bucket}/{s3_key}")
        return s3_key
    
def handle_error_and_exit(e: Exception, config: Dict[str, Any], dynamodb_client: Any) -> None:
    job_id = config.get("JOB_ID", "unknown")
    error_msg = f"Sensitivity analysis failed: {str(e)}"
    print(f"\n[ERROR] {error_msg}", file=sys.stderr)

    # Update job status in DynamoDB: FAILED
    update_job_status(dynamodb_client, config, status='FAILED', error_msg=error_msg)
    
    print(json.dumps({
        "status": "failed",
        "job_id": job_id,
        "error": error_msg
    }))
    sys.exit(1)

def main():
    print("=" * 80)
    print("HybridTool Sensitivity Analysis - Starting")
    print("=" * 80)

    dynamodb_client = None

    try:
        # 1. Read environment variables and validate them
        config = get_job_config()

        # 2. Initialize DynamoDB client if needed
        if config["JOBS_TABLE_NAME"]:
            dynamodb_client = boto3.client('dynamodb', region_name=config["AWS_REGION"])

        # 3. Update job status in DynamoDB: RUNNING
        update_job_status(dynamodb_client, config, status='RUNNING')

        # 4. Load BBN data and input information
        bbn_data, bbn_input_info = load_bbn_data_and_info(config)

        # 5. Run sensitivity analysis (include handling for test mode)
        if config["TEST_MODE"]:
            print("\n[TEST MODE] Skipping computation, using dummy values")
            num_tests = 99999
            result_metrics = {
                "num_tests": num_tests,
                "prior_mean": config["PFD_GOAL"],
                "prior_confidence": config["CONFIDENCE_GOAL"],
            }
            print(f"[STEP 2] Required number of tests (DUMMY): {num_tests}")
        else:
            result_metrics = run_sensitivity_analysis(config, bbn_data)

        # 6. Upload results to S3/Local
        s3_location = upload_results_to_s3(config, result_metrics, bbn_input_info)

        # 7. Update job status in DynamoDB: COMPLETED
        s3_key_for_db = s3_location if not config["TEST_OUTPUT_DIR"] else None
        update_job_status(dynamodb_client, config, status='COMPLETED', s3_key=s3_key_for_db)

        # 8. Print completion payload
        print("\n" + "=" * 80)
        print("HybridTool Sensitivity Analysis - Completed Successfully")
        print("=" * 80)

        completion_payload = {
            "status": "completed",
            "job_id": config["JOB_ID"],
            "num_tests": result_metrics["num_tests"]
        }
        if config["TEST_OUTPUT_DIR"]:
            completion_payload["local_path"] = s3_location
        else:
            completion_payload["s3_location"] = f"s3://{config['S3_BUCKET']}/{s3_location}"
            
        print(json.dumps(completion_payload))

    except Exception as e:
        handle_error_and_exit(e, config, dynamodb_client)


if __name__ == "__main__":
    main()

