"""
Lambda Function: hybrid-tool-list-bbn-results

기능:
- REST API 요청 수신 (GET /api/v1/results)
- S3 버킷의 BBN 결과 JSON 파일 목록을 반환
- key 쿼리 파라미터가 있으면 해당 파일의 내용을 반환

스테이지 분기:
- develop: BBN_RESULTS_BUCKET_DEV / BBN_RESULTS_PREFIX_DEV (기본: hybrid-tool-results / results/bbn/)
- prod:    BBN_RESULTS_BUCKET     / BBN_RESULTS_PREFIX     (기본: bayesian-simulation-results-bucket / results/)
"""

import json
import os
from typing import Dict, Any, List, Optional, Tuple

import boto3
from botocore.exceptions import ClientError
from datetime import datetime

s3_client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "ap-northeast-2"))

# 프로덕션 기본값 (아직 구버킷 사용)
DEFAULT_BUCKET_PROD = "bayesian-simulation-results-bucket"
DEFAULT_PREFIX_PROD = "results/"

# 개발 기본값 (새 버킷 / 하위 폴더)
DEFAULT_BUCKET_DEV = "hybrid-tool-results"
DEFAULT_PREFIX_DEV = "results/bbn/"


def _response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,x-api-key",
            "Content-Type": "application/json",
        },
        "body": json.dumps(body, default=_json_serializer),
    }


def _json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def _get_stage(event: Dict[str, Any]) -> str:
    stage = event.get("requestContext", {}).get("stage", "")
    if stage:
        return stage
    path = event.get("path", "")
    if path.startswith("/develop/"):
        return "develop"
    return "prod"


def _get_bucket_and_prefix(stage: str) -> Tuple[str, str]:
    if stage == "develop":
        bucket = os.environ.get("BBN_RESULTS_BUCKET_DEV", DEFAULT_BUCKET_DEV)
        prefix = os.environ.get("BBN_RESULTS_PREFIX_DEV", DEFAULT_PREFIX_DEV)
    else:
        bucket = os.environ.get("BBN_RESULTS_BUCKET", DEFAULT_BUCKET_PROD)
        prefix = os.environ.get("BBN_RESULTS_PREFIX", DEFAULT_PREFIX_PROD)

    if prefix and not prefix.endswith("/"):
        prefix = prefix + "/"
    return bucket, prefix


def _list_files(bucket: str, prefix: str, limit: int) -> Dict[str, Any]:
    paginator = s3_client.get_paginator("list_objects_v2")
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)

    items: List[Dict[str, Any]] = []
    for page in page_iterator:
        for obj in page.get("Contents", []):
            key = obj.get("Key")
            if not key or key.endswith("/"):
                continue
            if prefix and key.startswith(prefix):
                relative_key = key[len(prefix):]
            else:
                relative_key = key
            if relative_key.startswith("/"):
                continue
            if "//" in relative_key:
                continue
            relative_key = relative_key.lstrip("/")
            if not relative_key:
                continue
            if "/" in relative_key:
                # 하위 폴더 객체 제외
                continue
            if not relative_key.lower().endswith(".json"):
                continue
            items.append(
                {
                    "key": key,
                    "name": relative_key,
                    "size": obj.get("Size"),
                    "last_modified": obj.get("LastModified"),
                }
            )
            if len(items) >= limit:
                break
        if len(items) >= limit:
            break

    return {
        "bucket": bucket,
        "prefix": prefix,
        "count": len(items),
        "items": items,
    }


def _get_file(bucket: str, prefix: str, key: str) -> Dict[str, Any]:
    normalized_key = key
    if prefix and not key.startswith(prefix):
        normalized_key = prefix + key

    if ".." in normalized_key or normalized_key.startswith("/"):
        raise ValueError("Invalid key")

    try:
        obj = s3_client.get_object(Bucket=bucket, Key=normalized_key)
        content = obj["Body"].read().decode("utf-8")
        data = json.loads(content)
        return {
            "bucket": bucket,
            "key": normalized_key,
            "size": obj.get("ContentLength"),
            "last_modified": obj.get("LastModified"),
            "data": data,
        }
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        if error_code in ("NoSuchKey", "404"):
            return {
                "error": "not_found",
                "message": f"File not found: {normalized_key}",
            }
        raise


def handler(event, context):
    try:
        http_method = event.get("httpMethod", "GET")
        if http_method == "OPTIONS":
            return _response(200, {})

        if http_method != "GET":
            return _response(405, {"message": f"Method {http_method} not allowed"})

        stage = _get_stage(event)
        bucket, prefix = _get_bucket_and_prefix(stage)
        print(f"[CONFIG] stage={stage}, bucket={bucket}, prefix={prefix}")

        params: Optional[Dict[str, Any]] = event.get("queryStringParameters") or {}
        key = params.get("key") if isinstance(params, dict) else None
        limit_param = params.get("limit") if isinstance(params, dict) else None

        if key:
            try:
                file_result = _get_file(bucket, prefix, key)
                if "error" in file_result:
                    return _response(404, file_result)
                return _response(200, file_result)
            except ValueError as ve:
                return _response(400, {"message": str(ve)})
            except ClientError as ce:
                error_code = ce.response.get("Error", {}).get("Code", "Unknown")
                return _response(502, {"message": f"S3 error: {error_code}"})

        try:
            limit = int(limit_param) if limit_param else 100
        except (TypeError, ValueError):
            limit = 100

        if limit <= 0:
            limit = 1
        if limit > 500:
            limit = 500

        result = _list_files(bucket, prefix, limit)
        return _response(200, result)

    except Exception as exc:
        print(f"[ERROR] {exc}")
        return _response(500, {"message": f"Unexpected error: {exc}"})
