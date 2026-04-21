"""
pilot.py — Pilot evaluation for Issue #8

Runs a small subset of ConGra cases through two conditions:
  - no-skill: default ConGra system prompt
  - skill-v1: SKILL.md content as system message

For each case × condition, calls the local vLLM server (OpenAI-compatible API),
extracts the resolution, scores it with edit distance and winnowing similarity,
and writes results to JSONL.

Usage:
    # Start vLLM in a separate terminal first:
    #   vllm serve Qwen/Qwen3-8B --port 8000 --max-model-len 32768
    source /home/baebs/thesis/vllm-env/bin/activate
    python scripts/pilot.py

Output: scripts/results/pilot_results.jsonl
"""

import os
import json
import re
import time
from hashlib import sha1

from openai import OpenAI


# ── Inlined from ConGra/src/metrics.py ───────────────────────────────────────
# Copied directly to avoid importing ConGra's full dependency tree (langchain etc.)

def _remove_invisible(s: str) -> str:
    return re.sub(r"[\s\x00-\x1f\x7f-\x9f]+", "", s)

def metric_edit_distance(gen: str, ref: str) -> float:
    gen, ref = _remove_invisible(gen), _remove_invisible(ref)
    if not gen or not ref:
        return 0.0
    m, n = len(gen), len(ref)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, n + 1):
            temp = dp[j]
            dp[j] = prev if gen[i-1] == ref[j-1] else min(dp[j], dp[j-1], prev) + 1
            prev = temp
    return 1.0 - dp[n] / max(m, n)

def metric_winnowing(gen: str, ref: str) -> float:
    gen, ref = _remove_invisible(gen), _remove_invisible(ref)
    if not gen or not ref:
        # ConGra returns 1.0 for one-sided empty — wrong. We return 0.0.
        return 0.0
    k, w = 5, 4
    def fingerprint(text):
        kgrams = zip(*[text[i:] for i in range(k)])
        hashes = [(int(sha1("".join(kg).encode()).hexdigest()[-4:], 16), i)
                  for i, kg in enumerate(kgrams)]
        windows = zip(*[hashes[i:] for i in range(w)])
        seen, result = None, []
        for win in windows:
            m = min(win, key=lambda x: (x[0], -x[1]))
            if m != seen:
                result.append(m[0])
                seen = m
        return result
    a, b = fingerprint(gen), fingerprint(ref)
    sa, sb = set(a), set(b)
    intersect = sum(1 for x in a if x in sb) + sum(1 for x in b if x in sa)
    union = len(a) + len(b)
    return intersect / union if union else 0.0


# ── Inlined from ConGra/src/utils.py: load_conflict_and_answer ───────────────

def load_conflict_and_answer(source_path: str, file_path: str, k: int, n: int):
    """
    Returns (conflict_context, conflict_text, resolved_text) for conflict #k
    in the given file, with n lines of surrounding context.
    source_path: full path to the merged_without_base file (used to locate
                 .region and resolved files via path substitution).
    file_path:   full path to the hash file in congra_tiny_datasets.
    """
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

    resolved_path = source_path.replace("merged_without_base", "resolved").replace("regions", "resolved")
    with open(resolved_path, "r", encoding="utf-8", errors="ignore") as f:
        rlines = f.read().split("\n")
    rstart, rend = region[2] - 1, region[3]
    resolved_text = "\n".join(rlines[max(0, rstart):rend])

    return conflict_context, conflict_text, resolved_text

# ── Paths ────────────────────────────────────────────────────────────────────
REPO_ROOT   = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONGRA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../ConGra"))

DATA_ROOT   = os.path.join(CONGRA_ROOT, "data", "congra_tiny_datasets", "python", "func")
RAW_ROOT    = os.path.join(CONGRA_ROOT, "data", "raw_datasets")
SKILL_PATH  = os.path.join(REPO_ROOT, "skills", "merge-conflict-resolve-v1", "SKILL.md")
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
RESULTS_FILE = os.path.join(RESULTS_DIR, "pilot_results.jsonl")

# ── Config ───────────────────────────────────────────────────────────────────
MODEL_ID      = "Qwen/Qwen3-8B"
VLLM_BASE_URL = "http://localhost:8000/v1"
TEMPERATURE   = 0.0   # deterministic for reproducibility
MAX_TOKENS    = 2048
CONTEXT_LINES = 5     # lines of context around the conflict (ConGra default)
N_CASES       = 20    # how many cases to sample from meta_list.txt
LANGUAGE      = "python"

# ── ConGra default system prompt (from ConGra/src/prompt.py) ─────────────────
CONGRA_SYSTEM_PROMPT = (
    "You are an expert in code merge conflicts, "
    "providing the merged code based on the conflict and its context."
)

