#!/usr/bin/env bash
# HybridTool Lambda 함수 환경 변수 설정 스크립트
# 사용법: ./scripts/deploy/hybridTool/set-hybridTool-lambda-env.sh
# 디버그 모드: DEBUG=1 ./scripts/deploy/hybridTool/set-hybridTool-lambda-env.sh

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
: "${TASK_DEFINITION:?Set TASK_DEFINITION env var}"
: "${SUBNET_IDS:?Set SUBNET_IDS env var}"
: "${S3_BUCKET:?Set S3_BUCKET env var}"

# 선택적 환경 변수
: "${JOBS_TABLE_NAME:=}"
: "${CONTAINER_NAME:=hybrid-tool-container}"

echo "=========================================="
echo "Setting environment variables for HybridTool Lambda functions"
echo "=========================================="
echo ""
echo "Configuration:"
echo "  CLUSTER_NAME: $CLUSTER_NAME"
echo "  TASK_DEFINITION: $TASK_DEFINITION"
echo "  SUBNET_IDS: $SUBNET_IDS"
echo "  S3_BUCKET: $S3_BUCKET"
echo "  JOBS_TABLE_NAME: ${JOBS_TABLE_NAME:-'(not set - DynamoDB job tracking disabled)'}"
echo "  CONTAINER_NAME: $CONTAINER_NAME"
echo "  AWS_REGION: $AWS_REGION (Note: Lambda reserved variable, not set in env vars)"
echo ""

# 환경 변수 JSON 생성
# 주의: AWS_REGION은 Lambda의 예약된 환경 변수이므로 설정하지 않음
# Lambda 함수 코드에서 os.environ.get('AWS_REGION', 'ap-northeast-2')로 자동 처리됨
ENV_VARS_JSON=$(cat <<EOF
{
  "Variables": {
    "CLUSTER_NAME": "$CLUSTER_NAME",
    "TASK_DEFINITION": "$TASK_DEFINITION",
    "SUBNET_IDS": "$SUBNET_IDS",
    "S3_BUCKET": "$S3_BUCKET",
    "JOBS_TABLE_NAME": "${JOBS_TABLE_NAME:-}",
    "CONTAINER_NAME": "$CONTAINER_NAME"
  }
}
EOF
)

# JSON 유효성 검증 (Python 사용)
if command -v python3 > /dev/null 2>&1 || command -v python > /dev/null 2>&1; then
  PYTHON_CMD=$(command -v python3 2>/dev/null || command -v python)
  if ! echo "$ENV_VARS_JSON" | $PYTHON_CMD -m json.tool > /dev/null 2>&1; then
    echo "❌ Error: Generated JSON is invalid!"
    echo "JSON content:"
    echo "$ENV_VARS_JSON"
    exit 1
  fi
fi

# 디버그 모드에서 JSON 출력
if [ "$DEBUG" = "1" ]; then
  echo ""
  echo "Debug: Environment variables JSON:"
  if command -v jq > /dev/null 2>&1; then
    echo "$ENV_VARS_JSON" | jq .
  else
    echo "$ENV_VARS_JSON"
  fi
  echo ""
fi

# Lambda 함수 목록
LAMBDA_FUNCTIONS=(
  "hybrid-tool-trigger-full-analysis-task"
  "hybrid-tool-trigger-sensitivity-task"
  "hybrid-tool-trigger-update-pfd-task"
  "hybrid-tool-get-results"
  "hybrid-tool-get-job-status"
  "hybrid-tool-list-bbn-results"
)

# 각 Lambda 함수에 환경 변수 설정
for FUNCTION_NAME in "${LAMBDA_FUNCTIONS[@]}"; do
  echo "[Setting env vars] $FUNCTION_NAME..."
  
  # Windows 호환 임시 파일 경로
  if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    TMP_FILE="/tmp/lambda-update-$$.json"
    ERR_FILE="/tmp/lambda-error-$$.txt"
  else
    TMP_FILE=$(mktemp)
    ERR_FILE=$(mktemp)
  fi
  
  # Lambda 함수 존재 여부 확인
  if ! aws lambda get-function \
      --function-name "$FUNCTION_NAME" \
      --region "$AWS_REGION" \
      --profile "$AWS_PROFILE" \
      --output json > /dev/null 2>&1; then
    echo "  ⚠️  Function does not exist: $FUNCTION_NAME"
    echo "     (Deploy the function first using scripts/deploy/hybridTool/deploy-hybridTool-lambda.sh)"
    echo ""
    continue
  fi
  
  # 환경 변수 업데이트
  UPDATE_RESULT=$(aws lambda update-function-configuration \
      --function-name "$FUNCTION_NAME" \
      --environment "$ENV_VARS_JSON" \
      --region "$AWS_REGION" \
      --profile "$AWS_PROFILE" \
      --output json 2>"$ERR_FILE")
  UPDATE_EXIT_CODE=$?
  
  if [ $UPDATE_EXIT_CODE -eq 0 ]; then
    echo "$UPDATE_RESULT" > "$TMP_FILE"
    if command -v jq > /dev/null 2>&1; then
      echo "  ✅ Updated: $(echo "$UPDATE_RESULT" | jq -r '.FunctionName + " - Status: " + .LastUpdateStatus')"
    else
      echo "  ✅ Updated successfully"
    fi
  else
    echo "  ❌ Failed to update $FUNCTION_NAME"
    ERR_CONTENT=$(cat "$ERR_FILE")
    if [ -n "$ERR_CONTENT" ]; then
      echo "     Error details:"
      echo "$ERR_CONTENT" | sed 's/^/     /'
    else
      echo "     (No error message - check AWS CLI configuration and permissions)"
      echo "     Debug: Exit code = $UPDATE_EXIT_CODE"
      echo "     Debug: Try running manually:"
      echo "       aws lambda update-function-configuration \\"
      echo "         --function-name $FUNCTION_NAME \\"
      echo "         --environment '$ENV_VARS_JSON' \\"
      echo "         --region $AWS_REGION \\"
      echo "         --profile $AWS_PROFILE"
    fi
  fi
  
  rm -f "$TMP_FILE" "$ERR_FILE"
  echo ""
done

echo "=========================================="
echo "✅ Environment variables configuration completed!"
echo "=========================================="

