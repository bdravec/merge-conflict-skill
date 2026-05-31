#!/usr/bin/env python3
"""
plot_median_trends.py — median-trajectory line charts (issue #77).

Connects the per-condition median of a metric across the trajectory
    baseline (no-skill) -> v1 -> v2 -> v2.1
for Qwen3-8B and Apertus-8B, mirroring the median lines shown inside the
baseline violins (#56/#67).

Median convention matches scripts/plot_baseline_violin.py:
  - drop rows with a non-null `error`
  - empty resolutions (metrics.empty=True) map to 0.0
  - rows with null edit/winnowing are skipped

Skill points use the chosen placement (default: sys). Metric default: max.

Outputs (under docs/figures/, suffixed by metric):
  median_trend_overall_<metric>.png       — 2 lines, pooled over all buckets
  median_trend_per_bucket_<metric>.png     — 7 subplots, one per bucket
  median_trend_all_buckets_<metric>.png     — single panel, 14 lines
And a tidy CSV: docs/analysis/median_trends_<metric>.csv
"""

import argparse
import csv
import json
import os
from collections import defaultdict

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

HERE = os.path.dirname(__file__)
RESULTS = os.path.join(HERE, "results")
FIG_DIR = os.path.join(HERE, "..", "docs", "figures")
CSV_DIR = os.path.join(HERE, "..", "docs", "analysis")

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

# matches the baseline-violin palette (#56)
MODEL_COLOR = {"qwen3": "#4575b4", "apertus": "#d6604d"}
MODEL_LABEL = {"qwen3": "Qwen3-8B", "apertus": "Apertus-8B"}
MODEL_MARKER = {"qwen3": "o", "apertus": "s"}

CONDITIONS = ["baseline", "v1", "v2", "v2.1"]   # x-axis order


def cond_to_spec(model: str, cond: str, placement: str):
    """Return (jsonl_path, condition_string) for a (model, trajectory-point)."""
    if cond == "baseline":
        return (os.path.join(RESULTS, f"pilot_results_{model}_baseline_python_tiny.jsonl"),
                "no-skill")
    return (os.path.join(RESULTS, f"pilot_results_{model}_{cond}_python_tiny.jsonl"),
            f"skill-{cond}-{placement}")


def metric_value(m: dict, key: str):
    """Per-row metric, mirroring plot_baseline_violin.scores_per_bucket."""
    if m.get("empty"):
        return 0.0
    e, w = m.get("edit"), m.get("winnowing")
    if e is None or w is None:
        return None
    if key == "edit":
        return e
    if key == "winnowing":
        return w
    if key == "max":
        return max(e, w)
    raise ValueError(key)


def load_scores(path: str, condition: str, key: str):
    """{bucket: [scores]} for one file restricted to one condition."""
    out = {b: [] for b in BUCKETS}
    with open(path) as f:
        for line in f:
            r = json.loads(line)
            if r.get("condition") != condition:
                continue
            if r.get("error") is not None:
                continue
            v = metric_value(r["metrics"], key)
            if v is None:
                continue
            out[r["bucket"]].append(v)
    return out


def build_medians(key: str, placement: str):
    """
    Returns nested dict:
      medians[model][cond]["overall"]      -> float
      medians[model][cond]["bucket"][b]    -> float
    plus raw n for reporting.
    """
    medians = {}
    for model in MODEL_COLOR:
        medians[model] = {}
        for cond in CONDITIONS:
            path, condition = cond_to_spec(model, cond, placement)
            per_bucket = load_scores(path, condition, key)
            pooled = [v for vals in per_bucket.values() for v in vals]
            medians[model][cond] = {
                "overall": float(np.median(pooled)) if pooled else float("nan"),
                "overall_n": len(pooled),
                "bucket": {b: (float(np.median(per_bucket[b])) if per_bucket[b] else float("nan"))
                           for b in BUCKETS},
                "bucket_n": {b: len(per_bucket[b]) for b in BUCKETS},
            }
    return medians


# ── plots ────────────────────────────────────────────────────────────────────

