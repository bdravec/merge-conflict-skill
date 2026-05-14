# Per-case outcome distribution — v1 / v2 / v2.1 on `python/func` (n=20)

## Purpose

Slide 8 of `Thesis_Review_2026-05-08.pptx` summarises the v1, v2, and v2.1
pilots as per-condition mean edit-similarity, presented as side-by-side
text tables for Qwen3-8B and Apertus-8B. Pooled means hide the
case-level asymmetry the analyses in `docs/analysis_qwen3_v1_v2.md` (#40)
and `docs/analysis_apertus_v1_v2.md` (#41) already documented: the
median Δedit is zero, most cases are score-ties or no-ops, and the mean
is driven by a small active tail whose sign and magnitude differ
between the two models. This doc replaces the slide-8 means with the
underlying per-case Δedit distribution and threshold-based outcome
counts, so the asymmetry is visible at the granularity at which it
actually exists.

## Data

Twelve cells × 20 cases = 240 measurements. Each cell is one
(model, skill version, prompt injection) triple:

- model ∈ {Qwen3-8B, Apertus-8B}
- skill version ∈ {v1, v2, v2.1}
- prompt injection ∈ {`sys` (SKILL.md as system message), `user`
  (SKILL.md prepended to the user message)}

Cases are from the ConGra-tiny `python/func` bucket. Source pilot
JSONLs in `scripts/results/`; the file-to-cell mapping is in
`scripts/plot_per_case_outcomes.py`. The Δedit baseline for every case
is the `no-skill` condition recorded in the same JSONL (within-run
comparison; no cross-run drift):

```
Δedit = edit-similarity(skill condition) − edit-similarity(no-skill)
```

Errored cases and cases where either side scores `None` are dropped
before binning. In this corpus every cell retains all 20 cases.

## Thresholds

Each case is binned into one of five outcome categories:

| category | rule |
|---|---|
| clear better    | Δedit ≥ 0.05 |
| marginal better | 0.02 ≤ Δedit < 0.05 |
| same            | \|Δedit\| < 0.02 |
| marginal worse  | −0.05 < Δedit ≤ −0.02 |
| clear worse     | Δedit ≤ −0.05 |

The `same` band is wider than byte-identical so tiny-edit shifts (a
couple of token edits in a 50-token resolution) are not classified as a
directional effect. The 0.05 `clear` cutoff is a working threshold for
"noticeable change", not a metric-noise floor — the metric can produce
larger swings on identifier-divergence cases (see §6 /
`docs/metric_weakness_0xe4ff79aa.md`).

## Counts per cell

Each row sums to 20. Column order best → worst, matching the figure legend.

| pilot              | clear better | marginal better | same | marginal worse | clear worse |
|---|---:|---:|---:|---:|---:|
| qwen3 v1-sys       |  2 |  2 |  9 |  0 |  7 |
| qwen3 v1-user      |  3 |  1 | 10 |  1 |  5 |
| qwen3 v2-sys       |  3 |  1 | 11 |  1 |  4 |
| qwen3 v2-user      |  2 |  1 | 10 |  1 |  6 |
| qwen3 v2.1-sys     |  1 |  1 | 12 |  0 |  6 |
| qwen3 v2.1-user    |  1 |  1 | 12 |  0 |  6 |
| apertus v1-sys     |  2 |  0 | 14 |  1 |  3 |
| apertus v1-user    |  3 |  0 | 13 |  0 |  4 |
| apertus v2-sys     |  4 |  0 | 15 |  0 |  1 |
| apertus v2-user    |  4 |  0 | 14 |  0 |  2 |
| apertus v2.1-sys   |  5 |  0 | 13 |  0 |  2 |
| apertus v2.1-user  |  5 |  0 | 13 |  0 |  2 |

Bar form: `docs/figures/per_case_outcomes_v1_v2_v21.png`.

## Central tendency

Same 12 rows as §3 with sign-direction counts. `+ / 0 / −` count cases
with strictly positive / zero / strictly negative Δedit; the zero
column uses \|Δedit\| < 1e-9 (score-tied), *not* §3's "same" band
(\|Δedit\| < 0.02). Sign-test `p` is two-sided binomial with zeros
excluded.

| pilot              |  mean Δ | median Δ | + | 0 | − | sign p |
|---|---:|---:|---:|---:|---:|---:|
| qwen3 v1-sys       | −0.0475 | 0.0000 | 4 |  7 | 9 | 0.267 |
| qwen3 v1-user      | −0.0443 | 0.0000 | 4 |  7 | 9 | 0.267 |
| qwen3 v2-sys       | −0.0118 | 0.0000 | 5 | 10 | 5 | 1.000 |
| qwen3 v2-user      | −0.0395 | 0.0000 | 4 |  8 | 8 | 0.388 |
| qwen3 v2.1-sys     | −0.0370 | 0.0000 | 3 | 10 | 7 | 0.344 |
| qwen3 v2.1-user    | −0.0359 | 0.0000 | 3 | 10 | 7 | 0.344 |
| apertus v1-sys     | +0.0030 | 0.0000 | 5 |  9 | 6 | 1.000 |
| apertus v1-user    | +0.0056 | 0.0000 | 7 |  8 | 5 | 0.774 |
| apertus v2-sys     | +0.0338 | 0.0000 | 7 |  8 | 5 | 0.774 |
| apertus v2-user    | +0.0272 | 0.0000 | 7 | 10 | 3 | 0.344 |
| apertus v2.1-sys   | +0.0419 | 0.0000 | 8 |  8 | 4 | 0.388 |
| apertus v2.1-user  | +0.0376 | 0.0000 | 7 |  7 | 6 | 1.000 |

Smallest `p` is 0.267 (qwen3 v1). No cell rejects the null of
"skill has no directional effect" at α = 0.05.

## Findings

1. **Median Δedit = 0 in every cell.** §4 shows every cell with median
   0.0000 and 7–10 score-tied cases per cell. The mean is driven
   entirely by the active subset; the inactive subset is the skill
   emitting an output the model already produced unaided.

2. **No cell reaches significance at n=20.** Smallest two-sided
   sign-test p is 0.267 (qwen3 v1). Even the most-asymmetric cells —
   apertus v2-user (7/3) and v2.1-sys (8/4) — are consistent with
   chance at this sample size. The 0.05-threshold question reduces to
   "power", and at n=20 the sign test is too weak to settle it. The
   path to decidable is #46 plus matching skill runs at full
   python-tiny scale (n=3,597).

3. **Qwen3 is net-negative across all 6 cells.** Means range from
   −0.0118 (v2-sys) to −0.0475 (v1-sys). In every Qwen3 cell "clear
   worse" outnumbers "clear better" in §3. The skill is not a net win
   on Qwen3 at this scale on this bucket — consistent with
   `docs/analysis_qwen3_v1_v2.md` (#40), which attributes v2's measured
   gains on Qwen3 to over-generation suppression rather than pattern
   teaching.

4. **Apertus "clear better" grows monotonically v1 → v2 → v2.1.** Sys:
   2 → 4 → 5. User: 3 → 4 → 5. "Marginal worse" collapses to 0 from
   v2 onward; "clear worse" collapses to ≤ 2. This is the strongest
   case-level signal in the corpus that the skill is acquiring traction
   on Apertus, even though no single cell is significant.

5. **qwen3 v2-sys is "least active", not "best".** It has the smallest
   mean penalty (−0.012) but also the most ties (10/20 score-tied per
   §4) and the most symmetric split (5/+ 5/−). Reading slide 8's table
   alone, v2-sys looks like the best Qwen3 cell; in case-level view it
   is the cell where the skill most often does nothing — consistent
   with `pilot_results_qwen3_skill-v2.md` and the #40 diagnosis of v2
   on Qwen3 as harm-reduction via output discipline.

6. **v2.1 on Qwen3 widens "same" and shrinks both tails — except
   "clear worse" creeps back up.** "Same" goes 9 → 11 → 12 (sys) and
   10 → 10 → 12 (user) across v1 → v2 → v2.1. "Clear better" collapses
   to 1 in both v2.1 cells (from 2–3 under v2). "Clear worse" climbs
   4 → 6 in sys; flat at 6 in user. v2.1's stronger output-discipline
   framing pushes Qwen3 toward shorter "do nothing" outputs more
   often, suppressing the improvement tail and slightly extending the
   worsening tail — the case-level shape of the v2.1 regression
   already documented in `docs/pilot_results_v2_1.md`.

## Caveats and references

**Metric weakness.** Edit-similarity (the metric computed by
`pilot.py`) is known to mis-rank some identifier-divergence cases —
a wrong-pick output can score higher than a right-pick output when the
wrong pick is more compact (`docs/metric_weakness_0xe4ff79aa.md`).
All counts and means above are what the metric measures, not
necessarily ground-truth resolution quality. The 5-category binning
inherits this limitation: a case classified as "clear better" can
still be a quality regression on a minority of cases.

**n = 20 power.** The sign tests in §4 cannot rule out chance at this
sample size. Treat findings in §5 as tendencies on the `python/func`
bucket, not as established effects. The full python-tiny no-skill
baseline (#46) lands the Qwen3 and Apertus floors at n = 3,597 across
7 complexity buckets; matching skill runs at that scale will make the
sign tests decidable on the directional claims above (Apertus "clear
better" monotone, qwen3 v2-sys "least active", v2.1 regression on
qwen3).

**One bucket.** All 240 measurements are from the ConGra-tiny
`python/func` bucket. Findings here do not claim anything about
`sytx`, `text`, the combined buckets, or non-python languages.

### References

- `docs/analysis_qwen3_v1_v2.md` (#40), `docs/analysis_apertus_v1_v2.md`
  (#41) — per-case mechanism analyses summarised here.
- `docs/pilot_results_v2_1.md` — v2.1 phase results and mechanism
  hypothesis.
- `docs/metric_weakness_0xe4ff79aa.md` — metric ranking caveat.
- `scripts/plot_per_case_outcomes.py` — regenerator for the
  `per_case_outcomes_v1_v2_v21.png` figure and the §3 counts table.
