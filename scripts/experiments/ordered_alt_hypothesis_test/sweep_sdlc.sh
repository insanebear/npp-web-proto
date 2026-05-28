#!/usr/bin/env bash
# All-Low / All-Medium / All-High 3조건을 순서대로 실행하고 PFD HDI를 비교합니다.
# 사용법: bash scripts/experiments/ordered_alt_hypothesis_test/sweep_sdlc.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

_KST_TS="$(date -u -d '+9 hours' +%y%m%d_%H%M%S)"
OUT_DIR="$PROJECT_ROOT/tempDoc/hybrid-tool-test/comparison-$_KST_TS"
mkdir -p "$OUT_DIR"

echo "=================================================="
echo "PFD HDI Comparison — 3-condition run"
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
        bash "$SCRIPT_DIR/../lib/run_local.sh"

    if [ $? -ne 0 ]; then
        echo "❌ [$label] 실패. 중단합니다."
        exit 1
    fi
    echo "✅ [$label] 완료"
}

run_condition "All-Low"    "all-low"    "$PROJECT_ROOT/tempDoc/my-bbn-input-all-low.json"
run_condition "All-Medium" "all-medium" "$PROJECT_ROOT/tempDoc/my-bbn-input.json"
run_condition "All-High"   "all-high"   "$PROJECT_ROOT/tempDoc/my-bbn-input-all-high.json"

echo ""
echo "=================================================="
echo "비교 결과"
echo "=================================================="

COMPARISON_LOG="$OUT_DIR/comparison_result.log"
python "$SCRIPT_DIR/../lib/compare_pfd_hdi.py" \
    "All-Low=$OUT_DIR/results_bbn_results-all-low.json" \
    "All-Medium=$OUT_DIR/results_bbn_results-all-medium.json" \
    "All-High=$OUT_DIR/results_bbn_results-all-high.json" \
    | tee "$COMPARISON_LOG"
echo ""
echo "비교 결과 저장됨: $COMPARISON_LOG"
