# Appendix material — worked conflict examples

Paste-ready LaTeX fragments, one per ConGra conflict cited by ID in the
skill-design sections. Upload the `.tex` files to Overleaf and `\input` them
where the appendix entry belongs.

| File | Case | Cited for |
|---|---|---|
| `case_0x8e6579cb86af64a8.tex` | `0x8e6579cb86af64a8` | the same file splitting the two models — v2.1 in the system prompt is +0.216 on Apertus-8B and −0.206 on Qwen3-8B |
| `case_0xe63ff0ddae988357.tex` | `0xe63ff0ddae988357` | the pick correction — v2 raises winnowing 0.387 → 0.861 at unchanged output length |
| `case_listing_style.tex` | — | the `conflictcode` listing style; `\input` once in the preamble |

The body example for the findings section lives next door in
`../skill-design-loop/case_0x96d20e6c9b0f2395.tex`.

## Regenerating

Never edit these by hand — a hand-edited copy drifts from the repo silently.

```
python3 scripts/inspect_case.py 0x8e6579cb --latex --pilot-only \
    --show apertus:no-skill,apertus:skill-v2.1-sys,qwen3:no-skill,qwen3:skill-v2.1-sys \
    --out results_overleaf_figures/appendix
```

## Two things that will bite

**`--pilot-only` is not optional.** `scripts/results/` holds two run families that
disagree per case: the n=20 pilot (`pilot_results_<model>.jsonl`, `_skill-v2`,
`_skill-v2.1`), which is what the skill-design sections report, and the full slice
(`..._python_tiny.jsonl`, ~3,597 cases), which is what the RQ1 figures use. For
`0xe4ff79aa` on Apertus-8B with v1 in the system prompt, the pilot says 0.433 and
the full slice says 0.296. Without the flag the generator mixes them.

**The listings use `title=`, never `caption=`.** The thesis preamble renames
`\lstlistingname` to "Algorithmus", which would render on any captioned listing in
an English thesis. `title=` prints the heading without that prefix and keeps these
listings out of the list of listings, where they do not belong.
