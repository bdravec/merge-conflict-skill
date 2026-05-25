"""
build_bucket_examples.py — Generate per-bucket worked-example .md files (#70)

For each of the 7 ConGra buckets, picks 2 "worked" + 2 "failed" cases (definitions
below), loads the conflict + ground truth + 6 model outputs per case, and renders
a Markdown file with one HTML table per model (Apertus-8B + Qwen3-8B). Each table
has 5 columns (Conflict | v1-sys | v2-sys | v2.1-sys | Ground truth) and 3 rows
(header / code / per-cell auto-label).

Selection criteria:
  - worked: max score across all 6 (model × version) conditions > 0.8
  - failed: max score across all 6 (model × version) conditions ≤ 0.10
  - Within each pool, prefer cases with diverse outputs across the 6 conditions.

Pinned cases: certain (bucket, case_id) pairs are forced into the worked list to
preserve curated examples with hand-written observations. The pinned case is
emitted first; auto-labels are still emitted but can be patched by hand later.

Run from repo root:
    python scripts/build_bucket_examples.py
"""

import json
import os
from collections import defaultdict


REPO_ROOT    = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_DIR  = os.path.join(REPO_ROOT, "scripts", "results")
EXAMPLES_DIR = os.path.join(REPO_ROOT, "examples")
CONGRA_ROOT  = os.path.abspath(os.path.join(REPO_ROOT, "..", "ConGra"))

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

BUCKET_DESCRIPTIONS = {
    "func": (
        "Changes that **alter program behaviour** — added/removed control flow, "
        "asserts, branches. Short ground truths in this bucket make the "
        "length-mismatch penalty bite hard."
    ),
    "sytx": (
        "**Syntactically-different code statements** without changing behaviour: "
        "variable renames, restructured imports, reorganised signatures."
    ),
    "text": (
        "Changes in **textual content** — docstrings, comments, string literals. "
        "Not code logic."
    ),
    "sytx+func": (
        "Combined: code structure differs AND behaviour differs."
    ),
    "text+func": (
        "Combined: textual content differs AND behaviour differs."
    ),
    "text+sytx": (
        "Combined: textual content differs AND code structure differs."
    ),
    "text+sytx+func": (
        "All three aspects differ in the same conflict region — the hardest "
        "bucket. Distributions are bimodal (peaks near 0 and near 1)."
    ),
}

# Pinned worked cases per bucket. These are always included (and listed first).
# Used to preserve hand-written observations on selected cases.
PINNED_WORKED = {
    "func": ["0xc99534a64262c8c6"],
}

RUNS = [
    ("Apertus-8B", "v1-sys",   "pilot_results_apertus_v1_python_tiny.jsonl",   "skill-v1-sys"),
    ("Apertus-8B", "v2-sys",   "pilot_results_apertus_v2_python_tiny.jsonl",   "skill-v2-sys"),
    ("Apertus-8B", "v2.1-sys", "pilot_results_apertus_v2.1_python_tiny.jsonl", "skill-v2.1-sys"),
    ("Qwen3-8B",   "v1-sys",   "pilot_results_qwen3_v1_python_tiny.jsonl",     "skill-v1-sys"),
    ("Qwen3-8B",   "v2-sys",   "pilot_results_qwen3_v2_python_tiny.jsonl",     "skill-v2-sys"),
    ("Qwen3-8B",   "v2.1-sys", "pilot_results_qwen3_v2.1_python_tiny.jsonl",   "skill-v2.1-sys"),
]


def load_all_for_bucket(bucket: str):
    """Returns: {case_id: {(model, version): (resolution, edit, winn, max, empty), "_gt": str}}"""
    data = defaultdict(dict)
    for model, version, fname, cond in RUNS:
        path = os.path.join(RESULTS_DIR, fname)
        with open(path) as f:
            for line in f:
                r = json.loads(line)
                if r.get("bucket") != bucket or r.get("error") is not None:
                    continue
                if r.get("condition") != cond:
                    continue
                m = r["metrics"]
                if m.get("empty"):
                    e, w, score, empty = 0.0, 0.0, 0.0, True
                else:
                    e, w = m.get("edit"), m.get("winnowing")
                    if e is None or w is None:
                        continue
                    score, empty = max(e, w), False
                cid = r["case_id"]
                data[cid][(model, version)] = (r["resolution"], e, w, score, empty)
                data[cid]["_gt"] = r["ground_truth"]
    return data


