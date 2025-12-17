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

# 환경 변수 확인
: "${AWS_REGION:=ap-northeast-2}"
: "${AWS_PROFILE:=default}"
: "${ECR_REPOSITORY:=hybrid-tool-pymc}"
: "${DOCKER_IMAGE_TAG:=latest}"
: "${AWS_ACCOUNT_ID:?Set AWS_ACCOUNT_ID env var}"

ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPOSITORY}"

echo "Building and deploying Docker image to ECR"
echo "Repository: $ECR_REPOSITORY"
echo "Tag: $DOCKER_IMAGE_TAG"
echo "Region: $AWS_REGION"
echo "Profile: $AWS_PROFILE"
echo ""

# ECR 리포지토리 확인/생성
echo "[1/5] Checking ECR repository..."
if ! aws ecr describe-repositories \
  --repository-names "$ECR_REPOSITORY" \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" \
  > /dev/null 2>&1; then
  echo "Creating ECR repository: $ECR_REPOSITORY"
  aws ecr create-repository \
    --repository-name "$ECR_REPOSITORY" \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" \
    --output json | jq -r '.repository.repositoryUri'
else
  echo "ECR repository exists: $ECR_REPOSITORY"
fi

# ECR 로그인
echo "[2/5] Logging in to ECR..."
aws ecr get-login-password \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" | \
  docker login --username AWS --password-stdin "$ECR_URI"

# Docker 이미지 빌드
echo "[3/5] Building Docker image..."
docker build \
  -t "${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}" \
  -f Dockers/HybridTool/Dockerfile \
  .

# ECR 태그 추가
echo "[4/5] Tagging image for ECR..."
docker tag \
  "${ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}" \
  "${ECR_URI}:${DOCKER_IMAGE_TAG}"

# ECR에 푸시
echo "[5/5] Pushing image to ECR..."
docker push "${ECR_URI}:${DOCKER_IMAGE_TAG}"

echo ""
echo "✅ Docker image deployed successfully!"
echo "   Image URI: ${ECR_URI}:${DOCKER_IMAGE_TAG}"

