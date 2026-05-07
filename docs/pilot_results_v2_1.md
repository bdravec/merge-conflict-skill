# SKILL.md v2.1 — pilot evaluation results

Brief writeup for [#43](https://github.com/bdravec/merge-conflict-skill/issues/43). Evaluation of `skills/merge-conflict-resolve-v2.1/SKILL.md` against v2's pilot, on `python/func` subset (n=20), TEMPERATURE=0.0, three conditions per model.

Run date: 2026-05-07.
Raw data:
- `scripts/results/pilot_results_qwen3_skill-v2.1.jsonl`
- `scripts/results/pilot_results_apertus_skill-v2.1.jsonl`

---

## Headline

**Split outcome.** v2.1 modestly improves over v2 on Apertus, regresses on Qwen3-sys.

| Model | Condition | v2 mean edit | v2.1 mean edit | Δ vs v2 | Δ vs no-skill (v2) | Δ vs no-skill (v2.1) |
|---|---|--:|--:|--:|--:|--:|
| Qwen3   | no-skill | 0.3953 | 0.3953 | — | — | — |
| Qwen3   | sys      | 0.3836 | **0.3583** | **−0.0253** ⬇ | −0.0117 | **−0.0370** |
| Qwen3   | user     | 0.3558 | 0.3594 | +0.0036 ≈ | −0.0395 | −0.0359 |
| Apertus | no-skill | 0.2972 | 0.2972 | — | — | — |
| Apertus | sys      | 0.3310 | **0.3392** | **+0.0082** ⬆ | +0.0338 | **+0.0420** |
| Apertus | user     | 0.3244 | 0.3348 | +0.0104 ⬆ | +0.0272 | +0.0376 |

Identical-to-no-skill cases:

| Model | Condition | v2 | v2.1 |
|---|---|--:|--:|
| Qwen3 | sys | 9/20 | 7/20 |
| Qwen3 | user | 7/20 | 8/20 |
| Apertus | sys | 7/20 | 5/20 |
| Apertus | user | 9/20 | 7/20 |

v2.1 makes more changes from no-skill on three of four conditions. On Apertus those changes help on average; on Qwen3-sys they hurt.

---

## Predictions vs outcomes

`docs/skill_v2_1_design.md` §Evaluation plan predicted:

> *"the v2 → v2.1 reframing (recs 1+6+9) should strengthen Qwen3's harm-reduction effect (move from −0.012 toward 0) without regressing Apertus's +0.034."*

| Prediction | Outcome | Verdict |
|---|---|---|
| Apertus-sys: hold or improve at +0.034 | +0.0420 | ✅ held + improved |
| Qwen3-sys: move from −0.012 toward 0 | went to −0.037 (further from zero) | ❌ falsified |

The Qwen3 prediction got the *direction* wrong, not just the magnitude.

---

## Mechanism hypothesis

The asymmetry is consistent with the **headroom hypothesis** from `analysis_qwen3_v1_v2.md` sub-q 3: v2's effect on Qwen3 was already monotonic in baseline score (helps low, neutral middle, hurts top). v2.1's stronger output-discipline framing — front-loaded §3 with three explicit rules, the "Produce only the resolved code" framing in §2 — appears to *amplify* this monotonic tendency rather than redirect it:

- **Apertus** (lower no-skill baseline 0.297, more over-generation per case) → more headroom for harm-reduction → v2.1's stronger discipline produces more trimming, more wins. Identical-output count drops (7→5 sys), Δ improves.
- **Qwen3** (higher no-skill baseline 0.395, less over-generation per case) → less headroom → v2.1's stronger discipline trims into already-near-optimal output. Identical-output count drops (9→7 sys), Δ degrades.

The design intent of recs 1+6+9 was "make discipline primary, reduce pattern-taxonomy interference." The pilot confirms the discipline emphasis works as intended *mechanistically*, but the magnitude depends on whether the model has over-generation to trim. v2.1 is more skill, applied harder; on a model that doesn't need much, more skill = more harm.

This refines the design-doc framing:

> v2.1 is a stronger harm-reduction skill than v2. Its sign-of-effect is determined by the model's baseline over-generation rate, not by the skill content.

---

## Decision: keep / iterate / v3?

Per `docs/skill_v2_1_design.md`'s decision criteria:

> *"Keep v2.1 if it improves over v2 on at least one model without regressing on the other, or if regressions are explained by the known metric weakness rather than skill content."*

v2.1 **improves on Apertus** (+0.0082) and **regresses on Qwen3-sys** (−0.0253). The regression is **not** explained by the documented metric weakness (`docs/metric_weakness_0xe4ff79aa.md`); it's explained by the headroom mechanism above, which is a real skill-content effect.

**Strict reading of the criterion → iterate to v2.2.** The Qwen3 regression on -sys is large enough to disqualify v2.1 from the keep tier.

**But** consider:

- v2.1-user improves on Apertus and is roughly flat on Qwen3 (+0.0036). The user-injection variant is closer to a clean improvement.
- The Qwen3-sys regression may be partially explained by the same metric weakness identified for `0xe4ff79aa` — compact-wrong outputs on identifier-divergence cases that v2.1's discipline trims further. Per-case verification needed before fully attributing the regression to skill content.

**Recommended next steps** (deferred to next session):

1. **Per-case Δ comparison** of v2 vs v2.1 on Qwen3-sys to identify which cases drove the regression. Same `inspect_case.py` workflow.
2. **Check whether the regressors are metric-weakness cases** (identifier-divergence with heavy token overlap). If yes, the regression is partially metric artifact; v2.1 may be "keep" after all.
3. If the regression is genuine skill content, **iterate to v2.2** with a softer discipline framing for Qwen3 — possibly model-specific phrasing or a re-introduced softer pattern-taxonomy framing.

The decision should not be final until step 2.

---

## Related

- `skills/merge-conflict-resolve-v2.1/SKILL.md` — the artefact under evaluation.
- `docs/skill_v2_1_design.md` — design rationale and evaluation plan; predictions tested here.
- `docs/skill_v2_1_recommendations.md` — the nine recommendations v2.1 implements.
- `docs/metric_weakness_0xe4ff79aa.md` — relevant for step 2 of the next-steps list.
- Issue [#43](https://github.com/bdravec/merge-conflict-skill/issues/43) — tracking issue for evaluation.
