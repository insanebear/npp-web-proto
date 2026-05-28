#!/usr/bin/env python3
"""
JT (Jonckheere-Terpstra) test for ordered PFD distributions.

Usage:
  python compare_pfd_jt.py <label1>=<f1.json,f2.json,...> <label2>=... ...

  Groups must be in ascending PFD order (lowest PFD first).
  H1: PFD(group1) <= PFD(group2) <= ... with at least one strict inequality.

Example (SDLC, FP=200 fixed):
  python compare_pfd_jt.py \\
    All-High=rep1.json,rep2.json,...,rep10.json \\
    All-Medium=rep1.json,...,rep10.json \\
    All-Low=rep1.json,...,rep10.json
"""

import json
import sys
from pathlib import Path

import numpy as np
from scipy import stats

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


def parse_arg(arg: str):
    if "=" not in arg:
        raise ValueError(f"Expected label=file1,file2,... format, got: {arg}")
    label, paths_str = arg.split("=", 1)
    medians = [load_pfd_median(p.strip()) for p in paths_str.split(",") if p.strip()]
    return label, np.array(medians)


def kendall_tau(groups: list) -> float:
    concordant = discordant = total = 0
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            for a in groups[i]:
                for b in groups[j]:
                    total += 1
                    if a < b:
                        concordant += 1
                    elif a > b:
                        discordant += 1
    return (concordant - discordant) / total if total > 0 else 0.0


def tau_label(tau: float) -> str:
    if abs(tau) < 0.10:
        return "negligible"
    elif abs(tau) < 0.30:
        return "small"
    elif abs(tau) < 0.50:
        return "medium"
    return "large"


def jt_test(groups: list):
    """JT test (one-sided, ascending trend). Normal approximation.
    Returns (J_statistic, p_value).
    Assumes no ties; warns if ties detected.
    """
    all_vals = np.concatenate(groups)
    if len(all_vals) != len(set(all_vals.tolist())):
        print("  WARNING: tie(s) detected in data -- p-value may be slightly off (no tie correction applied)")

    N = sum(len(g) for g in groups)
    J = 0.0
    for i in range(len(groups)):
        for j in range(i + 1, len(groups)):
            for a in groups[i]:
                for b in groups[j]:
                    if a < b:
                        J += 1.0
                    elif a == b:
                        J += 0.5

    E_J = (N ** 2 - sum(len(g) ** 2 for g in groups)) / 4
    Var_J = (N ** 2 * (2 * N + 3) - sum(len(g) ** 2 * (2 * len(g) + 3) for g in groups)) / 72

    if Var_J <= 0:
        return J, 1.0
    Z = (J - E_J) / np.sqrt(Var_J)
    return J, float(1 - stats.norm.cdf(Z))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    labels, groups = [], []
    for arg in sys.argv[1:]:
        label, medians = parse_arg(arg)
        labels.append(label)
        groups.append(medians)

    print("\n=== JT Test: PFD Ordered Distribution Check ===\n")
    print(f"Groups (ascending PFD): {' < '.join(labels)}")
    print(f"NREPS per group       : {[len(g) for g in groups]}\n")

    print(f"{'Group':<18} {'n':>4} {'median':>12} {'mean':>12} {'std':>12}")
    print("-" * 60)
    for label, g in zip(labels, groups):
        print(
            f"{label:<18} {len(g):>4} {np.median(g):>12.4g}"
            f" {np.mean(g):>12.4g} {np.std(g, ddof=1):>12.4g}"
        )

    J_stat, p_value = jt_test(groups)
    tau = kendall_tau(groups)
    alpha = 0.05

    print(f"\n=== Jonckheere-Terpstra Test ===\n")
    print(f"  H0: 모든 그룹 분포가 동일")
    print(f"  H1: {' <= '.join(labels)} (단조 증가, 최소 하나 strict)")
    print(f"\n  JT statistic : {J_stat:.4f}")
    print(f"  p-value      : {p_value:.6f}")
    print(f"  Kendall's tau: {tau:.4f}  ({tau_label(tau)})")
    print(f"  alpha        : {alpha}")

    passed = p_value < alpha
    if passed:
        print(f"\n  -> PASS  p={p_value:.6f} < {alpha}")
        print(f"     단조 순서 {' < '.join(labels)} 통계적으로 유의미하게 확인됨")
    else:
        print(f"\n  -> FAIL  p={p_value:.6f} >= {alpha}")
        print(f"     단조 순서 통계적으로 확인되지 않음")

    print(f"\nJT_STATISTIC:{J_stat:.4f}")
    print(f"JT_PVALUE:{p_value:.6f}")
    print(f"JT_TAU:{tau:.4f}")
    print(f"JT_RESULT:{'PASS' if passed else 'FAIL'}")


if __name__ == "__main__":
    main()
