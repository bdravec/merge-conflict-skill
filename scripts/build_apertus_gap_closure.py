"""
build_apertus_gap_closure.py — Apertus scaling-axis gap-closure table (8B -> 70B, #98)

Apertus-family analogue of the Qwen3 scaling table (docs/RQ_123/qwen3_gap_closure_v2_1.md, #97).
Within-family scaling axis, python-tiny. Metric = max(edit, winnowing), solved = score > 0.8.

  Gap       = 70B - 8B            (no-skill baselines)
  Recovered = (8B + skill) - 8B
  Residual  = 70B - (8B + skill)  (= Gap - Recovered; residual gap left after the
                                    skill, in pp; negative => skill overtook 70B)
  Closure   = Recovered / Gap     (negative => skill fell below the 8B baseline)

Same solved-rate logic as plot_rq3_gap_closure_violin.py: errors skipped,
empty -> 0.0 (counts in the denominator, never solved).

Run with --validate to reproduce the Qwen3 #97 numbers as a correctness check.
"""

import json
import os
import sys

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]
T_SOLVED = 0.8


def solved_rates(jsonl, condition):
    """Per-bucket solved rate (%) and pooled aggregate, for one condition."""
    counts = {b: [0, 0] for b in BUCKETS}  # bucket -> [n_solved, n_total]
    with open(os.path.join(RESULTS_DIR, jsonl)) as f:
        for line in f:
            r = json.loads(line)
            if condition is not None and r.get("condition") != condition:
                continue
            if r.get("error") is not None:
                continue
            b = r["bucket"]
            m = r["metrics"]
            if m.get("empty"):
                score = 0.0
            else:
                e, w = m.get("edit"), m.get("winnowing")
                if e is None or w is None:
                    continue
                score = max(e, w)
            counts[b][1] += 1
            if score > T_SOLVED:
                counts[b][0] += 1
    per_bucket = {b: (100.0 * s / t if t else float("nan")) for b, (s, t) in counts.items()}
    tot_s = sum(s for s, _ in counts.values())
    tot_t = sum(t for _, t in counts.values())
    per_bucket["Aggregate"] = 100.0 * tot_s / tot_t if tot_t else float("nan")
    return per_bucket


def build_table(small_base, small_skill, large_base, skill_cond, label):
    small = solved_rates(small_base, "no-skill")
    skill = solved_rates(small_skill, skill_cond)
    large = solved_rates(large_base, "no-skill")

    rows = BUCKETS + ["Aggregate"]
    print(f"\n=== {label} ===")
    print(f"{'Bucket':16} {'8B':>7} {'8B+sk':>7} {'Large':>7} {'Gap':>7} {'Recov':>7} {'Resid':>7} {'Closure':>8}")
    for b in rows:
        s, sk, lg = small[b], skill[b], large[b]
        gap = lg - s
        rec = sk - s
        res = lg - sk  # residual gap after skill (= gap - rec); negative => skill overtook large
        clo = (rec / gap * 100.0) if gap else float("nan")
        print(f"{b:16} {s:7.2f} {sk:7.2f} {lg:7.2f} {gap:7.2f} {rec:+7.2f} {res:+7.2f} {clo:+7.0f}%")


if __name__ == "__main__":
    if "--validate" in sys.argv:
        build_table(
            "pilot_results_qwen3_baseline_python_tiny.jsonl",
            "pilot_results_qwen3_v2.1_python_tiny.jsonl",
            "pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl",
            "skill-v2.1-sys",
            "Qwen3 8B->32B (VALIDATION vs #97: expect agg 29.16 / 28.30 / 38.57)",
        )
    build_table(
        "pilot_results_apertus_baseline_python_tiny.jsonl",
        "pilot_results_apertus_v2.1_python_tiny.jsonl",
        "apertus-70b_baseline_python_tiny.jsonl",
        "skill-v2.1-sys",
        "Apertus 8B->70B (#98)",
    )
