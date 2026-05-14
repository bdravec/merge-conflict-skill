"""
build_examples_pptx.py — populate conflict_1-6_examples.pptx with 6
mechanism-revealing cases for the 2026-05-22 review appendix (issue #49).

Layout (slide is 10.00 x 5.62 in, 16:9-ish, Uni Bern template):

  ┌─────────────────────────────────────────────────────────────────────────┐
  │ Conflict N: <tag>                                          [Title, 24pt]│
  │ <one-line tagline>                                       [tagline, 12pt]│
  │                                                                          │
  │  Merge Conflict   Apertus Solution    Qwen3 Solution    Ground Truth    │
  │  [code box]       [code box]          [code box]        [code box]       │
  │                   [annotation]        [annotation]                       │
  │                   [score table]       [score table]                      │
  │                   [caption]           [caption]                          │
  │                                                                          │
  └─────────────────────────────────────────────────────────────────────────┘

Tables show edit + winnowing under no-skill / v1 / v2 / v2.1 (sys condition).

The 6 cases, their solution-box mode, taglines, annotations, and captions
are pinned in CASES[] below.

Output: writes /home/baebs/thesis/review_mtgs/conflict_1-6_examples.pptx.

Usage:
    python scripts/build_examples_pptx.py
"""

import json
from collections import defaultdict
from pathlib import Path

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.oxml.ns import qn


REPO_ROOT     = Path(__file__).resolve().parent.parent
RESULTS_DIR   = REPO_ROOT / "scripts" / "results"
CONGRA_ROOT   = Path("/home/baebs/thesis/ConGra")
TEMPLATE_PATH = Path("/home/baebs/thesis/review_mtgs/conflict_1-6_examples.pptx")
OUT_PATH      = Path("/home/baebs/thesis/review_mtgs/conflict_1-6_examples.pptx")

PILOTS = {
    ("qwen3",   "v1"):   "pilot_results_qwen3_v2.jsonl",
    ("qwen3",   "v2"):   "pilot_results_qwen3_skill-v2.jsonl",
    ("qwen3",   "v2.1"): "pilot_results_qwen3_skill-v2.1.jsonl",
    ("apertus", "v1"):   "pilot_results_apertus_v2.jsonl",
    ("apertus", "v2"):   "pilot_results_apertus_skill-v2.jsonl",
    ("apertus", "v2.1"): "pilot_results_apertus_skill-v2.1.jsonl",
}

# Column geometry (inches).
COL = {
    "conflict": {"L": 0.20, "W": 1.80},
    "apertus":  {"L": 2.10, "W": 2.55},
    "qwen3":    {"L": 4.75, "W": 2.55},
    "gt":       {"L": 7.40, "W": 2.40},
}
# Row geometry (inches).
ROW = {
    "title":      {"T": 0.10, "H": 0.40},
    "tagline":    {"T": 0.55, "H": 0.30},
    "label":      {"T": 0.92, "H": 0.20},
    "code":       {"T": 1.15, "H": 2.50},   # ends at 3.65
    "annotation": {"T": 3.70, "H": 0.25},   # ends at 3.95
    "table":      {"T": 4.05, "H": 0.70},   # ends at 4.75
    "caption":    {"T": 4.85, "H": 0.65},   # ends at 5.50
}

