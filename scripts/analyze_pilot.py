"""
analyze_pilot.py — Summarize pilot evaluation results from pilot_results.jsonl

Usage:
    python scripts/analyze_pilot.py
"""

import json
import os
from collections import defaultdict
from statistics import mean, median

# RESULTS_FILE = os.path.join(os.path.dirname(__file__), "results", "pilot_results.jsonl")
RESULTS_FILE = os.path.join(os.path.dirname(__file__), "results", "pilot_results_apertus.jsonl")


def main():
    records = []
    with open(RESULTS_FILE) as f:
        for line in f:
            records.append(json.loads(line))

    # Group by condition
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

    # Cases with identical output across conditions
    def outputs_identical(conds):
        vals = list(conds.values())
        return vals[0]["metrics"]["edit"] == vals[1]["metrics"]["edit"]

    identical = sum(1 for conds in cases.values() if len(conds) == 2 and outputs_identical(conds))

    n_cases = len(cases)
    conditions = sorted(scores.keys())

    print(f"Pilot results — {n_cases} cases, {len(records)} records\n")
    print(f"{'Condition':<12} {'N':>4}  {'Edit mean':>10} {'Edit med':>9}  {'Winn mean':>10} {'Winn med':>9}  {'Empty':>6} {'Errors':>7}")
    print("-" * 80)
    for cond in conditions:
        e = scores[cond]["edit"]
        w = scores[cond]["winnowing"]
        print(
            f"{cond:<12} {len(e):>4}  "
            f"{mean(e):>10.4f} {median(e):>9.4f}  "
            f"{mean(w):>10.4f} {median(w):>9.4f}  "
            f"{empty[cond]:>6} {errors[cond]:>7}"
        )

    print(f"\nIdentical outputs across both conditions: {identical}/{n_cases} cases")

    # Per-case delta (skill-v1 minus no-skill), positive = skill better
    print("\nPer-case edit distance delta (skill-v1 − no-skill), positive = skill better:")
    for key, conds in sorted(cases.items()):
        ns_edit = conds.get("no-skill", {}).get("metrics", {}).get("edit")
        sk_edit = conds.get("skill-v1", {}).get("metrics", {}).get("edit")
        if ns_edit is not None and sk_edit is not None:
            delta = round(sk_edit - ns_edit, 4)
            marker = " ↑" if delta > 0 else (" ↓" if delta < 0 else "  =")
            print(f"  {key[0]}  Δedit={delta:+.4f}{marker}")


if __name__ == "__main__":
    main()
