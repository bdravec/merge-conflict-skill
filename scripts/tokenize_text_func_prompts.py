"""
tokenize_text_func_prompts.py — refs #59

Tokenize every prompt pilot.py would send for bucket=text+func, skill=v1,
no vLLM hit. Output CSV + console summary cross-referenced against the c=1
rerun's 19 errored cases.

Run from repo root with vllm-env:
    /home/baebs/thesis/vllm-env/bin/python scripts/tokenize_text_func_prompts.py
"""

import json
import os
import re
import sys
from collections import Counter

from transformers import AutoTokenizer

# ── Mirror pilot.py constants/paths ──────────────────────────────────────────
REPO_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONGRA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../ConGra"))
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
DATA_ROOT   = os.path.join(CONGRA_ROOT, "data", "congra_tiny_datasets", "python", "text+func")
RAW_ROOT    = os.path.join(CONGRA_ROOT, "data", "raw_datasets")
SKILL_PATH  = os.path.join(REPO_ROOT, "skills", "merge-conflict-resolve-v1", "SKILL.md")
RERUN_JSONL = os.path.join(RESULTS_DIR, "pilot_results_apertus_v1_python_tiny_rerun_text+func.jsonl")
OUT_CSV     = os.path.join(RESULTS_DIR, "text_func_prompt_lengths.csv")

MODEL_ID      = "swiss-ai/Apertus-8B-Instruct-2509"
CONTEXT_LINES = 5
MAX_TOKENS    = 2048      # pilot.py
MAX_MODEL_LEN = 32768     # vLLM config
EFFECTIVE_CAP = MAX_MODEL_LEN - MAX_TOKENS   # 30720 — over this and vLLM 400s

CONGRA_SYSTEM_PROMPT = (
    "You are an expert in code merge conflicts, "
    "providing the merged code based on the conflict and its context."
)

CONGRA_USER_TEMPLATE = """\
Please provide the merged code based on the specified conflict and its context.
Please provide the merged code following the chain of thought:
1. Understand the cause of the conflict: Examine the conflicting code and its context to understand why the conflict occurred.
2. Decide how to merge: Based on the functionality and logic of the code, determine which changes should be kept or how the changes from both sides can be combined.
3. Provide the merged code, using "```{language}" as the beginning and "```" as the end of the merged code. You only need to output the resolution of the conflict without providing any context.

Here is the context related to the conflict:
```{language}
{conflict_context}
```
Here is the conflict that needs to be resolved:
```{language}
{conflict_text}
```
"""


def load_conflict_and_answer(source_path, file_path, k, n):
    region_path = source_path.replace("merged_without_base", "regions") + ".region"
    regions = []
    with open(region_path, "r") as f:
        for line in f:
            if "#" in line:
                continue
            line = line.strip()
            if line:
                regions.append(eval(line))
    region = regions[k - 1]
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.read().split("\n")
    start, end = region[0] - 1, region[1]
    conflict_text    = "\n".join(lines[start:end])
    conflict_context = "\n".join(lines[max(0, start - n):end + n])
    return conflict_context, conflict_text


