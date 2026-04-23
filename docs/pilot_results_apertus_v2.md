# Pilot Evaluation Results — Apertus-8B (v2, 3-condition)

**Date:** 2026-04-23
**Issue:** [#37](https://github.com/bdravec/merge-conflict-skill/issues/37)
**Script:** `scripts/pilot.py` · **Analysis:** `scripts/analyze_pilot.py`
**Results file:** `scripts/results/pilot_results_apertus_v2.jsonl`

> **Supersedes:** `docs/pilot_results_apertus.md` (2-condition run, 2026-04-22).
> The v1 run compared `no-skill` vs `skill-v1` (system injection only).
> This v2 run adds a third condition (`skill-v1-user`) and incorporates two
> pipeline fixes from issue #37: output cleaning (`extract_code_block`) and
> a system-prompt echo check (`prompt_echo_check`).

---

## Setup

- **Model:** Apertus-8B (`swiss-ai/Apertus-8B-Instruct-2509`) served via vLLM (`localhost:8000`)
- **Dataset:** 20 cases from `congra_tiny_datasets/python/func`
- **Conditions:**
  - `no-skill` — ConGra default system prompt, no skill content
  - `skill-v1-sys` — SKILL.md v1 content as system message (replaces default system prompt)
  - `skill-v1-user` — SKILL.md v1 content prepended to the user message, default system prompt kept
- **Metrics:** Edit distance similarity and winnowing similarity (from ConGra's `metrics.py`)
- **Temperature:** 0.0 (deterministic)
- **Output cleaning:** Model responses are passed through `extract_code_block()` before scoring — explanation text is stripped, only the fenced code block is evaluated

---

## Results

| Condition | N | Edit mean | Edit median | Edit stdev | Winn mean | Winn median | Winn stdev | Empty | Errors |
|-----------|---|-----------|-------------|------------|-----------|-------------|------------|-------|--------|
| no-skill | 20 | 0.2972 | 0.2897 | 0.1239 | 0.3971 | 0.4325 | 0.2001 | 0 | 0 |
| skill-v1-sys | 20 | 0.3002 | 0.2884 | 0.1449 | 0.3992 | 0.4406 | 0.1852 | 0 | 0 |
| skill-v1-user | 20 | 0.3028 | 0.3042 | 0.1427 | 0.3974 | 0.4339 | 0.1829 | 0 | 0 |

**Identical outputs (no-skill vs skill-v1-sys): 9/20 cases**
**Identical outputs (no-skill vs skill-v1-user): 8/20 cases**

**Cases above 0.80 correctness threshold: 0/20 in all conditions**

### Per-case edit delta — skill-v1-sys − no-skill

Positive = skill better.

| Case | Δ edit | Δ winn | Direction |
|------|--------|--------|-----------|
| 0xa4d50e39def807dd | +0.2264 | +0.3564 | ↑ skill better |
| 0xe63ff0ddae988357 | +0.2192 | +0.0460 | ↑ skill better |
| 0x8e6579cb86af64a8 | +0.0073 | +0.0338 | ↑ skill better |
| 0x425cf8014eda936b | +0.0015 | +0.0009 | ↑ skill better |
| 0xc00c4d82b7364e6d | +0.0013 | −0.0018 | ↑ skill better (edit only) |
| 0x6081a18de8689da7 | +0.0000 | +0.0000 | = [identical] |
| 0x6cdd08d5f0b0b367 | +0.0000 | +0.0000 | = [identical] |
| 0xd752694df9c5ba20 | +0.0000 | +0.0000 | = [identical] |
| 0x96d20e6c9b0f2395 | +0.0000 | +0.0000 | = [identical] |
| 0x999797db0c12ab9d | +0.0000 | +0.0000 | = [identical] |
| 0x7fb96fbf0a030ea  | +0.0000 | +0.0000 | = [identical] |
| 0xc6a534710cc98bb7 | +0.0000 | +0.0000 | = [identical] |
| 0x32d8c89b39c2860b | +0.0000 | +0.0000 | = [identical] |
| 0x2b864c36d694436b | +0.0000 | +0.0000 | = [identical] |
| 0xbe50e025d8e4d344 | −0.0030 | −0.0011 | ↓ skill worse |
| 0xe4ff79aa2f3f8922 | −0.0182 | −0.0374 | ↓ skill worse |
| 0xddd5322de12565fe | −0.0274 | +0.0431 | ↓ edit worse / ↑ winn better |
| 0x520debc691c88dc5 | −0.0625 | −0.0276 | ↓ skill worse |
| 0xd9272c5e0e8f15ee | −0.1116 | −0.2427 | ↓ skill worse |
| 0x223b29598e1c5cb9 | −0.1734 | −0.1287 | ↓ skill worse |

skill-v1-sys better: 5 · worse: 6 · identical: 9

### Per-case edit delta — skill-v1-user − no-skill

| Case | Δ edit | Δ winn | Direction |
|------|--------|--------|-----------|
| 0xa4d50e39def807dd | +0.2264 | +0.3564 | ↑ skill better |
| 0xe63ff0ddae988357 | +0.2192 | +0.0460 | ↑ skill better |
| 0x7fb96fbf0a030ea  | +0.0814 | −0.0206 | ↑ edit better / ↓ winn worse |
| 0x8e6579cb86af64a8 | +0.0073 | +0.0338 | ↑ skill better |
| 0xc00c4d82b7364e6d | +0.0047 | +0.0024 | ↑ skill better |
| 0x425cf8014eda936b | +0.0015 | +0.0009 | ↑ skill better |
| 0xbe50e025d8e4d344 | +0.0014 | −0.0011 | ↑ edit better / ↓ winn worse |
| 0x6081a18de8689da7 | +0.0000 | +0.0000 | = [identical] |
| 0x6cdd08d5f0b0b367 | +0.0000 | +0.0000 | = [identical] |
| 0xd752694df9c5ba20 | +0.0000 | +0.0000 | = [identical] |
| 0x96d20e6c9b0f2395 | +0.0000 | +0.0000 | = [identical] |
| 0x999797db0c12ab9d | +0.0000 | +0.0000 | = [identical] |
| 0xc6a534710cc98bb7 | +0.0000 | +0.0000 | = [identical] |
| 0x32d8c89b39c2860b | +0.0000 | +0.0000 | = [identical] |
| 0x2b864c36d694436b | +0.0000 | +0.0000 | = [identical] |
| 0xddd5322de12565fe | −0.0059 | +0.0528 | ↓ edit worse / ↑ winn better |
| 0x520debc691c88dc5 | −0.0625 | −0.0276 | ↓ skill worse |
| 0xe4ff79aa2f3f8922 | −0.0771 | −0.0660 | ↓ skill worse |
| 0xd9272c5e0e8f15ee | −0.1116 | −0.2427 | ↓ skill worse |
| 0x223b29598e1c5cb9 | −0.1734 | −0.1287 | ↓ skill worse |

skill-v1-user better: 7 · worse: 5 · identical: 8

---

## Findings

**skill-v1-user marginally outperforms skill-v1-sys.** User injection yields 7 wins / 5 losses vs system injection's 5 wins / 6 losses. Mean edit improvement is +0.006 (user) vs +0.003 (sys) over no-skill. Both are well within noise at n=20.

**Two outliers drive essentially all positive signal.** Cases `0xa4d50e39def807dd` (+0.23) and `0xe63ff0ddae988357` (+0.22) account for nearly all of the positive delta in both conditions. Both improve because the skill prompted a shorter, more focused response — the no-skill response was 2–3× longer than the ground truth, inflating the edit distance denominator. Removing these two cases would leave both skill conditions with neutral-to-negative averages.

**System prompt is being passed correctly — identical outputs are not a pipeline bug.** `prompt_echo_check()` passed before the run. skill-v1-user still produces 8/20 identical outputs despite injecting the skill into the user message where it cannot be ignored at the model level. Apertus-8B simply converges to the same resolution for these cases regardless of instruction context.

**0/20 cases above 0.80 threshold across all conditions.** This is unchanged from the v1 pilot. It confirms a model capability ceiling at 8B scale on `func`-type conflicts, not a pipeline issue.

**skill-v1-sys numbers are identical to the v1 pilot.** `no-skill` and `skill-v1-sys` in this run match the v1 pilot exactly, confirming the pipeline is deterministic (temperature=0.0) and that output cleaning did not change scores for Apertus (its responses were already being extracted from code blocks correctly in most cases).

---

## Comparison with Qwen3-8B v2

| Metric | Qwen3 no-skill | Qwen3 skill-v1-sys | Qwen3 skill-v1-user | Apertus no-skill | Apertus skill-v1-sys | Apertus skill-v1-user |
|--------|----------------|--------------------|---------------------|------------------|----------------------|-----------------------|
| Edit mean | 0.3953 | 0.3479 | 0.3511 | 0.2972 | 0.3002 | 0.3028 |
| Edit median | 0.3660 | 0.3822 | 0.3465 | 0.2897 | 0.2884 | 0.3042 |
| Winn mean | 0.4782 | 0.4296 | 0.4572 | 0.3971 | 0.3992 | 0.3974 |
| Above 0.80 | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 | 0/20 |
| Identical | 6/20 (sys) | — | 5/20 (user) | 9/20 (sys) | — | 8/20 (user) |
| Skill wins | — | 4 | 4 | — | 5 | 7 |
| Skill losses | — | 8 | 7 | — | 6 | 5 |

**Qwen3-8B is the stronger baseline at 8B scale.** Its no-skill edit mean (0.3953) is higher than Apertus's best condition (0.3028). For Qwen3, skill-v1 consistently *hurts* performance; for Apertus, the effect is near-zero with a slight positive lean from user injection.

---

## Pipeline Validation (Issue #37)

| Criterion | Status |
|-----------|--------|
| System prompt reaching model correctly | ✅ `prompt_echo_check()` passes |
| Output-cleaning step added | ✅ `extract_code_block()` strips explanation text |
| Re-run analysis with cleaned outputs | ✅ This document |
| Decision: ready to scale? | ✅ Yes — see below |

**Pipeline is ready to scale to the full tiny dataset.** All three pipeline issues from #37 are resolved. The weak skill effect is a property of SKILL.md v1 and the model, not the pipeline. Next step is evaluating SKILL.md v2.

---

## Next Steps

- Write SKILL.md v2 (issue #6) and re-run the 3-condition pilot
- Scale to full tiny dataset (issue #9)
- Test on additional conflict types (`text`, `sytx`)
