#!/usr/bin/env bash
# 개발용 HybridTool Task Definition 등록 스크립트
# dev 태그를 사용하는 개발용 Task Definition을 생성합니다.
# 사용법: ./scripts/deploy/hybridTool/deploy-hybridTool-task-definition-dev.sh

set -euo pipefail

# 프로젝트 루트로 이동 (스크립트 위치 기준)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

# 환경 변수 설정 파일이 있으면 로드
CONFIG_FILE="scripts/config/.nppswrel-env"
if [ -f "$CONFIG_FILE" ]; then
  set -a
  . "$CONFIG_FILE"
  set +a
fi

# 환경 변수 확인
: "${AWS_REGION:=ap-northeast-2}"
: "${AWS_PROFILE:=default}"
: "${ECR_REPOSITORY:=hybrid-tool-pymc}"
# Dev script always uses dev image tag (DOCKER_IMAGE_TAG_DEV takes priority, then dev default)
# config의 DOCKER_IMAGE_TAG가 latest로 설정돼 있어도 dev 스크립트는 항상 dev 태그 사용
DOCKER_IMAGE_TAG="${DOCKER_IMAGE_TAG_DEV:-dev}"
: "${AWS_ACCOUNT_ID:?Set AWS_ACCOUNT_ID env var}"

TASK_DEF_FILE="aws-configs/hybridTool-task-definition.json"

if [ ! -f "$TASK_DEF_FILE" ]; then
  echo "Error: Task definition file not found: $TASK_DEF_FILE"
  exit 1
fi

echo "Registering ECS Task Definition (Development)"
echo "File: $TASK_DEF_FILE"
echo "Image Tag: $DOCKER_IMAGE_TAG"
echo "Region: $AWS_REGION"
echo "Profile: $AWS_PROFILE"
echo ""

# 환경 변수 치환을 위한 임시 파일 생성 (Windows 호환)
TMP_FILE="task-def-tmp-dev-$$.json"

export AWS_ACCOUNT_ID
export AWS_REGION
export ECR_REPOSITORY
export DOCKER_IMAGE_TAG

# 환경 변수 치환 (Python 사용 - Windows 호환)
# family 이름도 dev로 변경
python3 <<PYTHON_SCRIPT
import sys
import os
import json

# 환경 변수 읽기
task_def_path = '$TASK_DEF_FILE'
tmp_file_path = '$TMP_FILE'

with open(task_def_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 환경 변수 치환
content = content.replace('\${AWS_ACCOUNT_ID}', os.environ.get('AWS_ACCOUNT_ID', ''))
content = content.replace('\${AWS_REGION}', os.environ.get('AWS_REGION', ''))
content = content.replace('\${ECR_REPOSITORY}', os.environ.get('ECR_REPOSITORY', ''))
content = content.replace('\${DOCKER_IMAGE_TAG}', os.environ.get('DOCKER_IMAGE_TAG', ''))

# JSON 파싱하여 family 이름 변경
task_def = json.loads(content)
task_def['family'] = task_def['family'] + '-dev'

# 파일 저장
with open(tmp_file_path, 'w', encoding='utf-8') as f:
    json.dump(task_def, f, indent=2, ensure_ascii=False)
PYTHON_SCRIPT

echo "[1/2] Task definition prepared with environment variables"
echo "      Family: hybrid-tool-pymc-task-dev"
echo "      Image Tag: $DOCKER_IMAGE_TAG"

# Task Definition 등록
echo "[2/2] Registering task definition..."
if command -v jq > /dev/null 2>&1; then
  aws ecs register-task-definition \
    --cli-input-json "file://$TMP_FILE" \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" \
    --output json | jq -r '.taskDefinition | "Family: \(.family), Revision: \(.revision)"'
else
  OUTPUT=$(aws ecs register-task-definition \
    --cli-input-json "file://$TMP_FILE" \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" \
    --output json)
  echo "$OUTPUT" | grep -E '(family|revision)' || echo "Task definition registered"
fi

# 임시 파일 정리
rm -f "$TMP_FILE"

echo ""
echo "✅ Development task definition registered successfully!"
echo "   Family: hybrid-tool-pymc-task-dev"
echo "   Image Tag: $DOCKER_IMAGE_TAG"
