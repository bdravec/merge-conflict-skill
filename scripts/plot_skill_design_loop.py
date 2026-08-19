"""
plot_skill_design_loop.py — the skill-design loop as a two-layer diagram (#117)

Supersedes the hand-drawn skill-design-loop.pdf (commit 2331fa4, removed once this
replaced it), with the structure fixed:

  - the procedure layer is GENERIC. The authored artefact is "SKILL.md vN", not an
    enumeration of versions, so the figure supports the "reusable" claim in its own
    title. The iteration count is an outcome, not a design parameter.
  - the study layer is MARKED SEPARATELY, in orange. Every orange box says how this
    thesis instantiated the generic step it sits under; delete the orange layer and
    the procedure still reads as a method someone else can follow.
  - the loop is governed by an explicit DECISION, so "iterate N times" has a stopping
    rule. Both exits are labelled generically; that this study exited without meeting
    the criterion is recorded in the orange layer, where it belongs.

Kept from the original: the visual language (numbered black pills, grey step boxes,
orange annotations, dark-navy stage containers) and the title.

Output:
  - docs/figures/skill_design_loop.png
  - results_overleaf_figures/skill-design-loop/skill_design_loop.pdf (via
    export_overleaf_figures.py, which tees savefig)
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "figures")

NAVY    = "#1f3a52"
INK     = "#1a1a1a"
STEP_FC = "#eff0f1"
STEP_EC = "#c7cbcf"
INST_FC = "#fdf1dc"
INST_EC = "#e0a03c"
INST_TX = "#7a4b0a"
ARROW   = "#3a3a3a"

# Stage containers: (x, y, w, h, number, title)
STAGES = [
    (  3.0,  5.0, 47.0, 71.0, "1", "Benchmark and research"),
    ( 57.0,  5.0, 47.0, 71.0, "2", "Pilot on ablation"),
    (112.0, 37.0, 38.0, 39.0, "3", "Run on models"),
]

# Generic steps: (x, y, w, h, text). Column x + 38 wide, vertical pitch 16.
STEPS = [
    (  6.0, 64.0, 38.0, 7.0, "Choose a benchmark for the skill"),
    (  6.0, 48.0, 38.0, 7.0, "Run it with no skill\nto get a baseline"),
    (  6.0, 32.0, 38.0, 7.0, "Review the empirical research"),
    (  6.0, 16.0, 38.0, 7.0, "Hypothesize what\nthe skill should teach"),
    ( 60.0, 64.0, 38.0, 7.0, "Author SKILL.md vN"),
    ( 60.0, 48.0, 38.0, 7.0, "Pilot it on the ablation slice"),
    ( 60.0, 32.0, 38.0, 7.0, "Analyze the pilot data per case"),
    ( 60.0, 16.0, 38.0, 7.0, "Cross-check failure modes\nacross models"),
    (115.0, 64.0, 32.0, 7.0, "Run the full benchmark"),
    (115.0, 48.0, 32.0, 7.0, "Compare to the baseline"),
]

# Study layer: (x, y, w, h, text) — each sits under the generic step it instantiates.
INSTANCES = [
    ( 14.0, 56.5, 34.0, 6.5, "ConGra merge-conflict resolution"),
    ( 14.0, 40.5, 34.0, 6.5, "python/func slice; baseline\n0.297 Apertus-8B / 0.395 Qwen3-8B"),
    ( 14.0, 24.5, 34.0, 6.5, "Boll et al. (2024):\npick / combine / empty / custom"),
    ( 14.0,  8.5, 34.0, 6.5, "spike — single-case ablation\non 0xe4ff79aa"),
    ( 68.0, 56.5, 34.0, 6.5, "three iterations: v1 → v2 → v2.1"),
    ( 68.0, 40.5, 34.0, 6.5, "n=20, three conditions,\nboth 8B models, T=0.0"),
    ( 68.0, 24.5, 34.0, 6.5, "analyze_pilot.py + inspect_case.py"),
    ( 68.0,  8.5, 34.0, 6.5, "same file, opposite verdict\nper model"),
    (123.0, 56.5, 24.0, 6.5, "python-tiny slice,\nn=3,597 per model"),
]

DIAMOND = (79.0, -4.0)
DIAMOND_HW, DIAMOND_HH = 17.0, 5.4


def rbox(ax, x, y, w, h, fc, ec, lw=1.1):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle="round,pad=0,rounding_size=1.3",
        facecolor=fc, edgecolor=ec, linewidth=lw, zorder=2))


def connect(ax, path):
    """Polyline with a single arrowhead on the last segment."""
    for i, ((x0, y0), (x1, y1)) in enumerate(zip(path, path[1:])):
        last = i == len(path) - 2
        ax.add_patch(FancyArrowPatch(
            (x0, y0), (x1, y1), arrowstyle="-|>" if last else "-",
            mutation_scale=13, color=ARROW, linewidth=1.2,
            shrinkA=0, shrinkB=0, zorder=3))


def edge_label(ax, x, y, text, rotation=0):
    ax.text(x, y, text, fontsize=8.4, style="italic", color=ARROW,
            ha="center", va="center", rotation=rotation, zorder=4,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none"))


def draw(ax):
    for x, y, w, h, num, title in STAGES:
        rbox(ax, x, y, w, h, "none", NAVY, lw=1.4)
        pill_w = 9.0 + 1.32 * len(title)
        rbox(ax, x + 1.5, y + h - 3.0, pill_w, 6.0, INK, INK)
        ax.text(x + 4.6, y + h, num, fontsize=13, fontweight="bold",
                color="white", ha="center", va="center", zorder=4)
        ax.text(x + 8.4, y + h, title, fontsize=10.5, color="white",
                ha="left", va="center", zorder=4)

    for x, y, w, h, text in STEPS:
        rbox(ax, x, y, w, h, STEP_FC, STEP_EC)
        ax.text(x + w / 2, y + h / 2, text, fontsize=9.2, color=INK,
                ha="center", va="center", linespacing=1.35, zorder=4)

    for x, y, w, h, text in INSTANCES:
        rbox(ax, x, y, w, h, INST_FC, INST_EC, lw=1.0)
        ax.text(x + w / 2, y + h / 2, text, fontsize=7.6, color=INST_TX,
                ha="center", va="center", linespacing=1.35, zorder=4)

    # Connectors run down the left of each column so they never cross the orange layer.
    for x in (12.0, 66.0):
        for y_top in (64.0, 48.0, 32.0):
            connect(ax, [(x, y_top), (x, y_top - 9.0)])
    connect(ax, [(121.0, 64.0), (121.0, 55.0)])

    connect(ax, [(50.0, 67.5), (60.0, 67.5)])          # stage 1 -> stage 2
    connect(ax, [(66.0, 16.0), (66.0, 4.2), (79.0, 4.2),
                 (79.0, DIAMOND[1] + DIAMOND_HH)])     # step 2 -> decision

    dx, dy = DIAMOND
    ax.add_patch(Polygon(
        [(dx, dy + DIAMOND_HH), (dx + DIAMOND_HW, dy),
         (dx, dy - DIAMOND_HH), (dx - DIAMOND_HW, dy)],
        closed=True, facecolor="white", edgecolor=NAVY, linewidth=1.4, zorder=2))
    ax.text(dx, dy, "keep criterion met?", fontsize=8.8, color=INK,
            ha="center", va="center", zorder=4)

    # no -> author vN+1, back up the corridor between stages 2 and 3
    connect(ax, [(dx + DIAMOND_HW, dy), (108.0, dy), (108.0, 67.5), (98.0, 67.5)])
    edge_label(ax, 108.0, 36.0, "no — author vN+1", rotation=90)

    # yes -> stage 3
    connect(ax, [(dx, dy - DIAMOND_HH), (dx, -14.0), (131.0, -14.0), (131.0, 37.0)])
    edge_label(ax, 90.0, -14.0, "yes")

    # The study layer records which exit this thesis actually took. Placed beside the
    # decision, unconnected, like every other annotation.
    rbox(ax, 8.0, -9.0, 48.0, 10.0, INST_FC, INST_EC, lw=1.0)
    ax.text(32.0, -4.0,
            "not met at n=20: v2.1 improved Apertus and\n"
            "regressed Qwen3, so the keep decision was\n"
            "escalated to the full benchmark, not taken here",
            fontsize=7.6, color=INST_TX, ha="center", va="center",
            linespacing=1.35, zorder=4)
    # Dotted leader, not an arrow: this annotates the decision, it is not a flow edge.
    ax.plot([56.0, dx - DIAMOND_HW], [dy, dy], linestyle=(0, (2, 2)),
            color=INST_EC, linewidth=1.1, zorder=1)


def main():
    fig, ax = plt.subplots(figsize=(15.0, 10.0))
    ax.set_xlim(0, 153)
    ax.set_ylim(-18, 92)
    ax.set_aspect("equal")
    ax.axis("off")

    ax.text(76.0, 87.0, "A reusable SKILL-design-loop", fontsize=19,
            fontweight="bold", color=INK, ha="center", va="center")

    rbox(ax, 33.0, 79.0, 3.4, 3.4, STEP_FC, STEP_EC)
    ax.text(38.0, 80.7, "generic step — the reusable procedure", fontsize=9.2,
            color=INK, ha="left", va="center")
    rbox(ax, 86.0, 79.0, 3.4, 3.4, INST_FC, INST_EC)
    ax.text(91.0, 80.7, "how this study instantiated it", fontsize=9.2,
            color=INST_TX, ha="left", va="center")

    draw(ax)

    out_path = os.path.join(FIG_DIR, "skill_design_loop.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