# Cases. Each: case_id, conflict_idx, tag, tagline, solution mode, optional
# per-column annotations (col=apertus|qwen3), captions either (apertus, qwen3)
# pair or a single full-width string.
CASES = [
    {
        "case_id": "0xe63ff0ddae988357", "conflict_idx": 1,
        "tag": "pattern-teaching win",
        "tagline": "Apertus changes its pick under v2 — TF API → Keras API",
        "solution_mode": "stacked",
        "annotations": {
            "apertus": "v1 picks tf.placeholder (wrong) — v2/v2.1 pick K.placeholder (correct)",
            "qwen3":   "",
        },
        "caption_apertus": "v1 → v2 routes Apertus from TF API to Keras API — "
                           "the one clean pattern-routing change in the corpus.",
        "caption_qwen3":   "Qwen3 already at 0.836 without skill; v1 drops it, "
                           "v2 recovers, v2.1 regresses. Skill is "
                           "neutral-to-harmful for Qwen3 here.",
    },
    {
        "case_id": "0x96d20e6c", "conflict_idx": 1,
        "tag": "over-generation trimmed",
        "tagline": "v2 suppresses Apertus's over-generation",
        "solution_mode": "v21",
        "annotations": {
            "apertus": "v2 trims Apertus's over-generation",
            "qwen3":   "",
        },
        "caption_apertus": "v2 suppresses Apertus's over-generation. "
                           "Pattern routing stays wrong; metric improves "
                           "from v1 to v2.",
        "caption_qwen3":   "No skill helps Qwen3 — surrounding code would be "
                           "needed to solve this correctly; Qwen3 is good "
                           "in what it sees.",
    },
    {
        "case_id": "0xe4ff79aa", "conflict_idx": 1,
        "tag": "metric inversion",
        "tagline": "Identifier-divergence (Pick) — metric vs. correctness diverge",
        "solution_mode": "v21",
        "annotations": {
            "apertus": "Picks pool_size correctly",
            "qwen3":   "Picks poolsize (wrong identifier)",
        },
        "caption_full": "Apertus picks pool_size (correct); Qwen3 picks "
                        "poolsize (wrong) — but the metric ranks Qwen3 higher "
                        "because its output is shorter (length-ratio dominates "
                        "the denominator).",
    },
    {
        "case_id": "0x8e6579cb86af64a8", "conflict_idx": 1,
        "tag": "v2.1 splits Apertus and Qwen3",
        "tagline": "Same framing — opposite effects across models",
        "solution_mode": "stacked",
        "annotations": {
            "apertus": "+0.21 under v2.1 (climbs from 0.375)",
            "qwen3":   "−0.21 under v2.1 (falls from 0.672)",
        },
        "caption_apertus": "v2.1's stronger output-discipline framing lifts "
                           "Apertus from 0.375 (v2) to 0.584 (v2.1).",
        "caption_qwen3":   "Same framing pushes Qwen3 to a shorter do-nothing "
                           "output; v2.1 drops Qwen3 from 0.672 back to 0.466.",
    },
    {
        "case_id": "0x32d8c89b39c2860b", "conflict_idx": 1,
        "tag": "byte-identical no-op",
        "tagline": "Apertus emits the same code under all 9 conditions",
        "solution_mode": "v21",
        "annotations": {
            "apertus": "Identical output every time",
            "qwen3":   "Wobbles to 0.512 under v2",
        },
        "caption_full": "Apertus produces the same output under all 9 "
                        "conditions (3 pilots × no-skill / sys / user). The "
                        "skill is a true no-op for Apertus. Qwen3 has zero "
                        "such cases — its outputs vary even when scores are tied.",
    },
    {
        "case_id": "0xd9272c5e0e8f15ee", "conflict_idx": 1,
        "tag": "skill harms Apertus, ignored by Qwen3",
        "tagline": "Task ceiling — and skill actively misleads Apertus",
        "solution_mode": "v21",
        "annotations": {
            "apertus": "Skill loses 0.11 vs no-skill",
            "qwen3":   "Stuck at 0.19 across all versions",
        },
        "caption_full": "Ground truth requires file-level pattern synthesis "
                        "outside the conflict region. No single-conflict "
                        "skill can recover this; on Apertus the skill actively "
                        "misleads (no-skill 0.289 → skill 0.177).",
    },
]


# ── ConGra data loaders (inlined from pilot.py) ───────────────────────────────
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
    if short_id in index:
        return short_id
    matches = [k for k in index if k.startswith(short_id)]
    if len(matches) == 1:
        return matches[0]
    raise KeyError(f"Cannot resolve case_id {short_id!r}: {len(matches)} matches")


def load_pilots():
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


def score_for(pilots, model, version, case_key):
    """Returns (edit, winnowing) for skill-vX-sys, or no-skill if version='no-skill'."""
    cond = "no-skill" if version == "no-skill" else f"skill-{version}-sys"
    # no-skill is identical across the 3 pilots; pick from v2.
    pilot_key = "v2" if version == "no-skill" else version
    rec = pilots[(model, pilot_key)].get(case_key, {}).get(cond)
    if not rec or rec.get("error"):
        return None, None
    m = rec.get("metrics", {})
    return m.get("edit"), m.get("winnowing")


def render_solution(pilots, model, case_key, mode):
    versions = ("v1", "v2", "v2.1")
    by_version = {}
    for v in versions:
        rec = pilots[(model, v)].get(case_key, {}).get(f"skill-{v}-sys")
        if rec and not rec.get("error"):
            by_version[v] = rec.get("resolution", "") or ""
        else:
            by_version[v] = ""
    if mode == "stacked":
        parts = []
        for v in versions:
            txt = by_version[v].strip() or "(empty)"
            parts.append(f"[{v}]\n{txt}")
        return "\n\n".join(parts)
    return by_version["v2.1"].strip() or "(empty)"


