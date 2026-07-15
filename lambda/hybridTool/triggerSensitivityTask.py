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

# 환경 변수 (기본값, handler에서 stage에 따라 오버라이드)
CLUSTER_NAME = os.environ.get('CLUSTER_NAME')
TASK_DEFINITION = os.environ.get('HYBRID_TASK_DEFINITION')
SUBNET_IDS = os.environ.get('SUBNET_IDS', '').split(',') if os.environ.get('SUBNET_IDS') else []
SECURITY_GROUP_IDS = os.environ.get('SECURITY_GROUP_IDS', '').split(',') if os.environ.get('SECURITY_GROUP_IDS') else []
CONTAINER_NAME = os.environ.get('CONTAINER_NAME', 'hybrid-tool-container')
S3_BUCKET = os.environ.get('S3_BUCKET')
AWS_REGION = os.environ.get('AWS_REGION', 'ap-northeast-2')
JOBS_TABLE_NAME = os.environ.get('JOBS_TABLE_NAME')


def get_stage_from_event(event):
    """API Gateway event에서 stage 정보 추출"""
    stage = event.get('requestContext', {}).get('stage')
    if stage:
        return stage
    path = event.get('path', '')
    if path.startswith('/develop/'):
        return 'develop'
    elif path.startswith('/prod/'):
        return 'prod'
    return 'prod'


def get_resource_config(stage):
    """Stage에 따라 사용할 리소스 설정 반환"""
    if stage == 'develop':
        return {
            'cluster_name': os.environ.get('CLUSTER_NAME_DEV') or os.environ.get('CLUSTER_NAME'),
            'task_definition': os.environ.get('HYBRID_TASK_DEFINITION_DEV') or os.environ.get('HYBRID_TASK_DEFINITION'),
        }
    else:
        return {
            'cluster_name': os.environ.get('CLUSTER_NAME'),
            'task_definition': os.environ.get('HYBRID_TASK_DEFINITION'),
        }


def handler(event, context):
    """
    요청 본문:
    {
        "pfd_goal": 0.0001,
        "confidence_goal": 0.95,
        "demand": 0,      # (optional) 지금까지 수행한 테스트 수
        "failures": 0     # (optional) 지금까지 관측된 실패 수
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
        # Stage 감지 및 리소스 설정
        stage = get_stage_from_event(event)
        resource_config = get_resource_config(stage)
        cluster_name = resource_config['cluster_name']
        task_definition = resource_config['task_definition']
        
        print(f"Detected stage: {stage}, using cluster: {cluster_name}, task: {task_definition}")
        
        # 환경 변수 검증
        missing_vars = []
        if not cluster_name:
            missing_vars.append('CLUSTER_NAME' + ('_DEV' if stage == 'develop' else ''))
        if not task_definition:
            missing_vars.append('HYBRID_TASK_DEFINITION' + ('_DEV' if stage == 'develop' else ''))
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
            demand = int(body.get('demand', 0))
            failures = int(body.get('failures', 0))
            test_mode = body.get('test_mode', False)
            bbn_input_s3_bucket = body.get('bbn_input_s3_bucket')
            bbn_input_s3_key = body.get('bbn_input_s3_key')
            bbn_job_id = body.get('bbn_job_id')
            # 업로드 탭에서 직접 전달된 prior trace S3 키 (없으면 bbn_job_id로 추론)
            prior_trace_s3_key = body.get('prior_trace_s3_key')
            # bbn_job_id가 없으면 bbn_input_s3_key에서 파싱 (예: results/results-{jobId}.json)
            if not bbn_job_id and bbn_input_s3_key:
                import re
                match = re.search(r'results-([^/]+)\.json$', bbn_input_s3_key)
                if match:
                    bbn_job_id = match.group(1)
            settings = body.get('settings', {})
            
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

            if demand < 0 or failures < 0 or failures > demand:
                return {
                    'statusCode': 400,
                    'headers': {
                        'Access-Control-Allow-Origin': '*',
                        'Content-Type': 'application/json'
                    },
                    'body': json.dumps({
                        'message': 'demand and failures must be non-negative, and failures cannot exceed demand'
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
                        'demand': str(demand),
                        'failures': str(failures),
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
            {'name': 'DEMAND', 'value': str(demand)},
            {'name': 'FAILURES', 'value': str(failures)},
            {'name': 'S3_BUCKET', 'value': S3_BUCKET},
            {'name': 'AWS_REGION', 'value': AWS_REGION},
            {'name': 'TEST_MODE', 'value': 'true' if test_mode else 'false'},
            {'name': 'JOBS_TABLE_NAME', 'value': JOBS_TABLE_NAME or ''},
            {'name': 'DRAWS', 'value': str(settings.get('draws', 1000))},
            {'name': 'TUNE', 'value': str(settings.get('tune', 100))},
            {'name': 'CHAINS', 'value': str(settings.get('chains', 4))},
            {'name': 'THIN', 'value': str(settings.get('thin', 1))},
        ]

        if bbn_input_s3_key:
            environment_overrides.append({'name': 'BBN_INPUT_PATH', 'value': bbn_input_s3_key})
        if bbn_input_s3_bucket:
            environment_overrides.append({'name': 'BBN_INPUT_BUCKET', 'value': bbn_input_s3_bucket})
        # prior_trace_s3_key: 직접 전달된 키 우선, 없으면 bbn_job_id로 추론
        resolved_trace_key = prior_trace_s3_key or (f'results/bbn/prior-trace-{bbn_job_id}.nc' if bbn_job_id else None)
        if resolved_trace_key:
            environment_overrides.append({'name': 'PRIOR_TRACE_S3_KEY', 'value': resolved_trace_key})

        response = ecs_client.run_task(
            cluster=cluster_name,
            taskDefinition=task_definition,
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
