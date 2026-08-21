# Appendix material — worked conflict examples

Paste-ready LaTeX fragments, one per ConGra conflict cited by ID in the
skill-design sections. Upload the `.tex` files to Overleaf and `\input` them
where the appendix entry belongs.

**Upload all five files and add one `\input{appendix_cases}` to the thesis.**
`appendix_cases.tex` is the only hand-written file: it carries the appendix heading
and the explanation of each case, then `\input`s the three generated fragments.
The section body references the appendix once, via `\ref{app:cases}`; no case is
discussed in the prose, so these explanations are where the examples are explained.

| File | Case | Shows |
|---|---|---|
| `appendix_cases.tex` | — | the wrapper: heading, `\label{app:cases}`, and the three explanations |
| `case_0x96d20e6c9b0f2395.tex` | `0x96d20e6c9b0f2395` | a gain from constraint alone — v2 keeps the *same wrong side* as no-skill and gains 0.320 → 0.454 by emitting three lines instead of twelve |
| `case_0xe63ff0ddae988357.tex` | `0xe63ff0ddae988357` | a gain from a corrected resolution — winnowing 0.387 → 0.861 at unchanged output length |
| `case_0x8e6579cb86af64a8.tex` | `0x8e6579cb86af64a8` | the same file, opposite verdicts — v2.1 in the system prompt is +0.216 on Apertus-8B and −0.206 on Qwen3-8B |
| `case_listing_style.tex` | — | the `conflictcode` listing style; `\input` once in the preamble |

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
