"""
plot_solved_gap.py — per-bucket %solved gap between Qwen3-8B and Apertus-8B (#56)

Reads the #46 no-skill baseline JSONLs, computes the per-bucket %solved
rate for each model under the ConGra paper convention (Zhang et al. 2024:
solved = max(edit, winnowing) > 0.8; empty rows folded in as score=0),
and emits a diverging bar chart showing the gap Qwen3 − Apertus per bucket.

Run from repo root:
    python scripts/plot_solved_gap.py
"""

import json
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
FIG_DIR     = os.path.join(os.path.dirname(__file__), "..", "docs", "figures")

PILOTS = [
    ("Qwen3-8B",   "pilot_results_qwen3_baseline_python_tiny.jsonl"),
    ("Apertus-8B", "pilot_results_apertus_baseline_python_tiny.jsonl"),
]

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

T_SOLVED = 0.8


def pct_solved_per_bucket(jsonl_path: str) -> dict[str, float]:
    counts = defaultdict(lambda: {"solved": 0, "n": 0})
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("error") is not None:
                continue
            m = r["metrics"]
            if m.get("empty"):
                counts[r["bucket"]]["n"] += 1
                continue
            e, w = m.get("edit"), m.get("winnowing")
            if e is None or w is None:
                continue
            counts[r["bucket"]]["n"] += 1
            if max(e, w) > T_SOLVED:
                counts[r["bucket"]]["solved"] += 1
    return {b: counts[b]["solved"] / counts[b]["n"] * 100 for b in BUCKETS}


def main():
    qwen = pct_solved_per_bucket(os.path.join(RESULTS_DIR, PILOTS[0][1]))
    aper = pct_solved_per_bucket(os.path.join(RESULTS_DIR, PILOTS[1][1]))
    gaps = [qwen[b] - aper[b] for b in BUCKETS]

    fig, ax = plt.subplots(figsize=(11, 4.5))
    x = np.arange(len(BUCKETS))
    colors = ["#4575b4" if g >= 0 else "#d6604d" for g in gaps]

    bars = ax.bar(x, gaps, color=colors, edgecolor="white",
                  linewidth=0.6, width=0.7)

    for rect, g, b in zip(bars, gaps, BUCKETS):
        q, a = qwen[b], aper[b]
        if g >= 0:
            ax.text(rect.get_x() + rect.get_width() / 2,
                    g + 0.5, f"+{g:.1f}",
                    ha="center", va="bottom", fontsize=9, fontweight="bold",
                    color="#2c5694")
        else:
            ax.text(rect.get_x() + rect.get_width() / 2,
                    g - 0.5, f"{g:.1f}",
                    ha="center", va="top", fontsize=9, fontweight="bold",
                    color="#94352c")
        ax.text(rect.get_x() + rect.get_width() / 2,
                -2.5,
                f"Q:{q:.1f}%\nA:{a:.1f}%",
                ha="center", va="top", fontsize=7, color="#555")

    ax.axhline(0, color="#333", linewidth=0.8)

    ax.set_xticks(x)
    ax.set_xticklabels(BUCKETS, rotation=20, fontsize=9, ha="right")
    ax.set_ylabel("Qwen3-8B  −  Apertus-8B   (pp)", fontsize=10)
    ax.set_title(
        "Per-bucket %solved gap (Qwen3-8B minus Apertus-8B), no-skill, python-tiny\n"
        f"solved = max(edit, winn) > {T_SOLVED} (Zhang et al. 2024)",
        fontsize=11, pad=12,
    )

    ymin = min(gaps) - 6
    ymax = max(gaps) + 4
    ax.set_ylim(ymin, ymax)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, "baseline_solved_gap.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")

    print()
    print(f"  {'bucket':<18} {'Qwen3':>6} {'Apertus':>8} {'gap':>6}")
    for b, g in zip(BUCKETS, gaps):
        print(f"  {b:<18} {qwen[b]:>5.1f}% {aper[b]:>7.1f}% {g:>+5.1f}")


if __name__ == "__main__":
    main()
