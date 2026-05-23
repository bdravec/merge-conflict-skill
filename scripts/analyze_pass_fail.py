"""analyze_pass_fail.py — performance analysis across no-skill / v1 / v2 / v2.1 (#62).

Reads four pilot JSONLs for one model (no-skill baseline + 3 skill sweeps,
each with sys/user conditions) and emits:

  - <out-csv>/<model>_tier_counts.csv  — per (skill, condition, bucket) tier
                                          composition (solved / partial / failed)
  - <out-csv>/<model>_transitions.csv  — per-cell 3x3 transition matrix vs
                                          the no-skill baseline (flattened)
  - <out-csv>/<model>_delta_edit.csv   — per-cell mean Δedit vs baseline
  - <out-fig>/<model>_tier_stacked.png — stacked bars: tier composition per
                                          (skill, condition) for ALL and each
                                          of the 7 complexity buckets
  - <out-fig>/<model>_transitions.png  — source-stratified stacked bars:
                                          for each skill condition, three
                                          bars (baseline tier = failed /
                                          partial / solved), each stacked
                                          into the destination distribution
  - <out-fig>/<model>_transitions_per_bucket.png — same idiom, small
                                                    multiples per bucket

Tier scheme (locked in #56):
  solved  = max(edit, winnowing) > 0.8   (ConGra paper convention,
                                          Zhang et al. 2024)
  failed  = max(edit, winnowing) <= 0.05 (data-cliff anchor)
  partial = otherwise
Empty resolutions (metrics.empty=True) fold in as score=0 -> failed.
Error rows (error != None) are excluded entirely.

Usage:
    python scripts/analyze_pass_fail.py \\
        --model qwen3 \\
        --baseline scripts/results/pilot_results_qwen3_baseline_python_tiny.jsonl \\
        --v1       scripts/results/pilot_results_qwen3_v1_python_tiny.jsonl \\
        --v2       scripts/results/pilot_results_qwen3_v2_python_tiny.jsonl \\
        --v2.1     scripts/results/pilot_results_qwen3_v2.1_python_tiny.jsonl
"""

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "scripts" / "results"
FIGURES_DIR = REPO_ROOT / "docs" / "figures"
ANALYSIS_DIR = REPO_ROOT / "docs" / "analysis"

BUCKETS = ["func", "sytx", "sytx+func", "text",
           "text+func", "text+sytx", "text+sytx+func"]

TIERS = ["failed", "partial", "solved"]

T_SOLVED = 0.8
T_FAIL = 0.05

COLORS = {
    "failed":  "#b2182b",
    "partial": "#bfbfbf",
    "solved":  "#1a9850",
}


def tier_of(record) -> str | None:
    """Return tier string, or None if the row should be excluded (error)."""
    if record.get("error") is not None:
        return None
    m = record["metrics"]
    if m.get("empty"):
        return "failed"
    e, w = m.get("edit"), m.get("winnowing")
    if e is None or w is None:
        return None
    s = max(e, w)
    if s > T_SOLVED:
        return "solved"
    if s <= T_FAIL:
        return "failed"
    return "partial"


def edit_of(record) -> float | None:
    if record.get("error") is not None:
        return None
    m = record["metrics"]
    if m.get("empty"):
        return 0.0
    return m.get("edit")


def load_condition(path: Path, condition: str) -> list[dict]:
    """Load rows for one condition from one JSONL."""
    out = []
    with path.open() as f:
        for line in f:
            r = json.loads(line)
            if r.get("condition") == condition:
                out.append(r)
    return out


def index_by_case(rows: list[dict]) -> dict[tuple, dict]:
    """Index rows by (case_id, conflict_idx)."""
    return {(r["case_id"], r["conflict_idx"]): r for r in rows}


# -------- tier counts --------

def tier_counts_for_cell(rows: list[dict]) -> dict[str, dict]:
    """Per bucket + ALL: dict[bucket] -> {n, failed, partial, solved}."""
    out = {b: {"n": 0, "failed": 0, "partial": 0, "solved": 0} for b in BUCKETS}
    out["ALL"] = {"n": 0, "failed": 0, "partial": 0, "solved": 0}
    for r in rows:
        t = tier_of(r)
        if t is None:
            continue
        b = r["bucket"]
        out[b]["n"] += 1
        out[b][t] += 1
        out["ALL"]["n"] += 1
        out["ALL"][t] += 1
    return out


