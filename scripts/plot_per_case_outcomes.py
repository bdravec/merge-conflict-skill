"""
plot_per_case_outcomes.py — per-case outcome stacked-bar chart for #48

Reads the 6 pilot JSONLs (Qwen3 + Apertus × v1 + v2 + v2.1), computes
Δedit = skill-condition − no-skill within each pilot, buckets each case
into 5 outcome categories using fixed thresholds, and emits a stacked
bar chart with 12 bars (6 Qwen3 left, 6 Apertus right).

Thresholds (Δedit):
  clear worse    : Δ ≤ −0.05
  marginal worse : −0.05 < Δ ≤ −0.02
  same           : |Δ| < 0.02
  marginal better: 0.02 ≤ Δ < 0.05
  clear better   : Δ ≥ 0.05

Run from repo root:
    python scripts/plot_per_case_outcomes.py

Output: docs/figures/per_case_outcomes_v1_v2_v21.png
"""

import json
import os
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
OUT_PATH    = os.path.join(os.path.dirname(__file__), "..", "docs", "figures",
                           "per_case_outcomes_v1_v2_v21.png")

PILOTS = [
    # (model_label, skill_version_label, jsonl_filename)
    ("Qwen3-8B",   "v1",   "pilot_results_qwen3_v2.jsonl"),
    ("Qwen3-8B",   "v2",   "pilot_results_qwen3_skill-v2.jsonl"),
    ("Qwen3-8B",   "v2.1", "pilot_results_qwen3_skill-v2.1.jsonl"),
    ("Apertus-8B", "v1",   "pilot_results_apertus_v2.jsonl"),
    ("Apertus-8B", "v2",   "pilot_results_apertus_skill-v2.jsonl"),
    ("Apertus-8B", "v2.1", "pilot_results_apertus_skill-v2.1.jsonl"),
]

# Bucket thresholds
T_SAME   = 0.02   # |Δ| < T_SAME    → same
T_CLEAR  = 0.05   # |Δ| ≥ T_CLEAR   → clear

# Bucket order (bottom-to-top in the stacked bar)
CATEGORIES = ["clear worse", "marginal worse", "same",
              "marginal better", "clear better"]

# Color scheme: red → grey → green diverging
COLORS = {
    "clear worse":     "#b2182b",  # dark red
    "marginal worse":  "#ef8a62",  # light red
    "same":            "#bfbfbf",  # grey
    "marginal better": "#91cf60",  # light green
    "clear better":    "#1a9850",  # dark green
}


def classify(delta: float) -> str:
    if abs(delta) < T_SAME:
        return "same"
    if delta >= T_CLEAR:
        return "clear better"
    if delta <= -T_CLEAR:
        return "clear worse"
    if delta > 0:
        return "marginal better"
    return "marginal worse"


def deltas_for_pilot(jsonl_path: str, skill_condition: str) -> list[float]:
    by_case = defaultdict(dict)
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            key = (r["case_id"], r["conflict_idx"])
            by_case[key][r["condition"]] = r
    out = []
    for conds in by_case.values():
        if "no-skill" not in conds or skill_condition not in conds:
            continue
        ns = conds["no-skill"]
        sk = conds[skill_condition]
        if ns["error"] or sk["error"]:
            continue
        ns_edit = ns["metrics"]["edit"]
        sk_edit = sk["metrics"]["edit"]
        if ns_edit is None or sk_edit is None:
            continue
        out.append(sk_edit - ns_edit)
    return out


def main():
    # Compute counts per (model, skill_version, sys/user) → 12 cells
    bar_specs = []   # (model_label, version, condition_label, counts dict)
    for model, version, fname in PILOTS:
        path = os.path.join(RESULTS_DIR, fname)
        for inject in ("sys", "user"):
            cond = f"skill-{version}-{inject}"
            deltas = deltas_for_pilot(path, cond)
            counts = {c: 0 for c in CATEGORIES}
            for d in deltas:
                counts[classify(d)] += 1
            bar_specs.append((model, version, inject, counts, len(deltas)))

    # Plot
    fig, ax = plt.subplots(figsize=(11, 5.5))
    n_bars = len(bar_specs)
    x = np.arange(n_bars, dtype=float)

    # Visual gap between Qwen3 group (first 6) and Apertus group (last 6)
    GAP = 0.6
    x[6:] += GAP

    bottoms = np.zeros(n_bars)
    for cat in CATEGORIES:
        heights = np.array([b[3][cat] for b in bar_specs], dtype=float)
        bars = ax.bar(x, heights, bottom=bottoms, width=0.78,
                      color=COLORS[cat], label=cat, edgecolor="white", linewidth=0.6)
        # In-segment count labels for non-trivial segments
        for rect, h, btm in zip(bars, heights, bottoms):
            if h >= 2:
                ax.text(rect.get_x() + rect.get_width() / 2,
                        btm + h / 2, f"{int(h)}",
                        ha="center", va="center",
                        fontsize=8, color="black" if cat == "same" else "white",
                        fontweight="bold")
        bottoms += heights

    # X-axis labels
    xtick_labels = [f"{v}-{inj}" for (_, v, inj, _, _) in bar_specs]
    ax.set_xticks(x)
    ax.set_xticklabels(xtick_labels, rotation=0, fontsize=9)

    # Model group labels above bars
    qwen_center = x[:6].mean()
    apertus_center = x[6:].mean()
    ax.text(qwen_center, 21.5, "Qwen3-8B",
            ha="center", va="bottom", fontsize=12, fontweight="bold")
    ax.text(apertus_center, 21.5, "Apertus-8B",
            ha="center", va="bottom", fontsize=12, fontweight="bold")

    # Y axis
    ax.set_ylim(0, 23)
    ax.set_yticks(range(0, 21, 5))
    ax.set_ylabel("cases (n=20 per condition)", fontsize=10)

    # Title + footer
    ax.set_title(
        "Per-case outcome distribution — skill-condition vs no-skill, python/func bucket\n"
        f"Same = |Δedit| < {T_SAME};  Clear = |Δedit| ≥ {T_CLEAR}",
        fontsize=11, pad=14,
    )

    # Legend
    handles, labels = ax.get_legend_handles_labels()
    # Reverse so legend reads top-to-bottom matching stack top-to-bottom
    ax.legend(handles[::-1], labels[::-1],
              loc="center left", bbox_to_anchor=(1.01, 0.5),
              frameon=False, fontsize=9)

    # Clean spines
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)

    plt.tight_layout()

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    plt.savefig(OUT_PATH, dpi=150, bbox_inches="tight")
    print(f"Saved: {OUT_PATH}")

    # Echo counts table
    print()
    print(f"{'pilot':<18} {'CB':>3} {'MB':>3} {'SA':>3} {'MW':>3} {'CW':>3}  n")
    for (model, v, inj, counts, n) in bar_specs:
        label = f"{model.split('-')[0].lower()} {v}-{inj}"
        print(f"{label:<18} "
              f"{counts['clear better']:>3} {counts['marginal better']:>3} "
              f"{counts['same']:>3} "
              f"{counts['marginal worse']:>3} {counts['clear worse']:>3}  {n}")


if __name__ == "__main__":
    main()
