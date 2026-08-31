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

# Palette (#123). TWO ORTHOGONAL ENCODINGS, each doing one job:
#   COLOUR = the MODEL   (same model = same fill in every figure)
#   HATCH  = the SKILL   (solid = no-skill, "///" = + skill)
# So Apertus-8B is #f4a582 whether or not it carries the skill; only the hatch moves.
#
# INK is the fill darkened x0.55, used for the hatch lines, the median bar and the
# number labels. It is not decoration: the light fills score 1.99:1 and 1.97:1 against
# white, so using them as text colour (as these figures did before) put the solved/failed
# percentages far under the 4.5:1 minimum. At x0.55 all four inks clear it (5.8-13.2:1),
# and the darker hatch lines are what make "+ skill" legible where both halves share a fill.
FILL = {
    "Apertus-8B":  "#f4a582",
    "Apertus-70B": "#b2182b",
    "Qwen3-8B":    "#91bfdb",
    "Qwen3-32B":   "#2166ac",
}
INK = {
    "Apertus-8B":  "#865b48",
    "Apertus-70B": "#620d18",
    "Qwen3-8B":    "#506978",
    "Qwen3-32B":   "#12385f",
}
SKILL_HATCH = "///"

# Fills at 0.8 rather than 0.7: the 30% white blend at 0.7 washed out both the fills
# and the hatch lines. The halves never overlap, so alpha only softens, never composites.
FILL_ALPHA = 0.8

T_SOLVED = 0.8
T_FAIL   = 0.05

VERSION = "2.1"

# 12x6, matching every other single-panel violin script (#122). These figures sit
# next to the baseline-scaling pair (plot_baseline_violin_scaling.py) in the thesis;
# at width=\textwidth a taller canvas gave their violins ~17% more vertical room, so
# the baseline pair read as squeezed by comparison. The earlier 12x7 was chosen as
# "the tallest that keeps a stacked pair inside a LaTeX float page" -- a ceiling, not
# a target. 6 fits that float just as well and keeps all four PDFs the same size.
FIGSIZE = (12, 6)

# (family, small label, small file, small model key,
#  large label, large file, large model key, out name)
FIGURES = [
    ("Apertus",
     "Apertus-8B",  "pilot_results_apertus_v2.1_python_tiny.jsonl",  "Apertus-8B",
     "Apertus-70B", "apertus-70b_baseline_python_tiny.jsonl",        "Apertus-70B",
     "skill_vs_scale_violin_apertus_v2.1_vs_70b.png"),
    ("Qwen3",
     "Qwen3-8B",  "pilot_results_qwen3_v2.1_python_tiny.jsonl",                "Qwen3-8B",
     "Qwen3-32B", "pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl",    "Qwen3-32B",
     "skill_vs_scale_violin_qwen3_v2.1_vs_32b.png"),
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


def render_split(ax, positions, data, side, color, ink=None, hatch=None):
    """One half-violin per bucket. `ink` colours the median bar and the hatch
    lines; `hatch` marks the + skill condition."""
    ink = ink or color
    parts = ax.violinplot(data, positions=positions, widths=0.9,
                          showmedians=True, showextrema=False)
    for body, x_center in zip(parts["bodies"], positions):
        verts = body.get_paths()[0].vertices
        if side == "left":
            verts[:, 0] = np.minimum(verts[:, 0], x_center)
        else:
            verts[:, 0] = np.maximum(verts[:, 0], x_center)
        body.set_facecolor(color)
        body.set_alpha(FILL_ALPHA)
        if hatch:
            body.set_hatch(hatch)
            body.set_edgecolor(ink)      # hatch lines take the edge colour
            body.set_linewidth(0.6)
        else:
            body.set_edgecolor(color)
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
        parts["cmedians"].set_color(ink)
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


def plot_family(family, small_label, small_file, small_key,
                large_label, large_file, large_key, out_name):
    positions = list(range(len(BUCKETS)))

    left  = load_max_scores(os.path.join(RESULTS_DIR, small_file),
                            condition_filter=f"skill-v{VERSION}-sys")
    right = load_max_scores(os.path.join(RESULTS_DIR, large_file),
                            condition_filter="no-skill")
    data_left  = [left[b]  for b in BUCKETS]
    data_right = [right[b] for b in BUCKETS]

    fig, ax = plt.subplots(figsize=FIGSIZE)

    # left = the small model WITH the skill -> hatched; right = the large no-skill baseline.
    render_split(ax, positions, data_left,  "left",  FILL[small_key],
                 ink=INK[small_key], hatch=SKILL_HATCH)
    render_split(ax, positions, data_right, "right", FILL[large_key], ink=INK[large_key])
    annotate_halves(ax, positions, data_left, data_right, INK[small_key], INK[large_key])

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
        Patch(facecolor=FILL[small_key], alpha=FILL_ALPHA, hatch=SKILL_HATCH,
              edgecolor=INK[small_key],
              label=f"{small_label} + skill-v{VERSION}-sys (left half)"),
        Patch(facecolor=FILL[large_key], alpha=FILL_ALPHA, edgecolor=FILL[large_key],
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