# ── Shape primitives ──────────────────────────────────────────────────────────
def add_textbox(slide, L, T, W, H, text, *,
                font_pt=10, bold=False, align=None, anchor=MSO_ANCHOR.TOP,
                color=None, font_name=None):
    """Add a textbox with a single paragraph styled uniformly."""
    box = slide.shapes.add_textbox(Inches(L), Inches(T), Inches(W), Inches(H))
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left   = Inches(0.05)
    tf.margin_right  = Inches(0.05)
    tf.margin_top    = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    # Use the first paragraph that text_frame.text creates, but support
    # multi-line content by splitting on \n.
    lines = text.split("\n") if text else [""]
    p = tf.paragraphs[0]
    p.text = lines[0]
    for extra in lines[1:]:
        new_p = tf.add_paragraph()
        new_p.text = extra
    for para in tf.paragraphs:
        if align is not None:
            para.alignment = align
        for run in para.runs:
            run.font.size = Pt(font_pt)
            run.font.bold = bold
            if font_name:
                run.font.name = font_name
            if color is not None:
                run.font.color.rgb = color
    return box


def add_score_table(slide, L, T, W, H, model_label, scores):
    """5 cols x 3 rows. scores = dict edit/win across {no-skill,v1,v2,v2.1}."""
    cols, rows = 5, 3
    tbl_shape = slide.shapes.add_table(rows, cols, Inches(L), Inches(T), Inches(W), Inches(H))
    tbl = tbl_shape.table

    # Header row
    headers = [model_label, "no-skill", "v1", "v2", "v2.1"]
    for c, h in enumerate(headers):
        cell = tbl.cell(0, c)
        cell.text = h
        for para in cell.text_frame.paragraphs:
            para.alignment = PP_ALIGN.CENTER
            for run in para.runs:
                run.font.size = Pt(9)
                run.font.bold = True

    # Edit Similarity row
    tbl.cell(1, 0).text = "Edit Similarity"
    tbl.cell(1, 1).text = fmt_score(scores["no-skill"][0])
    tbl.cell(1, 2).text = fmt_score(scores["v1"][0])
    tbl.cell(1, 3).text = fmt_score(scores["v2"][0])
    tbl.cell(1, 4).text = fmt_score(scores["v2.1"][0])

    # Winnowing row
    tbl.cell(2, 0).text = "Winnowing"
    tbl.cell(2, 1).text = fmt_score(scores["no-skill"][1])
    tbl.cell(2, 2).text = fmt_score(scores["v1"][1])
    tbl.cell(2, 3).text = fmt_score(scores["v2"][1])
    tbl.cell(2, 4).text = fmt_score(scores["v2.1"][1])

    # Uniform font for data rows
    for r_idx in (1, 2):
        for c_idx in range(cols):
            cell = tbl.cell(r_idx, c_idx)
            for para in cell.text_frame.paragraphs:
                para.alignment = PP_ALIGN.CENTER if c_idx > 0 else PP_ALIGN.LEFT
                for run in para.runs:
                    run.font.size = Pt(9)
    return tbl_shape


# ── Slide clearing ────────────────────────────────────────────────────────────
def clear_all_slides(prs):
    """Remove every slide so we can rebuild from scratch."""
    sldIdLst = prs.slides._sldIdLst
    pres_part = prs.part
    for sld_id in list(sldIdLst):
        rId = sld_id.get(qn("r:id"))
        sldIdLst.remove(sld_id)
        pres_part.rels.pop(rId)


def find_layout_by_name(prs, name):
    for master in prs.slide_masters:
        for layout in master.slide_layouts:
            if layout.name == name:
                return layout
    raise KeyError(f"Layout {name!r} not found.")


def remove_layout_placeholders(slide):
    """Strip layout-derived placeholder shapes from a freshly added slide."""
    for shape in list(slide.placeholders):
        sp = shape._element
        sp.getparent().remove(sp)


