"""
plot_key_differences_between_skills.py — what differs between v1, v2 and v2.1 (#119)

Companion to plot_skill_design_loop.py: that figure shows the procedure, this one
shows the artefacts the procedure produced. It reuses that script's design elements
(navy containers, black header pills, grey content boxes, orange annotation layer,
measured centred legend) so the two read as one pair in the chapter.

Scope, following the section split: the figure says what each file CONTAINS, never
how it scored. Every per-version delta is prose in the findings section, and no
number here is a result.

All content is read from the three SKILL.md files under skills/, not from the
analysis docs:
  merge-conflict-resolve-v1    277 words
  merge-conflict-resolve-v2    742 words
  merge-conflict-resolve-v2.1  1102 words

Output:
  - docs/figures/Key_differences_between_skills_v1_v2_v2_1.png
  - results_overleaf_figures/skill-design-loop/Key_differences_between_skills_v1_v2_v2_1.pdf
    (via export_overleaf_figures.py, which tees savefig)
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from plot_skill_design_loop import (
    INK, INST_EC, INST_FC, INST_TX, NAVY, STEP_EC, STEP_FC,
    connect, draw_legend, rbox, text_widths,
)

FIG_DIR = os.path.join(os.path.dirname(__file__), "..", "docs", "figures")

# Version columns: (x, version, size). Width 38, gap 8 for the arrow between them.
COL_W = 38.0
COLUMNS = [
    ( 30.0, "v1",   "277 words"),
    ( 76.0, "v2",   "742 words"),
    (122.0, "v2.1", "1102 words"),
]

Y_TOP    = 80.0   # container top edge; the header pill straddles it
Y_BOTTOM = 1.5
LABEL_X  = 27.0   # row labels are right-aligned here, left of the first column

# Compared dimensions: (label, y, h, (v1, v2, v2.1)). Heights follow the tallest
# cell in the row so the rows stay aligned across all three columns.
ROWS = [
    ("Resolution choice", 64.0, 9.0, (
        "four options, no order: keep a side,\ncombine, or write a new resolution",
        "four patterns in a fixed order:\nempty → combine → pick → custom;\nfirst match decides",
        "same order; the empty test splits\ninto both sides empty and\none side empty",
    )),
    ("Output discipline", 51.0, 9.0, (
        "one line in the output format:\nno text outside the code block",
        "adds a cap of |a| + |b| characters\nand a no-new-identifiers rule",
        "three rules hoisted above pattern\nselection; the cap becomes a\npost-hoc self-check",
    )),
    ("Worked examples", 40.0, 7.0, (
        "none",
        "three: pick, combine, custom",
        "five: adds identifier divergence\nand completeness over brevity",
    )),
    ("Edge cases", 27.0, 9.0, (
        "none",
        "five, at the end of the file",
        "five: one side empty moves into the\npattern test; file-level resolutions\nadded",
    )),
    ("Custom resolutions", 16.0, 7.0, (
        "unconstrained: write a new resolution",
        "only tokens already present on\nside a or side b",
        "surrounding-code tokens allowed\nas a secondary source",
    )),
]

# The orange layer: what each version is, in one line. v1 has nothing to change
# against, so its entry records that it is the starting point.
SUMMARIES = (
    "the control: deliberately generic,\nthe starting point for the loop",
    "rewrite around the pattern hierarchy\nand output discipline",
    "revision: discipline moved first,\nthe cap replaced by checkable rules",
)
SUMMARY_Y, SUMMARY_H = 5.0, 7.0

LEGEND = [
    (STEP_FC, STEP_EC, INK,     "what the file specifies"),
    (INST_FC, INST_EC, INST_TX, "what changed in this version"),
]


def header_pill(fig, ax, x, version, size):
    """Black pill straddling the container's top edge: bold version, then size.

    Width follows the rendered text, since "v2.1" is wider than "v1".
    """
    w_ver  = text_widths(fig, ax, [version], 13.0, fontweight="bold")[0]
    w_size = text_widths(fig, ax, [size], 10.5)[0]

    pad, gap = 3.0, 2.4
    rbox(ax, x + 1.5, Y_TOP - 3.0, pad * 2 + w_ver + gap + w_size, 6.0, INK, INK)
    ax.text(x + 1.5 + pad, Y_TOP, version, fontsize=13, fontweight="bold",
            color="white", ha="left", va="center", zorder=4)
    ax.text(x + 1.5 + pad + w_ver + gap, Y_TOP, size, fontsize=10.5,
            color="white", ha="left", va="center", zorder=4)


def draw(fig, ax):
    for x, version, size in COLUMNS:
        rbox(ax, x, Y_BOTTOM, COL_W, Y_TOP - Y_BOTTOM, "none", NAVY, lw=1.4)
        header_pill(fig, ax, x, version, size)

    # The loop is left to right, same as the procedure figure.
    for (x_from, *_), (x_to, *_) in zip(COLUMNS, COLUMNS[1:]):
        connect(ax, [(x_from + COL_W, 42.0), (x_to, 42.0)])

    for label, y, h, cells in ROWS:
        ax.text(LABEL_X, y + h / 2, label, fontsize=9.2, fontweight="bold",
                color=INK, ha="right", va="center", zorder=4)
        for (x, *_), text in zip(COLUMNS, cells):
            rbox(ax, x + 2.0, y, COL_W - 4.0, h, STEP_FC, STEP_EC)
            ax.text(x + COL_W / 2, y + h / 2, text, fontsize=8.4, color=INK,
                    ha="center", va="center", linespacing=1.35, zorder=4)

    for (x, *_), text in zip(COLUMNS, SUMMARIES):
        rbox(ax, x + 2.0, SUMMARY_Y, COL_W - 4.0, SUMMARY_H, INST_FC, INST_EC, lw=1.0)
        ax.text(x + COL_W / 2, SUMMARY_Y + SUMMARY_H / 2, text, fontsize=7.6,
                color=INST_TX, ha="center", va="center", linespacing=1.35, zorder=4)


def main():
    fig, ax = plt.subplots(figsize=(15.0, 9.6))
    ax.set_xlim(0, 164)
    ax.set_ylim(0, 97)
    ax.set_aspect("equal")
    ax.axis("off")

    # Centre the title and legend on the drawn content, which starts at the widest
    # row label rather than at the first column.
    label_w = max(text_widths(fig, ax, [r[0] for r in ROWS], 9.2, fontweight="bold"))
    center = ((LABEL_X - label_w) + (COLUMNS[-1][0] + COL_W)) / 2

    ax.text(center, 93.5, "Key differences between the merge-conflict skills",
            fontsize=19, fontweight="bold", color=INK, ha="center", va="center")
    draw_legend(fig, ax, y=87.5, entries=LEGEND, center=center)

    draw(fig, ax)

    out_path = os.path.join(FIG_DIR, "Key_differences_between_skills_v1_v2_v2_1.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
