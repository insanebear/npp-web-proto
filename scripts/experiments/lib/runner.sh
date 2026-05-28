#!/usr/bin/env bash
# 로컬 실행 core — run_local.sh 및 실험 스크립트에서 공통 호출
#
# Required env vars:
#   JOB_ID, TEST_OUTPUT_DIR
#   TASK_TYPE, S3_BUCKET, AWS_REGION
#   nChains, nIter, nBurnin, nThin
#
# Optional env vars:
#   CONDA_ENV_NAME  (default: gxx_env_311)
#   BBN_INPUT_FILE, FP_Input, TEST_MODE, 기타 task 설정

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

CONDA_ENV_NAME="${CONDA_ENV_NAME:-gxx_env_311}"

# ── 필수 env var 검증 ─────────────────────────────────────────
for var in JOB_ID TEST_OUTPUT_DIR TASK_TYPE S3_BUCKET AWS_REGION nChains nIter nBurnin nThin; do
    if [ -z "${!var}" ]; then
        echo "❌ 필수 환경변수 미설정: $var" >&2
        exit 1
    fi
done

# ── conda 초기화 및 환경 활성화 ──────────────────────────────
CONDA_BASE=$(conda info --base 2>/dev/null || echo "$HOME/miniconda3")
source "$CONDA_BASE/etc/profile.d/conda.sh" 2>/dev/null || {
    echo "❌ conda를 찾을 수 없습니다. miniconda가 설치되어 있는지 확인하세요." >&2
    exit 1
}

conda activate "$CONDA_ENV_NAME" 2>/dev/null || {
    echo "❌ conda 환경 '$CONDA_ENV_NAME'을 활성화할 수 없습니다." >&2
    echo "  conda env list 로 환경 목록을 확인하세요." >&2
    exit 1
}

echo "✅ conda 환경 활성화: $CONDA_ENV_NAME ($(python --version))"

# ── Python 3.11 버전 확인 ─────────────────────────────────────
PYTHON_MAJOR=$(python -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(python -c "import sys; print(sys.version_info.minor)")
if [ "$PYTHON_MAJOR" -ne 3 ] || [ "$PYTHON_MINOR" -ne 11 ]; then
    echo "❌ Python 3.11이 필요합니다. 현재: $(python --version)" >&2
    exit 1
fi

# ── pymc 설치 확인 ───────────────────────────────────────────
if ! python -c "import pymc" &>/dev/null; then
    echo "❌ pymc가 설치되어 있지 않습니다." >&2
    echo "  conda install -c conda-forge pymc 로 설치하세요." >&2
    exit 1
fi

echo "✅ 의존성 확인 완료 (JOB_ID: $JOB_ID)"

# ── Python 경로 및 출력 디렉토리 설정 ────────────────────────
export PYTHONPATH="$PROJECT_ROOT/server_min:$PROJECT_ROOT/Dockers/HybridTool:$PYTHONPATH"
mkdir -p "$TEST_OUTPUT_DIR"

# ── 실행 ─────────────────────────────────────────────────────
cd "$PROJECT_ROOT"
python "$SCRIPT_DIR/run_local.py"
