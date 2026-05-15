# Pilot conditions explained — system vs user message slots

Reference for the "Conditions" table in [`pilot_results.md`](pilot_results.md).
Explains what `system` and `user` messages are, where SKILL.md goes in each
of the three pilot conditions, and how to read the condition names.

---

## Modern chat LLMs take a structured message array, not one big prompt

Chat-tuned models (Qwen3, Apertus, GPT-4, Claude) don't take a single prompt
string. They take an **array of messages**, each tagged with a `role`. In
[`scripts/pilot.py:210-213`](../scripts/pilot.py#L210-L213):

```python
messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user",   "content": full_user},
]
```

Two slots per call: a **system message** and a **user message**. They are
not "placed" anywhere in a file — they are separate keys in a JSON payload
sent over HTTP to vLLM.

---

## What the two roles do

| Role | Purpose | Mental model |
|---|---|---|
| `system` | Instructions, persona, rules, constraints. Sent before any conversation turn. | "Setup for the model" — what it is, how it should behave. |
| `user` | The actual question or task from the human. | "The thing being asked right now." |

Chat-tuned models are post-trained (RLHF, instruction tuning) so the system
message carries stronger weight as authoritative instructions, while user
messages are treated as the request to act on. That is why people put "You
are an expert X…" or strict rules in the system slot — the model is
conditioned to follow it more reliably than the same words in a user
message. This is a soft convention learned during training, not enforced by
the model architecture.

---

## What goes in each slot in this thesis

### The ConGra default system prompt

From [`scripts/pilot.py:142-145`](../scripts/pilot.py#L142-L145):

```python
CONGRA_SYSTEM_PROMPT = (
    "You are an expert in code merge conflicts, "
    "providing the merged code based on the conflict and its context."
)
```

A one-line "you are an expert" persona, no rules or pattern guidance.

### The ConGra user-message template

From [`scripts/pilot.py:147-162`](../scripts/pilot.py#L147-L162):

```text
Please provide the merged code based on the specified conflict and its context.
Please provide the merged code following the chain of thought:
1. Understand the cause of the conflict: Examine the conflicting code and its context to understand why the conflict occurred.
2. Decide how to merge: Based on the functionality and logic of the code, determine which changes should be kept or how the changes from both sides can be combined.
3. Provide the merged code, using "```{language}" as the beginning and "```" as the end of the merged code. You only need to output the resolution of the conflict without providing any context.

Here is the context related to the conflict:
```{language}
{conflict_context}
```
Here is the conflict that needs to be resolved:
```{language}
{conflict_text}
```
```

This is a **chain-of-thought (CoT) prompt**: it instructs the model to
reason step-by-step ("understand cause → decide → emit") before producing
the resolution. CoT is a prompting style where the model is told to walk
through its reasoning before answering, rather than jumping straight to the
output.

The template contains both prompt scaffolding (the numbered CoT
instructions and the output-format hint) and the actual data being resolved
(the language hint, conflict context, and conflict text).

### What "SKILL.md content" means

A SKILL.md file has two parts: YAML frontmatter (between `---` markers,
defining `name`, `version`, `description`) and the prose body below.
[`load_skill_md()` in `scripts/pilot.py:165-171`](../scripts/pilot.py#L165-L171)
**strips the frontmatter** and returns just the prose body — the rules,
pattern hierarchy, worked examples, output discipline.

When this thesis refers to "SKILL.md vX content," it means that stripped
prose body, not the file as-written on disk.

---

## The three pilot conditions

| Condition | **system slot contains** | **user slot contains** |
|---|---|---|
| `no-skill` | ConGra default sysprompt: *"You are an expert in code merge conflicts…"* | ConGra CoT template (numbered instructions + payload) |
| `skill-vX-sys` | **SKILL.md vX body** — ConGra default is *dropped* and overwritten | ConGra CoT template (unchanged) |
| `skill-vX-user` | ConGra default sysprompt: *"You are an expert in code merge conflicts…"* — unchanged | **SKILL.md vX body** + `\n\n` + ConGra CoT template (skill is *prepended*) |

Three invariants follow from this table:

- The **system slot is never empty.** It contains either ConGra's "You are
  an expert…" line, or the SKILL.md body.
- The **user slot always contains the ConGra CoT template** (the numbered
  reasoning instructions plus the conflict payload). What changes is
  whether the SKILL.md body is prepended in front of it.
- The **skill** appears in exactly one place per condition: nowhere
  (`no-skill`), in the system slot (`-sys`), or in the user slot (`-user`).
  Never in both.

Wiring is in [`scripts/pilot.py:200-220`](../scripts/pilot.py#L200-L220)
(`call_vllm`) and the per-condition prompt assembly elsewhere in the file.

---

## How to read the condition names

The `-sys` / `-user` suffix names **the slot SKILL.md was injected into**,
not which slot is empty:

- `skill-v2.1-sys` reads as "skill version 2.1, injected into the
  **`sys`tem** slot."
- `skill-v2.1-user` reads as "skill version 2.1, injected into the
  **`user`** slot."

It does **not** mean "no skill in the system slot." Even in
`skill-vX-user`, the system slot still contains ConGra's "You are an
expert…" line. The naming describes injection position, not slot occupancy.
