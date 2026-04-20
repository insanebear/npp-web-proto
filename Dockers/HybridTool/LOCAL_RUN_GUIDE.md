# 로컬 실행 가이드

Docker 이미지를 빌드하지 않고 `run_full_analysis.py` 및 다른 HybridTool 스크립트를 로컬에서 실행하는 방법입니다.

> **중요**: PyMC, pytensor, JAX 등 과학 계산 패키지의 의존성 문제로 인해 venv 대신 **conda 환경**을 사용합니다. Python 3.11은 conda가 자동으로 관리합니다.

## 사전 요구사항

### 1. Miniconda 설치

#### Windows
1. [Miniconda 다운로드](https://docs.conda.io/en/latest/miniconda.html) 후 설치
2. Git Bash 재시작 후 확인:
   ```bash
   conda --version
   ```
3. conda가 인식되지 않으면:
   ```bash
   source ~/miniconda3/etc/profile.d/conda.sh
   ```

#### Mac
```bash
brew install --cask miniconda
conda init zsh  # 또는 bash
# 터미널 재시작 후
conda --version
```

#### Linux
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# 터미널 재시작 후
conda --version
```

### 2. conda 환경 생성

프로젝트 루트에서 한 번만 실행하면 됩니다. Python 3.11과 모든 의존성이 자동으로 설치됩니다:

```bash
conda env create -f environment.yml
```

## 빠른 시작

### Bash 스크립트 사용 (권장)

```bash
conda activate gxx_env_311
cd /path/to/npp-web-proto
bash Dockers/HybridTool/run_local.sh
```

다른 conda 환경을 사용할 경우:
```bash
CONDA_ENV_NAME=다른환경이름 bash Dockers/HybridTool/run_local.sh
```

**환경 재생성이 필요한 경우:**
```bash
conda env remove -n gxx_env_311
conda env create -f environment.yml
```

### 환경 변수 커스터마이징

```bash
export TASK_TYPE=bbn_inference
export JOB_ID=test-001
export FP_Input=56
export USE_NRC_DATA=true
export DRAWS=1000
export TUNE=500
export CHAINS=1
export TEST_OUTPUT_DIR=./tempDoc/hybrid-tool-test
bash Dockers/HybridTool/run_local.sh
```

## 환경 변수 설명

| 변수명 | 설명 | 기본값 |
|--------|------|--------|
| `TASK_TYPE` | 실행할 작업 타입 (`bbn_inference`, `full_analysis`, `sensitivity_analysis`, `update_pfd`) | `bbn_inference` |
| `JOB_ID` | 작업 식별자 | `local-full-001` |
| `FP_Input` | BBN 입력값 | `56` |
| `USE_NRC_DATA` | NRC 데이터 사용 여부 | `true` |
| `PFD_GOAL` | 목표 PFD 값 | `0.0001` |
| `CONFIDENCE_GOAL` | 목표 신뢰도 | `0.95` |
| `FAILURES` | 관찰된 실패 횟수 | `0` |
| `S3_BUCKET` | S3 버킷 이름 (TEST_MODE일 때는 사용 안 함) | `dummy` |
| `AWS_REGION` | AWS 리전 | `ap-northeast-2` |
| `TEST_MODE` | 테스트 모드 | `false` |
| `TEST_OUTPUT_DIR` | 로컬 출력 디렉토리 | `./tempDoc/hybrid-tool-test` |
| `DRAWS` | MCMC 샘플링 draws 수 | `19500` |
| `TUNE` | MCMC 튜닝 단계 수 | `500` |
| `CHAINS` | MCMC 체인 수 | `1` |
| `THIN` | MCMC thinning | `1` |

## 출력

- `TEST_OUTPUT_DIR`이 설정된 경우: 로컬 파일 시스템에 JSON 파일로 저장
- `TEST_OUTPUT_DIR`이 없는 경우: S3에 업로드 (실제 AWS 자격증명 필요)

## 문제 해결

### conda가 인식되지 않는 경우

```bash
source ~/miniconda3/etc/profile.d/conda.sh
conda activate gxx_env_311
```

### JAX/numpyro 호환성 오류

`environment.yml`로 환경을 새로 만드는 것을 권장합니다. 직접 설치할 경우 반드시 아래 버전을 사용하세요:

```bash
pip install "jax[cpu]==0.8.0" jaxlib==0.8.0 numpyro==0.19.0 --force-reinstall
```

### ModuleNotFoundError: No module named 'bbn_inference'

프로젝트 루트에서 실행하는지 확인하세요:
```bash
cd /path/to/npp-web-proto
bash Dockers/HybridTool/run_local.sh
```

### ModuleNotFoundError: No module named 'task_common'

위와 동일하게 프로젝트 루트에서 실행하세요.

## Docker 실행과의 차이점

- Docker: `python:3.11-slim` 이미지 + pip
- 로컬: conda 환경 (`gxx_env_311`) 사용
- Docker: `/app/server` 경로 사용
- 로컬: `./server_min` 경로 사용


