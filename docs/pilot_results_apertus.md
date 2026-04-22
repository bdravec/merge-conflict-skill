# Pilot Evaluation Results — Apertus-8B

**Date:** 2026-04-22
**Issue:** [#8](https://github.com/bdravec/merge-conflict-skill/issues/8)
**Script:** `scripts/pilot.py` · **Analysis:** `scripts/analyze_pilot.py`

---

## Setup

- **Model:** Apertus-8B (`swiss-ai/Apertus-8B-Instruct-2509`) served via vLLM (`localhost:8000`)
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
| no-skill  | 20 | 0.2972 | 0.2897 | 0.1239 | 0.3971 | 0.4325 | 0.2001 | 0 | 0 |
| skill-v1  | 20 | 0.3002 | 0.2884 | 0.1449 | 0.3992 | 0.4406 | 0.1852 | 0 | 0 |

**Identical outputs across both conditions: 9/20 cases**

**Cases above 0.80 correctness threshold: 0/20 in both conditions**

### Per-case edit distance delta (skill-v1 − no-skill)

Positive = skill better, negative = skill worse. Winnowing delta shown alongside for cross-metric comparison.

| Case | Δ edit | Δ winn | Direction |
|------|--------|--------|-----------|
| 0xa4d50e39def807dd | +0.2264 | +0.3564 | ↑ skill better |
| 0xe63ff0ddae988357 | +0.2192 | +0.0460 | ↑ skill better |
| 0x8e6579cb86af64a8 | +0.0073 | +0.0338 | ↑ skill better |
| 0x425cf8014eda936b | +0.0015 | +0.0009 | ↑ skill better |
| 0xc00c4d82b7364e6d | +0.0013 | −0.0018 | ↑ skill better (edit only) |
| 0x6081a18de8689da7 | +0.0000 | +0.0000 | = identical |
| 0x6cdd08d5f0b0b367 | +0.0000 | +0.0000 | = identical |
| 0xd752694df9c5ba20 | +0.0000 | +0.0000 | = identical |
| 0x96d20e6c9b0f2395 | +0.0000 | +0.0000 | = identical |
| 0x999797db0c12ab9d | +0.0000 | +0.0000 | = identical |
| 0x7fb96fbf0a030ea  | +0.0000 | +0.0000 | = identical |
| 0xc6a534710cc98bb7 | +0.0000 | +0.0000 | = identical |
| 0x32d8c89b39c2860b | +0.0000 | +0.0000 | = identical |
| 0x2b864c36d694436b | +0.0000 | +0.0000 | = identical |
| 0xbe50e025d8e4d344 | −0.0030 | −0.0011 | ↓ skill worse |
| 0xe4ff79aa2f3f8922 | −0.0182 | −0.0374 | ↓ skill worse |
| 0xddd5322de12565fe | −0.0274 | +0.0431 | ↓ skill worse (edit) / ↑ better (winn) |
| 0x520debc691c88dc5 | −0.0625 | −0.0276 | ↓ skill worse |
| 0xd9272c5e0e8f15ee | −0.1116 | −0.2427 | ↓ skill worse |
| 0x223b29598e1c5cb9 | −0.1734 | −0.1287 | ↓ skill worse |

---

## Comparison with Qwen3-8B

| Metric | Qwen3-8B no-skill | Qwen3-8B skill-v1 | Apertus-8B no-skill | Apertus-8B skill-v1 |
|--------|-------------------|-------------------|---------------------|---------------------|
| Edit mean | 0.3953 | 0.3479 | 0.2972 | 0.3002 |
| Edit median | 0.3660 | 0.3822 | 0.2897 | 0.2884 |
| Edit stdev | — | — | 0.1239 | 0.1449 |
| Winn mean | 0.4782 | 0.4296 | 0.3971 | 0.3992 |
| Above 0.80 threshold | 0/20 | 0/20 | 0/20 | 0/20 |
| Identical outputs | 7/20 | — | 9/20 | — |
| Skill better | 4 | — | 5 | — |
| Skill worse | 9 | — | 6 | — |

---

## Findings

**skill-v1 had no consistent effect on Apertus-8B.** The mean edit distance improvement is +0.003 — within the noise given a stdev of ~0.13. Specific findings:

**The "skill better" signal is driven by 2 outliers.** Cases `0xa4d50e39def807dd` (+0.23 edit) and `0xe63ff0ddae988357` (+0.22 edit) account for essentially all positive signal. The remaining 3 "skill better" cases gained ≤+0.007. Without these 2 cases, skill-v1 would perform uniformly worse.

**Neither condition solved a single case.** Using ConGra's 0.80 threshold (edit or winnowing ≥ 0.80), both conditions score 0/20. The task as set up is too hard for an 8B model on `func`-type conflicts at this context setting.

**Apertus-8B systematically over-generates.** Across nearly all cases, response length far exceeds the ground truth. Median response is ~1.8× ground truth length; worst case is 14.5× (`0x425cf8014eda936b`, gt=58 chars, ns=838 chars). The model wraps code in explanation rather than returning a clean resolution. This inflates edit distance denominator and directly lowers scores.

**9/20 identical outputs** — more system-prompt insensitivity than Qwen3-8B (7/20). In nearly half of cases, Apertus ignores the system prompt entirely. This is more pronounced here than with Qwen3.

**Apertus-8B scored lower overall than Qwen3-8B** (edit 0.30 vs 0.40 no-skill), confirming Qwen3-8B is the stronger baseline at 8B scale for this task.

**2 cases show divergent edit/winnowing signals** (`0xddd5322de12565fe`, `0xc00c4d82b7364e6d`), where one metric improved and the other worsened. This highlights that edit similarity and winnowing measure partially different properties.

---

## Response Length Analysis

Apertus-8B over-generates relative to ground truth in most cases:

| Case | GT chars | no-skill chars | skill-v1 chars | no-skill ratio | skill-v1 ratio |
|------|----------|----------------|----------------|----------------|----------------|
| 0x425cf8014eda936b | 58 | 838 | 810 | 14.45× | 13.97× |
| 0x999797db0c12ab9d | 111 | 633 | 633 | 5.70× | 5.70× |
| 0x6cdd08d5f0b0b367 | 84 | 408 | 408 | 4.86× | 4.86× |
| 0xbe50e025d8e4d344 | 70 | 298 | 280 | 4.26× | 4.00× |
| 0x2b864c36d694436b | 167 | 524 | 524 | 3.14× | 3.14× |
| 0xc00c4d82b7364e6d | 912 | 3296 | 3056 | 3.61× | 3.35× |

Cases where model under-generates (resolution shorter than GT): `0xd752694df9c5ba20` (0.35×), `0x223b29598e1c5cb9` (0.37×), `0x7fb96fbf0a030ea` (0.59×).

Over-generation is not improved by skill-v1 — the ratios are nearly identical across conditions.

---

## Limitations

- 20 cases is too small for statistical conclusions — results are directional only
- Only one conflict type (`func`) and one language (`python`) tested
- SKILL.md v1 is minimal — v2 and v3 may perform differently
- No token count data recorded (not captured by current `pilot.py`)

---

## Next Steps

- Investigate why both models produce identical outputs for 35–45% of cases — check whether system prompt is being passed correctly
- Add an output-cleaning step to strip explanation text and extract only the code resolution before scoring
- Scale to the full tiny dataset once pipeline is validated
- Evaluate SKILL.md v2 (more detailed instructions)
- Test on additional conflict types (`text`, `sytx`)
