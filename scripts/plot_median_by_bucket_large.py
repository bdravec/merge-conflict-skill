"""
plot_median_by_bucket_large.py — per-bucket median max-score, large pair (#89)

One grouped-bar figure per large-pair model. For each of the 7 python-tiny
buckets, four bars: the no-skill baseline (green) plus skill-v1/v2/v2.1-sys.
Bar height = median of max(edit, winnowing) over the bucket's cases. Median
value printed above each bar; per-bucket n printed below the group.

Both models use their RTX-box no-skill baseline (#87 for Qwen3-32B; Apertus-70B
was generated entirely on the RTX box, #83 — it has no other baseline). Data
wiring mirrors plot_rq1_baseline_vs_skill_violin_large.py.

Outputs:
  - docs/figures/median_by_bucket_qwen_max.png      (Qwen3-32B)
  - docs/figures/median_by_bucket_apertus_max.png   (Apertus-70B)
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

VERSIONS = ["1", "2", "2.1"]

# (label, output stem, baseline file, {version -> sys-only skill file}).
MODELS = [
    ("Qwen3-32B", "qwen",
     "pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl",     # RTX, #87
     {"1":   "qwen3-32b_v1_sysonly_clean.jsonl",
      "2":   "qwen3-32b_v2_python_tiny_sysonly_RAW.jsonl",
      "2.1": "qwen3-32b_v2.1_python_tiny_sysonly_RAW.jsonl"}),
    ("Apertus-70B", "apertus",
     "apertus-70b_baseline_python_tiny.jsonl",                     # RTX-only, #83
     {"1":   "apertus-70b_v1_python_tiny.jsonl",
      "2":   "apertus-70b_v2_python_tiny.jsonl",
      "2.1": "apertus-70b_v2.1_python_tiny.jsonl"}),
]

BASELINE_COLOR = "#1a9850"                       # green
SKILL_COLORS   = {"1": "#c6dbef", "2": "#6baed6", "2.1": "#2171b5"}  # light→dark blue

T_SOLVED = 0.8
T_FAIL   = 0.05


def load_max_scores(jsonl_path, condition_filter=None):
    out = {b: [] for b in BUCKETS}
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if condition_filter is not None and r.get("condition") != condition_filter:
                continue
            if r.get("error") is not None:
                continue
            bucket = r.get("bucket", "")
            if bucket.endswith("__resume"):
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


def plot_model(label, stem, baseline_fname, skill_fnames):
    # columns: baseline + each version
    series = [("baseline", BASELINE_COLOR,
               load_max_scores(os.path.join(RESULTS_DIR, baseline_fname)))]
    for v in VERSIONS:
        series.append((f"v{v}-sys", SKILL_COLORS[v],
                       load_max_scores(os.path.join(RESULTS_DIR, skill_fnames[v]),
                                       condition_filter=f"skill-v{v}-sys")))

    n_series = len(series)
    x = np.arange(len(BUCKETS))
    width = 0.8 / n_series

    fig, ax = plt.subplots(figsize=(13, 6))

    for i, (name, color, data) in enumerate(series):
        meds = [float(np.median(data[b])) if data[b] else np.nan for b in BUCKETS]
        offset = (i - (n_series - 1) / 2) * width
        bars = ax.bar(x + offset, meds, width, label=name, color=color,
                      edgecolor="white", linewidth=0.5)
        for bx, m in zip(x + offset, meds):
            if not np.isnan(m):
                ax.text(bx, m + 0.012, f"{m:.2f}", ha="center", va="bottom",
                        fontsize=6.5, rotation=90, color="#333")

    # per-bucket n (baseline n; equal across cells on the common slice)
    base_data = series[0][2]
    for bx, b in zip(x, BUCKETS):
        ax.text(bx, -0.055, f"n={len(base_data[b])}", ha="center", va="top",
                fontsize=7, color="#777")

    ax.axhline(T_SOLVED, color="#1a9850", linestyle=":", linewidth=0.9, alpha=0.6)
    ax.axhline(T_FAIL,   color="#b2182b", linestyle=":", linewidth=0.9, alpha=0.6)
    ax.set_ylim(0, 1.08)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("median max(edit, winnowing)", fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(BUCKETS, rotation=20, ha="right", fontsize=10)
    ax.set_title(
        f"{label}: per-bucket median resolution quality, baseline vs skill\n"
        f"max(edit, winnowing), python-tiny  (baseline = RTX no-skill)",
        fontsize=12,
    )

    handles = [Patch(facecolor=c, label=n) for n, c, _ in series]
    handles += [
        plt.Line2D([0], [0], color="#1a9850", linestyle=":", label=f"solved thr ({T_SOLVED})"),
        plt.Line2D([0], [0], color="#b2182b", linestyle=":", label=f"failed thr ({T_FAIL})"),
    ]
    ax.legend(handles=handles, loc="upper left", fontsize=9, ncol=1, frameon=False)

    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    plt.tight_layout()
    out_path = os.path.join(FIG_DIR, f"median_by_bucket_{stem}_max.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


def main():
    for label, stem, baseline_fname, skill_fnames in MODELS:
        plot_model(label, stem, baseline_fname, skill_fnames)


if __name__ == "__main__":
    main()
