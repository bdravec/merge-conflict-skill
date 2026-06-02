"""
analyze_baseline_passfail.py — phase 1 of issue #56.

Distribution analysis of the #46 no-skill python-tiny baseline JSONLs.
Per-bucket stats (mean, median, byte-identical rate, low-tail rate,
quartiles) for both metrics (edit, winnowing), plus histogram grids
saved to `docs/figures/`.

This script is *exploratory* — it does not pick a pass/fail threshold.
Its job is to make the distribution legible so a threshold can be
chosen with evidence, per the #56 brief.

Usage:
    python scripts/analyze_baseline_passfail.py
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean, median

import matplotlib.pyplot as plt
import numpy as np


REPO_ROOT   = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "scripts" / "results"
FIGURES_DIR = REPO_ROOT / "docs" / "figures"
DOCS_DIR    = REPO_ROOT / "docs"

# Tier scheme agreed 2026-05-15 (issue #56):
#   Solved:  score == 1.0 (byte-identical to GT)
#   Strong:  0.8 <= score < 1.0
#   Weak:    0.5 <= score < 0.8
#   Fail:    score < 0.5  OR  metrics.empty == True
TIERS = ["Solved", "Strong", "Weak", "Fail"]


def classify(record, metric_key):
    m = record["metrics"]
    if m["empty"]:
        return "Fail"
    v = m[metric_key]
    if v is None:
        return "Fail"
    if v >= 0.9999:
        return "Solved"
    if v >= 0.8:
        return "Strong"
    if v >= 0.5:
        return "Weak"
    return "Fail"


def tier_counts(records, metric_key):
    counts = {t: 0 for t in TIERS}
    for r in records:
        counts[classify(r, metric_key)] += 1
    return counts

BUCKETS = [
    "text",
    "sytx",
    "func",
    "text+sytx",
    "text+func",
    "sytx+func",
    "text+sytx+func",
]

METRICS = [
    ("edit",      "Edit similarity"),
    ("winnowing", "Winnowing"),
]


def load_records(path):
    records = []
    with open(path) as f:
        for line in f:
            records.append(json.loads(line))
    return records


def filter_no_skill_no_error(records):
    return [r for r in records if r["condition"] == "no-skill" and not r["error"]]


def per_bucket(records):
    by_bucket = defaultdict(list)
    for r in records:
        by_bucket[r["bucket"]].append(r)
    return by_bucket


def quantile(sorted_vals, q):
    if not sorted_vals:
        return float("nan")
    n = len(sorted_vals)
    i = max(0, min(n - 1, int(round(q * (n - 1)))))
    return sorted_vals[i]


def stats_row(records, metric_key):
    """Compute stats from a list of records. Records with empty=True (None
    metric) are coerced to 0.0 — empty resolution vs non-empty GT is a
    hard fail in pass/fail framing."""
    if not records:
        return None
    vals = []
    n_empty = 0
    for r in records:
        v = r["metrics"][metric_key]
        if v is None:
            n_empty += 1
            vals.append(0.0)
        else:
            vals.append(v)
    vals.sort()
    n = len(vals)
    byte_id   = sum(1 for v in vals if v >= 0.9999) / n
    low_tail  = sum(1 for v in vals if v < 0.1) / n
    above_50  = sum(1 for v in vals if v >= 0.5) / n
    above_80  = sum(1 for v in vals if v >= 0.8) / n
    return {
        "n":        n,
        "n_empty":  n_empty,
        "mean":     mean(vals),
        "median":   median(vals),
        "p25":      quantile(vals, 0.25),
        "p75":      quantile(vals, 0.75),
        "byte_id":  byte_id,
        "low_tail": low_tail,
        "above_50": above_50,
        "above_80": above_80,
    }


def print_table(model_label, metric_label, by_bucket, all_records, metric_key):
    print(f"\n=== {model_label} — {metric_label} ===")
    header = (
        f"{'bucket':<18} {'n':>5} {'empty':>5} {'mean':>7} {'median':>7} "
        f"{'p25':>6} {'p75':>6} "
        f"{'==1.0':>7} {'<0.1':>7} {'>=0.5':>7} {'>=0.8':>7}"
    )
    print(header)
    print("-" * len(header))

    def fmt(s):
        if s is None:
            return f"{'(empty)':<60}"
        return (
            f"{s['n']:>5} {s['n_empty']:>5} {s['mean']:>7.4f} {s['median']:>7.4f} "
            f"{s['p25']:>6.3f} {s['p75']:>6.3f} "
            f"{s['byte_id']*100:>6.1f}% {s['low_tail']*100:>6.1f}% "
            f"{s['above_50']*100:>6.1f}% {s['above_80']*100:>6.1f}%"
        )

    for bucket in BUCKETS:
        s = stats_row(by_bucket.get(bucket, []), metric_key)
        print(f"{bucket:<18} {fmt(s)}")
    s_all = stats_row(all_records, metric_key)
    print(f"{'ALL':<18} {fmt(s_all)}")


def plot_histograms(by_bucket_per_model, metric_key, metric_label, out_path):
    """Grid: rows=buckets, cols=models. Vertical line at 1.0 to flag byte-identical."""
    models = list(by_bucket_per_model.keys())
    n_buckets = len(BUCKETS)
    fig, axes = plt.subplots(
        n_buckets, len(models),
        figsize=(4 * len(models), 1.7 * n_buckets),
        sharex=True,
    )
    if len(models) == 1:
        axes = axes.reshape(-1, 1)

    for ri, bucket in enumerate(BUCKETS):
        for ci, model in enumerate(models):
            ax = axes[ri, ci]
            recs = by_bucket_per_model[model].get(bucket, [])
            if recs:
                vals = [
                    r["metrics"][metric_key] if r["metrics"][metric_key] is not None else 0.0
                    for r in recs
                ]
                ax.hist(
                    vals, bins=20, range=(0, 1),
                    color="steelblue", edgecolor="black", linewidth=0.4,
                )
                ax.axvline(1.0, color="green",   linestyle="--", linewidth=0.8)
                ax.axvline(0.8, color="orange",  linestyle=":",  linewidth=0.8)
                ax.axvline(0.5, color="grey",    linestyle=":",  linewidth=0.8)
                ax.text(
                    0.98, 0.92, f"n={len(vals)}",
                    transform=ax.transAxes, ha="right", va="top", fontsize=8,
                )
            ax.set_xlim(0, 1.02)
            ax.tick_params(labelsize=7)
            if ci == 0:
                ax.set_ylabel(bucket, fontsize=9)
            if ri == 0:
                ax.set_title(model, fontsize=11)
            if ri == n_buckets - 1:
                ax.set_xlabel(metric_label, fontsize=9)

    fig.suptitle(
        f"No-skill baseline (#46) — {metric_label} distribution per bucket",
        fontsize=13,
    )
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close(fig)


def render_tier_table_md(model_label, metric_label, by_bucket, all_records, metric_key):
    """Return a markdown table of tier counts for one (model, metric) combo."""
    lines = []
    lines.append(f"### {model_label} — {metric_label}\n")
    lines.append("| bucket | n | Solved | Strong | Weak | Fail |")
    lines.append("|---|--:|--:|--:|--:|--:|")
    def fmt_row(name, recs):
        if not recs:
            return f"| {name} | 0 | — | — | — | — |"
        c = tier_counts(recs, metric_key)
        n = len(recs)
        def cell(k):
            return f"{c[k]} ({c[k]/n*100:.1f}%)"
        return (
            f"| {name} | {n} | "
            f"{cell('Solved')} | {cell('Strong')} | {cell('Weak')} | {cell('Fail')} |"
        )
    for bucket in BUCKETS:
        lines.append(fmt_row(bucket, by_bucket.get(bucket, [])))
    lines.append(fmt_row("**ALL**", all_records))
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--qwen3", type=Path,
        default=RESULTS_DIR / "pilot_results_qwen3_baseline_python_tiny.jsonl",
    )
    ap.add_argument(
        "--apertus", type=Path,
        default=RESULTS_DIR / "pilot_results_apertus_baseline_python_tiny.jsonl",
    )
    ap.add_argument("--out-dir", type=Path, default=FIGURES_DIR)
    args = ap.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)

    by_bucket_per_model = {}
    all_records_per_model = {}
    for label, path in [("Qwen3-8B", args.qwen3), ("Apertus-8B", args.apertus)]:
        all_recs = load_records(path)
        clean = filter_no_skill_no_error(all_recs)
        print(
            f"{label}: loaded {len(all_recs)} records; "
            f"{len(clean)} after filtering errors+non-no-skill "
            f"(errored: {sum(1 for r in all_recs if r['error'])})"
        )
        by_bucket_per_model[label]   = per_bucket(clean)
        all_records_per_model[label] = clean

    md_sections = [
        "# Baseline pass/fail tier tables (issue #56)\n",
        "Source: `pilot_results_<model>_baseline_python_tiny.jsonl` (#46).\n",
        "Tier scheme (agreed 2026-05-15): "
        "Solved = score == 1.0 (byte-identical); "
        "Strong = 0.8 ≤ score < 1.0; "
        "Weak = 0.5 ≤ score < 0.8; "
        "Fail = score < 0.5 or empty resolution.\n",
    ]

    for metric_key, metric_label in METRICS:
        print(f"\n\n{'#'*72}\n# {metric_label}\n{'#'*72}")
        for model_label in by_bucket_per_model:
            print_table(
                model_label, metric_label,
                by_bucket_per_model[model_label],
                all_records_per_model[model_label],
                metric_key,
            )
        out_path = args.out_dir / f"baseline_{metric_key}_hist_per_bucket.png"
        plot_histograms(by_bucket_per_model, metric_key, metric_label, out_path)
        print(f"\nWrote {out_path}")

        print(f"\n--- Tier counts: {metric_label} ---")
        md_sections.append(f"\n## {metric_label}\n")
        for model_label in by_bucket_per_model:
            section = render_tier_table_md(
                model_label, metric_label,
                by_bucket_per_model[model_label],
                all_records_per_model[model_label],
                metric_key,
            )
            print()
            print(section)
            md_sections.append(section)

    md_path = DOCS_DIR / "baseline_passfail_tier_tables.md"
    md_path.write_text("\n".join(md_sections))
    print(f"\nWrote {md_path}")


if __name__ == "__main__":
    main()
