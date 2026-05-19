#!/usr/bin/env bash
# All-Medium SDLC 조건에서 FP를 50 / 200 / 1000으로 순서대로 실행하고 PFD HDI를 비교합니다.
# 사용법: bash Dockers/HybridTool/run_fp_sweep.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

_KST_TS="$(date -u -d '+9 hours' +%y%m%d_%H%M%S)"
OUT_DIR="$PROJECT_ROOT/tempDoc/hybrid-tool-test/fp-sweep-$_KST_TS"
mkdir -p "$OUT_DIR"

echo "=================================================="
echo "FP Sweep — All-Medium SDLC (FP: 50 / 200 / 1000)"
echo "출력 디렉토리: $OUT_DIR"
echo "=================================================="

run_condition() {
    local label="$1"
    local job_id="$2"
    local input_file="$3"

    echo ""
    echo ">>> [$label] 시작 ..."
    JOB_ID="$job_id" \
    BBN_INPUT_FILE="$input_file" \
    TEST_OUTPUT_DIR="$OUT_DIR" \
        bash "$SCRIPT_DIR/run_local.sh"

    if [ $? -ne 0 ]; then
        echo "❌ [$label] 실패. 중단합니다."
        exit 1
    fi
    echo "✅ [$label] 완료"
}

run_condition "FP-50"   "fp-50"   "$PROJECT_ROOT/tempDoc/my-bbn-input-fp50.json"
run_condition "FP-200"  "fp-200"  "$PROJECT_ROOT/tempDoc/my-bbn-input.json"
run_condition "FP-1000" "fp-1000" "$PROJECT_ROOT/tempDoc/my-bbn-input-fp1000.json"

echo ""
echo "=================================================="
echo "비교 결과"
echo "=================================================="

COMPARISON_LOG="$OUT_DIR/comparison_result.log"
python "$SCRIPT_DIR/compare_pfd_hdi.py" \
    "FP-1000=$OUT_DIR/results_bbn_results-fp-1000.json" \
    "FP-200=$OUT_DIR/results_bbn_results-fp-200.json" \
    "FP-50=$OUT_DIR/results_bbn_results-fp-50.json" \
    | tee "$COMPARISON_LOG"
echo ""
echo "비교 결과 저장됨: $COMPARISON_LOG"
