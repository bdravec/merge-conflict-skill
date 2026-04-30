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

### 5.1 Identify the conflict type
*(pending)*

### 5.2 Resolution strategy by type
*(pending)*

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
