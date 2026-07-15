"""
plot_congra_baseline_overview.py — 4-model ConGra baseline overview (#102)

One figure replacing the two per-family baseline PDFs: a horizontal 100%-stacked
bar per model showing solved / partial / failed rate on the no-skill python-tiny
ConGra baseline. Metric = max(edit, winnowing); solved > 0.8, failed <= 0.05,
partial in between (ConGra tiering). Errors skipped; empty -> 0.0 (failed).

Model baseline files match the gap-closure tables (RQ_123) so the numbers are
mutually consistent — in particular Qwen3-32B uses the same-env RTX run
(_rtx.jsonl, the #87 swap), NOT _32b.jsonl.

Outputs (docs/figures/baseline_diagrams/):
  - congra_baseline_overview.pdf   (for LaTeX)
  - congra_baseline_overview.png   (for the results .md)

Run from repo root:
    python scripts/plot_congra_baseline_overview.py
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

T_SOLVED = 0.8
T_FAIL   = 0.05

# top-to-bottom order; grouped by family. (label, jsonl)
MODELS = [
    ("Apertus-8B",  "pilot_results_apertus_baseline_python_tiny.jsonl"),
    ("Apertus-70B", "apertus-70b_baseline_python_tiny.jsonl"),
    ("Qwen3-8B",    "pilot_results_qwen3_baseline_python_tiny.jsonl"),
    ("Qwen3-32B",   "pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl"),
]

# outcome (ordinal, direct-labelled) — CVD-safe blue / neutral grey / red
C_SOLVED  = "#4575b4"
C_PARTIAL = "#bdbdbd"
C_FAILED  = "#d6604d"


def tiers(jsonl):
    """Return (solved%, partial%, failed%) over non-error no-skill cases."""
    s = p = f = 0
    with open(os.path.join(RESULTS_DIR, jsonl)) as fh:
        for line in fh:
            r = json.loads(line)
            if r.get("condition") != "no-skill" or r.get("error") is not None:
                continue
            m = r["metrics"]
            if m.get("empty"):
                score = 0.0
            else:
                e, w = m.get("edit"), m.get("winnowing")
                if e is None or w is None:
                    continue
                score = max(e, w)
            if score > T_SOLVED:
                s += 1
            elif score <= T_FAIL:
                f += 1
            else:
                p += 1
    n = s + p + f
    return (100.0 * s / n, 100.0 * p / n, 100.0 * f / n, n)


def main():
    labels, solved, partial, failed = [], [], [], []
    print(f"{'model':13} {'solved':>7} {'partial':>8} {'failed':>7} {'n':>6}")
    for label, jsonl in MODELS:
        sv, pt, fl, n = tiers(jsonl)
        labels.append(label); solved.append(sv); partial.append(pt); failed.append(fl)
        print(f"{label:13} {sv:6.1f}% {pt:7.1f}% {fl:6.1f}% {n:6d}")

    # y positions with a gap between the two families
    y = [3.4, 2.4, 1.0, 0.0]
    fig, ax = plt.subplots(figsize=(9, 3.6))
    h = 0.72

    seg = [(solved, C_SOLVED, "Solved (>0.8)"),
           (partial, C_PARTIAL, "Partial"),
           (failed, C_FAILED, "Failed (≤0.05)")]
    left = np.zeros(len(labels))
    for vals, color, _ in seg:
        ax.barh(y, vals, height=h, left=left, color=color,
                edgecolor="white", linewidth=1.2, zorder=3)
        for yi, v, l in zip(y, vals, left):
            if v >= 4:  # only label segments wide enough to read
                ax.text(l + v / 2, yi, f"{v:.1f}", ha="center", va="center",
                        fontsize=8.5, color="white" if color != C_PARTIAL else "#333333")
        left += np.array(vals)

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=10)
    ax.set_xlim(0, 100)
    ax.set_xlabel("Share of cases (%)")
    ax.set_title("ConGra no-skill baseline: solved / partial / failed "
                 "(python-tiny, max(edit, winnowing))", fontsize=11)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color="#ececec", linewidth=0.8, zorder=0)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(left=False)

    handles = [Patch(facecolor=c, label=l) for _, c, l in seg]
    ax.legend(handles=handles, ncol=3, frameon=False,
              loc="lower center", bbox_to_anchor=(0.5, -0.32))

    fig.tight_layout()
    os.makedirs(FIG_DIR, exist_ok=True)
    for ext in ("pdf", "png"):
        out = os.path.join(FIG_DIR, f"congra_baseline_overview.{ext}")
        fig.savefig(out, dpi=150, bbox_inches="tight")
        print(f"wrote {out}")


if __name__ == "__main__":
    main()
