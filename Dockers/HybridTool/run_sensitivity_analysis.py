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
import boto3
from typing import Dict, Any

sys.path.insert(0, '/app/server')

from bbn_inference.sensitivity_analysis import (
    get_number_of_required_demand,
    filter_outsiders,
    get_confidence,
)
from bbn_inference.examples.example_for_composite_model import run_example_for_composite_model


def main():
    print("=" * 80)
    print("HybridTool Sensitivity Analysis - Starting")
    print("=" * 80)
    
    # Read environment variables
    job_id = os.environ.get("JOB_ID")
    pfd_goal = float(os.environ.get("PFD_GOAL", "0"))
    confidence_goal = float(os.environ.get("CONFIDENCE_GOAL", "0"))
    s3_bucket = os.environ.get("S3_BUCKET")
    aws_region = os.environ.get("AWS_REGION", "ap-northeast-2")
    test_mode = os.environ.get("TEST_MODE", "false").lower() == "true"
    jobs_table_name = os.environ.get("JOBS_TABLE_NAME")
    
    dynamodb_client = None
    if jobs_table_name:
        dynamodb_client = boto3.client('dynamodb', region_name=aws_region)
    
    if not job_id:
        raise ValueError("JOB_ID environment variable is required")
    if not s3_bucket:
        raise ValueError("S3_BUCKET environment variable is required")
    if pfd_goal <= 0 or confidence_goal <= 0:
        raise ValueError("PFD_GOAL and CONFIDENCE_GOAL must be positive numbers")
    
    print(f"[CONFIG] JOB_ID: {job_id}")
    print(f"[CONFIG] PFD_GOAL: {pfd_goal}")
    print(f"[CONFIG] CONFIDENCE_GOAL: {confidence_goal}")
    print(f"[CONFIG] S3_BUCKET: {s3_bucket}")
    
    # DynamoDB 상태 업데이트: RUNNING
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
        if test_mode:
            print("\n[TEST MODE] Skipping computation, using dummy values")
            print("[STEP 1] Trace generation skipped (TEST MODE)")
            print("[STEP 2] Sensitivity analysis skipped (TEST MODE)")
            num_tests = 99999
            prior_mean = pfd_goal
            prior_conf = confidence_goal
            print(f"[STEP 2] Required number of tests (DUMMY): {num_tests}")
            print(f"[STEP 2] Prior mean (from input): {prior_mean}")
            print(f"[STEP 2] Prior confidence (from input): {prior_conf}")
        else:
            # Generate trace
            print("\n[STEP 1] Generating composite model trace...")
            trace = run_example_for_composite_model()
            print("[STEP 1] Trace generation completed")
            
            # 2. Sensitivity Analysis
            print("\n[STEP 2] Running sensitivity analysis...")
            num_tests = get_number_of_required_demand(
                trace, pfd_goal=pfd_goal, confidence_goal=confidence_goal
            )
            print(f"[STEP 2] Required number of tests: {int(num_tests)}")
            prior_mean = trace.posterior["PFD"].mean().item()
            prior_conf = get_confidence(data=trace.posterior["PFD"], goal=pfd_goal)
            
            print(f"[STEP 2] Prior mean: {prior_mean}")
            print(f"[STEP 2] Prior confidence @goal: {prior_conf}")
        
        # Build result JSON
        result_json = {
            "message": "Sensitivity analysis complete",
            "data": {
                "num_tests": int(num_tests),
                "prior_mean": prior_mean,
                "prior_confidence": prior_conf,
            },
        }
        
        # Upload to S3
        print("\n[STEP 3] Uploading results to S3...")
        s3_client = boto3.client('s3', region_name=aws_region)
        s3_key = f"results/sensitivity-analysis-{job_id}.json"
        
        s3_client.put_object(
            Bucket=s3_bucket,
            Key=s3_key,
            Body=json.dumps(result_json, indent=2),
            ContentType="application/json"
        )
        
        print(f"[STEP 3] Results uploaded to s3://{s3_bucket}/{s3_key}")
        
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
        print("HybridTool Sensitivity Analysis - Completed Successfully")
        print("=" * 80)
        
        print(json.dumps({
            "status": "completed",
            "job_id": job_id,
            "s3_location": f"s3://{s3_bucket}/{s3_key}",
            "num_tests": int(num_tests)
        }))
        
    except Exception as e:
        error_msg = f"Sensitivity analysis failed: {str(e)}"
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

