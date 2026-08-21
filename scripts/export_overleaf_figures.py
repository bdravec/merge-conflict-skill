"""
export_overleaf_figures.py — collect the Overleaf figures as vector PDF + PNG (#115)

Gathers the figures used in the thesis into results_overleaf_figures/ at the repo
root, writing each one twice:

  - <name>.pdf   vector, for \\includegraphics in Overleaf
  - <name>.png   copy of the raster version, for the markdown docs

Figures can also be routed into a subfolder (see WANTED). Subfolder exports are
PDF-only: they are Overleaf-bound, and docs/figures/ already carries the PNGs the
markdown links to.

The PDFs are rendered straight from matplotlib rather than converted from the
PNGs: a converted PNG would only embed the 150 dpi bitmap and print soft.

It imports the existing plot scripts and tees their savefig calls, so the plotting
code lives in exactly one place. The originals in docs/figures/ are rewritten
byte-identically as a side effect.

Figures exported (4 + 4):
  - skill_vs_scale_violin_apertus_v2.1_vs_70b   (plot_skill_vs_scale_violin, #114)
  - skill_vs_scale_violin_qwen3_v2.1_vs_32b     (plot_skill_vs_scale_violin, #114)
  - baseline_violin_scaling_apertus_max         (plot_baseline_violin_scaling, #84)
  - baseline_violin_scaling_qwen3_max           (plot_baseline_violin_scaling, #84)

  skill-design-loop/ — the loop diagram, the version comparison, plus one violin
  per version (#116, #117, #119):
  - skill_design_loop                           (plot_skill_design_loop, #117)
  - Key_differences_between_skills_v1_v2_v2_1   (plot_key_differences_between_skills, #119)
  - rq1_baseline_vs_v1_sys_max                  (plot_rq1_baseline_vs_skill_violin, #68)
  - rq1_baseline_vs_v2_sys_max                  (plot_rq1_baseline_vs_skill_violin, #68)
  - rq1_baseline_vs_v2.1_sys_max                (plot_rq1_baseline_vs_skill_violin, #68)

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
# Value = subfolder under results_overleaf_figures/, "" for the folder root.
WANTED = {
    "skill_vs_scale_violin_apertus_v2.1_vs_70b": "",
    "skill_vs_scale_violin_qwen3_v2.1_vs_32b":   "",
    "baseline_violin_scaling_apertus_max":       "",
    "baseline_violin_scaling_qwen3_max":         "",
    "skill_design_loop":                         "skill-design-loop",
    "Key_differences_between_skills_v1_v2_v2_1":  "skill-design-loop",
    "rq1_baseline_vs_v1_sys_max":                "skill-design-loop",
    "rq1_baseline_vs_v2_sys_max":                "skill-design-loop",
    "rq1_baseline_vs_v2.1_sys_max":              "skill-design-loop",
}

_orig_savefig = plt.savefig
_exported = []


def _tee_savefig(fname, *args, **kwargs):
    """Save where the plot script asked, then also into OUT_DIR as PNG + PDF."""
    _orig_savefig(fname, *args, **kwargs)

    stem = os.path.splitext(os.path.basename(str(fname)))[0]
    subdir = WANTED.get(stem)
    if subdir is None:
        return

    out_dir = os.path.join(OUT_DIR, subdir)
    os.makedirs(out_dir, exist_ok=True)

    if not subdir:                       # root exports keep the markdown-facing PNG
        _orig_savefig(os.path.join(out_dir, stem + ".png"), *args, **kwargs)

    pdf_kwargs = dict(kwargs)
    pdf_kwargs.pop("dpi", None)          # dpi is meaningless for vector output
    _orig_savefig(os.path.join(out_dir, stem + ".pdf"), *args, **pdf_kwargs)

    _exported.append(os.path.join(subdir, stem) if subdir else stem)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    plt.savefig = _tee_savefig
    try:
        import plot_skill_vs_scale_violin
        import plot_baseline_violin_scaling
        import plot_rq1_baseline_vs_skill_violin
        import plot_skill_design_loop
        import plot_key_differences_between_skills

        plot_skill_vs_scale_violin.main()
        plot_baseline_violin_scaling.main()
        plot_rq1_baseline_vs_skill_violin.main()
        plot_skill_design_loop.main()
        plot_key_differences_between_skills.main()
    finally:
        plt.savefig = _orig_savefig

    expected = {os.path.join(sub, stem) if sub else stem for stem, sub in WANTED.items()}
    missing = expected - set(_exported)
    if missing:
        raise SystemExit(f"ERROR: expected figures were never rendered: {sorted(missing)}")

    print(f"\nExported {len(_exported)} figures to {OUT_DIR}")
    for name in sorted(_exported):
        formats = f"{name}.pdf" if os.path.dirname(name) else f"{name}.pdf / {name}.png"
        print(f"  - {formats}")


if __name__ == "__main__":
    main()
