"""
plot_baseline_violin_split.py — Qwen3 (left half) vs Apertus (right half) split violins (#67)

Sibling to plot_baseline_violin.py. The original puts the two models side-by-side
(14 violins total, 7 per model, with a gap) so per-bucket cross-model comparison
requires the reader to cross a gap. This script renders one half-violin per model
at the same x per bucket: Qwen3-8B occupies the left half, Apertus-8B the right.
Per-bucket distribution shapes can be compared without occlusion.

Outputs:
  - baseline_violin_split_edit.png
  - baseline_violin_split_winnowing.png
  - baseline_violin_split_max.png

Tiering, empty-handling, and score keys are identical to plot_baseline_violin.py.
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
FIG_DIR     = os.path.join(os.path.dirname(__file__), "..", "docs", "figures")

PILOTS = [
    ("Qwen3-8B",   "pilot_results_qwen3_baseline_python_tiny.jsonl",   "#4575b4", "left"),
    ("Apertus-8B", "pilot_results_apertus_baseline_python_tiny.jsonl", "#d6604d", "right"),
]

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

T_SOLVED = 0.8
T_FAIL   = 0.05


def scores_per_bucket(jsonl_path: str, key: str) -> dict[str, list[float]]:
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


def plot_split(key: str, title_metric: str, out_path: str):
    positions = list(range(len(BUCKETS)))

    per_model_data, per_model_solved, per_model_failed, per_model_n = [], [], [], []
    for _model, fname, _color, _side in PILOTS:
        per_bucket = scores_per_bucket(os.path.join(RESULTS_DIR, fname), key)
        data = [per_bucket[b] for b in BUCKETS]
        per_model_data.append(data)
        per_model_solved.append(
            [sum(1 for s in scores if s >  T_SOLVED) / len(scores) * 100 for scores in data]
        )
        per_model_failed.append(
            [sum(1 for s in scores if s <= T_FAIL  ) / len(scores) * 100 for scores in data]
        )
        per_model_n.append([len(scores) for scores in data])

    fig, ax = plt.subplots(figsize=(12, 6))

    for (model, _fname, color, side), data in zip(PILOTS, per_model_data):
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

    for x in positions:
        ax.text(x - 0.22, 1.04, f"{per_model_solved[0][x]:.1f}%",
                ha="center", va="bottom", fontsize=8,
                color=PILOTS[0][2], fontweight="bold")
        ax.text(x + 0.22, 1.04, f"{per_model_solved[1][x]:.1f}%",
                ha="center", va="bottom", fontsize=8,
                color=PILOTS[1][2], fontweight="bold")
        ax.text(x - 0.22, -0.04, f"{per_model_failed[0][x]:.1f}%",
                ha="center", va="top", fontsize=8,
                color=PILOTS[0][2], fontweight="bold")
        ax.text(x + 0.22, -0.04, f"{per_model_failed[1][x]:.1f}%",
                ha="center", va="top", fontsize=8,
                color=PILOTS[1][2], fontweight="bold")
        n0, n1 = per_model_n[0][x], per_model_n[1][x]
        n_label = f"n={n0}" if n0 == n1 else f"n={n0}/{n1}"
        ax.text(x, -0.11, n_label, ha="center", va="top",
                fontsize=6.5, color="#777")

    ax.axhline(T_SOLVED, color="#1a9850", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axhline(T_FAIL,   color="#b2182b", linestyle=":", linewidth=0.8, alpha=0.5)

    ax.set_xticks(positions)
    ax.set_xticklabels(BUCKETS, rotation=30, fontsize=9, ha="right")
    ax.set_ylim(-0.17, 1.18)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel(title_metric, fontsize=10)
    ax.set_title(
        f"Baseline {title_metric} per bucket — Qwen3-8B (left half) vs Apertus-8B (right half) "
        f"(no-skill, python-tiny)\n"
        f"solved % above (>{T_SOLVED});  failed % below (≤{T_FAIL});  "
        f"colour-coded median line per model",
        fontsize=11, pad=14,
    )

    legend_handles = [
        Patch(facecolor=PILOTS[0][2], alpha=0.7, label=f"{PILOTS[0][0]} (left half)"),
        Patch(facecolor=PILOTS[1][2], alpha=0.7, label=f"{PILOTS[1][0]} (right half)"),
    ]
    ax.legend(handles=legend_handles, loc="upper left",
              bbox_to_anchor=(1.005, 1.0), fontsize=9, frameon=False)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    plot_split("edit", "edit-similarity",
               os.path.join(FIG_DIR, "baseline_violin_split_edit.png"))
    plot_split("winnowing", "winnowing",
               os.path.join(FIG_DIR, "baseline_violin_split_winnowing.png"))
    plot_split("max", "max(edit, winnowing)",
               os.path.join(FIG_DIR, "baseline_violin_split_max.png"))


if __name__ == "__main__":
    main()
