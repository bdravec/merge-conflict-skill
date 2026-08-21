---
name: swebench-repair-v1
description: Fix a bug in a software repository by producing a single unified-diff patch that both resolves the issue and applies cleanly with git apply. Use when given a GitHub issue and line-numbered source and asked to return a patch.
metadata:
  version: "1"
---

## Task

Fix a real bug in a software repository.

**Given:** a GitHub issue + the relevant source file(s), shown **with line numbers** (important — you need them to write the diff).

**Produce:** a single unified-diff patch that:

1. **Fixes the issue** — makes the failure go away, passes the project's tests, leaves unrelated behavior untouched.
2. **Applies cleanly** with `git apply`.

Return only the patch.

## Core principle

Two ideas govern every rule below:

1. **The diff is mechanical, not prose.** `git apply` matches your patch against the file exactly — line numbers, counts, and context lines must be correct to the character. Treat the diff as code, not formatting.
2. **Change as little as possible.** Edit the fewest lines that fix the issue. Lean toward a small, localized hunk.

## Locate the change

1. **Find the root cause.** Read the issue, then find the exact line(s) in the provided source that cause it.
2. **Note their line numbers.** The numbers shown beside the source are what you build the hunk header from — track where your edit starts.
3. **Edit only those lines.** Leave everything else identical. Do not reformat, re-indent, reorder imports, or rewrite surrounding code.
4. **Make a real change.** The patch must differ from the original — no no-op edits, no placeholder or TODO, no deleting-then-re-adding the same line.

## Write a valid unified diff

Per changed file:

```
--- a/<path>
+++ b/<path>
@@ -<old_start>,<old_count> +<new_start>,<new_count> @@
 context
-removed
+added
```

1. **Hunk header needs real integers.** `@@ -old_start,old_count +new_start,new_count @@`. Never `@@ def foo():` or empty `@@`. `old_start` = first hunk line's number from the shown context.
2. **Counts:** `old_count` = context + removed lines; `new_count` = context + added lines. Recount after editing.
3. **One prefix char per line:** space = context, `-` = removed, `+` = added. Blank context line keeps its space.
4. **Context verbatim** from the source — exact text and indentation, a few lines around the change.

## Example

Source (as shown to you):

```
12  def add(a, b):
13      return a - b
```

**Wrong** — hunk header has no numbers, so `git apply` rejects it:

```
--- a/calc.py
+++ b/calc.py
@@ def add(a, b):
-    return a - b
+    return a + b
```

**Right** — real line numbers and counts, verbatim context line:

```
--- a/calc.py
+++ b/calc.py
@@ -12,2 +12,2 @@
 def add(a, b):
-    return a - b
+    return a + b
```

Hunk starts at line 12; 2 lines before (context + removed), 2 after (context + added).

## Output

Return only the patch, in a single `<patch> ... </patch>` block as the prompt asks. Nothing before or after — no explanation, no markdown fence.
