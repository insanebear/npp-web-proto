# server/bbn_inference/api.py

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
import os, json, uuid

from bbn_inference.sensitivity_analysis import (
    get_number_of_required_demand,
    filter_outsiders,
    get_confidence,
    demand_model_func,
)
from bbn_inference.examples.example_for_composite_model import run_example_for_composite_model
from bbn_inference.bbn_utils import run_sampling
from bbn_inference.data import bayesian_data_from_json
from bbn_inference.bbn_data_model import BayesianData

router = APIRouter()

# ---------------- 저장 경로 ----------------
# (참고) main.py에서 StaticFiles로 /result_json 마운트해도 되지만,
#       실제 다운로드는 /api/download 엔드포인트를 쓰면 attachment로 떨어집니다.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))                  # server/bbn_inference
RESULT_DIR = os.path.join(os.path.dirname(BASE_DIR), "result_json")    # server/result_json
os.makedirs(RESULT_DIR, exist_ok=True)

# ---------------- Trace 캐시 (개발용 간단 캐시) ----------------
_TRACE_CACHE: Dict[str, Dict[str, Any]] = {}

def _build_and_cache_trace() -> str:
    trace = run_example_for_composite_model()
    trace_id = str(uuid.uuid4())
    _TRACE_CACHE[trace_id] = {
        "trace": trace,
        "filtered_pfd_trace": filter_outsiders(trace.posterior["PFD"]),
        "prior_mean": trace.posterior["PFD"].mean().item(),
        "prior_conf_getter": lambda pfd_goal: get_confidence(
            data=trace.posterior["PFD"], goal=pfd_goal
        ),
    }
    print(f"[TRACE] New trace created: trace_id={trace_id}")
    return trace_id

def _get_trace(trace_id: Optional[str]):
    if trace_id and trace_id in _TRACE_CACHE:
        return _TRACE_CACHE[trace_id]["trace"], _TRACE_CACHE[trace_id]
    new_id = _build_and_cache_trace()
    return _TRACE_CACHE[new_id]["trace"], _TRACE_CACHE[new_id]

# ---------------- 입력 스키마 ----------------
class InitTraceOutput(BaseModel):
    trace_id: str

class SensitivityInput(BaseModel):
    pfd_goal: float = Field(..., gt=0, description="목표 PFD (예: 1e-4)")
    confidence_goal: float = Field(..., gt=0, lt=1, description="목표 신뢰도 (예: 0.95)")
    trace_id: Optional[str] = Field(None, description="재사용할 trace_id (선택)")

class UpdatePFDInput(BaseModel):
    pfd_goal: float = Field(..., gt=0, description="목표 PFD")
    demand: int = Field(..., gt=0, description="시험 횟수(테스트 수)")
    failures: int = Field(..., ge=0, description="관측된 실패 수")
    trace_id: Optional[str] = Field(None, description="재사용할 trace_id (선택)")

class FullAnalysisInput(BaseModel):
    pfd_goal: float
    confidence_goal: float
    failures: int
    trace_id: Optional[str] = Field(None, description="재사용할 trace_id (선택)")

class InputJsonPayload(BaseModel):
    input: Dict[str, Any]

# ---------------- 0) trace 초기화 ----------------
@router.post("/init-trace")
def init_trace() -> Dict[str, Any]:
    try:
        trace_id = _build_and_cache_trace()
        prior_mean = _TRACE_CACHE[trace_id]["prior_mean"]
        print(f"[INIT] trace_id={trace_id}, prior_mean={prior_mean}")
        return {"message": "Trace initialized", "trace_id": trace_id, "prior_mean": prior_mean}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Init trace failed: {e}")

