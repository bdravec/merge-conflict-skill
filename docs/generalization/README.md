# Generalization workstream — skill evaluation beyond merge conflicts

Tracks [#94](https://github.com/bdravec/merge-conflict-skill/issues/94): extend skill evaluation **beyond merge-conflict resolution** to a broader set of SE tasks, and adopt a reusable methodology for deciding **when a SKILL.md helps vs. when a newer base model has made it redundant or harmful**.

This folder holds the survey, fit assessment, tooling evaluation, and decision docs for that issue. The existing merge-conflict pipeline (`pilot.py`, `docs/*_analysis.md`) stays where it is; this is the second-axis exploration.

## Why

Current thesis finding — **"skill direction = baseline strength"**: the Apertus skill helps where the baseline is weak, while Qwen3's strong baseline regresses with the skill (cf. the skill-vs-scale figures [#90](https://github.com/bdravec/merge-conflict-skill/issues/90)/[#91](https://github.com/bdravec/merge-conflict-skill/issues/91)/[#93](https://github.com/bdravec/merge-conflict-skill/issues/93)). That claim currently rests on **one** SE task. To generalise it we need a second task family with a clean deterministic verifier, plus a principled "update-or-retire skill" rule for cross-generation regression.

## #94 task → doc map

| # | Task | Status | Doc |
|---|---|---|---|
| 1 | Survey candidate SE benchmarks beyond merge conflicts | **done** | [`se_benchmark_survey.md`](se_benchmark_survey.md) |
| 2 | Per-benchmark fit assessment (verifier / oracle / container / paired control) | folded into survey; standalone planned | `benchmark_fit.md` *(planned)* |
| 3 | Evaluate Anthropic / SkillsBench (Harbor) skill-eval tooling for reuse | planned | `skill_eval_tooling.md` *(planned)* |
| 4 | Decide which task(s) + model(s) to add as the second axis | planned | `second_axis_decision.md` *(planned)* |
| 5 | Define the "update or remove skill" decision rule | planned | `second_axis_decision.md` *(planned)* |

## Current recommendation (subject to tasks 3–5)

- **Immediate next axis:** `HumanEvalFix` (program repair) — zero per-instance container, deterministic `exec` verifier, paired buggy/fixed oracle, reuses the `pilot.py` shape. Quickest way to get a *second* data point on the skill-direction claim.
- **Realistic but high-infra alternative:** `SWE-bench Verified` / `Lite` on the Harbor framework — strongest external validity, but a separate containerisation milestone, not a quick add. ("Lite/Verified" reduce instance count, **not** per-instance infra cost — see the survey.)

## References (from #94)

- **SkillsBench** — arXiv:2602.12670 (Feb 2026); Harbor framework (containerised env + deterministic verifier + oracle per task).
- **Anthropic skill-creator evals** (Mar 2026) — Create / Eval / Improve / Benchmark modes; blind A/B between skill versions.
- SkillLearnBench (arXiv:2604.20087); "Skills in the Wild" (arXiv:2604.04323).
