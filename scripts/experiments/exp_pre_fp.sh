#!/usr/bin/env bash
# 사전 실험: FP draws 탐색 (단조성 기준)
#   exp_fp.sh 실행에 앞서 안정적인 draws 최솟값 탐색
#   chains=1, thin=1 고정
#   tune=1000 고정, draws 그리드 서치로 단조성이 안정적으로 나오는 최솟값 탐색
#   tune을 여러 값으로 비교할 경우 TUNE_LIST에 값 추가
#   조건: FP-1000 PFD > FP-200 PFD > FP-50 PFD (median & mean 모두)
#
# 사용법:
#   bash scripts/experiments/exp_pre_fp.sh
#   MAX_JOBS=3 bash scripts/experiments/exp_pre_fp.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# ── 실험 설정 ─────────────────────────────────────────────────
NCHAINS=1
NTHIN=1
TUNE_LIST=(1000)            # 기본 1000 고정; 범위 비교 시 (1000 2000 ...) 으로 확장
DRAWS_LIST=(500 1000 2000 3000)
NREPS=3
MAX_JOBS="${MAX_JOBS:-4}"

S3_BUCKET="dummy"
AWS_REGION="ap-northeast-2"
TASK_TYPE="bbn_inference"

# compare_pfd_hdi.py는 입력 순서대로 단조 감소를 검사하므로 높은 FP부터 나열
CONDITION_KEYS=(fp-1000 fp-200 fp-50)
declare -A CONDITION_FILES
CONDITION_FILES[fp-1000]="$PROJECT_ROOT/tempDoc/my-bbn-input-fp1000.json"
CONDITION_FILES[fp-200]="$PROJECT_ROOT/tempDoc/my-bbn-input.json"
CONDITION_FILES[fp-50]="$PROJECT_ROOT/tempDoc/my-bbn-input-fp50.json"
declare -A CONDITION_LABELS
CONDITION_LABELS[fp-1000]="FP-1000"
CONDITION_LABELS[fp-200]="FP-200"
CONDITION_LABELS[fp-50]="FP-50"

# ── 출력 디렉토리 & 로그 ─────────────────────────────────────
_KST_TS="$(date -u -d '+9 hours' +%y%m%d_%H%M%S)"
OUT_DIR="$PROJECT_ROOT/tempDoc/hybrid-tool-test/exp-pre-fp-$_KST_TS"
mkdir -p "$OUT_DIR"
LOG_FILE="$OUT_DIR/exp_pre_fp_run.log"

# ── 결과 추적용 전역 배열 ─────────────────────────────────────
declare -A PASS_COUNT
declare -A PARTIAL_COUNT
declare -A FAIL_COUNT
declare -A MISSING_COUNT

# ─────────────────────────────────────────────────────────────
run_job() {
    local job_id="$1" cond="$2" niter="$3" tune="$4" combo_dir="$5"
    local log_file="$combo_dir/${job_id}.log"
    if [ -f "$log_file" ]; then
        echo "" >> "$log_file"
        echo "── RETRY $(date -u -d '+9 hours' '+%Y-%m-%d %H:%M:%S KST') ──" >> "$log_file"
    fi
    JOB_ID="$job_id" \
    BBN_INPUT_FILE="${CONDITION_FILES[$cond]}" \
    TEST_OUTPUT_DIR="$combo_dir" \
    nChains="$NCHAINS" \
    nIter="$niter" \
    nBurnin="$tune" \
    nThin="$NTHIN" \
    TASK_TYPE="$TASK_TYPE" \
    S3_BUCKET="$S3_BUCKET" \
    AWS_REGION="$AWS_REGION" \
    PYTENSOR_FLAGS="base_compiledir=/tmp/pt_${cond}" \
        bash "$SCRIPT_DIR/runner.sh" >> "$log_file" 2>&1
}

result_file_for() {
    local cond="$1" tune="$2" draw="$3" rep="$4"
    echo "$OUT_DIR/tune${tune}_draw${draw}/results_bbn_results-pre-fp-${cond}-tune${tune}-draw${draw}-rep${rep}.json"
}

