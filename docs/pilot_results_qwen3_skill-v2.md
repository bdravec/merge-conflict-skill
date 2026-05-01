# Pilot Evaluation Results — Qwen3-8B (skill v2)

**Date:** 2026-05-01
**Issue:** [#6](https://github.com/bdravec/merge-conflict-skill/issues/6) (v2 SKILL.md drafting)
**Script:** `scripts/pilot.py --model qwen3 --skill-version v2`
**Analysis:** `scripts/analyze_pilot.py --model qwen3 --skill-version v2`
**Results file:** `scripts/results/pilot_results_qwen3_skill-v2.jsonl`
**Skill:** [`skills/merge-conflict-resolve-v2/SKILL.md`](../skills/merge-conflict-resolve-v2/SKILL.md) (131 lines, pattern-based per Boll et al. EASE 2024)

> **Companion docs:**
> - v1-skill 3-condition baseline: [`pilot_results_qwen3_v2.md`](pilot_results_qwen3_v2.md)
> - Master summary: [`pilot_results.md`](pilot_results.md)
> - Skill design rationale: [`skill_v2_design.md`](skill_v2_design.md)

---

## Setup

- **Model:** Qwen3-8B (`Qwen/Qwen3-8B`) served via vLLM (`localhost:8000`), thinking mode disabled
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
| no-skill | 20 | 0.3953 | 0.3660 | 0.4782 | 0.5091 | 0 | 0 |
| skill-v2-sys | 20 | 0.3836 | 0.3777 | 0.4450 | 0.4782 | 0 | 0 |
| skill-v2-user | 20 | 0.3558 | 0.3777 | 0.4377 | 0.4626 | 0 | 0 |

**Identical outputs (no-skill vs skill-v2-sys): 9/20 cases**
**Identical outputs (no-skill vs skill-v2-user): 7/20 cases**

The `no-skill` row reproduces the v1-skill baseline exactly (same data, same temperature, same seeds) — confirming pipeline determinism.

---

## Comparison: v1 skill vs v2 skill

| Condition | v1-skill | v2-skill | Δ (v2 − v1) | vs no-skill |
|-----------|---------:|---------:|------------:|------------:|
| `*-sys` edit mean | 0.3479 | **0.3836** | **+0.0357** | −0.0117 |
| `*-user` edit mean | 0.3511 | **0.3558** | **+0.0047** | −0.0395 |
| `*-sys` winn mean | 0.4296 | 0.4450 | +0.0154 | −0.0332 |
| `*-user` winn mean | 0.4572 | 0.4377 | −0.0195 | −0.0405 |
| Identical (sys) | 6/20 | 9/20 | +3 | — |
| Identical (user) | 5/20 | 7/20 | +2 | — |
| Wins (sys) | 4 | 4 | 0 | — |
| Losses (sys) | 8 | 5 | **−3** | — |
| Wins (user) | 4 | 4 | 0 | — |
| Losses (user) | 7 | 7 | 0 | — |

---

## Per-case edit delta — skill-v2-sys − no-skill

Positive = skill better.

| Case | Δ edit | Direction |
|------|-------:|-----------|
| 0x96d20e6c9b0f2395 | +0.1836 | ↑ skill better |
| 0x999797db0c12ab9d | +0.1363 | ↑ skill better |
| 0x32d8c89b39c2860b | +0.0642 | ↑ skill better |
| 0xc00c4d82b7364e6d | +0.0403 | ↑ skill better |
| 0x6081a18de8689da7 | +0.0088 | ↑ skill better |
| 0x2b864c36d694436b | +0.0000 | = [identical] |
| 0x425cf8014eda936b | +0.0000 | = [identical] |
| 0x6cdd08d5f0b0b367 | +0.0000 | = [identical] |
| 0x8e6579cb86af64a8 | +0.0000 | = [identical] |
| 0xbe50e025d8e4d344 | +0.0000 | = [identical] |
| 0xc6a534710cc98bb7 | +0.0000 | = |
| 0xd752694df9c5ba20 | +0.0000 | = [identical] |
| 0xd9272c5e0e8f15ee | +0.0000 | = [identical] |
| 0xe4ff79aa2f3f8922 | +0.0000 | = [identical] |
| 0xe63ff0ddae988357 | +0.0000 | = [identical] |
| 0x223b29598e1c5cb9 | −0.0368 | ↓ skill worse |
| 0x7fb96fbf0a030ea | −0.0989 | ↓ skill worse |
| 0xa4d50e39def807dd | −0.1481 | ↓ skill worse |
| 0xddd5322de12565fe | −0.1626 | ↓ skill worse |
| 0x520debc691c88dc5 | −0.2218 | ↓ skill worse |

## Per-case edit delta — skill-v2-user − no-skill

Positive = skill better.

| Case | Δ edit | Direction |
|------|-------:|-----------|
| 0x96d20e6c9b0f2395 | +0.1836 | ↑ skill better |
| 0x32d8c89b39c2860b | +0.0642 | ↑ skill better |
| 0xc00c4d82b7364e6d | +0.0403 | ↑ skill better |
| 0x6081a18de8689da7 | +0.0088 | ↑ skill better |
| 0x2b864c36d694436b | +0.0000 | = [identical] |
| 0x425cf8014eda936b | +0.0000 | = [identical] |
| 0x6cdd08d5f0b0b367 | +0.0000 | = [identical] |
| 0xbe50e025d8e4d344 | +0.0000 | = [identical] |
| 0xc6a534710cc98bb7 | +0.0000 | = |
| 0xd752694df9c5ba20 | +0.0000 | = [identical] |
| 0xd9272c5e0e8f15ee | +0.0000 | = [identical] |
| 0xe4ff79aa2f3f8922 | +0.0000 | = [identical] |
| 0x999797db0c12ab9d | −0.0010 | ↓ skill worse |
| 0x223b29598e1c5cb9 | −0.0368 | ↓ skill worse |
| 0x7fb96fbf0a030ea | −0.0989 | ↓ skill worse |
| 0xa4d50e39def807dd | −0.1185 | ↓ skill worse |
| 0xddd5322de12565fe | −0.1692 | ↓ skill worse |
| 0x8e6579cb86af64a8 | −0.2062 | ↓ skill worse |
| 0x520debc691c88dc5 | −0.2218 | ↓ skill worse |
| 0xe63ff0ddae988357 | −0.2338 | ↓ skill worse |

---

## Key findings

### 1. v2-sys is a measurable improvement over v1-sys

Edit mean rises from 0.3479 → 0.3836 (+0.0357), winnowing mean from 0.4296 → 0.4450 (+0.0154). The pattern-based framing (Boll et al.: pick / combine / empty / custom) helps when the skill is in the system message. The v1-sys run was the worst-performing v1 condition; v2 closes most of the gap to no-skill.

### 2. v2-user is roughly flat to v1-user

Edit mean: 0.3511 → 0.3558 (+0.0047 — within noise at n=20). Winnowing mean actually drops slightly (−0.0195). Whatever lifted the sys condition did not transfer to user injection.

### 3. Both v2 conditions are still net-negative vs no-skill

skill-v2-sys is −0.0117 below no-skill, skill-v2-user is −0.0395 below. The skill hurts more than it helps on Qwen3-8B at 8B scale, just less than v1 did. The "harm reduction" is real but the absolute regression remains.

### 4. v2 has fewer losses than v1

skill-v1-sys had 8 cases where the skill made things worse; skill-v2-sys has 5. The user condition is unchanged (7 → 7). The sys-side improvement comes mostly from converting losses to ties, not losses to wins — wins counts stayed at 4 in both conditions.

### 5. v2 produces *more* identical-to-no-skill outputs

9/20 (sys) and 7/20 (user) for v2 vs 6/20 and 5/20 for v1. The tighter v2 framing (length cap, "no prose" stated twice, explicit no-new-identifiers) makes the model converge to the no-skill output more often. This is consistent with v2's design intent of constraining rather than elaborating, but it also means v2's content is load-bearing in fewer cases.

### 6. The case-level pattern shifted

v1 had two strong winners (`0xa4d50e39def807dd` and `0xe63ff0ddae988357`, both +0.22 edit). v2 loses both — they go negative or flat.

v2 has new winners (`0x96d20e6c9b0f2395` +0.18, `0x999797db0c12ab9d` +0.14 in sys, `0x32d8c89b39c2860b` +0.06).

The v2 wins are smaller in magnitude but more distributed. Combined with the loss-reduction in finding 4, this suggests v2 is a less brittle skill: less peak gain in any one case, more consistent near-baseline behavior.

### 7. Worst-case behavior is largely unchanged

Both v1 and v2 fail on the same hard cases — `0x520debc691c88dc5` (−0.22 in both v2 conditions, similar in v1) and `0x425cf8014eda936b` (the 14×-over-generation case from earlier pilots). These are model-capability ceiling cases, not skill-content cases.

---

## Decision input for §3.2 fallback

Per design doc §3.2: if v2 does not improve significantly, the fallback is iterating v2 (Option C: pattern-frequency EDA from real ConGra cases) before moving to v3.

The Qwen3-8B result is a **partial improvement**:
- v2-sys: real (+0.036) but small.
- v2-user: noise (+0.005).
- Both still net-negative vs no-skill.

**Verdict pending Apertus-8B run.** If Apertus shows similar sys-side improvement, the v2 framing is working but the skill content needs further iteration (Option C). If Apertus is flat or worse, the v2 sys-injection win was Qwen3-specific and the v2 redesign hasn't moved the needle in general.

---

## Limitations

- n=20 — directional only, no statistical significance.
- One conflict type (`func`) and one language (`python`) tested.
- Qwen3-8B with thinking mode disabled — enabling it may change results.
- No token-count or response-length data analyzed in this summary.
- The `*-user` injection result diverges from `*-sys` more in v2 than in v1; root cause not isolated (could be position-of-instructions effect, system-prompt anchoring, or interaction with ConGra's default user template).
