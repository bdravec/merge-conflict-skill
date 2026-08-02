"""
plot_skill_vs_scale.py — Review 3 skill-vs-scale diagrams (issues #90, #91).

Comparison figures mirroring plot_baseline_scaling.py's layout, but instead of
two no-skill baselines each pits a *skilled small model* against a *larger
baseline*:
  (col 1) <8B model>  with v2.1-sys skill   (condition "skill-v2.1-sys")
  (col 2) <large model> no-skill baseline    (condition "no-skill")

Two contrasting stories:
  Apertus (#90): weak baseline, skill helps — 8B+skill 28.6% solved (+7.4pp
                 over its own baseline), within ~3pp of the 70B baseline (31.5%).
  Qwen3   (#91): strong baseline, skill does not help — 8B+skill 28.3% solved
                 (-1.0pp vs its own baseline), staying ~10pp below the 32B
                 baseline (38.4%).

Two panels per figure (same as plot_baseline_scaling.py):
  (left)  #56 outcome tiers, stacked to 100%
          (Solved = max(edit,winn)>0.8, Failed = <=0.05 / empty, else Partial).
  (right) mean edit & winnowing similarity (empties coerced to 0.0).

Usage:
    python scripts/plot_skill_vs_scale.py
"""

import json
from pathlib import Path
from statistics import mean

import matplotlib.pyplot as plt
import numpy as np

REPO_ROOT   = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "scripts" / "results"
FIGURES_DIR = REPO_ROOT / "docs" / "figures" / "baseline_diagrams"

# Each figure: title, output filename, and two columns of
# (display label, results file, condition to keep).
FIGURES = [
    {
        "title": "Apertus skill vs scale",
        "out_name": "baseline_scaling_apertus_v2.1_vs_70b.png",
        "columns": [
            ("Apertus-8B\n+v2.1 skill", RESULTS_DIR / "pilot_results_apertus_v2.1_python_tiny.jsonl", "skill-v2.1-sys"),
            ("Apertus-70B\nbaseline",   RESULTS_DIR / "apertus-70b_baseline_python_tiny.jsonl",       "no-skill"),
        ],
    },
    {
        "title": "Qwen3 skill vs scale",
        "out_name": "baseline_scaling_qwen3_v2.1_vs_32b.png",
        "columns": [
            ("Qwen3-8B\n+v2.1 skill", RESULTS_DIR / "pilot_results_qwen3_v2.1_python_tiny.jsonl",            "skill-v2.1-sys"),
            ("Qwen3-32B\nbaseline",   RESULTS_DIR / "pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl", "no-skill"),
        ],
    },
    {
        # 3-column variant: 8B no-skill baseline first makes the regression
        # from v2.1 explicit (skill *hurts* the already-strong Qwen3 8B).
        "title": "Qwen3 skill vs scale (with 8B baseline)",
        "out_name": "baseline_scaling_qwen3_v2.1_vs_32b_with_8b.png",
        "columns": [
            ("Qwen3-8B\nbaseline",    RESULTS_DIR / "pilot_results_qwen3_v2.1_python_tiny.jsonl",            "no-skill"),
            ("Qwen3-8B\n+v2.1 skill", RESULTS_DIR / "pilot_results_qwen3_v2.1_python_tiny.jsonl",            "skill-v2.1-sys"),
            ("Qwen3-32B\nbaseline",   RESULTS_DIR / "pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl", "no-skill"),
        ],
    },
]

# Headline pass/fail definition (docs/baseline_32b_analysis.md, #56):
#   solved  = max(edit, winnowing) > 0.8
#   failed  = max(edit, winnowing) <= 0.05  (empties folded in as score 0)
#   partial = everything between
TIERS  = ["Solved", "Partial", "Failed"]
COLORS = {"Solved": "#2e7d32", "Partial": "#ffb74d", "Failed": "#e53935"}

# Right-panel per-column bar colors (first two preserve the original 2-col look).
BAR_COLORS = ["#90a4ae", "#1565c0", "#7b1fa2"]


def load_clean(path, condition):
    rows = [json.loads(l) for l in open(path)]
    return [r for r in rows if r["condition"] == condition and not r["error"]]