def write_tier_counts_csv(path: Path, model: str, cells: dict[str, list[dict]]):
    """cells: ordered {(skill, condition_label): [rows]}."""
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "skill", "condition", "bucket",
                    "n", "failed", "partial", "solved",
                    "failed_pct", "partial_pct", "solved_pct"])
        for (skill, cond), rows in cells.items():
            counts = tier_counts_for_cell(rows)
            for b in BUCKETS + ["ALL"]:
                c = counts[b]
                n = c["n"]
                if n == 0:
                    w.writerow([model, skill, cond, b, 0, 0, 0, 0, "", "", ""])
                else:
                    w.writerow([
                        model, skill, cond, b, n,
                        c["failed"], c["partial"], c["solved"],
                        f"{c['failed']/n*100:.2f}",
                        f"{c['partial']/n*100:.2f}",
                        f"{c['solved']/n*100:.2f}",
                    ])


# -------- transitions --------

def transitions_for_cell(
    baseline_by_case: dict[tuple, dict],
    cell_rows: list[dict],
) -> dict[str, dict]:
    """Per bucket + ALL: dict[bucket] -> dict[(src,dst)] -> count + n_paired."""
    init = lambda: {"n_paired": 0,
                    **{f"{s}->{d}": 0 for s in TIERS for d in TIERS}}
    out = {b: init() for b in BUCKETS}
    out["ALL"] = init()

    for r in cell_rows:
        key = (r["case_id"], r["conflict_idx"])
        if key not in baseline_by_case:
            continue
        src = tier_of(baseline_by_case[key])
        dst = tier_of(r)
        if src is None or dst is None:
            continue
        b = r["bucket"]
        out[b]["n_paired"] += 1
        out[b][f"{src}->{dst}"] += 1
        out["ALL"]["n_paired"] += 1
        out["ALL"][f"{src}->{dst}"] += 1
    return out


def write_transitions_csv(
    path: Path, model: str,
    baseline_by_case: dict[tuple, dict],
    cells: dict[str, list[dict]],
):
    cols = ["model", "skill", "condition", "bucket", "n_paired"]
    for s in TIERS:
        for d in TIERS:
            cols.append(f"{s}->{d}")
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for (skill, cond), rows in cells.items():
            t = transitions_for_cell(baseline_by_case, rows)
            for b in BUCKETS + ["ALL"]:
                c = t[b]
                row = [model, skill, cond, b, c["n_paired"]]
                for s in TIERS:
                    for d in TIERS:
                        row.append(c[f"{s}->{d}"])
                w.writerow(row)


# -------- delta-edit --------

def delta_edit_for_cell(
    baseline_by_case: dict[tuple, dict],
    cell_rows: list[dict],
) -> dict[str, dict]:
    """Mean Δedit (skill - baseline) per bucket + ALL."""
    out = {b: {"n_paired": 0, "sum_delta": 0.0,
               "n_skill_only": 0, "mean_skill": 0.0,
               "_sk": 0.0}
           for b in BUCKETS + ["ALL"]}
    for r in cell_rows:
        key = (r["case_id"], r["conflict_idx"])
        if key not in baseline_by_case:
            continue
        e_skill = edit_of(r)
        e_base = edit_of(baseline_by_case[key])
        if e_skill is None or e_base is None:
            continue
        b = r["bucket"]
        out[b]["n_paired"] += 1
        out[b]["sum_delta"] += e_skill - e_base
        out[b]["_sk"] += e_skill
        out["ALL"]["n_paired"] += 1
        out["ALL"]["sum_delta"] += e_skill - e_base
        out["ALL"]["_sk"] += e_skill
    for b in out:
        n = out[b]["n_paired"]
        out[b]["mean_delta"] = out[b]["sum_delta"] / n if n else 0.0
        out[b]["mean_skill"] = out[b]["_sk"] / n if n else 0.0
    return out


def write_delta_edit_csv(
    path: Path, model: str,
    baseline_by_case: dict[tuple, dict],
    cells: dict[str, list[dict]],
):
    with path.open("w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["model", "skill", "condition", "bucket",
                    "n_paired", "mean_delta_edit", "mean_skill_edit"])
        for (skill, cond), rows in cells.items():
            d = delta_edit_for_cell(baseline_by_case, rows)
            for b in BUCKETS + ["ALL"]:
                c = d[b]
                if c["n_paired"] == 0:
                    w.writerow([model, skill, cond, b, 0, "", ""])
                else:
                    w.writerow([
                        model, skill, cond, b, c["n_paired"],
                        f"{c['mean_delta']:.4f}",
                        f"{c['mean_skill']:.4f}",
                    ])


# -------- figures --------

def cell_label(skill: str, cond: str) -> str:
    if skill == "no-skill":
        return "no-skill"
    return f"{skill}\n{cond}"


