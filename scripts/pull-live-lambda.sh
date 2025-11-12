#!/usr/bin/env bash
set -euo pipefail

CONFIG_FILE="scripts/.lambda-env"
if [ -f "$CONFIG_FILE" ]; then
  set -a
  . "$CONFIG_FILE"
  set +a
fi

: "${FUNCTION_NAME:?Set FUNCTION_NAME env var}"
: "${AWS_REGION:?Set AWS_REGION env var}"
: "${AWS_PROFILE:?Set AWS_PROFILE env var}"

mkdir -p lambda/aws-live

TMP_URL=$(aws lambda get-function \
  --function-name "$FUNCTION_NAME" \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE" \
  --query 'Code.Location' --output text)

curl -L "$TMP_URL" -o lambda/aws-live/code.zip

rm -rf lambda/aws-live/extracted
mkdir -p lambda/aws-live/extracted
unzip -o lambda/aws-live/code.zip -d lambda/aws-live/extracted

echo "Pulled and extracted to lambda/aws-live/extracted"
