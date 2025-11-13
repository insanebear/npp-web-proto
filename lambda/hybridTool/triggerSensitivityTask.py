"""
Lambda Function: hybrid-tool-trigger-sensitivity-task

기능:
- API Gateway 요청 수신 (REST API: POST /api/v1/sensitivity-analysis)
- 입력 파라미터 검증
- ECS Fargate Task 실행 (sensitivity analysis)
- JOB_ID 반환
"""

import json
import os
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

ecs_client = boto3.client('ecs', region_name=os.environ.get('AWS_REGION', 'ap-northeast-2'))
dynamodb = boto3.resource('dynamodb', region_name=os.environ.get('AWS_REGION', 'ap-northeast-2'))

# 환경 변수
CLUSTER_NAME = os.environ.get('CLUSTER_NAME')
TASK_DEFINITION = os.environ.get('TASK_DEFINITION')
SUBNET_IDS = os.environ.get('SUBNET_IDS', '').split(',') if os.environ.get('SUBNET_IDS') else []
SECURITY_GROUP_IDS = os.environ.get('SECURITY_GROUP_IDS', '').split(',') if os.environ.get('SECURITY_GROUP_IDS') else []
CONTAINER_NAME = os.environ.get('CONTAINER_NAME', 'hybrid-tool-container')
S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_REGION = os.environ.get('AWS_REGION', 'ap-northeast-2')
JOBS_TABLE_NAME = os.environ.get('JOBS_TABLE_NAME')


def handler(event, context):
    """
    요청 본문:
    {
        "pfd_goal": 0.0001,
        "confidence_goal": 0.95
    }
    """
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
    
    try:
        # 환경 변수 검증
        missing_vars = []
        if not CLUSTER_NAME:
            missing_vars.append('CLUSTER_NAME')
        if not TASK_DEFINITION:
            missing_vars.append('TASK_DEFINITION')
        if not S3_BUCKET:
            missing_vars.append('S3_BUCKET')
        if not SUBNET_IDS or SUBNET_IDS == ['']:
            missing_vars.append('SUBNET_IDS')
        
        if missing_vars:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': f'Missing environment variables: {", ".join(missing_vars)}'
                })
            }
        
        # 요청 본문 파싱
        try:
            if isinstance(event.get('body'), str):
                body = json.loads(event['body'])
            else:
                body = event.get('body', {})
            
            pfd_goal = float(body.get('pfd_goal', 0))
            confidence_goal = float(body.get('confidence_goal', 0))
            test_mode = body.get('test_mode', False)
            bbn_input_s3_bucket = body.get('bbn_input_s3_bucket')
            bbn_input_s3_key = body.get('bbn_input_s3_key')
            
            # 입력 검증
            if pfd_goal <= 0:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'message': 'pfd_goal must be a positive number'
                    })
                }
            
            if not (0 < confidence_goal < 1):
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'message': 'confidence_goal must be between 0 and 1'
                    })
                }
        
        except (ValueError, TypeError) as e:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': f'Invalid request body: {str(e)}'
                })
            }
        
        # JOB_ID 생성
        import uuid
        job_id = str(uuid.uuid4())
        
        print(f"Starting ECS Task for sensitivity analysis, job_id: {job_id}")
        print(f"BBN Input - S3 Bucket: {bbn_input_s3_bucket or 'None'}, S3 Key: {bbn_input_s3_key or 'None'}")
        
        # DynamoDB에 작업 상태 저장 (PENDING)
        if JOBS_TABLE_NAME:
            try:
                table = dynamodb.Table(JOBS_TABLE_NAME)
                table.put_item(
                    Item={
                        'jobId': job_id,
                        'jobType': 'sensitivity-analysis',
                        'jobStatus': 'PENDING',
                        'createdAt': datetime.utcnow().isoformat(),
                        'pfdGoal': str(pfd_goal),
                        'confidenceGoal': str(confidence_goal),
                        'testMode': str(test_mode).lower(),
                        'bbnInputBucket': bbn_input_s3_bucket or '',
                        'bbnInputKey': bbn_input_s3_key or ''
                    }
                )
                print(f"Job status saved to DynamoDB: {job_id}")
            except Exception as e:
                print(f"WARNING: Failed to save job status to DynamoDB: {str(e)}")
        
        # ECS Task 실행
        network_config = {
            'awsvpcConfiguration': {
                'subnets': [s.strip() for s in SUBNET_IDS if s.strip()],
                'assignPublicIp': 'ENABLED'
            }
        }
        
        if SECURITY_GROUP_IDS and SECURITY_GROUP_IDS != ['']:
            network_config['awsvpcConfiguration']['securityGroups'] = [
                sg.strip() for sg in SECURITY_GROUP_IDS if sg.strip()
            ]
        
        environment_overrides = [
            {'name': 'TASK_TYPE', 'value': 'sensitivity_analysis'},
            {'name': 'JOB_ID', 'value': job_id},
            {'name': 'PFD_GOAL', 'value': str(pfd_goal)},
            {'name': 'CONFIDENCE_GOAL', 'value': str(confidence_goal)},
            {'name': 'S3_BUCKET', 'value': S3_BUCKET},
            {'name': 'AWS_REGION', 'value': AWS_REGION},
            {'name': 'TEST_MODE', 'value': 'true' if test_mode else 'false'},
            {'name': 'JOBS_TABLE_NAME', 'value': JOBS_TABLE_NAME or ''}
        ]

        if bbn_input_s3_key:
            environment_overrides.append({'name': 'BBN_INPUT_PATH', 'value': bbn_input_s3_key})
        if bbn_input_s3_bucket:
            environment_overrides.append({'name': 'BBN_INPUT_BUCKET', 'value': bbn_input_s3_bucket})

        response = ecs_client.run_task(
            cluster=CLUSTER_NAME,
            taskDefinition=TASK_DEFINITION,
            launchType='FARGATE',
            networkConfiguration=network_config,
            overrides={
                'containerOverrides': [{
                    'name': CONTAINER_NAME,
                    'environment': environment_overrides
                }]
            }
        )
        
        task_arn = response['tasks'][0]['taskArn']
        print(f"ECS Task started: {task_arn}")
        
        return {
            'statusCode': 202,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': 'Job accepted for processing',
                'job_id': job_id,
                'task_arn': task_arn
            })
        }
        
    except ClientError as e:
        error_msg = f"Failed to start ECS task: {str(e)}"
        print(f"ERROR: {error_msg}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': error_msg
            })
        }
    except Exception as e:
        # 모든 예외를 잡아서 로그 출력
        import traceback
        error_msg = f"Unexpected error: {str(e)}"
        print(f"ERROR: {error_msg}")
        print(f"Traceback: {traceback.format_exc()}")
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({
                'message': f'Internal server error: {error_msg}',
                'error_type': type(e).__name__
            })
        }
