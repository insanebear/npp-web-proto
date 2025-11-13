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
import boto3
from typing import Dict, Any

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


def main():
    print("=" * 80)
    print("HybridTool Full Analysis - Starting")
    print("=" * 80)
    
    job_id = os.environ.get("JOB_ID")
    pfd_goal = float(os.environ.get("PFD_GOAL", "0"))
    confidence_goal = float(os.environ.get("CONFIDENCE_GOAL", "0"))
    failures = int(os.environ.get("FAILURES", "0"))
    s3_bucket = os.environ.get("S3_BUCKET")
    aws_region = os.environ.get("AWS_REGION", "ap-northeast-2")
    test_mode = os.environ.get("TEST_MODE", "false").lower() == "true"
    bbn_input_path = os.environ.get("BBN_INPUT_PATH")
    bbn_input_bucket = os.environ.get("BBN_INPUT_BUCKET")
    jobs_table_name = os.environ.get("JOBS_TABLE_NAME")
    
    if not job_id:
        raise ValueError("JOB_ID environment variable is required")
    if not s3_bucket:
        raise ValueError("S3_BUCKET environment variable is required")
    if pfd_goal <= 0 or confidence_goal <= 0:
        raise ValueError("PFD_GOAL and CONFIDENCE_GOAL must be positive numbers")
    
    print(f"[CONFIG] JOB_ID: {job_id}")
    print(f"[CONFIG] PFD_GOAL: {pfd_goal}")
    print(f"[CONFIG] CONFIDENCE_GOAL: {confidence_goal}")
    print(f"[CONFIG] FAILURES: {failures}")
    print(f"[CONFIG] S3_BUCKET: {s3_bucket}")
    print(f"[CONFIG] AWS_REGION: {aws_region}")
    print(f"[CONFIG] BBN_INPUT_PATH: {bbn_input_path or 'default (nrc_report_data)'}")
    if bbn_input_bucket:
        print(f"[CONFIG] BBN_INPUT_BUCKET: {bbn_input_bucket}")
    
    dynamodb_client = None
    if jobs_table_name:
        dynamodb_client = boto3.client('dynamodb', region_name=aws_region)
    
    # Update DynamoDB status: RUNNING
    if jobs_table_name and dynamodb_client:
        try:
            dynamodb_client.update_item(
                TableName=jobs_table_name,
                Key={'jobId': {'S': job_id}},
                UpdateExpression='SET jobStatus = :s',
                ExpressionAttributeValues={':s': {'S': 'RUNNING'}}
            )
            print(f"[DynamoDB] Job status updated to RUNNING: {job_id}")
        except Exception as e:
            print(f"[WARNING] Failed to update DynamoDB status to RUNNING: {str(e)}")
    
    try:
        bbn_data = load_bayesian_data_from_env(
            bbn_input_path,
            bbn_input_bucket,
        )
        
        # Determine BBN input source for result metadata
        bbn_input_source = "default"
        bbn_input_info = {}
        if bbn_input_path and bbn_input_bucket:
            bbn_input_source = "s3"
            bbn_input_info = {
                "source": "s3",
                "bucket": bbn_input_bucket,
                "key": bbn_input_path
            }
        elif bbn_input_path:
            bbn_input_source = "local"
            bbn_input_info = {"source": "local", "path": bbn_input_path}
        else:
            bbn_input_info = {"source": "default", "description": "NRC report data (default)"}

        if test_mode:
            print("\n[TEST MODE] Skipping computation, using dummy values")
            print("[STEP 1] Trace generation skipped (TEST MODE)")
            print("[STEP 2] Sensitivity analysis skipped (TEST MODE)")
            print("[STEP 3] Full analysis skipped (TEST MODE)")
            demand_required = 99999
            prior_mean = pfd_goal
            prior_conf = confidence_goal
            pfd_output = [
                ["100", 99999],
                ["200", 99999],
                ["300", 99999],
                ["400", 99999],
                ["500", 99999],
            ]
            last_conf = 99999
            print(f"[STEP 2] Required number of tests (DUMMY): {demand_required}")
            print(f"[STEP 2] Prior mean (from input): {prior_mean}")
            print(f"[STEP 2] Prior confidence (from input): {prior_conf}")
            print(f"[STEP 3] Full analysis completed with dummy values")
        else:
            # Generate trace (composite model)
            print("\n[STEP 1] Generating composite model trace...")
            
            # TODO: modify the name of the function
            trace = run_example_for_composite_model(bbn_data)
            print("[STEP 1] Trace generation completed")
            
            # Sensitivity Analysis: calculate required demand
            print("\n[STEP 2] Running sensitivity analysis...")
            demand_required = get_number_of_required_demand(
                trace, pfd_goal=pfd_goal, confidence_goal=confidence_goal
            )
            print(f"[STEP 2] Required number of tests: {int(demand_required)}")
            
            # Trace preprocessing
            filtered_pfd_trace = filter_outsiders(trace.posterior["PFD"])
            prior_mean = trace.posterior["PFD"].mean().item()
            prior_conf = get_confidence(data=trace.posterior["PFD"], goal=pfd_goal)
            
            print(f"[STEP 2] Prior mean: {prior_mean}")
            print(f"[STEP 2] Prior confidence @goal: {prior_conf}")
            
            # Full Analysis: iterate through demand_list and sample
            print("\n[STEP 3] Running full analysis with demand list...")
            demand_list = list(range(500, int(demand_required) + 500, 500))
            pfd_output = []
            last_conf = None
            
            for idx, demand in enumerate(demand_list, 1):
                print(f"[STEP 3] Processing demand {idx}/{len(demand_list)}: {demand}")
                model = demand_model_func(
                    demand=demand, 
                    observed_failures=failures, 
                    pfd_trace=filtered_pfd_trace
                )
                updated_trace = run_sampling(model, draws=2000, tune=500)
                updated_mean = updated_trace.posterior["pfd_prior"].mean().item()
                last_conf = get_confidence(
                    data=updated_trace.posterior["pfd_prior"], goal=pfd_goal
                )
                pfd_output.append([str(demand), updated_mean])
                print(f"[STEP 3] Demand={demand} → PFD={updated_mean}, Confidence={last_conf}")
        
        # Build result JSON
        result_json = {
            "input": {
                "parameter": {
                    "test_count": int(demand_required),
                    "target": pfd_goal,
                    "prior": {
                        "distribution": "trace",
                        "mean": prior_mean,
                        "confidence": prior_conf,
                    },
                    "observed_failures": failures,
                },
                "bbn_input": bbn_input_info,
            },
            "output": {
                "pfd": pfd_output,
                "confidence": last_conf,
            },
        }
        
        # Upload to S3
        print("\n[STEP 4] Uploading results to S3...")
        s3_client = boto3.client('s3', region_name=aws_region)
        s3_key = f"results/full-analysis-{job_id}.json"
        
        s3_client.put_object(
            Bucket=s3_bucket,
            Key=s3_key,
            Body=json.dumps(result_json, indent=2),
            ContentType="application/json"
        )
        
        print(f"[STEP 4] Results uploaded to s3://{s3_bucket}/{s3_key}")
        
        # Update DynamoDB status: COMPLETED
        if jobs_table_name and dynamodb_client:
            try:
                dynamodb_client.update_item(
                    TableName=jobs_table_name,
                    Key={'jobId': {'S': job_id}},
                    UpdateExpression='SET jobStatus = :s, resultsPath = :p',
                    ExpressionAttributeValues={
                        ':s': {'S': 'COMPLETED'},
                        ':p': {'S': s3_key}
                    }
                )
                print(f"[DynamoDB] Job status updated to COMPLETED: {job_id}")
            except Exception as e:
                print(f"[WARNING] Failed to update DynamoDB status to COMPLETED: {str(e)}")
        
        print("\n" + "=" * 80)
        print("HybridTool Full Analysis - Completed Successfully")
        print("=" * 80)
        
        # Print result information (for CloudWatch Logs)
        print(json.dumps({
            "status": "completed",
            "job_id": job_id,
            "s3_location": f"s3://{s3_bucket}/{s3_key}",
            "demand_required": int(demand_required),
            "final_confidence": last_conf
        }))
        
    except Exception as e:
        error_msg = f"Full analysis failed: {str(e)}"
        print(f"\n[ERROR] {error_msg}", file=sys.stderr)
        
        # DynamoDB 상태 업데이트: FAILED
        if jobs_table_name and dynamodb_client:
            try:
                dynamodb_client.update_item(
                    TableName=jobs_table_name,
                    Key={'jobId': {'S': job_id}},
                    UpdateExpression='SET jobStatus = :s, errorMessage = :e',
                    ExpressionAttributeValues={
                        ':s': {'S': 'FAILED'},
                        ':e': {'S': error_msg[:500]}  # 최대 500자
                    }
                )
                print(f"[DynamoDB] Job status updated to FAILED: {job_id}")
            except Exception as db_error:
                print(f"[WARNING] Failed to update DynamoDB status to FAILED: {str(db_error)}")
        
        print(json.dumps({
            "status": "failed",
            "job_id": job_id,
            "error": error_msg
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()

