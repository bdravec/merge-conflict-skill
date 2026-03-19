# Thesis Proposal

**Working Title:**
Agent Skills for Merge Conflict Resolution: Designing and Evaluating SKILL.md-based Knowledge for Small and Large Language Models

**Department:** Software Engineering
**Supervisor:** Prof. Dr. Timo Kehrer, University of Bern — Software Engineering Group (SEG)
**Advisor:** Roman Makacek
**Candidate:** Barbara Dravec
**Date:** March 2026

---

## 1. Motivation

AI agents are increasingly used for software engineering tasks, but often lack the domain-specific procedural knowledge needed to perform reliably. The agentskills.io standard (originally developed by Anthropic, now an open standard adopted by 30+ agent tools including Claude Code, GitHub Copilot, Cursor, and OpenHands) introduces a lightweight mechanism — SKILL.md files — for injecting reusable, portable knowledge into agents at runtime.

Despite rapid ecosystem adoption, no skills exist for software engineering tasks, and no empirical evaluation of skill effectiveness has been published. This thesis addresses both gaps.

The core insight motivating this work: **agents are the delivery vehicle; skills are the knowledge.** Any agent that loads a SKILL.md skill benefits directly from the quality of that skill's content. By validating skill effectiveness at the LLM level — through controlled experiments with and without skill injection — this thesis provides a foundational answer: does the skill content actually help? If yes, every agent in the agentskills.io ecosystem that uses this skill inherits that benefit automatically.

---

## 2. Research Questions

**RQ1:** Does a domain-specific SKILL.md improve agent performance on merge conflict resolution compared to no skill?

**RQ2:** Does the effect vary by conflict complexity (text → syntax → functional)?

**RQ3:** Does a skill applied to a small model close the performance gap to a large model without one?

---

## 3. Contributions

1. **A merge-conflict-resolve skill** — a versioned SKILL.md skill (v1: minimal, v2: detailed, v3: with reference material and scripts) for the agentskills.io standard, published openly on GitHub
2. **An evaluation framework** — a reproducible pipeline for measuring skill effectiveness on the ConGra benchmark using open-source models
3. **Empirical results** — quantitative evidence of skill effectiveness across conflict complexity levels, model sizes, and model families (Qwen3 and Apertus)

---

## 4. Background

- **Agent skills and agentskills.io:** what skills are, how agents discover and activate them (progressive disclosure), the SKILL.md format
- **Merge conflicts:** what they are, why automated resolution is hard, existing approaches
- **LLMs for SE tasks:** brief overview, relevant prior results
- **Hermes Agent:** the target agent runtime; how it uses SKILL.md files in practice

---

## 5. Related Work

- **ConGra** (NeurIPS 2024 D&B): the primary benchmark used; prior LLM results on merge conflict resolution
- **Automated merge conflict resolution:** MergeBERT, prior neural and rule-based approaches
- **Prompt engineering and context injection:** how structured instructions affect LLM output on code tasks
- **Skills vs fine-tuning:** in-context knowledge injection as an alternative to model adaptation

---

## 6. Skill Design

The design contribution of the thesis — not simply writing a SKILL.md, but doing so systematically and documenting design decisions.

| Version | Contents | Hypothesis |
|---|---|---|
| v1 | Minimal: step-by-step resolution instructions | Establishes whether any skill helps |
| v2 | Detailed: per-complexity-type strategies, examples, edge cases | Tests whether skill quality matters |
| v3 | Full: v2 + bundled reference docs and scripts | Tests whether supporting artifacts help |

Design rationale for each decision will be documented as part of the thesis contribution.

---

## 7. Evaluation Setup

### Design choice: direct LLM calls vs. full agent loop

The evaluation uses direct LLM calls with skill content injected into the system prompt, rather than running a full agent loop (e.g., Hermes Agent). This isolates the effect of the skill content from agent orchestration overhead, making results cleaner and more reproducible. Evaluating skills in an end-to-end agent loop is left as future work (see §10).