def load_meta(data_root):
    cases = []
    with open(os.path.join(data_root, "meta_list.txt"), "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(": ")
            if len(parts) != 3:
                continue
            source_path, hash_idx, conflict_idx = parts
            cases.append({
                "source_path":  source_path,
                "hash_idx":     hash_idx,
                "conflict_idx": int(conflict_idx),
            })
    return cases


def load_skill_md(path):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        end = content.index("---", 3)
        content = content[end + 3:].strip()
    return content


def errored_cases_from_rerun():
    """Map case_id → set of conditions that errored in the c=1 rerun JSONL."""
    if not os.path.exists(RERUN_JSONL):
        return {}
    errored = {}
    for line in open(RERUN_JSONL):
        r = json.loads(line)
        if r["error"]:
            errored.setdefault(r["case_id"], {})[r["condition"]] = r["error"][:60]
    return errored


def main():
    print(f"Loading tokenizer {MODEL_ID}...", file=sys.stderr)
    tok = AutoTokenizer.from_pretrained(MODEL_ID)
    skill_text = load_skill_md(SKILL_PATH)
    cases = load_meta(DATA_ROOT)
    errored = errored_cases_from_rerun()
    print(f"  cases: {len(cases)}", file=sys.stderr)
    print(f"  skill_text chars: {len(skill_text)}", file=sys.stderr)
    print(f"  errored cases in rerun JSONL: {len(errored)}", file=sys.stderr)

    rows = []
    skipped = 0
    for case in cases:
        source_path = os.path.join(RAW_ROOT, case["source_path"])
        hash_file   = os.path.join(DATA_ROOT, case["hash_idx"])
        try:
            ctx, conflict = load_conflict_and_answer(
                source_path, hash_file, case["conflict_idx"], CONTEXT_LINES
            )
        except Exception as e:
            skipped += 1
            continue
        user_prompt = CONGRA_USER_TEMPLATE.format(
            language="python", conflict_context=ctx, conflict_text=conflict
        )
        conditions = [
            ("no-skill",      CONGRA_SYSTEM_PROMPT, user_prompt),
            ("skill-v1-sys",  skill_text,           user_prompt),
            ("skill-v1-user", CONGRA_SYSTEM_PROMPT, f"{skill_text}\n\n{user_prompt}"),
        ]
        for cond, sys_prompt, full_user in conditions:
            msgs = [
                {"role": "system", "content": sys_prompt},
                {"role": "user",   "content": full_user},
            ]
            ids = tok.apply_chat_template(
                msgs, add_generation_prompt=True, tokenize=True,
            )
            rows.append({
                "case_id":      case["hash_idx"],
                "conflict_idx": case["conflict_idx"],
                "condition":    cond,
                "n_tokens":     len(ids),
                "errored":      cond in errored.get(case["hash_idx"], {}),
            })

    print(f"  skipped (load failure): {skipped}", file=sys.stderr)

    # Write CSV
    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(OUT_CSV, "w") as f:
        f.write("case_id,conflict_idx,condition,n_tokens,errored\n")
        for r in rows:
            f.write(f"{r['case_id']},{r['conflict_idx']},{r['condition']},"
                    f"{r['n_tokens']},{int(r['errored'])}\n")
    print(f"  wrote {len(rows)} rows → {OUT_CSV}", file=sys.stderr)

    # ── Summary ──────────────────────────────────────────────────────────
    print()
    print("=" * 78)
    print(f"PROMPT LENGTH SUMMARY  (bucket=text+func, model=Apertus, "
          f"effective cap={EFFECTIVE_CAP} tokens)")
    print("=" * 78)

    by_cond = {}
    for r in rows:
        by_cond.setdefault(r["condition"], []).append(r["n_tokens"])
    for cond in ["no-skill", "skill-v1-sys", "skill-v1-user"]:
        ns = sorted(by_cond[cond])
        n  = len(ns)
        print(f"\n[{cond}] n={n}")
        print(f"  min={ns[0]}  p25={ns[n//4]}  median={ns[n//2]}  "
              f"p75={ns[3*n//4]}  p90={ns[int(0.9*n)]}  "
              f"p99={ns[min(n-1,int(0.99*n))]}  max={ns[-1]}")
        thresholds = [8192, 16384, 20480, 24576, 30720, MAX_MODEL_LEN]
        for t in thresholds:
            over = sum(1 for x in ns if x > t)
            print(f"  > {t:6d}: {over:4d} cases ({100*over/n:5.1f}%)")

    # ── Errored-vs-clean comparison ──────────────────────────────────────
    print()
    print("=" * 78)
    print("ERRORED CASES vs CLEAN CASES  (c=1 rerun, rows 0–263 attempted)")
    print("=" * 78)
    attempted = set()
    for line in open(RERUN_JSONL):
        r = json.loads(line)
        attempted.add(r["case_id"])
    print(f"\nAttempted in rerun: {len(attempted)} cases  "
          f"(of which errored: {len(errored)})")
    print()
    print(f"{'case_id':<22}  {'cf#':>3}  {'no-skill':>10}  "
          f"{'sys':>10}  {'user':>10}  err?  err_kind")
    print("-" * 78)
    by_case = {}
    for r in rows:
        by_case.setdefault((r["case_id"], r["conflict_idx"]), {})[r["condition"]] = r["n_tokens"]
    # Sort: errored first (longest no-skill desc), then clean attempted (longest first)
    attempted_rows = []
    for (cid, ci), conds in by_case.items():
        if cid not in attempted:
            continue
        ek = ""
        if cid in errored:
            kinds = {v.split(":")[0].split(".")[0].strip().lower()
                     for v in errored[cid].values()}
            ek = "/".join(sorted(kinds))
        attempted_rows.append((
            cid in errored, conds["no-skill"], cid, ci, conds, ek
        ))
    attempted_rows.sort(key=lambda x: (not x[0], -x[1]))
    for is_err, _ns, cid, ci, conds, ek in attempted_rows:
        marker = "ERR" if is_err else "   "
        print(f"{cid:<22}  {ci:>3}  {conds['no-skill']:>10}  "
              f"{conds['skill-v1-sys']:>10}  {conds['skill-v1-user']:>10}  "
              f"{marker}   {ek}")

    # ── Verdict ──────────────────────────────────────────────────────────
    print()
    print("=" * 78)
    err_lens = [conds["skill-v1-user"]
                for (cid, _ci), conds in by_case.items() if cid in errored]
    clean_attempted_lens = [conds["skill-v1-user"]
                            for (cid, _ci), conds in by_case.items()
                            if cid in attempted and cid not in errored]
    if err_lens and clean_attempted_lens:
        err_lens.sort(); clean_attempted_lens.sort()
        e_med = err_lens[len(err_lens)//2]
        c_med = clean_attempted_lens[len(clean_attempted_lens)//2]
        e_max = err_lens[-1]
        c_max = clean_attempted_lens[-1]
        print(f"skill-v1-user median: errored={e_med}  clean-attempted={c_med}")
        print(f"skill-v1-user max:    errored={e_max}  clean-attempted={c_max}")

if __name__ == "__main__":
    main()
