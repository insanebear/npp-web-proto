#!/usr/bin/env python3
"""
로컬에서 HybridTool 스크립트를 실행하기 위한 wrapper 스크립트
Docker 이미지 빌드 없이 빠르게 테스트할 수 있습니다.

사용법:
    python Dockers/HybridTool/run_local.py

환경 변수는 run_local.sh를 참고하거나 직접 export하여 설정하세요.
"""

import os
import sys
from pathlib import Path
from unittest.mock import MagicMock

# 프로젝트 루트 디렉토리 찾기
script_dir = Path(__file__).parent.absolute()
project_root = script_dir.parent.parent

# Python 경로 설정
# server_min을 먼저 추가하여 bbn_inference 모듈을 찾을 수 있도록 함
server_min_path = project_root / "server_min"
hybrid_tool_path = script_dir

sys.path.insert(0, str(server_min_path))
sys.path.insert(0, str(hybrid_tool_path))

# boto3를 mock하여 로컬 실행 시 boto3가 없어도 작동하도록 함
# 다른 모듈을 import하기 전에 mock을 설정해야 함
try:
    import boto3
except ImportError:
    # boto3가 없으면 mock 객체 생성
    mock_boto3 = MagicMock()
    mock_boto3.client = MagicMock(return_value=MagicMock())
    
    # botocore도 mock
    class MockClientError(Exception):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)
            self.response = kwargs.get('error_response', {})
    
    mock_botocore = MagicMock()
    mock_botocore.exceptions.ClientError = MockClientError
    
    # sys.modules에 mock 추가 (다른 모듈이 import할 때 사용됨)
    sys.modules['boto3'] = mock_boto3
    sys.modules['botocore'] = mock_botocore
    sys.modules['botocore.exceptions'] = mock_botocore.exceptions

# task_common.py가 /app/server를 sys.path에 추가하는데,
# 로컬 환경에서는 server_min을 /app/server로 인식하도록 심볼릭 링크를 만들거나
# 또는 task_common.py를 import하기 전에 /app/server를 server_min으로 매핑
# 하지만 더 간단하게는 server_min을 먼저 추가했으므로 문제없을 것임
# task_common.py의 sys.path.insert(0, '/app/server')는 존재하지 않는 경로를 추가하지만
# 이미 server_min이 sys.path에 있으므로 bbn_inference 모듈은 정상적으로 import됨

# bbn_input_loader는 같은 디렉토리(hybrid_tool_path)에 있으므로 문제없음

# 실행할 스크립트 선택
# Windows에서 multiprocessing을 사용할 때는 if __name__ == "__main__": 가드가 필수
if __name__ == "__main__":
    task_type = os.environ.get("TASK_TYPE", "full_analysis")
    
    if task_type == "full_analysis":
        from run_full_analysis import main
        main()
    elif task_type == "sensitivity_analysis":
        from run_sensitivity_analysis import main
        main()
    elif task_type == "update_pfd":
        from run_update_pfd import main
        main()
    elif task_type == "bbn_inference":
        from run_bbn_inference import main
        main()
    else:
        print(f"[ERROR] Unknown TASK_TYPE: {task_type}")
        print("[ERROR] Valid values: full_analysis, sensitivity_analysis, update_pfd, bbn_inference")
        sys.exit(1)

