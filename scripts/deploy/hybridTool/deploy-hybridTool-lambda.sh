#!/usr/bin/env bash
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

# 함수명과 파일 경로를 인자로 받음
FUNCTION_NAME="${1:?Usage: $0 <function-name> <lambda-file-path>}"
LAMBDA_FILE="${2:?Usage: $0 <function-name> <lambda-file-path>}"

# 환경 변수 확인
: "${AWS_REGION:=ap-northeast-2}"
: "${AWS_PROFILE:=default}"

if [ ! -f "$LAMBDA_FILE" ]; then
  echo "Error: Lambda file not found: $LAMBDA_FILE"
  exit 1
fi

echo "Deploying Lambda function: $FUNCTION_NAME"
echo "Source file: $LAMBDA_FILE"
echo "Region: $AWS_REGION"
echo "Profile: $AWS_PROFILE"
echo ""

# 임시 디렉토리 생성 (Windows 호환)
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
  # Windows Git Bash
  TMP_DIR=$(mktemp -d 2>/dev/null || echo "/tmp/lambda-deploy-$$")
  mkdir -p "$TMP_DIR"
else
  TMP_DIR=$(mktemp -d)
fi
ZIP_FILE="$TMP_DIR/function.zip"

# Lambda 파일을 zip으로 압축
# handler 함수가 파일명과 동일해야 함 (예: triggerTask.py -> handler)
LAMBDA_DIR="$(cd "$(dirname "$LAMBDA_FILE")" && pwd)"
FILE_NAME="$(basename "$LAMBDA_FILE")"

# Windows Git Bash에서 zip이 없을 수 있으므로 Python 사용
if command -v zip > /dev/null 2>&1; then
  cd "$LAMBDA_DIR"
  zip -q "$ZIP_FILE" "$FILE_NAME"
else
  # Python으로 zip 파일 생성
  cd "$LAMBDA_DIR"
  python3 -c "
import zipfile
import os
os.makedirs(os.path.dirname('$ZIP_FILE'), exist_ok=True)
with zipfile.ZipFile('$ZIP_FILE', 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write('$FILE_NAME', '$FILE_NAME')
" 2>/dev/null || python -c "
import zipfile
import os
os.makedirs(os.path.dirname('$ZIP_FILE'), exist_ok=True)
with zipfile.ZipFile('$ZIP_FILE', 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write('$FILE_NAME', '$FILE_NAME')
"
fi

echo "[1/2] Created zip file: $ZIP_FILE"

# Lambda 함수 업데이트
echo "[2/2] Updating Lambda function code..."
if command -v jq > /dev/null 2>&1; then
  aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file "fileb://$ZIP_FILE" \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" \
    --output json | jq -r '.FunctionName, .LastUpdateStatus'
else
  aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --zip-file "fileb://$ZIP_FILE" \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" \
    --output json | grep -E '(FunctionName|LastUpdateStatus)' || echo "Update initiated"
fi

# 임시 파일 정리
rm -rf "$TMP_DIR"

echo ""
echo "✅ Deployment completed: $FUNCTION_NAME"

