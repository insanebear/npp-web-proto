#!/usr/bin/env bash
# 실험 B: FP sweep
#   SDLC 속성 all-Medium 고정, FP=50 / 200 / 1000 비교
#   Draw: 1000~5000 (1000 단위), 각 NREPS회 반복
#   비교: draw level별 × rep별 조건간 단조성 검사 (FP-1000 > FP-200 > FP-50)
#
# 사용법:
#   bash scripts/experiments/exp_fp.sh
#   MAX_JOBS=3 bash scripts/experiments/exp_fp.sh   # 동시 실행 수 조절

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# ── 실험 설정 ─────────────────────────────────────────────────
NBURN=1000
NCHAINS=1
NTHIN=1
DRAWS_LIST=(1000)
# DRAWS_LIST=(6000 7000 8000 9000 10000)
NREPS=3
MAX_JOBS="${MAX_JOBS:-1}"   # 동시 실행 수 (부하가 크면 줄이세요)

S3_BUCKET="dummy"
AWS_REGION="ap-northeast-2"
TASK_TYPE="bbn_inference"

# 비교 방향: FP 높을수록 PFD 높아야 함 (FP-1000 > FP-200 > FP-50)
CONDITION_KEYS=(fp-50 fp-200 fp-1000)
COMPARE_ORDER=(fp-1000 fp-200 fp-50)
declare -A CONDITION_FILES
CONDITION_FILES[fp-50]="$PROJECT_ROOT/tempDoc/my-bbn-input-fp50.json"
CONDITION_FILES[fp-200]="$PROJECT_ROOT/tempDoc/my-bbn-input.json"
CONDITION_FILES[fp-1000]="$PROJECT_ROOT/tempDoc/my-bbn-input-fp1000.json"
declare -A CONDITION_LABELS
CONDITION_LABELS[fp-50]="FP-50"
CONDITION_LABELS[fp-200]="FP-200"
CONDITION_LABELS[fp-1000]="FP-1000"

# ── 출력 디렉토리 & 로그 설정 ─────────────────────────────────
_KST_TS="$(date -u -d '+9 hours' +%y%m%d_%H%M%S)"
OUT_DIR="$PROJECT_ROOT/tempDoc/hybrid-tool-test/exp-fp-$_KST_TS"
mkdir -p "$OUT_DIR"
LOG_FILE="$OUT_DIR/exp_fp_run.log"

# draw_dir: draw level별 하위 폴더 ($OUT_DIR/draw{N}/)
run_job() {
    local job_id="$1" cond="$2" niter="$3" draw_dir="$4"
    local log_file="$draw_dir/${job_id}.log"
    if [ -f "$log_file" ]; then
        echo "" >> "$log_file"
        echo "── RETRY $(date -u -d '+9 hours' '+%Y-%m-%d %H:%M:%S KST') ──" >> "$log_file"
    fi
    JOB_ID="$job_id" \
    BBN_INPUT_FILE="${CONDITION_FILES[$cond]}" \
    TEST_OUTPUT_DIR="$draw_dir" \
    nChains="$NCHAINS" \
    nIter="$niter" \
    nBurnin="$NBURN" \
    nThin="$NTHIN" \
    TASK_TYPE="$TASK_TYPE" \
    S3_BUCKET="$S3_BUCKET" \
    AWS_REGION="$AWS_REGION" \
    PYTENSOR_FLAGS="base_compiledir=/tmp/pytensor_${job_id}" \
        bash "$SCRIPT_DIR/runner.sh" >> "$log_file" 2>&1
}

result_file_for() {
    local cond="$1" draw="$2" rep="$3"
    echo "$OUT_DIR/draw${draw}/results_bbn_results-${cond}-draw${draw}-rep${rep}.json"
}

