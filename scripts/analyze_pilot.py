"""
analyze_pilot.py — Summarize pilot evaluation results

Usage:
    python scripts/analyze_pilot.py --model qwen3
    python scripts/analyze_pilot.py --model apertus
"""

import argparse
import json
import os
from collections import defaultdict
from statistics import mean, median

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

RESULT_FILES = {
    "qwen3":   "pilot_results_qwen3_v2.jsonl",
    "apertus": "pilot_results_apertus_v2.jsonl",
}

BASELINE = "no-skill"
SKILL_CONDITIONS = ["skill-v1-sys", "skill-v1-user"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=list(RESULT_FILES.keys()))
    args = parser.parse_args()

    results_file = os.path.join(RESULTS_DIR, RESULT_FILES[args.model])
    records = []
    with open(results_file) as f:
        for line in f:
            records.append(json.loads(line))

    scores = defaultdict(lambda: {"edit": [], "winnowing": []})
    errors = defaultdict(int)
    empty  = defaultdict(int)

    cases = {}
    for r in records:
        key = (r["case_id"], r["conflict_idx"])
        cases.setdefault(key, {})[r["condition"]] = r
        m = r["metrics"]
        if r["error"]:
            errors[r["condition"]] += 1
        elif m["empty"]:
            empty[r["condition"]] += 1
        else:
            scores[r["condition"]]["edit"].append(m["edit"])
            scores[r["condition"]]["winnowing"].append(m["winnowing"])

    n_cases = len(cases)
    conditions = sorted(scores.keys())

    print(f"Model: {args.model}  |  {n_cases} cases, {len(records)} records\n")
    print(f"{'Condition':<16} {'N':>4}  {'Edit mean':>10} {'Edit med':>9}  {'Winn mean':>10} {'Winn med':>9}  {'Empty':>6} {'Errors':>7}")
    print("-" * 84)
    for cond in conditions:
        e = scores[cond]["edit"]
        w = scores[cond]["winnowing"]
        print(
            f"{cond:<16} {len(e):>4}  "
            f"{mean(e):>10.4f} {median(e):>9.4f}  "
            f"{mean(w):>10.4f} {median(w):>9.4f}  "
            f"{empty[cond]:>6} {errors[cond]:>7}"
        )

    # Identical output counts per skill condition vs baseline
    print()
    for skill_cond in SKILL_CONDITIONS:
        identical = sum(
            1 for conds in cases.values()
            if BASELINE in conds and skill_cond in conds
            and conds[BASELINE]["resolution"].strip() == conds[skill_cond]["resolution"].strip()
        )
        print(f"Identical outputs ({BASELINE} vs {skill_cond}): {identical}/{n_cases} cases")

    # Per-case deltas vs baseline
    for skill_cond in SKILL_CONDITIONS:
        print(f"\nPer-case edit delta ({skill_cond} − {BASELINE}), positive = skill better:")
        for key, conds in sorted(cases.items()):
            ns_edit = conds.get(BASELINE, {}).get("metrics", {}).get("edit")
            sk_edit = conds.get(skill_cond, {}).get("metrics", {}).get("edit")
            if ns_edit is None or sk_edit is None:
                continue
            delta = round(sk_edit - ns_edit, 4)
            marker = " ↑" if delta > 0 else (" ↓" if delta < 0 else "  =")
            identical = conds[BASELINE]["resolution"].strip() == conds[skill_cond]["resolution"].strip()
            tag = " [identical]" if identical else ""
            print(f"  {key[0]}  Δedit={delta:+.4f}{marker}{tag}")


if __name__ == "__main__":
    main()
