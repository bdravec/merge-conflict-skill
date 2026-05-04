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

All five losses share a single underlying tendency: **v2-sys produces shorter outputs than no-skill, and the shorter output is the wrong answer.** This is consistent with finding 5 in the v2 results doc (v2 produces more no-skill-identical outputs, and when it diverges, it diverges shorter). The length cap, the empty-pattern position in the hierarchy, and the "smallest reconciliation" wording in the custom rule all push in the same direction.

### v2.1 implications (sub-q 2 additions)

Adding to the two recommendations from sub-q 1:

3. **Move the "one side empty" override into the pattern hierarchy.** The current edge-case position is too late in the document for the model to apply it under top-down reading. Either re-state it in step 1 of §"Resolution strategy" (*"Both sides are deletions or whitespace-only — note that if only one side is empty, this is **pick**"*) or split the empty test into two sub-cases (one-side-empty → pick non-empty, both-empty → empty pattern).

4. **Add a "verbose vs concise" worked example.** v2's pick criterion needs an example where the verbose side is correct. The `0x520debc6…` case (tuple-or-string handling) is a good candidate template, since the verbose side encodes a real semantic distinction (separate `item_field` and `output_field`) that the concise side flattens away. The skill should make explicit that *concise is not a tiebreaker*; surrounding-code consistency is.

5. **The length cap discussion should reference shapes 1 + 3 together.** Sub-q 1 already flagged the cap as too tight on combine; sub-q 2 adds that the same cap-driven minimisation pressure leaks into pick decisions ("when in doubt, pick shorter"). v2.1's revised cap should make clear that the cap blocks *over-generation only* and is not a target.

---

## Open sub-questions

- [x] Sub-question 2 — three shapes identified (one-side-empty pick error, verbose-vs-concise pick error, length-cap structural trim). v2.1 has 5 concrete recommendations.
- [ ] Sub-question 3: headroom hypothesis on no-skill wins.
- [ ] Sub-question 4: output-length distribution v1 vs v2.
