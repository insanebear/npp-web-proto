#!/usr/bin/env bash
# 실험 A: SDLC 비교
#   FP=200 고정, SDLC 속성 all-Low / all-Medium / all-High 비교
#   Draw=10000 (사전 실험으로 결정), PILOT_NREPS회 pilot -> power analysis -> JT test
#   가설: PFD(all-high) < PFD(all-medium) < PFD(all-low)
#
# 사용법:
#   bash scripts/experiments/exp_sdlc.sh
#   MAX_JOBS=3 bash scripts/experiments/exp_sdlc.sh        # 동시 실행 수 조절
#   RESULT_DIR=<path> bash scripts/experiments/exp_sdlc.sh # 기존 데이터 재분석

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"

# ── 실험 설정 ─────────────────────────────────────────────────
NBURN=1000
NCHAINS=1
NTHIN=1
DRAW=10000
PILOT_NREPS=10
MAX_NREPS=50
MAX_JOBS="${MAX_JOBS:-1}"

S3_BUCKET="dummy"
AWS_REGION="ap-northeast-2"
TASK_TYPE="bbn_inference"

CONDITION_KEYS=(all-low all-medium all-high)
declare -A CONDITION_FILES
CONDITION_FILES[all-low]="$PROJECT_ROOT/tempDoc/my-bbn-input-all-low.json"
CONDITION_FILES[all-medium]="$PROJECT_ROOT/tempDoc/my-bbn-input.json"
CONDITION_FILES[all-high]="$PROJECT_ROOT/tempDoc/my-bbn-input-all-high.json"
declare -A CONDITION_LABELS
CONDITION_LABELS[all-low]="All-Low"
CONDITION_LABELS[all-medium]="All-Medium"
CONDITION_LABELS[all-high]="All-High"

# JT test 순서: PFD 오름차순 (all-high PFD 가장 낮음, all-low 가장 높음)
JT_ORDER=(all-high all-medium all-low)

# ── 출력 디렉토리 & 로그 설정 ─────────────────────────────────
_KST_TS="$(date -u -d '+9 hours' +%y%m%d_%H%M%S)"
if [ -n "${RESULT_DIR:-}" ]; then
    OUT_DIR="$RESULT_DIR"
    LOG_FILE="$OUT_DIR/exp_sdlc_analysis_${_KST_TS}.log"
else
    OUT_DIR="$PROJECT_ROOT/tempDoc/hybrid-tool-test/exp-sdlc-$_KST_TS"
    mkdir -p "$OUT_DIR"
    LOG_FILE="$OUT_DIR/exp_sdlc_run.log"
fi

# ── 헬퍼 함수 ─────────────────────────────────────────────────
make_job_id() { echo "sdlc-${1}-draw${DRAW}-rep${3}"; }

result_file_for() {
    local cond="$1" draw="$2" rep="$3"
    echo "$OUT_DIR/draw${draw}/results_bbn_results-sdlc-${cond}-draw${draw}-rep${rep}.json"
}

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
        bash "$SCRIPT_DIR/../lib/runner.sh" >> "$log_file" 2>&1
}