main() {
    trap 'echo ""; echo "⚠ 중단됨 — 실행 중인 job 종료 중..."; kill 0' INT TERM

    local _start_ts _start_sec
    _start_ts="$(date -u -d '+9 hours' '+%Y-%m-%d %H:%M:%S KST')"
    _start_sec=$(date +%s)

    echo "=================================================="
    echo "실험 B: FP sweep (SDLC all-Medium 고정)"
    echo "FP 조건    : 50 / 200 / 1000"
    echo "Draw levels: ${DRAWS_LIST[*]}"
    echo "Reps       : $NREPS"
    echo "Max 동시 실행: $MAX_JOBS"
    echo "출력        : $OUT_DIR"
    echo "콘솔 로그   : $LOG_FILE"
    echo "시작        : $_start_ts"
    echo "=================================================="

    for draw in "${DRAWS_LIST[@]}"; do
        niter=$((NBURN + draw))
        draw_dir="$OUT_DIR/draw${draw}"
        mkdir -p "$draw_dir"

        echo ""
        echo "▶ Draw=$draw  (nIter=$niter, nBurnin=$NBURN) 실행 중 ..."

        flat_keys=()
        for cond in "${CONDITION_KEYS[@]}"; do
            for rep in $(seq 1 $NREPS); do
                flat_keys+=("${cond}:${rep}")
            done
        done

        # ── 1차: 병렬 배치 실행 ───────────────────────────────
        total=${#flat_keys[@]}
        i=0
        while [ $i -lt $total ]; do
            batch_pids=()
            batch_names=()
            batch_starts=()

            for ((b = 0; b < MAX_JOBS && i + b < total; b++)); do
                item="${flat_keys[$((i + b))]}"
                cond="${item%%:*}"
                rep="${item##*:}"
                job_id="${cond}-draw${draw}-rep${rep}"
                batch_names+=("$job_id")

                echo "  ▷ $job_id 시작"
                run_job "$job_id" "$cond" "$niter" "$draw_dir" &
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

        # ── 2차: 결과 파일 없는 job 순차 재시도 ──────────────
        retry_keys=()
        for item in "${flat_keys[@]}"; do
            cond="${item%%:*}"
            rep="${item##*:}"
            if [ ! -f "$(result_file_for "$cond" "$draw" "$rep")" ]; then
                retry_keys+=("$item")
            fi
        done

        if [ ${#retry_keys[@]} -gt 0 ]; then
            echo ""
            echo "  🔄 ${#retry_keys[@]}개 job 재시도 (순차 실행) ..."
            for item in "${retry_keys[@]}"; do
                cond="${item%%:*}"
                rep="${item##*:}"
                job_id="${cond}-draw${draw}-rep${rep}"
                local _rs _elapsed _m _s
                echo "  ▷ $job_id 재시도"
                _rs=$(date +%s)
                if run_job "$job_id" "$cond" "$niter" "$draw_dir"; then
                    _elapsed=$(( $(date +%s) - _rs ))
                    _m=$((_elapsed / 60)); _s=$((_elapsed % 60))
                    echo "  ✅ $job_id (재시도 성공)  (${_m}m ${_s}s)"
                else
                    _elapsed=$(( $(date +%s) - _rs ))
                    _m=$((_elapsed / 60)); _s=$((_elapsed % 60))
                    echo "  ❌ $job_id (재시도 실패)  (${_m}m ${_s}s) — 로그: $draw_dir/${job_id}.log"
                fi
            done
        fi

        echo "✅ Draw=$draw 실행 완료"

        # ── 비교: rep별로 조건간 단조성 검사 ──────────────────
        echo ""
        echo "── Draw=$draw 비교 결과 ──────────────────────────────"
        infra_fail=false
        mcmc_fail=false

        for rep in $(seq 1 $NREPS); do
            cmp_args=()
            missing=false
            for cond in "${COMPARE_ORDER[@]}"; do
                result_file="$(result_file_for "$cond" "$draw" "$rep")"
                if [ ! -f "$result_file" ]; then
                    echo "  [rep${rep}] ⚠ 결과 파일 없음 (재시도 후에도 실패) — 로그: $draw_dir/${cond}-draw${draw}-rep${rep}.log"
                    missing=true
                    infra_fail=true
                    break
                fi
                cmp_args+=("${CONDITION_LABELS[$cond]}=$result_file")
            done

            [ "$missing" = true ] && continue

            cmp_log="$draw_dir/comparison_rep${rep}.log"
            echo "  [rep${rep}]"
            python "$SCRIPT_DIR/compare_pfd_hdi.py" "${cmp_args[@]}" | tee "$cmp_log"

            if grep -q "FAIL" "$cmp_log"; then
                mcmc_fail=true
            fi
        done

        if [ "$infra_fail" = true ]; then
            echo "  → Draw=$draw: ⚠ job 실패 있음 (인프라) — MAX_JOBS 줄이거나 로그 확인 필요"
        fi
        if [ "$mcmc_fail" = true ]; then
            echo "  → Draw=$draw: ✗ MCMC FAIL — draws/tune 증가 검토 필요"
        fi
        if [ "$infra_fail" = false ] && [ "$mcmc_fail" = false ]; then
            echo "  → Draw=$draw: ✓ 전체 rep PASS"
        fi
    done

    local _end_ts _end_sec _elapsed _min _sec
    _end_ts="$(date -u -d '+9 hours' '+%Y-%m-%d %H:%M:%S KST')"
    _end_sec=$(date +%s)
    _elapsed=$((_end_sec - _start_sec))
    _min=$((_elapsed / 60))
    _sec=$((_elapsed % 60))

    echo ""
    echo "=================================================="
    echo "실험 B 완료: $OUT_DIR"
    echo "시작: $_start_ts"
    echo "종료: $_end_ts"
    echo "총 소요 시간: ${_min}m ${_sec}s"
    echo "=================================================="
}

main 2>&1 | tee "$LOG_FILE"
echo "콘솔 로그 저장됨: $LOG_FILE"
