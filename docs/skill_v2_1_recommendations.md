# SKILL.md v2.1 — Design Recommendations

Consolidated recommendations for the v2 → v2.1 iteration, derived from the v1-vs-v2 analyses on Qwen3-8B and Apertus-8B.

**Source analyses:**
- [`analysis_qwen3_v1_v2.md`](analysis_qwen3_v1_v2.md) — issue [#40](https://github.com/bdravec/merge-conflict-skill/issues/40) (closed 2026-05-04)
- [`analysis_apertus_v1_v2.md`](analysis_apertus_v1_v2.md) — issue [#41](https://github.com/bdravec/merge-conflict-skill/issues/41) (closed 2026-05-04)

Tracking issue for v2.1 design: *to be created*. Per design doc §3.2, this is the Option C fallback (iterate v2 from pattern-frequency EDA on real cases) before considering v3 (issue [#7](https://github.com/bdravec/merge-conflict-skill/issues/7)).

---

## Headline finding to design against

**v2 is predominantly a harm-reduction skill, not a pattern-teaching skill.** The pattern taxonomy (pick / combine / empty / custom) is largely orthogonal to v2's measured gains. What's doing the work is the output discipline around the pattern decision — length cap, "no prose, code only", suppression of surrounding-context echo. v2 could route patterns wrongly *or* rightly and still produce most of its measured gains, as long as it suppressed the surrounding fabrication.

Cross-model: same mechanism on both Qwen3 and Apertus; different *opportunity*. Apertus over-generates more often, so v2 has more chances to act, so the net Δedit reaches noise on Apertus and not on Qwen3. The "Apertus benefits, Qwen3 doesn't" framing is a function of the input distribution, not of skill effectiveness.

v2.1 should design *for* this finding: lead with the over-generation guard rules; treat the pattern taxonomy as secondary guidance.

---

## The nine recommendations

In priority order. Each entry includes the empirical finding it follows from, the concrete change to v2's text, and a source link.

### 1. Replace the numeric `|a|+|b|` cap with concrete content rules

**Current v2 text** (§"Output format"):
> The output must be no longer than `|a| + |b|` characters (the combined length of side `a` and side `b`).

**Empirical finding.** The cap is not enforced. 11/20 v2-sys outputs on Qwen3 exceed it; the worst violator (`0xc00c4d82`, cap=131) produced 2819 characters — 21× over. The cap functions as a soft "be brief" prior but does not bind on individual cases.

**Recommended change.** Replace the numeric limit with concrete content rules:
- *"Do not include any comments inside the code block unless they appear verbatim on side a or side b."*
- *"Do not echo lines from the surrounding context into the resolution unless they are part of side a or side b."*
- *"After producing the output, ask: is this longer than the union of side a and side b? If so, you have likely added unnecessary content."*

The post-hoc check at the end of generation is more enforceable than a cap-during-generation.

**Source.** [`analysis_qwen3_v1_v2.md`](analysis_qwen3_v1_v2.md) sub-q 4.

---

### 2. Hoist "one side empty → take non-empty side" into the pattern hierarchy

**Current v2 placement.** §"Edge cases" line 118: *"One side empty: take the non-empty side (this is pick, not the empty pattern — that one needs both sides to be deletions)."*

**Empirical finding.** 2/5 v2-sys losses on Qwen3 (`0x223b29598e1c5cb9`, `0x7fb96fbf0a030ea`) violate this rule. The model fires the empty test in step 1 of the pattern hierarchy before reaching the edge-case override at the bottom of the file. Under top-down reading, the override never gets applied.

**Recommended change.** Restate the rule in step 1 of §"Resolution strategy". Either:
- Reword step 1 as *"Both sides are deletions or whitespace-only → empty (produce no content). If only one side is empty, this is **pick**, not empty."*
- Or split into two sub-cases: 1a (one-side-empty → pick non-empty), 1b (both-empty → empty pattern).

**Source.** [`analysis_qwen3_v1_v2.md`](analysis_qwen3_v1_v2.md) sub-q 2 shape 1.

---

### 3. Add a worked pick-with-identifier-divergence example

**Empirical finding.** v2's pick criterion ("which side is more consistent with the surrounding code") is correct in principle but only fired correctly in 1/40 model-cases (`0xe63ff0dd` on Apertus, where v2 picked `K.placeholder` over `tf.placeholder` based on surrounding `K.` prefix style). It did not fire on the structurally similar `0xe4ff79aa` (Qwen3 picks `poolsize` instead of `pool_size` despite surrounding underscored-style consistency, and v2 fails to correct the pick; on Apertus, this case is not a pick failure — Apertus picks `pool_size` correctly in every condition without v2's intervention).

**Recommended change.** Add a worked example to §"Edge cases" that shows the Keras-vs-TF API divergence and walks through the pick criterion explicitly. Concretely:

```
<<<<<<< a
j_tf = K.placeholder(shape=(None, 32), dtype=K.floatx())
=======
j_tf = tf.placeholder(dtype=K.floatx())
>>>>>>> b
```

*"The surrounding code uses `K.` prefixes (`K.int_shape`, `K.floatx`). Pick a — its API style matches the rest of the file. Do not pick b just because it is shorter."*

**Source.** [`analysis_qwen3_v1_v2.md`](analysis_qwen3_v1_v2.md) sub-q 1; [`analysis_apertus_v1_v2.md`](analysis_apertus_v1_v2.md) sub-q 2.

---

### 4. Add a worked verbose-vs-concise pick example

**Empirical finding.** 2/5 v2-sys losses on Qwen3 (`0x520debc6`, `0xddd5322d`) come from v2 picking the more concise side when ground truth keeps the verbose side. v2's framing biases toward simplicity over completeness. The model needs explicit guidance that conciseness is not a tiebreaker.

**Recommended change.** Add a worked example showing the verbose-vs-concise pattern. The `0x520debc691c88dc5` case is a good template:

```
<<<<<<< a
if isinstance(field_name, str):
    item_field, output_field = field_name, field_name
else:
    item_field, output_field = field_name
if item_field in item:
    field = ... item.fields[item_field]
=======
if field_name in item:
    field = ... item.fields[field_name]
>>>>>>> b
```

*"Side a encodes a real semantic distinction: it handles `field_name` being either a string or a tuple, with `item_field` and `output_field` as separately-named variables. Side b flattens this away. Pick a — completeness encodes the distinction; conciseness erases it. Surrounding-code consistency is the tiebreaker, not output length."*

**Source.** [`analysis_qwen3_v1_v2.md`](analysis_qwen3_v1_v2.md) sub-q 2 shape 2.

---

### 5. Loosen the "smallest reconciliation" wording in the *custom* rule

**Current v2 text** (§"Resolution strategy" step 4 + §"Edge cases"):
> Custom escape. Only if pick cannot produce a coherent file AND combine does not apply → custom (smallest reconciliation from existing tokens).
> ... If neither side parses on its own, escape to *custom* and reconcile using only tokens from sides `a` and `b`.

**Empirical finding.** `0xa4d50e39def807dd` requires GT custom resolution that introduces tokens (`isinstance`, `list`, `tuple`) not present on either side. The "smallest reconciliation from existing tokens" wording forbids this by construction. The custom rule is therefore unable to express most real custom resolutions.

**Recommended change.** Reword to allow surrounding-context tokens (when present in the conflict context window) but maintain the "smallest reconciliation" ethos:

*"Custom escape. Only if pick cannot produce a coherent file AND combine does not apply → custom. Use tokens from sides a and b first. If those alone cannot produce a coherent resolution, use tokens from the surrounding code (within the visible context) as a secondary source. Do not invent tokens that appear nowhere."*

**Source.** [`analysis_qwen3_v1_v2.md`](analysis_qwen3_v1_v2.md) sub-q 1 case B.

---

### 6. Reframe v2.1 as primarily an over-generation guard

**Empirical finding.** v2's impact across both models is monotonic in baseline score and dominated by harm-reduction. On Qwen3: hurts top (−0.06 mean Δ), neutral middle, helps bottom (+0.025). On Apertus: 3/6 wins gain through harm-reduction *despite* incorrect pattern routing. v2 trims over-generation; it does not teach pattern competence.

**Recommended change.** Rewrite §"How to use this skill" or the skill's opening section to lead with the over-generation guard rules (recommendation 1's content rules). Move the pattern taxonomy to a secondary section. Frame the skill as:

*"You are resolving a Git merge conflict. Your job is to produce only the resolved code for the conflict region — no commentary, no extra context, no fabricated method bodies. The resolution should typically pick or combine the two sides; only escape to a custom resolution when neither pick nor combine produces a coherent file."*

The four-pattern taxonomy can remain as a checklist later in the file, but it should not be the first thing the model reads.

**Source.** [`analysis_qwen3_v1_v2.md`](analysis_qwen3_v1_v2.md) sub-q 3; [`analysis_apertus_v1_v2.md`](analysis_apertus_v1_v2.md) sub-q 5.

---

### 7. Investigate why pattern-teaching fires unevenly between structurally similar cases

> ✅ **Ablation complete (2026-05-06).** See [`docs/ablation_0xe4ff79aa.md`](ablation_0xe4ff79aa.md) for setup, results, and verdict. Headline: H1 (prompt-level) supported at the most extreme end — explicit per-case answer flips Qwen3's pick from `poolsize` to `pool_size`. H2 (model-level capability ceiling) ruled out. The proposed rec-3 worked example (Keras-vs-TF) does **not transfer** to underscore-vs-no-underscore identifier divergence on Qwen3. Implication for v2.1 § 6: keep the rec-3 example as drafted (option a in the ablation doc) and document the non-transfer finding in the thesis chapter on limitations.

**Empirical finding.** v2's pick criterion fired correctly on `0xe63ff0dd` Apertus (picked `K.placeholder` over `tf.placeholder` per surrounding `K.` prefix). On the structurally similar `0xe4ff79aa`, the firing pattern is **model-dependent**: Apertus picks `pool_size` (correct) in every condition without v2's intervention; Qwen3 picks `poolsize` (wrong) in every condition and v2 fails to correct it. Both are identifier-divergence-with-surrounding-context-tiebreaker cases. The mechanism that determines whether v2's pick criterion is needed and whether it activates is model-dependent and not currently characterised.

**Recommended action.** This is a research/diagnostic recommendation, not a SKILL.md edit. Before v2.1 is finalised, run an ablation on `0xe4ff79aa` against **Qwen3** (the model that fails this case) with explicit pick-criterion prompting (e.g. *"surrounding code uses underscores in identifiers — pick `pool_size`"* added as a hint) to see if the fix is at the prompt level or the model level. If prompt-level, the v2.1 worked example (recommendation 3) should fix it. If model-level, document as a capability ceiling. Tracked in issue [#44](https://github.com/bdravec/merge-conflict-skill/issues/44).

**Source.** [`analysis_apertus_v1_v2.md`](analysis_apertus_v1_v2.md) sub-q 2.

---

### 8. Acknowledge file-level resolutions exist and are out of scope

**Empirical finding.** `0xd9272c5e0e8f15ee` has a GT resolution that abandons both sides and synthesises a new line consistent with a file-level architectural pattern (`x += reshape(bias, ...)` matches the analogous lines for ndim=3 and ndim=5 in the same file). v2's *custom escape* rule, even after recommendation 5's loosening, cannot reach this. The case is a task-ceiling, not a skill failure.

**Recommended change.** Add a short acknowledgement to §"Edge cases":

*"Some conflicts have ground-truth resolutions that depend on file-level patterns invisible from the conflict region alone (e.g. an architectural decision the rest of the file encodes but the conflict snippet does not). The skill cannot solve these. If neither pick, combine, empty, nor custom (within the visible context) produces a coherent resolution, your best bet is the closest pick — the metric will reward it more than over-confident invention."*

**Source.** [`analysis_apertus_v1_v2.md`](analysis_apertus_v1_v2.md) sub-q 3.

---

### 9. Decouple the pattern taxonomy from the output-discipline rules

**Empirical finding.** v2's pattern taxonomy is largely orthogonal to v2's measured gains. 2/6 Apertus v2-sys winners gain through harm-reduction *despite* applying the wrong pattern (`0x96d20e6c` picks b vs GT pick-a; `0xddd5322d` combine vs GT custom). The output discipline does the work; the pattern taxonomy is mostly inert. (Original analysis listed 3/6 here, with `0xe4ff79aa` grouped as wrong-pick on Apertus; cross-model verification corrected this — Apertus picks `pool_size` correctly on `0xe4ff79aa` in every condition, so v2's win there is harm-reduction with already-correct routing, not despite-wrong routing.)

**Recommended change.** Restructure the SKILL.md document so that:
1. **§Output discipline** (over-generation guards from recommendation 1) comes first, framed as the primary requirement.
2. **§Pattern taxonomy** (pick / combine / empty / custom) comes second, framed as guidance for cases where the model's no-skill behaviour is already focused.

This reframes the skill from *"here is how to resolve conflicts"* to *"here is how to cleanly produce whatever resolution you would otherwise produce."* The empirical data supports the latter framing more strongly.

**Source.** [`analysis_apertus_v1_v2.md`](analysis_apertus_v1_v2.md) sub-q 5.

---

## Implementation order

If the v2.1 implementation is to be staged, I would do it in this order:

1. **Recommendations 1, 6, 9** — the core reframing. These together produce a meaningfully different SKILL.md. Test in isolation: re-run the pilot on both models with these changes alone and check if the harm-reduction effect strengthens (Qwen3 should move from −0.012 toward zero; Apertus should hold or improve at +0.034).
2. **Recommendations 2, 3, 4** — pattern-clarification additions. Layer onto the reframed v2.1. Test for whether they lift the pattern-teaching rate above 7.5%.
3. **Recommendations 5, 8** — custom-rule scope. Lower priority because they affect a small number of cases (the custom and task-ceiling cases).
4. **Recommendation 7** — diagnostic ablation. Run before finalising recommendation 3's worked example.

This staging lets the analysis isolate whether the reframing alone (1/6/9) is sufficient, or whether the additional clarifications (2/3/4) are doing meaningful additional work.

---

## What this design does *not* address

- **Pattern-teaching uplift.** The 7.5% pattern-teaching rate is a corpus-level finding at n=20. v2.1's recommendations may shift it but are not designed to multiply it. If the thesis needs a stronger pattern-teaching story, that's a v3 question (per issue #7), not v2.1.
- **Metric tension.** Sub-q 3 of #41 surfaced that the ConGra edit-similarity metric rewards leak as a proxy for pattern-recognition. This is a metric problem, not a skill problem; v2.1 cannot fix it. Document as a Chapter 7 limitation.
- **Sample size.** All these recommendations come from n=20 per model on `python/func` only. Before v2.1 is canonised, the recommendations should be sanity-checked on a larger sample or a different language/conflict-type bucket.