def select_cases(data: dict, bucket: str) -> tuple[list[str], list[str]]:
    pinned = PINNED_WORKED.get(bucket, [])

    worked_pool, failed_pool = [], []
    for cid, conds in data.items():
        scores = [conds[(m, v)][3] for m, v, _, _ in RUNS if (m, v) in conds]
        if len(scores) != 6:
            continue
        outs = {conds[(m, v)][0] for m, v, _, _ in RUNS if (m, v) in conds}
        diversity = len(outs)
        max_s = max(scores)
        gt_len = len(conds["_gt"])
        if max_s > 0.8:
            worked_pool.append((cid, max_s, diversity, gt_len))
        if max_s <= 0.10:
            failed_pool.append((cid, max_s, diversity, gt_len))

    # worked: prefer diverse outputs (more interesting cross-version story), high score
    worked_pool.sort(key=lambda x: (-x[2], -x[1]))
    # failed: prefer diverse outputs; pick one short-GT and one longer-GT for variety
    failed_pool.sort(key=lambda x: (-x[2], x[1]))

    worked = list(pinned)
    for cid, *_ in worked_pool:
        if cid in worked:
            continue
        if len(worked) >= 2:
            break
        worked.append(cid)

    # failed: pick one short, one longer GT, both with diversity ≥ 2 if possible
    failed = []
    short_pool = [x for x in failed_pool if x[3] < 100]
    long_pool  = [x for x in failed_pool if x[3] >= 100]
    if short_pool:
        failed.append(short_pool[0][0])
    if long_pool:
        failed.append(long_pool[0][0])
    # Top up to 2 if either was empty
    for cid, *_ in failed_pool:
        if len(failed) >= 2:
            break
        if cid not in failed:
            failed.append(cid)

    return worked[:2], failed[:2]


def load_conflict_and_gt(case_id: str, bucket: str) -> tuple[str, str] | tuple[None, None]:
    meta = os.path.join(CONGRA_ROOT, "data", "congra_tiny_datasets", "python", bucket, "meta_list.txt")
    if not os.path.exists(meta):
        return None, None
    with open(meta) as f:
        for line in f:
            line = line.strip()
            if not line or case_id not in line:
                continue
            parts = line.split(": ")
            if len(parts) != 3:
                continue
            source_path, hash_idx, k = parts
            k = int(k)
            region_path = os.path.join(
                CONGRA_ROOT, "data", "raw_datasets",
                source_path.replace("merged_without_base", "regions") + ".region"
            )
            try:
                with open(region_path) as rf:
                    regions = [eval(l.strip()) for l in rf if l.strip() and "#" not in l]
                region = regions[k - 1]
                hash_full = os.path.join(
                    CONGRA_ROOT, "data", "congra_tiny_datasets", "python", bucket, hash_idx
                )
                with open(hash_full, encoding="utf-8", errors="ignore") as hf:
                    lines = hf.read().split("\n")
                conflict = "\n".join(lines[region[0] - 1:region[1]])
                resolved_path = os.path.join(
                    CONGRA_ROOT, "data", "raw_datasets",
                    source_path.replace("merged_without_base", "resolved")
                )
                with open(resolved_path, encoding="utf-8", errors="ignore") as rf:
                    rlines = rf.read().split("\n")
                gt = "\n".join(rlines[region[2] - 1:region[3]])
                return conflict, gt
            except (FileNotFoundError, IndexError, SyntaxError):
                return None, None
    return None, None


def parse_conflict_sides(conflict: str) -> tuple[str, str]:
    if not conflict:
        return "", ""
    a_lines, b_lines, state = [], [], None
    for line in conflict.split("\n"):
        if line.startswith("<<<<<<<"):
            state = "a"
        elif line.startswith("======="):
            state = "b"
        elif line.startswith(">>>>>>>"):
            state = None
        elif state == "a":
            a_lines.append(line)
        elif state == "b":
            b_lines.append(line)
    return "\n".join(a_lines).strip(), "\n".join(b_lines).strip()


def classify_pattern(resolution: str, side_a: str, side_b: str) -> str:
    if not resolution or not resolution.strip():
        return "empty"
    if any(m in resolution for m in ["<<<<<<<", "=======", ">>>>>>>"]):
        return "marker-echo"
    r = resolution.strip()
    has_a = bool(side_a) and side_a in r
    has_b = bool(side_b) and side_b in r
    if has_a and has_b:
        return "combine"
    if has_a:
        return "pick-a"
    if has_b:
        return "pick-b"
    return "custom"