### Dataset
ConGra (tiny subset) — one conflict per file, Python and Java languages, stratified by conflict type:
- Text conflicts
- Syntax conflicts
- Functional conflicts
- Combined types

### Models

|  | Runs on | No skill | Skill v1 | Skill v2 | Skill v3 |
|---|---|---|---|---|---|
| **Qwen3-8B** | Local GPU (24GB) | ✓ | ✓ | ✓ | ✓ |
| **Apertus-8B** | Local GPU (24GB) | ✓ | ✓ | ✓ | ✓ |
| **Qwen3-32B** | Cluster (96GB) | ✓ | — | ✓ | — |
| **Apertus-70B** | Cluster (96GB) | ✓ | — | ✓ | — |

Small models (8B) run on a local 24GB GPU. Large models (32B/70B) run on a university datacenter cluster (SLURM, 96GB GPU). Models are served via vLLM, which exposes an OpenAI-compatible endpoint.

### Metrics
- **Edit similarity** — normalized character-level edit distance vs ground truth
- **Semantic similarity** — cosine similarity using code embeddings vs ground truth
- **Winnowing similarity** — fingerprinting-based code similarity vs ground truth

All three metrics are taken directly from ConGra's evaluation pipeline. A resolution is considered correct when at least one metric exceeds 80% (ConGra's threshold).

### Statistical analysis
Significance testing across skill vs no-skill conditions per model and per conflict type.

---

## 8. Expected Results Structure

- **RQ1:** Overall effect of skill (does any version of the skill improve resolution rates?)
- **RQ2:** Effect broken down by conflict type (hypothesis: functional conflicts benefit most from structured skill knowledge)
- **RQ3:** Qwen3-8B + best skill vs Qwen3-32B without skill (hypothesis: skill partially or fully closes the gap)
- **Secondary:** Does Apertus respond to skill injection differently than Qwen3?

---

## 9. Discussion

- What makes a skill effective? Lessons from v1 → v2 → v3 comparison
- Implications for the agentskills.io ecosystem and skill authors
- Threats to validity: ConGra ground truth quality, metric sensitivity, prompt sensitivity
- Limitations: single task domain, two languages, one benchmark

---

## 10. Conclusion and Future Work

Summary of findings and open questions. Suggested future directions:
- Extending the skill library to code review and commit message generation
- Evaluating skills in an end-to-end agent loop (Hermes Agent) rather than isolated LLM calls
- Community contribution of the skill to the agentskills.io reference library

---

## 11. Proposed Timeline

| Month | Milestone |
|---|---|
| 1 | Literature review; set up ConGra pipeline, vLLM, and models locally and on cluster |
| 2 | Skill design (v1 → v3); pilot runs to validate pipeline |
| 3 | Full evaluation runs on cluster |
| 4 | Data analysis; write chapters 1–3 (Introduction, Background, Related Work) |
| 5 | Write chapters 4–7 (Design, Evaluation, Results, Discussion) |
| 6 | Revisions, final review, defense preparation |

---

## 12. Infrastructure

| Resource | Purpose |
|---|---|
| Local GPU (24GB VRAM) | Qwen3-8B, Apertus-8B evaluation |
| University cluster (SLURM, 96GB GPU) | Qwen3-32B, Apertus-70B evaluation |
| GitHub (public repo) | Code, skill files, evaluation scripts |
| vLLM | OpenAI-compatible model serving |
| ConGra | Benchmark dataset and evaluation pipeline |

---

## 13. References (preliminary)

- Zhang et al. (2024). *ConGra: Benchmarking Automatic Conflict Resolution.* NeurIPS 2024 Datasets & Benchmarks.
- Swiss AI (2025). *Apertus: A Fully Open, Transparent, Multilingual Language Model.* ETH Zurich / EPFL / CSCS.
- agentskills.io specification — https://agentskills.io/specification
- Hermes Agent — https://hermes-agent.org
- ConGra GitHub — https://github.com/HKU-System-Security-Lab/ConGra
- Anthropic skills examples — https://github.com/anthropics/skills
