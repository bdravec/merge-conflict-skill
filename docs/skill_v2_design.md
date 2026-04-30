# SKILL.md v2 — Design Notes

This document captures the analysis and design decisions behind SKILL.md v2 (`merge-conflict-resolve-v2`). It is a living document: it starts as a gap analysis grounded in v1 and the v2 pilot results, and grows into a section-by-section rationale as design choices are made. It feeds Chapter 4 (Skill Design) of the thesis.

Tracking issue: [#6 — Write SKILL.md v2 — detailed](https://github.com/bdravec/merge-conflict-skill/issues/6).

---

## 1. What v1 Provides

`skills/merge-conflict-resolve-v1/SKILL.md` (47 lines) is intentionally minimal — the experimental baseline against which v2 must improve. It contains:

- A task description and a definition of Git conflict markers
- Five generic resolution steps: locate the region, read both sides, read surrounding code, choose a resolution, produce the file
- An output-format specification: a single fenced code block, no prose

What v1 does **not** contain, and what v2 is being written to add:

- Any distinction between conflict types (text / syntax / functional)
- Worked examples
- Edge cases (empty side, identical sides, imports, broken syntax)
- Any explanation of *why* a particular strategy is recommended

---

## 2. Constraints From the v2 Pilot

The 3-condition pilot (no-skill / skill-v1-sys / skill-v1-user) on Qwen3-8B and Apertus-8B (n=20 each, `python/func`) is documented in `pilot_results.md`. Four findings shape what v2 must do:

1. **Skill v1 hurt Qwen3-8B and was near-neutral for Apertus-8B.** Edit-mean dropped −0.04 to −0.05 on Qwen3 with both injection positions. More skill text is not automatically better — every section v2 adds must earn its place by changing model behavior in a contested case.
2. **35–45% of outputs were identical across conditions.** For a large fraction of cases, the skill content did not change the model's answer. v2 must be load-bearing in the cases where v1 had no effect.
3. **Over-generation is pervasive — up to 14× ground-truth length.** Both models routinely wrap the resolution in explanatory prose. v1's "do not include explanations" instruction was not strong enough; v2 needs a more emphatic and better-positioned output constraint.
4. **The two cases where the skill helped Apertus did so by making outputs shorter, not longer.** When the skill helped, it helped by *constraining*. v2 should lean on constraint, not elaboration.

These findings argue against treating v2 as "v1 plus more advice." v2 is a redesign that adds type-specific structure and tighter output discipline, sized so the model can hold it all at once.

---

## 3. Design Decisions

| # | Decision | Choice |
|---|----------|--------|
| 1 | Total length budget | **~110–140 lines** (≈ 2.5× v1) — see §3.1 |
| 2 | Examples — synthetic or real ConGra cases | **Option A: synthetic, minimal** — see §3.2 |
| 3 | Where the design rationale lives | **No rationale section in SKILL.md** — all rationale lives in this doc (see §3.3) |

The "load-bearing" criterion (every sentence must change behavior in some identifiable class of cases) governs all three.

### 3.1 Why ~110–140 lines and not more

The first instinct was 180–250 lines (4–5× v1). Three reasons argued for going tighter:

1. **The pilot itself argues against bulk.** Skill v1 hurt Qwen3-8B — non-load-bearing text is not free, it competes for the model's attention. A larger budget pre-authorizes filler.
2. **The v1 → v2 → v3 ladder is not about line count.** Per the agentskills.io spec, v3 grows by adding *external resources* (`scripts/`, `references/`) that the model loads on demand, not by inflating SKILL.md itself. v3's SKILL.md may even be shorter than v2's if it delegates to references. v2 therefore does not need to "leave room" by being mid-sized.
3. **Models imitate the prose style of their system prompt.** Over-generation was a top pilot finding (up to 14× ground-truth length). A terse, structured SKILL.md models the output behavior we want; a chatty one undermines its own output-format instruction.

Rough allocation:

| Section | Lines |
|---------|------:|
| Frontmatter + Task | ~12 |
| Identify the conflict type | ~10 |
| Resolution strategy by type (3 + combined) | ~35 |
| Worked examples (3 short) | ~40 |
| Edge cases (bullet list) | ~15 |
| Output format (re-emphasized) | ~10 |

Total: ~120 lines, leaving ~20 lines of headroom inside the 110–140 ceiling. Rationale is intentionally excluded — see §3.3.

The budget is a ceiling, not a floor. If during drafting a section cannot pass the load-bearing test, it is cut.

### 3.2 Why synthetic examples (Option A)

Three options were considered:

- **Option A — synthetic examples.** Compact, isolate one teaching point each, no methodological risk. Risk: strawman heuristics that don't survive contact with messy real conflicts.
- **Option B — real ConGra cases.** Authentic and benchmark-aligned, but **methodologically disqualifying**: embedding test-set cases in the skill that is then evaluated on the same dataset would let a reviewer credibly argue the skill scores are inflated. Real cases also exceed the line budget — median Python conflict file is ~26 KB, and truncated examples contradict the skill's own "read the surrounding code" instruction.
- **Option C — synthetic examples modeled on observed ConGra patterns.** Strongest defense (ecological validity + control), but requires a pattern-frequency EDA pass we have not done. Higher upfront cost.

**Choice: Option A for v2, with a fallback to Option C if v2 does not improve over v1.**

Reasoning:
- A is cheap and fast. If v2 with synthetic examples already shows uplift, the cost of doing C up front would have been wasted.
- If v2 does **not** improve, the right next step is to iterate v2 itself (Option C examples, possibly bumped to v2.1) — **not** to fold Option C into v3.
- v3 must isolate a different design dimension (external resources: `scripts/`, `references/` per the agentskills.io spec). Bundling Option C example-quality into v3 would confound two changes and break the v1 → v2 → v3 contrast.
- A null result for v2 (prose-only scaffolding doesn't help at 8B) is itself a defensible thesis finding that motivates v3's external-resource approach.

Note: Option-C-style pattern analysis still has a natural home in v3, but as a `references/conflict_patterns.md` that the model loads on demand — a structurally different artifact from inline SKILL.md examples.

### 3.3 Why no rationale section in SKILL.md

The first proposal was a short rationale paragraph at the bottom of SKILL.md plus a full rationale in this doc. On reflection, the inline paragraph fails the load-bearing test:

- **Not in the agentskills.io spec.** The spec defines frontmatter, operational content, and optional `scripts/` / `references/`. It does not call for or recommend a rationale section.
- **Wrong audience.** The reader of SKILL.md is the **model**, not a human reviewer. The model needs the strategy stated, not justified. Humans seeking the "why" come to this design doc.
- **Fails the load-bearing test.** Removing a rationale paragraph would not change any model output — the operational instructions govern behavior on their own. Under the criterion governing every other v2 decision, rationale in SKILL.md is filler.
- **The "reasoning is more persuasive" argument is weak here.** Adding "X because Y" can sometimes nudge compliance, but it costs tokens that should go to load-bearing instructions, and the pilot already showed the model is sensitive to extra prose.

**Decision: all rationale lives in `docs/skill_v2_design.md` (this file).** SKILL.md ends with the output-format section. The ~8 lines this frees up go back into the budget as headroom, not new content — smaller-and-tighter is fine.

### 3.4 Why "pick over invent" is the default operation

Two distinct defaults are at stake — collapsing them is the trap §3.4 has to avoid.

1. **Default *operation* (this section's claim):** when uncertain, copy one of the two existing sides verbatim rather than fabricate new code.
2. **Default *side* (deferred to §5.2):** *which* of the two sides to pick — a criterion question, not a frequency question.

Boll et al. (EASE 2024, see §7.1) report that ~80% of real-world conflict chunks are resolved by keeping one entire side (62.4% *ours* + 17.6% *theirs*); concatenation patterns account for ~5–7%, full deletion for ~2%, and custom resolution for ~12%. ~88% of resolutions are derivable from existing tokens. The empirical centre of mass is overwhelmingly *pick over invent*. Boll's distribution does **not** justify a default *side* — that ordering depends on branch semantics (ours = main, theirs = dev) which ConGra strips (see §6 working note on a/b labels).

The pick-over-invent default connects directly to §2 finding #3 (over-generation up to 14× ground-truth length). When the model wraps the resolution in explanatory prose or invents new code, it is, in effect, treating ~80% of cases as if they were custom resolutions. Pick-over-invent as the explicit default is therefore not just a frequency-driven simplification — it is a corrective for the pilot's worst failure mode.

The which-side question routes to §5.2 with surrounding-code consistency as the primary criterion: imports, symbol references, and local style should remain coherent after the chunk is replaced. Degenerate cases (one side empty, one side a strict superset) decide themselves. Beyond that, a residual class of cases is genuinely interchangeable — two valid alternative implementations where consistency does not discriminate. In real-world work, branch authority breaks the tie; in ConGra's neutral-label setting it cannot. v2 accepts this as an honest ceiling rather than papering over it with an arbitrary tiebreaker (which would either bias toward whichever side ConGra happened to label `a`, or simply be wrong half the time).

Consequences for v2:
- The pattern-identification rule (§5.1) opens with "default to pick (one side, verbatim)" and only deviates on positive evidence (independent additions → combine; matching deletions → empty; truly novel intent → custom).
- The which-side criterion lives in §5.2: surrounding-code consistency first; if undecided, commit to one side without inventing.
- The output-format section (§5.5) reinforces "do not invent code unless §5.1 routes you to *custom*".
- The worked examples (§5.3) lead with a *pick* example; *combine* and *custom* follow.

---

## 4. Proposed v2 Structure

Working outline. The framing shifted after reviewing the literature (see §7): v2 is organized around **empirical resolution patterns** (Boll et al., EASE 2024) rather than the ConGra type taxonomy. The ConGra types are kept as a secondary signal, not the primary frame.

1. **Frontmatter** — `name`, `description`, `metadata.version: "2"`
2. **Task** — minimal, ~5 lines (kept close to v1)
3. **Identify the resolution pattern** — short decision rule mapping the conflict shape to one of four patterns: pick, combine, empty, custom
4. **Resolution strategy by pattern**
   - **Pick a side** (~80% of real conflicts) — the default
   - **Combine** (~5–7%) — when both sides add independent content
   - **Empty** (~2%) — when both sides delete the same construct
   - **Custom** (~12%) — out-of-scope acknowledgment; do best-effort
   - Cross-reference to ConGra types (text/sytx/func) as a secondary signal
5. **Worked examples** — one per pattern (pick / combine / custom), kept short
6. **Edge cases** — both sides identical, one side empty, imports, broken syntax, comment-only changes
7. **Output format** — re-emphasized, with explicit length expectation

(No rationale section in SKILL.md — see §3.3.)

---

## 5. Section-by-Section Rationale

*To be filled in as decisions are made.*

### 5.1 Identify the resolution pattern

§5.2 specifies what to do once the pattern is known. This section specifies how the model identifies the pattern from the conflict region itself.

**The decision rule (in order):**

1. **Empty test.** Are both sides deletions or whitespace-only? If yes → **empty**. Otherwise continue.
2. **Combine test.** Do the two sides add *independent*, non-overlapping content — different imports, different methods on the same class, different parameters in the same signature? If yes → **combine**. Otherwise continue.
3. **Pick (default).** Apply §5.2's surrounding-code consistency criterion to choose side `a` or side `b`. → **pick**.
4. **Custom escape.** Only if step 3 cannot produce a coherent file with *either* side AND step 2's test fails AND step 1's does not apply, → **custom**. Use sparingly: over-generation in the pilot (§2 finding #3) was almost always the model misclassifying a pick-eligible conflict as custom.

**Why this ordering.**

Empty and combine are tested first because they have positive, recognisable triggers in the conflict region — both-sides-deleted is a shape, independent-additions is a shape. Pick is the default because it covers ~80% of real cases (Boll, §7.1) *and* it is the operation least likely to introduce bugs: copying existing tokens cannot fabricate behavior. Custom is the escape rather than a positive branch because the pilot showed the model is biased toward it; making it the fallback rather than a peer-tested option lowers the activation energy for the cheaper patterns.

The rule deliberately does not include a positional prior over `a`/`b`. ConGra strips the *ours/theirs* branch semantics that would justify one (§6). Once §5.1 routes to *pick*, §5.2 chooses which side based on file content, not label position.

**ConGra type as secondary signal.**

ConGra annotates each conflict as `text`, `sytx`, or `func`. v2 does not gate pattern identification on this label — it is metadata, not always available outside ConGra, and §5.1 must work without it. But when present, the type provides a weak prior that is useful for diagnosing failure modes by category:

- **text** → almost always *pick*. Two wordings of the same line; rarely combinable.
- **sytx** → *pick* or *combine*. Concatenation may or may not parse; the combine test resolves it.
- **func** → *pick* by default. *Custom* only when neither side compiles or runs correctly with the rest of the file.

The skill does not surface this mapping to the model — it would be misleading when the type is wrong, and redundant with the decision rule when it is right. The mapping is recorded here for chapter writing and for slicing the v2 evaluation by ConGra type.

### 5.2 Resolution strategy by pattern

§5.1 routes the model to one of four patterns. This section specifies the strategy each pattern triggers. The strategies are deliberately asymmetric — *pick* gets the most attention because §3.4 makes it the default operation, and *custom* gets a hard limit because it is the failure-mode-prone branch.

**Pick — primary criterion: surrounding-code consistency.**

The choice between side `a` and side `b` is anchored on whether the file remains coherent after the chunk is replaced. Three signals, in priority order:

1. **Symbol references.** If one side defines or imports a symbol that the code outside the chunk uses, picking the other side breaks the file. This decides most non-trivial pick cases.
2. **Import / dependency consistency.** If one side adds an import that its own body needs, picking the other side strands the import or strands the use.
3. **Local style.** If 1 and 2 do not discriminate, prefer the side that matches naming and indentation in the surrounding 5–10 lines.

Degenerate cases decide themselves: one side empty → take the non-empty side; one side a strict superset of the other → take the superset.

**Genuinely interchangeable cases.** When the two sides are valid alternative implementations that surrounding-code consistency cannot discriminate, commit to one side. Do *not* fabricate a third option, do *not* concatenate as a hedge. This is §3.4's honest ceiling — accept that ConGra strips the branch semantics that real developers use to break this tie.

**Combine — only when both sides add *independent* content.**

Trigger: the two sides do not modify the *same* construct; they add disjoint content (e.g., two unrelated imports, two separate parameter additions, two new methods on the same class). Operation: concatenate the two bodies in the language-appropriate order (alphabetical for imports, source order otherwise).

Anti-pattern: combining sides that modify the *same* thing differently. That is *pick*, not *combine* — concatenating two alternative implementations of the same function produces broken code.

Boll's distribution (§7.1): combine variants total ~5–7%; *ours+theirs* (1.34%) is the most common, followed by *theirs+base* (1.29%) and *ours+base+theirs* (1.22%). v2 does not surface the *base* variant in SKILL.md — the model does not see a separate base in ConGra's chunk view — but the design doc records that combine without base is the dominant form.

**Empty — both sides delete the same construct.**

Trigger: both sides remove (semantically) the same code. Operation: produce no content for the chunk. Verification: if either side adds non-trivial content, the pattern is *pick* or *combine*, not *empty*. This is the smallest budget allocation in SKILL.md — one or two lines.

**Custom — smallest derivation from existing tokens.**

Trigger: §5.1 has ruled out pick, combine, and empty. Operation: produce the smallest reconciliation of the two intents using only tokens already present in sides `a` and `b`. Do not invent new identifiers, new functions, or new abstractions.

Honest limit: ~16% of custom cases (MergeBERT user study, §7.2) require information outside the conflict region — neighbouring files, commit history, task context. For those, the in-file strategy degrades to a best-effort *pick* of whichever side is more self-contained. v2 acknowledges this ceiling explicitly rather than encouraging fabrication.

Anti-pattern: writing new functions, new abstractions, or explanatory commentary. Every pilot over-generation case (§2 finding #3) is the model treating a pick-eligible conflict as if it were custom.

### 5.3 Worked examples
*(pending)*

### 5.4 Edge cases
*(pending)*

### 5.5 Output format
*(pending)*

*(No §5.6 — rationale section deliberately omitted from SKILL.md, see §3.3.)*

---

## 6. Working Notes / Q&A

Notes on terminology and decisions that came up during design — kept so future-Barbara (and Chapter 4) can reconstruct the reasoning.

### What does "load-bearing" mean?

A load-bearing wall actually holds the building up. Remove it and the structure collapses. Applied to skill design: a sentence is load-bearing if removing it would change the model's output in some identifiable class of cases. The v1 pilot showed that non-load-bearing text is not free — it competes for the model's attention and can degrade output. Every section in v2 has to pass the test "which cases does this fix?" before it earns its place.

### Boll's *ours/theirs* vs. ConGra's *a/b*

Boll et al. (§7.1) report *ours* (62.4%) > *theirs* (17.6%) — i.e. the incumbent branch wins more often than the merged-in one. This depends on a semantic distinction: *ours* = main, *theirs* = the merged-in dev branch. ConGra's tiny dataset uses neutral labels `a` and `b` and does not preserve that asymmetry. v2 can therefore teach "pick a side" with confidence, but cannot teach "prefer side a" or rely on positional bias. The skill stays neutral on *which* side to pick and anchors the choice on consistency with surrounding code instead.

The *ours* > *theirs* ordering also holds for every language in Boll's study except C; Python and Java both follow it. This is corroborating evidence for the existence of a dominant side in real-world workflows, but is not actionable inside ConGra.

---

## 7. Literature Anchors

Two papers ground v2's central design decisions. Both are referenced from §3.4 (default heuristic) and §4 (outline).

### 7.1 Boll et al. — empirical resolution patterns

Boll, A. et al. *Characteristics, Challenges, and Resolutions of Merge Conflicts: An Empirical Study.* EASE 2024 (Distinguished Paper). n=131,154 conflicts across 10,000 GitHub projects.

Resolution patterns and frequencies:

| Pattern | Frequency | What it is |
|---------|----------:|------------|
| ours | 62.4% | Keep entire branch-A version |
| theirs | 17.6% | Keep entire branch-B version |
| empty | 2.45% | Remove chunk entirely |
| ours+theirs | 1.34% | Concatenate |
| theirs+base | 1.29% | Concatenate |
| ours+base+theirs | 1.22% | Concatenate |
| base | 0.97% | Revert to base |
| ours+base | 0.66% | Concatenate |
| Other compound | <1% | Concatenate variants |
| **Total derivable from existing tokens** | **87.9%** | |
| Custom (non-derivable) | 12.1% | Requires new code |

Headline implications used in v2:
- ~80% of chunks are resolved by picking one entire side. → §3.4 default.
- Concatenation patterns combined are ~5–7%. → "combine" branch in §5.1.
- Custom resolution is rare (~12%). → §5.5 reinforces "do not invent code unless routed to *custom*".
- The *ours* > *theirs* ordering is real but not exploitable in ConGra — see §6 working note.

### 7.2 MergeBERT user study — the limit of in-context resolution

MergeBERT (Svyatkovskiy et al.) reports a user-study finding that, of conflicts requiring custom resolution, ~16% need information that exists outside the conflict region — in other files, in commit history, or in the developer's task context. A SKILL.md operating on the file alone has a structural ceiling on this slice.

Implication for v2: the *custom* branch (§5.1) acknowledges this ceiling explicitly rather than encouraging the model to fabricate. When the resolution truly requires external context, "best-effort, signal uncertainty" is the honest behavior. This also frames a v3 hypothesis: external `references/` material may close part of this gap, but cannot close all of it.
