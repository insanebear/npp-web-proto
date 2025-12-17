#!/usr/bin/env bash
# BayesianStarterLambda 배포 스크립트
# TypeScript로 작성된 Bayesian 시뮬레이션 시작 Lambda 함수를 배포합니다.
# 사용법: ./scripts/deploy/bbn/deploy-bbn-lambda.sh
# 환경변수: scripts/config/.nppswrel-env 파일에 BBN_LAMBDA_FUNCTION_NAME, AWS_REGION, AWS_PROFILE 설정 필요

set -euo pipefail

# 프로젝트 루트로 이동 (스크립트 위치 기준)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

CONFIG_FILE="scripts/config/.nppswrel-env"
if [ -f "$CONFIG_FILE" ]; then
  set -a
  . "$CONFIG_FILE"
  set +a
fi

: "${BBN_LAMBDA_FUNCTION_NAME:?Set BBN_LAMBDA_FUNCTION_NAME env var}"
FUNCTION_NAME="$BBN_LAMBDA_FUNCTION_NAME"
: "${AWS_REGION:?Set AWS_REGION env var}"
: "${AWS_PROFILE:?Set AWS_PROFILE env var}"

echo "[1/4] Clean"
rm -rf lambda-build lambda/bundle.zip

echo "[2/4] Build"
npx tsc -p lambda/tsconfig.json

# Handler is configured as: lambda/BayesianStarterLambda.handler
# With rootDir=lambda/ and outDir=lambda-build/, the compiled output preserves the path

echo "[3/4] Zip"
(cd lambda-build && npx --yes bestzip ../lambda/bundle.zip .)

echo "[4/4] Deploy"
if aws lambda update-function-code \
  --function-name "$BBN_LAMBDA_FUNCTION_NAME" \
  --zip-file fileb://lambda/bundle.zip \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" \
  --output json > /dev/null 2>&1; then
  echo "✅ Deployment completed: $BBN_LAMBDA_FUNCTION_NAME"
else
  echo "❌ Deployment failed"
  # 에러 메시지 출력
  aws lambda update-function-code \
    --function-name "$BBN_LAMBDA_FUNCTION_NAME" \
    --zip-file fileb://lambda/bundle.zip \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" 2>&1 | head -10
  exit 1
fi

