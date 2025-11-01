"""
Lambda Function: hybrid-tool-get-results

기능:
- REST API 요청 수신 (GET /api/v1/results/{job_id})
- JOB_ID로 S3에서 결과 조회
- 직접 JSON 반환 (presigned URL 문제 해결을 위해 Lambda에서 직접 반환)
"""

import json
import os
import boto3
from botocore.exceptions import ClientError
from datetime import timedelta

s3_client = boto3.client('s3', region_name=os.environ.get('AWS_REGION', 'ap-northeast-2'))

# 환경 변수
S3_BUCKET = os.environ.get('S3_BUCKET')
PRESIGNED_URL_EXPIRY = int(os.environ.get('PRESIGNED_URL_EXPIRY', '3600'))  # 기본 1시간


def handler(event, context):
    """
    Lambda 핸들러 함수
    
    요청:
    GET /api/v1/results/{job_id}?type={type} (REST API Gateway)
    - type: 'sensitivity-analysis' | 'update-pfd' | 'full-analysis'
    
    응답:
    {
        "statusCode": 200,
        "body": {
            "job_id": "uuid",
            "download_url": "https://presigned-url...",
            "status": "completed"
        }
    }
    """
    try:
        print(f"Received event: {json.dumps(event)}")
        
        # CORS Preflight 요청 처리 (OPTIONS 메서드)
        if event.get('httpMethod') == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,x-api-key',
                    'Content-Type': 'application/json'
                },
                'body': ''
            }
        
        if not S3_BUCKET:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'S3_BUCKET environment variable not set'
                })
            }
        
        # JOB_ID 추출
        job_id = None
        
        # 경로 파라미터에서 추출 (API Gateway 경로: /results/{job_id})
        # REST API / HTTP API v2 호환: pathParameters는 딕셔너리 또는 None
        if event.get('pathParameters'):
            # REST API와 HTTP API v2 모두에서 경로 파라미터 이름이 그대로 키로 사용됨
            # 경로가 /results/{job_id}라면 'job_id' 또는 다른 이름일 수 있음
            path_params = event['pathParameters']
            # 여러 가능한 파라미터 이름 시도 (REST API 호환)
            job_id = path_params.get('job_id') or path_params.get('jobId') or path_params.get('id')
        
        # 요청 본문에서 추출 (POST /results-url)
        if not job_id:
            try:
                if isinstance(event.get('body'), str):
                    body = json.loads(event['body'])
                else:
                    body = event.get('body', {})
                job_id = body.get('job_id') or body.get('jobId')
            except (json.JSONDecodeError, AttributeError):
                pass
        
        # 쿼리 파라미터에서 추출
        if not job_id and event.get('queryStringParameters'):
            job_id = event['queryStringParameters'].get('job_id') or event['queryStringParameters'].get('jobId')
        
        print(f"Extracted job_id: {job_id}")
        
        if not job_id:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'job_id is required',
                    'debug': {
                        'pathParameters': event.get('pathParameters'),
                        'queryStringParameters': event.get('queryStringParameters'),
                        'body': event.get('body')
                    }
                })
            }
        
        # 결과 타입 확인 (경로 파라미터, 쿼리 파라미터, 또는 요청 본문에서)
        result_type = None
        
        # 1. 쿼리 파라미터에서 확인 (가장 일반적: GET /results/{job_id}?type=sensitivity-analysis)
        if event.get('queryStringParameters'):
            result_type = event['queryStringParameters'].get('type')
        
        # 2. 경로 파라미터에서 확인
        if not result_type and event.get('pathParameters'):
            result_type = event['pathParameters'].get('type')
        
        # 3. 요청 본문에서 확인 (POST 요청)
        if not result_type:
            try:
                if isinstance(event.get('body'), str):
                    body = json.loads(event['body'])
                else:
                    body = event.get('body', {})
                result_type = body.get('type')
            except:
                pass
        
        # 기본값은 full-analysis
        result_type = result_type or 'full-analysis'
        print(f"Result type: {result_type}, S3_BUCKET: {S3_BUCKET}")
        
        # S3 경로 결정 (flattened: results/{endpoint}-{job_id}.json)
        if result_type == 'sensitivity-analysis':
            s3_key = f"results/sensitivity-analysis-{job_id}.json"
        elif result_type == 'update-pfd':
            s3_key = f"results/update-pfd-{job_id}.json"
        else:  # full-analysis
            s3_key = f"results/full-analysis-{job_id}.json"
        
        print(f"Checking S3 key: {s3_key}")
        
        # Lambda에서 S3 파일 직접 읽어서 반환 (CORS 문제 우회)
        try:
            print(f"Fetching S3 object: s3://{S3_BUCKET}/{s3_key}")
            
            # S3에서 파일 가져오기
            response = s3_client.get_object(Bucket=S3_BUCKET, Key=s3_key)
            file_content = response['Body'].read().decode('utf-8')
            
            # 모든 타입을 Lambda에서 직접 반환 (presigned URL 서명 문제 해결)
            if result_type == 'sensitivity-analysis':
                # sensitivity-analysis는 data 필드에 포함
                result_data = json.loads(file_content)
                print(f"Successfully fetched and parsed result for job_id: {job_id}")
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'job_id': job_id,
                        'status': 'completed',
                        'data': result_data,
                        's3_location': f's3://{S3_BUCKET}/{s3_key}'
                    })
                }
            else:
                # update-pfd, full-analysis: presigned URL 문제 해결을 위해 데이터 직접 반환
                result_data = json.loads(file_content)
                print(f"Successfully fetched result for job_id: {job_id}, returning data directly")
                
                return {
                    'statusCode': 200,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'job_id': job_id,
                        'status': 'completed',
                        'data': result_data,  # 데이터 직접 제공 (프론트엔드에서 blob URL 생성)
                        's3_location': f's3://{S3_BUCKET}/{s3_key}'
                    })
                }
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            print(f"S3 ClientError: {error_code}, {str(e)}")
            
            # 파일이 없으면 404 반환 (폴링 계속)
            if error_code == 'NoSuchKey' or error_code == '404':
                return {
                    'statusCode': 404,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'message': f'Results not found for job_id: {job_id}',
                        'job_id': job_id,
                        'status': 'not_found',
                        's3_key': s3_key
                    })
                }
            else:
                # 다른 에러는 500
                return {
                    'statusCode': 500,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'message': f'Failed to retrieve results: {str(e)}',
                        'error_code': error_code
                    })
                }
    
    except Exception as e:
        # 예상치 못한 모든 예외 처리
        error_msg = f'Unexpected error: {str(e)}'
        print(f"ERROR: {error_msg}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': error_msg,
                'error_type': type(e).__name__
            })
        }

