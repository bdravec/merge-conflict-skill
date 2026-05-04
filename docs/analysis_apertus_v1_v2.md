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

## Sub-question 4 — outlier-driven concern

The Apertus v2-sys result is a **+0.034** mean edit gain over no-skill (n=20). Sub-q 4 asks whether that mean is broadly distributed or driven by a small number of outlier cases.

### Median test

| Condition | mean | median | mean Δ | median Δ |
|---|--:|--:|--:|--:|
| no-skill | 0.2972 | 0.2897 | — | — |
| skill-v1-sys | 0.3002 | 0.2884 | +0.003 | +0.000 |
| skill-v1-user | 0.3028 | 0.3042 | +0.006 | +0.000 |
| **skill-v2-sys** | **0.3310** | 0.3076 | **+0.034** | **+0.000** |
| skill-v2-user | 0.3244 | 0.2914 | +0.027 | +0.000 |

**The median Δedit is zero in every skill condition.** The reason is structural: 8/20 v2-sys outputs are byte-identical to no-skill, so 8 zeros sit at the centre of the distribution. The median Δedit being zero is not a sign of noise; it's a sign that the modal v2 effect is *no effect*.

### Trimmed-mean test

| Drop top N positive outliers | mean Δedit | n |
|---|--:|--:|
| 0 | **+0.0338** | 20 |
| 1 | +0.0212 | 19 |
| 2 | +0.0098 | 18 |
| 3 | **+0.0004** | 17 |
| 4 | −0.0080 | 16 |
| 5 | −0.0090 | 15 |

The entire Apertus v2 uplift is concentrated in **three cases**: `0xe63ff0dd` (+0.272), `0xa4d50e39` (+0.226), `0xe4ff79aa` (+0.169). Drop those and the mean Δedit collapses to essentially zero. Drop four (adding `0x96d20e6c` +0.134) and the mean turns negative.

These three cases are the same v2-over-v1 winners characterised in sub-q 1 (modulo `0x223b2959`, which is a v1-loss recovery rather than a no-skill gain — it sits at v2-sys Δ ≈ 0 vs no-skill).

### Sign distribution

| Direction | count |
|---|--:|
| v2-sys > no-skill | 7 / 20 |
| v2-sys < no-skill | 5 / 20 |
| v2-sys = no-skill | 8 / 20 |

At n=20 with 7 positives and 5 negatives, the binomial sign test against the null (skill has no effect) gives p ≈ 0.39 — not significant. A Wilcoxon signed-rank test would also fail to reject the null because the rank sums are dominated by ties and the few non-zero deltas are mostly small. **The +0.034 mean is statistically a function of the heavy right tail, not a broad effect across cases.**

### Conditional analysis — when v2 does change the output

Excluding the 8 byte-identical cases, the remaining 12 v2-sys outputs differ from no-skill:

|  | n | mean Δedit |
|---|--:|--:|
| v2-sys positive (changed and helped) | 7 | **+0.122** |
| v2-sys negative (changed and hurt) | 5 | −0.028 |

Among cases where v2 acts at all, the positive moves are ≈4× larger than the negative moves. So v2 *when it acts* is a clear net win on Apertus — but it only acts on a minority (12/20 = 60% of cases overall, and only 4 of those 12 contribute non-trivial positive deltas).

### Reading

The Apertus v2 effect is real but narrow:

- **Real:** when v2 acts, positive effects strongly outweigh negative effects in magnitude.
- **Narrow:** v2 acts on the minority of cases where Apertus over-generates (the harm-reduction profile from sub-q 1). On the majority, v2 either changes nothing (8 ties) or makes a small adjustment that nets near zero (5 small negatives).

This refines #40's headroom finding. The headroom hypothesis predicted that v2's effect concentrates at the bottom of the score distribution. Sub-q 4 sharpens this: v2's effect concentrates at *specific* cases — the ones with severe over-generation in the no-skill output — not at any case in the low-baseline tier. Bucketing by no-skill score on Apertus is a coarser view than the actual mechanism.

