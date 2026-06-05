#!/usr/bin/env python3
"""
Compare PFD 95% HDI across multiple BBN run result JSONs.

Usage:
  python compare_pfd_hdi.py <label1>=<result1.json> <label2>=<result2.json> ...

Example:
  python compare_pfd_hdi.py \
    All-Low=tempDoc/hybrid-tool-test/comparison-xxx/results_bbn_results-all-low.json \
    All-Medium=tempDoc/hybrid-tool-test/comparison-xxx/results_bbn_results-all-medium.json \
    All-High=tempDoc/hybrid-tool-test/comparison-xxx/results_bbn_results-all-high.json

Pass/Fail criterion (right-skewed 분포 기준):
  median과 mean 모두 입력 순서대로 단조 감소하면 PASS.
  upper bound(hdi_97.5%)는 heavy-tailed 분포에서 극단 샘플에 민감하므로 제외.
"""

import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
from pathlib import Path


def load_pfd_stats(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    output = data.get("output", data)
    pfd = output.get("PFD")
    if pfd is None:
        raise KeyError(f"'PFD' not found in output of {path}")
    return pfd


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    entries = []
    for arg in sys.argv[1:]:
        if "=" not in arg:
            print(f"ERROR: expected label=path format, got: {arg}")
            sys.exit(1)
        label, path = arg.split("=", 1)
        pfd = load_pfd_stats(path)
        entries.append((label, pfd))

    print("\n=== PFD 95% HDI Comparison ===\n")
    print(f"{'Condition':<18} {'HDI lower':>14} {'HDI upper':>14} {'mean':>14} {'median':>14}")
    print("-" * 78)

    hdi_present = True
    for label, pfd in entries:
        lo     = pfd.get("hdi_2.5%")
        hi     = pfd.get("hdi_97.5%")
        mean   = pfd.get("mean")
        median = pfd.get("median")
        if lo is None or hi is None:
            print(f"{label:<18}  [HDI not available — re-run with updated code]")
            hdi_present = False
        else:
            print(f"{label:<18} {lo:>14.4g} {hi:>14.4g} {mean:>14.4g} {median:>14.4g}")

    if not hdi_present or len(entries) < 2:
        return

    medians = [pfd.get("median") for _, pfd in entries]
    means   = [pfd.get("mean")   for _, pfd in entries]

    median_ordered = all(medians[i] > medians[i + 1] for i in range(len(medians) - 1))
    mean_ordered   = all(means[i]   > means[i + 1]   for i in range(len(means)   - 1))

    median_str = " > ".join(f"{v:.4g}" for v in medians)
    mean_str   = " > ".join(f"{v:.4g}" for v in means)

    print("\n=== Separation Check (median & mean ordering) ===\n")
    print(f"  median : {median_str}  →  {'PASS ✓' if median_ordered else 'FAIL ✗'}")
    print(f"  mean   : {mean_str}  →  {'PASS ✓' if mean_ordered else 'FAIL ✗'}")

    if median_ordered and mean_ordered:
        print("\n  PASS — 두 지표 모두 조건 순서대로 단조 감소")
    elif median_ordered or mean_ordered:
        print("\n  PARTIAL — 한 지표만 순서 일치. 결과 재확인 권장")
    else:
        print("\n  FAIL — 조건별 입력값 확인 또는 draws/tune 증가 필요")


if __name__ == "__main__":
    main()
