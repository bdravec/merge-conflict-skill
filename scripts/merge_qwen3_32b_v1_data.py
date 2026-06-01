"""Merge the qwen3-32b v1 python-tiny partial run with its text+sytx+func resume
into one canonical file (refs #75; resume was needed because of the #80 vLLM hang).

The 2026-06-01 run hung at 3123/3604 cases on a wedged vLLM request. The
remaining 481 cases (all text+sytx+func) were finished by a filtered resume on
the hardened runner (see setup_qwen3_32b_v1_resume.py).

Sources:
  - partial : pilot_results_qwen3-32b_v1_python_tiny.jsonl
              3123 cases across all buckets; rows carry a "bucket" field
              (original run was --bucket all).
  - resume  : pilot_results_qwen3-32b_v1_python_tiny_tsf_resume.jsonl
              481 text+sytx+func cases; rows lack "bucket" (ran with
              --data-root, so multi_bucket was off) -> assigned here.

The partial is first copied to *_partial_pre_resume.jsonl as a forensic
snapshot, then the canonical filename is rewritten with the merged set.

Dedup key: (case_id, conflict_idx, condition, bucket). Resume case_ids are the
not-yet-done ones, so they are disjoint from the partial — dedup is a safety net.

Usage:
    python scripts/merge_qwen3_32b_v1_data.py [--dry-run] [--force]

`--dry-run` reports what would be merged without writing.
`--force`   writes even when a bucket is short of its expected count.
"""
import argparse
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

RESULTS = Path(__file__).resolve().parent / "results"

PARTIAL = RESULTS / "pilot_results_qwen3-32b_v1_python_tiny.jsonl"
RESUME  = RESULTS / "pilot_results_qwen3-32b_v1_python_tiny_tsf_resume.jsonl"
SNAPSHOT = RESULTS / "pilot_results_qwen3-32b_v1_python_tiny_partial_pre_resume.jsonl"
OUTPUT   = PARTIAL  # canonical filename

RESUME_BUCKET = "text+sytx+func"

# Achieved case counts per bucket (meta counts minus the handful of deterministic
# load-failure drops — a case whose .region/resolved file won't parse). These are
# model-independent (same dataset), so they match the 8B run's merge_qwen3_v1_data.py
# and are confirmed against the completed buckets in this run's partial.
EXPECTED_CASES = {
    "func": 553, "sytx": 446, "sytx+func": 128, "text": 820,
    "text+func": 663, "text+sytx": 81, "text+sytx+func": 906,
}
N_CONDITIONS = 3  # no-skill, skill-v1-sys, skill-v1-user


def load_rows(path: Path, assign_bucket: str | None = None) -> list[dict]:
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            if assign_bucket is not None and "bucket" not in r:
                r["bucket"] = assign_bucket
            rows.append(r)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true",
                    help="Report what would be merged without writing.")
    ap.add_argument("--force", action="store_true",
                    help="Write even when buckets are short of expected counts.")
    args = ap.parse_args()

    missing = [p for p in (PARTIAL, RESUME) if not p.exists()]
    if missing:
        print("ERROR: missing source file(s):", file=sys.stderr)
        for m in missing:
            print(f"  {m}", file=sys.stderr)
        sys.exit(1)

    merged: list[dict] = []
    seen: set[tuple] = set()
    per_source = Counter()

    for label, path, assign in (("partial", PARTIAL, None),
                                ("resume", RESUME, RESUME_BUCKET)):
        added = 0
        for r in load_rows(path, assign):
            key = (r["case_id"], r["conflict_idx"], r["condition"], r["bucket"])
            if key in seen:
                continue
            seen.add(key)
            merged.append(r)
            added += 1
        per_source[label] = added

    bucket_totals = Counter(r["bucket"] for r in merged)
    cond_totals = Counter(r["condition"] for r in merged)
    errs = sum(1 for r in merged if r.get("error"))

    print(f"merged rows: {len(merged)}")
    print(f"errors: {errs} ({errs / len(merged) * 100:.2f}%)")
    print("\nper source (rows added):")
    for label, n in per_source.items():
        print(f"  {n:6d}  {label}")
    print("\nper condition:")
    for cond, n in sorted(cond_totals.items()):
        print(f"  {n:6d}  {cond}")
    print("\nper bucket:")
    short = []
    for bucket in sorted(EXPECTED_CASES):
        actual = bucket_totals[bucket]
        expected = EXPECTED_CASES[bucket] * N_CONDITIONS
        if actual == expected:
            print(f"  {actual:6d}  {bucket:18s} OK")
        else:
            print(f"  {actual:6d}  {bucket:18s} (expected {expected}, "
                  f"diff {actual - expected:+d})")
            short.append(bucket)

    if short and not args.force:
        print(f"\nERROR: {len(short)} bucket(s) off expected count. "
              f"Investigate, or pass --force to write anyway.", file=sys.stderr)
        sys.exit(2)

    if args.dry_run:
        print("\n--dry-run set: not writing.")
        return

    shutil.copy2(PARTIAL, SNAPSHOT)
    print(f"\nsnapshot of partial -> {SNAPSHOT}")
    with OUTPUT.open("w") as f:
        for r in merged:
            f.write(json.dumps(r) + "\n")
    print(f"wrote canonical -> {OUTPUT}  ({len(merged)} rows)")


if __name__ == "__main__":
    main()