# ─────────────────────────────────────────────────────────────
run_combo() {
    local tune="$1" draw="$2"
    local niter=$((tune + draw))
    local combo_dir="$OUT_DIR/tune${tune}_draw${draw}"
    mkdir -p "$combo_dir"

    echo ""
    echo "▶ tune=$tune  draw=$draw  (nIter=$niter) 실행 중..."

    local flat_keys=()
    for cond in "${CONDITION_KEYS[@]}"; do
        for rep in $(seq 1 $NREPS); do
            flat_keys+=("${cond}:${rep}")
        done
    done

    # ── 1차: 병렬 배치 실행 ───────────────────────────────────
    local total=${#flat_keys[@]}
    local i=0
    while [ $i -lt $total ]; do
        local batch_pids=() batch_names=() batch_starts=()
        for ((b = 0; b < MAX_JOBS && i + b < total; b++)); do
            local item="${flat_keys[$((i + b))]}"
            local cond="${item%%:*}"
            local rep="${item##*:}"
            local job_id="pre-fp-${cond}-tune${tune}-draw${draw}-rep${rep}"
            batch_names+=("$job_id")
            echo "  ▷ $job_id 시작"
            run_job "$job_id" "$cond" "$niter" "$tune" "$combo_dir" &
            batch_pids+=($!)
            batch_starts+=($(date +%s))
        done

        for k in "${!batch_pids[@]}"; do
            local _elapsed _m _s
            if wait "${batch_pids[$k]}"; then
                _elapsed=$(( $(date +%s) - ${batch_starts[$k]} ))
                _m=$((_elapsed / 60)); _s=$((_elapsed % 60))
                echo "  ✅ ${batch_names[$k]}  (${_m}m ${_s}s)"
            else
                _elapsed=$(( $(date +%s) - ${batch_starts[$k]} ))
                _m=$((_elapsed / 60)); _s=$((_elapsed % 60))
                echo "  ❌ ${batch_names[$k]} 실패  (${_m}m ${_s}s)"
            fi
        done
        i=$((i + MAX_JOBS))
    done

    # ── 2차: 결과 파일 없는 job 순차 재시도 ──────────────────
    local retry_keys=()
    for item in "${flat_keys[@]}"; do
        local cond="${item%%:*}"
        local rep="${item##*:}"
        if [ ! -f "$(result_file_for "$cond" "$tune" "$draw" "$rep")" ]; then
            retry_keys+=("$item")
        fi
    done

    if [ ${#retry_keys[@]} -gt 0 ]; then
        echo "  🔄 ${#retry_keys[@]}개 job 재시도 (순차 실행)..."
        for item in "${retry_keys[@]}"; do
            local cond="${item%%:*}"
            local rep="${item##*:}"
            local job_id="pre-fp-${cond}-tune${tune}-draw${draw}-rep${rep}"
            local _rs _elapsed _m _s
            _rs=$(date +%s)
            if run_job "$job_id" "$cond" "$niter" "$tune" "$combo_dir"; then
                _elapsed=$(( $(date +%s) - _rs ))
                _m=$((_elapsed / 60)); _s=$((_elapsed % 60))
                echo "  ✅ $job_id (재시도)  (${_m}m ${_s}s)"
            else
                _elapsed=$(( $(date +%s) - _rs ))
                _m=$((_elapsed / 60)); _s=$((_elapsed % 60))
                echo "  ❌ $job_id 재시도 실패  (${_m}m ${_s}s) — 로그: $combo_dir/${job_id}.log"
            fi
        done
    fi

    # ── rep별 단조성 검사 및 집계 ──────────────────────────────
    local key="${tune}:${draw}"
    PASS_COUNT[$key]=0
    PARTIAL_COUNT[$key]=0
    FAIL_COUNT[$key]=0
    MISSING_COUNT[$key]=0

    echo ""
    echo "  ── tune=$tune draw=$draw 비교 결과 ──"
    for rep in $(seq 1 $NREPS); do
        local cmp_args=() missing=false
        for cond in "${CONDITION_KEYS[@]}"; do
            local result_file
            result_file="$(result_file_for "$cond" "$tune" "$draw" "$rep")"
            if [ ! -f "$result_file" ]; then
                echo "  [rep${rep}] ⚠ 결과 파일 없음 — $combo_dir/pre-fp-${cond}-tune${tune}-draw${draw}-rep${rep}.log"
                missing=true
                MISSING_COUNT[$key]=$(( ${MISSING_COUNT[$key]} + 1 ))
                break
            fi
            cmp_args+=("${CONDITION_LABELS[$cond]}=$result_file")
        done
        [ "$missing" = true ] && continue

        local cmp_log="$combo_dir/comparison_rep${rep}.log"
        python "$SCRIPT_DIR/compare_pfd_hdi.py" "${cmp_args[@]}" > "$cmp_log" 2>&1
        echo "  [rep${rep}]"
        grep -E "median|mean|PASS|PARTIAL|FAIL" "$cmp_log" | sed 's/^/    /'

        if grep -q "  PASS —" "$cmp_log"; then
            PASS_COUNT[$key]=$(( ${PASS_COUNT[$key]} + 1 ))
        elif grep -q "  PARTIAL —" "$cmp_log"; then
            PARTIAL_COUNT[$key]=$(( ${PARTIAL_COUNT[$key]} + 1 ))
        else
            FAIL_COUNT[$key]=$(( ${FAIL_COUNT[$key]} + 1 ))
        fi
    done

    local p=${PASS_COUNT[$key]}
    local pa=${PARTIAL_COUNT[$key]}
    local f=${FAIL_COUNT[$key]}
    local m=${MISSING_COUNT[$key]}
    local label
    if [ "$p" -eq "$NREPS" ]; then
        label="✓ ALL PASS"
    elif [ "$f" -eq 0 ] && [ "$m" -eq 0 ]; then
        label="△ PARTIAL"
    else
        label="✗ FAIL/MISSING"
    fi
    echo "  → tune=$tune draw=$draw: PASS=${p}/${NREPS} PARTIAL=${pa} FAIL=${f} MISSING=${m}  $label"
}

# ─────────────────────────────────────────────────────────────
print_summary_table() {
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "  최종 요약 테이블  (PASS count / $NREPS reps)"
    echo "  ✓ = ALL PASS  △ = PARTIAL only  ✗ = FAIL/MISSING 포함"
    echo "════════════════════════════════════════════════════════════════"

    local header
    header="$(printf '  %-14s' 'tune \ draws')"
    for draw in "${DRAWS_LIST[@]}"; do
        header+="$(printf '%12s' "draws=$draw")"
    done
    echo "$header"
    echo "  $(printf -- '-%.0s' $(seq 1 $((14 + 12 * ${#DRAWS_LIST[@]}))))"

    local best_tune="" best_draw="" best_found=false

    for tune in "${TUNE_LIST[@]}"; do
        local row
        row="$(printf '  %-14s' "tune=$tune")"
        for draw in "${DRAWS_LIST[@]}"; do
            local key="${tune}:${draw}"
            local p="${PASS_COUNT[$key]:-?}"
            local pa="${PARTIAL_COUNT[$key]:-?}"
            local f="${FAIL_COUNT[$key]:-?}"
            local m="${MISSING_COUNT[$key]:-?}"
            local cell
            if [ "$p" = "?" ]; then
                cell="?"
            elif [ "$p" -eq "$NREPS" ]; then
                cell="${p}/${NREPS} ✓"
                if [ "$best_found" = false ]; then
                    best_tune="$tune"
                    best_draw="$draw"
                    best_found=true
                fi
            elif [ "$f" -eq 0 ] && [ "$m" -eq 0 ]; then
                cell="${p}/${NREPS} △"
            else
                cell="${p}/${NREPS} ✗"
            fi
            row+="$(printf '%12s' "$cell")"
        done
        echo "$row"
    done

    echo ""
    if [ "$best_found" = true ]; then
        echo "  ★ 추천 설정 (전 rep PASS 기준 최솟값):"
        echo ""
        echo "    chains = 1"
        echo "    tune   = $best_tune   (nBurnin)"
        echo "    draws  = $best_draw   (nIter = $((best_tune + best_draw)))"
        echo "    thin   = 1"
        echo ""
        echo "  → exp_fp.sh에서 아래 값으로 설정하세요:"
        echo "    NBURN=$best_tune"
        echo "    DRAWS_LIST=($best_draw)"
        echo "    NCHAINS=1"
        echo "    NTHIN=1"
    else
        echo "  ⚠ 전 rep PASS 조합 없음 — TUNE_LIST / DRAWS_LIST 범위 확대 필요"
    fi
    echo "════════════════════════════════════════════════════════════════"
}

# ─────────────────────────────────────────────────────────────
main() {
    trap 'echo ""; echo "⚠ 중단됨 — 실행 중인 job 종료 중..."; kill 0' INT TERM

    local _start_ts _start_sec
    _start_ts="$(date -u -d '+9 hours' '+%Y-%m-%d %H:%M:%S KST')"
    _start_sec=$(date +%s)

    local total_combos=$(( ${#TUNE_LIST[@]} * ${#DRAWS_LIST[@]} ))
    local total_jobs=$(( total_combos * ${#CONDITION_KEYS[@]} * NREPS ))

    echo "=================================================="
    echo "사전 실험: FP draws 탐색 (단조성 기준)"
    echo "  chains=1, thin=1 고정"
    echo "  tune   : ${TUNE_LIST[*]}  (기본 1000 고정)"
    echo "  draws  : ${DRAWS_LIST[*]}"
    echo "  reps   : $NREPS"
    echo "  조합 수 : $total_combos  (총 runner 실행: $total_jobs)"
    echo "  동시실행 : $MAX_JOBS"
    echo "  출력    : $OUT_DIR"
    echo "  시작    : $_start_ts"
    echo "=================================================="

    for tune in "${TUNE_LIST[@]}"; do
        for draw in "${DRAWS_LIST[@]}"; do
            run_combo "$tune" "$draw"
        done
    done

    print_summary_table

    local _end_ts _end_sec _elapsed _min _sec
    _end_ts="$(date -u -d '+9 hours' '+%Y-%m-%d %H:%M:%S KST')"
    _end_sec=$(date +%s)
    _elapsed=$((_end_sec - _start_sec))
    _min=$((_elapsed / 60))
    _sec=$((_elapsed % 60))

    echo ""
    echo "=================================================="
    echo "사전 실험 (FP) 완료: $OUT_DIR"
    echo "시작: $_start_ts  /  종료: $_end_ts"
    echo "총 소요 시간: ${_min}m ${_sec}s"
    echo "=================================================="
}

main 2>&1 | tee "$LOG_FILE"
echo "콘솔 로그 저장됨: $LOG_FILE"
