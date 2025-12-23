# 개발자 매뉴얼

이 문서는 NPP Web Proto 프로젝트의 개발 환경 설정, 배포, 그리고 프로젝트 구조에 대한 가이드입니다.

---

## 목차

1. [로컬 개발 환경 설정](#로컬-개발-환경-설정)
2. [환경 변수 설정](#환경-변수-설정)
3. [AWS 설정](#aws-설정)
4. [프로젝트 구조](#프로젝트-구조)
5. [배포 가이드](#배포-가이드)
6. [주의사항](#주의사항)
7. [트러블슈팅](#트러블슈팅)

---

## 로컬 개발 환경 설정

### 필수 도구 설치

#### 1. Git 설치
- **Windows**: [Git for Windows](https://git-scm.com/downloads) 다운로드 및 설치
- **Mac/Linux**: Homebrew를 통한 설치
  ```bash
  brew install git
  ```

#### 2. Node.js 설치
- **필수 버전**: Node.js 20.x 이상 (권장: 20 LTS 또는 22 LTS)
- **이유**: 
  - React 19.1.0 사용 (Node.js 18+ 필요)
  - Vite 7.1.10 사용 (최신 Node.js 필요)
  - `@types/node` 22.7.5 사용
- [Node.js 공식 웹사이트](https://nodejs.org/)에서 LTS 버전 다운로드 및 설치
- 설치 확인:
  ```bash
  node --version
  npm --version
  ```
- **버전 확인**: `node --version` 출력이 `v20.x.x` 이상이어야 합니다

#### 3. Python 설치
- **필수 버전**: Python 3.11
- **이유**: 
  - Docker 컨테이너에서 `python:3.11-slim` 사용
  - Lambda 함수에서 `python:3.11` 사용
  - PyMC, JAX 등 과학 계산 라이브러리가 Python 3.11에서 최적화됨
- **Windows**: [Python 공식 웹사이트](https://www.python.org/downloads/)에서 Python 3.11 다운로드 및 설치
  - 설치 시 "Add Python to PATH" 옵션 체크 필수
- **Mac/Linux**: 
  - 시스템에 Python 3.11이 없으면 설치 필요
  - Homebrew (Mac): `brew install python@3.11`
  - 또는 pyenv 사용 권장
- 설치 확인:
  ```bash
  python --version
  # 또는
  python3 --version
  ```
- **버전 확인**: 출력이 `Python 3.11.x`여야 합니다
- **참고**: 배포 스크립트가 환경 변수 치환 및 JSON 검증을 위해 Python을 사용합니다. (`deploy-*-task-definition.sh`, `set-*-lambda-env.sh` 등)

#### 4. Docker 설치
- [Docker 공식 웹사이트](https://www.docker.com/)에서 다운로드 및 설치
- **OS별 요구사항**:
  - **Windows**: 
    - Windows 10/11 Pro 이상 또는 Windows 10/11 Home (WSL 2 사용)
    - 대부분의 최신 컴퓨터는 가상화가 기본 활성화되어 있으나, 문제 발생 시 BIOS에서 가상화 기능 확인 필요
  - **Mac**: 
    - Apple Silicon (M1/M2): 가상화 자동 지원
    - Intel Mac: 가상화 필요 (대부분 기본 활성화)
  - **Linux**: 가상화 불필요 (컨테이너는 리눅스 커널 기능 사용)
- 설치 확인:
  ```bash
  docker --version
  docker ps
  ```
- **참고**: Docker 이미지 빌드 및 ECR 푸시를 위해 로컬 Docker 설치가 필요합니다. 배포 스크립트(`deploy-*-docker.sh`)가 Docker를 사용합니다.

#### 5. AWS CLI 설치 및 설정
- **설치**: [AWS CLI 설치 가이드](https://aws.amazon.com/cli/) 참고
- **설정**:
  ```bash
  aws configure
  ```
  다음 정보 입력:
  - AWS Access Key ID
  - AWS Secret Access Key
  - Default region: `ap-northeast-2` (서울 리전)
  - Default output format: `json`

- **프로필 설정** (여러 AWS 계정 사용 시):
  ```bash
  aws configure --profile <YOUR_AWS_PROFILE_NAME>
  ```

- **설정 확인**:
  ```bash
  aws sts get-caller-identity --profile <YOUR_AWS_PROFILE_NAME>
  ```

### 프로젝트 클론 및 의존성 설치

```bash
# 프로젝트 클론
git clone https://github.com/insanebear/npp-web-proto.git
cd npp-web-proto

# 프론트엔드 의존성 설치
cd apps/frontend
npm install
cd ../..
```

---

## 환경 변수 설정

⚠️ **중요**: 환경 변수 파일에는 민감한 정보가 포함되어 있으므로 **절대 Git에 커밋하지 마세요**. 모든 환경 변수 파일은 `.gitignore`에 포함되어 있습니다.

> **💡 Placeholder 안내**: 아래 예시에서 `<YOUR_VALUE>` 형식으로 표시된 부분은 실제 값으로 반드시 교체해야 합니다. 예: `<YOUR_API_GATEWAY_ID>` → `abc123xyz`

### 1. 프론트엔드 환경 변수

프론트엔드는 Vite를 사용하므로 환경 변수는 `VITE_` 접두사가 필요합니다.

**로컬 개발용 `.env` 파일 생성** (`apps/frontend/.env`):

```bash
# Bayesian API Gateway URL
# ⚠️ <YOUR_API_GATEWAY_ID>를 실제 API Gateway ID로 교체하세요
VITE_API_BASE_URL=https://<YOUR_API_GATEWAY_ID>.execute-api.ap-northeast-2.amazonaws.com/prod

# Statistical (SST) API Gateway URL
# ⚠️ <YOUR_API_GATEWAY_ID>를 실제 API Gateway ID로 교체하세요
VITE_API_BASE_URL_SST=https://<YOUR_API_GATEWAY_ID>.execute-api.ap-northeast-2.amazonaws.com/prod
```

**주의사항**:
- `.env` 파일은 Git에 커밋되지 않습니다 (`.gitignore`에 포함됨)
- `<YOUR_API_GATEWAY_ID>` 부분을 실제 API Gateway ID로 교체해야 합니다

### 2. 배포용 환경 변수

#### BBN/HybridTool 배포 설정

**파일 위치**: `scripts/config/.nppswrel-env`

**설정 방법**:
```bash
# 예시 파일 복사
cp scripts/config/.nppswrel-env.example scripts/config/.nppswrel-env

# 파일 편집 (실제 값으로 교체)
# Windows: notepad scripts/config/.nppswrel-env
# Mac/Linux: nano scripts/config/.nppswrel-env
```

**필수 환경 변수**:
```bash
# AWS 설정
export AWS_REGION=ap-northeast-2
export AWS_PROFILE=<YOUR_AWS_PROFILE_NAME>          # ⚠️ 실제 AWS 프로필 이름으로 교체
export AWS_ACCOUNT_ID=<YOUR_AWS_ACCOUNT_ID>         # ⚠️ 실제 AWS 계정 ID로 교체 (예: 123456789012)

# ECR 설정
export ECR_REPOSITORY=hybrid-tool-pymc
export DOCKER_IMAGE_TAG=latest

# ECS 설정
export CLUSTER_NAME=bayesian-cluster
export TASK_DEFINITION=hybrid-tool-pymc-task
export SUBNET_IDS=<YOUR_SUBNET_ID_1>,<YOUR_SUBNET_ID_2>  # ⚠️ 실제 서브넷 ID로 교체 (예: subnet-abc123,subnet-def456)

# S3 설정
export S3_BUCKET=hybrid-tool-results

# Lambda 함수명 (HybridTool)
export LAMBDA_TRIGGER_SENSITIVITY_FUNCTION=hybrid-tool-trigger-sensitivity-task
export LAMBDA_TRIGGER_UPDATE_PFD_FUNCTION=hybrid-tool-trigger-update-pfd-task
export LAMBDA_TRIGGER_FULL_ANALYSIS_FUNCTION=hybrid-tool-trigger-full-analysis-task
export LAMBDA_GET_RESULTS_FUNCTION=hybrid-tool-get-results
export LAMBDA_LIST_BBN_RESULTS_FUNCTION=hybrid-tool-list-bbn-results

# Lambda 함수명 (BBN)
export BBN_LAMBDA_FUNCTION_NAME=my-starter

# BBN ECS 설정
export BBN_TASK_DEFINITION=bayesian-simulation-task
export BBN_CONTAINER_NAME=bayesian-simulation-app

# API Gateway
export API_GATEWAY_ID=<YOUR_API_GATEWAY_ID>         # ⚠️ 실제 API Gateway ID로 교체
export API_GATEWAY_BASE_PATH=/api/v1

# DynamoDB 설정
export JOBS_TABLE_NAME=BayesianSimulationJobs
```

#### 웹사이트 배포 설정

**파일 위치**: `scripts/config/.website-env`

**설정 방법**:
```bash
# 예시 파일 복사
cp scripts/config/.website-env.sample scripts/config/.website-env

# 파일 편집
```

**필수 환경 변수**:
```bash
export S3_BUCKET=<YOUR_S3_BUCKET_NAME>              # ⚠️ 실제 S3 버킷 이름으로 교체
export CLOUDFRONT_DISTRIBUTION=<YOUR_CLOUDFRONT_DISTRIBUTION_ID>  # ⚠️ 실제 CloudFront 배포 ID로 교체
export AWS_REGION=us-east-1
export AWS_PROFILE=default                           # 필요시 <YOUR_AWS_PROFILE_NAME>으로 변경
```

### 3. 환경 변수 확인

배포 전 환경 변수가 올바르게 설정되었는지 확인:

```bash
# BBN/HybridTool 설정 확인
source scripts/config/.nppswrel-env
echo $AWS_ACCOUNT_ID
echo $CLUSTER_NAME

# 웹사이트 설정 확인
source scripts/config/.website-env
echo $S3_BUCKET
```

---

## AWS 설정

### 필수 AWS 리소스

프로젝트를 배포하기 전에 다음 AWS 리소스가 준비되어 있어야 합니다:

#### 1. ECS 클러스터
- **이름**: `bayesian-cluster`
- **타입**: Fargate
- **리전**: `ap-northeast-2` (서울)

#### 2. ECR 리포지토리
- **HybridTool**: `hybrid-tool-pymc`
- **BayesianPage**: `bayesian-page-repo`

#### 3. S3 버킷
- **HybridTool 결과**: `hybrid-tool-results`
- **Bayesian 결과**: `bayesian-simulation-results-bucket`

#### 4. DynamoDB 테이블
- **이름**: `BayesianSimulationJobs`
- **용도**: 작업 상태 추적

#### 5. Lambda 함수
**HybridTool Lambda 함수들**:
- `hybrid-tool-trigger-full-analysis-task`
- `hybrid-tool-trigger-sensitivity-task`
- `hybrid-tool-trigger-update-pfd-task`
- `hybrid-tool-get-results`
- `hybrid-tool-get-job-status`
- `hybrid-tool-list-bbn-results`

**BBN Lambda 함수**:
- `my-starter`

#### 6. IAM 역할 및 정책

**필수 IAM 역할**:
- `ecsTaskExecutionRole`: ECS 작업 실행 역할
- `BayesianSimulationFargateTaskRole`: ECS 작업 역할
- Lambda 실행 역할들

**IAM 정책 예시**: `aws-configs/hybridTool-iam-policies.json` 참고

### AWS 리소스 생성 가이드

#### ECS 클러스터 생성
```bash
# ⚠️ <YOUR_AWS_PROFILE_NAME>을 실제 AWS 프로필 이름으로 교체하세요
aws ecs create-cluster \
  --cluster-name bayesian-cluster \
  --region ap-northeast-2 \
  --profile <YOUR_AWS_PROFILE_NAME>
```

#### ECR 리포지토리 생성
```bash
# HybridTool 리포지토리
# ⚠️ <YOUR_AWS_PROFILE_NAME>을 실제 AWS 프로필 이름으로 교체하세요
aws ecr create-repository \
  --repository-name hybrid-tool-pymc \
  --region ap-northeast-2 \
  --profile <YOUR_AWS_PROFILE_NAME>

# BayesianPage 리포지토리
aws ecr create-repository \
  --repository-name bayesian-page-r \
  --region ap-northeast-2 \
  --profile <YOUR_AWS_PROFILE_NAME>
```

#### S3 버킷 생성
```bash
# HybridTool 결과 버킷
# ⚠️ <YOUR_AWS_PROFILE_NAME>을 실제 AWS 프로필 이름으로 교체하세요
aws s3 mb s3://hybrid-tool-results \
  --region ap-northeast-2 \
  --profile <YOUR_AWS_PROFILE_NAME>

# Bayesian 결과 버킷
aws s3 mb s3://bayesian-simulation-results-bucket \
  --region ap-northeast-2 \
  --profile <YOUR_AWS_PROFILE_NAME>
```

#### DynamoDB 테이블 생성
```bash
# ⚠️ <YOUR_AWS_PROFILE_NAME>을 실제 AWS 프로필 이름으로 교체하세요
aws dynamodb create-table \
  --table-name BayesianSimulationJobs \
  --attribute-definitions AttributeName=jobId,AttributeType=S \
  --key-schema AttributeName=jobId,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-northeast-2 \
  --profile <YOUR_AWS_PROFILE_NAME>
```

### VPC 및 네트워크 설정

ECS Fargate 작업은 VPC 내에서 실행되므로 다음이 필요합니다:

- **서브넷 ID**: 공개 IP 할당이 가능한 서브넷
- **보안 그룹**: 필요 시 설정 (선택사항)

서브넷 ID 확인:
```bash
# ⚠️ <YOUR_AWS_PROFILE_NAME>을 실제 AWS 프로필 이름으로 교체하세요
aws ec2 describe-subnets \
  --region ap-northeast-2 \
  --profile <YOUR_AWS_PROFILE_NAME> \
  --query 'Subnets[*].[SubnetId,Tags[?Key==`Name`].Value|[0]]' \
  --output table
```

---

## 프로젝트 구조

```
npp-web-proto/
├── apps/
│   └── frontend/              # React + TypeScript 프론트엔드
│       ├── src/
│       │   ├── features/      # 기능별 컴포넌트
│       │   │   ├── bayesian/  # Bayesian 분석 페이지
│       │   │   ├── statistical/ # 통계 분석 페이지
│       │   │   ├── reliability/ # 신뢰성 분석 페이지
│       │   │   └── settings/   # 설정 페이지
│       │   ├── shared/        # 공통 컴포넌트 및 유틸리티
│       │   │   ├── components/ # 재사용 가능한 컴포넌트
│       │   │   ├── services/   # API 서비스
│       │   │   ├── hooks/      # React 커스텀 훅
│       │   │   └── types/      # TypeScript 타입 정의
│       │   └── main.tsx        # 애플리케이션 진입점
│       ├── package.json
│       └── vite.config.ts
│
├── server_min/               # 최소 서버 코드 (Docker 컨테이너용)
│   └── bbn_inference/        # Bayesian 분석 핵심 로직
│
├── lambda/                   # AWS Lambda 함수
│   ├── BayesianStarterLambda.ts  # BBN 작업 트리거 Lambda
│   ├── hybridTool/           # HybridTool Lambda 함수들
│   │   ├── triggerTask.py     # 작업 트리거
│   │   ├── getResults.py      # 결과 조회
│   │   ├── getJobStatus.py    # 작업 상태 조회
│   │   └── listBbnResults.py  # BBN 결과 목록
│   └── utils-bayesian/       # Bayesian Lambda 유틸리티
│
├── Dockers/                   # Docker 컨테이너 정의
│   ├── BayesianPage/         # R 기반 Bayesian 분석 컨테이너
│   │   ├── Dockerfile
│   │   └── run_simulation.R
│   └── HybridTool/           # Python 기반 HybridTool 컨테이너
│       ├── Dockerfile
│       └── run_*.py          # 작업 실행 스크립트들
│
├── aws-configs/               # AWS 리소스 설정 파일
│   ├── bayesianPage-task-definition.json  # ECS Task Definition
│   ├── hybridTool-task-definition.json
│   └── hybridTool-iam-policies.json      # IAM 정책 예시
│
└── scripts/                  # 배포 및 유틸리티 스크립트
    ├── deploy/               # 배포 스크립트
    │   ├── bbn/              # BBN 배포 스크립트
    │   ├── hybridTool/       # HybridTool 배포 스크립트
    │   └── deploy-website.sh # 웹사이트 배포 스크립트
    ├── config/               # 환경 변수 설정 파일
    │   ├── .nppswrel-env.example
    │   └── .website-env.sample
    └── utils/                # 유틸리티 스크립트
```

### 주요 폴더 설명

#### `apps/frontend/`
- **용도**: React + TypeScript로 작성된 프론트엔드 애플리케이션
- **수정 시 주의사항**:
  - 새로운 API 엔드포인트 추가 시 `src/shared/services/apiService.ts` 확인
  - 환경 변수는 `VITE_` 접두사 필요
  - 빌드: `npm run build` (배포 전 필수)

#### `lambda/`
- **용도**: AWS Lambda 함수 코드
- **수정 시 주의사항**:
  - TypeScript 파일은 빌드 후 배포 (`lambda-build/` 폴더)
  - Python 파일은 직접 배포 가능
  - 환경 변수는 배포 스크립트를 통해 설정

#### `Dockers/`
- **용도**: ECS Fargate 작업용 Docker 컨테이너 정의
- **수정 시 주의사항**:
  - Dockerfile 수정 후 이미지 재빌드 필요
  - `run_*.py` 또는 `run_simulation.R` 스크립트가 작업 실행

#### `aws-configs/`
- **용도**: AWS 리소스 정의 파일 (Task Definition, IAM 정책 등)
- **수정 시 주의사항**:
  - 환경 변수 치환이 필요 (`${AWS_ACCOUNT_ID}` 등)
  - 배포 스크립트가 자동으로 처리

#### `scripts/deploy/`
- **용도**: 배포 자동화 스크립트
- **수정 시 주의사항**:
  - Git Bash 환경에서 실행 (Windows)
  - 환경 변수 파일(`scripts/config/.nppswrel-env`) 필수

---

## 배포 가이드

### BBN (Bayesian) 배포

BBN 배포는 Docker 이미지, ECS Task Definition, Lambda 함수를 순서대로 배포합니다.

**배포 순서가 중요한 이유**:
- **Docker 이미지 → Task Definition**: Task Definition 등록은 이미지 없이도 가능하지만, 실제 ECS Task 실행 시에는 이미지가 ECR에 있어야 합니다.
- **Lambda 함수 → Lambda 환경 변수**: Lambda 함수가 먼저 배포되어 있어야 환경 변수를 설정할 수 있습니다.
- **Lambda 함수 배포**: 다른 단계와 독립적이므로 순서와 무관합니다.

#### 전체 배포 (권장)
```bash
# 환경 변수 설정 확인
source scripts/config/.nppswrel-env

# 전체 배포 실행
bash scripts/deploy/bbn/deploy-bbn-all.sh
```

#### 단계별 배포

1. **Docker 이미지 빌드 및 ECR 푸시**
   ```bash
   bash scripts/deploy/bbn/deploy-bbn-docker.sh
   ```

2. **ECS Task Definition 등록**
   ```bash
   bash scripts/deploy/bbn/deploy-bbn-task-definition.sh
   ```

3. **Lambda 함수 배포**
   ```bash
   bash scripts/deploy/bbn/deploy-bbn-lambda.sh
   ```

4. **Lambda 함수 환경 변수 설정**
   ```bash
   bash scripts/deploy/bbn/set-bbn-lambda-env.sh
   ```

### HybridTool 배포

HybridTool 배포도 동일한 순서로 진행됩니다.

**배포 순서가 중요한 이유**: BBN 배포와 동일합니다 (위 참고).

#### 전체 배포 (권장)
```bash
# 환경 변수 설정 확인
source scripts/config/.nppswrel-env

# 전체 배포 실행
bash scripts/deploy/hybridTool/deploy-hybridTool-all.sh
```

#### 단계별 배포

1. **Docker 이미지 빌드 및 ECR 푸시**
   ```bash
   bash scripts/deploy/hybridTool/deploy-hybridTool-docker.sh
   ```

2. **ECS Task Definition 등록**
   ```bash
   bash scripts/deploy/hybridTool/deploy-hybridTool-task-definition.sh
   ```

3. **Lambda 함수 배포**
   ```bash
   bash scripts/deploy/hybridTool/deploy-hybridTool-lambdas-all.sh
   ```

4. **Lambda 함수 환경 변수 설정**
   ```bash
   bash scripts/deploy/hybridTool/set-hybridTool-lambda-env.sh
   ```

### 웹사이트 배포

프론트엔드를 S3 + CloudFront에 배포합니다.

```bash
# 환경 변수 설정 확인
source scripts/config/.website-env

# 배포 실행
bash scripts/deploy/deploy-website.sh
```

**배포 프로세스**:
1. React 프로젝트 빌드 (`npm run build`)
2. S3 버킷에 업로드
3. CloudFront 캐시 무효화

---

## 주의사항

### 1. 환경 변수 보안
- ⚠️ **절대 Git에 커밋하지 마세요**: `.env`, `.nppswrel-env`, `.website-env` 파일은 모두 `.gitignore`에 포함되어 있습니다
- 환경 변수 파일은 로컬에만 보관하고, 공유 시 별도 채널로 공유하세요
- AWS 자격 증명이 포함된 파일은 특히 주의하세요

### 2. 배포 전 확인사항
- [ ] 환경 변수가 올바르게 설정되었는지 확인
- [ ] AWS CLI가 올바른 프로필로 설정되었는지 확인
- [ ] 필요한 AWS 리소스가 생성되어 있는지 확인
- [ ] Docker 이미지가 올바르게 빌드되는지 확인

### 3. Windows 개발 환경
- **Git Bash 사용 필수**: 배포 스크립트는 Unix 스타일 명령어를 사용합니다
- PowerShell 대신 Git Bash 터미널을 사용하세요
- 경로는 슬래시(`/`)를 사용하세요

### 4. Docker 이미지 태그
- 기본 태그는 `latest`입니다
- 프로덕션 배포 시 버전 태그 사용을 권장합니다:
  ```bash
  export DOCKER_IMAGE_TAG=v1.0.0
  ```

### 5. Lambda 함수 배포
- TypeScript Lambda 함수는 빌드 후 배포됩니다 (`lambda-build/` 폴더)
- Python Lambda 함수는 직접 배포됩니다
- 환경 변수는 배포 후 별도로 설정해야 합니다

### 6. ECS Task Definition
- Task Definition은 환경 변수 치환이 필요합니다
- 배포 스크립트가 자동으로 처리하지만, 수동 배포 시 `envsubst` 사용:
  ```bash
  envsubst < aws-configs/hybridTool-task-definition.json > /tmp/task-def.json
  ```

### 7. API Gateway 설정
- Lambda 함수 배포 후 API Gateway에 연결해야 합니다
- CORS 설정이 필요할 수 있습니다
- API Gateway ID는 환경 변수에 설정되어야 합니다

---

## 추가 리소스

### 유용한 명령어

**AWS 리소스 확인**:
```bash
# ECS 클러스터 확인
aws ecs describe-clusters --clusters bayesian-cluster

# ECR 리포지토리 확인
aws ecr describe-repositories --repository-names hybrid-tool-pymc

# Lambda 함수 목록
aws lambda list-functions --query 'Functions[*].FunctionName'

# DynamoDB 테이블 확인
aws dynamodb describe-table --table-name BayesianSimulationJobs
```

**로컬 개발 서버 실행**:
```bash
# 프론트엔드 개발 서버
cd apps/frontend
npm run dev
```

### 참고 문서
- [AWS ECS 공식 문서](https://docs.aws.amazon.com/ecs/)
- [AWS Lambda 공식 문서](https://docs.aws.amazon.com/lambda/)
- [Vite 공식 문서](https://vitejs.dev/)

---

**마지막 업데이트**: 2025년

