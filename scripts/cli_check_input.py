"""
CLI utility: Validate and summarize Bayesian input JSON

Purpose
- Loads a Bayesian input JSON (either full object or { "input": { ... } })
- Converts it to BayesianData via server.bbn_inference.data.bayesian_data_from_json
- Prints a short summary (FP, complexity, attribute state counts)

Usage (from repo root, Git Bash on Windows)
  python scripts/cli_check_input.py \
    "/c/Users/<username>/Downloads/your-file.json"

Notes
- Accepts section labels as-is; expects inner field keys to be Python code keys (SR_*, SD_*, ...)
- FP accepts both FP_Input and "FP Input"
"""

import json
import sys
from server.bbn_inference.data import bayesian_data_from_json


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/cli_check_input.py <path-to-json>")
        sys.exit(1)

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)

    # allow top-level to have either full object or `{ input: {...} }`
    input_obj = obj.get("input", obj)

    bd = bayesian_data_from_json(input_obj)

    # summarize
    total = len(bd.attr_states)
    high = sum(1 for v in bd.attr_states.values() if v == 0)
    med = sum(1 for v in bd.attr_states.values() if v == 1)
    low = sum(1 for v in bd.attr_states.values() if v == 2)

    print("=== BayesianData summary ===")
    print(f"Function Point: {bd.function_point}")
    print(f"Complexity (0=High,1=Medium,2=Low): {bd.complexity}")
    print(f"Attributes: total={total}, High={high}, Medium={med}, Low={low}")


if __name__ == "__main__":
    main()


