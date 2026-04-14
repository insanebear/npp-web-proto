#!/usr/bin/env bash
# BBN Lambda 함수 환경 변수 설정 스크립트
# 사용법: ./scripts/deploy/bbn/set-bbn-lambda-env.sh
# 디버그 모드: DEBUG=1 ./scripts/deploy/bbn/set-bbn-lambda-env.sh

set -euo pipefail

# 프로젝트 루트로 이동 (스크립트 위치 기준)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

# 디버그 모드
DEBUG="${DEBUG:-0}"

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

# 필수 환경 변수 확인
: "${CLUSTER_NAME:?Set CLUSTER_NAME env var}"
: "${BBN_TASK_DEFINITION:?Set BBN_TASK_DEFINITION env var}"
: "${SUBNET_IDS:?Set SUBNET_IDS env var}"
: "${BBN_LAMBDA_FUNCTION_NAME:?Set BBN_LAMBDA_FUNCTION_NAME env var}"

# 선택적 환경 변수
: "${JOBS_TABLE_NAME:=}"
: "${BBN_CONTAINER_NAME:=bayesian-simulation-app}"

# 개발 환경 변수 (선택적, 없으면 프로덕션 변수 사용)
: "${CLUSTER_NAME_DEV:=}"
: "${BBN_TASK_DEFINITION_DEV:=}"

echo "=========================================="
echo "Setting environment variables for BBN Lambda function"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  CLUSTER_NAME: $CLUSTER_NAME"
echo "  BBN_TASK_DEFINITION: $BBN_TASK_DEFINITION"
echo "  SUBNET_IDS: $SUBNET_IDS"
echo "  JOBS_TABLE_NAME: ${JOBS_TABLE_NAME:-'(not set - DynamoDB job tracking disabled)'}"
echo "  BBN_CONTAINER_NAME: $BBN_CONTAINER_NAME"
if [ -n "$CLUSTER_NAME_DEV" ]; then
  echo "  CLUSTER_NAME_DEV: $CLUSTER_NAME_DEV (for /develop stage)"
fi
if [ -n "$BBN_TASK_DEFINITION_DEV" ]; then
  echo "  BBN_TASK_DEFINITION_DEV: $BBN_TASK_DEFINITION_DEV (for /develop stage)"
fi
if [ -n "$BBN_CONTAINER_NAME_DEV" ]; then
  echo "  BBN_CONTAINER_NAME_DEV: $BBN_CONTAINER_NAME_DEV (for /develop stage)"
fi
echo "  AWS_REGION: $AWS_REGION (Note: Lambda reserved variable, not set in env vars)"
echo ""

# Windows 호환 임시 파일 경로
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
  ENV_JSON_FILE="/tmp/lambda-env-$$.json"
  CLI_INPUT_FILE="/tmp/lambda-input-$$.json"
  ERR_FILE="/tmp/lambda-error-$$.txt"
else
  ENV_JSON_FILE=$(mktemp)
  CLI_INPUT_FILE=$(mktemp)
  ERR_FILE=$(mktemp)
fi

# Python으로 JSON 생성 (Windows bash에서 echo \n 이슈 방지)
# 주의: AWS_REGION은 Lambda의 예약된 환경 변수이므로 설정하지 않음
PYTHON_CMD=$(command -v python3 2>/dev/null || command -v python)
if [ -z "$PYTHON_CMD" ]; then
  echo "❌ Error: python3 or python not found"
  exit 1
fi

$PYTHON_CMD - <<PYEOF > "$ENV_JSON_FILE"
import json, sys

variables = {
    "CLUSTER_NAME": "$CLUSTER_NAME",
    "BBN_TASK_DEFINITION": "$BBN_TASK_DEFINITION",
    "SUBNET_IDS": "$SUBNET_IDS",
    "JOBS_TABLE_NAME": "${JOBS_TABLE_NAME:-}",
    "CONTAINER_NAME": "$BBN_CONTAINER_NAME",
}

cluster_dev = "$CLUSTER_NAME_DEV"
task_def_dev = "$BBN_TASK_DEFINITION_DEV"
container_dev = "$BBN_CONTAINER_NAME_DEV"

if cluster_dev:
    variables["CLUSTER_NAME_DEV"] = cluster_dev
if task_def_dev:
    variables["BBN_TASK_DEFINITION_DEV"] = task_def_dev
if container_dev:
    variables["CONTAINER_NAME_DEV"] = container_dev

print(json.dumps({"Variables": variables}, indent=2))
PYEOF

# JSON 유효성 검증
if ! $PYTHON_CMD -m json.tool "$ENV_JSON_FILE" > /dev/null 2>&1; then
  echo "❌ Error: Generated JSON is invalid!"
  cat "$ENV_JSON_FILE"
  rm -f "$ENV_JSON_FILE" "$CLI_INPUT_FILE" "$ERR_FILE"
  exit 1
fi

# --cli-input-json 용 파일 생성
$PYTHON_CMD - <<PYEOF > "$CLI_INPUT_FILE"
import json

with open("$ENV_JSON_FILE") as f:
    env = json.load(f)

print(json.dumps({
    "FunctionName": "$BBN_LAMBDA_FUNCTION_NAME",
    "Environment": env
}))
PYEOF

# 디버그 모드에서 JSON 출력
if [ "$DEBUG" = "1" ]; then
  echo ""
  echo "Debug: cli-input-json:"
  cat "$CLI_INPUT_FILE"
  echo ""
fi

# Lambda 함수 존재 여부 확인
echo "[Setting env vars] $BBN_LAMBDA_FUNCTION_NAME..."

if ! aws lambda get-function \
    --function-name "$BBN_LAMBDA_FUNCTION_NAME" \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" \
    --output json > /dev/null 2>&1; then
  echo "  ⚠️  Function does not exist: $BBN_LAMBDA_FUNCTION_NAME"
  echo "     (Deploy the function first using scripts/deploy/bbn/deploy-bbn-lambda.sh)"
  echo ""
  rm -f "$ENV_JSON_FILE" "$CLI_INPUT_FILE" "$ERR_FILE"
  exit 1
fi

# 환경 변수 업데이트 (file://로 전달하여 Windows bash 파싱 문제 방지)
UPDATE_RESULT=$(aws lambda update-function-configuration \
    --cli-input-json "file://$CLI_INPUT_FILE" \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" \
    --output json 2>"$ERR_FILE")
UPDATE_EXIT_CODE=$?

if [ $UPDATE_EXIT_CODE -eq 0 ]; then
  if command -v jq > /dev/null 2>&1; then
    echo "  ✅ Updated: $(echo "$UPDATE_RESULT" | jq -r '.FunctionName + " - Status: " + .LastUpdateStatus')"
  else
    echo "  ✅ Updated successfully"
  fi
else
  echo "  ❌ Failed to update $BBN_LAMBDA_FUNCTION_NAME"
  ERR_CONTENT=$(cat "$ERR_FILE")
  if [ -n "$ERR_CONTENT" ]; then
    echo "     Error details:"
    echo "$ERR_CONTENT" | sed 's/^/     /'
  fi
fi

rm -f "$ENV_JSON_FILE" "$CLI_INPUT_FILE" "$ERR_FILE"

echo ""
echo "=========================================="
echo "✅ Environment variables configuration completed!"
echo "=========================================="

