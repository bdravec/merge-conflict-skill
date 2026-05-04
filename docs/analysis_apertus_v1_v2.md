# Analysis — Apertus-8B v1 vs v2 SKILL.md

**Date:** 2026-05-04
**Issue:** [#41](https://github.com/bdravec/merge-conflict-skill/issues/41)
**Inputs:**
- v1-skill 3-condition: [`pilot_results_apertus_v2.md`](pilot_results_apertus_v2.md), `scripts/results/pilot_results_apertus_v2.jsonl`
- v2-skill 3-condition: [`pilot_results_apertus_skill-v2.md`](pilot_results_apertus_skill-v2.md), `scripts/results/pilot_results_apertus_skill-v2.jsonl`
- Companion analysis: [`analysis_qwen3_v1_v2.md`](analysis_qwen3_v1_v2.md)

> **Premise check.** Issue #41's headline figures (`0xa4d50e39def807dd` v1 +0.23 / v2 +0.23; `0xe63ff0ddae988357` v1 +0.22 / v2 +0.27) verify against the JSONL records. These are real Apertus v1 winners. (The same case IDs were *not* v1 winners on Qwen3 — see `analysis_qwen3_v1_v2.md` premise correction. The `+0.22`-figures appear to have been Apertus deltas that were mis-attributed to Qwen3 in the v2 doc finding #6.)

---

## Sub-question 1 — model-agnostic vs Apertus-specific

### Cross-tabulation (n=20, edit means)

| Model × condition | edit µ | Δ vs no-skill |
|---|--:|--:|
| Qwen3 no-skill | 0.3953 | — |
| Qwen3 v1-sys | 0.3479 | −0.047 |
| Qwen3 v2-sys | 0.3836 | −0.012 |
| Apertus no-skill | 0.2972 | — |
| Apertus v1-sys | 0.3002 | +0.003 |
| **Apertus v2-sys** | **0.3310** | **+0.034** |

Apertus v2-sys is the only positive-and-above-noise effect at n=20. Qwen3's v2-sys is approximately neutral (sub-q 4 of #40); v1 was negative on Qwen3 and a wash on Apertus.

### Per-case decomposition of Apertus v2-over-v1

The Apertus v2 uplift (+0.031 over v1-sys, +0.022 over v1-user) is concentrated in three cases:

| Case | Apertus v1-sys | Apertus v2-sys | v2 over v1 | Apertus no-skill |
|---|--:|--:|--:|--:|
| `0x223b29598e1c5cb9` | 0.286 | 0.458 | **+0.172** | 0.460 (v2 ≈ no-skill) |
| `0xe4ff79aa2f3f8922` | 0.433 | 0.620 | **+0.187** | 0.451 |
| `0x96d20e6c9b0f2395` | 0.320 | 0.454 | **+0.134** | 0.320 |
| `0xe63ff0ddae988357` | 0.649 | 0.702 | +0.053 | 0.430 |
| `0x520debc691c88dc5` | 0.362 | 0.425 | +0.063 | 0.425 (v2 = no-skill) |

The v1 winners (`0xa4d50e39`, `0xe63ff0dd`) survive but are not the source of v2's net improvement over v1. The improvement comes from one v1-loss recovery (`0x223b2959`) and two new wins that v1 didn't have (`0xe4ff79aa`, `0x96d20e6c`).

### Mechanism — what does v2 do on these three cases?

Inspection of the Apertus model outputs across all five conditions for each case:

**`0x223b2959` — v1 catastrophic loss recovery (+0.172)**

The conflict adds an `assert self.subsample == (1, 1)` line on side a; side b is empty. Apertus's behaviour by condition:

- *no-skill* (0.46): emitted the literal conflict markers (`=======`, `>>>>>>> b`) in the output alongside the correct surrounding code. The metric is forgiving enough that the markers don't tank the score.
- *v1-sys* (0.29): wholesale invention. Wrapped the resolution in a fabricated `def get_output(self, train=False):` method body (`X = self.get_input(train)`, `T.reshape`, `self.activation`, etc.) and a stub `def get_config(self):` declaration after the conflict region. None of that code exists on either side or in the surrounding context.
- *v2-sys* (0.46): clean. Kept side a's assert, dropped the fabrication, output ≈ no-skill modulo absence of the conflict markers.

v2-sys does not produce a pattern-correct resolution; it produces a no-skill-like output without v1's hallucinated method body.

**`0xe4ff79aa` — new v2 win (+0.187 over v1, +0.169 over no-skill)**

The conflict differs only in identifier (`pool_size` vs `poolsize`); ground truth picks side a and adds new lines after.

- *no-skill* (0.45): pick-b for the conflict region itself, then continued generating an `@property def output_shape(self):` body with a malformed `tuple(slice(s, s + p - 1) for s, p in zip(...))` expression. Broken syntax.
- *v1-sys* (0.43): same pick-b, same fabricated `output_shape` body, different broken-syntax slice expressions.
- *v2-sys* (0.62): same pick-b, but stops at `input_shape = self.input_shape`. The fabricated body is gone.

The pick-side decision (b, wrong) is identical in all three conditions. v2's gain is purely from cutting off the fabrication.

**`0x96d20e6c` — new v2 win (+0.134 over v1)**

The conflict differs in a single identifier (`data_format` vs `dim_ordering`); ground truth uses `data_format` (side a) and adds preamble.

- *no-skill* / *v1-sys* / *v1-user* (all 0.32): identical outputs. Each adds a 4-line preamble from the surrounding context (`if data_format == 'default': data_format = image_data_format()` plus a `ValueError` check), pick-b for the conflict region, plus 4 lines of epilogue from below the conflict. None of the preamble or epilogue is part of the actual conflict region.
- *v2-sys* (0.45): just the 3 lines that constitute the conflict region itself. Same wrong-side pick, no preamble, no epilogue.

Again: pick-side decision unchanged, gain entirely from trimming surrounding-context echo.

### Cross-model reading

All three v2-over-v1 wins on Apertus arise from the same mechanism: **v2 suppresses Apertus's tendency to extend the resolution into adjacent code** (preambles echoed from above, epilogues echoed from below, fabricated method bodies, conflict markers in the output). v2 does not change which side Apertus picks or whether it routes to combine; it changes whether Apertus stays inside the conflict region.

This is the same harm-reduction mechanism identified for Qwen3 in the companion analysis (#40 sub-q 4: v2 trims over-generation; gains only when no-skill was over-generating). The mechanism is model-agnostic. What differs is *opportunity*: Apertus over-generates on more cases at no-skill / v1, so v2 has more places to act, so v2's net Δedit is larger and reaches the n=20 noise floor. Qwen3 over-generates less, so v2's per-case effects largely cancel out across the run.

The headroom hypothesis from #40 sub-q 3 was framed as "Qwen3 is at-or-near v2's ceiling because Qwen3 is already applying v2's patterns." The Apertus data refines this: v2's effective "ceiling" isn't pattern competence at all — it's the point at which over-generation stops. Qwen3 hits that point earlier (lower no-skill over-generation rate). Apertus has further to fall, so v2's mechanism has more room to bite.

This is consistent with the v2 design intent (length cap + "no prose, code only") working as intended — but the working mechanism is content-trimming, not pattern teaching, on both models.

### Implications for the thesis (cross-model)

Two things follow for Chapter 6 / 7:

1. **The "Apertus benefits, Qwen3 doesn't" framing is misleading.** Both models benefit from the same mechanism; only the opportunity differs. The right framing for RQ1 ("does SKILL.md improve resolution quality?") is "yes, by suppressing the model's over-generation tendency, with magnitude proportional to the model's baseline over-generation rate." Apertus shows a larger net effect because it over-generates more, not because v2 is more skilful for it.
2. **RQ3 ("does small model + skill close the gap to large model without skill?") needs reformulation.** What the skill closes is the *over-generation gap*, not the resolution-quality gap. The pick-side decisions on `0x96d20e6c` and `0xe4ff79aa` were wrong in all conditions; v2 just made the surrounding noise quieter.

---

## Open sub-questions

- [x] Sub-question 1 — v2-over-v1 mechanism on Apertus is over-generation suppression. Same mechanism as Qwen3; different opportunity.
- [ ] Sub-question 2 — why did v1 winners (`0xa4d50e39`, `0xe63ff0dd`) survive on Apertus but flip on Qwen3? (Preview: likely the same mechanism — Apertus's over-generation makes v1's stricter framing actually beneficial, where Qwen3 didn't need it.)
- [ ] Sub-question 3 — persistent Apertus loss `0xd9272c5e0e8f15ee` (−0.11 in both v1 and v2).
- [ ] Sub-question 4 — outlier-driven concern: median delta vs mean.
- [ ] Sub-question 5 — pattern-routing diagnostic: did v2 actually apply the *correct* pattern on each Apertus winning case?
