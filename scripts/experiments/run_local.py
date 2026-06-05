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

script_dir = Path(__file__).parent.absolute()
project_root = script_dir.parent.parent

server_min_path = project_root / "server_min"
hybrid_tool_path = script_dir

sys.path.insert(0, str(server_min_path))
sys.path.insert(0, str(hybrid_tool_path))

# 다른 모듈을 import하기 전에 mock을 설정해야 함
try:
    import boto3
except ImportError:
    mock_boto3 = MagicMock()
    mock_boto3.client = MagicMock(return_value=MagicMock())

    class MockClientError(Exception):
        def __init__(self, *args, **kwargs):
            super().__init__(*args)
            self.response = kwargs.get('error_response', {})

    mock_botocore = MagicMock()
    mock_botocore.exceptions.ClientError = MockClientError

    sys.modules['boto3'] = mock_boto3
    sys.modules['botocore'] = mock_botocore
    sys.modules['botocore.exceptions'] = mock_botocore.exceptions

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
