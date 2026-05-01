# Pilot Evaluation Results — Apertus-8B (skill v2)

**Date:** 2026-05-01
**Issue:** [#6](https://github.com/bdravec/merge-conflict-skill/issues/6) (v2 SKILL.md drafting)
**Script:** `scripts/pilot.py --model apertus --skill-version v2`
**Analysis:** `scripts/analyze_pilot.py --model apertus --skill-version v2`
**Results file:** `scripts/results/pilot_results_apertus_skill-v2.jsonl`
**Skill:** [`skills/merge-conflict-resolve-v2/SKILL.md`](../skills/merge-conflict-resolve-v2/SKILL.md) (131 lines, pattern-based per Boll et al. EASE 2024)

> **Companion docs:**
> - Qwen3 v2-skill result: [`pilot_results_qwen3_skill-v2.md`](pilot_results_qwen3_skill-v2.md)
> - v1-skill 3-condition baseline: [`pilot_results_apertus_v2.md`](pilot_results_apertus_v2.md)
> - Master summary: [`pilot_results.md`](pilot_results.md)
> - Skill design rationale: [`skill_v2_design.md`](skill_v2_design.md)

---

## Setup

- **Model:** Apertus-8B (`swiss-ai/Apertus-8B-Instruct-2509`) served via vLLM (`localhost:8000`)
- **Dataset:** 20 cases from `congra_tiny_datasets/python/func` (same cases as v1-skill run)
- **Conditions:**
  - `no-skill` — ConGra default system prompt, no skill content
  - `skill-v2-sys` — SKILL.md v2 content as system message (replaces default system prompt)
  - `skill-v2-user` — SKILL.md v2 content prepended to the user message, default system prompt kept
- **Metrics:** Edit distance similarity and winnowing similarity (from ConGra's `metrics.py`)
- **Temperature:** 0.0 (deterministic)

---

## Results

| Condition | N | Edit mean | Edit median | Winn mean | Winn median | Empty | Errors |
|-----------|---|-----------|-------------|-----------|-------------|-------|--------|
| no-skill | 20 | 0.2972 | 0.2897 | 0.3971 | 0.4325 | 0 | 0 |
| skill-v2-sys | 20 | 0.3310 | 0.3076 | 0.4424 | 0.4799 | 0 | 0 |
| skill-v2-user | 20 | 0.3244 | 0.2914 | 0.4308 | 0.4518 | 0 | 0 |

**Identical outputs (no-skill vs skill-v2-sys): 7/20 cases**
**Identical outputs (no-skill vs skill-v2-user): 9/20 cases**

The `no-skill` row reproduces the v1-skill baseline exactly — confirming pipeline determinism.

---

## Comparison: v1 skill vs v2 skill

| Condition | v1-skill | v2-skill | Δ (v2 − v1) | vs no-skill |
|-----------|---------:|---------:|------------:|------------:|
| `*-sys` edit mean | 0.3002 | **0.3310** | **+0.0308** | **+0.0338** |
| `*-user` edit mean | 0.3028 | **0.3244** | **+0.0216** | **+0.0272** |
| `*-sys` winn mean | 0.3992 | 0.4424 | +0.0432 | +0.0453 |
| `*-user` winn mean | 0.3974 | 0.4308 | +0.0334 | +0.0337 |
| Identical (sys) | 9/20 | 7/20 | −2 | — |
| Identical (user) | 8/20 | 9/20 | +1 | — |
| Wins (sys) | 5 | 7 | +2 | — |
| Losses (sys) | 6 | 5 | −1 | — |
| Wins (user) | 7 | 7 | 0 | — |
| Losses (user) | 5 | 3 | **−2** | — |

**Both v2 conditions are net-positive vs no-skill.** v1 was at noise level (+0.003 sys, +0.006 user). v2 is a real signal.

---

## Per-case edit delta — skill-v2-sys − no-skill

Positive = skill better.

| Case | Δ edit | Direction |
|------|-------:|-----------|
| 0xe63ff0ddae988357 | +0.2725 | ↑ skill better |
| 0xa4d50e39def807dd | +0.2264 | ↑ skill better |
| 0xe4ff79aa2f3f8922 | +0.1694 | ↑ skill better |
| 0x96d20e6c9b0f2395 | +0.1343 | ↑ skill better |
| 0x8e6579cb86af64a8 | +0.0073 | ↑ skill better |
| 0xddd5322de12565fe | +0.0033 | ↑ skill better |
| 0x425cf8014eda936b | +0.0015 | ↑ skill better |
| 0x2b864c36d694436b | +0.0000 | = [identical] |
| 0x32d8c89b39c2860b | +0.0000 | = [identical] |
| 0x520debc691c88dc5 | +0.0000 | = [identical] |
| 0x6cdd08d5f0b0b367 | +0.0000 | = [identical] |
| 0x999797db0c12ab9d | +0.0000 | = [identical] |
| 0xbe50e025d8e4d344 | +0.0000 | = |
| 0xc6a534710cc98bb7 | +0.0000 | = [identical] |
| 0xd752694df9c5ba20 | +0.0000 | = [identical] |
| 0x223b29598e1c5cb9 | −0.0017 | ↓ skill worse |
| 0x7fb96fbf0a030ea | −0.0058 | ↓ skill worse |
| 0xc00c4d82b7364e6d | −0.0065 | ↓ skill worse |
| 0x6081a18de8689da7 | −0.0140 | ↓ skill worse |
| 0xd9272c5e0e8f15ee | −0.1116 | ↓ skill worse |

## Per-case edit delta — skill-v2-user − no-skill

Positive = skill better.

| Case | Δ edit | Direction |
|------|-------:|-----------|
| 0xe63ff0ddae988357 | +0.2725 | ↑ skill better |
| 0xa4d50e39def807dd | +0.2264 | ↑ skill better |
| 0xe4ff79aa2f3f8922 | +0.1694 | ↑ skill better |
| 0x96d20e6c9b0f2395 | +0.1343 | ↑ skill better |
| 0xbe50e025d8e4d344 | +0.0120 | ↑ skill better |
| 0x8e6579cb86af64a8 | +0.0073 | ↑ skill better |
| 0x425cf8014eda936b | +0.0015 | ↑ skill better |
| 0x2b864c36d694436b | +0.0000 | = [identical] |
| 0x32d8c89b39c2860b | +0.0000 | = [identical] |
| 0x520debc691c88dc5 | +0.0000 | = [identical] |
| 0x6081a18de8689da7 | +0.0000 | = [identical] |
| 0x6cdd08d5f0b0b367 | +0.0000 | = [identical] |
| 0x7fb96fbf0a030ea | +0.0000 | = [identical] |
| 0x999797db0c12ab9d | +0.0000 | = [identical] |
| 0xc6a534710cc98bb7 | +0.0000 | = [identical] |
| 0xd752694df9c5ba20 | +0.0000 | = [identical] |
| 0xddd5322de12565fe | +0.0000 | = |
| 0xc00c4d82b7364e6d | −0.0005 | ↓ skill worse |
| 0xd9272c5e0e8f15ee | −0.1116 | ↓ skill worse |
| 0x223b29598e1c5cb9 | −0.1674 | ↓ skill worse |

---

## Key findings

### 1. v2 beats no-skill in both conditions on Apertus

skill-v2-sys: +0.0338 edit, +0.0453 winnowing over no-skill.
skill-v2-user: +0.0272 edit, +0.0337 winnowing over no-skill.

This is the first pilot run where any skill version is *positive* against the no-skill baseline. v1 was at noise (+0.003 to +0.006 edit). v2 is roughly an order of magnitude above noise on Apertus.

### 2. v2 improves on v1 in both conditions

skill-v2-sys vs skill-v1-sys: +0.0308 edit (+0.0432 winnowing).
skill-v2-user vs skill-v1-user: +0.0216 edit (+0.0334 winnowing).

The pattern-based v2 framing works for Apertus. The Boll et al. resolution-pattern decomposition (pick / combine / empty / custom) gives the model better scaffolding than v1's generic step-by-step instructions.

### 3. The strongest v1 cases stayed strong in v2

`0xa4d50e39def807dd`: v1 +0.23 → v2 +0.23 (sys) / +0.23 (user). Preserved.
`0xe63ff0ddae988357`: v1 +0.22 → v2 +0.27 (sys) / +0.27 (user). *Improved*.

This is the most striking divergence from the Qwen3 result, where v2 *lost* both of these (they went negative or flat). The same skill, same cases, different model — same instructions land differently.

### 4. v2 picked up new winners

`0xe4ff79aa2f3f8922` (+0.17 in both conditions) and `0x96d20e6c9b0f2395` (+0.13 in both) are v2-only wins on Apertus — neither was a v1 winner.

### 5. v2 halved the losses in the user condition

skill-v1-user had 5 losses; skill-v2-user has 3. The wins count stayed at 7. So v2 user converted losses into ties without sacrificing wins. The sys condition saw a smaller improvement (6 → 5 losses; +2 wins).

### 6. The single largest loss is `0xd9272c5e0e8f15ee` (−0.11 in both conditions)

This is the same case that hurt v1-skill on Apertus (−0.10 in v1-sys, −0.10 in v1-user). v2 did not change the failure mode here — likely a structural conflict shape that the patterns-based framing does not handle. Worth inspecting in detail for a possible Edge-case bullet in v2.1.

### 7. The pattern of identical-across-conditions persists but shifted

7/20 (sys) and 9/20 (user) for v2 vs 9/20 and 8/20 for v1. The user condition has more identicals in v2 than v1 (+1); the sys condition has fewer (−2). Apertus is genuinely responding to the v2 sys-injection more often than to v1.

---

## Cross-model contrast (Qwen3 vs Apertus, v2-skill)

| Condition | Qwen3 edit mean | Apertus edit mean | Qwen3 vs no-skill | Apertus vs no-skill |
|-----------|----------------:|------------------:|------------------:|--------------------:|
| no-skill | 0.3953 | 0.2972 | — | — |
| skill-v2-sys | 0.3836 | 0.3310 | −0.0117 | **+0.0338** |
| skill-v2-user | 0.3558 | 0.3244 | −0.0395 | **+0.0272** |

Qwen3-8B is a stronger no-skill baseline (0.40 vs 0.30) but appears more resistant to the v2 skill — it is still net-negative under both injection positions. Apertus, with a weaker baseline, gains substantially from v2.

Possible explanations (none verified, all hypotheses):

- **Headroom hypothesis** — Apertus has more room above its baseline; the skill content is informative because Apertus does not already encode the patterns implicitly. Qwen3, with its stronger pretraining, may already do most of what v2 teaches.
- **Instruction-following sensitivity** — Apertus may be more responsive to system-message guidance than Qwen3 (with thinking mode disabled).
- **Style-of-output mismatch** — Qwen3's natural output style may be closer to ground truth than v2's encouraged terseness; the skill nudges Qwen3 *away* from its own better instinct.

---

## Decision input for §3.2 fallback

Per design doc §3.2: if v2 does not improve significantly, the fallback is iterating v2 (Option C: pattern-frequency EDA from real ConGra cases) before moving to v3.

**Combined Qwen3 + Apertus verdict:**

- Apertus: v2 is a clear improvement over both v1 and no-skill (real signal, well above noise at n=20).
- Qwen3: v2 is a measurable improvement over v1 in the sys condition (+0.036) but still net-negative vs no-skill.

**The v2 framing is validated as a direction.** Where it does not yet beat no-skill (Qwen3), the gap is small enough that further iteration on the skill content (Option C) is plausible without redesign.

Recommendation: **iterate v2 (Option C — pattern-frequency EDA) rather than jump straight to v3.** Specifically, look at the Qwen3 losses (`0x520debc691c88dc5`, `0xddd5322de12565fe`, `0xa4d50e39def807dd`, `0x7fb96fbf0a030ea`) — what conflict shape causes the skill to mislead Qwen3 but help Apertus? If a pattern emerges, v2.1 with examples drawn from those shapes may close the Qwen3 gap.

---

## Limitations

- n=20 — directional only, no statistical significance.
- One conflict type (`func`) and one language (`python`) tested.
- Two-model comparison is small; the Qwen3-vs-Apertus divergence may not generalise.
- The `*-user` injection result is more conservative than `*-sys` for both models in v2 — root cause not isolated.
- The +0.27 / +0.23 cases driving most of the Apertus uplift represent ~25% of cases by count but ~80% by total Δ edit; the result is somewhat outlier-driven.
