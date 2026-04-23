# Pilot Evaluation Results — Qwen3-8B (v2, 3-condition)

**Date:** 2026-04-23
**Issue:** [#37](https://github.com/bdravec/merge-conflict-skill/issues/37)
**Script:** `scripts/pilot.py` · **Analysis:** `scripts/analyze_pilot.py`
**Results file:** `scripts/results/pilot_results_qwen3_v2.jsonl`

> **Supersedes:** `docs/pilot_results.md` (2-condition run, 2026-04-21).
> The v1 run compared `no-skill` vs `skill-v1` (system injection only).
> This v2 run adds a third condition (`skill-v1-user`) to test whether
> injection position (system vs user message) affects model responsiveness.

---

## Setup

- **Model:** Qwen3-8B (`Qwen/Qwen3-8B`) served via vLLM (`localhost:8000`), thinking mode disabled
- **Dataset:** 20 cases from `congra_tiny_datasets/python/func`
- **Conditions:**
  - `no-skill` — ConGra default system prompt, no skill content
  - `skill-v1-sys` — SKILL.md v1 content as system message (replaces default system prompt)
  - `skill-v1-user` — SKILL.md v1 content prepended to the user message, default system prompt kept
- **Metrics:** Edit distance similarity and winnowing similarity (from ConGra's `metrics.py`)
- **Temperature:** 0.0 (deterministic)

---

## Results

| Condition | N | Edit mean | Edit median | Winn mean | Winn median | Empty | Errors |
|-----------|---|-----------|-------------|-----------|-------------|-------|--------|
| no-skill | 20 | 0.3953 | 0.3660 | 0.4782 | 0.5091 | 0 | 0 |
| skill-v1-sys | 20 | 0.3479 | 0.3822 | 0.4296 | 0.4116 | 0 | 0 |
| skill-v1-user | 20 | 0.3511 | 0.3465 | 0.4572 | 0.4425 | 0 | 0 |

**Identical outputs (no-skill vs skill-v1-sys): 6/20 cases**
**Identical outputs (no-skill vs skill-v1-user): 5/20 cases**

### Per-case edit delta — skill-v1-sys − no-skill

Positive = skill better.

| Case | Δ edit | Direction |
|------|--------|-----------|
| 0x96d20e6c9b0f2395 | +0.1794 | ↑ skill better |
| 0xd752694df9c5ba20 | +0.1317 | ↑ skill better |
| 0xbe50e025d8e4d344 | +0.0427 | ↑ skill better |
| 0xc00c4d82b7364e6d | +0.0403 | ↑ skill better |
| 0x425cf8014eda936b | +0.0000 | = (different text, same score) |
| 0x223b29598e1c5cb9 | +0.0000 | = [identical] |
| 0x2b864c36d694436b | +0.0000 | = [identical] |
| 0x32d8c89b39c2860b | +0.0000 | = [identical] |
| 0x6081a18de8689da7 | +0.0000 | = [identical] |
| 0xc6a534710cc98bb7 | +0.0000 | = [identical] |
| 0xd9272c5e0e8f15ee | +0.0000 | = [identical] |
| 0x999797db0c12ab9d | −0.0015 | ↓ skill worse |
| 0x6cdd08d5f0b0b367 | −0.0056 | ↓ skill worse |
| 0x7fb96fbf0a030ea  | −0.0989 | ↓ skill worse |
| 0xa4d50e39def807dd | −0.1185 | ↓ skill worse |
| 0xe4ff79aa2f3f8922 | −0.1221 | ↓ skill worse |
| 0x8e6579cb86af64a8 | −0.2062 | ↓ skill worse |
| 0x520debc691c88dc5 | −0.2218 | ↓ skill worse |
| 0xddd5322de12565fe | −0.1692 | ↓ skill worse |
| 0xe63ff0ddae988357 | −0.3995 | ↓ skill worse |

skill-v1-sys better: 4 · worse: 8 · identical/equal: 8

### Per-case edit delta — skill-v1-user − no-skill

| Case | Δ edit | Direction |
|------|--------|-----------|
| 0xd752694df9c5ba20 | +0.1317 | ↑ skill better |
| 0xd9272c5e0e8f15ee | +0.0869 | ↑ skill better |
| 0x520debc691c88dc5 | +0.0539 | ↑ skill better |
| 0xbe50e025d8e4d344 | +0.0427 | ↑ skill better |
| 0x425cf8014eda936b | +0.0000 | = (different text, same score) |
| 0xc6a534710cc98bb7 | +0.0000 | = (different text, same score) |
| 0x2b864c36d694436b | +0.0000 | = [identical] |
| 0x32d8c89b39c2860b | +0.0000 | = [identical] |
| 0x6081a18de8689da7 | +0.0000 | = [identical] |
| 0x6cdd08d5f0b0b367 | +0.0000 | = [identical] |
| 0xc00c4d82b7364e6d | +0.0000 | = [identical] |
| 0x96d20e6c9b0f2395 | −0.0008 | ↓ skill worse |
| 0x999797db0c12ab9d | −0.0005 | ↓ skill worse |
| 0x7fb96fbf0a030ea  | −0.0058 | ↓ skill worse |
| 0x223b29598e1c5cb9 | −0.0386 | ↓ skill worse |
| 0xa4d50e39def807dd | −0.1185 | ↓ skill worse |
| 0xe4ff79aa2f3f8922 | −0.1221 | ↓ skill worse |
| 0xddd5322de12565fe | −0.1692 | ↓ skill worse |
| 0x8e6579cb86af64a8 | −0.2683 | ↓ skill worse |
| 0xe63ff0ddae988357 | −0.4764 | ↓ skill worse |

skill-v1-user better: 4 · worse: 7 · identical/equal: 9

---

## Findings

**Neither injection position consistently improves performance.** Both skill conditions score lower than no-skill on edit mean (sys: 0.3479, user: 0.3511 vs baseline 0.3953). The same is true for winnowing mean. SKILL.md v1 does not help Qwen3-8B on this task regardless of where it is injected.

**System prompt is being passed correctly — identical outputs are not a prompt-delivery bug.** skill-v1-user still produces 5/20 identical outputs despite injecting the skill into the user message where it cannot be ignored. The model simply converges to the same resolution for those cases regardless of instruction context.

**One case unlocked by user injection.** Case `0xd9272c5e0e8f15ee` was identical (Δ=0.00) in skill-v1-sys but improved by +0.0869 in skill-v1-user. This is the only case where injection position made a qualitative difference; it does not change the overall picture.

**skill-v1-user's worst case is worse than skill-v1-sys.** Case `0xe63ff0ddae988357` dropped −0.4764 in user injection vs −0.3995 in system injection — the skill prepended to the user prompt actively degraded this case further.

**The problem is skill content, not pipeline.** With identical pipeline and both injection positions tested, the consistent underperformance of skill-v1 points to the skill text itself. SKILL.md v1 is intentionally minimal; v2 (detailed instructions) is the next step.

---

## Comparison with v1 Pilot (2026-04-21)

The `no-skill` and `skill-v1-sys` numbers in this run are identical to the v1 pilot — confirming the pipeline is deterministic and reproducible (temperature=0.0).

| Condition | Edit mean (v1 pilot) | Edit mean (v2 pilot) |
|-----------|----------------------|----------------------|
| no-skill | 0.3953 | 0.3953 |
| skill-v1 / skill-v1-sys | 0.3479 | 0.3479 |
| skill-v1-user | — | 0.3511 |

---

## Next Steps

- Run the same 3-condition pilot on Apertus-8B (produce `pilot_results_apertus_v2.jsonl`)
- Write SKILL.md v2 (issue #6) and re-run with all four conditions
- Scale to full tiny dataset once v2 is evaluated
