"""
Lambda Function: hybrid-tool-generate-presigned-url

기능:
- POST /api/v1/upload-url : 파일 업로드용 presigned PUT URL 생성
  body: { filename: str, content_type: str }
  response: { upload_url: str, s3_key: str, bucket: str }

- GET /api/v1/download-url?key=... : 파일 다운로드용 presigned GET URL 생성
  response: { download_url: str }

업로드 대상 prefix: uploads/temp/
S3 lifecycle 정책으로 uploads/temp/ prefix는 24시간 후 자동 삭제됨.
"""

import json
import os
import uuid
from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "ap-northeast-2"))

DEFAULT_BUCKET = os.environ.get("S3_BUCKET", "hybrid-tool-results")
UPLOAD_PREFIX = "uploads/temp/"
UPLOAD_URL_EXPIRY = 300   # 5 minutes
DOWNLOAD_URL_EXPIRY = 300  # 5 minutes

ALLOWED_CONTENT_TYPES = {
    "application/json",
    "application/octet-stream",
    "application/x-netcdf",
}

ALLOWED_EXTENSIONS = {".json", ".nc"}


def _response(status_code: int, body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "statusCode": status_code,
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,x-api-key",
            "Content-Type": "application/json",
        },
        "body": json.dumps(body),
    }


def _generate_upload_url(body: Dict[str, Any]) -> Dict[str, Any]:
    filename = body.get("filename", "")
    content_type = body.get("content_type", "application/octet-stream")

    if not filename:
        return _response(400, {"message": "filename is required"})

    # Validate extension
    ext = ""
    if "." in filename:
        ext = "." + filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return _response(400, {"message": f"File extension not allowed: {ext}. Allowed: {list(ALLOWED_EXTENSIONS)}"})

    # Sanitize filename
    safe_name = "".join(c for c in filename if c.isalnum() or c in "-_.")
    if not safe_name:
        safe_name = "upload"

    s3_key = f"{UPLOAD_PREFIX}{uuid.uuid4()}-{safe_name}"
    bucket = DEFAULT_BUCKET

    try:
        upload_url = s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": bucket,
                "Key": s3_key,
                "ContentType": content_type,
            },
            ExpiresIn=UPLOAD_URL_EXPIRY,
        )
        return _response(200, {
            "upload_url": upload_url,
            "s3_key": s3_key,
            "bucket": bucket,
        })
    except ClientError as e:
        print(f"[ERROR] generate_presigned_url (put): {e}")
        return _response(500, {"message": f"Failed to generate upload URL: {e}"})


def _generate_download_url(key: str) -> Dict[str, Any]:
    if not key:
        return _response(400, {"message": "key is required"})

    # Basic path traversal guard
    if ".." in key or key.startswith("/"):
        return _response(400, {"message": "Invalid key"})

    bucket = DEFAULT_BUCKET

    try:
        download_url = s3_client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": bucket,
                "Key": key,
            },
            ExpiresIn=DOWNLOAD_URL_EXPIRY,
        )
        return _response(200, {"download_url": download_url, "key": key, "bucket": bucket})
    except ClientError as e:
        error_code = e.response.get("Error", {}).get("Code", "Unknown")
        print(f"[ERROR] generate_presigned_url (get): {e}")
        if error_code in ("NoSuchKey", "404"):
            return _response(404, {"message": f"File not found: {key}"})
        return _response(500, {"message": f"Failed to generate download URL: {e}"})


def handler(event, context):
    try:
        http_method = event.get("httpMethod", "GET")

        if http_method == "OPTIONS":
            return _response(200, {})

        if http_method == "POST":
            raw_body = event.get("body") or "{}"
            try:
                body = json.loads(raw_body)
            except (json.JSONDecodeError, TypeError):
                body = {}
            return _generate_upload_url(body)

        if http_method == "GET":
            params = event.get("queryStringParameters") or {}
            key = params.get("key", "") if isinstance(params, dict) else ""
            return _generate_download_url(key)

        return _response(405, {"message": f"Method {http_method} not allowed"})

    except Exception as exc:
        print(f"[ERROR] Unexpected: {exc}")
        return _response(500, {"message": f"Unexpected error: {exc}"})
