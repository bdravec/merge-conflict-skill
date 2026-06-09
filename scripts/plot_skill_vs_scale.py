"""
plot_skill_vs_scale.py — Review 3 skill-vs-scale diagram (issue #90).

One comparison figure mirroring plot_baseline_scaling.py's layout, but instead
of two no-skill baselines it pits a *skilled small model* against a *larger
baseline*:
  (col 1) Apertus-8B  with v2.1-sys skill   (condition "skill-v2.1-sys")
  (col 2) Apertus-70B no-skill baseline     (condition "no-skill")

Story: 8B+skill ~= 28.6% solved, +7.4pp over its own no-skill baseline,
landing within ~3pp of the 9x-larger 70B baseline (31.5%).

Two panels (same as plot_baseline_scaling.py):
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

# (display label, results file, condition to keep)
COLUMNS = [
    ("Apertus-8B\n+v2.1 skill", RESULTS_DIR / "pilot_results_apertus_v2.1_python_tiny.jsonl", "skill-v2.1-sys"),
    ("Apertus-70B\nbaseline",   RESULTS_DIR / "apertus-70b_baseline_python_tiny.jsonl",       "no-skill"),
]
TITLE    = "Apertus skill vs scale"
OUT_NAME = "baseline_scaling_apertus_v2.1_vs_70b.png"

# Headline pass/fail definition (docs/baseline_32b_analysis.md, #56):
#   solved  = max(edit, winnowing) > 0.8
#   failed  = max(edit, winnowing) <= 0.05  (empties folded in as score 0)
#   partial = everything between
TIERS  = ["Solved", "Partial", "Failed"]
COLORS = {"Solved": "#2e7d32", "Partial": "#ffb74d", "Failed": "#e53935"}


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


def make_figure():
    labels = [lab for lab, _, _ in COLUMNS]
    data   = {lab: load_clean(path, cond) for lab, path, cond in COLUMNS}

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
    w = 0.35
    xm = np.arange(len(metrics))
    for i, lab in enumerate(labels):
        vals = [mean_sim(data[lab], k) for k, _ in metrics]
        bars = axR.bar(xm + (i - 0.5) * w, vals, w, label=lab.replace("\n", " "),
                       color=("#90a4ae" if i == 0 else "#1565c0"), edgecolor="black", linewidth=0.5)
        axR.bar_label(bars, fmt="%.3f", fontsize=9, padding=2)
    axR.set_xticks(xm)
    axR.set_xticklabels([lbl for _, lbl in metrics], fontsize=11)
    axR.set_ylabel("mean similarity")
    axR.set_ylim(0, 1.0)
    axR.set_title("Mean similarity")
    axR.legend(frameon=False, fontsize=9)

    fig.suptitle(f"{TITLE}  —  python-tiny", fontsize=14)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    out = FIGURES_DIR / OUT_NAME
    fig.savefig(out, dpi=140, bbox_inches="tight")
    plt.close(fig)

    # ---- console summary ----
    print(f"\n=== {TITLE} ===")
    for lab in labels:
        p, c, n = tier_pct(data[lab])
        print(f"  {lab.replace(chr(10),' '):22} n={n:5}  Solved {p['Solved']:5.1f}%  Partial {p['Partial']:5.1f}%  "
              f"Failed {p['Failed']:5.1f}%  | "
              f"edit {mean_sim(data[lab],'edit'):.3f}  winn {mean_sim(data[lab],'winnowing'):.3f}")
    sm, lg = labels
    dsolved = tier_pct(data[lg])[0]["Solved"] - tier_pct(data[sm])[0]["Solved"]
    print(f"  Δ(70B-baseline − 8B+skill): solved {dsolved:+.1f}pp")
    print(f"  wrote {out}")


if __name__ == "__main__":
    make_figure()
