"""
plot_rq1_baseline_vs_skill_violin_large.py — RQ1 baseline-vs-skill split violins, large pair (#86)

Large-pair analog of plot_rq1_baseline_vs_skill_violin.py (8B, #68). For each
skill version (v1, v2, v2.1) renders one figure with two stacked subplots
(Qwen3-32B top, Apertus-70B bottom). Each subplot is a per-bucket split violin:
LEFT half = no-skill baseline, RIGHT half = skill-vX-sys. Metric:
max(edit, winnowing). Rendering/tiering identical to the 8B script.

Supersedes the single-subplot plot_rq1_baseline_vs_skill_violin_32b.py (#82),
now that the Apertus-70B half exists (#83). Filenames are not uniform across the
large pair (32B sys-only files have ad-hoc names), so paths are given explicitly
per (model, version) rather than via a template.

Outputs:
  - docs/figures/rq1_large_baseline_vs_v1_sys_max.png
  - docs/figures/rq1_large_baseline_vs_v2_sys_max.png
  - docs/figures/rq1_large_baseline_vs_v2.1_sys_max.png
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

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

# Each model: (label, baseline file, {version -> sys-only skill file}, colour).
MODELS = [
    ("Apertus-70B",
     "apertus-70b_baseline_python_tiny.jsonl",
     {"1":   "apertus-70b_v1_python_tiny.jsonl",
      "2":   "apertus-70b_v2_python_tiny.jsonl",
      "2.1": "apertus-70b_v2.1_python_tiny.jsonl"},
     "#d6604d"),
    ("Qwen3-32B",
     "pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl",
     {"1":   "qwen3-32b_v1_sysonly_clean.jsonl",
      "2":   "qwen3-32b_v2_python_tiny_sysonly_RAW.jsonl",
      "2.1": "qwen3-32b_v2.1_python_tiny_sysonly_RAW.jsonl"},
     "#4575b4"),
]

BASELINE_COLOR = "#888888"

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


def plot_rq1(version: str):
    positions = list(range(len(BUCKETS)))
    fig, axes = plt.subplots(2, 1, figsize=(12, 11), sharex=True)

    for ax, (model, baseline_fname, skill_fnames, model_color) in zip(axes, MODELS):
        baseline = load_max_scores(os.path.join(RESULTS_DIR, baseline_fname))
        skill    = load_max_scores(
            os.path.join(RESULTS_DIR, skill_fnames[version]),
            condition_filter=f"skill-v{version}-sys",
        )

        data_left  = [baseline[b] for b in BUCKETS]
        data_right = [skill[b]    for b in BUCKETS]

        render_split(ax, positions, data_left,  "left",  BASELINE_COLOR)
        render_split(ax, positions, data_right, "right", model_color)
        annotate_halves(ax, positions, data_left, data_right, BASELINE_COLOR, model_color)

        ax.axhline(T_SOLVED, color="#1a9850", linestyle=":", linewidth=0.8, alpha=0.5)
        ax.axhline(T_FAIL,   color="#b2182b", linestyle=":", linewidth=0.8, alpha=0.5)
        ax.set_ylim(-0.17, 1.18)
        ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
        ax.set_ylabel(f"{model}\nmax(edit, winnowing)", fontsize=10)

        # Legend centred above each panel, i.e. under the suptitle for the top one (#112).
        # Per-panel rather than one figure-level legend: the right-half colour differs by
        # model, so a shared legend could not be colour-correct for both. Anchored above the
        # axes because the solved-% labels sit inside them at y=1.04 (ylim reaches 1.18).
        legend_handles = [
            Patch(facecolor=BASELINE_COLOR, alpha=0.7, label="baseline (no-skill, left)"),
            Patch(facecolor=model_color,    alpha=0.7, label=f"skill-v{version}-sys (right)"),
        ]
        ax.legend(handles=legend_handles, loc="lower center",
                  bbox_to_anchor=(0.5, 1.0), ncol=2, columnspacing=2.0,
                  fontsize=8, frameon=False)

        for spine in ("top", "right"):
            ax.spines[spine].set_visible(False)

    axes[1].set_xticks(positions)
    axes[1].set_xticklabels(BUCKETS, rotation=30, fontsize=9, ha="right")

    fig.suptitle(
        f"RQ1 (large pair): does skill-v{version}-sys help vs no-skill, per model?  "
        f"max(edit, winnowing), python-tiny\n"
        f"left half = baseline;  right half = skill-v{version}-sys;  "
        f"solved % above (>{T_SOLVED});  failed % below (≤{T_FAIL})",
        fontsize=11, y=1.0,
    )

    plt.tight_layout(rect=[0, 0, 1, 0.99])  # room for the suptitle above the top legend
    out_path = os.path.join(FIG_DIR, f"rq1_large_baseline_vs_v{version}_sys_max.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    for version in ["1", "2", "2.1"]:
        plot_rq1(version)


if __name__ == "__main__":
    main()
