#!/usr/bin/env bash
# 로컬에서 HybridTool 스크립트를 실행하기 위한 헬퍼 스크립트
# Docker 이미지 빌드 없이 빠르게 테스트할 수 있습니다.
# conda 환경(gxx_env)을 사용합니다.

# 프로젝트 루트 디렉토리 찾기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

CONDA_ENV_NAME="${CONDA_ENV_NAME:-gxx_env_311}"

# conda 초기화 및 환경 활성화
CONDA_BASE=$(conda info --base 2>/dev/null || echo "$HOME/miniconda3")
source "$CONDA_BASE/etc/profile.d/conda.sh" 2>/dev/null || {
    echo "❌ conda를 찾을 수 없습니다. miniconda가 설치되어 있는지 확인하세요."
    exit 1
}

conda activate "$CONDA_ENV_NAME" 2>/dev/null || {
    echo "❌ conda 환경 '$CONDA_ENV_NAME'을 활성화할 수 없습니다."
    echo "  conda env list 로 환경 목록을 확인하세요."
    exit 1
}

echo "✅ conda 환경 활성화: $CONDA_ENV_NAME ($(python --version))"

# Python 3.11 버전 확인 (Docker 환경과 동일해야 함)
PYTHON_MINOR=$(python -c "import sys; print(sys.version_info.minor)")
PYTHON_MAJOR=$(python -c "import sys; print(sys.version_info.major)")
if [ "$PYTHON_MAJOR" -ne 3 ] || [ "$PYTHON_MINOR" -ne 11 ]; then
    echo "❌ Python 3.11이 필요합니다. 현재: $(python --version)"
    echo "  conda install python=3.11 로 설치하거나 다른 환경을 사용하세요."
    exit 1
fi

# pymc 설치 확인
if ! python -c "import pymc" &> /dev/null; then
    echo "❌ pymc가 설치되어 있지 않습니다."
    echo "  conda install -c conda-forge pymc 로 설치하세요."
    exit 1
fi

echo "✅ 의존성 확인 완료"

# Python 경로 설정
export PYTHONPATH="$PROJECT_ROOT/server_min:$PROJECT_ROOT/Dockers/HybridTool:$PYTHONPATH"

# 환경 변수 설정 (필요에 따라 수정하세요)
_KST_TS="$(date -u -d '+9 hours' +%y%m%d_%H%M%S)"
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
# BayesianPage 폼 데이터 예시값 (실제 값으로 교체 가능)
export FP_Input="${FP_Input:-200}"

# BBN_INPUT_FILE: 설정하면 해당 JSON 파일로 실행, 미설정 시 my-bbn-input.json 사용
export BBN_INPUT_FILE="${BBN_INPUT_FILE:-$PROJECT_ROOT/tempDoc/my-bbn-input.json}"

export nChains="${nChains:-1}"
export nIter="${nIter:-19500}"
export nBurnin="${nBurnin:-500}"
export nThin="${nThin:-1}"

# 출력 디렉토리 생성
mkdir -p "$TEST_OUTPUT_DIR"

# Python wrapper 스크립트 실행
LOG_FILE="$TEST_OUTPUT_DIR/run_local_$(date -u -d '+9 hours' +%y%m%d_%H%M%S).log"
cd "$PROJECT_ROOT"
python "$SCRIPT_DIR/run_local.py" 2>&1 | tee "$LOG_FILE"
echo ""
echo "로그 저장됨: $LOG_FILE"

