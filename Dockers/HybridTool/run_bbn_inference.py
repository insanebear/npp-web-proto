#!/usr/bin/env python3
"""
ECS Fargate Task: BBN Inference (using PyMC MCMC)

Receives attribute state env vars from Lambda,
runs PyMC composite model, 
and saves:
  1. results/results-{JOB_ID}.json
  2. results/prior-trace-{JOB_ID}.nc — full InferenceData trace for downstream tasks

Environment variables (passed by BayesianStarterLambda as flat key=value):
- JOB_ID: Job identifier
- S3_BUCKET: S3 bucket name for results
- AWS_REGION: AWS region
- FP_Input: function point value
- SR_SDP_state, SR_CD_state, ... (all attribute state values)
- nChains, nIter, nBurnin, nThin: MCMC settings
- JOBS_TABLE_NAME: (optional) DynamoDB table for job status
- TEST_MODE: (optional) skip computation, use dummy values
- TEST_OUTPUT_DIR: (optional) save results locally instead of S3
"""

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

import boto3
import numpy as np

sys.path.insert(0, '/app/server')

from task_common import save_trace_to_s3, update_job_status
from bbn_inference.runners.composite_model import run_composite_model
from bbn_inference.data import bayesian_data_from_json
from bbn_inference.bbn_data_model import BayesianData

# Used to reconstruct sectioned input JSON from flat env vars
SECTION_KEYS: Dict[str, list] = {
    "FP": ["FP_Input"],
    "Requirement Dev": [
        "SR_SDP_state", "SR_CD_state", "SR_SRS_state", "SR_TA_state", "SR_CA_state",
        "SR_HA_state", "SR_SA_state", "SR_RA_state", "SR_SQTPG_state", "SR_SATPG_state",
        "SR_CM_state", "SR_RaA_state",
    ],
    "Requirement V&V": [
        "SR_SVVP_state", "SR_CDE_state", "SR_HRAA_state", "SR_SRE_state", "SR_IAVV_state",
        "SR_TAVV_state", "SR_CAVV_state", "SR_HAVV_state", "SR_SAVV_state", "SR_RAVV_state",
        "SR_VVSQTPG_state", "SR_VVSATPG_state", "SR_CMA_state", "SR_RaAVV_state", "SR_VVASRG_state",
    ],
    "Design Dev": [
        "SD_SAD_state", "SD_SDD_state", "SD_TA_state", "SD_CA_state", "SD_HA_state",
        "SD_SA_state", "SD_RA_state", "SD_SCTPG_state", "SD_SITPG_state", "SD_SCTDG_state",
        "SD_SITDG_state", "SD_SQTDG_state", "SD_SATDG_state", "SD_CM_state", "SD_RaA_state",
    ],
    "Design V&V": [
        "SD_DE_state", "SD_IAVV_state", "SD_TAVV_state", "SD_CAVV_state", "SD_HAVV_state",
        "SD_SAVV_state", "SD_RAVV_state", "SD_VVSCTPG_state", "SD_VVSITPG_state",
        "SD_VVSCTDG_state", "SD_VVSITDG_state", "SD_VVSQTDG_state", "SD_VVSATDG_state",
        "SD_CMVV_state", "SD_RaAVV_state", "SD_VVASRG_state",
    ],
    "Implementation Dev": [
        "IM_SCaSCDG_state", "IM_TA_state", "IM_CA_state", "IM_HA_state", "IM_SA_state",
        "IM_RA_state", "IM_CTCG_state", "IM_SITCG_state", "IM_SQTCG_state", "IM_SATCG_state",
        "IM_SCTPG_state", "IM_SITPG_state", "IM_SQTPG_state", "IM_SCTE_state",
        "IM_CM_state", "IM_RaA_state",
    ],
    "Implementation V&V": [
        "IM_SCaSCDE_state", "IM_IAVV_state", "IM_TAVV_state", "IM_CAVV_state", "IM_HAVV_state",
        "IM_SAVV_state", "IM_RAVV_state", "IM_VVSCTCG_state", "IM_VVSITCG_state",
        "IM_VVSQTCG_state", "IM_VVSATCG_state", "IM_VVSCTPG_state", "IM_VVSITPG_state",
        "IM_VVSQTPG_state", "IM_VVSCTE_state", "IM_CMVV_state", "IM_RaAVV_state", "IM_VVASRG_state",
    ],
    "Test Dev": [
        "ST_TA_state", "ST_HA_state", "ST_SA_state", "ST_RA_state", "ST_SATE_state",
        "ST_SAPG_state", "ST_SITE_state", "ST_SQTE_state", "ST_CM_state", "ST_RaA_state",
    ],
    "Test V&V": [
        "ST_TAVV_state", "ST_HAVV_state", "ST_SAVV_state", "ST_RAVV_state", "ST_VVSATE_state",
        "ST_VVSAPG_state", "ST_VVSITE_state", "ST_VVSQTE_state", "ST_CMVV_state",
        "ST_RaAVV_state", "ST_VVASRG_state",
    ],
    "Installation and Checkout Dev": [
        "IC_IPG_state", "IC_IaC_state", "IC_HA_state", "IC_SA_state", "IC_RA_state",
    ],
    "Installation and Checkout V&V": [
        "IC_ICAVV_state", "IC_ICVV_state", "IC_HAVV_state", "IC_SAVV_state", "IC_RAVV_state",
        "IC_VVASRG_state", "IC_VVFRG_state",
    ],
}

