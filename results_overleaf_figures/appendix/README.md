# Appendix material

Two independent appendix pieces. Take either or both.

## 1. The five SKILL.md files (#118 section 1)

Upload `appendix_skills.tex` **and the `skills/` folder**, then `\input{appendix_skills}`.
The `.md` files are pulled in with `\lstinputlisting` rather than pasted, so the
thesis cannot hold a copy that has drifted from the repo. Refresh them with:

```
python3 scripts/collect_skill_files.py
```

That script exists because the five files live in **two repos** — the three
merge-conflict versions here, `secure-coding-v1` and `swebench-repair-v1` in the
sibling `swe-skills-benchmarks` checkout — and because five files all named
`SKILL.md` cannot share one directory, so they are renamed on the way in.

⚠️ `\lstinputlisting` paths resolve from the **project root**, not from the folder
holding the `.tex`. `skills/` has to sit at the top level of the Overleaf project.

Label: `app:skills`. Referenced from §3.2's closing paragraph.

## 2. Worked conflict examples (#118 section 2)

Paste-ready LaTeX fragments, one per ConGra conflict cited by ID in the
skill-design sections. Upload the `.tex` files to Overleaf and `\input` them
where the appendix entry belongs.

**Simplest route: paste `appendix_cases_standalone.tex` and reference `\ref{app:cases}`.**
It is self-contained — style, heading, explanations and listings in one file.

The split version below exists only so the generated fragments can be regenerated
without touching the prose; it is the same content via `\input{appendix_cases}`.
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
