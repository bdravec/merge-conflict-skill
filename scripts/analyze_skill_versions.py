"""Compare one or more skill-version runs against a shared no-skill baseline.

Reusable across models (8B / 32B / 70B) and skill versions (v1 / v2 / v2.1).
Built for the sys-only large-pair convention (each version file holds only its
skill-{ver}-sys rows; the no-skill baseline is shared), but also works on the
8B-style multi-condition files — it auto-picks the sys skill condition.

For each version it reports, paired on the cases present in BOTH that version
and the baseline:
  - mean edit-sim and winnowing for baseline vs skill, and the delta
  - exact-match rate (normalised resolution == ground_truth)
  - win / tie / loss over per-case edit deltas
  - per-bucket edit deltas
And a cross-version head-to-head matrix (edit), so you can see the v1->v2->v2.1
trend at a glance.

Usage:
    python scripts/analyze_skill_versions.py \
        --baseline scripts/results/pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl \
        --version v1=scripts/results/qwen3-32b_v1_sysonly_clean.jsonl \
        --version v2=scripts/results/qwen3-32b_v2_python_tiny_sysonly_RAW.jsonl \
        --version v2.1=scripts/results/qwen3-32b_v2.1_python_tiny_sys.jsonl

Notes:
  - Rows whose bucket ends in "__resume" are collapsed onto the base bucket and
    de-duplicated by case_id (handles the accidental resume re-scores).
  - A "scored" row is one with no error and a non-null metrics.edit.
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from statistics import mean, median


def norm(s: str) -> str:
    return "\n".join(line.rstrip() for line in (s or "").strip().splitlines())


def load(path: str, condition: str | None):
    """Return {case_id: {edit, win, bucket, exact}} for scored rows of the
    chosen condition. `condition` None = take the single condition present
    (errors if the file is multi-condition and ambiguous)."""
    rows = [json.loads(l) for l in open(path)]

    # normalise the __resume bucket leak, then dedup by (case_id, condition)
    for r in rows:
        if r.get("bucket", "").endswith("__resume"):
            r["bucket"] = r["bucket"][: -len("__resume")]

    conds = {r["condition"] for r in rows}
    if condition is None:
        skill_conds = {c for c in conds if c != "no-skill"}
        if len(conds) == 1:
            condition = next(iter(conds))
        elif len(skill_conds) == 1:
            condition = next(iter(skill_conds))
        else:
            # prefer a *-sys skill condition
            sys_conds = {c for c in skill_conds if c.endswith("-sys")}
            if len(sys_conds) == 1:
                condition = next(iter(sys_conds))
            else:
                sys.exit(f"{path}: ambiguous conditions {sorted(conds)} — pass --condition")

    out = {}
    dup = 0
    for r in rows:
        if r["condition"] != condition:
            continue
        if r.get("error") or r["case_id"] in out:
            if r["case_id"] in out:
                dup += 1
            continue
        m = r.get("metrics") or {}
        if m.get("edit") is None:
            continue
        out[r["case_id"]] = {
            "edit": m["edit"],
            "win": m.get("winnowing"),
            "bucket": r.get("bucket", "?"),
            "exact": norm(r.get("resolution")) == norm(r.get("ground_truth")),
        }
    return out, condition, dup


def wtl(deltas, eps=1e-6):
    w = sum(1 for d in deltas if d > eps)
    l = sum(1 for d in deltas if d < -eps)
    return w, len(deltas) - w - l, l


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", required=True, help="no-skill baseline jsonl")
    ap.add_argument("--version", action="append", default=[], metavar="LABEL=PATH",
                    help="skill-version run, e.g. v2=results/...jsonl (repeatable)")
    ap.add_argument("--condition", default=None,
                    help="condition to score in version files (default: auto-pick the sys skill condition)")
    args = ap.parse_args()
    if not args.version:
        ap.error("need at least one --version LABEL=PATH")

    base, bcond, bdup = load(args.baseline, "no-skill")
    print(f"baseline: {len(base)} scored cases  (condition={bcond}"
          + (f", {bdup} dup dropped" if bdup else "") + ")\n")

    versions = {}  # label -> case_id -> dict
    for spec in args.version:
        if "=" not in spec:
            ap.error(f"--version must be LABEL=PATH, got {spec!r}")
        label, path = spec.split("=", 1)
        v, cond, dup = load(path, args.condition)
        versions[label] = v
        print(f"loaded {label}: {len(v)} scored cases  (condition={cond}"
              + (f", {dup} dup dropped" if dup else "") + ")")
    print()

    # ---- per-version vs baseline ----
    print("=" * 78)
    print("PAIRED vs no-skill baseline")
    print("=" * 78)
    for label, v in versions.items():
        common = sorted(set(v) & set(base))
        ed = [v[c]["edit"] - base[c]["edit"] for c in common]
        be, se = mean(base[c]["edit"] for c in common), mean(v[c]["edit"] for c in common)
        bw = [base[c]["win"] for c in common if base[c]["win"] is not None]
        sw = [v[c]["win"] for c in common if v[c]["win"] is not None]
        w, t, l = wtl(ed)
        bx = sum(base[c]["exact"] for c in common)
        sx = sum(v[c]["exact"] for c in common)
        print(f"\n[{label}]  n={len(common)} common scored cases")
        print(f"  edit-sim   : base {be:.4f}  skill {se:.4f}   delta {se-be:+.4f}")
        if bw and sw:
            print(f"  winnowing  : base {mean(bw):.4f}  skill {mean(sw):.4f}   delta {mean(sw)-mean(bw):+.4f}")
        print(f"  exact-match: base {bx} ({100*bx/len(common):.2f}%)  skill {sx} ({100*sx/len(common):.2f}%)")
        print(f"  per-case edit delta: mean {mean(ed):+.4f}  median {median(ed):+.4f}")
        print(f"  win/tie/loss: {w}/{t}/{l}  ({100*w/len(ed):.1f}% / {100*t/len(ed):.1f}% / {100*l/len(ed):.1f}%)")

        # per-bucket
        bb = defaultdict(lambda: {"b": [], "s": []})
        for c in common:
            bb[v[c]["bucket"]]["b"].append(base[c]["edit"])
            bb[v[c]["bucket"]]["s"].append(v[c]["edit"])
        print(f"  per-bucket edit (base -> skill, delta):")
        for bk in sorted(bb):
            d = bb[bk]
            print(f"     {bk:16}n={len(d['s']):<5} {mean(d['b']):.4f} -> {mean(d['s']):.4f}  {mean(d['s'])-mean(d['b']):+.4f}")

    # ---- cross-version head-to-head (edit) ----
    if len(versions) > 1:
        print("\n" + "=" * 78)
        print("CROSS-VERSION head-to-head (edit-sim, paired)")
        print("=" * 78)
        labels = list(versions)
        print(f"\n{'':10}" + "".join(f"{l:>12}" for l in labels))
        for a in labels:
            cells = []
            for b in labels:
                if a == b:
                    cells.append(f"{'—':>12}")
                    continue
                common = sorted(set(versions[a]) & set(versions[b]))
                d = mean(versions[a][c]["edit"] - versions[b][c]["edit"] for c in common)
                cells.append(f"{d:>+12.4f}")
            print(f"{a:10}" + "".join(cells))
        print("\n(cell = row mean - col mean; positive => row version scores higher)")


if __name__ == "__main__":
    main()
