#!/usr/bin/env python3
"""
Common utility module for HybridTool Tasks

Shared functions used across all task types (sensitivity_analysis, update_pfd, full_analysis)
"""

import os
import sys
import json
import tempfile
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, Callable
import boto3

sys.path.insert(0, '/app/server')

from bbn_input_loader import load_bayesian_data_from_env


def get_base_config() -> Dict[str, Any]:
    """Read base common environment variables"""
    config = {
        "JOB_ID": os.environ.get("JOB_ID"),
        "PFD_GOAL": float(os.environ.get("PFD_GOAL", "0")),
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
        "THIN": int(os.environ.get("THIN", "1")),
    }
    
    # TODO(fix/test-mode): TEST_MODE와 TEST_OUTPUT_DIR이 잘못 묶여 있음.
    # 이 줄로 인해 TEST_MODE=true이면 자동으로 TEST_OUTPUT_DIR이 설정되어 S3 업로드가 건너뛰어짐.
    # 결과적으로 프론트엔드 폴링이 S3에서 결과를 찾지 못해 오류 발생.
    # 수정 방향: 이 자동 설정 줄을 제거하고, 로컬 Docker 테스트 스크립트에서
    # TEST_OUTPUT_DIR을 명시적으로 환경변수로 설정하도록 변경.
    if config["TEST_MODE"] and not config["TEST_OUTPUT_DIR"]:
        config["TEST_OUTPUT_DIR"] = os.path.join("tempDoc", "hybrid-tool-test")
    
    return config


def validate_base_config(config: Dict[str, Any]) -> None:
    """Validate base common configuration"""
    if not config["JOB_ID"]:
        raise ValueError("JOB_ID environment variable is required")
    if not config["S3_BUCKET"]:
        raise ValueError("S3_BUCKET environment variable is required")
    if config["PFD_GOAL"] <= 0:
        raise ValueError("PFD_GOAL must be a positive number")
    if config["DRAWS"] <= 0:
        raise ValueError("DRAWS must be a positive number")
    if config["TUNE"] < 0:
        raise ValueError("TUNE must be non-negative")
    if config["CHAINS"] <= 0:
        raise ValueError("CHAINS must be a positive number")
    if config["THIN"] <= 0:
        raise ValueError("THIN must be a positive number")


def print_base_config(config: Dict[str, Any]) -> None:
    """Print base configuration"""
    print(f"[CONFIG] JOB_ID: {config['JOB_ID']}")
    print(f"[CONFIG] PFD_GOAL: {config['PFD_GOAL']}")
    print(f"[CONFIG] S3_BUCKET: {config['S3_BUCKET']}")
    print(f"[CONFIG] AWS_REGION: {config['AWS_REGION']}")
    print(f"[CONFIG] BBN_INPUT_PATH: {config['BBN_INPUT_PATH'] or 'default (nrc_report_data)'}")
    if config['BBN_INPUT_BUCKET']:
        print(f"[CONFIG] BBN_INPUT_BUCKET: {config['BBN_INPUT_BUCKET']}")


def update_job_status(
    dynamodb_client: Any, 
    config: Dict[str, Any], 
    status: str, 
    s3_key: Optional[str] = None, 
    error_msg: Optional[str] = None
) -> None:
    """Update job status in DynamoDB"""
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
    """Load BBN data and generate input information"""
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


def upload_results_to_s3(
    config: Dict[str, Any], 
    result_json: Dict[str, Any],
    s3_key_prefix: str
) -> str:
    """Upload results to S3 or save locally"""
    job_id = config["JOB_ID"]
    s3_bucket = config["S3_BUCKET"]
    aws_region = config["AWS_REGION"]
    test_output_dir = config["TEST_OUTPUT_DIR"]
    
    s3_key = f"results/{s3_key_prefix}-{job_id}.json"
    
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
        print(f"[UPLOAD] Results uploaded to s3://{s3_bucket}/{s3_key}")
        return s3_key


