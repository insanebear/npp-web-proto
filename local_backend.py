#!/usr/bin/env python3
"""
로컬 테스트용 백엔드 서버
run_simulation.R의 결과를 ResultsDisplay.tsx에서 표시할 수 있도록 하는 서버
"""

import json
import os
import subprocess
import tempfile
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

# 결과 저장 디렉토리
RESULTS_DIR = Path("/Volumes/insanebearP31/Projects/npp-web-proto/local_results")
RESULTS_DIR.mkdir(exist_ok=True)

@app.route('/simulations/bayesian', methods=['POST'])
def start_simulation():
    """시뮬레이션 시작"""
    try:
        data = request.get_json()
        form_data = json.loads(data.get('data', '{}'))
        
        # 고유한 job ID 생성
        job_id = str(uuid.uuid4())
        
        # 시뮬레이션 실행 (비동기로 처리)
        result = run_bayesian_simulation(job_id, form_data)
        
        return jsonify({
            "message": "Simulation started",
            "jobId": job_id,
            "status": "COMPLETED" if result["success"] else "FAILED",
            "result": result.get("data")
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/jobs/<job_id>')
def get_job_status(job_id):
    """작업 상태 조회"""
    result_file = RESULTS_DIR / f"{job_id}.json"
    
    if result_file.exists():
        return jsonify({
            "jobId": job_id,
            "jobStatus": "COMPLETED"
        })
    else:
        return jsonify({
            "jobId": job_id,
            "jobStatus": "PENDING"
        }), 404

@app.route('/jobs/<job_id>/results-url', methods=['POST'])
def get_results_url(job_id):
    """결과 다운로드 URL 생성"""
    result_file = RESULTS_DIR / f"{job_id}.json"
    
    if result_file.exists():
        return jsonify({
            "downloadUrl": f"http://localhost:5001/jobs/{job_id}/results"
        })
    else:
        return jsonify({"error": "Results not found"}), 404

@app.route('/jobs/<job_id>/results')
def download_results(job_id):
    """결과 파일 다운로드"""
    result_file = RESULTS_DIR / f"{job_id}.json"
    
    if result_file.exists():
        return send_file(result_file, as_attachment=True)
    else:
        return jsonify({"error": "Results not found"}), 404

def run_bayesian_simulation(job_id, form_data):
    """Bayesian 시뮬레이션 실행"""
    try:
        # 환경변수 설정
        env = os.environ.copy()
        env.update({
            "FP Input": str(form_data.get("tab1", {}).get("FP Input", 50)),
            "Software Development Planning": form_data.get("tab1", {}).get("Software Development Planning", "Medium"),
            "Development of Concept": form_data.get("tab1", {}).get("Development of Concept", "Medium"),
            "nChains": str(form_data.get("settings", {}).get("nChains", 2)),
            "nIter": str(form_data.get("settings", {}).get("nIter", 1000)),
            "nBurnin": str(form_data.get("settings", {}).get("nBurnin", 500))
        })
        
        # R 스크립트 실행
        script_path = "/Volumes/insanebearP31/Projects/npp-web-proto/Dockers/BayesianPage/run_simulation_local.R"
        
        if not os.path.exists(script_path):
            return {"success": False, "error": "R script not found"}
        
        # R 스크립트 실행
        result = subprocess.run(
            ["Rscript", script_path],
            env=env,
            capture_output=True,
            text=True,
            cwd="/Volumes/insanebearP31/Projects/npp-web-proto/Dockers/BayesianPage"
        )
        
        if result.returncode == 0:
            # 결과 파일 읽기
            result_file = "/Volumes/insanebearP31/Projects/npp-web-proto/Dockers/BayesianPage/local_test_results.json"
            
            if os.path.exists(result_file):
                with open(result_file, 'r') as f:
                    simulation_data = json.load(f)
                
                # 결과를 job_id로 저장
                output_file = RESULTS_DIR / f"{job_id}.json"
                with open(output_file, 'w') as f:
                    json.dump(simulation_data, f, indent=2)
                
                return {"success": True, "data": simulation_data}
            else:
                return {"success": False, "error": "Result file not generated"}
        else:
            return {"success": False, "error": f"R script failed: {result.stderr}"}
            
    except Exception as e:
        return {"success": False, "error": str(e)}

if __name__ == '__main__':
    print("로컬 백엔드 서버 시작...")
    print("결과 저장 디렉토리:", RESULTS_DIR)
    app.run(host='0.0.0.0', port=5000, debug=True)
