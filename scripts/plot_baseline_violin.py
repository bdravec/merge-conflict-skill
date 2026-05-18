"""
plot_baseline_violin.py — per-bucket baseline distribution violins (#56)

Reads the #46 no-skill baseline JSONLs for Qwen3-8B and Apertus-8B on
python-tiny, and emits three violin charts:

  - baseline_violin_edit.png       (per-metric distribution of edit-sim)
  - baseline_violin_winnowing.png  (per-metric distribution of winnowing)
  - baseline_violin_max.png        (max(edit, winnowing) — the score that
                                    drives the ConGra pass/fail tiering)

Tiering follows the ConGra paper convention (Zhang et al. 2024):
  solved = max(edit, winn) > 0.8   (at least one metric exceeds 80%)
  failed = max(edit, winn) ≤ 0.05  (data-cliff anchor; our addition)
  partial = everything else

Empty-resolution rows (metrics.empty=True; pilot.py:229–230 returns
edit=None, winn=None when the model produced no output for a non-empty
ground truth) are folded in as score=0 — they show as a spike at the
bottom of each violin and count as failed.

Run from repo root:
    python scripts/plot_baseline_violin.py
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
    ("Qwen3-8B",   "pilot_results_qwen3_baseline_python_tiny.jsonl",   "#4575b4"),
    ("Apertus-8B", "pilot_results_apertus_baseline_python_tiny.jsonl", "#d6604d"),
]

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

T_SOLVED = 0.8
T_FAIL   = 0.05


def scores_per_bucket(jsonl_path: str, key: str) -> dict[str, list[float]]:
    """
    key ∈ {"edit", "winnowing", "max"}.
    Drops error rows; empty rows are mapped to 0.0 for the requested key.
    """
    out = {b: [] for b in BUCKETS}
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("error") is not None:
                continue
            m = r["metrics"]
            if m.get("empty"):
                out[r["bucket"]].append(0.0)
                continue
            e, w = m.get("edit"), m.get("winnowing")
            if e is None or w is None:
                continue
            if key == "edit":
                out[r["bucket"]].append(e)
            elif key == "winnowing":
                out[r["bucket"]].append(w)
            elif key == "max":
                out[r["bucket"]].append(max(e, w))
            else:
                raise ValueError(key)
    return out


def plot_metric(key: str, title_metric: str, out_path: str):
    n_per_model = len(BUCKETS)
    GAP = 1.5
    positions, data_groups, colors = [], [], []
    n_per_violin, pct_solved, pct_failed = [], [], []
    bucket_labels = []

    for i, (model, fname, color) in enumerate(PILOTS):
        offset = i * (n_per_model + GAP)
        per_bucket = scores_per_bucket(os.path.join(RESULTS_DIR, fname), key)
        for j, b in enumerate(BUCKETS):
            scores = per_bucket[b]
            positions.append(offset + j)
            data_groups.append(scores)
            colors.append(color)
            n = len(scores)
            n_per_violin.append(n)
            pct_solved.append(sum(1 for s in scores if s > T_SOLVED) / n * 100)
            pct_failed.append(sum(1 for s in scores if s <= T_FAIL) / n * 100)
            bucket_labels.append(b)

    fig, ax = plt.subplots(figsize=(14, 6))
    parts = ax.violinplot(data_groups, positions=positions,
                          widths=0.9, showmedians=True, showextrema=False)

    for i, body in enumerate(parts["bodies"]):
        body.set_facecolor(colors[i])
        body.set_edgecolor("#333")
        body.set_alpha(0.55)
        body.set_linewidth(0.7)

    if "cmedians" in parts:
        parts["cmedians"].set_color("#222")
        parts["cmedians"].set_linewidth(1.4)

    for x, n, ps, pf in zip(positions, n_per_violin, pct_solved, pct_failed):
        ax.text(x, 1.04, f"{ps:.1f}%", ha="center", va="bottom",
                fontsize=7.5, color="#1a9850", fontweight="bold")
        ax.text(x, -0.04, f"{pf:.1f}%", ha="center", va="top",
                fontsize=7.5, color="#b2182b", fontweight="bold")
        ax.text(x, -0.10, f"n={n}", ha="center", va="top",
                fontsize=6.5, color="#777")

    ax.axhline(T_SOLVED, color="#1a9850", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axhline(T_FAIL,   color="#b2182b", linestyle=":", linewidth=0.8, alpha=0.5)

    ax.set_xticks(positions)
    ax.set_xticklabels(bucket_labels, rotation=30, fontsize=9, ha="right")

    qwen_center = np.mean(positions[:n_per_model])
    apertus_center = np.mean(positions[n_per_model:])
    ax.text(qwen_center, 1.18, PILOTS[0][0],
            ha="center", va="bottom", fontsize=12, fontweight="bold",
            color=PILOTS[0][2])
    ax.text(apertus_center, 1.18, PILOTS[1][0],
            ha="center", va="bottom", fontsize=12, fontweight="bold",
            color=PILOTS[1][2])

    ax.set_ylim(-0.15, 1.22)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel(title_metric, fontsize=10)
    ax.set_title(
        f"Baseline {title_metric} distribution per bucket — no-skill, python-tiny\n"
        f"green % = solved ({title_metric} > {T_SOLVED});  "
        f"red % = failed ({title_metric} ≤ {T_FAIL});  black bar = median",
        fontsize=11, pad=14,
    )

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    plot_metric("edit", "edit-similarity",
                os.path.join(FIG_DIR, "baseline_violin_edit.png"))
    plot_metric("winnowing", "winnowing",
                os.path.join(FIG_DIR, "baseline_violin_winnowing.png"))
    plot_metric("max", "max(edit, winnowing)",
                os.path.join(FIG_DIR, "baseline_violin_max.png"))


if __name__ == "__main__":
    main()
