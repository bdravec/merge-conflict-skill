"""
build_examples_pptx.py — populate conflict_1-6_examples.pptx with 6
mechanism-revealing cases for the 2026-05-22 review appendix (issue #49).

For each case the slide shows:
  - Conflict text  (raw <<<< a / ==== / >>>>>> b block)
  - Apertus solution (default: v2.1 output; overridable to stacked v1/v2/v2.1)
  - Qwen3 solution   (default: v2.1 output; overridable to stacked v1/v2/v2.1)
  - Ground truth resolution
  - Apertus score table: edit + winnowing across v1/v2/v2.1 (sys condition)
  - Qwen3   score table: edit + winnowing across v1/v2/v2.1 (sys condition)

Score column = `skill-vX-sys` condition (the deck convention).

Reads:
  - The template at conflict_1-6_examples.pptx (one slide; cloned 6x).
  - meta_list.txt files across all python buckets to find each case's bucket
    and source_path.
  - Pilot JSONLs in scripts/results/ to pull per-case resolutions + scores.
  - ConGra raw_datasets + congra_tiny_datasets to load conflict text + GT.

Writes the populated deck back to the same path.

Usage:
    python scripts/build_examples_pptx.py
"""

import os
import json
from copy import deepcopy
from collections import defaultdict
from pathlib import Path

from pptx import Presentation
from pptx.util import Pt
from pptx.oxml.ns import qn


REPO_ROOT       = Path(__file__).resolve().parent.parent
RESULTS_DIR     = REPO_ROOT / "scripts" / "results"
CONGRA_ROOT     = Path("/home/baebs/thesis/ConGra")
TEMPLATE_PATH   = Path("/home/baebs/thesis/review_mtgs/conflict_1-6_examples.pptx")

# JSONLs that hold the 6 (model x version) pilots.
PILOTS = {
    ("qwen3",   "v1"):   "pilot_results_qwen3_v2.jsonl",
    ("qwen3",   "v2"):   "pilot_results_qwen3_skill-v2.jsonl",
    ("qwen3",   "v2.1"): "pilot_results_qwen3_skill-v2.1.jsonl",
    ("apertus", "v1"):   "pilot_results_apertus_v2.jsonl",
    ("apertus", "v2"):   "pilot_results_apertus_skill-v2.jsonl",
    ("apertus", "v2.1"): "pilot_results_apertus_skill-v2.1.jsonl",
}

# 6 cases. Each entry: case_id (hex with 0x), conflict_idx, the slide title
# tagline, the pattern-description text shown below the title, and which
# solution-box format to use ("v21" | "stacked").
CASES = [
    {
        "case_id": "0xe63ff0ddae988357", "conflict_idx": 1,
        "tag": "pattern-teaching win",
        "pattern": "Pick. Apertus changes its pick under v2 — the one clean "
                   "pattern-routing change observed in the v2 corpus.",
        "solution_mode": "stacked",
    },
    {
        "case_id": "0x96d20e6c", "conflict_idx": 1,  # NOTE: hex prefix; full id is longer — will be expanded below.
        "tag": "over-generation trimmed",
        "pattern": "Pick. v2 suppresses Apertus's over-generation. Pattern "
                   "routing stays wrong, but the metric improves.",
        "solution_mode": "v21",
    },
    {
        "case_id": "0xe4ff79aa", "conflict_idx": 1,
        "tag": "metric inversion",
        "pattern": "Identifier-divergence (Pick). Apertus picks pool_size "
                   "(correct); Qwen3 picks poolsize (wrong) — but the metric "
                   "ranks Qwen3 higher because its output is shorter.",
        "solution_mode": "v21",
    },
    {
        "case_id": "0x8e6579cb86af64a8", "conflict_idx": 1,
        "tag": "v2.1 regression",
        "pattern": "Qwen3 v2 → v2.1: Δedit = −0.21. v2.1's stronger "
                   "output-discipline framing pushes Qwen3 toward a shorter "
                   "do-nothing output.",
        "solution_mode": "stacked",
    },
    {
        "case_id": "0x32d8c89b39c2860b", "conflict_idx": 1,
        "tag": "byte-identical no-op",
        "pattern": "Apertus produces the same output under all 9 conditions "
                   "(3 pilots × no-skill/sys/user). The skill is a true no-op "
                   "on this case. Qwen3 has zero cases that achieve this.",
        "solution_mode": "v21",
    },
    {
        "case_id": "0xd9272c5e0e8f15ee", "conflict_idx": 1,
        "tag": "task ceiling",
        "pattern": "Custom. Ground truth requires file-level pattern "
                   "synthesis that lives outside the conflict region; no "
                   "single-conflict skill can recover this.",
        "solution_mode": "v21",
    },
]


