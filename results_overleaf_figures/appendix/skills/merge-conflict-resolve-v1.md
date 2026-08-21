---
name: merge-conflict-resolve-v1
description: Resolves Git merge conflicts in source code files. Use when given a file containing Git conflict markers (<<<<<<< a, =======, >>>>>>> b) and asked to produce a resolved version.
metadata:
  version: "1"
---

## Task

You are given a source code file containing one Git merge conflict marked with:

```
<<<<<<< a
<lines from branch A>
=======
<lines from branch B>
>>>>>>> b
```

Your task is to resolve the conflict and return the complete resolved file.

## Steps

1. **Locate the conflict region.** Find the block delimited by `<<<<<<< a` and `>>>>>>> b`.

2. **Read both sides.** The lines between `<<<<<<< a` and `=======` are from branch A. The lines between `=======` and `>>>>>>> b` are from branch B.

3. **Read the surrounding code.** Understand what the file does and what each branch was trying to achieve.

4. **Determine the correct resolution.** Choose one of:
   - Keep branch A's changes if they are correct and branch B's are not.
   - Keep branch B's changes if they are correct and branch A's are not.
   - Combine both changes if both are valid and compatible.
   - Write a new resolution if neither side alone is correct but both contribute to the right answer.

5. **Produce the resolved file.** Replace the entire conflict block (including the `<<<<<<< a`, `=======`, and `>>>>>>> b` markers) with your chosen resolution. Return the complete file with no conflict markers remaining.

## Output format

Return only the resolved file wrapped in a single code block with the appropriate language tag:

\```python
<resolved file contents>
\```

Do not include explanations, comments about your reasoning, or any text outside the code block.
