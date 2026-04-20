#!/usr/bin/env bash
# 로컬에서 HybridTool 스크립트를 실행하기 위한 헬퍼 스크립트
# Docker 이미지 빌드 없이 빠르게 테스트할 수 있습니다.
# Python 3.11 가상환경을 자동으로 생성하고 관리합니다.

# 프로젝트 루트 디렉토리 찾기
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
VENV_DIR="$PROJECT_ROOT/.venv-hybridtool"
REQUIREMENTS_FILE="$PROJECT_ROOT/server_min/requirements.txt"

# Python 3.11 필수로 찾기 (Docker 환경과 동일하게)
PYTHON_CMD=""
PYTHON_VERSION=""
PYTHON_MAJOR=0
PYTHON_MINOR=0

# Python 3.11을 찾기 (여러 가능한 명령어 시도)
# Windows Python Launcher (py -3.11)는 공백이 있어서 별도 처리
if command -v py &> /dev/null; then
    PYTHON_VERSION=$(py -3.11 --version 2>&1 | awk '{print $2}')
    if [ $? -eq 0 ] && [ -n "$PYTHON_VERSION" ]; then
        PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
        PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
        if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -eq 11 ]; then
            PYTHON_CMD="py -3.11"
        fi
    fi
fi

# 다른 명령어 시도
if [ -z "$PYTHON_CMD" ]; then
    for py_cmd in python3.11 python311; do
        if command -v "$py_cmd" &> /dev/null; then
            PYTHON_VERSION=$("$py_cmd" --version 2>&1 | awk '{print $2}')
            PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
            PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)
            if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -eq 11 ]; then
                PYTHON_CMD="$py_cmd"
                break
            fi
        fi
    done
fi

if [ -z "$PYTHON_CMD" ]; then
    echo "❌ Python 3.11을 찾을 수 없습니다."
    echo ""
    echo "Python 3.11을 설치해주세요 (Docker 환경과 동일한 버전 필요):"
    echo "  - Windows: https://www.python.org/downloads/release/python-3119/"
    echo "    설치 시 'Add Python to PATH' 옵션을 체크하세요"
    echo "  - Mac: brew install python@3.11"
    echo "  - Linux: sudo apt-get install python3.11 python3.11-venv"
    echo ""
    echo "설치 후 다음 명령어로 확인:"
    echo "  python3.11 --version"
    echo ""
    echo "현재 시스템 Python 버전:"
    python3 --version 2>&1 || python --version 2>&1 || echo "Python이 설치되어 있지 않습니다."
    exit 1
fi

echo "✅ Python 3.11 발견: $PYTHON_CMD ($PYTHON_VERSION)"

# 가상환경이 없으면 생성
if [ ! -d "$VENV_DIR" ]; then
    echo ""
    echo "가상환경 생성 중... ($VENV_DIR)"
    # py -3.11 같은 공백이 있는 명령어를 처리하기 위해 eval 사용
    eval "$PYTHON_CMD -m venv \"$VENV_DIR\""
    if [ $? -ne 0 ]; then
        echo "❌ 가상환경 생성 실패"
        exit 1
    fi
    echo "✅ 가상환경 생성 완료"
fi

# 가상환경 활성화
if [ -f "$VENV_DIR/Scripts/activate" ]; then
    # Windows Git Bash
    source "$VENV_DIR/Scripts/activate"
elif [ -f "$VENV_DIR/bin/activate" ]; then
    # Linux/Mac
    source "$VENV_DIR/bin/activate"
else
    echo "❌ 가상환경 활성화 스크립트를 찾을 수 없습니다: $VENV_DIR"
    exit 1
fi

# pip 업그레이드
echo "pip 업그레이드 중..."
python -m pip install --quiet --upgrade pip

# 의존성 설치 확인 (requirements.txt의 패키지 중 하나만 체크)
if ! python -c "import pymc" &> /dev/null; then
    echo ""
    echo "의존성 패키지 설치 중... (시간이 걸릴 수 있습니다)"
    echo ""
    python -m pip install -r "$REQUIREMENTS_FILE"
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ 의존성 설치 실패"
        exit 1
    fi
    echo ""
    echo "✅ 의존성 설치 완료"
else
    echo "✅ 의존성 이미 설치되어 있음"
fi

# Python 경로 설정
export PYTHONPATH="$PROJECT_ROOT/server_min:$PROJECT_ROOT/Dockers/HybridTool:$PYTHONPATH"

# 환경 변수 설정 (필요에 따라 수정하세요)
export TASK_TYPE="${TASK_TYPE:-full_analysis}"
export JOB_ID="${JOB_ID:-local-full-001}"
export PFD_GOAL="${PFD_GOAL:-0.0001}"
export CONFIDENCE_GOAL="${CONFIDENCE_GOAL:-0.95}"
export FAILURES="${FAILURES:-0}"
export DEMAND_REQUIRED="${DEMAND_REQUIRED:-10000}"
export S3_BUCKET="${S3_BUCKET:-dummy}"
export AWS_REGION="${AWS_REGION:-ap-northeast-2}"
export TEST_MODE="${TEST_MODE:-true}"
export TEST_OUTPUT_DIR="${TEST_OUTPUT_DIR:-$PROJECT_ROOT/tempDoc/hybrid-tool-test}"
export DRAWS="${DRAWS:-19500}"
export TUNE="${TUNE:-500}"
export CHAINS="${CHAINS:-1}"
export THIN="${THIN:-1}"

# bbn_inference용 환경 변수 (TASK_TYPE=bbn_inference 시 사용)
# BayesianPage 폼 데이터 예시값 (실제 값으로 교체 가능)
export FP_Input="${FP_Input:-56}"
# USE_NRC_DATA=true: nrc_report_data() 값으로 실행 (로컬 테스트 기본값)
# USE_NRC_DATA=false: env var로 직접 속성값을 지정할 때 사용
export USE_NRC_DATA="${USE_NRC_DATA:-true}"
export nChains="${nChains:-1}"
export nIter="${nIter:-500}"
export nBurnin="${nBurnin:-100}"
export nThin="${nThin:-1}"

# 출력 디렉토리 생성
mkdir -p "$TEST_OUTPUT_DIR"

# Python wrapper 스크립트 실행
cd "$PROJECT_ROOT"
python "$SCRIPT_DIR/run_local.py"

