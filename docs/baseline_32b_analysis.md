# Qwen3-32B No-Skill Baseline — python-tiny

Baseline floor for the large-pair evaluation. Generated on UBELIX, relayed to the
analysis server 2026-05-31. Source: `scripts/results/pilot_results_qwen3-32b_baseline_python_tiny_32b.jsonl`.
Tracking issue: #76. Skill conditions (v1/v2/v2.1) for the 32B model are tracked under #75 (RTX 6000).

## Method

Same tiering convention as the 8B baseline analysis (#56, Zhang et al. 2024):

- **solved**: `max(edit, winnowing) > 0.8`
- **failed**: `max(edit, winnowing) <= 0.05`
- **partial**: otherwise
- **Empty resolutions** (model returned nothing) are folded in as `failed` (score 0).
- **Transfer/serving errors** (rows with a non-null `error`) are dropped from scoring.

## File integrity

- **3,577 rows**, single `no-skill` condition, model `Qwen/Qwen3-32B`. 14 MB, valid JSONL.
- All **7 complexity buckets** present at the expected python-tiny counts.
- **20 transfer/serving errors** (0.56%), clustered in long buckets (text x12, text+sytx+func x7,
  text+func x1) — the usual max-context/connection pattern. Dropped from scoring.
- **66 empty resolutions** (1.8%) folded in as `failed`.
- Scored cases after dropping errors: **3,557**.

## Headline (3,557 scored cases)

| metric | value |
|---|---|
| edit mean | **0.521** |
| winnowing mean | **0.621** |
| solved (`max>0.8`) | **38.4%** (1,366) |
| partial | 55.1% (1,959) |
| failed (`max<=0.05`) | **6.5%** (232) |

## Per bucket

Bracketed values in `solved%` / `failed%` are the difference vs the Qwen3-8B no-skill baseline
(#56, same tiering), in percentage points (32B − 8B; positive = 32B higher).

| bucket | n | edit | winn | solved% (compared to 8B) | failed% (compared to 8B) |
|---|---|---|---|---|---|
| func | 553 | 0.441 | 0.524 | 19.7% (+7.8) | 3.4% (-0.2) |
| sytx | 446 | 0.467 | 0.586 | 26.7% (+12.4) | 3.6% (0.0) |
| sytx+func | 128 | 0.410 | 0.530 | 19.5% (+8.6) | 4.7% (-1.5) |
| text | 808 | 0.561 | 0.644 | 41.3% (+10.1) | 5.7% (+0.6) |
| text+func | 662 | 0.528 | 0.642 | 39.0% (+13.8) | 3.9% (+0.3) |
| text+sytx | 81 | 0.589 | 0.681 | 45.7% (+8.7) | 4.9% (0.0) |
| text+sytx+func | 879 | 0.567 | 0.670 | 55.1% (+5.0) | 13.1% (-0.3) |

## Comparison vs Qwen3-8B baseline

Against **Qwen3-8B no-skill** (#56: 29.2% solved / 6.5% failed), the 32B is **+9.2 pp solved at the
same 6.5% failure rate** — a clean scaling gain. The per-bucket columns above show it is **broad,
not bucket-specific**: every one of the 7 buckets improves on solved-rate. The largest gains are in
the **mid-complexity** buckets — `text+func` +13.8 pp (25.2→39.0) and `sytx` +12.4 pp (14.3→26.7),
with `text` +10.1 pp — while the **hardest bucket gains the least**: `text+sytx+func` only +5.0 pp
(50.1→55.1).

**Failure rates are essentially flat per bucket** (within ±1.5 pp, no systematic direction), so
scaling buys solved-rate, not failure reduction.[^failnoise] The bucket-ordering quirk from the 8B baseline
persists in both models: `text+sytx+func` is simultaneously the highest-solved and the
highest-failed bucket (bimodal — the polarization visible in the 8B violins), and its high failure
share (13.4% → 13.1%) is what scaling leaves untouched.

[^failnoise]: The only two positive (worse) failure deltas — `text` +0.6 pp and `text+func` +0.3 pp —
are not significant. On the paired cases (identical 808 / 662 cases per model), they amount to +5 and
+2 extra failures; a McNemar exact test gives p = 0.23 (`text`, discordance 8 vs 3) and p = 0.73
(`text+func`, 5 vs 3). Failures are largely shared across the two models (38 of 41 `text` failures and
21 of 24 `text+func` failures fail under both), and several of 32B's extra failures are empty outputs
(10 of 46 in `text`, 5 of 26 in `text+func`) rather than quality regressions.
