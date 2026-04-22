# Pilot Evaluation Results — Qwen3-8B

**Date:** 2026-04-21
**Issue:** [#8](https://github.com/bdravec/merge-conflict-skill/issues/8)
**Script:** `scripts/pilot.py` · **Analysis:** `scripts/analyze_pilot.py`

---

## Setup

- **Model:** Qwen3-8B (`Qwen/Qwen3-8B`) served via vLLM (`localhost:8000`), thinking mode disabled
- **Dataset:** 20 cases from `congra_tiny_datasets/python/func`
- **Conditions:**
  - `no-skill` — ConGra default system prompt
  - `skill-v1` — SKILL.md v1 content as system message, same user prompt
- **Metrics:** Edit distance similarity and winnowing similarity (both from ConGra's `metrics.py`)
- **Temperature:** 0.0 (deterministic)

---

## Results

| Condition | N | Edit mean | Edit median | Edit stdev | Winn mean | Winn median | Winn stdev | Empty | Errors |
|-----------|---|-----------|-------------|------------|-----------|-------------|------------|-------|--------|
| no-skill  | 20 | 0.3953 | 0.3660 | 0.2299 | 0.4782 | 0.5091 | 0.2344 | 0 | 0 |
| skill-v1  | 20 | 0.3479 | 0.3822 | 0.1597 | 0.4296 | 0.4116 | 0.2033 | 0 | 0 |

**Identical outputs across both conditions: 7/20 cases** (6 with identical text; 1 further case with different text but Δedit=0)

**Cases above 0.80 correctness threshold: no-skill 1/20, skill-v1 0/20** — the skill removed the one case that was solved.

### Per-case edit distance delta (skill-v1 − no-skill)

Positive = skill better, negative = skill worse. Winnowing delta shown alongside for cross-metric comparison.

| Case | Δ edit | Δ winn | Direction |
|------|--------|--------|-----------|
| 0x96d20e6c9b0f2395 | +0.1794 | +0.1059 | ↑ skill better |
| 0xd752694df9c5ba20 | +0.1317 | +0.0836 | ↑ skill better |
| 0xbe50e025d8e4d344 | +0.0427 | +0.1044 | ↑ skill better |
| 0xc00c4d82b7364e6d | +0.0403 | +0.0305 | ↑ skill better |
| 0x425cf8014eda936b | +0.0000 | +0.0000 | = equal (non-identical text, same score) |
| 0x223b29598e1c5cb9 | +0.0000 | +0.0000 | = identical |
| 0xd9272c5e0e8f15ee | +0.0000 | +0.0000 | = identical |
| 0x6081a18de8689da7 | +0.0000 | +0.0000 | = identical |
| 0xc6a534710cc98bb7 | +0.0000 | +0.0000 | = identical |
| 0x32d8c89b39c2860b | +0.0000 | +0.0000 | = identical |
| 0x2b864c36d694436b | +0.0000 | +0.0000 | = identical |
| 0x999797db0c12ab9d | −0.0015 | −0.0750 | ↓ skill worse |
| 0x6cdd08d5f0b0b367 | −0.0056 | +0.0000 | ↓ skill worse (edit only) |
| 0x7fb96fbf0a030ea  | −0.0989 | −0.1544 | ↓ skill worse |
| 0xa4d50e39def807dd | −0.1185 | −0.1894 | ↓ skill worse |
| 0xe4ff79aa2f3f8922 | −0.1221 | −0.0564 | ↓ skill worse |
| 0xddd5322de12565fe | −0.1692 | −0.1687 | ↓ skill worse |
| 0x8e6579cb86af64a8 | −0.2062 | −0.1127 | ↓ skill worse |
| 0x520debc691c88dc5 | −0.2218 | −0.2784 | ↓ skill worse |
| 0xe63ff0ddae988357 | −0.3995 | −0.2620 | ↓ skill worse |

---

## Comparison with Apertus-8B

| Metric | Qwen3-8B no-skill | Qwen3-8B skill-v1 | Apertus-8B no-skill | Apertus-8B skill-v1 |
|--------|-------------------|-------------------|---------------------|---------------------|
| Edit mean | 0.3953 | 0.3479 | 0.2972 | 0.3002 |
| Edit median | 0.3660 | 0.3822 | 0.2897 | 0.2884 |
| Edit stdev | 0.2299 | 0.1597 | 0.1239 | 0.1449 |
| Winn mean | 0.4782 | 0.4296 | 0.3971 | 0.3992 |
| Above 0.80 threshold | 1/20 | 0/20 | 0/20 | 0/20 |
| Identical outputs | 7/20 | — | 9/20 | — |
| Skill better | 4 | — | 5 | — |
| Skill worse | 9 | — | 6 | — |

---

## Findings

**skill-v1 did not consistently improve performance and made things slightly worse on average.** Mean edit distance dropped from 0.3953 to 0.3479 (−0.047). However, no-skill stdev is 0.2299 — nearly as large as the mean itself — so this difference is not statistically meaningful at 20 cases.

**The skill removed the one solved case.** No-skill produced 1/20 cases above the 0.80 correctness threshold; skill-v1 produced 0/20. This is the clearest signal that skill-v1 actively interfered in at least one case.

**The "skill better" signal is concentrated in 2 cases.** Cases `0x96d20e6c9b0f2395` (+0.18) and `0xd752694df9c5ba20` (+0.13) account for most of the positive signal. The remaining 2 gains were ≤+0.04.

**7/20 identical outputs** — Qwen3-8B ignored the system prompt entirely in a significant fraction of cases. In 6 of these the resolution text was byte-for-byte identical; in 1 further case the text differed but produced the same edit score.

**`0xd752694df9c5ba20` near-empty response in no-skill.** No-skill returned only 9 characters (gt=748 chars, ratio=0.01×). This is a near-failure that inflates the no-skill mean downward, making the no-skill → skill-v1 comparison less clean than it appears. The skill-v1 condition returned 262 chars for the same case, which is still short but functional.

**Both conditions over-generate in many cases.** Similar to Apertus-8B, Qwen3-8B frequently returns responses much longer than the ground truth. The worst case (`0x425cf8014eda936b`) was ~14× the ground truth in both conditions (810–812 chars vs gt=58 chars).

**Qwen3-8B outperformed Apertus-8B overall** — edit mean 0.3953 vs 0.2972 no-skill, and Qwen3 achieved at least 1 solved case where Apertus achieved none.

---

## Response Length Analysis

| Case | GT chars | no-skill chars | skill-v1 chars | no-skill ratio | skill-v1 ratio |
|------|----------|----------------|----------------|----------------|----------------|
| 0x425cf8014eda936b | 58 | 810 | 812 | 13.97× | 14.00× |
| 0x999797db0c12ab9d | 111 | 546 | 550 | 4.92× | 4.95× |
| 0xbe50e025d8e4d344 | 70 | 296 | 334 | 4.23× | 4.77× |
| 0x2b864c36d694436b | 167 | 525 | 525 | 3.14× | 3.14× |
| 0xc00c4d82b7364e6d | 912 | 3291 | 2819 | 3.61× | 3.09× |
| 0xc6a534710cc98bb7 | 122 | 335 | 335 | 2.75× | 2.75× |

Cases where model under-generates notably: `0xd752694df9c5ba20` (0.01× no-skill — near-empty), `0x7fb96fbf0a030ea` (0.50× / 0.24×), `0x223b29598e1c5cb9` (0.32× both).

---

## Limitations

- 20 cases is too small for statistical conclusions — results are directional only
- Only one conflict type (`func`) and one language (`python`) tested
- SKILL.md v1 is minimal — v2 and v3 may perform differently
- Thinking mode was disabled for Qwen3; enabling it may change results
- No token count data recorded (not captured by current `pilot.py`)

---

## Next Steps

- Investigate why 7/20 outputs were identical — check whether prompt is reaching the model correctly
- Add an output-cleaning step to strip explanation text and extract only the code resolution before scoring
- Run the same pilot with Apertus-8B ✓ (see `pilot_results_apertus.md`)
- Evaluate on more conflict types (`text`, `sytx`)
- Scale to the full tiny dataset once pipeline is validated
