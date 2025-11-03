#!/usr/bin/env bash
set -euo pipefail

# 환경 변수 설정 파일이 있으면 로드
CONFIG_FILE="scripts/.website-env"
if [ -f "$CONFIG_FILE" ]; then
  set -a
  . "$CONFIG_FILE"
  set +a
fi

# 환경 변수 확인
: "${S3_BUCKET:?Set S3_BUCKET env var}"
: "${CLOUDFRONT_DISTRIBUTION:?Set CLOUDFRONT_DISTRIBUTION env var}"
: "${AWS_REGION:=us-east-1}"
: "${AWS_PROFILE:=default}"

echo "[1/3] Building React project..."
npm run build

if [ ! -d "dist" ]; then
  echo "Error: dist directory not found after build"
  exit 1
fi

echo "[2/3] Uploading to S3 bucket: $S3_BUCKET..."
aws s3 sync dist/ s3://$S3_BUCKET/ \
  --delete \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" \
  --cache-control "public, max-age=31536000, immutable" \
  --exclude "*.html" \
  --exclude "index.html"

# HTML 파일은 별도로 업로드 (캐싱 없이)
aws s3 sync dist/ s3://$S3_BUCKET/ \
  --delete \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" \
  --cache-control "public, max-age=0, must-revalidate" \
  --include "*.html"

echo "[3/3] Invalidating CloudFront cache for distribution: $CLOUDFRONT_DISTRIBUTION..."
INVALIDATION_ID=$(aws cloudfront create-invalidation \
  --distribution-id "$CLOUDFRONT_DISTRIBUTION" \
  --paths "/*" \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" \
  --query 'Invalidation.Id' \
  --output text)

echo "CloudFront invalidation created: $INVALIDATION_ID"
echo ""
echo "✅ Deployment completed successfully!"
echo "   S3 Bucket: $S3_BUCKET"
echo "   CloudFront Distribution: $CLOUDFRONT_DISTRIBUTION"
echo "   Invalidation ID: $INVALIDATION_ID"