def plot_tier_stacked(
    out_path: Path, model: str,
    cells_in_order: list[tuple[str, str]],
    cells: dict[tuple, list[dict]],
):
    """Grid of stacked bars: rows = bucket panels (ALL + 7 buckets),
    bars within each row = one per (skill, condition) cell."""
    panels = ["ALL"] + BUCKETS
    n_panels = len(panels)
    # 3x3 grid: 8 panels + 1 reserved for legend so it never overlaps data.
    fig, axes = plt.subplots(3, 3, figsize=(13, 11),
                             sharey=True)
    axes_flat = axes.flatten()

    for idx, panel in enumerate(panels):
        ax = axes_flat[idx]
        labels = [cell_label(s, c) for s, c in cells_in_order]
        failed = []
        partial = []
        solved = []
        ns = []
        for cell_key in cells_in_order:
            counts = tier_counts_for_cell(cells[cell_key])[panel]
            n = counts["n"]
            ns.append(n)
            if n == 0:
                failed.append(0); partial.append(0); solved.append(0)
            else:
                failed.append(counts["failed"] / n * 100)
                partial.append(counts["partial"] / n * 100)
                solved.append(counts["solved"] / n * 100)
        xs = np.arange(len(cells_in_order))
        ax.bar(xs, failed, color=COLORS["failed"], label="failed")
        ax.bar(xs, partial, bottom=failed,
               color=COLORS["partial"], label="partial")
        bot = [a + b for a, b in zip(failed, partial)]
        ax.bar(xs, solved, bottom=bot, color=COLORS["solved"], label="solved")
        ax.set_xticks(xs)
        ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=7)
        ax.set_ylim(0, 100)
        ax.set_title(f"{panel}  (n_max={max(ns)})", fontsize=10)
        ax.tick_params(axis="y", labelsize=8)
        if idx % 3 == 0:
            ax.set_ylabel("share (%)", fontsize=9)

    # Hide unused panels (3x3 = 9 slots; 8 panels + 1 legend slot).
    for k in range(n_panels, len(axes_flat)):
        axes_flat[k].axis("off")
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=COLORS["solved"]),
        plt.Rectangle((0, 0), 1, 1, color=COLORS["partial"]),
        plt.Rectangle((0, 0), 1, 1, color=COLORS["failed"]),
    ]
    axes_flat[-1].legend(handles, ["solved (>0.8)",
                                   "partial",
                                   "failed (≤0.05 or empty)"],
                         loc="center", fontsize=11, frameon=False)

    fig.suptitle(f"{model} — tier composition (no-skill + 3 skill versions × sys/user)",
                 fontsize=12)
    fig.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close(fig)


def plot_transitions(
    out_path: Path, model: str,
    cells_in_order: list[tuple[str, str]],
    baseline_by_case: dict[tuple, dict],
    cells: dict[tuple, list[dict]],
    per_bucket: bool,
):
    """Source-stratified stacked bars: for each skill condition, three bars
    (baseline tier = failed / partial / solved), each stacked into the
    destination distribution. If per_bucket, grid of 7 buckets × N cells;
    else single ALL row."""
    skill_cells = [(s, c) for s, c in cells_in_order if s != "no-skill"]
    panels = BUCKETS if per_bucket else ["ALL"]
    n_rows = len(panels)
    n_cols = len(skill_cells)

    fig_w = max(12, 2.2 * n_cols)
    fig_h = max(3.5, 1.7 * n_rows + 0.5)
    fig, axes = plt.subplots(
        n_rows, n_cols,
        figsize=(fig_w, fig_h),
        sharey=True,
    )
    if n_rows == 1 and n_cols == 1:
        axes = np.array([[axes]])
    elif n_rows == 1:
        axes = axes.reshape(1, -1)
    elif n_cols == 1:
        axes = axes.reshape(-1, 1)

    for ri, panel in enumerate(panels):
        for ci, (skill, cond) in enumerate(skill_cells):
            ax = axes[ri, ci]
            t = transitions_for_cell(baseline_by_case, cells[(skill, cond)])[panel]
            xs = np.arange(len(TIERS))
            failed = []
            partial = []
            solved = []
            ns = []
            for src in TIERS:
                row_total = sum(t[f"{src}->{d}"] for d in TIERS)
                ns.append(row_total)
                if row_total == 0:
                    failed.append(0); partial.append(0); solved.append(0)
                else:
                    failed.append(t[f"{src}->failed"]   / row_total * 100)
                    partial.append(t[f"{src}->partial"] / row_total * 100)
                    solved.append(t[f"{src}->solved"]   / row_total * 100)
            ax.bar(xs, failed, color=COLORS["failed"], width=0.8)
            ax.bar(xs, partial, bottom=failed,
                   color=COLORS["partial"], width=0.8)
            bot = [a + b for a, b in zip(failed, partial)]
            ax.bar(xs, solved, bottom=bot, color=COLORS["solved"], width=0.8)
            ax.set_xticks(xs)
            ax.set_xticklabels(
                [f"{src}\n(n={n})" for src, n in zip(TIERS, ns)],
                fontsize=6,
            )
            ax.set_ylim(0, 100)
            ax.tick_params(axis="y", labelsize=7)
            if ri == 0:
                ax.set_title(cell_label(skill, cond).replace("\n", " "),
                             fontsize=9)
            if ci == 0:
                if per_bucket:
                    ax.set_ylabel(f"{panel}\nshare (%)", fontsize=8)
                else:
                    ax.set_ylabel("share (%)", fontsize=9)

    handles = [
        plt.Rectangle((0, 0), 1, 1, color=COLORS["solved"]),
        plt.Rectangle((0, 0), 1, 1, color=COLORS["partial"]),
        plt.Rectangle((0, 0), 1, 1, color=COLORS["failed"]),
    ]
    fig.legend(handles, ["destination: solved",
                         "destination: partial",
                         "destination: failed"],
               loc="lower center", ncol=3, fontsize=9, frameon=False,
               bbox_to_anchor=(0.5, -0.02))

    title = f"{model} — destination tier given baseline tier"
    if per_bucket:
        title += " (per bucket)"
    fig.suptitle(title, fontsize=12)
    fig.tight_layout(rect=[0, 0.03, 1, 0.97])
    fig.savefig(out_path, dpi=130, bbox_inches="tight")
    plt.close(fig)


