"""
export_overleaf_figures.py — collect the Overleaf figures as vector PDF + PNG (#115)

Gathers the figures used in the thesis into results_overleaf_figures/ at the repo
root, writing each one twice:

  - <name>.pdf   vector, for \\includegraphics in Overleaf
  - <name>.png   copy of the raster version, for the markdown docs

The PDFs are rendered straight from matplotlib rather than converted from the
PNGs: a converted PNG would only embed the 150 dpi bitmap and print soft.

It imports the existing plot scripts and tees their savefig calls, so the plotting
code lives in exactly one place. The originals in docs/figures/ are rewritten
byte-identically as a side effect.

Figures exported (4):
  - skill_vs_scale_violin_apertus_v2.1_vs_70b   (plot_skill_vs_scale_violin, #114)
  - skill_vs_scale_violin_qwen3_v2.1_vs_32b     (plot_skill_vs_scale_violin, #114)
  - baseline_violin_scaling_apertus_max         (plot_baseline_violin_scaling, #84)
  - baseline_violin_scaling_qwen3_max           (plot_baseline_violin_scaling, #84)

Run from repo root:
    python scripts/export_overleaf_figures.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.dirname(SCRIPT_DIR)
OUT_DIR    = os.path.join(REPO_ROOT, "results_overleaf_figures")

sys.path.insert(0, SCRIPT_DIR)

# Only these basenames are exported; anything else a script emits is left alone.
WANTED = {
    "skill_vs_scale_violin_apertus_v2.1_vs_70b",
    "skill_vs_scale_violin_qwen3_v2.1_vs_32b",
    "baseline_violin_scaling_apertus_max",
    "baseline_violin_scaling_qwen3_max",
}

_orig_savefig = plt.savefig
_exported = []


def _tee_savefig(fname, *args, **kwargs):
    """Save where the plot script asked, then also into OUT_DIR as PNG + PDF."""
    _orig_savefig(fname, *args, **kwargs)

    stem = os.path.splitext(os.path.basename(str(fname)))[0]
    if stem not in WANTED:
        return

    _orig_savefig(os.path.join(OUT_DIR, stem + ".png"), *args, **kwargs)

    pdf_kwargs = dict(kwargs)
    pdf_kwargs.pop("dpi", None)          # dpi is meaningless for vector output
    _orig_savefig(os.path.join(OUT_DIR, stem + ".pdf"), *args, **pdf_kwargs)

    _exported.append(stem)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    plt.savefig = _tee_savefig
    try:
        import plot_skill_vs_scale_violin
        import plot_baseline_violin_scaling

        plot_skill_vs_scale_violin.main()
        plot_baseline_violin_scaling.main()
    finally:
        plt.savefig = _orig_savefig

    missing = WANTED - set(_exported)
    if missing:
        raise SystemExit(f"ERROR: expected figures were never rendered: {sorted(missing)}")

    print(f"\nExported {len(_exported)} figures (PDF + PNG) to {OUT_DIR}")
    for stem in sorted(_exported):
        print(f"  - {stem}.pdf / {stem}.png")


if __name__ == "__main__":
    main()
