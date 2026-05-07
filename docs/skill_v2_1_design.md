# SKILL.md v2.1 — Design rationale

Companion to [`skills/merge-conflict-resolve-v2.1/SKILL.md`](../skills/merge-conflict-resolve-v2.1/SKILL.md). Records the design decisions, their empirical justifications, and the open caveats for the v2 → v2.1 iteration.

Closes [#42](https://github.com/bdravec/merge-conflict-skill/issues/42) (Design SKILL.md v2.1) along with the SKILL.md file.

---

## Overview

v2.1 is the Option C iteration of v2 (per [#42](https://github.com/bdravec/merge-conflict-skill/issues/42)) — pattern-frequency-EDA-driven refinement of v2's text rather than a full redesign (which would be v3, [#7](https://github.com/bdravec/merge-conflict-skill/issues/7)). The iteration is driven by the nine recommendations consolidated in [`docs/skill_v2_1_recommendations.md`](skill_v2_1_recommendations.md), themselves derived from the v1-vs-v2 analyses on Qwen3-8B ([#40](https://github.com/bdravec/merge-conflict-skill/issues/40), [`docs/analysis_qwen3_v1_v2.md`](analysis_qwen3_v1_v2.md)) and Apertus-8B ([#41](https://github.com/bdravec/merge-conflict-skill/issues/41), [`docs/analysis_apertus_v1_v2.md`](analysis_apertus_v1_v2.md)).

The headline finding from those analyses, reframed as a design constraint:

> v2 is predominantly a **harm-reduction** skill — it suppresses model over-generation. The pattern taxonomy (pick / combine / empty / custom) is largely orthogonal to v2's measured gains. v2.1 should design *for* this finding: lead with output-discipline; treat the pattern taxonomy as secondary guidance.

---

## Design principles

Three principles applied throughout the walkthrough, recorded here for chapter-6 / chapter-7 reference.

**(1) Minimal change relative to v2.** Each wording change must be justified by one of the nine v2.1 recommendations and its empirical source. Stylistic improvements without empirical backing were rejected. This keeps v2 → v2.1 evaluation comparability clean: a measured Δedit between v2 and v2.1 can be attributed to specific evidence-backed changes rather than confounded by stylistic drift.

**(2) Internal consistency.** Where v2 used multiple framings of the same concept, v2.1 unifies. Specifically: "surrounding code" replaces v2's mix of "coherent file" / "outside the conflict block" / "surrounding context". Single source of truth for repeated rules: each prohibition appears in exactly one §, with cross-references where needed (rather than duplicated text that risks drifting).

**(3) Section-by-section / paragraph-by-paragraph review.** v2.1 was assembled through a structured walkthrough rather than written and then reviewed. Every section's text was confirmed before the next one was discussed; within each section, paragraphs and lists were confirmed individually. This is the workflow recorded in `feedback_skill_review.md` (memory) and applies to load-bearing artefacts in this project.

---

## Diff summary

High-level structural changes vs v2:

| § | Section | Type | Empirical source |
|---|---|---|---|
| 1 | Frontmatter | minor | bump `name` to `merge-conflict-resolve-v2.1`, `version` to `"2.1"`; description verbatim (`pilot.py` strips frontmatter, so description doesn't affect performance) |
| 2 | Task | minor | append new bolded "Produce only the resolved code" paragraph (rec 6) |
| 3 | **Output discipline** (NEW) | new section | rec 1 (replace numeric cap with content rules), rec 6 (front-load over-generation guard), rec 9 (decouple from pattern taxonomy) |
| 4 | Identify the resolution pattern | medium | step 1 split into 1a/1b for one-side-empty (rec 2); step 4 loosened (rec 5); "coherent file" → "fits the surrounding code" |
| 5 | Resolution strategy by pattern | minor | Pick / Combine / Empty unchanged; Custom trimmed to 1 sentence (redundancy with §3 rule 3 + §4 step 4) |
| 6 | Worked examples | additive | 2 new Pick examples — Keras-vs-TF identifier divergence (rec 3), `0x520debc6`-style verbose-vs-concise (rec 4) |
| 7 | Edge cases | minor | one-side-empty bullet removed (now in §4 step 1b); broken syntax aligned with loosened custom rule; new file-level resolutions bullet (rec 8) |
| 8 | Output format | minor | numeric `\|a\|+\|b\|` cap replaced with post-hoc length check (rec 1); identifiers sentence removed (now in §3 rule 3) |

Net structural: 1 new top-level section (§3), no sections removed, 5 paragraph-level edits, 3 bullet-level edits.

---

## Section-by-section design notes

### §1 Frontmatter

Bumped `name` to `merge-conflict-resolve-v2.1` and `version` to `"2.1"`. Description kept verbatim from v2.

**Verified empirically:** `scripts/pilot.py` strips the YAML frontmatter (lines 161–166) before injecting the skill into the prompt. Description text is therefore not part of the model's context and changing it cannot affect resolution quality. Method-section caveat for the thesis: noted explicitly in chapter 6 to pre-empt reviewer concerns about description-wording confounds.

### §2 Task statement

v2's existing two sentences ("You are given a source code file..." and "Replace the conflict block...") kept verbatim. Added one new bolded paragraph appended at the end:

> **Produce only the resolved code.** No commentary, no explanations, no fabricated method bodies, no echoing of the surrounding code. The resolution should typically pick or combine the two sides; only escape to a custom resolution when neither pick nor combine fits the surrounding code.

**Empirical source:** rec 6 (reframe v2.1 as primarily an over-generation guard). The data showed v2's actual mechanism is harm-reduction; the new paragraph front-loads that framing in the model's context.

### §3 Output discipline (new section)

Three rules, positioned between §Task and §Pattern hierarchy.

**Why a new section:** rec 1, rec 6, and rec 9 jointly motivate promoting output-discipline rules to a primary position. v2 had these scattered (numeric cap in §Output format, identifier prohibition in §Custom, no-prose rule in §Output format). v2.1 consolidates them into one § that the model reads before any pattern guidance.

**Three rules**, not four (count corrected during walkthrough):
1. No comments unless verbatim from sides — rec 1, first content rule.
2. No surrounding-code echo — rec 1, second content rule, with an added explanatory sentence ("The resolution replaces the conflict block; the rest of the file is already there.") to address the misreading we observed in v2's `0xc00c4d82` over-generation case.
3. No fabricated identifiers — consolidates v2's two scattered identifier prohibitions (§Custom and §Output format) into one rule. Uses `e.g.` enumeration ("function names, variables, imports, attributes") to signal non-exhaustive — closes the expressio-unius loophole that pure abstract "identifiers" leaves open.

**"Surrounding code" left unbounded** (option c during walkthrough). Rec 5 originally proposed "(within the visible context)" as a window-bounded version; we dropped that for consistency with v2's unbounded usage. No empirical evidence of fabrication via distant identifiers in the v2 pilot.

### §4 Identify the resolution pattern

Four-step hierarchy retained. Two changes:

**Step 1 split into 1a/1b** (rec 2). Two of five v2-sys losses on Qwen3 (`0x223b29598e1c5cb9`, `0x7fb96fbf0a030ea`) misclassified one-side-empty cases as the empty pattern. The fix is structural rather than textual: present both sub-cases as distinct numbered tests rather than one rule + one footnote, so neither gets dropped on top-down reading. β formatting (sub-bullets under step 1) chosen over α (in-place reword) for this reason.

**Step 4 loosened** (rec 5). v2's "smallest reconciliation from existing tokens" wording was empirically too restrictive — `0xa4d50e39def807dd` requires GT custom resolution using tokens not present in either side. Reworded to: tokens from a/b first, surrounding code as secondary, never invent. The "smallest reconciliation" *intent* is preserved by the priority order.

**`coherent file` → `fits the surrounding code`** here and throughout the document. Terminological consistency change agreed during the walkthrough — keeping divergent framings of the same concept in different sections risks the model treating them as distinct.

### §5 Resolution strategy by pattern

Four-subsection structure retained (option A during walkthrough — minimal structural change). Pick / Combine / Empty unchanged from v2.

**§Custom trimmed** from three sentences to one. The two removed sentences ("Produce the smallest reconciliation..." and "Do not introduce new identifiers...") are now redundant: the first contradicts the loosened §4 step 4, the second is fully covered by §3 rule 3. The remaining sentence ("If even the surrounding code does not provide the tokens needed, prefer a *pick* of the more self-contained side over fabrication.") gives the unique fallback guidance not stated elsewhere.

### §6 Worked examples

Five examples, grouped Pick → Combine → Custom. Three retained from v2 verbatim; two new added between v2's first Pick example and v2's Combine example.

**Pick example ordering** is priority-order (option ii during walkthrough): symbol references (§5 criterion 1) → identifier divergence (criterion 1/3 boundary) → completeness over brevity (criterion 3 / fallback). Reading order matches §5's reasoning order.

**New example 1** — *Pick — identifier divergence* (rec 3, Keras-vs-TF). Empirically grounded in `0xe63ff0dd` Apertus pick-correction (the one clean pattern-teaching case in the 40-case corpus). Wording verbatim from rec 3.

**New example 2** — *Pick — completeness over brevity* (rec 4, `0x520debc6`-style template). Empirically grounded in 2/5 v2-sys losses on Qwen3 where the model picked the more concise side when GT kept the verbose side. Wording adapted from rec 4 to v2's example-prose style.

**Caveat on rec-3 transfer** — see [Limitations](#known-limitations) below. The ablation showed this example does not transfer to underscore-vs-no-underscore identifier divergence on Qwen3.

**No Empty example added.** Reasoning: rec 2's textual reword (§4 step 1b) is the targeted fix. Adding a worked example for Empty would introduce a second mechanism for the same fix without empirical evidence of need. Per minimal-change principle, deferred until a future iteration if needed.

### §7 Edge cases

Five bullets. Three changes:

**One-side-empty bullet removed.** Now in §4 step 1b. Single source of truth.

**Broken syntax bullet reworded.** v2 said "reconcile using only tokens from sides a and b". Rec 5's loosening of §4 step 4 makes the "only" misleading — the §4 rule now permits surrounding-code tokens as secondary. Bullet now mirrors that priority order: "Use tokens from sides a and b first; surrounding-code tokens are a secondary source."

**File-level resolutions bullet added** (rec 8). Empirically grounded in `0xd9272c5e0e8f15ee` task-ceiling case (`docs/analysis_apertus_v1_v2.md` sub-q 3). Acknowledges that some GT resolutions depend on file-level patterns invisible from the conflict region. Includes the metric-rationalised fallback ("your best bet is the closest pick — the metric will reward it more than over-confident invention") so the model has a directive even when the rule says "the skill cannot solve these".

### §8 Output format

Title kept ("Output format") rather than renamed to "Output format check" — no empirical evidence the v2 name caused issues; minimal change.

**Numeric `|a|+|b|` cap removed** (rec 1). Empirically not enforced — 11/20 v2-sys outputs over the cap on Qwen3, worst violator 21× (`0xc00c4d82`).

**Post-hoc length check added** (rec 1's third content rule). Verbatim wording: *"After producing the output, ask: is this longer than the union of side a and side b? If so, you have likely added unnecessary content."* The check is positioned at the **end of §8** (just before the closing "No prose. Code only.") rather than mid-section — semantically the post-hoc check is the last thing the model does, so its placement should reflect that. Wording is rec 1's literal text (soft consequence) rather than expanded directive — no empirical pressure to be more directive.

**Identifiers sentence removed.** v2's "Do not introduce identifiers..." line is now §3 rule 3. Single source of truth.

---

## Cross-cutting decisions

### Single source of truth

Each prohibition stated exactly once in v2.1, with cross-references where helpful:

| Concept | Where in v2.1 | Removed from |
|---|---|---|
| One-side-empty | §4 step 1b | §7 Edge cases |
| No fabricated identifiers | §3 rule 3 | §5 §Custom; §8 Output format |
| Custom-rule token sources | §4 step 4 | §5 §Custom (largely; one fallback sentence kept) |

### Terminology

| v2 phrasing | v2.1 phrasing | Where |
|---|---|---|
| "coherent file" | "fits the surrounding code" | §2, §4 step 4, §7 file-level bullet |
| "outside the conflict block" | "the surrounding code" | §3 rule 2 |
| "surrounding context" | "surrounding code" | §2 new paragraph, §3 rule 2 name |
| "surrounding 5–10 lines" | unchanged | §5 §Pick criterion 3 (intentionally bounded; preserved for specificity) |

### Three rules, not four

§3 was originally planned with four rules (per the section structure outline). During walkthrough we reconciled with rec 1's actual text — rec 1 lists *three* content rules (no comments, no echo, post-hoc length check). The fourth rule we'd informally added ("no fabricated identifiers") was actually a rec-9 promotion of v2's existing identifier prohibition, not a rec-1 rule. The section structure was corrected to: §3 has three rules (in-line discipline); §8 has the post-hoc check (verification step).

---

## Known limitations

These are the chapter-7 caveats — limitations of v2.1 known at design time, recorded here for citation.

### Rec-3 worked example does not transfer to underscore-vs-no-underscore divergence on Qwen3

**Source:** [`docs/ablation_0xe4ff79aa.md`](ablation_0xe4ff79aa.md) (rec-7 diagnostic ablation).

The proposed Pick — identifier divergence worked example uses `K.placeholder` vs `tf.placeholder` (Keras-vs-TF, namespace-prefix divergence). The target failure case `0xe4ff79aa` is `pool_size` vs `poolsize` (underscore-vs-no-underscore, internal-punctuation divergence). The 4-condition ablation showed:

- H2 (model-level capability ceiling) is ruled out — Qwen3 *can* pick correctly when given an explicit per-case answer.
- H1 (prompt-level fixable) is supported — but only at the most extreme end. The proposed worked example **does not flip Qwen3's pick** on the structurally-similar `0xe4ff79aa`. Generalising from namespace divergence to internal-punctuation divergence does not happen automatically at 8B scale.

**Implication for v2.1:** the rec-3 example is retained (option a from the ablation doc) because it is empirically helpful on `0xe63ff0dd` and might generalise to other namespace-divergence cases. It should *not* be cited as a fix for the broader category of identifier-divergence pick failures. Chapter 7 should document the non-transfer finding as a result about how worked-example transfer works at 8B scale.

### File-level resolutions remain out of scope

**Source:** rec 8; [`docs/analysis_apertus_v1_v2.md`](analysis_apertus_v1_v2.md) sub-q 3 (`0xd9272c5e0e8f15ee`).

Some GT resolutions abandon both sides and synthesise content consistent with file-level architectural patterns invisible from the ±5-line conflict region. v2.1 acknowledges this in §7 Edge cases as a task-ceiling category but cannot solve it. Chapter 7 should categorise this alongside `0xd9272c5e` as a model-capability ceiling rather than a skill failure.

### Metric weakness on identifier-divergence cases

**Source:** [`docs/metric_weakness_0xe4ff79aa.md`](metric_weakness_0xe4ff79aa.md).

ConGra's edit-similarity metric can rank a wrong-pick output higher than a right-pick output when the wrong-pick output is more compact and the right-pick output extends past the conflict region. Concretely on `0xe4ff79aa`: Qwen3 wrong = 0.785; Apertus right = 0.620. v2.1 cannot fix this — it is a metric problem, not a skill problem. Chapter 7 should cite this finding alongside `0xd9272c5e`'s leak-rewards-alignment as concrete evidence that edit-similarity is an imperfect proxy for resolution quality.

---

## Evaluation plan

Tracked in [#43](https://github.com/bdravec/merge-conflict-skill/issues/43) (Evaluate SKILL.md v2.1).

**Method:** pilot both models (Qwen3-8B, Apertus-8B) with the existing `scripts/pilot.py` infrastructure, three conditions (no-skill, v2.1-sys, v2.1-user), 20 cases on `python/func`. Compare against the existing v1 and v2 pilot results.

**Decision after evaluation:**

- **Keep v2.1** if it improves over v2 on at least one model without regressing on the other, or if regressions are explained by the known metric weakness rather than skill content.
- **Iterate to v2.2** if the data suggests targeted fixes (specific recommendations not yet implemented, or new shapes surfaced by v2.1).
- **Move to v3** if v2.1 reaches a clear plateau (per [#7](https://github.com/bdravec/merge-conflict-skill/issues/7)).

**Expected effect sizes** (from analyses): the v2 → v2.1 reframing (recs 1+6+9) should strengthen Qwen3's harm-reduction effect (move from −0.012 toward 0) without regressing Apertus's +0.034. Pattern-clarification additions (recs 2+3+4) may lift the 7.5% pattern-teaching rate, though the rec-3 ablation suggests this lift will be modest at 8B scale.

---

## Related

- **`skills/merge-conflict-resolve-v2.1/SKILL.md`** — the artefact this doc describes.
- **`docs/skill_v2_1_recommendations.md`** — the nine recommendations the design implements.
- **`docs/ablation_0xe4ff79aa.md`** — rec-7 ablation; rec-3 transfer finding.
- **`docs/metric_weakness_0xe4ff79aa.md`** — chapter-7 metric-limitation evidence.
- **`docs/analysis_apertus_v1_v2.md`**, **`docs/analysis_qwen3_v1_v2.md`** — empirical sources for all nine recommendations.
- Issues: [#42](https://github.com/bdravec/merge-conflict-skill/issues/42) (this doc closes it), [#43](https://github.com/bdravec/merge-conflict-skill/issues/43) (evaluation, blocked on this), [#44](https://github.com/bdravec/merge-conflict-skill/issues/44) (rec-7 ablation, closed).
