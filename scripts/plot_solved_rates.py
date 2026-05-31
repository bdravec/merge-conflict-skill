#!/usr/bin/env python3
"""
plot_solved_rates.py — per-bucket solved-case-count charts (issue #78).

For Qwen3-8B and Apertus-8B, plots the COUNT of solved cases per complexity
bucket across the trajectory baseline (no-skill) -> v1 -> v2 -> v2.1 (sys),
mirroring the per-bucket median charts (#77, scripts/plot_median_trends.py).

Solved = max(edit, winnowing) > 0.8 (the #56 tiering). Empty resolutions
(metrics.empty=True) count as not-solved (score 0). Rows with a non-null
`error` are dropped.

Outputs:
  docs/figures/solved_count_by_bucket.png       — 8 lines, y = solved count
  docs/analysis/solved_counts.csv                — n / solved / solved% per cell
"""

import argparse
import csv
import json
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(__file__)
RESULTS = os.path.join(HERE, "results")
FIG_DIR = os.path.join(HERE, "..", "docs", "figures")
CSV_DIR = os.path.join(HERE, "..", "docs", "analysis")

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]
CONDITIONS = ["baseline", "v1", "v2", "v2.1"]
T_SOLVED = 0.8

MODEL_LABEL = {"qwen3": "Qwen3-8B", "apertus": "Apertus-8B"}
MODEL_MARKER = {"qwen3": "o", "apertus": "s"}
QWEN_SHADE = {"v1": "#9ecae1", "v2": "#4292c6", "v2.1": "#08306b"}
APER_SHADE = {"v1": "#fcae91", "v2": "#fb6a4a", "v2.1": "#99000d"}
BASE_GREEN = {"qwen3": "#74c476", "apertus": "#238b45"}
LS = {"baseline": "-", "v1": ":", "v2": "--", "v2.1": "-"}


def cond_to_spec(model, cond, placement):
    if cond == "baseline":
        return (os.path.join(RESULTS, f"pilot_results_{model}_baseline_python_tiny.jsonl"),
                "no-skill")
    return (os.path.join(RESULTS, f"pilot_results_{model}_{cond}_python_tiny.jsonl"),
            f"skill-{cond}-{placement}")


def solved_max(m):
    """max(edit, winn) with empties mapped to 0; None if the row should be skipped."""
    if m.get("empty"):
        return 0.0
    e, w = m.get("edit"), m.get("winnowing")
    if e is None or w is None:
        return None
    return max(e, w)


def counts(path, condition):
    """{bucket: [n, solved]} for one file restricted to one condition."""
    out = {b: [0, 0] for b in BUCKETS}
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("condition") != condition:
                continue
            if r.get("error") is not None:
                continue
            s = solved_max(r["metrics"])
            if s is None:
                continue
            b = r["bucket"]
            out[b][0] += 1
            if s > T_SOLVED:
                out[b][1] += 1
    return out


def build(placement):
    data = {}
    for model in MODEL_LABEL:
        data[model] = {}
        for cond in CONDITIONS:
            path, condition = cond_to_spec(model, cond, placement)
            data[model][cond] = counts(path, condition)
    return data


def color(model, cond):
    if cond == "baseline":
        return BASE_GREEN[model]
    return (QWEN_SHADE if model == "qwen3" else APER_SHADE)[cond]


def plot(data, out_path, mode):
    """mode = 'count' (y = solved cases) or 'rate' (y = solved %)."""
    fig, ax = plt.subplots(figsize=(11, 6.5))
    x = range(len(BUCKETS))
    for model in MODEL_LABEL:
        for cond in CONDITIONS:
            if mode == "count":
                ys = [data[model][cond][b][1] for b in BUCKETS]
            else:  # rate
                ys = [100 * data[model][cond][b][1] / data[model][cond][b][0]
                      if data[model][cond][b][0] else float("nan")
                      for b in BUCKETS]
            ax.plot(x, ys, linestyle=LS[cond], color=color(model, cond),
                    marker=MODEL_MARKER[model], markersize=6, linewidth=2,
                    label=f"{MODEL_LABEL[model]} {cond}")
    # per-bucket case count (max across the 8 series = full bucket size;
    # series differ only by a few dropped error rows)
    bucket_n = {b: max(data[m][c][b][0] for m in MODEL_LABEL for c in CONDITIONS)
                for b in BUCKETS}
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{b}\n(n={bucket_n[b]})" for b in BUCKETS],
                       rotation=25, ha="right")
    ax.set_xlabel("complexity bucket")
    if mode == "count":
        ax.set_ylabel(f"solved cases (count, max(edit, winn) > {T_SOLVED})")
        what = "count"
    else:
        ax.set_ylabel(f"solved rate (%, max(edit, winn) > {T_SOLVED})")
        what = "rate"
    ax.set_title(f"Solved-case {what} per bucket — 8B models, python-tiny, sys placement\n"
                 "baseline (green) vs v1/v2/v2.1 (Qwen3 blue, Apertus red)")
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend(loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=9,
              title="model x condition")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def write_csv(data, out_path):
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "condition", "scope", "bucket", "n", "solved", "solved_pct"])
        for model in MODEL_LABEL:
            for cond in CONDITIONS:
                tot_n = tot_s = 0
                for b in BUCKETS:
                    n, s = data[model][cond][b]
                    tot_n += n
                    tot_s += s
                    pct = f"{100 * s / n:.1f}" if n else ""
                    w.writerow([model, cond, "bucket", b, n, s, pct])
                tpct = f"{100 * tot_s / tot_n:.1f}" if tot_n else ""
                w.writerow([model, cond, "overall", "", tot_n, tot_s, tpct])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--placement", default="sys", choices=["sys", "user"])
    args = ap.parse_args()
    os.makedirs(FIG_DIR, exist_ok=True)
    os.makedirs(CSV_DIR, exist_ok=True)
    data = build(args.placement)
    plot(data, os.path.join(FIG_DIR, "solved_count_by_bucket.png"), "count")
    plot(data, os.path.join(FIG_DIR, "solved_rate_by_bucket.png"), "rate")
    write_csv(data, os.path.join(CSV_DIR, "solved_counts.csv"))
    print("wrote solved_count_by_bucket.png + solved_rate_by_bucket.png + solved_counts.csv")
    for model in MODEL_LABEL:
        row = "  ".join(
            f"{c}={sum(data[model][c][b][1] for b in BUCKETS)}" for c in CONDITIONS)
        print(f"  {MODEL_LABEL[model]:12} total solved: {row}")


if __name__ == "__main__":
    main()
