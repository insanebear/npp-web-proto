"""
Lambda Function: hybrid-tool-get-job-status

기능:
- REST API 요청 수신 (GET /api/v1/jobs/{job_id})
- job_id로 DynamoDB에서 작업 상태 조회
- BayesianPage와 동일한 API 스키마 제공
"""

import json
import os
import boto3
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'ap-northeast-2'))

# 환경 변수
JOBS_TABLE_NAME = os.environ.get('JOBS_TABLE_NAME')


def handler(event, context):
    """
    Lambda 핸들러 함수
    
    요청:
    GET /api/v1/jobs/{job_id} (REST API Gateway)
    
    응답:
    {
        "jobId": "uuid",
        "jobType": "sensitivity-analysis",
        "jobStatus": "PENDING" | "RUNNING" | "COMPLETED" | "FAILED",
        "createdAt": "2025-11-01T12:00:00",
        "resultsPath": "s3://bucket/path" (optional),
        "errorMessage": "error message" (optional)
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
        
        if not JOBS_TABLE_NAME:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'JOBS_TABLE_NAME environment variable not set'
                })
            }
        
        # job_id 추출
        job_id = None
        
        # 경로 파라미터에서 추출 (API Gateway 경로: /jobs/{job_id})
        # REST API / HTTP API v2 호환: pathParameters는 딕셔너리 또는 None
        if event.get('pathParameters'):
            path_params = event['pathParameters']
            # 여러 가능한 파라미터 이름 시도 (REST API 호환)
            job_id = path_params.get('job_id') or path_params.get('jobId') or path_params.get('id')
        
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
                        'queryStringParameters': event.get('queryStringParameters')
                    }
                })
            }
        
        # DynamoDB에서 조회
        try:
            table = dynamodb.Table(JOBS_TABLE_NAME)
            response = table.get_item(Key={'jobId': job_id})
            
            if 'Item' not in response:
                return {
                    'statusCode': 404,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'message': f'Job not found: {job_id}'
                    })
                }
            
            item = response['Item']
            
            # BayesianPage 스키마에 맞춰 반환 (jobId, jobStatus 필드)
            result = {
                'jobId': item.get('jobId', job_id),
                'jobType': item.get('jobType', 'unknown'),
                'jobStatus': item.get('jobStatus', 'UNKNOWN'),
            }
            
            # 선택적 필드 추가
            if 'createdAt' in item:
                result['createdAt'] = item['createdAt']
            if 'resultsPath' in item:
                result['resultsPath'] = item['resultsPath']
            if 'errorMessage' in item:
                result['errorMessage'] = item['errorMessage']
            # BBN 입력 정보 추가
            bbn_input_meta = {}
            if 'bbnInputBucket' in item and item['bbnInputBucket']:
                bbn_input_meta['bucket'] = item['bbnInputBucket']
            if 'bbnInputKey' in item and item['bbnInputKey']:
                bbn_input_meta['key'] = item['bbnInputKey']
            if bbn_input_meta:
                bbn_input_meta['source'] = 's3'
                result['bbnInput'] = bbn_input_meta
            elif not bbn_input_meta:
                result['bbnInput'] = {'source': 'default', 'description': 'NRC report data (default)'}
            
            print(f"Successfully retrieved job status: {job_id} -> {result['jobStatus']}")
            
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps(result)
            }
            
        except ClientError as e:
            error_code = e.response.get('Error', {}).get('Code', 'Unknown')
            print(f"DynamoDB ClientError: {error_code}, {str(e)}")
            
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': f'Failed to retrieve job status: {str(e)}',
                    'error_code': error_code
                })
            }
    
    except Exception as e:
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

