#!/bin/bash

# 로컬 환경 구축 스크립트
# /Volumes/insanebearP31/ 경로에 필요한 도구들을 설치

echo "=== 로컬 환경 구축 시작 ==="

# 1. Python 가상환경 생성 (이미 있다면 스킵)
if [ ! -d "/Volumes/insanebearP31/Projects/npp-web-proto/.venv" ]; then
    echo "Python 가상환경 생성 중..."
    python3 -m venv /Volumes/insanebearP31/Projects/npp-web-proto/.venv
fi

# 2. 가상환경 활성화
echo "가상환경 활성화 중..."
source /Volumes/insanebearP31/Projects/npp-web-proto/.venv/bin/activate

# 3. Python 패키지 설치
echo "Python 패키지 설치 중..."
pip install flask flask-cors

# 4. R 설치 확인 및 안내
echo "=== R 설치 확인 ==="
if command -v R &> /dev/null; then
    echo "✓ R이 이미 설치되어 있습니다."
    R --version
else
    echo "⚠ R이 설치되어 있지 않습니다."
    echo "다음 명령어로 R을 설치하세요:"
    echo "cd /Volumes/insanebearP31/"
    echo "curl -O https://cran.r-project.org/bin/macosx/base/R-4.4.1-arm64.pkg"
    echo "sudo installer -pkg R-4.4.1-arm64.pkg -target /"
fi

# 5. R 패키지 설치 확인
if command -v R &> /dev/null; then
    echo "=== R 패키지 설치 확인 ==="
    R -e "if (!require('rjags')) install.packages('rjags', repos='https://cloud.r-project.org')"
    R -e "if (!require('jsonlite')) install.packages('jsonlite', repos='https://cloud.r-project.org')"
    echo "✓ R 패키지 설치 완료"
fi

# 6. 결과 디렉토리 생성
echo "=== 결과 디렉토리 생성 ==="
mkdir -p /Volumes/insanebearP31/Projects/npp-web-proto/local_results
echo "✓ 결과 디렉토리 생성 완료"

echo "=== 설치 완료 ==="
echo "다음 명령어로 로컬 백엔드 서버를 시작하세요:"
echo "cd /Volumes/insanebearP31/Projects/npp-web-proto"
echo "source .venv/bin/activate"
echo "python local_backend.py"
