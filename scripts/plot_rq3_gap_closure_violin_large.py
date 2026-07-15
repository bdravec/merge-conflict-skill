"""
plot_rq3_gap_closure_violin_large.py — RQ3 gap-closure split violins, large pair (#86)

RQ3 asks whether a small/weak model + skill closes the gap to a stronger model
without skill. This renders TWO complementary framings of that question at the
large-pair scale, for each skill version (v1, v2, v2.1). Metric:
max(edit, winnowing); rendering/tiering identical to the 8B script (#69).

Framing A — WITHIN-SCALE (direct analog of the 8B RQ3 chart):
    LEFT  = Qwen3-32B no-skill        (stronger large baseline)
    RIGHT = Apertus-70B skill-vX-sys  (weaker family, large, + skill)
  Single per-bucket split-violin panel. "Does the weaker large model + skill
  catch the stronger large baseline?"
  -> docs/RQ_123/rq3_large_gap_closure_v{ver}_max.png

Framing B — SCALING-AXIS (the literal RQ3 wording, family held fixed so only
  scale + skill vary):
    LEFT  = large no-skill            (Qwen3-32B / Apertus-70B baseline)
    RIGHT = small + skill-vX-sys      (Qwen3-8B / Apertus-8B skill)
  Two stacked panels (Qwen family top, Apertus family bottom). "Does the small
  model + skill close the gap to the large model with no skill?"
  -> docs/RQ_123/rq3_scaling_gap_closure_v{ver}_max.png

Outputs (6 figures total):
  - docs/RQ_123/rq3_large_gap_closure_v{1,2,2.1}_max.png
  - docs/RQ_123/rq3_scaling_gap_closure_v{1,2,2.1}_max.png
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
BASELINE_COLOR = "#888888"

T_SOLVED = 0.8
T_FAIL   = 0.05

# --- file map -------------------------------------------------------------
QWEN32_BASELINE   = "pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl"
APERTUS70_BASELINE = "apertus-70b_baseline_python_tiny.jsonl"

APERTUS70_SKILL = {  # version -> sys-only file (uniform naming)
    "1":   "apertus-70b_v1_python_tiny.jsonl",
    "2":   "apertus-70b_v2_python_tiny.jsonl",
    "2.1": "apertus-70b_v2.1_python_tiny.jsonl",
}
QWEN8_SKILL_TPL    = "pilot_results_qwen3_v{ver}_python_tiny.jsonl"
APERTUS8_SKILL_TPL = "pilot_results_apertus_v{ver}_python_tiny.jsonl"


def load_max_scores(jsonl_path: str, condition_filter: str | None = None) -> dict[str, list[float]]:
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


def _style_axis(ax):
    ax.axhline(T_SOLVED, color="#1a9850", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axhline(T_FAIL,   color="#b2182b", linestyle=":", linewidth=0.8, alpha=0.5)
    ax.set_ylim(-0.17, 1.18)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)


# --- Framing A: within-scale ---------------------------------------------

def plot_within_scale(version: str):
    positions = list(range(len(BUCKETS)))
    left  = load_max_scores(os.path.join(RESULTS_DIR, QWEN32_BASELINE))
    right = load_max_scores(
        os.path.join(RESULTS_DIR, APERTUS70_SKILL[version]),
        condition_filter=f"skill-v{version}-sys",
    )
    data_left  = [left[b]  for b in BUCKETS]
    data_right = [right[b] for b in BUCKETS]

    fig, ax = plt.subplots(figsize=(12, 6))
    render_split(ax, positions, data_left,  "left",  QWEN_COLOR)
    render_split(ax, positions, data_right, "right", APERTUS_COLOR)
    annotate_halves(ax, positions, data_left, data_right, QWEN_COLOR, APERTUS_COLOR)
    _style_axis(ax)

    ax.set_xticks(positions)
    ax.set_xticklabels(BUCKETS, rotation=30, fontsize=9, ha="right")
    ax.set_ylabel("max(edit, winnowing)", fontsize=10)
    ax.set_title(
        f"RQ3 within-scale: does Apertus-70B + skill-v{version}-sys catch "
        f"Qwen3-32B no-skill?  python-tiny\n"
        f"left half = Qwen3-32B no-skill;  right half = Apertus-70B skill-v{version}-sys;  "
        f"solved % above (>{T_SOLVED});  failed % below (≤{T_FAIL})",
        fontsize=11, pad=14,
    )
    legend_handles = [
        Patch(facecolor=QWEN_COLOR,    alpha=0.7, label="Qwen3-32B no-skill (left)"),
        Patch(facecolor=APERTUS_COLOR, alpha=0.7, label=f"Apertus-70B skill-v{version}-sys (right)"),
    ]
    ax.legend(handles=legend_handles, loc="upper left",
              bbox_to_anchor=(1.005, 1.0), fontsize=8, frameon=False)

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, f"rq3_large_gap_closure_v{version}_max.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


# --- Framing B: scaling-axis (family fixed) -------------------------------

def plot_scaling(version: str):
    positions = list(range(len(BUCKETS)))
    # (family label, large baseline file, small skill file, small skill colour)
    families = [
        ("Qwen3", QWEN32_BASELINE,
         QWEN8_SKILL_TPL.format(ver=version), "Qwen3-32B no-skill",
         "Qwen3-8B", QWEN_COLOR),
        ("Apertus", APERTUS70_BASELINE,
         APERTUS8_SKILL_TPL.format(ver=version), "Apertus-70B no-skill",
         "Apertus-8B", APERTUS_COLOR),
    ]
    fig, axes = plt.subplots(2, 1, figsize=(12, 11), sharex=True)

    for ax, (fam, base_f, small_f, base_label, small_label, color) in zip(axes, families):
        left  = load_max_scores(os.path.join(RESULTS_DIR, base_f))
        right = load_max_scores(
            os.path.join(RESULTS_DIR, small_f),
            condition_filter=f"skill-v{version}-sys",
        )
        data_left  = [left[b]  for b in BUCKETS]
        data_right = [right[b] for b in BUCKETS]

        render_split(ax, positions, data_left,  "left",  BASELINE_COLOR)
        render_split(ax, positions, data_right, "right", color)
        annotate_halves(ax, positions, data_left, data_right, BASELINE_COLOR, color)
        _style_axis(ax)
        ax.set_ylabel(f"{fam} family\nmax(edit, winnowing)", fontsize=10)

        legend_handles = [
            Patch(facecolor=BASELINE_COLOR, alpha=0.7, label=f"{base_label} (large, left)"),
            Patch(facecolor=color, alpha=0.7,
                  label=f"{small_label} skill-v{version}-sys (small + skill, right)"),
        ]
        ax.legend(handles=legend_handles, loc="upper left",
                  bbox_to_anchor=(1.005, 1.0), fontsize=8, frameon=False)

    axes[1].set_xticks(positions)
    axes[1].set_xticklabels(BUCKETS, rotation=30, fontsize=9, ha="right")
    fig.suptitle(
        f"RQ3 scaling-axis: does small + skill-v{version}-sys close the gap to "
        f"the large model with no skill?  python-tiny\n"
        f"left half = large no-skill;  right half = small + skill-v{version}-sys;  "
        f"solved % above (>{T_SOLVED});  failed % below (≤{T_FAIL})",
        fontsize=11, y=0.995,
    )

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, f"rq3_scaling_gap_closure_v{version}_max.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    for version in ["1", "2", "2.1"]:
        plot_within_scale(version)
        plot_scaling(version)


if __name__ == "__main__":
    main()