def classify(rec):
    m = rec["metrics"]
    if m["empty"]:
        return "Failed"
    s = max(m["edit"] or 0.0, m["winnowing"] or 0.0)
    if s > 0.8:
        return "Solved"
    if s <= 0.05:
        return "Failed"
    return "Partial"


def tier_pct(recs):
    n = len(recs)
    c = {t: 0 for t in TIERS}
    for r in recs:
        c[classify(r)] += 1
    return {t: c[t] / n * 100 for t in TIERS}, c, n


def mean_sim(recs, key):
    vals = [(r["metrics"][key] if r["metrics"][key] is not None else 0.0) for r in recs]
    return mean(vals) if vals else float("nan")


def make_figure(spec):
    title, out_name, columns = spec["title"], spec["out_name"], spec["columns"]
    labels = [lab for lab, _, _ in columns]
    data   = {lab: load_clean(path, cond) for lab, path, cond in columns}

    fig, (axL, axR) = plt.subplots(1, 2, figsize=(11, 5))

    # ---- left: stacked tier % ----
    x = np.arange(len(labels))
    bottoms = np.zeros(len(labels))
    pcts = {lab: tier_pct(data[lab])[0] for lab in labels}
    for tier in TIERS:
        vals = [pcts[lab][tier] for lab in labels]
        axL.bar(x, vals, bottom=bottoms, width=0.55,
                color=COLORS[tier], label=tier, edgecolor="white", linewidth=0.6)
        for xi, (v, b) in enumerate(zip(vals, bottoms)):
            if v >= 3:
                axL.text(xi, b + v / 2, f"{v:.1f}%", ha="center", va="center",
                         fontsize=9, color="black" if tier == "Partial" else "white")
        bottoms += np.array(vals)
    axL.set_xticks(x)
    axL.set_xticklabels(labels, fontsize=11)
    axL.set_ylabel("share of cases (%)")
    axL.set_ylim(0, 100)
    axL.set_title("Outcome share (solved>0.8 / failed≤0.05, max(edit,winn), #56)", fontsize=10)
    axL.legend(loc="upper center", bbox_to_anchor=(0.5, -0.08), ncol=3, frameon=False, fontsize=9)

    # ---- right: mean edit & winnowing ----
    metrics = [("edit", "Edit"), ("winnowing", "Winnowing")]
    n = len(labels)
    w = min(0.35, 0.8 / n)  # keeps the 2-column layout byte-identical
    xm = np.arange(len(metrics))
    for i, lab in enumerate(labels):
        vals = [mean_sim(data[lab], k) for k, _ in metrics]
        bars = axR.bar(xm + (i - (n - 1) / 2) * w, vals, w, label=lab.replace("\n", " "),
                       color=BAR_COLORS[i % len(BAR_COLORS)], edgecolor="black", linewidth=0.5)
        axR.bar_label(bars, fmt="%.3f", fontsize=9, padding=2)
    axR.set_xticks(xm)
    axR.set_xticklabels([lbl for _, lbl in metrics], fontsize=11)
    axR.set_ylabel("mean similarity")
    axR.set_ylim(0, 1.0)
    axR.set_title("Mean similarity")
    axR.legend(frameon=False, fontsize=9)

    fig.suptitle(f"{title}  —  python-tiny", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out = FIGURES_DIR / out_name
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)

    # ---- console summary ----
    print(f"\n=== {title} ===")
    for lab in labels:
        p, c, n = tier_pct(data[lab])
        print(f"  {lab.replace(chr(10),' '):22} n={n:5}  Solved {p['Solved']:5.1f}%  Partial {p['Partial']:5.1f}%  "
              f"Failed {p['Failed']:5.1f}%  | "
              f"edit {mean_sim(data[lab],'edit'):.3f}  winn {mean_sim(data[lab],'winnowing'):.3f}")
    sm, lg = labels
    dsolved = tier_pct(data[lg])[0]["Solved"] - tier_pct(data[sm])[0]["Solved"]
    print(f"  Δ({lg.replace(chr(10),' ')} − {sm.replace(chr(10),' ')}): solved {dsolved:+.1f}pp")
    print(f"  wrote {out}")


def main():
    for spec in FIGURES:
        make_figure(spec)


if __name__ == "__main__":
    main()
