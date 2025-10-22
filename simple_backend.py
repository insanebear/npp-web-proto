#!/usr/bin/env python3
"""
R 없이 테스트할 수 있는 간단한 백엔드 서버
"""

import json
import uuid
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 결과 저장 디렉토리
RESULTS_DIR = "/Volumes/insanebearP31/Projects/npp-web-proto/local_results"

@app.route('/simulations/bayesian', methods=['POST'])
def start_simulation():
    """시뮬레이션 시작 - 테스트용 더미 데이터 반환"""
    try:
        data = request.get_json()
        form_data = json.loads(data.get('data', '{}'))
        
        # 고유한 job ID 생성
        job_id = str(uuid.uuid4())
        
        # 테스트용 더미 결과 생성
        dummy_results = {
            "PFD": {
                "mean": 0.002551391491596329,
                "sd": 0.000123456789,
                "median": 0.002500000000000000,
                "q2_5": 0.002300000000000000,
                "q97_5": 0.002800000000000000
            },
            "SR_Total_Remained_Defect": {
                "mean": 15.234567890123456,
                "sd": 2.345678901234567,
                "median": 15.000000000000000,
                "q2_5": 11.000000000000000,
                "q97_5": 20.000000000000000
            },
            "SD_Total_Remained_Defect": {
                "mean": 12.876543210987654,
                "sd": 1.876543210987654,
                "median": 12.500000000000000,
                "q2_5": 9.500000000000000,
                "q97_5": 16.500000000000000
            },
            "IM_Total_Remained_Defect": {
                "mean": 8.765432109876543,
                "sd": 1.234567890123456,
                "median": 8.500000000000000,
                "q2_5": 6.500000000000000,
                "q97_5": 11.500000000000000
            },
            "ST_Total_Remained_Defect": {
                "mean": 5.432109876543210,
                "sd": 0.876543210987654,
                "median": 5.200000000000000,
                "q2_5": 3.800000000000000,
                "q97_5": 7.200000000000000
            },
            "IC_Total_Remained_Defect": {
                "mean": 2.109876543210987,
                "sd": 0.432109876543210,
                "median": 2.000000000000000,
                "q2_5": 1.300000000000000,
                "q97_5": 3.000000000000000
            }
        }
        
        # 결과를 파일로 저장
        import os
        os.makedirs(RESULTS_DIR, exist_ok=True)
        result_file = f"{RESULTS_DIR}/{job_id}.json"
        with open(result_file, 'w') as f:
            json.dump(dummy_results, f, indent=2)
        
        return jsonify({
            "message": "Simulation completed (dummy data)",
            "jobId": job_id,
            "status": "COMPLETED",
            "result": dummy_results
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/jobs/<job_id>')
def get_job_status(job_id):
    """작업 상태 조회"""
    import os
    result_file = f"{RESULTS_DIR}/{job_id}.json"
    
    if os.path.exists(result_file):
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
    return jsonify({
        "downloadUrl": f"http://localhost:5000/jobs/{job_id}/results"
    })

@app.route('/jobs/<job_id>/results')
def download_results(job_id):
    """결과 파일 다운로드"""
    from flask import send_file
    import os
    result_file = f"{RESULTS_DIR}/{job_id}.json"
    
    if os.path.exists(result_file):
        return send_file(result_file, as_attachment=True)
    else:
        return jsonify({"error": "Results not found"}), 404

@app.route('/health')
def health_check():
    """서버 상태 확인"""
    return jsonify({"status": "ok", "message": "Simple backend server is running"})

if __name__ == '__main__':
    print("간단한 백엔드 서버 시작...")
    print("결과 저장 디렉토리:", RESULTS_DIR)
    app.run(host='0.0.0.0', port=5001, debug=True)
