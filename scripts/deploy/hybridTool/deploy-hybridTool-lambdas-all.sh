#!/usr/bin/env bash
# HybridTool Lambda 함수 일괄 배포 스크립트
# 사용법: ./scripts/deploy/hybridTool/deploy-hybridTool-lambdas-all.sh

set -euo pipefail

# 프로젝트 루트로 이동 (스크립트 위치 기준)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$PROJECT_ROOT"

DEPLOY_SCRIPT="scripts/deploy/hybridTool/deploy-hybridTool-lambda.sh"

echo "=========================================="
echo "Deploying all HybridTool Lambda functions"
echo "=========================================="
echo ""

# 1. Full Analysis Trigger
echo "[1/6] Deploying hybrid-tool-trigger-full-analysis-task..."
$DEPLOY_SCRIPT "hybrid-tool-trigger-full-analysis-task" "lambda/hybridTool/triggerTask.py"
echo ""

# 2. Sensitivity Analysis Trigger
echo "[2/6] Deploying hybrid-tool-trigger-sensitivity-task..."
$DEPLOY_SCRIPT "hybrid-tool-trigger-sensitivity-task" "lambda/hybridTool/triggerSensitivityTask.py"
echo ""

# 3. Update PFD Trigger
echo "[3/6] Deploying hybrid-tool-trigger-update-pfd-task..."
$DEPLOY_SCRIPT "hybrid-tool-trigger-update-pfd-task" "lambda/hybridTool/triggerUpdatePfdTask.py"
echo ""

# 4. Get Results
echo "[4/6] Deploying hybrid-tool-get-results..."
$DEPLOY_SCRIPT "hybrid-tool-get-results" "lambda/hybridTool/getResults.py"
echo ""

# 5. Get Job Status
echo "[5/6] Deploying hybrid-tool-get-job-status..."
$DEPLOY_SCRIPT "hybrid-tool-get-job-status" "lambda/hybridTool/getJobStatus.py"
echo ""

# 6. List BBN Results
echo "[6/6] Deploying hybrid-tool-list-bbn-results..."
$DEPLOY_SCRIPT "hybrid-tool-list-bbn-results" "lambda/hybridTool/listBbnResults.py"
echo ""

echo "=========================================="
echo "✅ All deployments completed!"
echo "=========================================="

