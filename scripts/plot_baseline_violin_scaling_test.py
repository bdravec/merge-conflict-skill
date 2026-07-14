"""
plot_baseline_violin_scaling_test.py — THROWAWAY demo variant (#96, delete after review)

Same split-violin baseline scaling figure as plot_baseline_violin_scaling.py, but
each violin half is flanked by a thin STACKED PROPORTION BAR (failed / partial /
solved) sized to the actual rates. The violin still shows score SHAPE (KDE density);
the bar carries the fail/solved RATE as a readable magnitude — fixing the trap where
the smeared bottom tail of the violin (exact-0.0 cases bleed below y=0) makes a
higher fail rate look smaller (e.g. Qwen3-32B text bucket 5.7% vs Qwen3-8B 5.1%).

Only the Qwen3 pair is rendered here (demo). Run from repo root:
    python scripts/plot_baseline_violin_scaling_test.py
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

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

T_SOLVED = 0.8
T_FAIL   = 0.05

# model identity colors (unchanged from the original figure)
C8, C32 = "#91bfdb", "#2166ac"
# tier status colors (match the figure's threshold lines: red 0.05, green 0.8)
C_FAIL, C_MID, C_SOLVED = "#d73027", "#d9d9d9", "#1a9850"

PILOTS = [
    ("Qwen3-8B",  "pilot_results_qwen3_baseline_python_tiny.jsonl",        C8,  "left"),
    ("Qwen3-32B", "pilot_results_qwen3-32b_baseline_python_tiny_32b.jsonl", C32, "right"),
]

OUT_NAME = "baseline_violin_scaling_qwen3_test.png"


def max_scores_per_bucket(jsonl_path):
    """max(edit, winnowing) per bucket; no-skill + no-error rows; empties -> 0.0."""
    out = {b: [] for b in BUCKETS}
    with open(jsonl_path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("condition") != "no-skill" or r.get("error") is not None:
                continue
            m = r["metrics"]
            if m.get("empty"):
                out[r["bucket"]].append(0.0)
                continue
            e, w = m.get("edit"), m.get("winnowing")
            if e is None or w is None:
                continue
            out[r["bucket"]].append(max(e, w))
    return out


def main():
    positions = list(range(len(BUCKETS)))

    per_data, per_solved, per_fail, per_n = [], [], [], []
    for _label, fname, _color, _side in PILOTS:
        per_bucket = max_scores_per_bucket(os.path.join(RESULTS_DIR, fname))
        data = [per_bucket[b] for b in BUCKETS]
        per_data.append(data)
        per_solved.append([sum(1 for s in d if s > T_SOLVED) / len(d) * 100 for d in data])
        per_fail.append([sum(1 for s in d if s <= T_FAIL) / len(d) * 100 for d in data])
        per_n.append([len(d) for d in data])

    fig, ax = plt.subplots(figsize=(13, 6.5))

    # --- violins (KDE density, shape only) ---
    for (label, _fname, color, side), data in zip(PILOTS, per_data):
        parts = ax.violinplot(data, positions=positions, widths=0.7,
                              showmedians=True, showextrema=False)
        for body, xc in zip(parts["bodies"], positions):
            v = body.get_paths()[0].vertices
            v[:, 0] = np.minimum(v[:, 0], xc) if side == "left" else np.maximum(v[:, 0], xc)
            body.set_facecolor(color)
            body.set_edgecolor(color)
            body.set_alpha(0.55)
            body.set_linewidth(1.0)
        if "cmedians" in parts:
            segs = []
            for seg, xc in zip(parts["cmedians"].get_segments(), positions):
                seg = seg.copy()
                if side == "left":
                    seg[1, 0] = xc
                else:
                    seg[0, 0] = xc
                segs.append(seg)
            parts["cmedians"].set_segments(segs)
            parts["cmedians"].set_color(color)
            parts["cmedians"].set_linewidth(2.0)

    # --- stacked proportion bars (the rate, as magnitudes) ---
    BAR_W = 0.11

    def stacked_bar(x, fail_pct, solved_pct):
        f = fail_pct / 100.0
        s = solved_pct / 100.0
        mid = 1 - f - s
        ax.bar(x, f,   BAR_W, bottom=0,       color=C_FAIL,   edgecolor="white", linewidth=0.6, zorder=5)
        ax.bar(x, mid, BAR_W, bottom=f,       color=C_MID,    edgecolor="white", linewidth=0.6, zorder=5)
        ax.bar(x, s,   BAR_W, bottom=f + mid, color=C_SOLVED, edgecolor="white", linewidth=0.6, zorder=5)
        ax.text(x, -0.035, f"{fail_pct:.1f}", ha="center", va="top", fontsize=7.5,
                color=C_FAIL, fontweight="bold")
        ax.text(x, 1.035, f"{solved_pct:.1f}", ha="center", va="bottom", fontsize=7.5,
                color=C_SOLVED, fontweight="bold")

    for x in positions:
        stacked_bar(x - 0.40, per_fail[0][x], per_solved[0][x])
        stacked_bar(x + 0.40, per_fail[1][x], per_solved[1][x])
        n0, n1 = per_n[0][x], per_n[1][x]
        ax.text(x, -0.10, f"n={n0}" if n0 == n1 else f"n={n0}/{n1}",
                ha="center", va="top", fontsize=6.5, color="#777")

    ax.axhline(T_SOLVED, color=C_SOLVED, linestyle=":", linewidth=0.8, alpha=0.5)
    ax.axhline(T_FAIL,   color=C_FAIL,   linestyle=":", linewidth=0.8, alpha=0.5)

    ax.set_xticks(positions)
    ax.set_xticklabels(BUCKETS, rotation=30, fontsize=9, ha="right")
    ax.set_xlim(-0.65, len(BUCKETS) - 1 + 0.65)
    ax.set_ylim(-0.16, 1.14)
    ax.set_yticks([0, 0.2, 0.4, 0.6, 0.8, 1.0])
    ax.set_ylabel("max(edit, winnowing)", fontsize=10)
    ax.set_title(
        "Qwen3 baseline scaling — Qwen3-8B (left) vs Qwen3-32B (right), no-skill, python-tiny\n"
        "violin = score SHAPE (KDE density);  flanking stacked bars = actual failed / partial / solved RATE",
        fontsize=11, pad=14,
    )

    handles = [
        Patch(facecolor=C8,  alpha=0.55, label="Qwen3-8B (violin, left)"),
        Patch(facecolor=C32, alpha=0.55, label="Qwen3-32B (violin, right)"),
        Patch(facecolor=C_SOLVED, label="solved (>0.8)"),
        Patch(facecolor=C_MID,    label="partial"),
        Patch(facecolor=C_FAIL,   label="failed (≤0.05)"),
    ]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(1.005, 1.0),
              fontsize=8.5, frameon=False)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    plt.tight_layout()
    os.makedirs(FIG_DIR, exist_ok=True)
    out_path = os.path.join(FIG_DIR, OUT_NAME)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
