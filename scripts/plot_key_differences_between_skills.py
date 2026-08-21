"""
plot_key_differences_between_skills.py — what differs between v1, v2 and v2.1 (#119)

Companion to plot_skill_design_loop.py: that figure shows the procedure, this one
shows the artefacts the procedure produced. It reuses that script's design elements
(navy containers, black header pills, grey content boxes, orange annotation layer,
measured centred legend) so the two read as one pair in the chapter.

Structure and wording follow Barbara's own draft, uploaded to
results_overleaf_figures/skill-design-loop/ on 2026-08-21: three blocks per version
— unique factor, why built, key excerpt — with the excerpt quoted verbatim. The
colour layers map onto her blocks: grey is what the file specifies, orange is the
rationale, and the excerpt sits in a plain quote box.

Two departures from that draft, both flagged for her:
  - sizes are given in WORDS, not lines, matching the section prose (line count is
    a formatting artefact).
  - "taxonomy" is replaced by "pattern hierarchy", the one term the chapter uses.

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

QUOTE_FC = "#ffffff"

# Version columns: (x, version, size). Width 50, gap 6 for the arrow between them.
COL_W = 50.0
COLUMNS = [
    ( 28.0, "v1 SKILL.md",   "277 words"),
    ( 84.0, "v2 SKILL.md",   "742 words"),
    (140.0, "v2.1 SKILL.md", "1102 words"),
]

Y_TOP    = 78.0   # container top edge; the header pill straddles it
Y_BOTTOM = 15.0
LABEL_X  = 25.0   # row labels are right-aligned here, left of the first column

# Her three blocks: (label, y, h, style, (v1, v2, v2.1)). Line breaks are hand-set:
# a cell is 46 units wide, which holds ~38 characters at the body size.
ROWS = [
    ("Unique factor", 53.0, 18.0, "spec", (
        "minimalist: locate the conflict,\n"
        "read both sides, decide, output.\n"
        "Four options as a flat list, and\n"
        "no pattern hierarchy.",

        "a four-pattern hierarchy — empty,\n"
        "combine, pick, custom — applied as\n"
        "ordered tests, plus a priority\n"
        "ladder for pick on symbol\n"
        "references.",

        "an upfront output-discipline section:\n"
        "no comments, no surrounding-code\n"
        "echo, no fabricated identifiers.\n"
        "The empty test splits so one empty\n"
        "side becomes pick; custom may use\n"
        "surrounding-code tokens.",
    )),
    ("Why built", 37.0, 12.0, "why", (
        "establish a baseline prompt: resolve\n"
        "one conflict block and return only the\n"
        "resolved file, so later versions have\n"
        "a control to improve on.",

        "decision-procedure framing — turn the\n"
        "open-ended choice into a strict ordered\n"
        "test, so the model defaults to pick and\n"
        "only escapes to custom when justified.",

        "target the failure modes v2 still\n"
        "allowed: echoing the surrounding code,\n"
        "fabricating identifiers, and adding\n"
        "comments.",
    )),
    ("Key excerpt", 19.0, 14.0, "quote", (
        "Determine the correct resolution.\n"
        "Choose one of: Keep branch A's changes /\n"
        "Keep branch B's / Combine both / Write a\n"
        "new resolution.",

        "There are four patterns: empty, combine,\n"
        "pick, custom. Apply the following tests\n"
        "in order — the first match decides. … Do\n"
        "not jump to custom. Most conflicts are\n"
        "pick.",

        "No comments in the code block … No\n"
        "surrounding-code echo. Do not copy lines\n"
        "from the surrounding code into the\n"
        "resolution … No fabricated identifiers.",
    )),
]

# (facecolor, edgecolor, textcolor, fontsize, extra text kwargs) per row style.
STYLES = {
    "spec":  (STEP_FC, STEP_EC, INK,     8.4, {}),
    "why":   (INST_FC, INST_EC, INST_TX, 7.6, {}),
    "quote": (QUOTE_FC, STEP_EC, INK,    7.6, {"family": "monospace", "style": "italic"}),
}

LEGEND = [
    (STEP_FC, STEP_EC, INK,     "what the version specifies"),
    (INST_FC, INST_EC, INST_TX, "why it was built that way"),
    (QUOTE_FC, STEP_EC, INK,    "quoted verbatim from the file"),
]


def header_pill(fig, ax, x, version, size):
    """Black pill straddling the container's top edge: bold version, then size.

    Width follows the rendered text, since "v2.1 SKILL.md" is wider than "v1".
    """
    w_ver  = text_widths(fig, ax, [version], 11.5, fontweight="bold")[0]
    w_size = text_widths(fig, ax, [size], 9.5)[0]

    pad, gap = 3.0, 2.4
    rbox(ax, x + 1.5, Y_TOP - 3.0, pad * 2 + w_ver + gap + w_size, 6.0, INK, INK)
    ax.text(x + 1.5 + pad, Y_TOP, version, fontsize=11.5, fontweight="bold",
            color="white", ha="left", va="center", zorder=4)
    ax.text(x + 1.5 + pad + w_ver + gap, Y_TOP, size, fontsize=9.5,
            color="white", ha="left", va="center", zorder=4)


def draw(fig, ax):
    for x, version, size in COLUMNS:
        rbox(ax, x, Y_BOTTOM, COL_W, Y_TOP - Y_BOTTOM, "none", NAVY, lw=1.4)
        header_pill(fig, ax, x, version, size)

    # The versions run left to right, same direction as the procedure figure.
    for (x_from, *_), (x_to, *_) in zip(COLUMNS, COLUMNS[1:]):
        connect(ax, [(x_from + COL_W, 46.5), (x_to, 46.5)])

    for label, y, h, style, cells in ROWS:
        fc, ec, tc, fs, kwargs = STYLES[style]
        ax.text(LABEL_X, y + h / 2, label, fontsize=9.2, fontweight="bold",
                color=INK, ha="right", va="center", zorder=4)
        for (x, *_), text in zip(COLUMNS, cells):
            rbox(ax, x + 2.0, y, COL_W - 4.0, h, fc, ec, lw=1.0)
            ax.text(x + COL_W / 2, y + h / 2, text, fontsize=fs, color=tc,
                    ha="center", va="center", linespacing=1.35, zorder=4, **kwargs)


def main():
    fig, ax = plt.subplots(figsize=(15.0, 6.4))
    ax.set_xlim(0, 190)
    ax.set_ylim(13, 93)
    ax.set_aspect("equal")
    ax.axis("off")

    # Centre the title and legend on the drawn content, which starts at the widest
    # row label rather than at the first column.
    label_w = max(text_widths(fig, ax, [r[0] for r in ROWS], 9.2, fontweight="bold"))
    center = ((LABEL_X - label_w) + (COLUMNS[-1][0] + COL_W)) / 2

    ax.text(center, 91.0, "Key differences between skill v1, v2, v2.1",
            fontsize=19, fontweight="bold", color=INK, ha="center", va="center")
    draw_legend(fig, ax, y=85.5, entries=LEGEND, center=center, gap=6.0)

    draw(fig, ax)

    out_path = os.path.join(FIG_DIR, "Key_differences_between_skills_v1_v2_v2_1.png")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    plt.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
