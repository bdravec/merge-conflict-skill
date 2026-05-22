"""Merge Qwen3 v1 python-tiny rerun JSONLs into one canonical file (closes #63).

The 2026-05-15 c=4 attempt produced clean rows for func/sytx/sytx+func, and a
partial text bucket (703/820 cases clean). text+func, text+sytx, and
text+sytx+func were 100% trashed by vLLM connection errors. Reruns of those
3 broken buckets plus a fresh rerun of text (refs #63) replace the trash; the
3 fully-clean buckets are reused from the 2026-05-15 raw file (TEMPERATURE=0,
so c=4 vs c=2 produces the same deterministic outputs).

Sources merge in declared order; rows from later sources never override earlier
ones (the bucket filters are disjoint, so dedupe is just a safety net).

Output writes the canonical filename; the 2026-05-15 raw and the 2026-05-22
aborted file remain untouched on disk as forensic snapshots.

Usage:
    python scripts/merge_qwen3_v1_data.py [--dry-run] [--force]

`--dry-run` reports what would be merged without writing.
`--force` proceeds even when a bucket's row count doesn't match expected.
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path


RESULTS = Path(__file__).resolve().parent / "results"

SOURCES = [
    # (filename, allowed_buckets) — rows whose bucket is outside this set are skipped
    ("pilot_results_qwen3_v1_python_tiny_raw_2026-05-15.jsonl",
     {"func", "sytx", "sytx+func"}),
    ("pilot_results_qwen3_v1_python_tiny_c2_text+sytx.jsonl",
     {"text+sytx"}),
    ("pilot_results_qwen3_v1_python_tiny_c2_text.jsonl",
     {"text"}),
    ("pilot_results_qwen3_v1_python_tiny_c2_text+func.jsonl",
     {"text+func"}),
    ("pilot_results_qwen3_v1_python_tiny_c2_text+sytx+func.jsonl",
     {"text+sytx+func"}),
]

EXPECTED_CASES = {
    "func": 553, "sytx": 446, "sytx+func": 128, "text": 820,
    "text+func": 663, "text+sytx": 81, "text+sytx+func": 906,
}
N_CONDITIONS = 3  # no-skill, skill-v1-sys, skill-v1-user

OUTPUT = RESULTS / "pilot_results_qwen3_v1_python_tiny.jsonl"


def load_source(path: Path, allowed: set[str]) -> list[dict]:
    rows = []
    assign_bucket = next(iter(allowed)) if len(allowed) == 1 else None
    with path.open() as f:
        for line in f:
            r = json.loads(line)
            if assign_bucket is not None and "bucket" not in r:
                r["bucket"] = assign_bucket
            if r.get("bucket") in allowed:
                rows.append(r)
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Report what would be merged without writing.")
    parser.add_argument("--force", action="store_true",
                        help="Merge even when buckets are short of expected counts.")
    args = parser.parse_args()

    missing = [name for name, _ in SOURCES if not (RESULTS / name).exists()]
    if missing:
        print("ERROR: missing source files:", file=sys.stderr)
        for m in missing:
            print(f"  {RESULTS / m}", file=sys.stderr)
        sys.exit(1)

    merged: list[dict] = []
    seen: set[tuple] = set()
    per_source = Counter()

    for name, allowed in SOURCES:
        path = RESULTS / name
        added = 0
        for r in load_source(path, allowed):
            key = (r["case_id"], r["conflict_idx"], r["condition"], r["bucket"])
            if key in seen:
                continue
            seen.add(key)
            merged.append(r)
            added += 1
        per_source[name] = added

    bucket_totals = Counter(r["bucket"] for r in merged)
    errs = sum(1 for r in merged if r.get("error"))
    cond_totals = Counter(r["condition"] for r in merged)

    print(f"merged rows: {len(merged)}")
    print(f"errors: {errs} ({errs / len(merged) * 100:.2f}%)")
    print(f"\nper source:")
    for name, n in per_source.items():
        print(f"  {n:5d}  {name}")
    print(f"\nper condition:")
    for cond, n in sorted(cond_totals.items()):
        print(f"  {n:5d}  {cond}")
    print(f"\nper bucket:")
    short_buckets = []
    for bucket in sorted(EXPECTED_CASES):
        actual = bucket_totals[bucket]
        expected = EXPECTED_CASES[bucket] * N_CONDITIONS
        if actual == expected:
            print(f"  {actual:5d}  {bucket:18s} OK")
        else:
            print(f"  {actual:5d}  {bucket:18s} (expected {expected}, short by {expected - actual})")
            short_buckets.append(bucket)

    if short_buckets and not args.force:
        print(f"\nERROR: {len(short_buckets)} bucket(s) short of expected count. "
              f"Re-run those buckets, or pass --force to merge anyway.",
              file=sys.stderr)
        sys.exit(2)

    if args.dry_run:
        print("\n--dry-run set: not writing")
        return

    with OUTPUT.open("w") as f:
        for r in merged:
            f.write(json.dumps(r) + "\n")
    print(f"\nwrote {OUTPUT}")


if __name__ == "__main__":
    main()
