"""
plot_family_gap_closure_comparison.py — cross-family skill effect (#100)

Compares the two families' scaling-axis skill effect per bucket (Qwen3 #97 vs
Apertus #98, summary #99). Plots Recovered (pp) = (8B+skill) - 8B, which is in
comparable units across families (unlike Gap or the Closure ratio), so the sign
flip reads directly against a zero baseline: Qwen3 neutral/negative, Apertus
positive in every bucket.

python-tiny, metric = max(edit, winnowing), solved = score > 0.8, skill =
skill-v2.1-sys. Reuses solved_rates() so numbers match the tables exactly.

Output: docs/figures/family_gap_closure_comparison.png
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from build_apertus_gap_closure import solved_rates, BUCKETS

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "figures")

# Family colours — identical to the existing repo figures (colour follows entity).
QWEN_COLOR    = "#4575b4"
APERTUS_COLOR = "#d6604d"

FAMILIES = {
    "Qwen3 (8B→ 32B)": {
        "color": QWEN_COLOR,
        "base":  "pilot_results_qwen3_baseline_python_tiny.jsonl",
        "skill": "pilot_results_qwen3_v2.1_python_tiny.jsonl",
    },
    "Apertus (8B→ 70B)": {
        "color": APERTUS_COLOR,
        "base":  "pilot_results_apertus_baseline_python_tiny.jsonl",
        "skill": "pilot_results_apertus_v2.1_python_tiny.jsonl",
    },
}

ROWS = BUCKETS + ["Aggregate"]
XLABELS = BUCKETS + ["Aggregate"]


def recovered(cfg):
    base  = solved_rates(cfg["base"], "no-skill")
    skill = solved_rates(cfg["skill"], "skill-v2.1-sys")
    return [skill[b] - base[b] for b in ROWS]


def main():
    fig, ax = plt.subplots(figsize=(10, 5.2))

    x = np.arange(len(ROWS), dtype=float)
    x[-1] += 0.35  # small extra gap before the pooled Aggregate group
    width = 0.38

    for i, (name, cfg) in enumerate(FAMILIES.items()):
        vals = recovered(cfg)
        offset = (i - 0.5) * width
        bars = ax.bar(x + offset, vals, width * 0.92, label=name,
                      color=cfg["color"], edgecolor="white", linewidth=0.8, zorder=3)
        for b, v in zip(bars, vals):
            ax.annotate(f"{v:+.1f}", (b.get_x() + b.get_width() / 2,
                        v + (0.25 if v >= 0 else -0.25)),
                        ha="center", va="bottom" if v >= 0 else "top",
                        fontsize=8, color="#333333")

    ax.axhline(0, color="#555555", linewidth=1.0, zorder=2)
    ax.set_ylabel("Recovered (pp)  =  (8B + skill) − 8B baseline")
    ax.set_title("Skill effect by family: percentage points recovered by "
                 "skill-v2.1-sys\n(8B, python-tiny; positive = skill helped)",
                 fontsize=11)
    ax.set_xticks(x)
    ax.set_xticklabels(XLABELS, rotation=25, ha="right", fontsize=9)
    # emphasise the pooled Aggregate tick
    ax.get_xticklabels()[-1].set_fontweight("bold")
    ax.legend(frameon=False, loc="upper left")
    ax.grid(axis="y", color="#e5e5e5", linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)

    fig.tight_layout()
    out = os.path.join(FIG_DIR, "family_gap_closure_comparison.png")
    fig.savefig(out, dpi=150, bbox_inches="tight")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
