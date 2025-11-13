#!/usr/bin/env python3
"""
ECS Fargate Task: Update PFD

Environment variables:
- JOB_ID: Job identifier
- PFD_GOAL: Target PFD value
- DEMAND: Number of tests
- FAILURES: Observed number of failures
- S3_BUCKET: S3 bucket name for results
- AWS_REGION: AWS region

Output:
- Uploads JSON to S3: s3://{S3_BUCKET}/results/update-pfd-{JOB_ID}.json
"""

import os
import sys
import json
import boto3

sys.path.insert(0, '/app/server')

from bbn_inference.sensitivity_analysis import (
    filter_outsiders,
    get_confidence,
    demand_model_func,
)
from bbn_inference.examples.example_for_composite_model import run_example_for_composite_model
from bbn_inference.bbn_utils import run_sampling
from bbn_input_loader import load_bayesian_data_from_env


def main():
    print("=" * 80)
    print("HybridTool Update PFD - Starting")
    print("=" * 80)
    
    # Read environment variables
    job_id = os.environ.get("JOB_ID")
    pfd_goal = float(os.environ.get("PFD_GOAL", "0"))
    demand = int(os.environ.get("DEMAND", "0"))
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
    if pfd_goal <= 0:
        raise ValueError("PFD_GOAL must be a positive number")
    if demand <= 0:
        raise ValueError("DEMAND must be a positive number")
    if failures < 0:
        raise ValueError("FAILURES must be non-negative")
    if failures > demand:
        raise ValueError("failures cannot exceed demand")
    
    print(f"[CONFIG] JOB_ID: {job_id}")
    print(f"[CONFIG] PFD_GOAL: {pfd_goal}")
    print(f"[CONFIG] DEMAND: {demand}")
    print(f"[CONFIG] FAILURES: {failures}")
    print(f"[CONFIG] S3_BUCKET: {s3_bucket}")
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

        if test_mode:
            print("\n[TEST MODE] Skipping computation, using dummy values")
            print("[STEP 1] Trace generation skipped (TEST MODE)")
            print("[STEP 2] Trace preprocessing skipped (TEST MODE)")
            print("[STEP 3] PFD update sampling skipped (TEST MODE)")
            prior_mean = pfd_goal
            before_conf = 0.95
            updated_pfd_mean = 99999
            updated_conf = 99999
            print(f"[STEP 2] Prior mean (from input): {prior_mean}")
            print(f"[STEP 2] Prior confidence (dummy): {before_conf}")
            print(f"[STEP 3] Updated PFD mean (DUMMY): {updated_pfd_mean}")
            print(f"[STEP 3] Updated confidence (DUMMY): {updated_conf}")
        else:
            # Generate trace
            print("\n[STEP 1] Generating composite model trace...")
            trace = run_example_for_composite_model(bbn_data)
            print("[STEP 1] Trace generation completed")
            
            # Trace preprocessing
            filtered_pfd_trace = filter_outsiders(trace.posterior["PFD"])
            prior_mean = trace.posterior["PFD"].mean().item()
            before_conf = get_confidence(data=trace.posterior["PFD"], goal=pfd_goal)
            
            print(f"[STEP 2] Prior mean: {prior_mean}")
            print(f"[STEP 2] Prior confidence @goal: {before_conf}")
            
            # PFD update (sampling)
            print("\n[STEP 3] Running PFD update sampling...")
            model = demand_model_func(
                demand=demand,
                observed_failures=failures,
                pfd_trace=filtered_pfd_trace,
            )
            updated_trace = run_sampling(model, draws=2000, tune=500)
            
            updated_pfd_mean = updated_trace.posterior["pfd_prior"].mean().item()
            updated_conf = get_confidence(
                data=updated_trace.posterior["pfd_prior"], goal=pfd_goal
            )
            
            print(f"[STEP 3] Updated PFD mean: {updated_pfd_mean}")
            print(f"[STEP 3] Updated confidence @goal: {updated_conf}")
        
        # Build result JSON
        result_json = {
            "message": "PFD updated",
            "data": {
                "updated_pfd": updated_pfd_mean,
                "updated_confidence": updated_conf,
                "prior_mean": prior_mean,
                "prior_confidence": before_conf,
            },
            "bbn_input": bbn_input_info,
        }
        
        # Upload to S3
        print("\n[STEP 4] Uploading results to S3...")
        s3_client = boto3.client('s3', region_name=aws_region)
        s3_key = f"results/update-pfd-{job_id}.json"
        
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
        print("HybridTool Update PFD - Completed Successfully")
        print("=" * 80)
        
        print(json.dumps({
            "status": "completed",
            "job_id": job_id,
            "s3_location": f"s3://{s3_bucket}/{s3_key}",
            "updated_pfd": updated_pfd_mean,
            "updated_confidence": updated_conf
        }))
        
    except Exception as e:
        error_msg = f"Update PFD failed: {str(e)}"
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