# ---------------- 1) Number of Tests 계산 ----------------
@router.post("/sensitivity-analysis")
def sensitivity_analysis(input: SensitivityInput):
    try:
        trace, ctx = _get_trace(input.trace_id)
        num_tests = get_number_of_required_demand(
            trace, pfd_goal=input.pfd_goal, confidence_goal=input.confidence_goal
        )
        prior_mean = ctx["prior_mean"]
        prior_conf = ctx["prior_conf_getter"](input.pfd_goal)

        print(f"[SENS] trace_id={input.trace_id or 'new'}")
        print(f"[SENS] PFD goal: {input.pfd_goal}, Confidence goal: {input.confidence_goal}")
        print(f"[SENS] Prior PFD mean: {prior_mean}")
        print(f"[SENS] Required number of tests: {int(num_tests)}")
        print(f"[SENS] Prior confidence @goal: {prior_conf}")

        ensured_id = None
        for k, v in _TRACE_CACHE.items():
            if v["trace"] is trace:
                ensured_id = k
                break

        return {
            "message": "Sensitivity analysis complete",
            "trace_id": ensured_id,
            "data": {
                "num_tests": int(num_tests),
                "prior_mean": prior_mean,
                "prior_confidence": prior_conf,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sensitivity analysis failed: {e}")

# ---------------- 2) PFD 업데이트 ----------------
@router.post("/update-pfd")
def update_pfd(input: UpdatePFDInput):
    try:
        if input.failures > input.demand:
            raise HTTPException(status_code=400, detail="failures cannot exceed demand")

        trace, ctx = _get_trace(input.trace_id)
        filtered_pfd_trace = ctx["filtered_pfd_trace"]

        model = demand_model_func(
            demand=input.demand,
            observed_failures=input.failures,
            pfd_trace=filtered_pfd_trace,
        )
        updated_trace = run_sampling(model, draws=2000, tune=500)

        prior_mean = ctx["prior_mean"]
        updated_pfd_mean = updated_trace.posterior["pfd_prior"].mean().item()
        before_conf = ctx["prior_conf_getter"](input.pfd_goal)
        updated_conf = get_confidence(
            data=updated_trace.posterior["pfd_prior"], goal=input.pfd_goal
        )

        print(f"[UPD] trace_id={input.trace_id or 'new'}")
        print(f"[UPD] Mean of prior PFD: {prior_mean}")
        print(f"[UPD] Mean of updated PFD: {updated_pfd_mean}")
        print(f"[UPD] PFD goal: {input.pfd_goal}")
        print(f"[UPD] Before testing, confidence level: {before_conf}")
        print(f"[UPD] Testing results: #test cases: {input.demand}, #failures: {input.failures}")
        print(f"[UPD] After testing, confidence level: {updated_conf}")

        ensured_id = None
        for k, v in _TRACE_CACHE.items():
            if v["trace"] is trace:
                ensured_id = k
                break

        return {
            "message": "PFD updated",
            "trace_id": ensured_id,
            "data": {
                "updated_pfd": updated_pfd_mean,
                "updated_confidence": updated_conf,
                "prior_confidence": before_conf,
            },
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Update PFD failed: {e}")

# ---------------- 3) 전체 분석 + JSON 저장 ----------------
@router.post("/full-analysis")
def run_full_analysis(input: FullAnalysisInput):
    try:
        pfd_goal = input.pfd_goal
        confidence_goal = input.confidence_goal
        failures = input.failures

        trace, ctx = _get_trace(input.trace_id)

        demand_required = get_number_of_required_demand(
            trace, pfd_goal=pfd_goal, confidence_goal=confidence_goal
        )

        filtered_pfd_trace = ctx["filtered_pfd_trace"]
        prior_mean = ctx["prior_mean"]
        prior_conf = ctx["prior_conf_getter"](pfd_goal)

        demand_list = list(range(500, int(demand_required) + 500, 500))
        pfd_output, last_conf = [], None

        print(f"[FULL] trace_id={input.trace_id or 'new'}")
        print(f"[FULL] Required number of tests: {int(demand_required)}")
        print(f"[FULL] Prior mean: {prior_mean}, Prior confidence @goal: {prior_conf}")

        for demand in demand_list:
            model = demand_model_func(
                demand=demand, observed_failures=failures, pfd_trace=filtered_pfd_trace
            )
            updated_trace = run_sampling(model, draws=2000, tune=500)
            updated_mean = updated_trace.posterior["pfd_prior"].mean().item()
            last_conf = get_confidence(
                data=updated_trace.posterior["pfd_prior"], goal=pfd_goal
            )
            pfd_output.append([str(demand), updated_mean])
            print(f"[FULL] Demand={demand} → PFD={updated_mean}, Confidence={last_conf}")

        result_json = {
            "input": {
                "parameter": {
                    "test_count": int(demand_required),
                    "target": pfd_goal,
                    "prior": {
                        "distribution": "trace",
                        "mean": prior_mean,
                        "confidence": prior_conf,
                    },
                    "observed_failures": failures,
                }
            },
            "output": {"pfd": pfd_output, "confidence": last_conf},
        }

        # 고유 파일명으로 저장 (서버 내부 파일명)
        public_name = f"{uuid.uuid4()}.json"
        filepath = os.path.join(RESULT_DIR, public_name)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result_json, f, indent=2)

        ensured_id = None
        for k, v in _TRACE_CACHE.items():
            if v["trace"] is trace:
                ensured_id = k
                break

        print(f"[FULL] Saved result to {filepath}")

        # 브라우저에서 바로 다운로드되는 엔드포인트 반환
        download_url = f"/api/download/{public_name}"

        return {
            "message": "Analysis complete",
            "trace_id": ensured_id,
            "filepath": filepath,          # 서버 내부 경로(로그용)
            "download_url": download_url,  # 프론트는 이 URL을 사용
            "result": result_json,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full analysis failed: {e}")

# ---------------- 4) 다운로드 전용 엔드포인트 ----------------
@router.get("/download/{file_name}")
def download_result(file_name: str):
    """
    저장된 JSON을 첨부(attachment)로 내려서 브라우저 다운로드 트레이로 바로 떨어지게 함.
    파일명은 'update_pfd_result_YYYYMMDD.json' 형식으로 지정됨.
    """
    safe_name = os.path.basename(file_name)  # 경로 탈출 방지
    path = os.path.join(RESULT_DIR, safe_name)
    if not os.path.isfile(path):
        raise HTTPException(status_code=404, detail="File not found")

    # 오늘 날짜 붙여서 다운로드 파일명 지정
    today_str = datetime.now().strftime("%Y%m%d")
    download_name = f"update_pfd_result_{today_str}.json"

    return FileResponse(
        path,
        media_type="application/json",
        filename=download_name,  # 다운로드 파일명 강제
    )

# ---------------- X) JSON -> BayesianData 파싱 테스트/유틸 ----------------
@router.post("/bbn/parse-input")
def parse_input_to_bbn(payload: InputJsonPayload):
    try:
        bd: BayesianData = bayesian_data_from_json(payload.input)
        # 간단한 요약 정보만 반환 (연결 확인용)
        non_default = sum(1 for k, v in bd.attr_states.items())
        return {
            "message": "Parsed successfully",
            "function_point": bd.function_point,
            "complexity": bd.complexity,
            "attributes_count": non_default,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse input: {e}")
