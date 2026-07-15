# Qwen3 scaling-axis gap closure — skill-v2.1-sys (#97)

Does a small Qwen3-8B with the skill-v2.1 SKILL.md in the system prompt close the
performance gap to the larger Qwen3-32B run without a skill? Per-bucket and
aggregate, on the `python-tiny` subset. Metric = `max(edit, winnowing)`, solved =
score > 0.8. Numbers match the figure `docs/RQ_123/rq3_scaling_gap_closure_v2.1_max.png`.

**Definitions**
- **Gap** = 32B − 8B solved rate (no-skill baselines).
- **Recovered** = (8B + skill) − 8B baseline.
- **Residual** = 32B − (8B + skill), i.e. Gap − Recovered: the gap *remaining*
  after the skill, in pp. A *negative* residual would mean the 8B + skill overtook
  the 32B baseline (it never does here).
- **Closure** = Recovered / Gap. A *negative* closure means the 8B + skill solved
  rate fell *below* the 8B baseline (the skill widened, not closed, the gap).

All derived columns are computed at full precision and rounded to one decimal, so a
row entry may differ by up to 0.1 from subtracting the rounded columns.

**Data sources**
- 8B no-skill baseline: `scripts/results/pilot_results_qwen3_baseline_python_tiny.jsonl` (`no-skill`)
- 8B + skill: `scripts/results/pilot_results_qwen3_v2.1_python_tiny.jsonl` (`skill-v2.1-sys`)
- 32B no-skill baseline: `scripts/results/pilot_results_qwen3-32b_baseline_python_tiny_rtx.jsonl` (`no-skill`)

## Table

| Bucket | 8B (%) | 8B+skill (%) | 32B (%) | Gap (pp) | Recovered (pp) | Residual (pp) | Closure |
|---|---:|---:|---:|---:|---:|---:|---:|
| func | 11.9 | 9.4 | 19.9 | 8.0 | −2.5 | +10.5 | −32% |
| sytx | 14.3 | 14.8 | 26.7 | 12.3 | +0.4 | +11.9 | +4% |
| sytx+func | 10.9 | 14.1 | 19.5 | 8.6 | +3.1 | +5.5 | +36% |
| text | 31.2 | 30.6 | 41.5 | 10.3 | −0.6 | +10.9 | −6% |
| text+func | 25.2 | 24.2 | 38.8 | 13.6 | −1.0 | +14.6 | −8% |
| text+sytx | 37.0 | 35.8 | 45.7 | 8.6 | −1.2 | +9.9 | −14% |
| text+sytx+func | 50.1 | 49.0 | 55.3 | 5.2 | −1.1 | +6.3 | −22% |
| **Aggregate** | **29.16** | **28.30** | **38.57** | **9.42** | **−0.86** | **+10.28** | **−9%** |

Closure is negative in 5 of 7 buckets; positive only in `sytx` (+4%) and
`sytx+func` (+36%). In aggregate the skill recovers none of the 9.42 pp gap.

## LaTeX source

```latex
\begin{table}[htbp]
  \centering
  \caption{Qwen3 scaling-axis gap closure with skill-v2.1 in the system prompt,
    python-tiny. \emph{Gap} is the 32B$-$8B no-skill difference; \emph{Recovered}
    is the 8B+skill gain over the 8B baseline; \emph{Residual} $=$ 32B$-$(8B+skill)
    $=$ Gap$-$Recovered is the gap remaining after the skill (negative would mean
    the 8B+skill overtook 32B; it never does here); \emph{Closure} $=$
    Recovered\,/\,Gap. A negative closure means the 8B+skill solved rate fell below
    the 8B baseline. Derived columns are rounded to one decimal, so entries may
    differ by up to 0.1 from subtracting the columns.}
  \label{tab:qwen3_gap_closure}
  \begin{tabular}{lrrrrrrr}
    \toprule
                   & \multicolumn{3}{c}{Solved rate (\%)} &          &            &            &          \\
    \cmidrule(lr){2-4}
    Bucket         & 8B    & 8B+skill & 32B   & Gap (pp) & Recov.\ (pp) & Resid.\ (pp)   & Closure          \\
    \midrule
    func           & 11.9  & \phantom{0}9.4 & 19.9  & \phantom{0}8.0 & $-2.5$          & $+10.5$         & $-32\%$          \\
    sytx           & 14.3  & 14.8           & 26.7  & 12.3           & $+0.4$          & $+11.9$         & $+4\%$           \\
    sytx+func      & 10.9  & 14.1           & 19.5  & \phantom{0}8.6 & $+3.1$          & \phantom{0}$+5.5$ & $+36\%$        \\
    text           & 31.2  & 30.6           & 41.5  & 10.3           & $-0.6$          & $+10.9$         & $-6\%$           \\
    text+func      & 25.2  & 24.2           & 38.8  & 13.6           & $-1.0$          & $+14.6$         & $-8\%$           \\
    text+sytx      & 37.0  & 35.8           & 45.7  & \phantom{0}8.6 & $-1.2$          & \phantom{0}$+9.9$ & $-14\%$        \\
    text+sytx+func & 50.1  & 49.0           & 55.3  & \phantom{0}5.2 & $-1.1$          & \phantom{0}$+6.3$ & $-22\%$        \\
    \midrule
    Aggregate      & 29.16 & 28.30          & 38.57 & \phantom{0}9.42 & $-0.86$        & $+10.28$        & $-9\%$           \\
    \bottomrule
  \end{tabular}
\end{table}
```
