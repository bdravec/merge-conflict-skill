"""
plot_rq3_gap_closure_violin.py — RQ3 gap-closure split violins (#69)

RQ3 asks whether a small model + skill closes the gap to a stronger model
without skill. The 8B-pair experiment is the proxy: Apertus-8B (weaker) + skill
vs Qwen3-8B (stronger) baseline. For each skill version, render one figure with
per-bucket split-violins where:

  LEFT half  = Qwen3-8B no-skill   (the stronger 8B baseline)
  RIGHT half = Apertus-8B skill-vX-sys  (the weaker 8B + skill)

If the right half sits at or above the left half per bucket, Apertus has caught
Qwen3 baseline — the RQ3 positive signal. v2.1-sys should show this; v1-sys
should show the opposite.

Metric: max(edit, winnowing).

Outputs:
  - docs/RQ_123/rq3_gap_closure_v1_max.png
  - docs/RQ_123/rq3_gap_closure_v2_max.png
  - docs/RQ_123/rq3_gap_closure_v2.1_max.png
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
FIG_DIR     = os.path.join(os.path.dirname(__file__), "..", "docs", "RQ_123")

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

QWEN_COLOR    = "#4575b4"
APERTUS_COLOR = "#d6604d"

QWEN_BASELINE_JSONL    = "pilot_results_qwen3_baseline_python_tiny.jsonl"
APERTUS_SKILL_JSONL_TPL = "pilot_results_apertus_v{ver}_python_tiny.jsonl"

T_SOLVED = 0.8
T_FAIL   = 0.05


def load_max_scores(jsonl_path: str, condition_filter: str | None = None) -> dict[str, list[float]]:
    out = {b: [] for b in BUCKETS}
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if condition_filter is not None and r.get("condition") != condition_filter:
                continue
            if r.get("error") is not None:
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


def render_split(ax, positions, data, side: str, color: str):
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


def annotate_halves(ax, positions, data_left, data_right):
    for x, dl, dr in zip(positions, data_left, data_right):
        nl, nr = len(dl), len(dr)
        sl = sum(1 for s in dl if s >  T_SOLVED) / nl * 100
        sr = sum(1 for s in dr if s >  T_SOLVED) / nr * 100
        fl = sum(1 for s in dl if s <= T_FAIL ) / nl * 100
        fr = sum(1 for s in dr if s <= T_FAIL ) / nr * 100
        ax.text(x - 0.22, 1.04, f"{sl:.1f}%", ha="center", va="bottom",
                fontsize=8, color=QWEN_COLOR,    fontweight="bold")
        ax.text(x + 0.22, 1.04, f"{sr:.1f}%", ha="center", va="bottom",
                fontsize=8, color=APERTUS_COLOR, fontweight="bold")
        ax.text(x - 0.22, -0.04, f"{fl:.1f}%", ha="center", va="top",
                fontsize=8, color=QWEN_COLOR,    fontweight="bold")
        ax.text(x + 0.22, -0.04, f"{fr:.1f}%", ha="center", va="top",
                fontsize=8, color=APERTUS_COLOR, fontweight="bold")
        n_label = f"n={nl}" if nl == nr else f"n={nl}/{nr}"
        ax.text(x, -0.11, n_label, ha="center", va="top",
                fontsize=6.5, color="#777")


def plot_rq3(version: str):
    positions = list(range(len(BUCKETS)))

    qwen_baseline = load_max_scores(os.path.join(RESULTS_DIR, QWEN_BASELINE_JSONL))
    apertus_skill = load_max_scores(
        os.path.join(RESULTS_DIR, APERTUS_SKILL_JSONL_TPL.format(ver=version)),
        condition_filter=f"skill-v{version}-sys",
    )

    data_left  = [qwen_baseline[b] for b in BUCKETS]
    data_right = [apertus_skill[b] for b in BUCKETS]

    fig, ax = plt.subplots(figsize=(12, 6))

    render_split(ax, positions, data_left,  "left",  QWEN_COLOR)
    render_split(ax, positions, data_right, "right", APERTUS_COLOR)
    annotate_halves(ax, positions, data_left, data_right)

    ax.axhline(T_SOLVED, color="#1a9850", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axhline(T_FAIL,   color="#b2182b", linestyle=":", linewidth=0.8, alpha=0.5)

    ax.set_xticks(positions)
    ax.set_xticklabels(BUCKETS, rotation=30, fontsize=9, ha="right")
    ax.set_ylim(-0.17, 1.18)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("max(edit, winnowing)", fontsize=10)
    ax.set_title(
        f"RQ3: does Apertus-8B + skill-v{version}-sys catch Qwen3-8B no-skill?  "
        f"python-tiny\n"
        f"left half = Qwen3-8B no-skill;  right half = Apertus-8B skill-v{version}-sys;  "
        f"solved % above (>{T_SOLVED});  failed % below (≤{T_FAIL})",
        fontsize=11, pad=14,
    )

    legend_handles = [
        Patch(facecolor=QWEN_COLOR,    alpha=0.7, label="Qwen3-8B no-skill (left)"),
        Patch(facecolor=APERTUS_COLOR, alpha=0.7, label=f"Apertus-8B skill-v{version}-sys (right)"),
    ]
    ax.legend(handles=legend_handles, loc="upper left",
              bbox_to_anchor=(1.005, 1.0), fontsize=8, frameon=False)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, f"rq3_gap_closure_v{version}_max.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    for version in ["1", "2", "2.1"]:
        plot_rq3(version)


if __name__ == "__main__":
    main()
