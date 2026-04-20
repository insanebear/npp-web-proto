#!/usr/bin/env bash
# HybridTool 전체 배포 스크립트 (개발 - dev 태그)
# Docker 이미지, Task Definition, Lambda 함수를 순서대로 배포
# 사용법: ./scripts/deploy/hybridTool/deploy-hybridTool-all-dev.sh
#
# npm run dev → /develop API 스테이지 → Lambda에서 CLUSTER_NAME_DEV + HYBRID_TASK_DEFINITION_DEV 사용
# Lambda 함수는 prod와 공유 (코드 변경 시 prod에도 반영됨)

set -euo pipefail

# 프로젝트 루트로 이동
cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/../../.."

# 환경 변수 설정 파일이 있으면 로드
CONFIG_FILE="scripts/config/.nppswrel-env"
if [ -f "$CONFIG_FILE" ]; then
  set -a
  . "$CONFIG_FILE"
  set +a
fi

# 개발 배포: 항상 dev 태그 사용 (config 파일의 DOCKER_IMAGE_TAG 무시)
export DOCKER_IMAGE_TAG="${DOCKER_IMAGE_TAG_DEV:-dev}"

echo "=========================================="
echo "HybridTool 전체 배포 프로세스 (dev / $DOCKER_IMAGE_TAG)"
echo "=========================================="
echo ""

# 1. Docker 이미지 빌드 및 ECR 푸시 (dev 태그)
echo "[1/4] Building and pushing Docker image to ECR (tag: $DOCKER_IMAGE_TAG)..."
bash scripts/deploy/hybridTool/deploy-hybridTool-docker.sh
echo ""

# 2. ECS Task Definition 등록 (dev family: hybrid-tool-pymc-task-dev)
echo "[2/4] Registering ECS Task Definition (dev)..."
bash scripts/deploy/hybridTool/deploy-hybridTool-task-definition-dev.sh
echo ""

# 3. Lambda 함수 배포 (prod와 공유 함수 - Lambda 코드 변경이 있을 때만 필요)
echo "[3/4] Deploying Lambda functions..."
echo "      (주의: Lambda 함수는 prod/dev 공유. 코드 변경이 없으면 이 단계는 생략 가능)"
bash scripts/deploy/hybridTool/deploy-hybridTool-lambdas-all.sh
echo ""

# 4. Lambda 함수 환경 변수 설정 (CLUSTER_NAME_DEV, HYBRID_TASK_DEFINITION_DEV 포함)
echo "[4/4] Setting Lambda function environment variables (including DEV vars)..."
bash scripts/deploy/hybridTool/set-hybridTool-lambda-env.sh
echo ""

echo "=========================================="
echo "✅ 개발 환경 배포 완료!"
echo "=========================================="
echo ""
echo "확인 사항:"
echo "1. npm run dev → /develop 스테이지 → dev 이미지($DOCKER_IMAGE_TAG) ECS Task 실행"
echo "2. Lambda 환경변수: HYBRID_TASK_DEFINITION_DEV=${HYBRID_TASK_DEFINITION_DEV:-미설정}"
echo "3. Lambda 환경변수: CLUSTER_NAME_DEV=${CLUSTER_NAME_DEV:-미설정}"
echo ""
