"""
pilot.py — Pilot evaluation for Issue #8

Runs a small subset of ConGra cases through two conditions:
  - no-skill: default ConGra system prompt
  - skill-v1: SKILL.md content as system message

Usage:
    source /home/baebs/thesis/vllm-env/bin/activate
    python scripts/pilot.py --model qwen3
    python scripts/pilot.py --model apertus
"""

import argparse
import os
import json
import re
import time
from hashlib import sha1

from openai import OpenAI


# ── Model configs ─────────────────────────────────────────────────────────────

MODELS = {
    "qwen3": {
        "model_id":    "Qwen/Qwen3-8B",
        "results_file": "pilot_results_qwen3.jsonl",
        # Disable chain-of-thought thinking mode for cleaner output
        "extra_body":  {"chat_template_kwargs": {"enable_thinking": False}},
    },
    "apertus": {
        "model_id":    "swiss-ai/Apertus-8B-Instruct-2509",
        "results_file": "pilot_results_apertus.jsonl",
        "extra_body":  {},
    },
}


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
RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")

# ── Config ───────────────────────────────────────────────────────────────────
VLLM_BASE_URL = "http://localhost:8000/v1"
TEMPERATURE   = 0.0   # deterministic for reproducibility
MAX_TOKENS    = 2048
CONTEXT_LINES = 5     # lines of context around the conflict (ConGra default)
N_CASES       = 20    # how many cases to sample from meta_list.txt
LANGUAGE      = "python"

SKILL_PATH = os.path.join(REPO_ROOT, "skills", "merge-conflict-resolve-v1", "SKILL.md")

# ── ConGra default system prompt (from ConGra/src/prompt.py) ─────────────────
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


def load_skill_md(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        end = content.index("---", 3)
        content = content[end + 3:].strip()
    return content


def load_meta(data_root: str, n: int) -> list[dict]:
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


def call_vllm(client: OpenAI, model_id: str, system_prompt: str, user_prompt: str,
              extra_body: dict) -> str:
    kwargs = dict(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ],
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
    )
    if extra_body:
        kwargs["extra_body"] = extra_body
    response = client.chat.completions.create(**kwargs)
    return response.choices[0].message.content or ""


def score(resolution: str, ground_truth: str) -> dict:
    if not resolution.strip():
        return {"edit": None, "winnowing": None, "empty": True}
    return {
        "edit":      round(metric_edit_distance(resolution, ground_truth), 4),
        "winnowing": round(metric_winnowing(resolution, ground_truth), 4),
        "empty":     False,
    }


def prompt_echo_check(client: OpenAI, model_id: str, extra_body: dict) -> bool:
    """
    Sanity check: send a trivial request with a distinctive system prompt and
    confirm the model acknowledges it. Warns if the system prompt appears to be
    ignored. Returns True if the check passes.
    """
    marker = "SYSTEM_PROMPT_ECHO_TEST_XK9"
    try:
        response = call_vllm(
            client, model_id,
            system_prompt=f"Always begin your reply with the token: {marker}",
            user_prompt="Say hello.",
            extra_body=extra_body,
        )
        if marker in response:
            print(f"  [prompt-echo] PASS — model acknowledged system prompt")
            return True
        else:
            print(f"  [prompt-echo] WARN — system prompt may be ignored (marker not found in: {response[:100]!r})")
            return False
    except Exception as e:
        print(f"  [prompt-echo] ERROR — {e}")
        return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True, choices=list(MODELS.keys()),
                        help="Model to evaluate")
    parser.add_argument("--data-root", default=None,
                        help="Override path to congra_tiny_datasets/<lang>/<type>")
    args = parser.parse_args()

    cfg = MODELS[args.model]
    model_id    = cfg["model_id"]
    extra_body  = cfg["extra_body"]
    results_file = os.path.join(RESULTS_DIR, cfg["results_file"])

    data_root = args.data_root or os.path.join(
        CONGRA_ROOT, "data", "congra_tiny_datasets", "python", "func"
    )

    print(f"Model:       {model_id}")
    print(f"Results:     {results_file}")
    print(f"Data:        {data_root}")

    print(f"\nLoading SKILL.md from {SKILL_PATH}")
    skill_system_prompt = load_skill_md(SKILL_PATH)

    print(f"Loading {N_CASES} cases from {data_root}")
    cases = load_meta(data_root, N_CASES)
    print(f"  → {len(cases)} cases loaded")

    client = OpenAI(api_key="none", base_url=VLLM_BASE_URL)

    print("\nRunning prompt-echo sanity check...")
    prompt_echo_check(client, model_id, extra_body)

    conditions = [
        ("no-skill", CONGRA_SYSTEM_PROMPT),
        ("skill-v1", skill_system_prompt),
    ]

    os.makedirs(RESULTS_DIR, exist_ok=True)
    with open(results_file, "w", encoding="utf-8") as out:
        for i, case in enumerate(cases):
            source_path = os.path.join(CONGRA_ROOT, "data", "raw_datasets", case["source_path"])
            hash_file   = os.path.join(data_root, case["hash_idx"])

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
                    raw_response = call_vllm(client, model_id, system_prompt, user_prompt, extra_body)
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
                    "model":         model_id,
                    "resolution":    resolution,
                    "raw_response":  raw_response,
                    "ground_truth":  ground_truth,
                    "metrics":       metrics,
                    "elapsed_s":     elapsed,
                    "error":         error,
                }
                out.write(json.dumps(record) + "\n")
                out.flush()

    print(f"\nDone. Results saved to {results_file}")


if __name__ == "__main__":
    main()