def save_trace_to_s3(trace: Any, config: Dict[str, Any], job_id: str) -> str:
    """Save InferenceData trace to S3 as NetCDF (.nc) file"""
    import arviz as az

    s3_key = f"results/prior-trace-{job_id}.nc"
    s3_bucket = config["S3_BUCKET"]
    aws_region = config["AWS_REGION"]
    test_output_dir = config["TEST_OUTPUT_DIR"]

    with tempfile.NamedTemporaryFile(suffix=".nc", delete=False) as f:
        tmp_path = f.name

    try:
        az.to_netcdf(trace, tmp_path)

        if test_output_dir:
            output_path = Path(test_output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            local_file = output_path / s3_key.replace("/", "_")
            import shutil
            shutil.copy(tmp_path, local_file)
            print(f"[TEST MODE] Trace saved locally to {local_file}")
            return str(local_file)
        else:
            s3_client = boto3.client('s3', region_name=aws_region)
            s3_client.upload_file(tmp_path, s3_bucket, s3_key)
            print(f"[UPLOAD] Trace uploaded to s3://{s3_bucket}/{s3_key}")
            return s3_key
    finally:
        os.unlink(tmp_path)


def load_trace_from_s3(config: Dict[str, Any], trace_s3_key: str) -> Any:
    """Load InferenceData trace from S3 NetCDF (.nc) file"""
    import arviz as az

    s3_bucket = config["S3_BUCKET"]
    aws_region = config["AWS_REGION"]

    with tempfile.NamedTemporaryFile(suffix=".nc", delete=False) as f:
        tmp_path = f.name

    try:
        s3_client = boto3.client('s3', region_name=aws_region)
        s3_client.download_file(s3_bucket, trace_s3_key, tmp_path)
        print(f"[DOWNLOAD] Trace downloaded from s3://{s3_bucket}/{trace_s3_key}")
        trace = az.from_netcdf(tmp_path)
        # Force eager loading before deleting the temp file
        # (az.from_netcdf uses xarray lazy loading by default)
        for group_name in trace._groups:
            group = getattr(trace, group_name, None)
            if group is not None:
                group.load()
        return trace
    finally:
        os.unlink(tmp_path)


def handle_error_and_exit(
    e: Exception,
    config: Dict[str, Any], 
    dynamodb_client: Any,
    task_name: str
) -> None:
    """Handle error and exit"""
    job_id = config.get("JOB_ID", "unknown")
    error_msg = f"{task_name} failed: {str(e)}"
    print(f"\n[ERROR] {error_msg}", file=sys.stderr)

    # Update job status in DynamoDB: FAILED
    update_job_status(dynamodb_client, config, status='FAILED', error_msg=error_msg)
    
    print(json.dumps({
        "status": "failed",
        "job_id": job_id,
        "error": error_msg
    }))
    sys.exit(1)


def run_task(
    task_name: str,
    get_config_func: Callable[[], Dict[str, Any]],
    run_analysis_func: Callable[[Dict[str, Any], Any], Dict[str, Any]],
    build_result_json_func: Callable[[Dict[str, Any], Dict[str, Any], Dict[str, Any]], Dict[str, Any]],
    build_completion_payload_func: Callable[[Dict[str, Any], Dict[str, Any], str], Dict[str, Any]],
    s3_key_prefix: str,
    test_mode_dummy_func: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None
) -> None:
    """
    Common task execution flow (Template Method Pattern)
    
    Args:
        task_name: Task name (for logging)
        get_config_func: Function to read and validate environment variables
        run_analysis_func: Function to run actual analysis (config, bbn_data) -> result_metrics
        build_result_json_func: Function to build result JSON (config, result_metrics, bbn_input_info) -> result_json
        build_completion_payload_func: Function to build completion payload (config, result_metrics, s3_location) -> completion_payload
        s3_key_prefix: S3 key prefix (e.g., "full-analysis", "sensitivity-analysis")
        test_mode_dummy_func: Function to generate dummy data for test mode (optional)
    """
    print("=" * 80)
    print(f"HybridTool {task_name} - Starting")
    print("=" * 80)
    
    dynamodb_client = None
    config = {}
    
    try:
        # 1. Read environment variables and validate them
        config = get_config_func()
        
        # 2. Initialize DynamoDB client
        if config["JOBS_TABLE_NAME"]:
            dynamodb_client = boto3.client('dynamodb', region_name=config["AWS_REGION"])
            
        # 3. Update job status in DynamoDB: RUNNING
        update_job_status(dynamodb_client, config, status='RUNNING')
        
        # 4. Load BBN data and input information
        bbn_data, bbn_input_info = load_bbn_data_and_info(config)
        
        # 5. Run analysis (include handling for test mode)
        if config["TEST_MODE"]:
            print("\n[TEST MODE] Skipping computation, using dummy values")
            if test_mode_dummy_func:
                result_metrics = test_mode_dummy_func(config)
            else:
                raise ValueError("TEST_MODE requires test_mode_dummy_func")
        else:
            result_metrics = run_analysis_func(config, bbn_data)
        
        # 6. Build result JSON and upload to S3/Local
        result_json = build_result_json_func(config, result_metrics, bbn_input_info)
        s3_location = upload_results_to_s3(config, result_json, s3_key_prefix)
        
        # 7. Update job status in DynamoDB: COMPLETED
        s3_key_for_db = s3_location if not config["TEST_OUTPUT_DIR"] else None
        update_job_status(dynamodb_client, config, status='COMPLETED', s3_key=s3_key_for_db)
        
        # 8. Print completion payload
        print("\n" + "=" * 80)
        print(f"HybridTool {task_name} - Completed Successfully")
        print("=" * 80)
        
        completion_payload = build_completion_payload_func(config, result_metrics, s3_location)
        print(json.dumps(completion_payload))
        
    except Exception as e:
        handle_error_and_exit(e, config if 'config' in locals() else {}, dynamodb_client, task_name)

