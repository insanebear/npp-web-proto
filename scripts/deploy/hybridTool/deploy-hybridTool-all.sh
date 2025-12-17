#!/usr/bin/env bash
# HybridTool 전체 배포 스크립트
# Docker 이미지, Task Definition, Lambda 함수를 순서대로 배포
# 사용법: ./scripts/deploy/hybridTool/deploy-hybridTool-all.sh

set -euo pipefail

# 환경 변수 설정 파일이 있으면 로드
CONFIG_FILE="scripts/config/.nppswrel-env"
if [ -f "$CONFIG_FILE" ]; then
  set -a
  . "$CONFIG_FILE"
  set +a
fi

# 프로젝트 루트로 이동
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../../.."

echo "=========================================="
echo "HybridTool 전체 배포 프로세스"
echo "=========================================="
echo ""

# 1. Docker 이미지 빌드 및 ECR 푸시
echo "[1/4] Building and pushing Docker image to ECR..."
bash scripts/deploy/hybridTool/deploy-hybridTool-docker.sh
echo ""

# 2. ECS Task Definition 등록
echo "[2/4] Registering ECS Task Definition..."
bash scripts/deploy/hybridTool/deploy-hybridTool-task-definition.sh
echo ""

# 3. Lambda 함수 배포
echo "[3/4] Deploying Lambda functions..."
bash scripts/deploy/hybridTool/deploy-hybridTool-lambdas-all.sh
echo ""

# 4. Lambda 함수 환경 변수 설정
echo "[4/4] Setting Lambda function environment variables..."
bash scripts/deploy/hybridTool/set-hybridTool-lambda-env.sh
echo ""

echo "=========================================="
echo "✅ 전체 배포 완료!"
echo "=========================================="
echo ""
echo "다음 단계:"
echo "1. Lambda 함수가 정상적으로 실행되는지 테스트"
echo "2. ECS Task가 정상적으로 시작되는지 확인"
echo "3. CloudWatch Logs에서 오류 확인"
echo ""

