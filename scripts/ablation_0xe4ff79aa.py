"""
ablation_0xe4ff79aa.py — Diagnostic ablation for issue #44 / rec 7

One case (0xe4ff79aa) × Qwen3-8B × 4 prompt conditions × 1 sampling run
(TEMPERATURE=0.0, matches pilot.py).

Tests whether explicit pick-criterion prompting flips Qwen3 from picking
`poolsize` (wrong) to picking `pool_size` (correct, matches GT).

Conditions:
  1. baseline-v2:              v2 SKILL as-is (replicates pilot failure)
  2. v2 + explicit answer:     v2 SKILL + "Surrounding code uses underscores; pick `pool_size`."
  3. v2 + criterion hint:      v2 SKILL + "Examine surrounding code's identifier style before picking."
  4. v2 + worked example:      v2 SKILL + Keras-vs-TF identifier-divergence worked example

Interpretation:
  - If condition 2 fails (still picks b) → H2 (model-level capability ceiling).
  - If condition 2 succeeds but 3/4 fail → prompt-level fixable, but rec-3 example needs strengthening.
  - If condition 4 succeeds → the proposed rec-3 worked example transfers to this case.

Usage:
    source /home/baebs/thesis/vllm-env/bin/activate
    # Make sure Qwen3-8B is being served (port 8000):
    #   pkill -f "vllm serve"
    #   export HF_HUB_OFFLINE=1
    #   vllm serve Qwen/Qwen3-8B --port 8000 --max-model-len 32768 &
    python scripts/ablation_0xe4ff79aa.py
"""

import json
import os
import sys
import time

from openai import OpenAI

# Reuse pilot.py helpers
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pilot import (
    MODELS, VLLM_BASE_URL, RESULTS_DIR, CONGRA_ROOT,
    CONGRA_USER_TEMPLATE,
    load_conflict_and_answer, load_skill_md, call_vllm,
    extract_code_block, score, skill_path_for,
)

# ── Config ────────────────────────────────────────────────────────────────────

CASE_ID         = "0xe4ff79aa2f3f8922"
CONFLICT_IDX    = 1
CONTEXT_LINES   = 5
LANGUAGE        = "python"
MODEL_KEY       = "qwen3"   # rec 7 target — Qwen3 is the model that fails this case
SKILL_VERSION   = "v2"

DATA_ROOT   = os.path.join(CONGRA_ROOT, "data", "congra_tiny_datasets", "python", "func")
SOURCE_PATH = "Python/keras/conflict_files_62/merged_without_base/convolutional.py"


# ── Condition-specific additions to the v2 SKILL ──────────────────────────────

EXPLICIT_ANSWER_HINT = """

## Hint specific to this case

The surrounding code in this file uses underscores in identifiers (e.g. `pool_size`-style, not `poolsize`-style). The correct pick is `pool_size`.
"""

CRITERION_ONLY_HINT = """

## Hint specific to this case

Examine the surrounding code's identifier style before picking. Match the convention used in the rest of the file.
"""

WORKED_EXAMPLE = """

## Additional worked example

### Pick — identifier divergence with surrounding-code style as tiebreaker

```
<<<<<<< a
j_tf = K.placeholder(shape=(None, 32), dtype=K.floatx())
=======
j_tf = tf.placeholder(dtype=K.floatx())
>>>>>>> b
```

The surrounding code uses `K.` prefixes (`K.int_shape`, `K.floatx`). Pick a — its API style matches the rest of the file. Do not pick b just because it is shorter.
"""


# ── Pick-side detection ───────────────────────────────────────────────────────

def detect_pick(resolution: str) -> str:
    """For 0xe4ff79aa: returns 'a' (pool_size), 'b' (poolsize), 'hybrid', or 'none'.

    `pool_size` contains an underscore; `poolsize` does not. The two strings do
    not overlap as substrings, so a simple `in` check is reliable.
    """
    has_pool_size = "pool_size" in resolution
    has_poolsize  = "poolsize" in resolution
    if has_pool_size and not has_poolsize:
        return "a"
    if has_poolsize and not has_pool_size:
        return "b"
    if has_pool_size and has_poolsize:
        return "hybrid"
    return "none"


