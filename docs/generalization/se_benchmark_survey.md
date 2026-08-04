# SE benchmark survey — beyond merge conflicts

Contributes to [#94](https://github.com/bdravec/merge-conflict-skill/issues/94) **task 1** (survey candidate SE benchmarks) and feeds **task 2** (fit assessment). See [`README.md`](README.md) for the workstream overview and the #94 task→doc map.

**Context.** The thesis so far evaluates skills on a single SE task (merge-conflict resolution) and finds *skill direction = baseline strength*: the skill helps where the base model is weak (Apertus) and regresses where it is strong (Qwen3). To test whether that claim generalises, we need a **second SE task family**; this doc surveys the candidates.

**Goal.** Not "which benchmark is best" in the abstract, but **which task family is the best second axis for the skill-vs-scale comparison** (cf. [#90](https://github.com/bdravec/merge-conflict-skill/issues/90)/[#91](https://github.com/bdravec/merge-conflict-skill/issues/91)/[#93](https://github.com/bdravec/merge-conflict-skill/issues/93)) given this project's constraints: open models served on a single GPU box via vLLM, an existing `pilot.py` harness, and a deliberately *deterministic* (non-LLM-judge) success metric.

---

## Fit criteria

Distilled from issue #94 task 2 and the SkillsBench/Harbor recipe (containerised env + deterministic verifier + oracle solution). A candidate is a good fit for **skill evaluation** if it scores well on:

1. **Deterministic verifier** — pass/fail (or graded) outcome from running tests, *not* an LLM-judge. This is what makes the skill / no-skill Δ trustworthy, the same reason our merge-conflict metric is byte/edit-based rather than judged.
2. **Oracle solution** — a reference patch/answer exists, for sanity-checking the harness and for "is the model close" analysis.
3. **Containerisation cost** — can a single instance be verified with a plain `python exec` (cheap), or does it need a per-instance Docker image with a built repo + test suite (expensive)? This dominates wall-clock and engineering cost on our single-box vLLM setup, **not** model inference.
4. **Natural SKILL.md** — is there a plausible written-guidance document a model could be given for this task? A skill only makes sense where domain conventions / a procedure can be written down (this is the whole premise of the thesis).
5. **Difficulty spread** — does it span easy→hard so the **skill-direction hypothesis** ("skill helps where the baseline is weak, regresses where strong") can actually be tested across the Apertus-weak / Qwen3-strong axis?

---

## Candidates

### A. Code generation / creation

| Benchmark | Size (#instances) | Task | Verifier | Oracle | Container cost | Natural skill? |
|---|---|---|---|---|---|---|
| **HumanEval** | 164 | complete a function from docstring | unit tests, `exec` | yes (canonical soln) | none — stdlib only | weak — task is self-contained, little "convention" to encode |
| **MBPP** (sanitized 427 / full 974) | ~1k | short Python from NL prompt | unit tests, `exec` | yes | none | weak |
| **BigCodeBench** | 1140 | complex calls across many libraries | unit tests, `exec` | yes | medium — many third-party libs preinstalled, but one shared env (not per-instance) | **moderate** — library-usage conventions are skillable |
| **LiveCodeBench** | rolling | competitive-programming, contamination-resistant | unit tests | yes | low | weak — algorithmic, not convention-driven |

### B. Bug fixing / program repair

| Benchmark | Size (#instances) | Task | Verifier | Oracle | Container cost | Natural skill? |
|---|---|---|---|---|---|---|
| **QuixBugs** | 40 (Py+Java) | fix a single-line bug | unit tests, `exec` | yes | none | moderate |
| **HumanEvalFix** (HumanEvalPack) | 164 × 6 langs | repair a buggy function | unit tests, `exec` | yes | none — stdlib only | **moderate** — "debugging procedure" is skillable, and it is the cleanest paired buggy/fixed control |
| **Defects4J** | 835 real bugs / 17 Java projects | program repair | per-project test suite | yes | **high** — per-project JVM build + test infra | moderate |
| **SWE-bench** | 2294 real GitHub issues / 12 Py repos | resolve issue via patch | repo test suite | yes (gold PR) | **very high** — per-instance Docker image, repo built at a commit | strong — but cost-dominated |
| **SWE-bench Verified** | 500 (human-validated subset) | as above | repo test suite | yes | **high** — same image machinery, fewer instances | strong |
| **SWE-bench Lite** | 300 (self-contained subset) | as above | repo test suite | yes | **high** — still per-repo Docker, but lightest realistic variant | strong |

### C. Vulnerability detection & repair

| Benchmark | Size (#instances) | Task | Verifier | Oracle | Container cost | Natural skill? |
|---|---|---|---|---|---|---|
| **CyberSecEval** (Purple Llama) | large | insecure-code-gen + detection | partly rule/static-analysis, partly LLM-judge | partial | low–medium | strong — security guidance is exactly skill-shaped |
| **SecurityEval** | 121 | generate code for CWE-prone prompts | static checks (CodeQL etc.) | partial | medium | strong |
| **CVEfixes / Big-Vul / Devign** | large | vuln *detection* (classification) | label match | labels | low | strong, but task is classification, not generation — weaker tie to our pipeline |
| **VJBench / vuln-repair sets** | small–medium | repair a known CVE | test or PoC re-run | yes | high | strong |

### D. Code review / refactoring / test generation

| Benchmark | Size (#instances) | Task | Verifier | Oracle | Container cost | Natural skill? |
|---|---|---|---|---|---|---|
| **SWT-bench** | ~ SWE-bench scale | generate a *test* that reproduces an issue | does test fail-then-pass on gold patch | yes | very high | strong |
| **CodeReviewer** (MS) | large | predict review comment / quality | **LLM-judge / BLEU** | reference comment | low | strong, but **no deterministic verifier** |
| **Refactoring sets** | varies | apply a refactoring | behaviour-preservation tests, often partial | partial | high | strong, but verifier is the weak point |
| **TestEval / CodeT** | medium | generate tests | coverage / mutation score | n/a | medium | strong |

---

## Reading against the fit criteria

- **Deterministic verifier is the hard gate.** It eliminates CodeReviewer and the judged half of CyberSecEval as *primary* axes — they would reintroduce exactly the LLM-judge noise we deliberately avoided in the merge-conflict metric. Everything in groups A/B with `exec`-based unit tests passes this gate cleanly.
- **Container cost is the second gate, and it splits the field sharply.** HumanEval(-Fix)/MBPP/QuixBugs are *zero-infra* (run a function against asserts in a sandbox). BigCodeBench needs one fat shared env. SWE-bench (any variant) and Defects4J need **per-instance built repositories** — that is a Harbor/Docker engineering project in its own right, and the cost is in the verification infra, not the model.
- **Natural-skill + difficulty-spread is what makes it a *thesis* axis, not just another benchmark.** HumanEval pure-generation is self-contained with little to encode in a skill; SWE-bench and vuln-repair are richly skillable but cost-dominated.

---

## On "SWE light?" — SWE-bench Lite / Verified

Yes — if we go the SWE-bench route, **the full 2294-instance set is the wrong target**; the realistic variants are:

- **SWE-bench Lite (300)** — curated to be self-contained / quicker to run; the standard "I want SWE-bench signal without the full cost" choice.
- **SWE-bench Verified (500)** — human-validated that the issue is actually solvable and the tests are fair; the variant most papers now report. Higher-quality labels, more instances than Lite.

**Important caveat:** "lite" only reduces the *instance count*. Every SWE-bench instance still requires its repo built at a specific commit inside a container with the right test suite — so even Lite is **high-infra** compared with HumanEvalFix. The model-inference cost is negligible next to maintaining ~300 Docker environments. This is precisely the plumbing SkillsBench's Harbor framework standardises, so if we commit to SWE-bench we should adopt Harbor rather than extend `pilot.py`.

Net: SWE-bench Lite/Verified is the right pick **if** the second axis must be "realistic repo-level work," but it is a separate infrastructure commitment, not a quick add.

---

## Recommendation (input to #94 tasks 4–5, see [`second_axis_decision.md`](second_axis_decision.md))

Two viable strategies, depending on how much infra we want to take on:

1. **Cheap, fast second axis — `HumanEvalFix` (program repair).**
   Zero per-instance container, deterministic `exec` verifier, paired buggy/fixed oracle, plausible "debugging procedure" SKILL.md, and it reuses our existing `pilot.py` shape almost directly (prompt → patch → run tests). Best for *quickly* testing whether the skill-direction hypothesis generalises beyond merge conflicts on the same 8B Apertus / Qwen3 pair. **Recommended as the immediate next axis.**

2. **Realistic, high-infra axis — `SWE-bench Verified` (or Lite) on Harbor.**
   Strongest external-validity story and aligns the harness with SkillsBench, but it is a containerisation project and should be scoped as its own milestone, not bolted onto `pilot.py`.

A defensible plan: do **(1)** now to get a second data point on the skill-direction claim, and file **(2)** as a separate scoped issue if the thesis needs repo-level realism.

Open question for tasks 4–5: the **"update or remove skill" decision rule** is orthogonal to the benchmark choice — it needs at least two model generations on the *same* task. HumanEvalFix's low cost makes it the better substrate for that cross-generation experiment too.

---

> **Verification note (web-verified 2026-06-09):** all benchmark sizes/variants below were confirmed against primary sources and are citation-ready:
> - **HumanEval** 164 problems; **MBPP** 974 full / **427** sanitized ([HF: Muennighoff/mbpp](https://huggingface.co/datasets/Muennighoff/mbpp)); **BigCodeBench** 1140 tasks, 139 libraries across 7 domains ([bigcode-project/bigcodebench](https://github.com/bigcode-project/bigcodebench)).
> - **SWE-bench** 2294 instances / 12 Python repos; **Verified** 500 (engineer-confirmed solvable); **Lite** 300 (functional bug-fixes, 11 of 12 repos) ([swebench.com FAQ](https://www.swebench.com/SWE-bench/faq/), [HF: SWE-bench_Verified](https://huggingface.co/datasets/SWE-bench/SWE-bench_Verified)).
> - **QuixBugs** 40 programs (Python + Java, single-line bug) ([QuixBugs paper](https://dl.acm.org/doi/10.1145/3135932.3135941)); **Defects4J** v2.0.0 = 835 bugs / 17 Java projects ([rjust/defects4j](https://github.com/rjust/defects4j)); **HumanEvalFix** = 164 buggy functions × 6 languages, part of HumanEvalPack ([OctoPack, arXiv:2308.07124](https://arxiv.org/abs/2308.07124)).
>
> SkillsBench/Harbor details remain per the references in #94 (not independently re-verified here).
