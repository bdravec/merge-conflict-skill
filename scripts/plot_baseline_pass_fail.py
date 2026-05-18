"""
plot_baseline_pass_fail.py — per-bucket baseline pass/fail stacked bars (#56)

Reads the #46 no-skill baseline JSONLs for Qwen3-8B and Apertus-8B on
python-tiny, bins each scorable + empty case into 3 tiers using the
ConGra paper convention (Zhang et al. 2024), and emits one stacked bar
chart for the combined max(edit, winnowing) score that drives tiering.

Tiers:
  solved  = max(edit, winn) > 0.8   (paper convention; at least one
                                    of the two computed metrics exceeds
                                    80% — note our pipeline does not
                                    compute semantic similarity, so this
                                    is a strict subset of the paper's
                                    3-metric definition)
  failed  = max(edit, winn) <= 0.05 (data-cliff anchor)
  partial = everything else

Empty-resolution rows (metrics.empty=True; pilot.py:229–230) are folded
in as score=0 and count as failed.

Run from repo root:
    python scripts/plot_baseline_pass_fail.py
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
T_FAIL   = 0.05

CATEGORIES = ["failed", "partial", "solved"]

COLORS = {
    "failed":  "#b2182b",
    "partial": "#bfbfbf",
    "solved":  "#1a9850",
}


def tier(score: float) -> str:
    if score > T_SOLVED:
        return "solved"
    if score <= T_FAIL:
        return "failed"
    return "partial"


def counts_per_bucket(jsonl_path: str) -> dict[str, dict[str, int]]:
    out = {b: {c: 0 for c in CATEGORIES} for b in BUCKETS}
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("error") is not None:
                continue
            m = r["metrics"]
            if m.get("empty"):
                out[r["bucket"]][tier(0.0)] += 1
                continue
            e, w = m.get("edit"), m.get("winnowing")
            if e is None or w is None:
                continue
            out[r["bucket"]][tier(max(e, w))] += 1
    return out


def plot_combined(out_path: str):
    bar_specs = []
    for model, fname in PILOTS:
        path = os.path.join(RESULTS_DIR, fname)
        per_bucket = counts_per_bucket(path)
        for b in BUCKETS:
            counts = per_bucket[b]
            n = sum(counts.values())
            bar_specs.append((model, b, counts, n))

    fig, ax = plt.subplots(figsize=(13, 5.5))
    n_bars = len(bar_specs)
    x = np.arange(n_bars, dtype=float)
    GAP = 0.8
    x[len(BUCKETS):] += GAP

    bottoms = np.zeros(n_bars)
    for cat in CATEGORIES:
        heights = np.array([b[2][cat] for b in bar_specs], dtype=float)
        bars = ax.bar(x, heights, bottom=bottoms, width=0.78,
                      color=COLORS[cat], label=cat,
                      edgecolor="white", linewidth=0.6)
        for rect, h, btm in zip(bars, heights, bottoms):
            if h >= 30:
                ax.text(rect.get_x() + rect.get_width() / 2,
                        btm + h / 2, f"{int(h)}",
                        ha="center", va="center",
                        fontsize=8,
                        color="black" if cat == "partial" else "white",
                        fontweight="bold")
        bottoms += heights

    max_total = max(b[3] for b in bar_specs)
    for xi, (_, _, _, n) in zip(x, bar_specs):
        ax.text(xi, n + max_total * 0.015, f"n={n}",
                ha="center", va="bottom", fontsize=7, color="#555")

    xtick_labels = [b for (_, b, _, _) in bar_specs]
    ax.set_xticks(x)
    ax.set_xticklabels(xtick_labels, rotation=30, fontsize=9, ha="right")

    qwen_center = x[:len(BUCKETS)].mean()
    apertus_center = x[len(BUCKETS):].mean()
    ax.text(qwen_center, max_total * 1.12, "Qwen3-8B",
            ha="center", va="bottom", fontsize=12, fontweight="bold")
    ax.text(apertus_center, max_total * 1.12, "Apertus-8B",
            ha="center", va="bottom", fontsize=12, fontweight="bold")

    ax.set_ylim(0, max_total * 1.18)
    ax.set_ylabel("cases", fontsize=10)
    ax.set_title(
        "Baseline pass/fail distribution per bucket — no-skill, python-tiny\n"
        f"solved = max(edit, winn) > {T_SOLVED} (Zhang et al. 2024);  "
        f"failed = max(edit, winn) ≤ {T_FAIL}",
        fontsize=11, pad=14,
    )

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1],
              loc="center left", bbox_to_anchor=(1.01, 0.5),
              frameon=False, fontsize=9)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")

    # Echo counts table
    print()
    print(f"  {'model':<11} {'bucket':<18} {'failed':>7} {'partial':>8} {'solved':>7}  n")
    for (model, b, counts, n) in bar_specs:
        print(f"  {model:<11} {b:<18} "
              f"{counts['failed']:>7} {counts['partial']:>8} {counts['solved']:>7}  {n}")


def main():
    plot_combined(os.path.join(FIG_DIR, "baseline_pass_fail.png"))


if __name__ == "__main__":
    main()
