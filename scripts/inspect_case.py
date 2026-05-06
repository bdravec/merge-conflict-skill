"""
inspect_case.py — Side-by-side view of one ConGra case across all pilot runs.

Shows the conflict region (sides a vs b), the ground-truth resolution, and
every model resolution recorded in any scripts/results/pilot_results_*.jsonl
file for that case.

Usage:
    python3 scripts/inspect_case.py <case_id_substring>

Example:
    python3 scripts/inspect_case.py 0xe4ff79aa

The argument matches any case_id that contains the substring, so an 8-hex-char
prefix (as used in analysis docs) is enough.
"""

import argparse
import glob
import json
import os
import sys


REPO_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RESULTS_DIR = os.path.join(REPO_ROOT, "scripts", "results")
CONGRA_ROOT = os.path.abspath(os.path.join(REPO_ROOT, "..", "ConGra"))
DATA_ROOT   = os.path.join(CONGRA_ROOT, "data", "congra_tiny_datasets", "python", "func")
META_PATH   = os.path.join(DATA_ROOT, "meta_list.txt")


def load_conflict_region(case_id: str) -> tuple[str, str, str] | None:
    """Returns (conflict_context, conflict_text, ground_truth) for the given
    case_id by looking it up in meta_list.txt and reading the dataset files.
    Returns None if the case is not found in meta_list.txt."""
    with open(META_PATH) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(": ")
            if len(parts) != 3:
                continue
            source_path, hash_idx, conflict_idx = parts
            if case_id in hash_idx:
                conflict_idx = int(conflict_idx)
                source_full  = os.path.join(CONGRA_ROOT, "data", "raw_datasets", source_path)
                hash_file    = os.path.join(DATA_ROOT, hash_idx)
                return _load_conflict_and_answer(source_full, hash_file, conflict_idx, n=5)
    return None


def _load_conflict_and_answer(source_path: str, file_path: str, k: int, n: int):
    """Lifted from pilot.py. Returns (conflict_context, conflict_text, ground_truth)."""
    region_path = source_path.replace("merged_without_base", "regions") + ".region"
    regions = []
    with open(region_path) as f:
        for line in f:
            if "#" in line:
                continue
            line = line.strip()
            if line:
                regions.append(eval(line))
    region = regions[k - 1]

    with open(file_path, encoding="utf-8", errors="ignore") as f:
        lines = f.read().split("\n")
    start, end = region[0] - 1, region[1]
    conflict_text    = "\n".join(lines[start:end])
    conflict_context = "\n".join(lines[max(0, start - n):end + n])

    resolved_path = source_path.replace("merged_without_base", "resolved").replace("regions", "resolved")
    with open(resolved_path, encoding="utf-8", errors="ignore") as f:
        rlines = f.read().split("\n")
    rstart, rend = region[2] - 1, region[3]
    ground_truth = "\n".join(rlines[max(0, rstart):rend])

    return conflict_context, conflict_text, ground_truth


def find_matching_records(case_substring: str) -> list[tuple[str, dict]]:
    """Returns [(filename, record), ...] for every record whose case_id contains the substring."""
    matches = []
    for path in sorted(glob.glob(os.path.join(RESULTS_DIR, "pilot_results_*.jsonl"))):
        filename = os.path.basename(path)
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    r = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if case_substring in r.get("case_id", ""):
                    matches.append((filename, r))
    return matches


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("case_id", help="Case id (or substring; e.g. '0xe4ff79aa')")
    args = parser.parse_args()

    case_substring = args.case_id

    print("=" * 78)
    print(f"CASE: {case_substring}")
    print("=" * 78)

    # 1. Conflict region from the dataset.
    region = load_conflict_region(case_substring)
    if region is None:
        print(f"\n[!] Case '{case_substring}' not found in {META_PATH}")
    else:
        conflict_context, conflict_text, ground_truth = region
        print("\n--- CONFLICT REGION (with surrounding context, n=5) ---\n")
        print(conflict_context)
        print("\n--- CONFLICT TEXT (markers and bodies only) ---\n")
        print(conflict_text)
        print("\n--- GROUND TRUTH RESOLUTION ---\n")
        print(ground_truth)

    # 2. All matching records across every pilot run.
    matches = find_matching_records(case_substring)
    if not matches:
        print(f"\n[!] No pilot result records found for '{case_substring}' in {RESULTS_DIR}")
        sys.exit(0)

    print(f"\n--- MODEL OUTPUTS ({len(matches)} records across pilot runs) ---")
    for filename, r in matches:
        metrics = r.get("metrics", {})
        edit = metrics.get("edit")
        winnowing = metrics.get("winnowing")
        print()
        print(f"[{filename}] condition={r.get('condition')} model={r.get('model')}")
        print(f"  edit={edit}  winnowing={winnowing}")
        print("  --- resolution ---")
        for line in (r.get("resolution") or "").split("\n"):
            print(f"  {line}")


if __name__ == "__main__":
    main()
