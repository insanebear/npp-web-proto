#!/usr/bin/env bash
# 사전 실험: FP draws 탐색 (median 안정성 기준)
#   exp_fp.sh 실행에 앞서 안정적인 draws 최솟값 탐색
#   chains=1, thin=1 고정
#   tune=1000 고정, draws 그리드 서치로 median이 안정적으로 나오는 최솟값 탐색
#   tune을 여러 값으로 비교할 경우 TUNE_LIST에 값 추가
#   조건: FP-200 단일 조건으로 대표 테스트
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
DRAWS_LIST=(1000 2000 3000)
NREPS=30
MAX_JOBS="${MAX_JOBS:-4}"

S3_BUCKET="dummy"
AWS_REGION="ap-northeast-2"
TASK_TYPE="bbn_inference"

CONDITION_KEYS=(fp-200)
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
declare -A STABILITY
declare -A CV

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

    # ── rep 간 autocorrelation 비교 HTML 생성 ─────────────────────
    local autocorr_json_files=()
    for cond in "${CONDITION_KEYS[@]}"; do
        for rep in $(seq 1 $NREPS); do
            local af="$combo_dir/autocorr-pre-fp-${cond}-tune${tune}-draw${draw}-rep${rep}.json"
            [ -f "$af" ] && autocorr_json_files+=("$af")
        done
    done
    if [ ${#autocorr_json_files[@]} -gt 1 ]; then
        local combined_html="$combo_dir/autocorr_combined-tune${tune}_draw${draw}.html"
        python "$SCRIPT_DIR/combine_autocorr.py" "$combined_html" "${autocorr_json_files[@]}" \
            && echo "  📊 Autocorr 비교 HTML: $combined_html"
    fi

    # ── 조건별 median 안정성 체크 ─────────────────────────────────
    echo ""
    echo "  ── tune=$tune draw=$draw  median 안정성 (relative range) ──"
    for cond in "${CONDITION_KEYS[@]}"; do
        local rep_files=() all_present=true
        for rep in $(seq 1 $NREPS); do
            local rf
            rf="$(result_file_for "$cond" "$tune" "$draw" "$rep")"
            if [ ! -f "$rf" ]; then
                all_present=false
                break
            fi
            rep_files+=("$rf")
        done

        if [ "$all_present" = false ]; then
            echo "    [${CONDITION_LABELS[$cond]}] ⚠ 결과 파일 누락 — 계산 불가"
            STABILITY["${cond}:${tune}:${draw}"]="N/A"
            continue
        fi

        local stab_out
        stab_out=$(python "$SCRIPT_DIR/check_median_stability.py" \
            "${CONDITION_LABELS[$cond]}" "${rep_files[@]}" 2>&1)
        echo "$stab_out" | grep -v "^STABILITY_PCT:" | grep -v "^CV_PCT:" | sed 's/^/  /'

        local pct cv_val
        pct=$(echo "$stab_out" | grep "^STABILITY_PCT:" | cut -d: -f2)
        cv_val=$(echo "$stab_out" | grep "^CV_PCT:" | cut -d: -f2)
        STABILITY["${cond}:${tune}:${draw}"]="${pct:-N/A}"
        CV["${cond}:${tune}:${draw}"]="${cv_val:-N/A}"
    done
}

# ─────────────────────────────────────────────────────────────
print_summary_table() {
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "  Median 안정성 요약 — CV (변동계수) & relative range across reps"
    echo "  CV = std / mean  |  relative range = (max - min) / mean  (참고)"
    echo "════════════════════════════════════════════════════════════════"

    for tune in "${TUNE_LIST[@]}"; do
        local hdr
        hdr="$(printf '  %-16s' "tune=$tune")"
        for draw in "${DRAWS_LIST[@]}"; do
            hdr+="$(printf '%20s' "draw=$draw")"
        done
        echo "$hdr"
        echo "  $(printf -- '-%.0s' $(seq 1 $((16 + 20 * ${#DRAWS_LIST[@]}))))"

        # CV 행
        for cond in "${CONDITION_KEYS[@]}"; do
            local row
            row="$(printf '  %-10s %-6s' "${CONDITION_LABELS[$cond]}" "(CV)")"
            for draw in "${DRAWS_LIST[@]}"; do
                local key="${cond}:${tune}:${draw}"
                local val="${CV[$key]:-?}"
                local cell
                if [ "$val" = "?" ] || [ "$val" = "N/A" ]; then
                    cell="$val"
                else
                    cell="${val}%"
                fi
                row+="$(printf '%20s' "$cell")"
            done
            echo "$row"
        done

        # relative range 행 (참고)
        for cond in "${CONDITION_KEYS[@]}"; do
            local row
            row="$(printf '  %-10s %-6s' "${CONDITION_LABELS[$cond]}" "(RR)")"
            for draw in "${DRAWS_LIST[@]}"; do
                local key="${cond}:${tune}:${draw}"
                local val="${STABILITY[$key]:-?}"
                local cell
                if [ "$val" = "?" ] || [ "$val" = "N/A" ]; then
                    cell="$val"
                else
                    cell="${val}%"
                fi
                row+="$(printf '%20s' "$cell")"
            done
            echo "$row"
        done
    done
    echo "════════════════════════════════════════════════════════════════"
}

CV_THRESHOLD=5.0

print_conclusion() {
    echo ""
    echo "════════════════════════════════════════════════════════════════"
    echo "  결론 — CV < ${CV_THRESHOLD}% 기준"
    echo "════════════════════════════════════════════════════════════════"

    local recommended_draw=""
    for tune in "${TUNE_LIST[@]}"; do
        for cond in "${CONDITION_KEYS[@]}"; do
            echo "  [${CONDITION_LABELS[$cond]}]"
            for draw in "${DRAWS_LIST[@]}"; do
                local key="${cond}:${tune}:${draw}"
                local cv_val="${CV[$key]:-N/A}"
                if [ "$cv_val" = "N/A" ] || [ "$cv_val" = "?" ]; then
                    echo "    draw=$draw:  CV=N/A  →  계산 불가"
                else
                    local pass
                    pass=$(awk -v v="$cv_val" -v t="$CV_THRESHOLD" 'BEGIN { print (v < t) ? "yes" : "no" }')
                    if [ "$pass" = "yes" ]; then
                        echo "    draw=$draw:  CV=${cv_val}%  →  기준 충족 (< ${CV_THRESHOLD}%)"
                        [ -z "$recommended_draw" ] && recommended_draw="$draw"
                    else
                        echo "    draw=$draw:  CV=${cv_val}%  →  기준 미달 (≥ ${CV_THRESHOLD}%)"
                    fi
                fi
            done
        done
    done

    echo ""
    if [ -n "$recommended_draw" ]; then
        echo "  ✅ 권장 draw: $recommended_draw  (CV < ${CV_THRESHOLD}% 충족하는 최솟값)"
    else
        echo "  ⚠ 모든 draw에서 CV ≥ ${CV_THRESHOLD}% — draw=${DRAWS_LIST[-1]} 보수적 채택 권장"
        echo "    (NREPS 추가 또는 draw 범위 확장 검토)"
    fi
    echo "════════════════════════════════════════════════════════════════"
}

# ─────────────────────────────────────────────────────────────
main() {
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
    print_conclusion

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

trap 'trap - INT TERM; echo ""; echo "⚠ 중단됨 — 실행 중인 job 종료 중..."; kill 0' INT TERM
main 2>&1 | tee "$LOG_FILE"
echo "콘솔 로그 저장됨: $LOG_FILE"