# ── Conditions ────────────────────────────────────────────────────────────────

def build_conditions(skill_v2: str) -> list[tuple[str, str]]:
    """Returns [(condition_name, system_prompt), ...] for the 4 conditions."""
    return [
        ("baseline-v2",              skill_v2),
        ("v2-plus-explicit-answer",  skill_v2 + EXPLICIT_ANSWER_HINT),
        ("v2-plus-criterion-hint",   skill_v2 + CRITERION_ONLY_HINT),
        ("v2-plus-worked-example",   skill_v2 + WORKED_EXAMPLE),
    ]


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    cfg        = MODELS[MODEL_KEY]
    model_id   = cfg["model_id"]
    extra_body = cfg["extra_body"]

    skill_path = skill_path_for(SKILL_VERSION)
    skill_v2   = load_skill_md(skill_path)

    source_full = os.path.join(CONGRA_ROOT, "data", "raw_datasets", SOURCE_PATH)
    hash_file   = os.path.join(DATA_ROOT, CASE_ID)

    print(f"Model:       {model_id}")
    print(f"Case:        {CASE_ID} (conflict #{CONFLICT_IDX})")
    print(f"Skill:       {SKILL_VERSION} ({skill_path})")

    conflict_context, conflict_text, ground_truth = load_conflict_and_answer(
        source_full, hash_file, CONFLICT_IDX, CONTEXT_LINES,
    )

    user_prompt = CONGRA_USER_TEMPLATE.format(
        language=LANGUAGE,
        conflict_context=conflict_context,
        conflict_text=conflict_text,
    )

    conditions = build_conditions(skill_v2)
    client = OpenAI(api_key="none", base_url=VLLM_BASE_URL)

    results_file = os.path.join(RESULTS_DIR, f"ablation_{CASE_ID}.jsonl")
    os.makedirs(RESULTS_DIR, exist_ok=True)

    print(f"\nRunning {len(conditions)} conditions, results → {results_file}\n")

    records = []
    with open(results_file, "w") as out:
        for condition_name, system_prompt in conditions:
            print(f"  [{condition_name}] ... ", end="", flush=True)
            t0 = time.time()

            try:
                raw_response = call_vllm(client, model_id, system_prompt, user_prompt, extra_body)
                resolution   = extract_code_block(raw_response)
                metrics      = score(resolution, ground_truth)
                pick         = detect_pick(resolution)
                elapsed      = round(time.time() - t0, 2)
                error        = None
            except Exception as e:
                raw_response = ""
                resolution   = ""
                metrics      = {"edit": None, "winnowing": None, "empty": None}
                pick         = "error"
                elapsed      = round(time.time() - t0, 2)
                error        = str(e)

            print(f"pick={pick:<6}  edit={metrics['edit']}  ({elapsed}s)")

            record = {
                "case_id":       CASE_ID,
                "conflict_idx":  CONFLICT_IDX,
                "condition":     condition_name,
                "model":         model_id,
                "pick":          pick,
                "resolution":    resolution,
                "raw_response":  raw_response,
                "ground_truth":  ground_truth,
                "metrics":       metrics,
                "elapsed_s":     elapsed,
                "error":         error,
                "system_prompt": system_prompt,
            }
            records.append(record)
            out.write(json.dumps(record) + "\n")
            out.flush()

    # ── Verdict summary ──
    print("\n--- Verdict ---")
    print(f"{'condition':<28} {'pick':<8} {'edit':>8}  flipped?")
    print("-" * 64)
    baseline_pick = next(r["pick"] for r in records if r["condition"] == "baseline-v2")
    for r in records:
        cond, pick = r["condition"], r["pick"]
        edit = r["metrics"]["edit"]
        edit_str = f"{edit}" if edit is not None else "err"
        if cond == "baseline-v2":
            flipped = "(baseline)"
        elif pick == "a" and baseline_pick == "b":
            flipped = "YES (b→a)"
        elif pick == baseline_pick:
            flipped = "no"
        else:
            flipped = f"({baseline_pick}→{pick})"
        print(f"{cond:<28} {pick:<8} {edit_str:>8}  {flipped}")

    print(f"\nDone. Raw results in {results_file}")


if __name__ == "__main__":
    main()