SETTINGS_KEYS = ["nChains", "nIter", "nBurnin", "nThin", "computeDIC", "includeTraceData"]


def build_input_json_from_env() -> Dict[str, Any]:
    """Reconstruct sectioned input JSON from flat env vars."""
    input_json: Dict[str, Any] = {}

    for section, keys in SECTION_KEYS.items():
        section_data = {}
        for key in keys:
            val = os.environ.get(key)
            if val is not None:
                section_data[key] = val
        if section_data:
            input_json[section] = section_data

    settings = {}
    for key in SETTINGS_KEYS:
        val = os.environ.get(key)
        if val is not None:
            settings[key] = val
    if settings:
        input_json["settings"] = settings

    return input_json


def get_job_config() -> Dict[str, Any]:
    config = {
        "JOB_ID": os.environ.get("JOB_ID"),
        "S3_BUCKET": os.environ.get("S3_BUCKET"),
        "AWS_REGION": os.environ.get("AWS_REGION", "ap-northeast-2"),
        "TEST_MODE": os.environ.get("TEST_MODE", "false").lower() == "true",
        "TEST_OUTPUT_DIR": os.environ.get("TEST_OUTPUT_DIR"),
        "JOBS_TABLE_NAME": os.environ.get("JOBS_TABLE_NAME"),
        "DRAWS": int(os.environ.get("nIter", os.environ.get("DRAWS", "1000"))),
        "TUNE": int(os.environ.get("nBurnin", os.environ.get("TUNE", "100"))),
        "CHAINS": int(os.environ.get("nChains", os.environ.get("CHAINS", "4"))),
        "THIN": int(os.environ.get("nThin", os.environ.get("THIN", "1"))),
    }

    if not config["JOB_ID"]:
        raise ValueError("JOB_ID environment variable is required")
    if not config["S3_BUCKET"]:
        raise ValueError("S3_BUCKET environment variable is required")

    print(f"[CONFIG] JOB_ID: {config['JOB_ID']}")
    print(f"[CONFIG] S3_BUCKET: {config['S3_BUCKET']}")
    print(f"[CONFIG] AWS_REGION: {config['AWS_REGION']}")
    print(f"[CONFIG] DRAWS: {config['DRAWS']}")
    print(f"[CONFIG] TUNE: {config['TUNE']}")
    print(f"[CONFIG] CHAINS: {config['CHAINS']}")
    print(f"[CONFIG] THIN: {config['THIN']}")

    return config


def _pfd_stats(pfd_samples: Any) -> Dict[str, float]:
    """Compute summary statistics from PFD posterior samples."""
    values = np.array(pfd_samples).flatten()
    return {
        "mean": float(values.mean()),
        "sd": float(values.std()),
        "median": float(np.median(values)),
        "q2_5": float(np.percentile(values, 2.5)),
        "q97_5": float(np.percentile(values, 97.5)),
    }


