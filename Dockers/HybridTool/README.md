# HybridTool PyMC Fargate Task

PyMC 베이지안 추론 작업을 ECS Fargate에서 실행하기 위한 Docker 이미지 및 스크립트

## 구조

```
Dockers/HybridTool/
├── Dockerfile                      # PyMC, JAX 포함 Python 환경
├── run_sensitivity_analysis.py    # Sensitivity Analysis 스크립트
├── run_update_pfd.py              # Update PFD 스크립트
├── run_full_analysis.py            # Full Analysis 스크립트
├── .dockerignore
└── README.md
```

## 세 가지 작업 타입

### 1. Sensitivity Analysis (`run_sensitivity_analysis.py`)
- **기능**: 필요한 시험 수 계산
- **입력**: `PFD_GOAL`, `CONFIDENCE_GOAL`
- **출력**: S3에 `results/sensitivity-analysis-{JOB_ID}.json`

### 2. Update PFD (`run_update_pfd.py`)
- **기능**: 단일 샘플링으로 PFD 업데이트
- **입력**: `PFD_GOAL`, `DEMAND`, `FAILURES`
- **출력**: S3에 `results/update-pfd-{JOB_ID}.json`

### 3. Full Analysis (`run_full_analysis.py`)
- **기능**: 전체 분석 (sensitivity + 여러 demand 샘플링)
- **입력**: `PFD_GOAL`, `CONFIDENCE_GOAL`, `FAILURES`
- **출력**: S3에 `results/full-analysis-{JOB_ID}.json`

## 실행 흐름

1. Lambda 함수가 ECS Task 실행
2. 환경 변수 `TASK_TYPE`으로 스크립트 선택:
   - `sensitivity_analysis` → `run_sensitivity_analysis.py`
   - `update_pfd` → `run_update_pfd.py`
   - `full_analysis` → `run_full_analysis.py`
3. 환경 변수로 입력 파라미터 전달
4. 스크립트 실행 후 결과를 S3에 JSON으로 업로드
5. CloudWatch Logs에 로그 출력

## 환경 변수

### 공통 환경 변수
- `TASK_TYPE`: 작업 타입 (`sensitivity_analysis`, `update_pfd`, `full_analysis`)
- `JOB_ID`: 작업 식별자 (UUID)
- `S3_BUCKET`: 결과 저장 S3 버킷명
- `AWS_REGION`: AWS 리전

### Sensitivity Analysis 전용
- `PFD_GOAL`: 목표 PFD 값
- `CONFIDENCE_GOAL`: 목표 신뢰도

### Update PFD 전용
- `PFD_GOAL`: 목표 PFD 값
- `DEMAND`: 시험 횟수
- `FAILURES`: 관측된 실패 수

### Full Analysis 전용
- `PFD_GOAL`: 목표 PFD 값
- `CONFIDENCE_GOAL`: 목표 신뢰도
- `FAILURES`: 관측된 실패 수

## 빌드 및 배포

```bash
# 환경 변수 설정
cp scripts/.hybridTool-env.example scripts/.hybridTool-env
# .hybridTool-env 파일을 편집하여 값 설정

# Docker 이미지 빌드 및 ECR 푸시
./scripts/deploy-hybridTool-docker.sh
```

## 로컬 테스트

```bash
# Docker 이미지 빌드
docker build -t hybrid-tool-pymc:test -f Dockers/HybridTool/Dockerfile .

# Sensitivity Analysis 테스트
docker run --rm \
  -e TASK_TYPE=sensitivity_analysis \
  -e JOB_ID=test-123 \
  -e PFD_GOAL=0.0001 \
  -e CONFIDENCE_GOAL=0.95 \
  -e S3_BUCKET=hybrid-tool-results \
  -e AWS_REGION=ap-northeast-2 \
  -v ~/.aws:/root/.aws:ro \
  hybrid-tool-pymc:test

# Update PFD 테스트
docker run --rm \
  -e TASK_TYPE=update_pfd \
  -e JOB_ID=test-124 \
  -e PFD_GOAL=0.0001 \
  -e DEMAND=1000 \
  -e FAILURES=0 \
  -e S3_BUCKET=hybrid-tool-results \
  -e AWS_REGION=ap-northeast-2 \
  -v ~/.aws:/root/.aws:ro \
  hybrid-tool-pymc:test

# Full Analysis 테스트
docker run --rm \
  -e TASK_TYPE=full_analysis \
  -e JOB_ID=test-125 \
  -e PFD_GOAL=0.0001 \
  -e CONFIDENCE_GOAL=0.95 \
  -e FAILURES=0 \
  -e S3_BUCKET=hybrid-tool-results \
  -e AWS_REGION=ap-northeast-2 \
  -v ~/.aws:/root/.aws:ro \
  hybrid-tool-pymc:test
```

## 출력

- **Sensitivity Analysis**: `s3://{S3_BUCKET}/results/sensitivity-analysis-{JOB_ID}.json`
- **Update PFD**: `s3://{S3_BUCKET}/results/update-pfd-{JOB_ID}.json`
- **Full Analysis**: `s3://{S3_BUCKET}/results/full-analysis-{JOB_ID}.json`
- **CloudWatch Logs**: `/ecs/npp-hybrid-tool`