# -------- main --------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", required=True,
                    help="Model label used in output filenames + CSV column.")
    ap.add_argument("--baseline", type=Path, required=True)
    ap.add_argument("--v1", type=Path, required=True)
    ap.add_argument("--v2", type=Path, required=True)
    ap.add_argument("--v2.1", dest="v21", type=Path, required=True)
    ap.add_argument("--out-csv", type=Path, default=ANALYSIS_DIR)
    ap.add_argument("--out-fig", type=Path, default=FIGURES_DIR)
    args = ap.parse_args()

    args.out_csv.mkdir(parents=True, exist_ok=True)
    args.out_fig.mkdir(parents=True, exist_ok=True)

    # Build cell -> rows mapping in stable order.
    cells: dict[tuple[str, str], list[dict]] = {}
    cells[("no-skill", "no-skill")] = load_condition(args.baseline, "no-skill")
    cells[("v1", "sys")]   = load_condition(args.v1, "skill-v1-sys")
    cells[("v1", "user")]  = load_condition(args.v1, "skill-v1-user")
    cells[("v2", "sys")]   = load_condition(args.v2, "skill-v2-sys")
    cells[("v2", "user")]  = load_condition(args.v2, "skill-v2-user")
    cells[("v2.1", "sys")] = load_condition(args.v21, "skill-v2.1-sys")
    cells[("v2.1", "user")] = load_condition(args.v21, "skill-v2.1-user")

    baseline_by_case = index_by_case(cells[("no-skill", "no-skill")])

    print(f"{args.model}: loaded cells:")
    for k, rows in cells.items():
        errs = sum(1 for r in rows if r.get("error"))
        print(f"  {k!s:30s}  rows={len(rows):5d}  errors={errs:4d}")
    print(f"baseline_by_case keys: {len(baseline_by_case)}")

    cell_order = list(cells.keys())

    tier_csv = args.out_csv / f"{args.model}_tier_counts.csv"
    trans_csv = args.out_csv / f"{args.model}_transitions.csv"
    delta_csv = args.out_csv / f"{args.model}_delta_edit.csv"

    write_tier_counts_csv(tier_csv, args.model, cells)
    print(f"wrote {tier_csv}")

    write_transitions_csv(trans_csv, args.model, baseline_by_case, cells)
    print(f"wrote {trans_csv}")

    write_delta_edit_csv(delta_csv, args.model, baseline_by_case, cells)
    print(f"wrote {delta_csv}")

    fig_stacked = args.out_fig / f"{args.model}_tier_stacked.png"
    plot_tier_stacked(fig_stacked, args.model, cell_order, cells)
    print(f"wrote {fig_stacked}")

    fig_trans = args.out_fig / f"{args.model}_transitions.png"
    plot_transitions(fig_trans, args.model, cell_order,
                     baseline_by_case, cells, per_bucket=False)
    print(f"wrote {fig_trans}")

    fig_trans_pb = args.out_fig / f"{args.model}_transitions_per_bucket.png"
    plot_transitions(fig_trans_pb, args.model, cell_order,
                     baseline_by_case, cells, per_bucket=True)
    print(f"wrote {fig_trans_pb}")


if __name__ == "__main__":
    main()
