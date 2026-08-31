"""
plot_baseline_violin_scaling.py — per-bucket baseline scaling split violins (#84)

Scaling sibling of plot_baseline_violin_split.py (#67). Instead of Qwen3-vs-Apertus,
each figure compares the SMALL vs LARGE model of one family on the no-skill /
python-tiny baseline, as a per-bucket split violin (LEFT half = small, RIGHT half
= large). Metric = max(edit, winnowing), the score driving the ConGra pass/fail
tiering. Rendering / tiering / empty-handling identical to plot_baseline_violin_split.py.

Outputs (into docs/figures/baseline_diagrams/):
  - baseline_violin_scaling_qwen3_max.png    (Qwen3-8B vs Qwen3-32B)
  - baseline_violin_scaling_apertus_max.png  (Apertus-8B vs Apertus-70B)

Run from repo root:
    python scripts/plot_baseline_violin_scaling.py
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
FIG_DIR     = os.path.join(os.path.dirname(__file__), "..", "docs", "figures", "baseline_diagrams")

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

T_SOLVED = 0.8
T_FAIL   = 0.05

# Each pair: (family_title, out_name, [(label, fname, color, side), ...])
# Same hue per family, light = small / dark = large.
PAIRS = [
    ("Qwen3", "baseline_violin_scaling_qwen3_max.png", [
        ("Qwen3-8B",  "pilot_results_qwen3_baseline_python_tiny.jsonl",        "#91bfdb", "left"),
        ("Qwen3-32B", "pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl", "#2166ac", "right"),
    ]),
    ("Apertus", "baseline_violin_scaling_apertus_max.png", [
        ("Apertus-8B",  "pilot_results_apertus_baseline_python_tiny.jsonl", "#f4a582", "left"),
        ("Apertus-70B", "apertus-70b_baseline_python_tiny.jsonl",           "#b2182b", "right"),
    ]),
]


def max_scores_per_bucket(jsonl_path):
    """max(edit, winnowing) per bucket; no-skill + no-error rows; empties -> 0.0."""
    out = {b: [] for b in BUCKETS}
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("condition") != "no-skill" or r.get("error") is not None:
                continue
            m = r["metrics"]
            if m.get("empty"):
                out[r["bucket"]].append(0.0)
                continue
            e, w = m.get("edit"), m.get("winnowing")
            if e is None or w is None:
                continue
            out[r["bucket"]].append(max(e, w))
    return out


def plot_pair(family, out_name, pilots):
    positions = list(range(len(BUCKETS)))

    per_model_data, per_model_solved, per_model_failed, per_model_n = [], [], [], []
    for _label, fname, _color, _side in pilots:
        per_bucket = max_scores_per_bucket(os.path.join(RESULTS_DIR, fname))
        data = [per_bucket[b] for b in BUCKETS]
        per_model_data.append(data)
        per_model_solved.append(
            [sum(1 for s in scores if s >  T_SOLVED) / len(scores) * 100 for scores in data]
        )
        per_model_failed.append(
            [sum(1 for s in scores if s <= T_FAIL) / len(scores) * 100 for scores in data]
        )
        per_model_n.append([len(scores) for scores in data])

    fig, ax = plt.subplots(figsize=(12, 6))

    for (label, _fname, color, side), data in zip(pilots, per_model_data):
        parts = ax.violinplot(data, positions=positions, widths=0.9,
                              showmedians=True, showextrema=False)
        for body, x_center in zip(parts["bodies"], positions):
            verts = body.get_paths()[0].vertices
            if side == "left":
                verts[:, 0] = np.minimum(verts[:, 0], x_center)
            else:
                verts[:, 0] = np.maximum(verts[:, 0], x_center)
            body.set_facecolor(color)
            body.set_edgecolor(color)
            body.set_alpha(0.7)
            body.set_linewidth(1.0)
        if "cmedians" in parts:
            segs = parts["cmedians"].get_segments()
            clipped = []
            for seg, x_center in zip(segs, positions):
                seg = seg.copy()
                if side == "left":
                    seg[1, 0] = x_center
                else:
                    seg[0, 0] = x_center
                clipped.append(seg)
            parts["cmedians"].set_segments(clipped)
            parts["cmedians"].set_color(color)
            parts["cmedians"].set_linewidth(2.0)

    c_small, c_large = pilots[0][2], pilots[1][2]
    for x in positions:
        ax.text(x - 0.22, 1.04, f"{per_model_solved[0][x]:.1f}%",
                ha="center", va="bottom", fontsize=8, color=c_small, fontweight="bold")
        ax.text(x + 0.22, 1.04, f"{per_model_solved[1][x]:.1f}%",
                ha="center", va="bottom", fontsize=8, color=c_large, fontweight="bold")
        ax.text(x - 0.22, -0.04, f"{per_model_failed[0][x]:.1f}%",
                ha="center", va="top", fontsize=8, color=c_small, fontweight="bold")
        ax.text(x + 0.22, -0.04, f"{per_model_failed[1][x]:.1f}%",
                ha="center", va="top", fontsize=8, color=c_large, fontweight="bold")
        n0, n1 = per_model_n[0][x], per_model_n[1][x]
        n_label = f"n={n0}" if n0 == n1 else f"n={n0}/{n1}"
        ax.text(x, -0.11, n_label, ha="center", va="top", fontsize=6.5, color="#777")

    ax.axhline(T_SOLVED, color="#1a9850", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axhline(T_FAIL,   color="#b2182b", linestyle=":", linewidth=0.8, alpha=0.5)

    ax.set_xticks(positions)
    ax.set_xticklabels(BUCKETS, rotation=30, fontsize=9, ha="right")
    ax.set_ylim(-0.17, 1.18)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("max(edit, winnowing)", fontsize=10)
    ax.set_title(
        f"{family} baseline scaling — {pilots[0][0]} (left half) vs {pilots[1][0]} (right half) "
        f"per bucket (no-skill, python-tiny)\n"
        f"solved % above (>{T_SOLVED});  failed % below (≤{T_FAIL});  "
        f"colour-coded median line per model",
        fontsize=11, pad=30,
    )

    # Legend sits centred between the title and the plot area (#112). It must be anchored
    # ABOVE the axes, not inside them: the solved-% labels are drawn at y=1.04 and ylim
    # runs to 1.18, so an in-axes legend would land on top of them.
    legend_handles = [
        Patch(facecolor=c_small, alpha=0.7, label=f"{pilots[0][0]} (left half)"),
        Patch(facecolor=c_large, alpha=0.7, label=f"{pilots[1][0]} (right half)"),
    ]
    ax.legend(handles=legend_handles, loc="lower center",
              bbox_to_anchor=(0.5, 1.0), ncol=2, columnspacing=2.0,
              fontsize=9, frameon=False)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    os.makedirs(FIG_DIR, exist_ok=True)
    out_path = os.path.join(FIG_DIR, out_name)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    for family, out_name, pilots in PAIRS:
        plot_pair(family, out_name, pilots)


if __name__ == "__main__":
    main()
