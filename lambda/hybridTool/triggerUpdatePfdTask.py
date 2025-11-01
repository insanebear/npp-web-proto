"""
Lambda Function: hybrid-tool-trigger-update-pfd-task

기능:
- API Gateway 요청 수신 (REST API: POST /api/v1/update-pfd)
- 입력 파라미터 검증
- ECS Fargate Task 실행 (update PFD)
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
        "demand": 1000,
        "failures": 0
    }
    """
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
        demand = int(body.get('demand', 0))
        failures = int(body.get('failures', 0))
        test_mode = body.get('test_mode', False)
        
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
        
        if demand <= 0:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'demand must be a positive number'
                })
            }
        
        if failures < 0:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'failures must be non-negative'
                })
            }
        
        if failures > demand:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'failures cannot exceed demand'
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
    
    print(f"Starting ECS Task for update PFD, job_id: {job_id}")
    
    # DynamoDB에 작업 상태 저장 (PENDING)
    if JOBS_TABLE_NAME:
        try:
            table = dynamodb.Table(JOBS_TABLE_NAME)
            table.put_item(
                Item={
                    'jobId': job_id,
                    'jobType': 'update-pfd',
                    'jobStatus': 'PENDING',
                    'createdAt': datetime.utcnow().isoformat(),
                    'pfdGoal': str(pfd_goal),
                    'demand': str(demand),
                    'failures': str(failures),
                    'testMode': str(test_mode).lower()
                }
            )
            print(f"Job status saved to DynamoDB: {job_id}")
        except Exception as e:
            print(f"WARNING: Failed to save job status to DynamoDB: {str(e)}")
    
    # ECS Task 실행
    try:
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
        
        response = ecs_client.run_task(
            cluster=CLUSTER_NAME,
            taskDefinition=TASK_DEFINITION,
            launchType='FARGATE',
            networkConfiguration=network_config,
            overrides={
                'containerOverrides': [{
                    'name': CONTAINER_NAME,
                    'environment': [
                        {'name': 'TASK_TYPE', 'value': 'update_pfd'},
                        {'name': 'JOB_ID', 'value': job_id},
                        {'name': 'PFD_GOAL', 'value': str(pfd_goal)},
                        {'name': 'DEMAND', 'value': str(demand)},
                        {'name': 'FAILURES', 'value': str(failures)},
                        {'name': 'S3_BUCKET', 'value': S3_BUCKET},
                        {'name': 'AWS_REGION', 'value': AWS_REGION},
                        {'name': 'TEST_MODE', 'value': 'true' if test_mode else 'false'},
                        {'name': 'JOBS_TABLE_NAME', 'value': JOBS_TABLE_NAME or ''}
                    ]
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