# rep from_rep~to_rep 실행 (배치 + 재시도)
run_reps() {
    local from_rep=$1 to_rep=$2 draw=$3 draw_dir=$4
    local niter=$((NBURN + draw))

    local flat_keys=()
    for cond in "${CONDITION_KEYS[@]}"; do
        for rep in $(seq "$from_rep" "$to_rep"); do
            flat_keys+=("${cond}:${rep}")
        done
    done

    # 1차: 병렬 배치 실행
    local total=${#flat_keys[@]} i=0
    while [ $i -lt $total ]; do
        local batch_pids=() batch_names=() batch_starts=()
        for ((b = 0; b < MAX_JOBS && i + b < total; b++)); do
            local item="${flat_keys[$((i + b))]}"
            local cond="${item%%:*}" rep="${item##*:}"
            local job_id; job_id=$(make_job_id "$cond" "$draw" "$rep")
            batch_names+=("$job_id")
            echo "  > $job_id 시작"
            run_job "$job_id" "$cond" "$niter" "$draw_dir" &
            batch_pids+=($!)
            batch_starts+=($(date +%s))
        done
        for k in "${!batch_pids[@]}"; do
            local _elapsed _m _s
            if wait "${batch_pids[$k]}"; then
                _elapsed=$(( $(date +%s) - ${batch_starts[$k]} ))
                _m=$((_elapsed / 60)); _s=$((_elapsed % 60))
                echo "  OK ${batch_names[$k]}  (${_m}m ${_s}s)"
            else
                _elapsed=$(( $(date +%s) - ${batch_starts[$k]} ))
                _m=$((_elapsed / 60)); _s=$((_elapsed % 60))
                echo "  FAIL ${batch_names[$k]}  (${_m}m ${_s}s)"
            fi
        done
        i=$((i + MAX_JOBS))
    done

    # 2차: 결과 파일 없는 job 순차 재시도
    local retry_keys=()
    for item in "${flat_keys[@]}"; do
        local cond="${item%%:*}" rep="${item##*:}"
        [ ! -f "$(result_file_for "$cond" "$draw" "$rep")" ] && retry_keys+=("$item")
    done

    if [ ${#retry_keys[@]} -gt 0 ]; then
        echo ""
        echo "  [재시도] ${#retry_keys[@]}개 job 순차 실행 ..."
        for item in "${retry_keys[@]}"; do
            local cond="${item%%:*}" rep="${item##*:}"
            local job_id; job_id=$(make_job_id "$cond" "$draw" "$rep")
            local _rs _elapsed _m _s
            echo "  > $job_id 재시도"
            _rs=$(date +%s)
            if run_job "$job_id" "$cond" "$niter" "$draw_dir"; then
                _elapsed=$(( $(date +%s) - _rs ))
                _m=$((_elapsed / 60)); _s=$((_elapsed % 60))
                echo "  OK $job_id (재시도 성공)  (${_m}m ${_s}s)"
            else
                _elapsed=$(( $(date +%s) - _rs ))
                _m=$((_elapsed / 60)); _s=$((_elapsed % 60))
                echo "  FAIL $job_id (재시도 실패)  (${_m}m ${_s}s) -- 로그: $draw_dir/${job_id}.log"
            fi
        done
    fi
}

# 각 조건에서 연속으로 존재하는 rep 수 중 최솟값 반환
detect_nreps() {
    local draw=$1
    local min_reps=$MAX_NREPS
    for cond in "${CONDITION_KEYS[@]}"; do
        local count=0
        for rep in $(seq 1 "$MAX_NREPS"); do
            if [ -f "$(result_file_for "$cond" "$draw" "$rep")" ]; then
                count=$rep
            else
                break
            fi
        done
        [ $count -lt $min_reps ] && min_reps=$count
    done
    echo "$min_reps"
}

# JT test / power analysis 인수 문자열 생성 (JT_ORDER 순서)
build_jt_args() {
    local nreps=$1 draw=$2
    for cond in "${JT_ORDER[@]}"; do
        local files=""
        for rep in $(seq 1 "$nreps"); do
            local f; f=$(result_file_for "$cond" "$draw" "$rep")
            f=$(cygpath -w "$f" 2>/dev/null || echo "$f")
            [ -z "$files" ] && files="$f" || files="$files,$f"
        done
        echo "${CONDITION_LABELS[$cond]}=$files"
    done
}

# Power analysis 실행 후 권장 NREPS를 stdout으로 반환
# 전체 출력은 stderr로 전달 (콘솔 + 로그 파일에 표시됨)
run_power_analysis() {
    local nreps=$1 draw=$2 draw_dir=$3
    local jt_args=()
    while IFS= read -r line; do jt_args+=("$line"); done \
        < <(build_jt_args "$nreps" "$draw")

    local win_draw_dir
    win_draw_dir=$(cygpath -w "$draw_dir" 2>/dev/null || echo "$draw_dir")

    local output
    output=$(python "$SCRIPT_DIR/../lib/power_test_jt.py" \
        "${jt_args[@]}" \
        --alpha 0.05 --target-power 0.80 --B 1000 \
        --out-dir "$win_draw_dir" 2>&1)

    echo "$output" >&2
    echo "$output" > "$draw_dir/power_analysis.log"

    echo "$output" | grep "^RECOMMENDED_NREPS:" | cut -d: -f2 | tr -d ' \r\n'
}

# JT test 실행
run_jt_test() {
    local nreps=$1 draw=$2 draw_dir=$3
    local jt_args=()
    while IFS= read -r line; do jt_args+=("$line"); done \
        < <(build_jt_args "$nreps" "$draw")

    local jt_log="$draw_dir/jt_test_result.log"
    echo ""
    echo "── JT Test 결과 ──────────────────────────────────"
    python "$SCRIPT_DIR/../lib/compare_pfd_jt.py" "${jt_args[@]}" | tee "$jt_log"

    if grep -q "^JT_RESULT:PASS" "$jt_log"; then
        echo "  -> PASS -- 단조 순서 통계적으로 확인됨"
    else
        echo "  -> FAIL -- 단조 순서 통계적으로 확인되지 않음"
    fi
}

main() {
    local _start_ts _start_sec
    _start_ts="$(date -u -d '+9 hours' '+%Y-%m-%d %H:%M:%S KST')"
    _start_sec=$(date +%s)

    echo "=================================================="
    echo "실험 A: SDLC 비교 (FP=200 고정)"
    echo "SDLC 조건   : ${CONDITION_KEYS[*]}"
    echo "Draw        : $DRAW  (nBurn=$NBURN)"
    if [ -n "${RESULT_DIR:-}" ]; then
        echo "모드         : 기존 데이터 재분석 (RESULT_DIR=$RESULT_DIR)"
    else
        echo "Pilot NREPS : $PILOT_NREPS"
        echo "Max NREPS   : $MAX_NREPS"
        echo "Max 동시 실행: $MAX_JOBS"
    fi
    echo "출력         : $OUT_DIR"
    echo "시작         : $_start_ts"
    echo "=================================================="

    local draw=$DRAW
    local draw_dir="$OUT_DIR/draw${draw}"
    mkdir -p "$draw_dir"

    local FINAL_NREPS

    if [ -n "${RESULT_DIR:-}" ]; then
        # ── 기존 데이터 재분석 모드 ───────────────────────────
        echo ""
        echo "> 기존 결과 파일 확인 ..."
        FINAL_NREPS=$(detect_nreps "$draw")
        if [ "$FINAL_NREPS" -eq 0 ]; then
            echo "ERROR: $draw_dir 에서 결과 파일을 찾을 수 없습니다"
            exit 1
        fi
        echo "  감지된 NREPS: $FINAL_NREPS"
    else
        # ── Phase 1: Pilot run ────────────────────────────────
        echo ""
        echo "> Phase 1: Pilot run  (rep 1~$PILOT_NREPS, draw=$draw) ..."
        run_reps 1 "$PILOT_NREPS" "$draw" "$draw_dir"
        echo "Pilot 완료"

        # ── Power analysis ────────────────────────────────────
        echo ""
        echo "> Power analysis ..."
        FINAL_NREPS=$(run_power_analysis "$PILOT_NREPS" "$draw" "$draw_dir")

        if [ -z "$FINAL_NREPS" ] || ! [[ "$FINAL_NREPS" =~ ^[0-9]+$ ]]; then
            echo "WARNING: NREPS 파싱 실패, Pilot NREPS=$PILOT_NREPS 사용"
            FINAL_NREPS=$PILOT_NREPS
        fi
        if [ "$FINAL_NREPS" -gt "$MAX_NREPS" ]; then
            echo "WARNING: 권장 NREPS=$FINAL_NREPS > MAX_NREPS=$MAX_NREPS -> MAX_NREPS 적용"
            FINAL_NREPS=$MAX_NREPS
        fi
        echo "  최종 NREPS: $FINAL_NREPS"

        # ── Phase 2: 추가 실행 (필요한 경우) ─────────────────
        if [ "$FINAL_NREPS" -gt "$PILOT_NREPS" ]; then
            echo ""
            echo "> Phase 2: 추가 실행  (rep $((PILOT_NREPS + 1))~$FINAL_NREPS) ..."
            run_reps $((PILOT_NREPS + 1)) "$FINAL_NREPS" "$draw" "$draw_dir"
            echo "추가 실행 완료"
        else
            echo "  Pilot NREPS로 충분 -- 추가 실행 없음"
        fi
    fi

    # ── Power analysis (재분석 모드) ──────────────────────────
    if [ -n "${RESULT_DIR:-}" ]; then
        echo ""
        echo "> Power analysis ..."
        run_power_analysis "$FINAL_NREPS" "$draw" "$draw_dir" > /dev/null
    fi

    # ── JT test ───────────────────────────────────────────────
    run_jt_test "$FINAL_NREPS" "$draw" "$draw_dir"

    local _end_ts _end_sec _elapsed _min _sec
    _end_ts="$(date -u -d '+9 hours' '+%Y-%m-%d %H:%M:%S KST')"
    _end_sec=$(date +%s)
    _elapsed=$((_end_sec - _start_sec))
    _min=$((_elapsed / 60))
    _sec=$((_elapsed % 60))

    echo ""
    echo "=================================================="
    echo "실험 A 완료: $OUT_DIR"
    echo "시작: $_start_ts"
    echo "종료: $_end_ts"
    echo "총 소요 시간: ${_min}m ${_sec}s"
    echo "=================================================="
}

trap 'trap - INT TERM; echo ""; echo "WARNING: 중단됨 -- 실행 중인 job 종료 중..."; kill 0' INT TERM
main 2>&1 | tee "$LOG_FILE"
echo "콘솔 로그 저장됨: $LOG_FILE"
