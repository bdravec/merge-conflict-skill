"""
plot_skill_vs_scale_violin.py — skill-vs-scale split violins, one figure per family (#114)

Violin counterpart of plot_skill_vs_scale.py, which draws the same comparison as
bar charts. Each figure pits a *skilled small model* against a *larger baseline*
of the same family, as a per-bucket split violin:

  LEFT half  = <8B model> + skill-v2.1-sys   (the small model, with the skill)
  RIGHT half = <large model> no-skill        (the larger baseline)

If the left half sits at or above the right half in a bucket, the small model +
skill has caught the larger baseline there.

Same comparison as Framing B of plot_rq3_gap_closure_violin_large.py, but with
the halves swapped and the two families split into separate figures instead of
stacked panels. That script is left untouched.

Metric = max(edit, winnowing); tiering per #56 (solved > 0.8, failed <= 0.05).
The Qwen3-32B baseline is the RTX re-run, not the UBELIX one.

Outputs (into docs/figures/baseline_diagrams/):
  - skill_vs_scale_violin_apertus_v2.1_vs_70b.png
  - skill_vs_scale_violin_qwen3_v2.1_vs_32b.png

Run from repo root:
    python scripts/plot_skill_vs_scale_violin.py
"""

import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch


RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
FIG_DIR     = os.path.join(os.path.dirname(__file__), "..", "docs", "figures",
                           "baseline_diagrams")

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

QWEN_COLOR     = "#4575b4"
APERTUS_COLOR  = "#d6604d"
BASELINE_COLOR = "#888888"

T_SOLVED = 0.8
T_FAIL   = 0.05

VERSION = "2.1"

# 12x7 rather than the 12x6 used elsewhere: these two are stacked as subfigures in
# one float, and 7 is the tallest that keeps the pair inside a LaTeX float page
# (9.0 cm per panel at a 15.5 cm textwidth, ~20.9 cm for the pair plus captions).
FIGSIZE = (12, 7)

# (family, small label, small file, large label, large file, small colour, out name)
FIGURES = [
    ("Apertus",
     "Apertus-8B",  "pilot_results_apertus_v2.1_python_tiny.jsonl",
     "Apertus-70B", "apertus-70b_baseline_python_tiny.jsonl",
     APERTUS_COLOR, "skill_vs_scale_violin_apertus_v2.1_vs_70b.png"),
    ("Qwen3",
     "Qwen3-8B",  "pilot_results_qwen3_v2.1_python_tiny.jsonl",
     "Qwen3-32B", "pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl",
     QWEN_COLOR, "skill_vs_scale_violin_qwen3_v2.1_vs_32b.png"),
]


def load_max_scores(jsonl_path, condition_filter=None):
    """max(edit, winnowing) per bucket; empties -> 0.0; error rows dropped."""
    out = {b: [] for b in BUCKETS}
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if condition_filter is not None and r.get("condition") != condition_filter:
                continue
            if r.get("error") is not None:
                continue
            bucket = r.get("bucket", "")
            if bucket.endswith("__resume"):          # collapse the resume leak
                bucket = bucket[: -len("__resume")]
            if bucket not in out:
                continue
            m = r["metrics"]
            if m.get("empty"):
                out[bucket].append(0.0)
                continue
            e, w = m.get("edit"), m.get("winnowing")
            if e is None or w is None:
                continue
            out[bucket].append(max(e, w))
    return out


def render_split(ax, positions, data, side, color):
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


def annotate_halves(ax, positions, data_left, data_right, color_left, color_right):
    for x, dl, dr in zip(positions, data_left, data_right):
        nl, nr = len(dl), len(dr)
        sl = sum(1 for s in dl if s >  T_SOLVED) / nl * 100
        sr = sum(1 for s in dr if s >  T_SOLVED) / nr * 100
        fl = sum(1 for s in dl if s <= T_FAIL ) / nl * 100
        fr = sum(1 for s in dr if s <= T_FAIL ) / nr * 100
        ax.text(x - 0.22, 1.04, f"{sl:.1f}%", ha="center", va="bottom",
                fontsize=8, color=color_left,  fontweight="bold")
        ax.text(x + 0.22, 1.04, f"{sr:.1f}%", ha="center", va="bottom",
                fontsize=8, color=color_right, fontweight="bold")
        ax.text(x - 0.22, -0.04, f"{fl:.1f}%", ha="center", va="top",
                fontsize=8, color=color_left,  fontweight="bold")
        ax.text(x + 0.22, -0.04, f"{fr:.1f}%", ha="center", va="top",
                fontsize=8, color=color_right, fontweight="bold")
        n_label = f"n={nl}" if nl == nr else f"n={nl}/{nr}"
        ax.text(x, -0.11, n_label, ha="center", va="top",
                fontsize=6.5, color="#777")


def plot_family(family, small_label, small_file, large_label, large_file,
                small_color, out_name):
    positions = list(range(len(BUCKETS)))

    left  = load_max_scores(os.path.join(RESULTS_DIR, small_file),
                            condition_filter=f"skill-v{VERSION}-sys")
    right = load_max_scores(os.path.join(RESULTS_DIR, large_file),
                            condition_filter="no-skill")
    data_left  = [left[b]  for b in BUCKETS]
    data_right = [right[b] for b in BUCKETS]

    fig, ax = plt.subplots(figsize=FIGSIZE)

    render_split(ax, positions, data_left,  "left",  small_color)
    render_split(ax, positions, data_right, "right", BASELINE_COLOR)
    annotate_halves(ax, positions, data_left, data_right, small_color, BASELINE_COLOR)

    ax.axhline(T_SOLVED, color="#1a9850", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axhline(T_FAIL,   color="#b2182b", linestyle=":", linewidth=0.8, alpha=0.5)

    ax.set_xticks(positions)
    ax.set_xticklabels(BUCKETS, rotation=30, fontsize=9, ha="right")
    ax.set_ylim(-0.17, 1.18)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("max(edit, winnowing)", fontsize=10)
    ax.set_title(
        f"{family}: does {small_label} + skill-v{VERSION}-sys reach the "
        f"{large_label} no-skill baseline?  python-tiny\n"
        f"left half = {small_label} + skill-v{VERSION}-sys;  "
        f"right half = {large_label} no-skill;  "
        f"solved % above (>{T_SOLVED});  failed % below (≤{T_FAIL})",
        fontsize=11, pad=30,
    )

    # Legend centred between the title and the plot area (#112). Anchored above
    # the axes, not inside them: the solved-% labels sit at y=1.04 and ylim
    # reaches 1.18, so an in-axes legend would land on top of them.
    legend_handles = [
        Patch(facecolor=small_color,    alpha=0.7,
              label=f"{small_label} + skill-v{VERSION}-sys (left half)"),
        Patch(facecolor=BASELINE_COLOR, alpha=0.7,
              label=f"{large_label} no-skill (right half)"),
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
    for spec in FIGURES:
        plot_family(*spec)


if __name__ == "__main__":
    main()
