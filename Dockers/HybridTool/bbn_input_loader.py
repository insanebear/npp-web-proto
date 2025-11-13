import json
from pathlib import Path
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import ClientError

from bbn_inference.data import bayesian_data_from_json, nrc_report_data
from bbn_inference.bbn_data_model import BayesianData


def _load_from_local(path_str: str) -> Dict[str, Any]:
    """Load JSON from local file system."""
    path = Path(path_str)
    if not path.is_file():
        raise FileNotFoundError(f"BBN input JSON file not found: {path_str}")
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in file {path_str}: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to load BBN input from file {path_str}: {str(e)}")


def _load_from_s3(bucket: str, key: str) -> Dict[str, Any]:
    """Load JSON from S3 bucket."""
    s3_client = boto3.client("s3")
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        body = response["Body"].read().decode("utf-8")
        return json.loads(body)
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        if error_code == 'NoSuchKey':
            raise FileNotFoundError(f"BBN input file not found in S3: s3://{bucket}/{key}")
        raise RuntimeError(f"Failed to load BBN input from S3 s3://{bucket}/{key}: {error_code}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in S3 file s3://{bucket}/{key}: {str(e)}")
    except Exception as e:
        raise RuntimeError(f"Failed to load BBN input from S3 s3://{bucket}/{key}: {str(e)}")


def load_bayesian_data_from_env(
    json_path: Optional[str],
    s3_bucket: Optional[str],
) -> BayesianData:
    """
    Load BayesianData from one of the provided sources.

    Priority:
      1. json_path pointing to local file (absolute or relative path)
      2. json_path interpreted as S3 key paired with s3_bucket
      3. Fall back to nrc_report_data defaults
    """
    data_obj: Optional[Dict[str, Any]] = None

    if json_path:
        if json_path.startswith("s3://"):
            # Allow full s3://bucket/key format
            _, _, remainder = json_path.partition("s3://")
            bucket, _, key = remainder.partition("/")
            if not bucket or not key:
                raise ValueError(f"Invalid S3 URI for BBN input: {json_path}")
            data_obj = _load_from_s3(bucket, key)
        elif s3_bucket:
            data_obj = _load_from_s3(s3_bucket, json_path)
        else:
            data_obj = _load_from_local(json_path)

    if data_obj is None:
        return nrc_report_data()

    return bayesian_data_from_json(data_obj)


