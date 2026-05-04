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

## Open sub-questions

- [ ] Sub-question 2: characterise the 5 v2-sys losses (`0x223b29598e1c5cb9`, `0x520debc691c88dc5`, `0x7fb96fbf0a030ea`, `0xa4d50e39def807dd`, `0xddd5322de12565fe`).
- [ ] Sub-question 3: headroom hypothesis on no-skill wins.
- [ ] Sub-question 4: output-length distribution v1 vs v2.
