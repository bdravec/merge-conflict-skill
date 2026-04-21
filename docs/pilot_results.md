# Pilot Evaluation Results

**Date:** 2026-04-21
**Issue:** [#8](https://github.com/bdravec/merge-conflict-skill/issues/8)
**Script:** `scripts/pilot.py` · **Analysis:** `scripts/analyze_pilot.py`

---

## Setup

- **Model:** Qwen3-8B served via vLLM (`localhost:8000`), thinking mode disabled
- **Dataset:** 20 cases from `congra_tiny_datasets/python/func`
- **Conditions:**
  - `no-skill` — ConGra default system prompt
  - `skill-v1` — SKILL.md v1 content as system message, same user prompt
- **Metrics:** Edit distance similarity and winnowing similarity (both from ConGra's `metrics.py`)
- **Temperature:** 0.0 (deterministic)

---

## Results

| Condition | N | Edit mean | Edit median | Winn mean | Winn median | Empty | Errors |
|-----------|---|-----------|-------------|-----------|-------------|-------|--------|
| no-skill  | 20 | 0.3953 | 0.3660 | 0.4782 | 0.5091 | 0 | 0 |
| skill-v1  | 20 | 0.3479 | 0.3822 | 0.4296 | 0.4116 | 0 | 0 |

**Identical outputs across both conditions: 7/20 cases** — the model produced the exact same resolution regardless of the system prompt.

### Per-case edit distance delta (skill-v1 − no-skill)

Positive = skill better, negative = skill worse.

| Case | Δ edit | Direction |
|------|--------|-----------|
| 0x96d20e6c9b0f2395 | +0.1794 | ↑ skill better |
| 0xd752694df9c5ba20 | +0.1317 | ↑ skill better |
| 0xbe50e025d8e4d344 | +0.0427 | ↑ skill better |
| 0xc00c4d82b7364e6d | +0.0403 | ↑ skill better |
| 0x223b29598e1c5cb9 | +0.0000 | = identical |
| 0x2b864c36d694436b | +0.0000 | = identical |
| 0x32d8c89b39c2860b | +0.0000 | = identical |
| 0x425cf8014eda936b | +0.0000 | = identical |
| 0x6081a18de8689da7 | +0.0000 | = identical |
| 0xc6a534710cc98bb7 | +0.0000 | = identical |
| 0xd9272c5e0e8f15ee | +0.0000 | = identical |
| 0x999797db0c12ab9d | −0.0015 | ↓ skill worse |
| 0x6cdd08d5f0b0b367 | −0.0056 | ↓ skill worse |
| 0x7fb96fbf0a030ea  | −0.0989 | ↓ skill worse |
| 0xa4d50e39def807dd | −0.1185 | ↓ skill worse |
| 0xe4ff79aa2f3f8922 | −0.1221 | ↓ skill worse |
| 0xddd5322de12565fe | −0.1692 | ↓ skill worse |
| 0x8e6579cb86af64a8 | −0.2062 | ↓ skill worse |
| 0x520debc691c88dc5 | −0.2218 | ↓ skill worse |
| 0xe63ff0ddae988357 | −0.3995 | ↓ skill worse |

---

## Findings

**skill-v1 did not consistently improve performance.** Across 20 cases:

- skill-v1 was **better in 4 cases**, **worse in 9 cases**, and **identical in 7 cases**
- Mean edit distance was slightly lower with the skill (0.3479 vs 0.3953), driven by the 7 identical cases pulling both means toward each other — not a reliable signal at this sample size

**7/20 identical outputs** is a notable finding. Qwen3-8B appears to ignore the system prompt in a significant fraction of cases, producing the same resolution regardless of whether the skill is injected. This may indicate the model's instruction-following at system-prompt level is weak, or that the conflict itself is simple enough that the system prompt makes no difference.

**The skill did not hurt either** — the 4 cases where it helped had meaningful gains (up to +0.18 edit distance), while the 9 cases where it hurt varied widely.

---

## Limitations

- 20 cases is too small for statistical conclusions — results are directional only
- Only one conflict type (`func`) and one language (`python`) tested
- Only one model (Qwen3-8B); Apertus-8B not yet evaluated
- SKILL.md v1 is minimal — v2 and v3 may perform differently
- Thinking mode was disabled for Qwen3; enabling it may change results

---

## Next Steps

- Run the same pilot with Apertus-8B
- Evaluate on more conflict types (`text`, `sytx`)
- Investigate why 7/20 outputs were identical — check whether prompt is reaching the model correctly
- Scale to the full tiny dataset once pipeline is validated
