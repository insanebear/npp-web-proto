# 로컬 실행 가이드

Docker 이미지를 빌드하지 않고 `run_full_analysis.py` 및 다른 HybridTool 스크립트를 로컬에서 실행하는 방법입니다.

## 사전 요구사항

**Python 3.11 설치** (필수 - Docker 환경과 동일한 버전)

로컬 실행 스크립트가 자동으로:
- Python 3.11을 찾아서 사용
- 가상환경을 자동 생성 (`.venv-hybridtool`)
- 필요한 의존성을 자동 설치

### Python 3.11 설치 방법

#### Windows
1. [Python 3.11.9 다운로드](https://www.python.org/downloads/release/python-3119/)
2. 설치 시 **"Add Python to PATH"** 옵션을 반드시 체크
3. 설치 확인:
   ```bash
   python3.11 --version
   # 또는
   python311 --version
   # 또는 (Windows Python Launcher 사용 시)
   py -3.11 --version
   ```

#### Mac
```bash
brew install python@3.11
python3.11 --version
```

#### Linux
```bash
sudo apt-get update
sudo apt-get install python3.11 python3.11-venv
python3.11 --version
```

**참고**: Python 3.13 등 다른 버전이 설치되어 있어도 괜찮습니다. Python 3.11을 추가로 설치하면 됩니다.

## 빠른 시작

### Bash 스크립트 사용 (권장)

```bash
# 기본 설정으로 실행
cd /c/Users/yljung/Documents/npp-web-proto
./Dockers/HybridTool/run_local.sh
```

**첫 실행 시:**
- Python 3.11을 자동으로 찾습니다 (없으면 에러 메시지 표시)
- `.venv-hybridtool` 가상환경을 Python 3.11로 자동 생성합니다
- 필요한 의존성을 자동 설치합니다 (시간이 걸릴 수 있음)
- 출력 디렉토리(`tempDoc/hybrid-tool-test`) 자동 생성 (없어도 자동으로 만들어짐)

**두 번째 실행부터:**
- 이미 생성된 가상환경을 사용합니다
- 의존성이 이미 설치되어 있으면 스킵합니다

**Python 버전 변경 시:**
기존 가상환경을 삭제하고 다시 생성:
```bash
rm -rf .venv-hybridtool
./Dockers/HybridTool/run_local.sh
```

### 환경 변수 커스터마이징

```bash
export TASK_TYPE=full_analysis
export JOB_ID=test-001
export PFD_GOAL=0.0001
export CONFIDENCE_GOAL=0.95
export FAILURES=0
export DRAWS=1000
export TUNE=500
export CHAINS=2
export THIN=1
export TEST_OUTPUT_DIR=./tempDoc/hybrid-tool-test
./Dockers/HybridTool/run_local.sh
```

## 가상환경 관리

가상환경은 프로젝트 루트의 `.venv-hybridtool` 디렉토리에 생성됩니다.

**가상환경 삭제 (의존성 재설치하려는 경우):**
```bash
rm -rf .venv-hybridtool
```

다음 실행 시 자동으로 다시 생성되고 의존성이 설치됩니다.

## 환경 변수 설명

| 변수명 | 설명 | 기본값 | 필수 |
|--------|------|--------|------|
| `TASK_TYPE` | 실행할 작업 타입 (`full_analysis`, `sensitivity_analysis`, `update_pfd`) | `full_analysis` | 아니오 |
| `JOB_ID` | 작업 식별자 | `local-full-001` | 아니오 |
| `PFD_GOAL` | 목표 PFD 값 | `0.0001` | 아니오 |
| `CONFIDENCE_GOAL` | 목표 신뢰도 | `0.95` | 아니오 |
| `FAILURES` | 관찰된 실패 횟수 | `0` | 아니오 |
| `S3_BUCKET` | S3 버킷 이름 (TEST_MODE일 때는 사용 안 함) | `dummy` | 아니오 |
| `AWS_REGION` | AWS 리전 | `ap-northeast-2` | 아니오 |
| `TEST_MODE` | 테스트 모드 (실제 계산 생략) | `false` | 아니오 |
| `TEST_OUTPUT_DIR` | 로컬 출력 디렉토리 | `./tempDoc/hybrid-tool-test` | 아니오 |
| `DRAWS` | MCMC 샘플링 draws 수 | `1000` | 아니오 |
| `TUNE` | MCMC 튜닝 단계 수 | `500` | 아니오 |
| `CHAINS` | MCMC 체인 수 | `2` | 아니오 |
| `THIN` | MCMC thinning | `1` | 아니오 |
| `BBN_INPUT_PATH` | BBN 입력 JSON 파일 경로 (선택사항) | - | 아니오 |
| `BBN_INPUT_BUCKET` | BBN 입력 S3 버킷 (선택사항) | - | 아니오 |

## 출력

- `TEST_OUTPUT_DIR`이 설정된 경우: 로컬 파일 시스템에 JSON 파일로 저장
- `TEST_OUTPUT_DIR`이 없는 경우: S3에 업로드 (실제 AWS 자격증명 필요)

## 문제 해결

### ModuleNotFoundError: No module named 'bbn_inference'

`server_min` 디렉토리가 Python 경로에 포함되어 있는지 확인하세요:
```bash
export PYTHONPATH=./server_min:./Dockers/HybridTool:$PYTHONPATH
```

### ModuleNotFoundError: No module named 'task_common'

현재 디렉토리가 프로젝트 루트인지 확인하세요:
```bash
cd /c/Users/yljung/Documents/npp-web-proto
```

### 의존성 패키지 오류

필요한 패키지가 설치되어 있는지 확인하세요:
```bash
pip install -r server_min/requirements.txt
```

## Docker 실행과의 차이점

- Docker: `/app/server` 경로 사용
- 로컬: `./server_min` 경로 사용
- 로컬 실행 시 `task_common.py`의 `/app/server` 경로는 무시되며, 이미 `server_min`이 `sys.path`에 추가되어 있으므로 정상 작동합니다.


