# Analysis — Qwen3-8B v1 vs v2 SKILL.md

**Date:** 2026-05-04
**Issue:** [#40](https://github.com/bdravec/merge-conflict-skill/issues/40)
**Inputs:**
- v1-skill 3-condition: [`pilot_results_qwen3_v2.md`](pilot_results_qwen3_v2.md), `scripts/results/pilot_results_qwen3_v2.jsonl`
- v2-skill 3-condition: [`pilot_results_qwen3_skill-v2.md`](pilot_results_qwen3_skill-v2.md), `scripts/results/pilot_results_qwen3_skill-v2.jsonl`
- v2 design rationale: [`skill_v2_design.md`](skill_v2_design.md)

> **Premise correction.** Issue #40's headline framed `0xa4d50e39def807dd` and `0xe63ff0ddae988357` as "v1 winners that v2 lost." That framing was wrong (see correction note in [`pilot_results_qwen3_skill-v2.md`](pilot_results_qwen3_skill-v2.md) §6). Both cases were v1's two **biggest losers** on Qwen3, and v2-sys actually *improves* one of them (`0xe63ff0dd`: −0.40 → 0.00). The interesting question is therefore not "what did v1 do that v2 stopped doing" but **"how does the failure mode change between v1 and v2 on these two cases, and what does that tell us about v2.1?"** This analysis answers the reframed question for sub-question 1.

---

## Sub-question 1 (reframed) — failure-mode comparison on `0xa4d50e39` and `0xe63ff0dd`

### Per-condition edit scores

| Case | no-skill | v1-sys | v1-user | v2-sys | v2-user |
|---|---:|---:|---:|---:|---:|
| `0xa4d50e39def807dd` | 0.6000 | 0.4815 | 0.4815 | **0.4519** | 0.4815 |
| `0xe63ff0ddae988357` | 0.8364 | 0.4369 | 0.3600 | **0.8364** | 0.6026 |

Bold marks the v2-sys cell — the cell the issue's table flagged as a regression.

### Case A — `0xe63ff0ddae988357` (test_topology.py, conflict #1)

**Conflict:**
```
<<<<<<< a
    j_tf = K.placeholder(shape=(None, 32), dtype=K.floatx())
    k_tf = K.placeholder(shape=(None, 32), dtype=K.floatx())
    m_tf, n_tf = outer_model([j_tf, k_tf])
    assert K.int_shape(m_tf) == (None, 64)
    assert K.int_shape(n_tf) == (None, 5)
=======
        j_tf = tf.placeholder(dtype=K.floatx())
        k_tf = tf.placeholder(dtype=K.floatx())
        m_tf, n_tf = tf_model([j_tf, k_tf])
        assert m_tf.get_shape().as_list() == [None, 64]
        assert n_tf.get_shape().as_list() == [None, 5]
>>>>>>> b
```

**Ground truth:** **exact pick-a** (both content and indentation). Side b is discarded entirely.

| Condition | Output (truncated) | Pattern | Issue |
|---|---|---|---|
| no-skill (0.84) | a's `K.placeholder` ✓, but b's `tf_model` and b's `m_tf.get_shape()` | partial pick-a (mixed identifiers) | identifier-leak from b |
| v1-sys (0.44) | b's `tf.placeholder(dtype=...)` + over-generation block (`# test merge`, `concatenate`, `add`) | wrong-side + over-generation | flips to b *and* synthesises new code |
| v1-user (0.36) | adds invented preamble (`Input(...)`, `outer_model = Model(...)`), then b's `tf.placeholder`, plus over-generation | custom-from-imagination | worst output of the four |
| **v2-sys (0.84)** | **byte-identical to no-skill** | inert | length cap + "no prose" suppressed v1's failure modes |
| v2-user (0.60) | a's `K.placeholder` ✓, but kept the over-generation block | partial pick-a + over-generation | sys-injection blocks the over-gen, user-injection doesn't |

**Reading.** v1 took a textbook pick-a case and made it worse in two ways: it picked the wrong side, and it synthesised code outside the conflict markers (the `# test merge` / `concatenate` / `add` block). v2-sys's length cap (`≤ |a|+|b|`) and "no prose, code only" rule shut down the synthesis path entirely; the model fell back to whatever it produces with no skill at all. v2-sys did **not** teach the model to pick a more cleanly than no-skill did — it just stopped the bleeding.

### Case B — `0xa4d50e39def807dd` (tensorflow_backend.py, conflict #1)

**Conflict:**
```
<<<<<<< a
    with tf_ops.init_scope():
        return variable(tf.eye(size, dtype=dtype), dtype, name)
=======
    tf_dtype = tf.as_dtype(dtype)
    return variable(tf.eye(size, dtype=tf_dtype), dtype, name)
>>>>>>> b
```

**Ground truth:** **custom**. Adds a brand-new `if isinstance(size, (list, tuple)): n, m = size; else: n, m = size, size` preamble, keeps `with tf_ops.init_scope():` from a, uses `tf_dtype` from b, and changes `tf.eye(size, ...)` → `tf.eye(n, m, ...)`. The unpacking line exists on neither side and cannot be derived by combine.

| Condition | Output | Pattern | Issue |
|---|---|---|---|
| no-skill (0.60) | b's `tf_dtype = tf.as_dtype(dtype)` + a's `with tf_ops.init_scope():` + b's body inside a's scope | clean **combine** | best non-custom answer; misses the n,m unpack |
| v1-sys/user (0.48) | adds `if dtype is None: dtype = floatx()` (context-leak), drops `init_scope`, keeps b's two lines | combine + leak − init_scope | introduces a line from outside the conflict region |
| **v2-sys (0.45)** | only `tf_dtype = tf.as_dtype(dtype)` and `return variable(tf.eye(size, dtype=tf_dtype), dtype, name)` | pure **pick-b** | length cap killed the `init_scope` line that was correct in no-skill |
| v2-user (0.48) | same as v1-sys | combine + leak − init_scope | sys-injection trims more aggressively than user-injection |

**Reading.** No-skill produced the **optimal non-custom answer**: a clean combine that keeps `init_scope` from a and `tf_dtype` from b. Both skill versions corrupted it. v1's failure mode was a context-leak (`if dtype is None: dtype = floatx()` from above the conflict); v2-sys's failure mode was the opposite — its stricter length cap stripped `with tf_ops.init_scope():` and produced pure pick-b. **v2-sys is a real regression here**, and the cause is identifiable: the length cap is too aggressive when the optimal output is essentially `len(a) + len(b) - len(overlap)`.

The case is also a custom-pattern case, so neither v1 nor v2 can score above ~0.60 without producing the n,m unpacking line. The skill's job here is therefore to *not make it worse*; v2-sys fails that bar.

---

## What v1 was doing that v2 stopped doing

| Behaviour | v1 | v2-sys |
|---|---|---|
| Synthesise new code outside the conflict region | yes (`0xe63ff0dd`'s `# test merge` block) | no (length cap blocks it) |
| Leak unrelated lines from surrounding context | yes (`0xa4d50e39`'s `if dtype is None: dtype = floatx()`) | sometimes (v2-user only) |
| Pick the wrong side | yes (`0xe63ff0dd`'s `tf.placeholder`) | inherits no-skill's choice (passive) |
| Drop already-correct lines under length pressure | no | yes (`0xa4d50e39`'s `init_scope`) |

v2 traded one failure mode (over-generation, context-leak) for a different one (over-trimming under the length cap). On `0xe63ff0dd` the trade is positive (no-skill happened to be near-optimal). On `0xa4d50e39` the trade is negative (no-skill *was* optimal, v2 took bites out of it).

> **Cross-reference (added 2026-05-04):** the `0xa4d50e39` regression on Qwen3 also fits a different framing developed in [`analysis_apertus_v1_v2.md`](analysis_apertus_v1_v2.md) sub-q 2 — it is the one case in the 40-case corpus where v2 changed the model's *pattern* decision in the wrong direction (combine → pick-b). The Apertus analysis identifies one right-direction pattern-teaching event (`0xe63ff0dd` Apertus pick-correction) and one marginal one (`0xddd5322d` Apertus combine attempt). v2's pattern-teaching effect is real but rare (3/40 model-cases) and bidirectional. The harm-reduction story remains primary on both models.

---

## Implications for v2.1

Two concrete edits to SKILL.md v2 follow from this analysis.

1. **Loosen the length cap.** v2 §"Output format" says: *"The output must be no longer than `|a| + |b|` characters."* For combine-pattern cases the optimal output approaches `|a| + |b|` minus the overlap; a strict cap discourages preserving lines that should be preserved. Either drop the cap to a soft guideline ("avoid output longer than `|a| + |b|`") or rephrase as a check against over-generation specifically (e.g., "if your output is longer than `|a| + |b|`, you have likely added unnecessary code").

2. **Add a worked pick-with-identifier-divergence example.** v2 §"Edge cases" covers imports and broken syntax but not the case where two sides use different APIs for the same operation (`K.placeholder` vs `tf.placeholder`, `K.int_shape` vs `.get_shape().as_list()`). The skill's pick-criterion ("which side is more consistent with the surrounding code") is correct in principle but didn't transfer here. A worked example showing a Keras-vs-TF divergence resolved by pick-a would fill the gap. This is exactly the kind of pattern Option C (pattern-frequency EDA) should surface from the broader dataset.

A third recommendation requires a separate run to test:

3. **Distinguish "custom escape" from "do nothing."** `0xa4d50e39` shows that when ground truth requires inventing a new preamble, both v1 and v2 fall back to combine and cap at ~0.60. v2 §"Custom escape" says *"smallest reconciliation from existing tokens"* — but the n,m unpacking case requires tokens (`isinstance`, `list`, `tuple`) that don't exist on either side. Either v2.1 needs to broaden "existing tokens" to include the surrounding context, or it needs to acknowledge that some custom resolutions are not recoverable from a surface-level skill and should be labelled as such in the evaluation.

---

## Sub-question 2 — what characterises the 5 v2-sys losses?

The five cases where v2-sys scores below no-skill are `0x223b29598e1c5cb9`, `0x520debc691c88dc5`, `0x7fb96fbf0a030ea`, `0xa4d50e39def807dd`, and `0xddd5322de12565fe`. `0xa4d50e39` is already characterised above (case B). The remaining four cluster into two recurring shapes.

### Shape 1 — "one side empty, v2 picks the empty side" (2/5)

| Case | Side a | Side b | v2-sys output |
|---|---|---|---|
| `0x223b29598e1c5cb9` | `assert self.subsample == (1, 1)` | (empty) | dropped the assert (took b) |
| `0x7fb96fbf0a030ea` | `if isinstance(mask, list): return mask[0]` | (empty) | dropped the lines (took b) |

In both, side b is a deletion (empty content) while side a adds a guard. v2 §"Edge cases" line 118 explicitly says *"One side empty: take the non-empty side (this is pick, not the empty pattern — that one needs both sides to be deletions)."* The model violated this rule on both cases.

The mechanism appears to be ordering. v2's pattern hierarchy at the top of §"Resolution strategy" lists the **empty test** as step 1: *"Both sides are deletions or whitespace-only → empty (produce no content)."* The edge-case override that says "one side empty is *pick*, not *empty*" is buried in §"Edge cases" near the end of the file. A model under temperature 0 that reads top-down and stops at the first matching rule will fire the empty pattern when one side is whitespace and never reach the override.

In both cases the ground truth is custom anyway, so no skill version recovers fully — but no-skill and v1-sys at least kept side a's lines (Δ = 0 vs no-skill), giving them a higher score on the surrounding context. v2-sys threw those lines away.

### Shape 2 — "v2 picks the more concise side when ground truth wants the verbose side" (2/5)

| Case | Side a (verbose) | Side b (concise) | Ground truth | v2-sys |
|---|---|---|---|---|
| `0x520debc691c88dc5` | tuple-or-string handling for `field_name`, separate `item_field`/`output_field` | one-line `field_name` lookup | extends side a | pick-b |
| `0xddd5322de12565fe` | `if mask is not None:` (one-line guard) | `if mask is None: ... else:` (multi-line) | side a + new context | pick-b |

`0x520debc6…` is the cleaner of the two: side a explicitly adds a code path that ground truth keeps, side b removes it. v2 takes side b. `0xddd5322d…` is the inverse case (side b is the verbose one); v2 again takes the more elaborated form, which happens to be wrong here.

The unifying mechanism is not "shorter side" specifically — it is *whichever side the model judges syntactically simpler under the v2 framing*. v2's pick criterion ("which side is more consistent with the surrounding code") is the one rule that should help here, but the length cap and the "no prose, code only, smallest reconciliation" framing all bias toward simplicity over completeness. When the verbose side is the correct one, that bias hurts.

### Shape 3 — "custom case + length cap trims a correct line" (1/5)

`0xa4d50e39def807dd`. Already covered as case B above. The v2 length cap stripped `with tf_ops.init_scope():` from a clean combine that no-skill produced.

### Cross-cutting observation

Four of the five losses share a single underlying tendency: **v2-sys produces shorter outputs than no-skill, and the shorter output is the wrong answer.** The exception is `0xddd5322d` — see sub-q 4 for the corrected picture (v2 *lengthens* that case rather than shortening it; the failure is over-generation, not under-generation). For the other four (`0x223b2959`, `0x520debc6`, `0x7fb96fbf`, `0xa4d50e39`), the length cap, the empty-pattern position in the hierarchy, and the "smallest reconciliation" wording in the custom rule all push the model toward outputs that are too short.

### v2.1 implications (sub-q 2 additions)

Adding to the two recommendations from sub-q 1:

3. **Move the "one side empty" override into the pattern hierarchy.** The current edge-case position is too late in the document for the model to apply it under top-down reading. Either re-state it in step 1 of §"Resolution strategy" (*"Both sides are deletions or whitespace-only — note that if only one side is empty, this is **pick**"*) or split the empty test into two sub-cases (one-side-empty → pick non-empty, both-empty → empty pattern).

4. **Add a "verbose vs concise" worked example.** v2's pick criterion needs an example where the verbose side is correct. The `0x520debc6…` case (tuple-or-string handling) is a good candidate template, since the verbose side encodes a real semantic distinction (separate `item_field` and `output_field`) that the concise side flattens away. The skill should make explicit that *concise is not a tiebreaker*; surrounding-code consistency is.

5. **The length cap discussion should reference shapes 1 + 3 together.** Sub-q 1 already flagged the cap as too tight on combine; sub-q 2 adds that the same cap-driven minimisation pressure leaks into pick decisions ("when in doubt, pick shorter"). v2.1's revised cap should make clear that the cap blocks *over-generation only* and is not a target.

---

## Sub-question 4 — output length distribution v1 vs v2

The skill v2 §"Output format" rule states *"the output must be no longer than `|a| + |b|` characters."* Sub-q 4 asks whether that rule actually changes output lengths, and whether shortening helps or hurts edit similarity.

### Aggregates (n=20, character lengths)

| Condition | median | mean | over-cap | edit mean |
|---|---:|---:|---:|---:|
| no-skill | 323.5 | 518.5 | 13/20 | 0.3953 |
| skill-v1-sys | 355.5 | 514.7 | 12/20 | 0.3479 |
| skill-v1-user | 485.0 | 591.0 | 15/20 | 0.3511 |
| **skill-v2-sys** | **274.5** | **428.1** | **11/20** | **0.3836** |
| skill-v2-user | 308.0 | 471.6 | 11/20 | 0.3558 |

**v2 does shorten outputs.** Median length drops from 324 to 275 (−15%), mean from 519 to 428 (−17%) under v2-sys. v1 does *not* shorten — v1-sys median is actually higher than no-skill (356 vs 324), and v1-user is much longer (485). The shortening is a v2-specific effect.

### The `|a|+|b|` cap is not enforced

11/20 v2-sys outputs exceed the cap, including some egregious violators:

| Case | cap | v2-sys length | factor |
|---|---:|---:|---:|
| `0xc00c4d82b7364e6d` | 131 | 2819 | 21.5× |
| `0x32d8c89b39c2860b` | 54 | 903 | 16.7× |
| `0x425cf8014eda936b` | 88 | 810 | 9.2× |
| `0xddd5322de12565fe` | 116 | 396 | 3.4× |

The cap is doing what a soft prior does — it shifts the distribution toward shorter outputs — but it does not bind on individual cases. A model that respected the cap would never produce a 2819-character output for a conflict with `|a|+|b|=131`. The cap is currently functioning as a vague "be brief" signal, not an enforced constraint.

### Length-shift vs edit-shift relative to no-skill

| Condition | shorter (n) | mean Δedit | longer (n) | mean Δedit | same (n) |
|---|---:|---:|---:|---:|---:|
| skill-v1-sys | 4 | −0.025 | 10 | −0.085 | 6 |
| skill-v1-user | 2 | −0.019 | 13 | −0.065 | 5 |
| **skill-v2-sys** | **10** | **−0.007** | **1** | **−0.163** | **9** |
| skill-v2-user | 8 | −0.008 | 5 | −0.146 | 7 |

Two readings:

1. **v1 hurt the most when it lengthened.** The 10–13 cases where v1 produced longer outputs averaged Δedit −0.07 to −0.09 — the dominant failure mode for v1 was over-generation. Fixing that was the central design intent of v2.
2. **v2-sys's shortening is net neutral on average (−0.007), but variance is high.** The 10 v2-sys shortenings break down as:

| Case | Δlen | Δedit | reading |
|---|---:|---:|---|
| `0x96d20e6c9b0f2395` | −432 | **+0.184** | trimmed over-generation |
| `0x999797db0c12ab9d` | −410 | **+0.136** | trimmed over-generation |
| `0x32d8c89b39c2860b` | −234 | +0.064 | trimmed over-generation |
| `0xc00c4d82b7364e6d` | −472 | +0.040 | trimmed over-generation |
| `0x6081a18de8689da7` | −203 | +0.009 | trimmed over-generation |
| `0xc6a534710cc98bb7` | −1 | 0.000 | tiny trim, no effect |
| `0x223b29598e1c5cb9` | −41 | −0.037 | trimmed correct content |
| `0x7fb96fbf0a030ea` | −70 | **−0.099** | trimmed correct content |
| `0xa4d50e39def807dd` | −34 | **−0.148** | trimmed correct content |
| `0x520debc691c88dc5` | −184 | **−0.222** | trimmed correct content |

The split is clean: shortening **helps** when no-skill was over-generating (top half — large trims, positive Δedit), and **hurts** when no-skill was already close to optimal (bottom half — smaller trims, negative Δedit). The net is nearly neutral because the gains and losses are similar in magnitude.

### The one v2-sys case that lengthened

`0xddd5322de12565fe`: no-skill=125 → v2-sys=396 (+271 chars), Δedit −0.163. Both v1 and v2 add an over-generation block (`# build an all-zero tensor…`, `initial_output = T.unbroadcast(…)`) that exists nowhere in the conflict region. The skill text doesn't suppress this — the model attaches the comment+code block regardless of the skill content. This is the same case that contradicts sub-q 2's cross-cutting "shorter is wrong" framing (corrected above).

### Implication for v2.1 — replace the cap with an over-generation guard

The character-count cap is the wrong mechanism. The model can't reliably count characters at inference time, and the cap is violated by 21× in the worst case. What the cap is *trying* to express — "don't add commentary or external code beyond the conflict region" — should be stated directly as content rules, not as a numeric limit:

- **Don't add comments inside the code block.** Already in v2 §"Output format" but not as its own rule. Promote to a top-level constraint.
- **Don't repeat content from the surrounding context unless the resolution requires it.** The cases that blow the cap by 9–21× are all wrapping the resolution in re-explanations of the conflict context (`0xc00c4d82` is a 25× explainer; `0x425cf8014eda936b` is a 9× explainer). Stating "do not echo the surrounding context back" would be more enforceable than a length number.
- **Replace the numeric cap with a check.** *"After producing the output, ask: is this longer than the union of side a and side b? If so, you have likely added unnecessary content."* The check at the end of generation is more likely to fire than a cap-during-generation.

This refines v2.1 recommendation 5 from sub-q 2 (which already said "reframe the length cap as an over-generation guard") with concrete content.

### Summary of length findings

- v2 shortens outputs (median −15%); v1 does not.
- The cap is not enforced — the worst violator is 21× over.
- Shortening helps when no-skill was over-generating, hurts when no-skill was close to optimal. v2's net effect on the 10 shortened cases is nearly zero.
- v1's dominant failure mode was over-generation; v2 mitigates it but at the cost of trimming correct content in 4–5 cases.
- One v2-sys loss (`0xddd5322d`) is a *length-up* failure, not a length-down failure.

---

## Sub-question 3 — headroom hypothesis

The hypothesis: Qwen3-8B's no-skill baseline (0.40 edit mean) is ~33% higher than Apertus-8B's (0.30). If Qwen3 is already producing the resolutions v2 tries to teach, v2 has little headroom and the cases where v2 helps should concentrate at the bottom of the score distribution, not the top.

### Bucket effect

Splitting the 20 cases by no-skill baseline:

| Baseline tier | n | no-skill µ | v2-sys µ | Δ µ | byte-identical to no-skill |
|---|--:|--:|--:|--:|--:|
| High (≥0.50) | 6 | 0.6734 | 0.6117 | **−0.0617** | 4/6 |
| Mid (0.30–0.50) | 7 | 0.3920 | 0.3861 | −0.0060 | 0/7 |
| Low (<0.30) | 7 | 0.1603 | 0.1855 | **+0.0252** | 5/7 |

v2 *hurts* high-baseline cases, is neutral in the middle, and *helps* low-baseline cases. The pattern is monotonic in the baseline-score axis.

### Where v2 actually changes the output

In the high bucket, 4/6 v2-sys outputs are byte-identical to no-skill — v2 has zero influence. The two divergent cases (`0x520debc691c88dc5` and `0xa4d50e39def807dd`) both regressed (covered as case B and as shape 2 elsewhere in this doc). In the low bucket, 5/7 are byte-identical too. The two divergent cases (`0x999797db0c12ab9d`: Δ +0.136, `0xc00c4d82b7364e6d`: Δ +0.040) both gained — and both gains came from v2 trimming runaway over-generation that no-skill produced (length-shifts of −410 and −472 chars respectively, see sub-q 4).

So v2's net effect on Qwen3 is a sum of (a) doing nothing in 9/20 cases, (b) trimming a few real over-generations in low-baseline cases, and (c) corrupting a few high-baseline cases by trimming or mis-routing.

### Are the top no-skill scorers actually applying v2 patterns?

For the headroom hypothesis to hold, the top no-skill scorers should already implement textbook *pick* / *combine* / *empty* / *custom*. Sampled inspection of the top six:

| Case | no-skill | what no-skill produces | v2 pattern | correctly applied? |
|---|--:|---|---|---|
| `0xe63ff0dd` | 0.84 | pick-a (with some identifier-leak from b) | pick | ✅ partially (mixes b's `tf_model`, `get_shape`) |
| `0xe4ff79aa` | 0.79 | pick-b (`poolsize`) | pick | ❌ ground truth wants a (`pool_size`); high score is metric forgiveness — sides differ only by underscores |
| `0x8e6579cb` | 0.67 | pick-a (4-space indentation) | pick | ✅ |
| `0x520debc6` | 0.65 | pick-a (verbose tuple-or-string handling) | pick | ✅ |
| `0xa4d50e39` | 0.60 | combine (b's `tf_dtype` + a's `init_scope`) | combine | ✅ (optimal non-custom answer) |
| `0x6cdd08d5` | 0.50 | pick-b (`o._keras_shape`) | pick | ❌ ground truth wants a (`o.get_shape().as_list()`); again metric forgiveness |

**4/6 are real pattern applications.** Qwen3's no-skill behaviour on these cases is what v2 would prescribe. **2/6 score high despite picking the wrong side**, because the ConGra edit-similarity metric is forgiving when sides have heavy token overlap (`pool_size`/`poolsize`, `get_shape`/`_keras_shape`). v2 doesn't fix these — it produces the same wrong-side output as no-skill — but neither does it hurt them.

**Update (2026-05-06).** The `0xe4ff79aa` case has acquired additional analytical weight after the cross-model verification recorded in `analysis_apertus_v1_v2.md`'s correction note. Apertus picks `pool_size` (correct) on this case in every condition, while Qwen3 picks `poolsize` (wrong) in every condition — the same identifier-divergence task is solved correctly by one 8B model and incorrectly by the other. v2 doesn't shift Qwen3's pick under any of the three conditions (no-skill, v2-sys, v2-user), suggesting either (a) v2's pick criterion as written is insufficient for Qwen3 to apply, or (b) Qwen3 has a model-specific blind spot for this category of identifier-divergence. **This is the target case for the rec 7 diagnostic ablation (issue #44).**

### Verdict on the headroom hypothesis

**Supported.** Three pieces of evidence converge:

1. **Distributional.** v2's impact is monotonic in baseline score: hurts the top (−0.06), neutral in the middle, helps the bottom (+0.025). This is the signature of a skill that operates by trimming/shortening — it has the most room to act when the model is over-generating, and acts as a (sometimes harmful) constraint when the model is already producing close-to-optimal output.

2. **Mechanistic.** Inspection of top no-skill scorers shows Qwen3 is already applying *pick* and *combine* in the way v2 prescribes (4/6 cases), and v2-sys is byte-identical to no-skill on 4/6 of those high cases — the skill content has no purchase. Where v2 *does* divert from no-skill at the high end, it diverts in the wrong direction (case B: `0xa4d50e39`).

3. **Symmetric on the low end.** Low-baseline cases that v2 changed all changed for the better, because the failure mode there was over-generation — a problem v2's framing (length cap, "no prose") attacks directly. v2 doesn't teach the model new resolution patterns; it teaches the model to produce less commentary.

### Implications for the thesis framing

This reframes what "SKILL.md improves merge conflict resolution" means at 8B scale on Qwen3:

- **v2 is doing harm-reduction, not skill-elevation.** It mostly stops the model from over-generating, which improves scores in low-baseline cases. It does not give the model new resolution-pattern competence; the patterns Qwen3 was going to apply with no skill are the ones it applies with v2.
- **The high-baseline ceiling is real.** The cases where Qwen3 plateaus at 0.5–0.85 mostly already implement the right v2 pattern. Pushing scores higher in those cases requires the model to invent custom resolutions (case B's `n, m = size` unpack), which neither v1 nor v2 elicits and which is bounded by 8B-scale capability.
- **v2's positive Apertus-8B result becomes more coherent.** Apertus has lower no-skill baseline (0.30 vs Qwen3's 0.40), so more of its cases fall into the bucket where v2's harm-reduction mechanism has room to help. Headroom is asymmetric across models — RQ3 ("does small model + skill close the gap to large model without skill") may need re-framing as "does skill close the over-generation gap, leaving the resolution-quality gap intact."

### v2.1 implications (sub-q 3 additions)

The four prior recommendations stand. The headroom finding adds one more:

6. **Make v2's harm-reduction explicit, not implicit.** v2 currently tries to be both an over-generation guard and a pattern teacher. The data says it succeeds at the first and largely fails at the second. v2.1 could more directly state the over-generation guard rules (per sub-q 4 recommendation 5: no comments in code block, no echoing surrounding context) and de-emphasise the pattern hierarchy, since the model already executes the patterns when its output stays focused. Alternative framing: lead the skill with "Common failure mode: explanation-wrapping. Don't." rather than with the four-pattern taxonomy.

---

## Final synthesis

Across all four sub-questions:

- **Sub-q 1.** The two cases the issue framed as "v1 wins lost by v2" were actually v1's biggest losers; v2 recovered one (`0xe63ff0dd`) by going inert and worsened the other (`0xa4d50e39`) by trimming a correct combine line.
- **Sub-q 2.** The five v2-sys losses cluster into three shapes: empty-side mis-pick (rule ordering bug), verbose-vs-concise mis-pick (length bias bleeding into pick decisions), and length-cap structural trim. All point to v2's minimisation pressure being too strong.
- **Sub-q 3.** v2's impact is monotonic in baseline score: harmful at the top, neutral in the middle, helpful at the bottom. The headroom hypothesis is supported. v2 is doing harm-reduction (trimming over-generation), not skill-elevation.
- **Sub-q 4.** v2 does shorten outputs (median −15%); the `|a|+|b|` cap is not enforced (worst violator 21× over). Shortening is net neutral on average — helps when no-skill was over-generating, hurts when no-skill was close to optimal.

**Six v2.1 recommendations**, in priority order:

1. (sub-q 4) Replace the numeric `|a|+|b|` cap with concrete content rules: no comments in the code block, no echoing of surrounding context. The cap as a number is not enforced; the cap as a content rule can be.
2. (sub-q 2) Hoist the "one side empty → take non-empty side" rule into the pattern hierarchy at step 1, not the edge-case section.
3. (sub-q 1) Add a worked pick-with-identifier-divergence example (Keras vs TF API) to the edge cases.
4. (sub-q 2) Add a worked verbose-vs-concise pick example showing that completeness can be the right tiebreaker.
5. (sub-q 1) Loosen the structural pressure of "smallest reconciliation" wording in the *custom* rule — flag that custom resolutions sometimes require new tokens.
6. (sub-q 3) Reframe the skill as primarily an over-generation guard. Lead with "don't wrap the resolution in commentary"; the pattern taxonomy is secondary because the model already executes most patterns correctly when its output stays focused.

---

## Open sub-questions

- [x] Sub-question 2 — three shapes identified.
- [x] Sub-question 3 — headroom hypothesis supported. v2 does harm-reduction, not skill-elevation.
- [x] Sub-question 4 — v2 shortens; cap not enforced; net neutral on shortening cases.
