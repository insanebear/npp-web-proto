# 로컬 환경 구축 및 테스트 가이드

## 1. 환경 구축

### 필요한 도구 설치
```bash
# 1. 설치 스크립트 실행
cd /Volumes/insanebearP31/Projects/npp-web-proto
./install_requirements.sh

# 2. R 설치 (스크립트에서 안내받은 경우)
cd /Volumes/insanebearP31/
curl -O https://cran.r-project.org/bin/macosx/base/R-4.4.1-arm64.pkg
sudo installer -pkg R-4.4.1-arm64.pkg -target /
```

## 2. 로컬 백엔드 서버 실행

```bash
# 가상환경 활성화
cd /Volumes/insanebearP31/Projects/npp-web-proto
source .venv/bin/activate

# 백엔드 서버 시작
python local_backend.py
```

서버가 `http://localhost:5000`에서 실행됩니다.

## 3. 프론트엔드 실행

새 터미널에서:
```bash
cd /Volumes/insanebearP31/Projects/npp-web-proto
npm run dev
```

## 4. 테스트 방법

1. 웹 브라우저에서 `http://localhost:5173` (또는 표시된 포트) 접속
2. Bayesian 페이지에서 시뮬레이션 파라미터 입력
3. "Start Simulation" 버튼 클릭
4. 결과가 `ResultsDisplay.tsx`에서 표시되는지 확인

## 5. 결과 확인

### 백엔드에서 생성되는 결과
- **위치**: `/Volumes/insanebearP31/Projects/npp-web-proto/local_results/`
- **형식**: `{job_id}.json`
- **내용**: Bayesian 시뮬레이션의 모든 파라미터 (PFD, SR_Total_Remained_Defect 등)

### 프론트엔드에서 표시되는 결과
- **PFD**: Probability of Failure on Demand
- **SR_Total_Remained_Defect**: Software Requirements 단계의 잔존 결함
- **SD_Total_Remained_Defect**: Software Design 단계의 잔존 결함
- **IM_Total_Remained_Defect**: Implementation 단계의 잔존 결함
- **ST_Total_Remained_Defect**: Software Testing 단계의 잔존 결함
- **IC_Total_Remained_Defect**: Integration & Commissioning 단계의 잔존 결함

각 파라미터는 다음 통계 정보를 포함합니다:
- Mean (평균)
- SD (표준편차)
- Median (중앙값)
- 95% CI (신뢰구간)

## 6. 문제 해결

### R 스크립트 실행 오류
```bash
# R 패키지 재설치
R -e "install.packages(c('rjags', 'jsonlite'), repos='https://cloud.r-project.org')"
```

### 백엔드 서버 오류
```bash
# Python 패키지 재설치
pip install --upgrade flask flask-cors
```

### 프론트엔드 연결 오류
- `src/services/apiService.ts`에서 `API_BASE_URL`이 `http://localhost:5000`인지 확인
- 백엔드 서버가 실행 중인지 확인

## 7. 개발 팁

### run_simulation.R 수정 시
1. `Dockers/BayesianPage/run_simulation_local.R` 파일 수정
2. 백엔드 서버 재시작
3. 새로운 시뮬레이션 실행

### ResultsDisplay.tsx 수정 시
1. 파일 수정 후 저장
2. 브라우저 새로고침
3. 결과 확인