def build_slide(prs, layout, idx, case, pilots):
    slide = prs.slides.add_slide(layout)
    remove_layout_placeholders(slide)

    case_key = (case["case_id"], case["conflict_idx"])

    # Title chip
    add_textbox(
        slide, 0.20, ROW["title"]["T"], 9.60, ROW["title"]["H"],
        f"Conflict {idx}: {case['tag']}",
        font_pt=24, bold=True,
    )

    # Tagline
    add_textbox(
        slide, 0.20, ROW["tagline"]["T"], 9.60, ROW["tagline"]["H"],
        case["tagline"],
        font_pt=12,
    )

    # Column labels
    for key, label in [("conflict", "Merge Conflict"),
                       ("apertus",  "Apertus Solution"),
                       ("qwen3",    "Qwen3 Solution"),
                       ("gt",       "Ground Truth")]:
        add_textbox(
            slide, COL[key]["L"], ROW["label"]["T"], COL[key]["W"], ROW["label"]["H"],
            label,
            font_pt=8, bold=True,
        )

    # Code boxes
    apertus_text = render_solution(pilots, "apertus", case_key, case["solution_mode"])
    qwen3_text   = render_solution(pilots, "qwen3",   case_key, case["solution_mode"])
    for key, content in [("conflict", case["conflict_text"]),
                         ("apertus",  apertus_text),
                         ("qwen3",    qwen3_text),
                         ("gt",       case["ground_truth"])]:
        add_textbox(
            slide, COL[key]["L"], ROW["code"]["T"], COL[key]["W"], ROW["code"]["H"],
            content,
            font_pt=7, font_name="Consolas",
        )

    # Annotations (between code and table) — apertus + qwen3 columns
    for key in ("apertus", "qwen3"):
        ann = (case.get("annotations") or {}).get(key, "")
        if ann:
            add_textbox(
                slide, COL[key]["L"], ROW["annotation"]["T"], COL[key]["W"], ROW["annotation"]["H"],
                ann,
                font_pt=9, bold=True, align=PP_ALIGN.CENTER, color=RGBColor(0xB2, 0x18, 0x2B),
            )

    # Score tables (5 cols × 3 rows: header + edit + winnowing)
    a_scores = {v: score_for(pilots, "apertus", v, case_key)
                for v in ("no-skill", "v1", "v2", "v2.1")}
    q_scores = {v: score_for(pilots, "qwen3", v, case_key)
                for v in ("no-skill", "v1", "v2", "v2.1")}
    add_score_table(slide, COL["apertus"]["L"], ROW["table"]["T"],
                    COL["apertus"]["W"], ROW["table"]["H"],
                    "Scores", a_scores)
    add_score_table(slide, COL["qwen3"]["L"], ROW["table"]["T"],
                    COL["qwen3"]["W"], ROW["table"]["H"],
                    "Scores", q_scores)

    # Captions
    if "caption_full" in case:
        add_textbox(
            slide, 0.20, ROW["caption"]["T"], 9.60, ROW["caption"]["H"],
            case["caption_full"],
            font_pt=10,
        )
    else:
        add_textbox(
            slide, COL["apertus"]["L"], ROW["caption"]["T"],
            COL["apertus"]["W"], ROW["caption"]["H"],
            case.get("caption_apertus", ""),
            font_pt=10,
        )
        add_textbox(
            slide, COL["qwen3"]["L"], ROW["caption"]["T"],
            COL["qwen3"]["W"], ROW["caption"]["H"],
            case.get("caption_qwen3", ""),
            font_pt=10,
        )

    return slide


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    print("Loading case index...")
    case_idx = build_case_index()
    print(f"  {len(case_idx)} python cases indexed")

    print("Loading pilot JSONLs...")
    pilots = load_pilots()

    print("\nResolving cases:")
    resolved = []
    for spec in CASES:
        cid = normalize_case_id(spec["case_id"], case_idx)
        bucket, src_rel, _ = case_idx[cid]
        source_path = str(CONGRA_ROOT / "data" / "raw_datasets" / src_rel)
        hash_file   = str(CONGRA_ROOT / "data" / "congra_tiny_datasets"
                          / "python" / bucket / cid)
        conflict_text, gt = load_conflict_and_answer(
            source_path, hash_file, spec["conflict_idx"], n=5,
        )
        resolved.append({**spec, "case_id": cid, "bucket": bucket,
                         "conflict_text": conflict_text, "ground_truth": gt})
        print(f"  {cid[:18]}... bucket={bucket:>16} "
              f"conflict={len(conflict_text.splitlines())}L "
              f"GT={len(gt.splitlines())}L")

    print(f"\nOpening template: {TEMPLATE_PATH}")
    prs = Presentation(str(TEMPLATE_PATH))

    print("Clearing existing slides...")
    clear_all_slides(prs)

    layout = find_layout_by_name(prs, "3: Titel-Folie ohne Bild")
    print(f"Using layout: {layout.name}")

    for i, case in enumerate(resolved, start=1):
        build_slide(prs, layout, i, case, pilots)
        print(f"  slide {i}: {case['case_id'][:14]}... '{case['tag']}' built")

    print(f"\nSaving: {OUT_PATH}")
    prs.save(str(OUT_PATH))
    print("Done.")


if __name__ == "__main__":
    main()
