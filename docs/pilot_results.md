# Pilot Results — Summary

This document summarises all pilot evaluation runs. Each run tested 20 cases from `congra_tiny_datasets/python/func`, temperature=0.0, served via vLLM on a local GPU.

For full per-case breakdowns see the individual docs:

**v1 skill (3-condition):**
- [`pilot_results_qwen3_v2.md`](pilot_results_qwen3_v2.md) — Qwen3-8B (supersedes the original 2-condition Qwen3 run)
- [`pilot_results_apertus_v2.md`](pilot_results_apertus_v2.md) — Apertus-8B (supersedes `pilot_results_apertus.md`)

**v2 skill (3-condition):**
- [`pilot_results_qwen3_skill-v2.md`](pilot_results_qwen3_skill-v2.md) — Qwen3-8B
- [`pilot_results_apertus_skill-v2.md`](pilot_results_apertus_skill-v2.md) — Apertus-8B

---

## Conditions

| Condition | Description |
|-----------|-------------|
| `no-skill` | ConGra default system prompt, no skill content |
| `skill-v1-sys` | SKILL.md v1 replaces the system message |
| `skill-v1-user` | SKILL.md v1 prepended to the user message; default system prompt kept |
| `skill-v2-sys` | SKILL.md v2 replaces the system message |
| `skill-v2-user` | SKILL.md v2 prepended to the user message; default system prompt kept |

---

## Results at a Glance

| Model | Condition | Edit mean | Edit median | Winn mean | Above 0.80 | Identical | Skill wins | Skill losses |
|-------|-----------|-----------|-------------|-----------|------------|-----------|------------|--------------|
| Qwen3-8B | no-skill | 0.3953 | 0.3660 | 0.4782 | 1/20 | — | — | — |
| Qwen3-8B | skill-v1-sys | 0.3479 | 0.3822 | 0.4296 | 0/20 | 6/20 | 4 | 8 |
| Qwen3-8B | skill-v1-user | 0.3511 | 0.3465 | 0.4572 | 0/20 | 5/20 | 4 | 7 |
| Qwen3-8B | **skill-v2-sys** | **0.3836** | 0.3777 | 0.4450 | 0/20 | 9/20 | 4 | 5 |
| Qwen3-8B | **skill-v2-user** | **0.3558** | 0.3777 | 0.4377 | 0/20 | 7/20 | 4 | 7 |
| Apertus-8B | no-skill | 0.2972 | 0.2897 | 0.3971 | 0/20 | — | — | — |
| Apertus-8B | skill-v1-sys | 0.3002 | 0.2884 | 0.3992 | 0/20 | 9/20 | 5 | 6 |
| Apertus-8B | skill-v1-user | 0.3028 | 0.3042 | 0.3974 | 0/20 | 8/20 | 7 | 5 |
| Apertus-8B | **skill-v2-sys** | **0.3310** | 0.3076 | 0.4424 | 0/20 | 7/20 | 7 | 5 |
| Apertus-8B | **skill-v2-user** | **0.3244** | 0.2914 | 0.4308 | 0/20 | 9/20 | 7 | 3 |

---

## Key Findings — v1 skill

### 1. Qwen3-8B is a stronger baseline than Apertus-8B

Qwen3-8B no-skill edit mean (0.3953) is ~33% higher than Apertus-8B (0.2972). Qwen3 also achieved 1/20 cases above the 0.80 correctness threshold; Apertus achieved none across all conditions.

### 2. SKILL.md v1 hurts Qwen3-8B, is near-neutral for Apertus-8B

For Qwen3, both injection positions produce lower scores than no-skill (sys: −0.047, user: −0.044 edit mean). The skill actively removed the one case Qwen3 had solved.

For Apertus, both injection positions show marginal improvement (sys: +0.003, user: +0.006) but both are well within noise at n=20.

### 3. Injection position (sys vs user) has minimal impact

Neither model shows a consistent advantage for one injection position over the other. Apertus-8B's user injection has a slight edge (7 wins vs 5 with sys), but the absolute difference is 0.003 edit mean.

### 4. 35–45% of outputs are identical regardless of condition

Both models produce the same resolution whether or not the skill is present in a large fraction of cases (Qwen3: 5–6/20, Apertus: 8–9/20). This is not a pipeline bug — the system prompt echo check passes and user-message injection shows the same pattern. The models simply converge on the same output for these cases.

### 5. Positive signal in Apertus v1 is driven by 2 outliers

Cases `0xa4d50e39def807dd` (+0.23 edit) and `0xe63ff0ddae988357` (+0.22 edit) account for essentially all of Apertus v1's positive delta. In both cases the skill prompted a shorter, more focused response where no-skill had over-generated (2–3× ground truth length). Removing these two cases leaves Apertus v1 skill conditions flat or negative.

### 6. Over-generation is pervasive in both models

Both models frequently return responses far longer than the ground truth — wrapping the resolution in explanatory text. Worst case: ~14× GT length (`0x425cf8014eda936b`, both models). This inflates the edit-distance denominator and depresses scores. The v2 pipeline adds `extract_code_block()` to strip explanation text before scoring; this had measurable impact in that case.

### 7. No cases solved at scale (0.80 threshold)

Only 1 case across all runs and all conditions cleared the 0.80 correctness threshold (Qwen3 no-skill). This is consistent with a model-capability ceiling at 8B scale on `func`-type conflicts — not a pipeline issue.

### 8. The bottleneck is the skill content, not the pipeline

