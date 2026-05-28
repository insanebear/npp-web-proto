#!/usr/bin/env python3
"""
여러 rep의 autocorrelation 데이터를 하나의 HTML로 합치기.
변수별 서브플롯에 rep들을 색으로 구분해 겹쳐 그림.

Usage:
  python combine_autocorr.py <output.html> <autocorr-rep1.json> <autocorr-rep2.json> ...

Example:
  python combine_autocorr.py autocorr_combined.html \
    autocorr-pre-sdlc-all-medium-tune1000-draw1000-rep1.json \
    autocorr-pre-sdlc-all-medium-tune1000-draw1000-rep2.json \
    autocorr-pre-sdlc-all-medium-tune1000-draw1000-rep3.json
"""

import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

REP_COLORS = ["steelblue", "tomato", "seagreen", "darkorange", "mediumpurple", "saddlebrown"]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    output_path = Path(sys.argv[1])
    json_paths = sys.argv[2:]

    # 각 rep 데이터 로드
    reps = []
    for path in json_paths:
        raw = json.loads(Path(path).read_text(encoding="utf-8"))
        meta = raw.pop("__meta__", {})
        reps.append({"meta": meta, "ac": raw})

    if not reps:
        print("[ERROR] 로드된 데이터 없음")
        sys.exit(1)

    # 변수 목록 (첫 rep 기준)
    var_names = [k for k in reps[0]["ac"]]
    max_lag = max(rep["meta"].get("max_lag", 50) for rep in reps)
    lags = list(range(max_lag + 1))

    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    import plotly.io as pio

    n_vars = len(var_names)
    fig = make_subplots(
        rows=n_vars,
        cols=1,
        subplot_titles=var_names,
        shared_xaxes=True,
        vertical_spacing=0.04,
    )

    for var_idx, var_name in enumerate(var_names):
        row = var_idx + 1
        for rep_idx, rep in enumerate(reps):
            ac = rep["ac"].get(var_name)
            if ac is None:
                continue
            rep_label = f"rep{rep_idx + 1}"
            color = REP_COLORS[rep_idx % len(REP_COLORS)]
            fig.add_trace(
                go.Scatter(
                    x=lags[: len(ac)],
                    y=ac[: max_lag + 1],
                    mode="lines+markers",
                    name=rep_label,
                    legendgroup=rep_label,
                    showlegend=(var_idx == 0),  # 범례는 첫 서브플롯에만 표시
                    line=dict(color=color, width=1.5),
                    marker=dict(size=4, color=color),
                ),
                row=row,
                col=1,
            )
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.4, row=row, col=1)
        fig.update_yaxes(title_text="autocorr", row=row, col=1)

    fig.update_xaxes(title_text="lag", row=n_vars, col=1)

    draws = reps[0]["meta"].get("draws", "?")
    fig.update_layout(
        height=220 * n_vars,
        title_text=f"Autocorrelation 비교 — {len(reps)} reps  (draws={draws})",
        title_font_size=14,
        legend=dict(orientation="h", x=0, y=1.02, xanchor="left", yanchor="bottom"),
    )

    pio.write_html(fig, str(output_path), include_plotlyjs="cdn")
    print(f"[COMBINE] Autocorr 비교 HTML 저장: {output_path}")


if __name__ == "__main__":
    main()
