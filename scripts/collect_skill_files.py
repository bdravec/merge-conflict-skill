"""
collect_skill_files.py — gather the five SKILL.md files for the thesis appendix (#118)

The appendix prints all five verbatim, but they live in two repos: the three
merge-conflict versions here, and the SALLM and SWE-bench Lite skills in the
sibling swe-skills-benchmarks checkout. This copies them into one folder so the
appendix is a single upload, and renames them on the way, since five files all
called SKILL.md cannot share a directory.

Run it again whenever a skill file changes; the appendix pulls the copies in with
\\lstinputlisting, so the thesis never holds a pasted copy that can drift.

Run from the repo root:
    python3 scripts/collect_skill_files.py
"""

import os
import shutil

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT  = os.path.dirname(SCRIPT_DIR)
SIBLING    = os.path.join(os.path.dirname(REPO_ROOT), "swe-skills-benchmarks")
OUT_DIR    = os.path.join(REPO_ROOT, "results_overleaf_figures", "appendix", "skills")

# (source repo, skill directory) -> copied as <skill directory>.md
SOURCES = [
    (REPO_ROOT, "merge-conflict-resolve-v1"),
    (REPO_ROOT, "merge-conflict-resolve-v2"),
    (REPO_ROOT, "merge-conflict-resolve-v2.1"),
    (SIBLING,   "secure-coding-v1"),
    (SIBLING,   "swebench-repair-v1"),
]


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    missing = []
    for repo, skill in SOURCES:
        src = os.path.join(repo, "skills", skill, "SKILL.md")
        if not os.path.exists(src):
            missing.append(src)
            continue
        dst = os.path.join(OUT_DIR, f"{skill}.md")
        shutil.copyfile(src, dst)
        with open(dst, encoding="utf-8") as f:
            text = f.read()
        longest = max((len(line) for line in text.split("\n")), default=0)
        print(f"  {skill + '.md':<36} {len(text.splitlines()):>4} lines "
              f"{len(text.split()):>5} words  longest line {longest}")

    if missing:
        raise SystemExit(
            "ERROR: could not find:\n  " + "\n  ".join(missing) +
            f"\n\nThe SALLM and SWE-bench Lite skills come from {SIBLING}; "
            "check that the sibling repo is checked out next to this one.")

    print(f"\nCollected {len(SOURCES)} skill files into {OUT_DIR}")


if __name__ == "__main__":
    main()
