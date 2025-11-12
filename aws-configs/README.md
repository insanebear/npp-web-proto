# AWS Resource Configuration Files

AWS resource definition files for HybridTool PyMC Fargate tasks

## File Structure

```
aws-configs/
├── hybridTool-task-definition.json  # ECS Task Definition
├── hybridTool-iam-policies.json     # IAM 역할 정책 예시
└── README.md
```

## ECS Task Definition

- **File**: `hybridTool-task-definition.json`
- **Family**: `hybrid-tool-pymc-task`
- **Resources**: 4 vCPU, 8GB memory
- **Network**: awsvpc mode (Fargate)

### Environment Variable Substitution

This JSON file uses environment variables. The following variables are required:
- `AWS_ACCOUNT_ID`: AWS account ID
- `AWS_REGION`: AWS region (default: ap-northeast-2)
- `ECR_REPOSITORY`: ECR repository name (default: hybrid-tool-pymc)
- `DOCKER_IMAGE_TAG`: Docker image tag (default: latest)

### Registration

Using deployment script (recommended):
```bash
# scripts/.hybridTool-env 파일에 환경 변수 설정 후
./scripts/deploy-hybridTool-task-definition.sh
```

For manual registration, environment variables must be substituted:
```bash
# envsubst를 사용하여 환경 변수 치환
envsubst < aws-configs/hybridTool-task-definition.json > /tmp/task-def.json
aws ecs register-task-definition \
  --cli-input-json file:///tmp/task-def.json \
  --region ap-northeast-2
```

## IAM Policies

The `hybridTool-iam-policies.json` file contains the following policies:

**Note**: This file also uses environment variables (`${AWS_ACCOUNT_ID}`, `${AWS_REGION}`).
Substitute environment variables or replace with actual values before applying IAM policies.

1. **taskExecutionRolePolicy**: Permissions for ECR image pull and CloudWatch Logs write
2. **taskRolePolicy**: Permissions for S3 result upload and CloudWatch Logs write
3. **lambdaTriggerRolePolicy**: Permissions for ECS Task execution
4. **lambdaGetResultsRolePolicy**: Permissions for S3 result retrieval

### IAM Role Creation

If roles do not exist:

```bash
# Task Execution Role
aws iam create-role \
  --role-name ecsTaskExecutionRole \
  --assume-role-policy-document file://<(echo '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ecs-tasks.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }')

aws iam put-role-policy \
  --role-name ecsTaskExecutionRole \
  --policy-name ecsTaskExecutionRolePolicy \
  --policy-document file://<(jq '.taskExecutionRolePolicy' aws-configs/hybridTool-iam-policies.json)

# Task Role
aws iam create-role \
  --role-name ecsTaskRole \
  --assume-role-policy-document file://<(echo '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "ecs-tasks.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }')

aws iam put-role-policy \
  --role-name ecsTaskRole \
  --policy-name ecsTaskRolePolicy \
  --policy-document file://<(jq '.taskRolePolicy' aws-configs/hybridTool-iam-policies.json)
```

## Resource Names

- **ECS Cluster**: `bayesian-cluster` (reusing existing)
- **ECR Repository**: `hybrid-tool-pymc`
- **Task Definition**: `hybrid-tool-pymc-task`
- **S3 Bucket**: `hybrid-tool-results`
- **CloudWatch Log Group**: `/ecs/npp-hybrid-tool`
- **Lambda Function 1**: `hybrid-tool-trigger-task`
- **Lambda Function 2**: `hybrid-tool-get-results`


