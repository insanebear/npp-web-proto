#!/usr/bin/env python3
"""
Bootstrap-based power analysis for JT test.
Estimates minimum NREPS to achieve target power using pilot data.

Usage:
  python power_test_jt.py \\
    <label1>=<f1.json,f2.json,...> \\
    <label2>=... \\
    ... \\
    [--alpha 0.05] [--target-power 0.80] [--B 1000] \\
    [--out-dir /path/to/output]

  Groups must be in ascending PFD order (same as compare_pfd_jt.py).
"""

import argparse
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
    return float(pfd["median"])


def parse_arg(arg: str):
    if "=" not in arg:
        raise ValueError(f"Expected label=file1,file2,... format: {arg}")
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


def jt_test(groups: list, warn: bool = True) -> float:
    """JT test p-value (one-sided: ascending trend, alternative='greater').
    Normal approximation (Hollander & Wolfe 1999).
    Assumes no ties; warns if ties detected (suppressed in bootstrap via warn=False).
    """
    if warn:
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
        return 1.0
    Z = (J - E_J) / np.sqrt(Var_J)
    return float(1 - stats.norm.cdf(Z))


def bootstrap_power(groups: list, nreps: int, B: int, alpha: float, rng) -> float:
    successes = 0
    for _ in range(B):
        sim = [rng.choice(g, size=nreps, replace=True) for g in groups]
        if jt_test(sim, warn=False) < alpha:
            successes += 1
    return successes / B


def wilson_ci(p: float, n: int, z: float = 1.96):
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def save_plot(labels, candidates, powers, n_pilot, recommended_nreps,
              target_power, alpha, out_dir):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        ns = sorted(powers.keys())
        ps = [powers[n] for n in ns]

        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(ns, ps, "o-", color="steelblue", linewidth=2, markersize=4,
                label="Estimated power")
        ax.axhline(target_power, color="red", linestyle="--", linewidth=1.5,
                   label=f"Target power = {target_power}")
        ax.axvline(recommended_nreps, color="orange", linestyle="--", linewidth=1.5,
                   label=f"Recommended NREPS = {recommended_nreps}")
        if n_pilot in powers:
            ax.plot(n_pilot, powers[n_pilot], "s", color="green", markersize=9,
                    zorder=5, label=f"Pilot n={n_pilot}  (power={powers[n_pilot]:.3f})")

        ax.set_xlabel("NREPS")
        ax.set_ylabel("Estimated Power")
        ax.set_title(
            f"Power Curve - JT Test  (alpha={alpha})\n"
            f"{' < '.join(labels)}"
        )
        ax.legend(fontsize=9)
        ax.set_ylim(0, 1.05)
        ax.set_xlim(min(ns) - 0.5, max(ns) + 0.5)
        ax.grid(True, alpha=0.3)

        out_path = Path(out_dir) / "power_curve.png"
        fig.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"\n  Power curve 저장됨: {out_path}")
    except ImportError:
        print("\n  WARNING: matplotlib 미설치 - 플롯 생략")
    except Exception as e:
        print(f"\n  WARNING: 플롯 저장 실패: {e}")


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--alpha", type=float, default=0.05)
    parser.add_argument("--target-power", type=float, default=0.80)
    parser.add_argument("--B", type=int, default=1000)
    parser.add_argument("--out-dir", type=str, default=".")
    opts, pos_args = parser.parse_known_args()

    if len(pos_args) < 2:
        print(__doc__)
        sys.exit(1)

    labels, groups = [], []
    for arg in pos_args:
        label, medians = parse_arg(arg)
        labels.append(label)
        groups.append(medians)

    n_pilot = min(len(g) for g in groups)
    tau = kendall_tau(groups)

    print("\n=== Power Analysis for JT Test (Bootstrap) ===\n")
    print(f"Groups (ascending order): {' < '.join(labels)}")
    print(f"Pilot n per group       : {n_pilot}")
    print(f"Observed Kendall's tau  : {tau:.4f}  ({tau_label(tau)})")

    if tau < 0.10:
        print(f"\n  WARNING: tau={tau:.4f} (negligible) - 조건 간 차이가 매우 작습니다.")
        print(f"    입력 파일이 올바른지 확인하세요.")
    elif tau < 0.30:
        print(f"\n  WARNING: tau={tau:.4f} (small) - 효과 크기가 작아 큰 NREPS가 필요할 수 있습니다.")

    print(f"\nSettings: alpha={opts.alpha}, target power={opts.target_power}, B={opts.B}\n")

    rng = np.random.default_rng(42)

    candidates = sorted(set(list(range(3, 16)) + [20, 25, 30, 40, 50] + [n_pilot]))

    print(f"{'NREPS':>8} {'Power':>10} {'CI lower':>10} {'CI upper':>10}")
    print("-" * 44)

    powers = {}
    recommended_nreps = None

    for n in candidates:
        p = bootstrap_power(groups, n, opts.B, opts.alpha, rng)
        ci_lo, ci_hi = wilson_ci(p, opts.B)
        powers[n] = p

        marker = ""
        if p >= opts.target_power and recommended_nreps is None:
            recommended_nreps = n
            marker = " <- 권장"
        pilot_marker = " (pilot)" if n == n_pilot else ""
        print(f"{n:>8} {p:>10.3f} {ci_lo:>10.3f} {ci_hi:>10.3f}{marker}{pilot_marker}")

    if recommended_nreps is None:
        recommended_nreps = candidates[-1]
        print(
            f"\n  WARNING: NREPS={candidates[-1]}에서도 "
            f"power={powers[candidates[-1]]:.3f} < {opts.target_power}"
        )
        print(f"    최대 후보 NREPS={candidates[-1]}을 사용합니다. 입력 조건을 확인하세요.")

    print(f"\n  권장 NREPS : {recommended_nreps}")
    print(f"  Pilot power: {powers[n_pilot]:.3f}  (n={n_pilot})")

    save_plot(labels, candidates, powers, n_pilot, recommended_nreps,
              opts.target_power, opts.alpha, opts.out_dir)

    # 쉘 스크립트 파싱용
    print(f"\nRECOMMENDED_NREPS:{recommended_nreps}")
    print(f"OBSERVED_TAU:{tau:.4f}")
    print(f"PILOT_POWER:{powers[n_pilot]:.4f}")


if __name__ == "__main__":
    main()
