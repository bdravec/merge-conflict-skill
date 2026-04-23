# Pilot Results — Summary

This document summarises all pilot evaluation runs. Each run tested 20 cases from `congra_tiny_datasets/python/func`, temperature=0.0, served via vLLM on a local GPU.

For full per-case breakdowns see the individual docs:
- [`pilot_results_qwen3_v2.md`](pilot_results_qwen3_v2.md) — Qwen3-8B, 3-condition (supersedes original Qwen3 v1 run)
- [`pilot_results_apertus_v2.md`](pilot_results_apertus_v2.md) — Apertus-8B, 3-condition (supersedes `pilot_results_apertus.md`)

---

## Conditions

| Condition | Description |
|-----------|-------------|
| `no-skill` | ConGra default system prompt, no skill content |
| `skill-v1-sys` | SKILL.md v1 replaces the system message |
| `skill-v1-user` | SKILL.md v1 prepended to the user message; default system prompt kept |

---

## Results at a Glance

| Model | Condition | Edit mean | Edit median | Winn mean | Above 0.80 | Identical | Skill wins | Skill losses |
|-------|-----------|-----------|-------------|-----------|------------|-----------|------------|--------------|
| Qwen3-8B | no-skill | 0.3953 | 0.3660 | 0.4782 | 1/20 | — | — | — |
| Qwen3-8B | skill-v1-sys | 0.3479 | 0.3822 | 0.4296 | 0/20 | 6/20 | 4 | 8 |
| Qwen3-8B | skill-v1-user | 0.3511 | 0.3465 | 0.4572 | 0/20 | 5/20 | 4 | 7 |
| Apertus-8B | no-skill | 0.2972 | 0.2897 | 0.3971 | 0/20 | — | — | — |
| Apertus-8B | skill-v1-sys | 0.3002 | 0.2884 | 0.3992 | 0/20 | 9/20 | 5 | 6 |
| Apertus-8B | skill-v1-user | 0.3028 | 0.3042 | 0.3974 | 0/20 | 8/20 | 7 | 5 |

---

## Key Findings

### 1. Qwen3-8B is a stronger baseline than Apertus-8B

Qwen3-8B no-skill edit mean (0.3953) is ~33% higher than Apertus-8B (0.2972). Qwen3 also achieved 1/20 cases above the 0.80 correctness threshold; Apertus achieved none across all conditions.

### 2. SKILL.md v1 hurts Qwen3-8B, is near-neutral for Apertus-8B

For Qwen3, both injection positions produce lower scores than no-skill (sys: −0.047, user: −0.044 edit mean). The skill actively removed the one case Qwen3 had solved.

For Apertus, both injection positions show marginal improvement (sys: +0.003, user: +0.006) but both are well within noise at n=20.

### 3. Injection position (sys vs user) has minimal impact

Neither model shows a consistent advantage for one injection position over the other. Apertus-8B's user injection has a slight edge (7 wins vs 5 with sys), but the absolute difference is 0.003 edit mean.

### 4. 35–45% of outputs are identical regardless of condition

Both models produce the same resolution whether or not the skill is present in a large fraction of cases (Qwen3: 5–6/20, Apertus: 8–9/20). This is not a pipeline bug — the system prompt echo check passes and user-message injection shows the same pattern. The models simply converge on the same output for these cases.

### 5. Positive signal in Apertus is driven by 2 outliers

Cases `0xa4d50e39def807dd` (+0.23 edit) and `0xe63ff0ddae988357` (+0.22 edit) account for essentially all of Apertus's positive delta. In both cases the skill prompted a shorter, more focused response where no-skill had over-generated (2–3× ground truth length). Removing these two cases leaves Apertus skill conditions flat or negative.

### 6. Over-generation is pervasive in both models

Both models frequently return responses far longer than the ground truth — wrapping the resolution in explanatory text. Worst case: ~14× GT length (`0x425cf8014eda936b`, both models). This inflates the edit-distance denominator and depresses scores. The v2 pipeline adds `extract_code_block()` to strip explanation text before scoring; this had measurable impact in that case.

### 7. No cases solved at scale (0.80 threshold)

Only 1 case across all runs and all conditions cleared the 0.80 correctness threshold (Qwen3 no-skill). This is consistent with a model-capability ceiling at 8B scale on `func`-type conflicts — not a pipeline issue.

### 8. The bottleneck is the skill content, not the pipeline

v2 confirmed the system prompt is reaching the model (`prompt_echo_check` passes), output is cleaned before scoring, and all v1 numbers reproduce exactly under temperature=0.0. The consistent underperformance of skill-v1 points to the skill text itself. SKILL.md v1 is intentionally minimal; v2 and v3 are the next step.

---

## Limitations

- 20 cases is too small for statistical conclusions — all results are directional only
- Only one conflict type (`func`) and one language (`python`) tested
- SKILL.md v1 is minimal by design — the experiment is a baseline, not a final evaluation
- Qwen3 thinking mode was disabled; enabling it may change results
- No token-count data recorded

---

## Next Steps

- Write SKILL.md v2 (issue [#6](https://github.com/bdravec/merge-conflict-skill/issues/6)) and re-run 3-condition pilot
- Scale to full tiny dataset (issue [#9](https://github.com/bdravec/merge-conflict-skill/issues/9))
- Test on additional conflict types (`text`, `sytx`)
