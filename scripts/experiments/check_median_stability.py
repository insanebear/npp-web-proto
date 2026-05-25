#!/usr/bin/env python3
"""
같은 조건의 반복 실행 결과에서 PFD median 안정성 확인.

Usage:
  python check_median_stability.py <label> <result1.json> <result2.json> ...

Example:
  python check_median_stability.py All-Low rep1.json rep2.json rep3.json

Output (마지막 줄):
  STABILITY_PCT:<value>  — 쉘 스크립트에서 파싱용
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def load_pfd_median(path: str) -> float:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    output = data.get("output", data)
    pfd = output.get("PFD")
    if pfd is None:
        raise KeyError(f"'PFD' not found in {path}")
    median = pfd.get("median")
    if median is None:
        raise KeyError(f"'median' not found in PFD of {path}")
    return float(median)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    label = sys.argv[1]
    paths = sys.argv[2:]

    medians = []
    for path in paths:
        try:
            medians.append(load_pfd_median(path))
        except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
            print(f"  [ERROR] {path}: {e}")
            sys.exit(1)

    mn = min(medians)
    mx = max(medians)
    mean = sum(medians) / len(medians)
    rel_range_pct = (mx - mn) / mean * 100 if mean > 0 else float("inf")

    print(f"  [{label}]  medians: {' / '.join(f'{v:.4g}' for v in medians)}")
    print(f"    min={mn:.4g}  max={mx:.4g}  mean={mean:.4g}")
    print(f"    relative range = ({mx:.4g} - {mn:.4g}) / {mean:.4g} = {rel_range_pct:.1f}%")
    # 쉘 스크립트 파싱용 — 이 줄은 grep으로 추출
    print(f"STABILITY_PCT:{rel_range_pct:.2f}")


if __name__ == "__main__":
    main()