# ── Inlined from pilot.py: load_conflict_and_answer ───────────────────────────
def load_conflict_and_answer(source_path, file_path, k, n=5):
    region_path = source_path.replace("merged_without_base", "regions") + ".region"
    regions = []
    with open(region_path, "r") as f:
        for line in f:
            if "#" in line:
                continue
            line = line.strip()
            if line:
                regions.append(eval(line))
    region = regions[k - 1]

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().split("\n")
    start, end = region[0] - 1, region[1]
    conflict_text = "\n".join(lines[start:end])

    resolved_path = source_path.replace("merged_without_base", "resolved").replace(
        "regions", "resolved"
    )
    with open(resolved_path, "r", encoding="utf-8", errors="ignore") as f:
        rlines = f.read().split("\n")
    rstart, rend = region[2] - 1, region[3]
    resolved_text = "\n".join(rlines[max(0, rstart):rend])
    return conflict_text, resolved_text


def build_case_index():
    """Scan meta_list.txt across all python buckets; return {case_id: (bucket, source_path, conflict_idx)}."""
    lang_root = CONGRA_ROOT / "data" / "congra_tiny_datasets" / "python"
    idx = {}
    for bucket_dir in sorted(lang_root.iterdir()):
        if not bucket_dir.is_dir():
            continue
        meta = bucket_dir / "meta_list.txt"
        if not meta.is_file():
            continue
        for line in meta.read_text().splitlines():
            line = line.strip()
            if not line or line.count(": ") != 2:
                continue
            source_path, hash_idx, conflict_idx = line.split(": ")
            idx[hash_idx] = (bucket_dir.name, source_path, int(conflict_idx))
    return idx


def normalize_case_id(short_id, index):
    """Some CASES entries use shortened case_ids; expand from the index."""
    if short_id in index:
        return short_id
    matches = [k for k in index if k.startswith(short_id)]
    if len(matches) == 1:
        return matches[0]
    raise KeyError(f"Cannot resolve case_id {short_id!r}: {len(matches)} matches")


def load_pilots():
    """Returns {(model, version): {(case_id, conflict_idx): {condition: record}}}."""
    out = {}
    for key, fname in PILOTS.items():
        path = RESULTS_DIR / fname
        by_case = defaultdict(dict)
        for line in open(path):
            r = json.loads(line)
            by_case[(r["case_id"], r["conflict_idx"])][r["condition"]] = r
        out[key] = by_case
    return out


def fmt_score(x):
    return "—" if x is None else f"{x:.3f}"


# ── Slide manipulation ────────────────────────────────────────────────────────
def duplicate_slide(prs, src_slide):
    """Clone src_slide into prs and return the new slide."""
    layout = src_slide.slide_layout
    new_slide = prs.slides.add_slide(layout)
    # Remove the default layout-derived shapes so we start from a blank slide
    for shape in list(new_slide.shapes):
        sp = shape._element
        sp.getparent().remove(sp)
    # Clone each shape from the source
    for shape in src_slide.shapes:
        new_el = deepcopy(shape._element)
        new_slide.shapes._spTree.insert_element_before(new_el, "p:extLst")
    return new_slide


def find_shape(slide, name):
    for shape in slide.shapes:
        if shape.name == name:
            return shape
    return None


def set_text(shape, text, font_size_pt=None):
    """Replace text_frame content; optionally set a uniform font size."""
    tf = shape.text_frame
    tf.text = text
    if font_size_pt is not None:
        for para in tf.paragraphs:
            for run in para.runs:
                run.font.size = Pt(font_size_pt)


def set_table_scores(shape, edit_v1, edit_v2, edit_v21, win_v1, win_v2, win_v21):
    """Fill the 4-col table: row 1 = Edit Similarity v1/v2/v2.1; row 2 = Winnowing v1/v2/v2.1."""
    tbl = shape.table
    tbl.cell(1, 1).text = fmt_score(edit_v1)
    tbl.cell(1, 2).text = fmt_score(edit_v2)
    tbl.cell(1, 3).text = fmt_score(edit_v21)
    tbl.cell(2, 1).text = fmt_score(win_v1)
    tbl.cell(2, 2).text = fmt_score(win_v2)
    tbl.cell(2, 3).text = fmt_score(win_v21)


