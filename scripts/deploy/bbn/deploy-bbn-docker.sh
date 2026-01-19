#!/usr/bin/env bash
set -euo pipefail

# 프로젝트 루트로 이동 (스크립트 위치 기준)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

# 명령줄에서 설정된 DOCKER_IMAGE_TAG 백업 (우선순위 보장)
DOCKER_IMAGE_TAG_OVERRIDE="${DOCKER_IMAGE_TAG:-}"

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
: "${BBN_ECR_REPOSITORY:=bayesian-simulation-repo}"

# Docker 이미지 태그 선택
if [ -n "${DOCKER_IMAGE_TAG_OVERRIDE:-}" ]; then
  # 명령줄에서 설정된 경우 우선 사용
  DOCKER_IMAGE_TAG="${DOCKER_IMAGE_TAG_OVERRIDE}"
  echo "Docker 이미지 태그: $DOCKER_IMAGE_TAG (명령줄에서 설정됨)"
else
  # 명령줄 인자가 없는 경우 사용자에게 선택 요청
  echo "Docker 이미지 태그를 선택하세요:"
  echo "  1) latest (프로덕션)"
  echo "  2) dev (개발)"
  echo "  3) 직접 입력"
  echo ""
  read -p "선택 [1-3] (기본값: 1): " tag_choice
  
  case "${tag_choice:-1}" in
    1)
      DOCKER_IMAGE_TAG="latest"
      ;;
    2)
      DOCKER_IMAGE_TAG="dev"
      ;;
    3)
      read -p "태그를 입력하세요: " DOCKER_IMAGE_TAG
      if [ -z "$DOCKER_IMAGE_TAG" ]; then
        echo "⚠️  태그가 입력되지 않았습니다. latest를 사용합니다."
        DOCKER_IMAGE_TAG="latest"
      fi
      ;;
    *)
      echo "⚠️  잘못된 선택입니다. latest를 사용합니다."
      DOCKER_IMAGE_TAG="latest"
      ;;
  esac
fi
: "${AWS_ACCOUNT_ID:?Set AWS_ACCOUNT_ID env var}"

ECR_URI="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${BBN_ECR_REPOSITORY}"

echo "Building and deploying Docker image to ECR"
echo "Repository: $BBN_ECR_REPOSITORY"
echo "Tag: $DOCKER_IMAGE_TAG"
echo "Region: $AWS_REGION"
echo "Profile: $AWS_PROFILE"
echo ""

# ECR 리포지토리 확인/생성
echo "[1/5] Checking ECR repository..."
if ! aws ecr describe-repositories \
  --repository-names "$BBN_ECR_REPOSITORY" \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" \
  > /dev/null 2>&1; then
  echo "Creating ECR repository: $BBN_ECR_REPOSITORY"
  aws ecr create-repository \
    --repository-name "$BBN_ECR_REPOSITORY" \
    --region "$AWS_REGION" \
    --profile "$AWS_PROFILE" \
    --output json | jq -r '.repository.repositoryUri'
else
  echo "ECR repository exists: $BBN_ECR_REPOSITORY"
fi

# ECR 로그인
echo "[2/5] Logging in to ECR..."
aws ecr get-login-password \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" | \
  docker login --username AWS --password-stdin "$ECR_URI"

# Docker 이미지 빌드
# 빌드 컨텍스트는 프로젝트 루트 (HybridTool과 동일한 방식)
echo "[3/5] Building Docker image..."
docker build \
  -t "${BBN_ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}" \
  -f Dockers/OpenBUGS_BBN/Dockerfile \
  Dockers/OpenBUGS_BBN

# ECR 태그 추가
echo "[4/5] Tagging image for ECR..."
docker tag \
  "${BBN_ECR_REPOSITORY}:${DOCKER_IMAGE_TAG}" \
  "${ECR_URI}:${DOCKER_IMAGE_TAG}"

# ECR에 푸시
echo "[5/5] Pushing image to ECR..."
docker push "${ECR_URI}:${DOCKER_IMAGE_TAG}"

echo ""
echo "✅ Docker image deployed successfully!"
echo "   Image URI: ${ECR_URI}:${DOCKER_IMAGE_TAG}"
