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
    demand_model_func,
)
from bbn_inference.examples.example_for_composite_model import run_example_for_composite_model
from bbn_inference.bbn_utils import run_sampling
from bbn_input_loader import load_bayesian_data_from_env


# Get job configuration from environment variables
def get_job_config() -> Dict[str, Any]:
    # Read environment variables
    config = {
        "JOB_ID": os.environ.get("JOB_ID"),
        "PFD_GOAL": float(os.environ.get("PFD_GOAL", "0")),
        "CONFIDENCE_GOAL": float(os.environ.get("CONFIDENCE_GOAL", "0")),
        "FAILURES": int(os.environ.get("FAILURES", "0")),
        "S3_BUCKET": os.environ.get("S3_BUCKET"),
        "AWS_REGION": os.environ.get("AWS_REGION", "ap-northeast-2"),
        "TEST_MODE": os.environ.get("TEST_MODE", "false").lower() == "true",
        "TEST_OUTPUT_DIR": os.environ.get("TEST_OUTPUT_DIR"),
        "BBN_INPUT_PATH": os.environ.get("BBN_INPUT_PATH"),
        "BBN_INPUT_BUCKET": os.environ.get("BBN_INPUT_BUCKET"),
        "JOBS_TABLE_NAME": os.environ.get("JOBS_TABLE_NAME"),
        "DRAWS": int(os.environ.get("DRAWS", "1000")),
        "TUNE": int(os.environ.get("TUNE", "100")),
        "CHAINS": int(os.environ.get("CHAINS", "4")),
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
    if config["FAILURES"] < 0:
        raise ValueError("FAILURES must be non-negative")

    print(f"[CONFIG] JOB_ID: {config['JOB_ID']}")
    print(f"[CONFIG] PFD_GOAL: {config['PFD_GOAL']}")
    print(f"[CONFIG] CONFIDENCE_GOAL: {config['CONFIDENCE_GOAL']}")
    print(f"[CONFIG] FAILURES: {config['FAILURES']}")
    print(f"[CONFIG] S3_BUCKET: {config['S3_BUCKET']}")
    print(f"[CONFIG] AWS_REGION: {config['AWS_REGION']}")
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

def run_full_analysis(config: Dict[str, Any], bbn_data: Any) -> Dict[str, Any]:
    
    pfd_goal = config["PFD_GOAL"]
    confidence_goal = config["CONFIDENCE_GOAL"]
    failures = config["FAILURES"]
    draws = config["DRAWS"]
    tune = config["TUNE"]
    chains = config["CHAINS"]
    
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
        updated_trace = run_sampling(model, draws=draws, tune=tune, chains=chains)
        
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

    # Upload to S3/Local
    print("\n[STEP 4] Uploading results...")
    s3_key = f"results/full-analysis-{job_id}.json"
    
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
        print(f"[STEP 4] Results uploaded to s3://{s3_bucket}/{s3_key}")
        return s3_key


def handle_error_and_exit(e: Exception, config: Dict[str, Any], dynamodb_client: Any) -> None:
    job_id = config.get("JOB_ID", "unknown")
    error_msg = f"Full analysis failed: {str(e)}"
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
    print("HybridTool Full Analysis - Starting")
    print("=" * 80)
    
    dynamodb_client = None
    config = {}
    
    try:
        # 1. Read environment variables and validate them
        config = get_job_config()
        
        # 2. Initialize DynamoDB client
        if config["JOBS_TABLE_NAME"]:
            dynamodb_client = boto3.client('dynamodb', region_name=config["AWS_REGION"])
            
        # 3. Update job status in DynamoDB: RUNNING
        update_job_status(dynamodb_client, config, status='RUNNING')
        
        # 4. Load BBN data and input information
        bbn_data, bbn_input_info = load_bbn_data_and_info(config)

        # 5. Run Full Analysis (include handling for test mode)
        if config["TEST_MODE"]:
            print("\n[TEST MODE] Skipping computation, using dummy values")
            demand_required = 99999
            result_metrics = {
                "demand_required": demand_required,
                "prior_mean": config["PFD_GOAL"],
                "prior_confidence": config["CONFIDENCE_GOAL"],
                "pfd_output": [["100", 99999], ["200", 99999]], # Dummy output structure
                "final_confidence": 99999.0
            }
            print(f"[STEP 3] Full analysis completed with dummy values")
        else:
            result_metrics = run_full_analysis(config, bbn_data)
        
        # 6. Upload results to S3/Local
        s3_location = upload_results_to_s3(config, result_metrics, bbn_input_info)
        
        # 7. Update job status in DynamoDB: COMPLETED
        s3_key_for_db = s3_location if not config["TEST_OUTPUT_DIR"] else None
        update_job_status(dynamodb_client, config, status='COMPLETED', s3_key=s3_key_for_db)
        
        # 8. Print completion payload
        print("\n" + "=" * 80)
        print("HybridTool Full Analysis - Completed Successfully")
        print("=" * 80)
        
        completion_payload = {
            "status": "completed",
            "job_id": config["JOB_ID"],
            "demand_required": result_metrics["demand_required"],
            "final_confidence": result_metrics["final_confidence"]
        }
        if config["TEST_OUTPUT_DIR"]:
            completion_payload["local_path"] = s3_location
        else:
            completion_payload["s3_location"] = f"s3://{config['S3_BUCKET']}/{s3_location}"
            
        print(json.dumps(completion_payload))
        
    except Exception as e:
        handle_error_and_exit(e, config if 'config' in locals() else {}, dynamodb_client)


if __name__ == "__main__":
    main()

