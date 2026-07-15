# Scaling-axis gap closure — cross-family summary (#99)

Aggregate-only summary of the two within-family scaling-axis gap-closure tables,
one row per family. Full per-bucket detail lives in the family docs:
[Qwen3 → 32B](qwen3_gap_closure_v2_1.md) (#97) and
[Apertus → 70B](apertus_gap_closure_v2_1.md) (#98).

`python-tiny`, metric = `max(edit, winnowing)`, solved = score > 0.8, skill =
skill-v2.1-sys. Rates are pooled across all buckets.

**Definitions** (identical to the family tables)
- **Gap** = Large − 8B solved rate (no-skill baselines).
- **Recovered** = (8B + skill) − 8B baseline.
- **Closure** = Recovered / Gap.

**Anchor note.** The large model differs by family — Qwen3 is **32B** (~4× the
8B), Apertus is **70B** (~9×). The `Gap` column is therefore *not* comparable
across rows; each row is a self-contained within-family scaling story. The row to
compare is **Closure**, which is normalised to each family's own gap.

## Table

| Family (large anchor) | 8B (%) | 8B+skill (%) | Large (%) | Gap (pp) | Recovered (pp) | Closure |
|---|---:|---:|---:|---:|---:|---:|
| Qwen3 (→ 32B) | 29.16 | 28.30 | 38.57 | 9.42 | −0.86 | −9% |
| Apertus (→ 70B) | 21.47 | 28.57 | 31.52 | 10.05 | +7.10 | +71% |

The same skill-v2.1-sys moves the two families in **opposite directions**: it
regresses Qwen3-8B (−9% closure, skill *widens* the gap) but recovers +71% of
Apertus-8B's gap to the 70B. The skill's effect tracks family / baseline strength,
not model scale.

## LaTeX source

```latex
\begin{table}[htbp]
  \centering
  \caption{Scaling-axis gap closure, aggregate per family (python-tiny,
    skill-v2.1-sys). \emph{Gap} $=$ Large$-$8B no-skill; \emph{Recovered} $=$
    8B+skill $-$ 8B; \emph{Closure} $=$ Recovered\,/\,Gap. The large anchor differs
    by family (Qwen3 32B $\sim$4$\times$, Apertus 70B $\sim$9$\times$), so \emph{Gap}
    is not comparable across rows; compare \emph{Closure}, which is normalised to
    each family's own gap.}
  \label{tab:scaling_gap_closure_summary}
  \begin{tabular}{lrrrrrr}
    \toprule
                        & \multicolumn{3}{c}{Solved rate (\%)} &          &            &          \\
    \cmidrule(lr){2-4}
    Family (anchor)     & 8B    & 8B+skill & Large & Gap (pp) & Recov.\ (pp)      & Closure          \\
    \midrule
    Qwen3 ($\to$32B)    & 29.16 & 28.30    & 38.57 & \phantom{0}9.42 & $-0.86$        & $-9\%$           \\
    Apertus ($\to$70B)  & 21.47 & 28.57    & 31.52 & 10.05           & $+7.10$        & $+71\%$          \\
    \bottomrule
  \end{tabular}
\end{table}
```