def render_solution(pilots, model, case_key, mode):
    """Return the solution text to place in the model's solution box."""
    versions = ("v1", "v2", "v2.1")
    by_version = {}
    for v in versions:
        rec = pilots[(model, v)].get(case_key, {}).get(f"skill-{v}-sys")
        if rec and not rec.get("error"):
            by_version[v] = rec.get("resolution", "")
        else:
            by_version[v] = ""

    if mode == "stacked":
        parts = []
        for v in versions:
            txt = by_version[v].strip() or "(empty)"
            parts.append(f"[{v}]\n{txt}")
        return "\n\n".join(parts)
    # default: v2.1 alone
    return by_version["v2.1"].strip() or "(empty)"


def score_for(pilots, model, version, case_key):
    """Return (edit, winnowing) for skill-vX-sys."""
    rec = pilots[(model, version)].get(case_key, {}).get(f"skill-{version}-sys")
    if not rec or rec.get("error"):
        return None, None
    m = rec.get("metrics", {})
    return m.get("edit"), m.get("winnowing")


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("Loading case index...")
    case_idx = build_case_index()
    print(f"  {len(case_idx)} python cases indexed")

    print("Loading pilot JSONLs...")
    pilots = load_pilots()

    # Resolve short case_ids and look up conflict text + GT
    print("\nResolving cases:")
    resolved_cases = []
    for spec in CASES:
        cid = normalize_case_id(spec["case_id"], case_idx)
        bucket, src_rel, conflict_idx_from_meta = case_idx[cid]
        cidx = spec["conflict_idx"]
        if cidx != conflict_idx_from_meta:
            print(f"  WARN: case {cid} conflict_idx mismatch "
                  f"(spec={cidx}, meta={conflict_idx_from_meta}); using spec.")
        source_path = str(CONGRA_ROOT / "data" / "raw_datasets" / src_rel)
        hash_file   = str(CONGRA_ROOT / "data" / "congra_tiny_datasets" / "python" / bucket / cid)
        conflict_text, gt = load_conflict_and_answer(source_path, hash_file, cidx, n=5)
        resolved_cases.append({**spec, "case_id": cid, "bucket": bucket,
                                "conflict_text": conflict_text, "ground_truth": gt})
        print(f"  {cid[:18]}... bucket={bucket:>16} "
              f"conflict={len(conflict_text.splitlines())}L GT={len(gt.splitlines())}L")

    # Open template, clone its single slide N-1 times so we have N slides.
    print(f"\nOpening template: {TEMPLATE_PATH}")
    prs = Presentation(str(TEMPLATE_PATH))
    template_slide = prs.slides[0]
    while len(prs.slides) < len(resolved_cases):
        duplicate_slide(prs, template_slide)
    print(f"  template now has {len(prs.slides)} slides (expected {len(resolved_cases)})")

    # Populate slides
    for i, case in enumerate(resolved_cases, start=1):
        slide = prs.slides[i - 1]
        case_key = (case["case_id"], case["conflict_idx"])

        # Title
        title = find_shape(slide, "Title 7")
        if title is not None:
            set_text(title, f"Conflict {i}: {case['tag']}", font_size_pt=24)

        # Pattern description
        desc = find_shape(slide, "Text Placeholder 2")
        if desc is not None:
            set_text(desc, case["pattern"], font_size_pt=12)

        # Code boxes
        for shape_name, content in [
            ("TextBox 1",  case["conflict_text"]),
            ("TextBox 9",  render_solution(pilots, "apertus", case_key, case["solution_mode"])),
            ("TextBox 14", render_solution(pilots, "qwen3",   case_key, case["solution_mode"])),
            ("TextBox 21", case["ground_truth"]),
        ]:
            shape = find_shape(slide, shape_name)
            if shape is not None:
                set_text(shape, content, font_size_pt=7)

        # Score tables
        ae1, aw1 = score_for(pilots, "apertus", "v1",   case_key)
        ae2, aw2 = score_for(pilots, "apertus", "v2",   case_key)
        ae3, aw3 = score_for(pilots, "apertus", "v2.1", case_key)
        qe1, qw1 = score_for(pilots, "qwen3",   "v1",   case_key)
        qe2, qw2 = score_for(pilots, "qwen3",   "v2",   case_key)
        qe3, qw3 = score_for(pilots, "qwen3",   "v2.1", case_key)
        atbl = find_shape(slide, "Table 26")
        qtbl = find_shape(slide, "Table 27")
        if atbl is not None:
            set_table_scores(atbl, ae1, ae2, ae3, aw1, aw2, aw3)
        if qtbl is not None:
            set_table_scores(qtbl, qe1, qe2, qe3, qw1, qw2, qw3)

        print(f"  slide {i}: {case['case_id'][:14]}... '{case['tag']}' populated")

    print(f"\nSaving: {TEMPLATE_PATH}")
    prs.save(str(TEMPLATE_PATH))
    print("Done.")


if __name__ == "__main__":
    main()