### Implications for the thesis

Two practical consequences:

1. **Statistical reporting.** The mean is the right summary for the headline ("v2 improves Apertus edit mean by +0.034"), but it should be paired with the median and the trimmed mean, plus the sign distribution. Reporting the mean alone hides that v2 leaves 13/20 cases essentially unchanged. A footnote to that effect prevents over-claiming.

2. **Generalisation claim for Chapter 7.** "v2 helps Apertus on the cases where Apertus over-generates" is a much more defensible claim than "v2 helps Apertus." The latter implies a broad-spectrum skill effect that the data doesn't support — even on the model where v2 does best. Cross-model generalisation should be framed as "the v2 mechanism (over-generation suppression) is model-agnostic; the population of cases where it can act is model-specific."

This sharpens v2.1 recommendation 6 from #40 (reframe as over-generation guard) further: an over-generation guard is exactly what v2 *is*, on both models. The skill should be designed and evaluated as one.

---

## Sub-question 2 — v1-winners survival on Apertus

The two cases the issue identifies as Apertus v1 winners — `0xa4d50e39def807dd` (+0.226 in v1, +0.226 in v2) and `0xe63ff0ddae988357` (+0.219 in v1, +0.272 in v2) — both survived the v2 redesign. On Qwen3, the same case-IDs were v1's two biggest *losers* (see #40 premise correction). The cross-model flip needs explanation.

### `0xa4d50e39` — harm-reduction explains both directions

