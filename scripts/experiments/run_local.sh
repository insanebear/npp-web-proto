#!/usr/bin/env bash
# Docker 이미지 빌드 없이 HybridTool 스크립트를 로컬에서 실행하는 헬퍼 스크립트.
# conda 환경(gxx_env_311)을 사용합니다.
#
# 사용법:
#   bash run_local.sh                          # 기본값: TASK_TYPE=bbn_inference
#   TASK_TYPE=full_analysis bash run_local.sh
#   TASK_TYPE=sensitivity_analysis bash run_local.sh
#   TASK_TYPE=update_pfd bash run_local.sh
#   TASK_TYPE=bbn_inference bash run_local.sh
#
# 주요 환경변수 오버라이드 예시:
#   nIter=5000 nBurnin=2000 nChains=4 bash run_local.sh
#   BBN_INPUT_FILE=/path/to/input.json bash run_local.sh
#   TEST_MODE=true bash run_local.sh           # 실제 계산 없이 더미 결과 반환

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

_KST_TS="$(date -u -d '+9 hours' +%y%m%d_%H%M%S)"

export CONDA_ENV_NAME="${CONDA_ENV_NAME:-gxx_env_311}"
export TASK_TYPE="${TASK_TYPE:-bbn_inference}"
export JOB_ID="${JOB_ID:-local-full-$_KST_TS}"
export PFD_GOAL="${PFD_GOAL:-0.0001}"
export CONFIDENCE_GOAL="${CONFIDENCE_GOAL:-0.95}"
export FAILURES="${FAILURES:-0}"
export DEMAND_REQUIRED="${DEMAND_REQUIRED:-10000}"
export S3_BUCKET="${S3_BUCKET:-dummy}"
export AWS_REGION="${AWS_REGION:-ap-northeast-2}"
export TEST_MODE="${TEST_MODE:-false}"
export TEST_OUTPUT_DIR="${TEST_OUTPUT_DIR:-$PROJECT_ROOT/tempDoc/hybrid-tool-test/$_KST_TS}"
# export DRAWS="${DRAWS:-1000}"
# export TUNE="${TUNE:-500}"
# export CHAINS="${CHAINS:-1}"
# export THIN="${THIN:-1}"

# bbn_inference용 환경 변수 (TASK_TYPE=bbn_inference 시 사용)
export FP_Input="${FP_Input:-200}"

# BBN_INPUT_FILE: 설정하면 해당 JSON 파일로 실행, 미설정 시 my-bbn-input.json 사용
export BBN_INPUT_FILE="${BBN_INPUT_FILE:-$PROJECT_ROOT/tempDoc/my-bbn-input.json}"

export nChains="${nChains:-1}"
export nIter="${nIter:-2000}"
export nBurnin="${nBurnin:-1000}"
export nThin="${nThin:-1}"

LOG_FILE="$TEST_OUTPUT_DIR/run_local_$_KST_TS.log"
mkdir -p "$TEST_OUTPUT_DIR"
bash "$SCRIPT_DIR/lib/runner.sh" 2>&1 | tee "$LOG_FILE"
echo ""
echo "로그 저장됨: $LOG_FILE"
