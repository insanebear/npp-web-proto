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

echo "[1/4] Clean"
rm -rf lambda-build lambda/bundle.zip

echo "[2/4] Build"
npx tsc -p lambda/tsconfig.json

# Handler is configured as: lambda/BayesianStarterLambda.handler
# With rootDir=lambda/ and outDir=lambda-build/, the compiled output preserves the path

echo "[3/4] Zip"
(cd lambda-build && npx --yes bestzip ../lambda/bundle.zip .)

echo "[4/4] Deploy"
aws lambda update-function-code \
  --function-name "$FUNCTION_NAME" \
  --zip-file fileb://lambda/bundle.zip \
  --region "$AWS_REGION" \
  --profile "$AWS_PROFILE"

echo "Done."
