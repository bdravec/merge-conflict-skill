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

| bucket | n | edit | winn | solved% | failed% |
|---|---|---|---|---|---|
| func | 553 | 0.441 | 0.524 | 19.7% | 3.4% |
| sytx | 446 | 0.467 | 0.586 | 26.7% | 3.6% |
| sytx+func | 128 | 0.410 | 0.530 | 19.5% | 4.7% |
| text | 808 | 0.561 | 0.644 | 41.3% | 5.7% |
| text+func | 662 | 0.528 | 0.642 | 39.0% | 3.9% |
| text+sytx | 81 | 0.589 | 0.681 | 45.7% | 4.9% |
| text+sytx+func | 879 | 0.567 | 0.670 | 55.1% | 13.1% |

## Comparison vs Qwen3-8B baseline

Against **Qwen3-8B no-skill** (#56: 29.2% solved / 6.5% failed), the 32B is **+9.2 pp solved at the
same 6.5% failure rate** — a clean scaling gain, concentrated in the text-heavy buckets. The
bucket-ordering quirk from the 8B baseline persists: `text+sytx+func` is both the highest-solved and
the highest-failed bucket (bimodal — the polarization visible in the 8B violins).
