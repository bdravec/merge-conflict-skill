# Apertus scaling-axis gap closure — skill-v2.1-sys (#98)

Does a small Apertus-8B with the skill-v2.1 SKILL.md in the system prompt close the
performance gap to the larger Apertus-70B run without a skill? Per-bucket and
aggregate, on the `python-tiny` subset. Metric = `max(edit, winnowing)`, solved =
score > 0.8. Apertus-family analogue of the Qwen3 scaling table
(`docs/RQ_123/qwen3_gap_closure_v2_1.md`, #97).

**Anchor note.** The Apertus large model is **70B** (~9× the 8B); the Qwen3 large
model is 32B (~4×). This table is a *within-family* scaling story — the `Gap`
column is not directly comparable to Qwen3's `Gap`.

**Definitions**
- **Gap** = 70B − 8B solved rate (no-skill baselines).
- **Recovered** = (8B + skill) − 8B baseline.
- **Residual** = 70B − (8B + skill), i.e. Gap − Recovered: the gap *remaining*
  after the skill, in pp. A *negative* residual means the 8B + skill *overtook* the
  70B baseline (equivalently, closure above 100%).
- **Closure** = Recovered / Gap. A *negative* closure means the 8B + skill solved
  rate fell *below* the 8B baseline. A closure *above 100%* means the 8B + skill
  solved rate *overtook* the 70B baseline.

All derived columns are computed at full precision and rounded to one decimal, so a
row entry may differ by up to 0.1 from subtracting the rounded columns.

**Data sources**
- 8B no-skill baseline: `scripts/results/pilot_results_apertus_baseline_python_tiny.jsonl` (`no-skill`)
- 8B + skill: `scripts/results/pilot_results_apertus_v2.1_python_tiny.jsonl` (`skill-v2.1-sys`)
- 70B no-skill baseline: `scripts/results/apertus-70b_baseline_python_tiny.jsonl` (`no-skill`)

Reproduce with `python scripts/build_apertus_gap_closure.py` (add `--validate` to
first re-derive the Qwen3 #97 numbers as a correctness check).

## Table

| Bucket | 8B (%) | 8B+skill (%) | 70B (%) | Gap (pp) | Recovered (pp) | Residual (pp) | Closure |
|---|---:|---:|---:|---:|---:|---:|---:|
| func | 7.1 | 11.7 | 15.6 | 8.5 | +4.7 | +3.8 | +55% |
| sytx | 4.7 | 11.7 | 17.5 | 12.8 | +7.0 | +5.8 | +54% |
| sytx+func | 11.7 | 14.8 | 14.1 | 2.3 | +3.1 | −0.8 | +133%[^overtake] |
| text | 22.9 | 27.4 | 34.0 | 11.1 | +4.5 | +6.7 | +40% |
| text+func | 19.4 | 25.6 | 27.2 | 7.9 | +6.2 | +1.7 | +79% |
| text+sytx | 17.3 | 25.9 | 34.6 | 17.3 | +8.6 | +8.6 | +50% |
| text+sytx+func | 40.8 | 53.0 | 51.5 | 10.7 | +12.2 | −1.5 | +114%[^overtake] |
| **Aggregate** | **21.47** | **28.57** | **31.52** | **10.05** | **+7.10** | **+2.95** | **+71%** |

Closure is **positive in all 7 buckets**. In aggregate the skill recovers +71% of
the 10.05 pp scale gap. In two buckets the 8B+skill *overtakes* the 70B baseline:
`sytx+func` (+133%) and `text+sytx+func` (+114%). This is the mirror image of the
Qwen3 family, where the same skill regressed the 8B (−9% aggregate closure) — the
skill's effect tracks family/baseline strength, not scale.

[^overtake]: A closure above 100% means Recovered exceeds the Gap, i.e.
    (8B+skill) − 8B is larger than 70B − 8B, so the 8B+skill solved rate
    *overtook* the 70B no-skill baseline on that bucket: `sytx+func`
    (14.8% vs 14.1%) and `text+sytx+func` (53.0% vs 51.5%). This reading holds
    because the Gap is positive in every Apertus bucket; a bucket with a negative
    Gap (8B already ahead of 70B) would flip the ratio's sign and would not carry
    this meaning.

## LaTeX source

```latex
\begin{table}[htbp]
  \centering
  \caption{Apertus scaling-axis gap closure with skill-v2.1 in the system prompt,
    python-tiny. \emph{Gap} is the 70B$-$8B no-skill difference; \emph{Recovered}
    is the 8B+skill gain over the 8B baseline; \emph{Residual} $=$ 70B$-$(8B+skill)
    $=$ Gap$-$Recovered is the gap remaining after the skill (negative $=$ 8B+skill
    overtook 70B); \emph{Closure} $=$ Recovered\,/\,Gap. A closure above $100\%$
    (equivalently, a negative residual) means the 8B+skill solved rate overtook the
    70B baseline. The Apertus large anchor is 70B ($\sim$9$\times$), so \emph{Gap}
    is not directly comparable to the Qwen3 (32B) table. Derived columns are rounded
    to one decimal, so entries may differ by up to 0.1 from subtracting the columns.}
  \label{tab:apertus_gap_closure}
  \begin{tabular}{lrrrrrrr}
    \toprule
                   & \multicolumn{3}{c}{Solved rate (\%)} &          &            &            &          \\
    \cmidrule(lr){2-4}
    Bucket         & 8B    & 8B+skill & 70B   & Gap (pp) & Recov.\ (pp) & Resid.\ (pp)   & Closure          \\
    \midrule
    func           & \phantom{0}7.1 & 11.7           & 15.6  & \phantom{0}8.5 & $+4.7$          & $+3.8$          & $+55\%$          \\
    sytx           & \phantom{0}4.7 & 11.7           & 17.5  & 12.8           & $+7.0$          & $+5.8$          & $+54\%$          \\
    sytx+func      & 11.7           & 14.8           & 14.1  & \phantom{0}2.3 & $+3.1$          & $-0.8$          & $+133\%$         \\
    text           & 22.9           & 27.4           & 34.0  & 11.1           & $+4.5$          & $+6.7$          & $+40\%$          \\
    text+func      & 19.4           & 25.6           & 27.2  & \phantom{0}7.9 & $+6.2$          & $+1.7$          & $+79\%$          \\
    text+sytx      & 17.3           & 25.9           & 34.6  & 17.3           & $+8.6$          & $+8.6$          & $+50\%$          \\
    text+sytx+func & 40.8           & 53.0           & 51.5  & 10.7           & $+12.2$         & $-1.5$          & $+114\%$         \\
    \midrule
    Aggregate      & 21.47          & 28.57          & 31.52 & 10.05          & $+7.10$         & $+2.95$         & $+71\%$          \\
    \bottomrule
  \end{tabular}
\end{table}
```