def _save_results(config: Dict[str, Any], result_json: Dict[str, Any]) -> str:
    """Save JSON results to S3 or locally."""
    job_id = config["JOB_ID"]
    s3_key = f"results/results-{job_id}.json"
    test_output_dir = config["TEST_OUTPUT_DIR"]

    if test_output_dir:
        output_path = Path(test_output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        local_file = output_path / s3_key.replace("/", "_")
        local_file.write_text(json.dumps(result_json, indent=2), encoding="utf-8")
        print(f"[TEST MODE] Results saved locally to {local_file}")
        return str(local_file)
    else:
        s3_client = boto3.client('s3', region_name=config["AWS_REGION"])
        s3_client.put_object(
            Bucket=config["S3_BUCKET"],
            Key=s3_key,
            Body=json.dumps(result_json, indent=2),
            ContentType="application/json",
        )
        print(f"[UPLOAD] Results uploaded to s3://{config['S3_BUCKET']}/{s3_key}")
        return s3_key


def main():
    print("=" * 80)
    print("HybridTool BBN Inference - Starting")
    print("=" * 80)

    dynamodb_client = None
    config = {}

    try:
        config = get_job_config()
        job_id = config["JOB_ID"]

        if config["JOBS_TABLE_NAME"]:
            dynamodb_client = boto3.client('dynamodb', region_name=config["AWS_REGION"])

        update_job_status(dynamodb_client, config, status='RUNNING')

        # Reconstruct input JSON from flat env vars
        input_json = build_input_json_from_env()
        bbn_data: BayesianData = bayesian_data_from_json(input_json)

        if config["TEST_MODE"]:
            print("\n[TEST MODE] Skipping computation, using dummy values")
            pfd_stats = {
                "mean": 0.0001, "sd": 0.00005,
                "median": 0.0001, "q2_5": 0.00005, "q97_5": 0.00015,
            }
            trace_s3_key = None
        else:
            # Run composite model
            print("\n[STEP 1] Running composite model...")
            trace = run_composite_model(
                bbn_data,
                draws=config["DRAWS"],
                tune=config["TUNE"],
                chains=config["CHAINS"],
                thin=config["THIN"],
            )
            print("[STEP 1] Composite model completed")

            # Compute PFD statistics
            pfd_stats = _pfd_stats(trace.posterior["PFD"])
            print(f"[STEP 1] PFD mean: {pfd_stats['mean']:.6g}, sd: {pfd_stats['sd']:.6g}")

            # Save trace to S3
            print("\n[STEP 2] Saving trace to S3...")
            trace_s3_key = save_trace_to_s3(trace, config, job_id)
            print(f"[STEP 2] Trace saved: {trace_s3_key}")

        # Build result JSON
        result_json = {
            "input": input_json,
            "output": {"PFD": pfd_stats},
        }
        s3_location = _save_results(config, result_json)

        s3_key_for_db = s3_location if not config["TEST_OUTPUT_DIR"] else None
        update_job_status(dynamodb_client, config, status='COMPLETED', s3_key=s3_key_for_db)

        print("\n" + "=" * 80)
        print("HybridTool BBN Inference - Completed Successfully")
        print("=" * 80)

        completion_payload = {
            "status": "completed",
            "job_id": job_id,
        }
        if config["TEST_OUTPUT_DIR"]:
            completion_payload["local_path"] = s3_location
        else:
            completion_payload["s3_location"] = f"s3://{config['S3_BUCKET']}/{s3_location}"

        print(json.dumps(completion_payload))

    except Exception as e:
        job_id = config.get("JOB_ID", "unknown")
        error_msg = f"BBN Inference failed: {str(e)}"
        print(f"\n[ERROR] {error_msg}", file=sys.stderr)
        update_job_status(dynamodb_client, config, status='FAILED', error_msg=error_msg)
        print(json.dumps({"status": "failed", "job_id": job_id, "error": error_msg}))
        sys.exit(1)


if __name__ == "__main__":
    main()