# ConGra's user prompt template (simplified: always use context version)
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


def load_skill_md(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        end = content.index("---", 3)
        content = content[end + 3:].strip()
    return content


def load_meta(data_root: str, n: int) -> list[dict]:
    """
    Read meta_list.txt and return up to n cases as dicts.
    Each line: source_path: hash_idx: conflict_idx
    """
    meta_path = os.path.join(data_root, "meta_list.txt")
    cases = []
    with open(meta_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(": ")
            if len(parts) != 3:
                continue
            source_path, hash_idx, conflict_idx = parts
            cases.append({
                "source_path": source_path,
                "hash_idx": hash_idx,
                "conflict_idx": int(conflict_idx),
            })
            if len(cases) >= n:
                break
    return cases


def extract_code_block(text: str) -> str:
    """Extract the first fenced code block from the model response."""
    match = re.search(r"```(?:\w+)?\n([\s\S]*?)```", text)
    if match:
        return match.group(1).strip()
    return ""


def call_vllm(client: OpenAI, system_prompt: str, user_prompt: str) -> str:
    """Send a chat completion request to vLLM and return the raw response text."""
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        # Disable Qwen3 chain-of-thought thinking mode for cleaner output
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    )
    return response.choices[0].message.content or ""


def score(resolution: str, ground_truth: str) -> dict:
    """
    Compute edit distance and winnowing similarity.
    Empty resolutions are flagged separately rather than scored — the winnowing
    bug (returns 1.0 for empty strings) would otherwise inflate scores.
    """
    if not resolution.strip():
        return {"edit": None, "winnowing": None, "empty": True}
    return {
        "edit":      round(metric_edit_distance(resolution, ground_truth), 4),
        "winnowing": round(metric_winnowing(resolution, ground_truth), 4),
        "empty":     False,
    }


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print(f"Loading SKILL.md from {SKILL_PATH}")
    skill_system_prompt = load_skill_md(SKILL_PATH)

    print(f"Loading {N_CASES} cases from {DATA_ROOT}")
    cases = load_meta(DATA_ROOT, N_CASES)
    print(f"  → {len(cases)} cases loaded")

    client = OpenAI(api_key="none", base_url=VLLM_BASE_URL)

    conditions = [
        ("no-skill", CONGRA_SYSTEM_PROMPT),
        ("skill-v1", skill_system_prompt),
    ]

    with open(RESULTS_FILE, "w", encoding="utf-8") as out:
        for i, case in enumerate(cases):
            # Build the full source path that load_conflict_and_answer expects
            source_path = os.path.join(RAW_ROOT, case["source_path"])
            hash_file   = os.path.join(DATA_ROOT, case["hash_idx"])

            print(f"\n[{i+1}/{len(cases)}] {case['hash_idx']} conflict #{case['conflict_idx']}")

            try:
                conflict_context, conflict_text, ground_truth = load_conflict_and_answer(
                    source_path, hash_file, case["conflict_idx"], CONTEXT_LINES
                )
            except Exception as e:
                print(f"  SKIP — failed to load: {e}")
                continue

            user_prompt = CONGRA_USER_TEMPLATE.format(
                language=LANGUAGE,
                conflict_context=conflict_context,
                conflict_text=conflict_text,
            )

            for condition_name, system_prompt in conditions:
                print(f"  condition: {condition_name} ... ", end="", flush=True)
                t0 = time.time()

                try:
                    raw_response = call_vllm(client, system_prompt, user_prompt)
                    resolution   = extract_code_block(raw_response)
                    metrics      = score(resolution, ground_truth)
                    elapsed      = round(time.time() - t0, 2)
                    error        = None
                except Exception as e:
                    raw_response = ""
                    resolution   = ""
                    metrics      = {"edit": None, "winnowing": None, "empty": None}
                    elapsed      = round(time.time() - t0, 2)
                    error        = str(e)

                print(f"edit={metrics['edit']}  winnowing={metrics['winnowing']}  ({elapsed}s)")

                record = {
                    "case_id":       case["hash_idx"],
                    "conflict_idx":  case["conflict_idx"],
                    "condition":     condition_name,
                    "model":         MODEL_ID,
                    "resolution":    resolution,
                    "ground_truth":  ground_truth,
                    "metrics":       metrics,
                    "elapsed_s":     elapsed,
                    "error":         error,
                }
                out.write(json.dumps(record) + "\n")
                out.flush()

    print(f"\nDone. Results saved to {RESULTS_FILE}")


if __name__ == "__main__":
    main()