def plot_overall(medians, key, title_metric, out_path):
    fig, ax = plt.subplots(figsize=(7, 5))
    x = range(len(CONDITIONS))
    for model in MODEL_COLOR:
        ys = [medians[model][c]["overall"] for c in CONDITIONS]
        ax.plot(x, ys, marker=MODEL_MARKER[model], color=MODEL_COLOR[model],
                linewidth=2.2, markersize=8, label=MODEL_LABEL[model])
        for xi, yi in zip(x, ys):
            ax.annotate(f"{yi:.3f}", (xi, yi), textcoords="offset points",
                        xytext=(0, 8), ha="center", fontsize=8,
                        color=MODEL_COLOR[model])
    ax.set_xticks(list(x))
    ax.set_xticklabels(CONDITIONS)
    ax.set_xlabel("skill condition (sys placement)")
    ax.set_ylabel(f"median {title_metric}")
    ax.set_title(f"Median {title_metric} trajectory — 8B models, python-tiny\n"
                 f"pooled over all buckets")
    ax.grid(True, axis="y", alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_per_bucket(medians, key, title_metric, out_path):
    fig, axes = plt.subplots(2, 4, figsize=(15, 7), sharex=True, sharey=True)
    axes = axes.ravel()
    x = range(len(CONDITIONS))
    for ax, b in zip(axes, BUCKETS):
        for model in MODEL_COLOR:
            ys = [medians[model][c]["bucket"][b] for c in CONDITIONS]
            ax.plot(x, ys, marker=MODEL_MARKER[model], color=MODEL_COLOR[model],
                    linewidth=2, markersize=6, label=MODEL_LABEL[model])
        ax.set_title(b, fontsize=10)
        ax.grid(True, axis="y", alpha=0.3)
        ax.set_xticks(list(x))
        ax.set_xticklabels(CONDITIONS, fontsize=8)
    # last cell: legend
    axes[-1].axis("off")
    axes[-1].legend(handles=[Line2D([0], [0], color=MODEL_COLOR[m],
                                    marker=MODEL_MARKER[m], linewidth=2,
                                    label=MODEL_LABEL[m]) for m in MODEL_COLOR],
                    loc="center", fontsize=11, title="model")
    fig.suptitle(f"Median {title_metric} per bucket — 8B models, python-tiny "
                 f"(baseline -> v1 -> v2 -> v2.1, sys)", fontsize=12)
    fig.supylabel(f"median {title_metric}")
    fig.tight_layout(rect=[0, 0, 1, 0.97])
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_all_buckets(medians, key, title_metric, out_path):
    fig, ax = plt.subplots(figsize=(9, 6.5))
    x = range(len(CONDITIONS))
    bucket_colors = plt.cm.viridis(np.linspace(0, 0.92, len(BUCKETS)))
    style = {"qwen3": "-", "apertus": "--"}
    for bi, b in enumerate(BUCKETS):
        for model in MODEL_COLOR:
            ys = [medians[model][c]["bucket"][b] for c in CONDITIONS]
            ax.plot(x, ys, linestyle=style[model], color=bucket_colors[bi],
                    linewidth=1.8, marker=MODEL_MARKER[model], markersize=5,
                    alpha=0.9)
    ax.set_xticks(list(x))
    ax.set_xticklabels(CONDITIONS)
    ax.set_xlabel("skill condition (sys placement)")
    ax.set_ylabel(f"median {title_metric}")
    ax.set_title(f"Median {title_metric} per bucket x model — 8B, python-tiny")
    ax.grid(True, axis="y", alpha=0.3)
    bucket_handles = [Line2D([0], [0], color=bucket_colors[bi], linewidth=2.5,
                             label=b) for bi, b in enumerate(BUCKETS)]
    model_handles = [Line2D([0], [0], color="#555", linestyle=style[m],
                            marker=MODEL_MARKER[m], label=MODEL_LABEL[m])
                     for m in MODEL_COLOR]
    leg1 = ax.legend(handles=bucket_handles, title="bucket (colour)",
                     loc="upper left", bbox_to_anchor=(1.01, 1.0), fontsize=8)
    ax.add_artist(leg1)
    ax.legend(handles=model_handles, title="model (line style)",
              loc="lower left", bbox_to_anchor=(1.01, 0.0), fontsize=8)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    plt.close(fig)


def write_csv(medians, key, out_path):
    with open(out_path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "condition", "scope", "bucket", "median", "n"])
        for model in MODEL_COLOR:
            for cond in CONDITIONS:
                d = medians[model][cond]
                w.writerow([model, cond, "overall", "", f"{d['overall']:.4f}", d["overall_n"]])
                for b in BUCKETS:
                    w.writerow([model, cond, "bucket", b,
                                f"{d['bucket'][b]:.4f}", d["bucket_n"][b]])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--placement", default="sys", choices=["sys", "user"])
    ap.add_argument("--metrics", nargs="+", default=["max"],
                    choices=["edit", "winnowing", "max"])
    args = ap.parse_args()

    os.makedirs(FIG_DIR, exist_ok=True)
    os.makedirs(CSV_DIR, exist_ok=True)
    titles = {"edit": "edit-similarity", "winnowing": "winnowing", "max": "max(edit, winn)"}

    for key in args.metrics:
        medians = build_medians(key, args.placement)
        plot_overall(medians, key, titles[key],
                     os.path.join(FIG_DIR, f"median_trend_overall_{key}.png"))
        plot_per_bucket(medians, key, titles[key],
                        os.path.join(FIG_DIR, f"median_trend_per_bucket_{key}.png"))
        plot_all_buckets(medians, key, titles[key],
                         os.path.join(FIG_DIR, f"median_trend_all_buckets_{key}.png"))
        write_csv(medians, key, os.path.join(CSV_DIR, f"median_trends_{key}.csv"))
        print(f"[{key}] wrote 3 figures + median_trends_{key}.csv")
        for model in MODEL_COLOR:
            row = "  ".join(f"{c}={medians[model][c]['overall']:.3f}" for c in CONDITIONS)
            print(f"    {MODEL_LABEL[model]:12} overall: {row}")


if __name__ == "__main__":
    main()