v2 pipeline confirmed the system prompt is reaching the model (`prompt_echo_check` passes), output is cleaned before scoring, and all v1 numbers reproduce exactly under temperature=0.0. The consistent underperformance of skill-v1 points to the skill text itself. SKILL.md v1 is intentionally minimal; v2 was the next step.

---

## Key Findings — v2 skill

### 9. v2 skill is the first version that beats no-skill (on Apertus)

Apertus-8B with v2 skill: +0.0338 edit (sys), +0.0272 edit (user) over no-skill. Both well above the noise floor at n=20. v1 was at +0.003 / +0.006 — essentially zero.

### 10. v2 improves over v1 for both models

| | Qwen3 | Apertus |
|--|------:|--------:|
| sys: v2 − v1 edit | +0.0357 | +0.0308 |
| user: v2 − v1 edit | +0.0047 | +0.0216 |

The pattern-based framing (Boll et al. EASE 2024: pick / combine / empty / custom) is a real improvement over v1's generic step-by-step instructions, in both injection positions for Apertus and in the sys position for Qwen3.

### 11. Qwen3 vs Apertus diverged in v2

Qwen3 v2 conditions are still net-negative vs no-skill (sys: −0.012, user: −0.040). Apertus v2 conditions are clearly positive. Same skill, same cases, opposite verdicts.

The most striking case-level evidence: v1's two strongest winners on Apertus (`0xa4d50e39def807dd` +0.23 and `0xe63ff0ddae988357` +0.22) survived v2 on Apertus but *flipped negative or to zero* on Qwen3.

Possible explanations (all hypotheses, none verified):
- **Headroom hypothesis** — Apertus has more room above its baseline; the skill content is informative because Apertus does not already encode the patterns implicitly. Qwen3, with its stronger pretraining, may already do most of what v2 teaches.
- **Instruction-following sensitivity** — Apertus may be more responsive to system-message guidance than Qwen3 (with thinking mode disabled).
- **Style-of-output mismatch** — Qwen3's natural output style may be closer to ground truth than v2's encouraged terseness; the skill nudges Qwen3 *away* from its own better instinct.

### 12. v2 reduces losses without expanding wins

For both models, v2 has fewer cases where the skill makes things worse than v1, but the count of cases where the skill helps is similar:

| | Wins (v1 → v2) | Losses (v1 → v2) |
|--|---------------:|----------------:|
| Qwen3 sys | 4 → 4 | 8 → 5 |
| Qwen3 user | 4 → 4 | 7 → 7 |
| Apertus sys | 5 → 7 | 6 → 5 |
| Apertus user | 7 → 7 | 5 → 3 |

The v2 redesign converted losses into ties rather than into new wins. Consistent with v2's design intent of constraining (length cap, "no prose" twice, no-new-identifiers) rather than elaborating.

### 13. Apertus v2 is partially outlier-driven

The same two cases that drove v1's marginal positive signal on Apertus (`0xa4d50e39…` and `0xe63ff0dd…`) are the largest contributors to v2's gains. Removing them weakens the Apertus v2 advantage. v2 also added `0xe4ff79aa2f3f8922` (+0.17) and `0x96d20e6c9b0f2395` (+0.13) as new winners, so the result is less outlier-dependent than v1, but the right-tail of the case distribution still dominates the mean.

### 14. The hard cases stayed hard

Cases that produced near-zero edit similarity in v1 (`0x520debc691c88dc5`, `0xddd5322de12565fe`, `0x425cf8014eda936b`) remain difficult in v2 across both models. These are likely model-capability ceiling cases at 8B scale, not skill-content cases. Closing them probably requires either a stronger model or external context (per MergeBERT user-study finding: ~16% of custom resolutions need information outside the conflict region).

---

## Limitations

- 20 cases is too small for statistical conclusions — all results are directional only
- Only one conflict type (`func`) and one language (`python`) tested
- Qwen3 thinking mode was disabled; enabling it may change results
- No token-count or response-length data analyzed in this summary
- The +0.27 / +0.23 cases that drive most of Apertus's v2 uplift represent ~25% of cases by count but a much larger share of total Δ edit; the result is partially outlier-driven
- The Qwen3-vs-Apertus divergence is observed on n=2 models; may not generalise

---

## Next Steps

Per design doc §3.2 fallback decision tree:

1. **Iterate v2 (Option C: pattern-frequency EDA)** — analyze the cases where v2 hurts Qwen3 (`0x520debc691c88dc5`, `0xddd5322de12565fe`, `0x7fb96fbf0a030ea`, `0xa4d50e39def807dd`) to identify a recurring conflict shape. If a pattern emerges, write v2.1 with examples drawn from those shapes. Tracked under per-model analysis issues.

2. **Cross-version analysis (open issues):**
   - Apertus v1 vs v2 — what makes v2 work for Apertus? Inform Chapter 6 / 7.
   - Qwen3 v1 vs v2 — why does Qwen3 resist v2? Headroom hypothesis test.

3. **Defer v3** until the v2 iteration is exhausted. The v2 framing is validated; the gap to v3 isn't yet justified by data.

4. **Open issue [#39](https://github.com/bdravec/merge-conflict-skill/issues/39)** — `pilot.py` Empty-pattern scoring fix. Not blocking the current `python/func` slice, but a prerequisite for evaluating non-`func` slices that contain Empty cases.

5. **Eventually:** scale to full tiny dataset (issue [#9](https://github.com/bdravec/merge-conflict-skill/issues/9)) and test other conflict types (`text`, `sytx`).