def cell_label(resolution: str, score: float, empty: bool,
               side_a: str, side_b: str, gt: str,
               prev_resolution: str | None) -> str:
    if empty or not resolution.strip():
        return f"**empty** &nbsp;·&nbsp; max=**{score:.3f}**"
    pattern = classify_pattern(resolution, side_a, side_b)
    parts = [f"**{pattern}**"]
    gt_len = max(1, len(gt))
    ratio = len(resolution) / gt_len
    if ratio > 1.5:
        parts.append(f"{ratio:.1f}× over-gen")
    elif ratio < 0.5:
        parts.append(f"{ratio:.1f}× under-gen")
    if prev_resolution is not None and resolution == prev_resolution:
        parts.append("= prev version")
    parts.append(f"max=**{score:.3f}**")
    return " &nbsp;·&nbsp; ".join(parts)


def render_table(model: str, case_id: str, conds: dict, conflict: str, gt: str) -> str:
    side_a, side_b = parse_conflict_sides(conflict)
    versions = ["v1-sys", "v2-sys", "v2.1-sys"]
    scores = {v: conds[(model, v)][3] for v in versions}

    out = []
    out.append(f"#### {model}\n")
    out.append('<table>')
    out.append('<tr>')
    out.append('<th align="left">Conflict</th>')
    for v in versions:
        out.append(f'<th align="left">{v} (max={scores[v]:.3f})</th>')
    out.append('<th align="left">Ground truth</th>')
    out.append('</tr>')

    out.append('<tr>')
    out.append(f'<td valign="top">\n\n```python\n{conflict}\n```\n\n</td>')
    for v in versions:
        res = conds[(model, v)][0]
        out.append(f'<td valign="top">\n\n```python\n{res}\n```\n\n</td>')
    out.append(f'<td valign="top">\n\n```python\n{gt}\n```\n\n</td>')
    out.append('</tr>')

    out.append('<tr>')
    out.append('<td valign="top">&mdash;</td>')
    prev = None
    for v in versions:
        res, _e, _w, s, empty = conds[(model, v)]
        out.append(f'<td valign="top">\n\n{cell_label(res, s, empty, side_a, side_b, gt, prev)}\n\n</td>')
        prev = res
    out.append('<td valign="top">&mdash;</td>')
    out.append('</tr>')

    out.append('</table>\n')
    return "\n".join(out)


def render_case(case_id: str, bucket: str, conds: dict) -> str:
    gt = conds["_gt"]
    conflict, _ = load_conflict_and_gt(case_id, bucket)
    if conflict is None:
        return f"### Case `{case_id}`\n\n_Conflict region not found in `{bucket}` meta_list (skipped)._\n"
    out = [f"### Case `{case_id}`\n"]
    for model in ["Apertus-8B", "Qwen3-8B"]:
        out.append(render_table(model, case_id, conds, conflict, gt))
    return "\n".join(out)


def render_bucket(bucket: str, data: dict, worked: list[str], failed: list[str]) -> str:
    out = [f"# `{bucket}` bucket — worked examples\n"]
    out.append(BUCKET_DESCRIPTIONS[bucket] + "\n")
    out.append("Auto-label vocabulary: **pick-a / pick-b / combine / custom / empty / "
               "marker-echo** describe what shape the model output is. Length ratios "
               "flag over- or under-generation vs the ground truth.\n")
    out.append("---\n")
    out.append("## Both models solve (at least one skill version)\n")
    if not worked:
        out.append("_No case in this bucket has any (model × version) cell with max > 0.8._\n")
    for cid in worked:
        out.append(render_case(cid, bucket, data[cid]))
        out.append("---\n")
    out.append("## Both models fail\n")
    if not failed:
        out.append("_No case in this bucket has all 6 (model × version) cells at max ≤ 0.10._\n")
    for cid in failed:
        out.append(render_case(cid, bucket, data[cid]))
        out.append("---\n")
    return "\n".join(out)


def main():
    os.makedirs(EXAMPLES_DIR, exist_ok=True)
    for bucket in BUCKETS:
        data = load_all_for_bucket(bucket)
        worked, failed = select_cases(data, bucket)
        md = render_bucket(bucket, data, worked, failed)
        path = os.path.join(EXAMPLES_DIR, f"{bucket}.md")
        with open(path, "w") as f:
            f.write(md)
        print(f"{bucket}: worked={worked} failed={failed} -> {path}")


if __name__ == "__main__":
    main()
