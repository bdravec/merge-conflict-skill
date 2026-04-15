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

**Broader relevance.** The question of whether structured, human-authored knowledge can meaningfully improve LLM performance is not only a technical one — it carries practical implications for how organizations will interact with AI systems at scale. Gartner predicts that by 2028, 33% of enterprise software applications will include agentic AI, up from less than 1% in 2024, and that at least 15% of day-to-day work decisions will be made autonomously through such systems (Gartner, 2025a). Gartner further predicts that by 2029, at least 50% of knowledge workers will develop new skills to work with, govern, or create AI agents on demand (Gartner, 2025b). In this emerging landscape, the bottleneck is not model capability alone, but the ability to supply agents with the right domain knowledge at the right time.

Skills address this bottleneck by decoupling *what an agent knows* from *how an agent works*. A domain expert who understands a business process — but not the internals of language models — can author a skill that encodes that process; the agent then executes it. This mirrors the broader "citizen developer" trend, where non-technical users increasingly build and maintain applications using low-code tools. Skills extend this logic to AI agents: they are, in effect, a natural-language interface for shaping LLM behavior through procedural descriptions rather than fine-tuning or code.

The scientific basis for this approach draws on research in in-context knowledge injection. A recent survey identifies several injection methods, including retrieval-augmented generation (RAG), instruction tuning, and knowledge prompting — the approach of transforming external knowledge into textual prompts without retraining the model (Li et al., 2025). Ovadia et al. (2024) compared fine-tuning and RAG for knowledge injection and found that RAG — which, like skills, provides knowledge at inference time — consistently outperformed unsupervised fine-tuning. In practitioner communities, Miessler (2024) has argued that business AI should be understood as the automation of *intelligence pipelines* — sequences of judgment tasks previously requiring human expertise — and that the quality of the scaffolding surrounding a model often matters more than model intelligence itself, reporting cases where a well-structured context enabled smaller models to outperform larger ones (Miessler, 2025).

This thesis contributes to this emerging picture with controlled empirical evidence. The core insight motivating the work is straightforward: **agents are the delivery vehicle; skills are the knowledge.** Any agent that loads a SKILL.md skill benefits directly from the quality of that skill's content. By validating skill effectiveness at the LLM level — through controlled experiments with and without skill injection — this thesis provides a foundational answer: does the skill content actually help? If yes, every agent in the agentskills.io ecosystem that uses this skill inherits that benefit automatically. And if structured, portable domain knowledge measurably improves performance, this strengthens the case for skills as a scalable mechanism through which domain experts — not only AI engineers — can shape agent behavior.

---

## 2. Research Questions

**RQ1:** Does a domain-specific SKILL.md improve LLM performance on merge conflict resolution compared to no skill?

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
- Ovadia, O., Brief, M., Mishaeli, M. & Elisha, O. (2024). *Fine-Tuning or Retrieval? Comparing Knowledge Injection in LLMs.* EMNLP 2024, pp. 237–250.
- Li, X. et al. (2025). *Injecting Domain-Specific Knowledge into Large Language Models: A Comprehensive Survey.* arXiv:2502.10708.
- Kujanpää, K. et al. (2024). *Efficient Knowledge Injection in LLMs via Self-Distillation.* arXiv:2412.14964.
- Gartner (2025a). *Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027.* Press release, June 2025.
- Gartner (2025b). *Gartner Predicts 40% of Enterprise Apps Will Feature Task-Specific AI Agents by 2026.* Press release, August 2025.
- Miessler, D. (2024). *Business AI Is the Automation of Intelligence Tasks.* danielmiessler.com/blog.
- Miessler, D. (2025). *Building a Personal AI Infrastructure.* danielmiessler.com/blog.
- agentskills.io specification — https://agentskills.io/specification
- Hermes Agent — https://hermes-agent.org
- ConGra GitHub — https://github.com/HKU-System-Security-Lab/ConGra
- Anthropic skills examples — https://github.com/anthropics/skills