The conflict combines side a's `with tf_ops.init_scope():` block with side b's `tf_dtype = tf.as_dtype(dtype)` line. Ground truth requires a custom resolution (a `n, m = size` unpack that exists on neither side; see #40 sub-q 1 case B).

Per-condition outputs on Apertus:

| Condition | Output (truncated) |
|---|---|
| no-skill (0.24) | `@symbolic\ndef zeros_like(x, dtype=None, name=None):\n    """Instantiates an all-zeros variable...\n    Parameters: ...\n    """\n    if dtype is None: dtype = floatx()\n    tf_dtype = tf.as_dtype(dtype)\n    return variable(tf.eye(size, dtype=tf_dtype), dtype, name)` |
| v1-sys (0.47) | `with tf_ops.init_scope():\n    return variable(tf.eye(size, dtype=tf.as_dtype(dtype)), dtype, name)` |
| v2-sys (0.47) | identical to v1-sys |

Apertus's no-skill output is a **hallucinated function definition** — it invented a `@symbolic` decorator, a `zeros_like` function name (the file is `tensorflow_backend.py`, the function is unrelated), a multi-line docstring, and parameter descriptions, all before getting to the actual conflict resolution. v1's "be brief" framing alone is enough to suppress this: v1's two-line combine is what no-skill *should* have produced.

The Qwen3 mirror image: Qwen3 no-skill already produces a clean three-line combine (#40 sub-q 1 case B); v1 *introduces* a context-leak by adding `if dtype is None: dtype = floatx()`, and v2 trims `init_scope` away under the length cap. Same skill, applied to two models with very different baseline failure modes — fixes catastrophic hallucination on Apertus, disrupts a working combine on Qwen3.

This is the same harm-reduction asymmetry as sub-q 1's three v2-over-v1 cases. Apertus over-generates; v1 trims; v2 maintains.

### `0xe63ff0dd` — harm-reduction *plus* a real pattern-teaching effect

The conflict is a textbook pick-a (side a's `K.placeholder(shape=..., dtype=K.floatx())` matches surrounding-code style; side b's `tf.placeholder(dtype=K.floatx())` is the lower-level API). Ground truth is exact pick-a.

| Condition | Pick side | Trimmed over-gen? | Edit |
|---|---|---|--:|
| no-skill | b (`tf.placeholder`) — wrong | no (kept `# test merge`, `concatenate`, `add` block) | 0.43 |
| v1-sys | b (`tf.placeholder`) — wrong | yes | 0.65 |
| v2-sys | **a (`K.placeholder`) — correct** | no (kept the over-gen block) | 0.70 |

v1's gain over no-skill (+0.22) is pure harm-reduction: same wrong pick, but trimmed the post-conflict `# test merge` invention. v2's gain over v1 (+0.05) is a different mechanism: **v2 flipped the pick from b to a**, while keeping the over-generation block that v1 had trimmed.

This is the only case across the entire 40-case (2 models × 20 cases) corpus where v2 applies a pick decision the model did not make under no-skill or v1, and applies it correctly. v2's pick criterion ("which side is more consistent with the surrounding code") fired here: surrounding code uses `K.` prefixes consistently, side a matches, and v2 picked a. This is genuine pattern-teaching, not harm-reduction.

### Survey: pattern-teaching across the full corpus

To check whether `0xe63ff0dd` is unique or representative, I inspected every v2-over-v1 case where the score changed by more than ±0.05 across both models:

| Case | Model | v2-over-v1 Δ | Mechanism |
|---|---|--:|---|
| `0xe63ff0dd` | Apertus | +0.053 | **Pattern-teaching:** v2 flipped pick from b (wrong) to a (correct) |
| `0xddd5322d` | Apertus | +0.030 | **Weak pattern-teaching:** v2 applied combine (`if not None:` from a + `else:` from b); GT wants custom, so gain is +0.003 vs no-skill |
| `0xa4d50e39` | Qwen3 | −0.030 | **Wrong-direction pattern-teaching:** v2 changed resolution from correct combine to pure pick-b |
| `0x223b2959` | Apertus | +0.172 | Harm-reduction (v2 suppressed v1's invented method body) |
| `0xe4ff79aa` | Apertus | +0.187 | Harm-reduction (trim) |
| `0x96d20e6c` | Apertus | +0.134 | Harm-reduction (trim) |
| `0x96d20e6c` | Qwen3 | +0.004 | Harm-reduction (same correct pick, trimmed surrounding) |
| `0x999797db` | Qwen3 | +0.138 | Harm-reduction (v1 already changed pick — to wrong side; v2 inherited and trimmed) |
| `0x32d8c89b` | Qwen3 | +0.064 | Lucky variation (GT is a custom rewrite; v2 produced different content that happened to align with parts of GT — no clean pattern applies) |

**Pattern-teaching is real but rare: 3/40 model-cases (7.5%).** One right-direction (`0xe63ff0dd` Apertus), one weak/marginal (`0xddd5322d` Apertus, +0.003), one wrong-direction (`0xa4d50e39` Qwen3, regression). Two of the three pattern-teaching events are on Apertus — but the headroom mechanism alone explains why v2 helps Apertus more, since the bulk of v2's effect is harm-reduction in both models.

### Refining the thesis claim

The picture from #40 said "v2 is doing harm-reduction, not skill-elevation." Sub-q 2 nuances this: v2 is *predominantly* harm-reduction (≥35/40 model-cases), with a **secondary pattern-teaching capability** that surfaces in ~5% of cases. The pattern-teaching capability is bidirectional — it can help (`0xe63ff0dd`'s pick correction) or hurt (`0xa4d50e39`'s combine→pick regression) — and the conditions that determine direction aren't currently characterised.

For the thesis: claiming v2 is "purely" a harm-reduction skill would understate the data. Claiming v2 is "primarily a pattern-teaching skill" overstates it. The defensible framing is *"v2 is a harm-reduction skill with a small, bidirectional pattern-teaching effect."* Sub-q 5 (pattern-routing diagnostic) is now positioned to ask whether v2's pattern-teaching is *correctly* routed when it does fire.

### v2.1 implications (sub-q 2 additions)

The earlier #40 v2.1 recommendations (1–6) all hold. Sub-q 2 adds one consideration:

7. **Investigate why pattern-teaching fires unevenly.** v2's pick criterion ("consistency with surrounding code") worked on `0xe63ff0dd` Apertus but didn't fire on the structurally similar `0xe4ff79aa` Apertus (where the model also picked the wrong side, `poolsize` instead of `pool_size`, and v2 didn't correct it). The difference between the two cases is worth understanding — both involve identifier-divergence-with-surrounding-context-tiebreaker, but only one was decided correctly. A worked example covering both shapes (per #40 recommendation 3) might surface what's missing.

---

## Sub-question 3 — persistent Apertus loss on `0xd9272c5e0e8f15ee`

The case scores Δedit −0.112 in v1-sys, v1-user, v2-sys, *and* v2-user on Apertus (Apertus no-skill 0.289, all skill conditions 0.177). Sub-q 3 asks: is this model-specific, shape-specific, or beyond 8B-scale capability?

### Conflict and ground truth

```
<<<<<<< a
            x = nn.bias_add(x, bias,
=======
            x = tf.nn.bias_add(x, bias,
>>>>>>> b
                               data_format='NCHW')
```

Two sides differ by a single token (the `tf.` prefix). Surface-shape: textbook pick.

Ground truth:

```
            # No support yet for NCHW in bias_add.
            x += reshape(bias, (1, int_shape(bias)[0], 1, 1))
        elif data_format == 'channels_last':
```

GT throws away *both* sides. It writes a comment explaining the abandonment and replaces `bias_add` with `x += reshape(bias, (1, int_shape(bias)[0], 1, 1))` — a line that matches the **file-level surrounding-code pattern**. The file has analogous `x += reshape(bias, ...)` lines for ndim=3 and ndim=5 in the lines around the conflict; GT extends that pattern to ndim=4 by abandoning the bias_add approach entirely.

The right resolution requires recognising the file pattern and synthesising a new line consistent with it, using tokens that exist neither in side a nor in side b.

### Per-condition outputs (both models)

| Model | Condition | Pick | Surrounding context retained? | Edit |
|---|---|---|---|--:|
| Apertus | no-skill | a (`nn.bias_add`) | yes (5 lines incl. `x += reshape(bias, (1, int_shape(bias)[0], 1))`) | **0.289** |
| Apertus | v1-sys / v1-user / v2-sys / v2-user | a (`nn.bias_add`) | no | 0.177 |
| Qwen3 | no-skill, v1-sys, v2-sys, v2-user | b (`tf.nn.bias_add`) | no | 0.193 |
| Qwen3 | v1-user | b (`tf.nn.bias_add`) | yes (5 lines, same as Apertus no-skill) | **0.280** |

The two highest-scoring outputs (Apertus no-skill, Qwen3 v1-user) both share one feature: they leaked the line from below the conflict — `x += reshape(bias, (1, int_shape(bias)[0], 1))` — into the resolution. That line is structurally close to GT's synthesised line (`x += reshape(bias, (1, int_shape(bias)[0], 1, 1))`); the only difference is the trailing `, 1` for the extra dimension. The metric credits the close-match line.

### Mechanism

The skill does exactly what it's designed to do: trim surrounding context, focus on the conflict region. On this particular case, that design *discards* the lucky line that no-skill happened to retain. Both v1 and v2 produce the same shorter output (just the conflict region resolution), and that output scores worse than no-skill's longer-with-leak output.

The skill's behaviour is **not wrong**. It's correctly applying its rules to a conflict that has the surface shape of a pick. What the skill can't see is that the right resolution lives in a file-level architectural pattern that neither side encodes.

### Is this model-, shape-, or capability-specific?

**Not model-specific.** Both models fail. The two highest scores come from accidental context retention, on different injection positions (Apertus no-skill, Qwen3 v1-user) — the underlying mechanism is the same.

**Not shape-specific in v2's taxonomy.** The conflict has the surface shape of a clean pick. v2's pattern hierarchy correctly classifies it as such. The mismatch is between the surface shape and the actual semantic resolution required.

**Capability-specific.** Recovering GT requires three things in sequence: (1) recognising that the file-level pattern uses `x += reshape(bias, ...)` for each ndim-and-data-format combination, (2) inferring that the bias_add path in the conflict is therefore inconsistent with that pattern, and (3) synthesising a new line that fits the pattern using the right shape tuple. None of these is achievable at 8B scale via the current task framing — the model sees only ±5 lines of context and is asked to pick or combine. v2 §"Custom escape" explicitly forbids the right answer: it requires *"smallest reconciliation from existing tokens"* and existing tokens means sides a and b, not surrounding code.

### A note on metric mechanics

`0xd9272c5e` exposes a tension in the ConGra edit-similarity metric: when GT lives outside the conflict region, *retaining surrounding context becomes a proxy* for the pattern-recognition the model can't actually do. The metric rewards leak, not understanding. This is structurally similar to over-generation (which inflates the denominator and depresses scores when the leak is wrong) but with the opposite sign: when the leak happens to align with GT, it inflates the score.

For the thesis, this argues for a metric that distinguishes "right content in the right structure" from "right tokens leaked from anywhere nearby." The current setup conflates these.

### Verdict

`0xd9272c5e` is a **task-ceiling case**, not a skill failure. The −0.11 Apertus skill regression is a skill artefact: v1 and v2 both do what they're designed to do (focus on the conflict region), and on this case that design discards a lucky alignment that the metric rewards. Both Qwen3 and Apertus can't produce GT under any condition. The case should be categorised in Chapter 6 alongside `0x425cf8014eda936b` (the 14×-over-generation case) as a model-capability ceiling case at 8B.

### v2.1 implications (sub-q 3 additions)

The earlier #40 v2.1 recommendations (1–6) and sub-q 2 recommendation 7 all hold. Sub-q 3 adds:

8. **Acknowledge file-level resolutions exist and are out of scope.** v2 §"Custom escape" should explicitly state that some conflicts have GT resolutions that depend on file-level patterns invisible to the conflict-region view. The skill cannot solve these and should not pretend to. A short sentence to that effect would prevent the model from over-confidently picking when the right answer is "neither side, and the right answer needs more context than I have." This is also a candidate for a Chapter 7 limitation.

---

## Sub-question 5 — pattern-routing diagnostic

For each Apertus v2-sys win (positive Δedit vs no-skill), classify what pattern v2 applied versus what pattern is required by ground truth. The question: when v2 helps, is it because v2 routed the case to the correct pattern, or for some other reason?

### Scorecard

| Case | Apertus v2-sys Δ | GT pattern | v2's applied pattern | Routing correct? | Source of gain |
|---|--:|---|---|---|---|
| `0xe63ff0dd` | +0.272 | pick-a | pick-a (right side, `K.placeholder`) | **✓ Correct** | Real pattern-teaching (sub-q 2) |
| `0xa4d50e39` | +0.226 | custom (`n, m = size` unpack) | combine (`init_scope` + `tf_dtype`) | ≈ Best reachable given 8B ceiling | Harm-reduction (replaced hallucinated function) |
| `0xe4ff79aa` | +0.169 | pick-a (`pool_size`) + custom-extend | pick-b (`poolsize`) | **✗ Wrong side** | Harm-reduction (trimmed broken-syntax fabrication) |
| `0x96d20e6c` | +0.134 | pick-a (`data_format`) + custom-extend | pick-b (`dim_ordering`) | **✗ Wrong side** | Harm-reduction (trimmed preamble + epilogue) |
| `0x8e6579cb` | +0.007 | pick-a + custom-rename (`vis_utils` → `layer_utils`) | pick-a (reformatted) + over-gen | Partial; custom out of reach | Marginal content alignment |
| `0xddd5322d` | +0.003 | custom (different body) | combine (`if not None:` + `else:` branch) | **✗ Wrong pattern** | Marginal |

### Reading

- **1/6** wins are routed correctly at the pattern level (`0xe63ff0dd`).
- **1/6** wins reach the best-reachable pattern given the 8B capability ceiling (`0xa4d50e39` — combine is the closest non-custom approximation).
- **3/6** wins gain through harm-reduction *despite* incorrect pattern routing — v2 either picked the wrong side (`0xe4ff79aa`, `0x96d20e6c`) or applied the wrong pattern (`0xddd5322d`), and the score went up anyway because the over-generation around the resolution was suppressed.
- **1/6** is marginal alignment with no clean pattern story (`0x8e6579cb`).

### Implication: pattern routing is largely orthogonal to where v2's gains come from

The strongest version of the headroom synthesis from sub-q 1 holds: v2's wins on Apertus are driven by **over-generation suppression, not by correct pattern application**. Even when v2 applies the wrong pattern (`0xe4ff79aa` and `0x96d20e6c` both pick-b, opposite of the correct pick-a), the wins materialise because the metric rewards trimmed fabrication around the resolution more than it rewards correct pick decisions on identifier-divergence cases.

This sharpens the thesis claim further. v2's pattern taxonomy (pick / combine / empty / custom) is not what's doing the work in the measured improvements. What's doing the work is the *output discipline* around the pattern decision — the length cap, the "no prose, code only" rule, the implicit pressure toward conflict-region focus. v2 could in principle route patterns correctly *or* wrongly and still produce most of its measured gains, as long as it suppressed the surrounding fabrication.

This is consistent with #40 sub-q 4's length-distribution finding (v2's gains correlate with output shortening when no-skill was over-generating) and sub-q 3's metric tension (when GT lives outside the conflict region, raw token-level alignment trumps pattern correctness).

### Verdict on the headline question

> **What does v2 add for Apertus that v1 didn't?**

v2 adds **stricter output discipline** that suppresses Apertus's tendency to extend resolutions into adjacent code (fabricated method bodies, broken-syntax inventions, preambles and epilogues echoed from surrounding context). v1 does some of this already; v2 does it more aggressively. On the Apertus cases where over-generation was a major component of the no-skill failure, v2's harm-reduction is enough to flip Δedit positive even when the pattern routing is incorrect.

v2 *also* adds a small pattern-teaching capability that fires correctly on `0xe63ff0dd` (pick-side correction). But this capability accounts for only one of the six positive Apertus cases and is bidirectional across the corpus (it fires wrong-direction on `0xa4d50e39` Qwen3, sub-q 2). It is not the primary mechanism.

### v2.1 implications (sub-q 5 additions)

Sub-q 5 reinforces #40 recommendations 1, 5, 6 (length cap → over-gen guard rules) and sub-q 2 recommendation 7 (investigate why pattern-teaching fires unevenly). It adds:

9. **Decouple the pattern taxonomy from the output-discipline rules.** v2 currently presents both as a unified rulebook. The data says only the latter is doing the measurable work. v2.1 could lead with the output-discipline rules (no over-generation, code only, no echoed surrounding context) and present the pattern taxonomy as secondary guidance for cases where the model's no-skill behaviour is already focused. This reframes the skill from "here is how to resolve conflicts" to "here is how to *cleanly produce* whatever resolution you would otherwise produce."

---

## Final synthesis

Across all five sub-questions:

- **Sub-q 1.** v2's three v2-over-v1 wins on Apertus (`0x223b2959`, `0xe4ff79aa`, `0x96d20e6c`) are all over-generation suppression. Same mechanism as Qwen3 (#40 sub-q 4); the difference is opportunity (Apertus over-generates more).
- **Sub-q 2.** v1 winners survived on Apertus because v1's "be brief" framing already does harm-reduction; v2 maintains it. `0xe63ff0dd` is the one clean pattern-teaching event (pick-side correction). Pattern-teaching across the 40-case corpus: 3/40 = 7.5%, bidirectional.
- **Sub-q 3.** `0xd9272c5e` is a task-ceiling case. GT requires file-level pattern synthesis that v2's "custom escape" forbids by construction. The −0.11 Apertus regression is a skill artefact: focusing on the conflict region discards a lucky surrounding-context line that scores well by metric proxy.
- **Sub-q 4.** The +0.034 Apertus mean uplift is concentrated in 3–4 cases. Median Δ = 0; sign test (7+/5−/8=) not significant at n=20. v2 *when it acts* is a clear net win (positive moves ≈4× larger than negative), but it only acts on a minority.
- **Sub-q 5.** Pattern routing is largely orthogonal to where v2's gains come from. 3/6 Apertus wins gain through harm-reduction *despite* incorrect pattern routing. v2's pattern taxonomy is not doing the measured work; v2's output discipline is.

**Cross-model picture.** v2 is the same skill on both models. The mechanism (over-generation suppression with a small pattern-teaching tail) is model-agnostic. The opportunity (how often the no-skill output exhibits the trim-able failure mode) is model-specific. Apertus over-generates more → v2 has more room → v2 reaches the n=20 noise floor on Apertus and not on Qwen3. The "Apertus benefits, Qwen3 doesn't" framing is a function of the input distribution, not of skill effectiveness.

**Nine v2.1 recommendations** stand at issue closure (1–6 from #40, 7–9 from this analysis). In priority order:

1. (sub-q 4 of #40) Replace the numeric `|a|+|b|` cap with concrete content rules: no comments in the code block, no echoing surrounding context.
2. (sub-q 2 of #40) Hoist "one side empty → take non-empty side" into the pattern hierarchy at step 1.
3. (sub-q 1 of #40) Add a worked pick-with-identifier-divergence example.
4. (sub-q 2 of #40) Add a worked verbose-vs-concise pick example.
5. (sub-q 1 of #40) Loosen "smallest reconciliation from existing tokens" wording in the custom rule.
6. (sub-q 3 of #40) Reframe the skill as primarily an over-generation guard.
7. (sub-q 2 of #41) Investigate why pattern-teaching fires unevenly between structurally similar cases.
8. (sub-q 3 of #41) Acknowledge file-level resolutions exist and are out-of-scope; skill should not pretend to solve them.
9. (sub-q 5 of #41) Decouple the pattern taxonomy from the output-discipline rules. Lead with output discipline; pattern taxonomy is secondary.

**Implication for thesis RQ1, RQ2, RQ3:**

- **RQ1 (does SKILL.md improve resolution quality?).** Yes, but predominantly via output discipline, not pattern teaching. The improvement is real on Apertus and concentrated in cases where the model would otherwise over-generate.
- **RQ2 (effect by complexity).** Out of scope here (the pilot is `python/func` only); the data so far suggests v2 helps when GT is recoverable from sides a/b plus disciplined output, and is neutral or harmful when GT requires file-level synthesis.
- **RQ3 (does small model + skill close the gap to large model without skill?).** Skill closes the **over-generation gap**; it does not close the **resolution-quality gap** (pick-side errors persist across all conditions on most cases; pattern-teaching is rare and bidirectional). Reframing RQ3 in those terms would be more defensible than the current formulation.

---

## Open sub-questions

- [x] Sub-question 1 — v2-over-v1 mechanism on Apertus is over-generation suppression. Same mechanism as Qwen3; different opportunity.
- [x] Sub-question 2 — v1-winners survived because Apertus's hallucinated baseline gives v1's "be brief" framing real work to do. `0xe63ff0dd` is the one clean pattern-teaching case across the 40-case corpus; full survey at 7.5% pattern-teaching rate (3/40).
- [x] Sub-question 3 — `0xd9272c5e` is a task-ceiling case: GT requires synthesising from a file-level pattern not present on either side. Skill correctly trims surrounding context; doing so discards a lucky alignment that no-skill happened to retain. Adds v2.1 recommendation 8.
- [x] Sub-question 4 — outlier-driven. Median Δ = 0; mean +0.034 collapses to +0.0004 after dropping top 3. Effect is real but concentrated in ≤4 cases out of 20. Sign test (7+/5−/8=) is not significant at n=20.
- [x] Sub-question 5 — pattern routing is largely orthogonal to where v2's gains come from. 3/6 Apertus wins gain through harm-reduction *despite* incorrect pattern routing. Adds v2.1 recommendation 9 (decouple pattern taxonomy from output-discipline rules).
