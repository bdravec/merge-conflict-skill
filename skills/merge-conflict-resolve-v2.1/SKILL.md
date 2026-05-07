---
name: merge-conflict-resolve-v2.1
description: Resolves Git merge conflicts in source code files. Use when given a file containing Git conflict markers (<<<<<<< a, =======, >>>>>>> b) and asked to produce a resolved version.
metadata:
  version: "2.1"
---

## Task

You are given a source code file containing one Git merge conflict:

```
<<<<<<< a
<lines from side a>
=======
<lines from side b>
>>>>>>> b
```

Replace the conflict block (markers and all) with the correct resolution. Return the complete resolved file with no conflict markers remaining.

**Produce only the resolved code.** No commentary, no explanations, no fabricated method bodies, no echoing of the surrounding code. The resolution should typically pick or combine the two sides; only escape to a custom resolution when neither pick nor combine fits the surrounding code.

## Output discipline

Apply these three rules to whatever resolution you produce. They apply before, during, and after pattern selection.

1. **No comments in the code block.** Do not include comments inside the code block unless they appear verbatim on side `a` or side `b`.
2. **No surrounding-code echo.** Do not copy lines from the surrounding code into the resolution unless they are part of side `a` or side `b`. The resolution replaces the conflict block; the rest of the file is already there.
3. **No fabricated identifiers.** Do not introduce identifiers — e.g., function names, variables, imports, attributes — that did not appear in side `a`, side `b`, or the surrounding code.

## Identify the resolution pattern

There are four patterns: **empty**, **combine**, **pick**, **custom**. Apply the following tests in order — the first match decides.

1. **Empty test.**
   - **1a.** *Both* sides are deletions or whitespace-only → **empty** (produce no content).
   - **1b.** Only *one* side is empty (the other is non-empty) → **pick** the non-empty side. This is *pick*, not empty.
2. **Combine test.** Sides add *independent*, non-overlapping content → **combine** (concatenate them).
3. **Pick (default).** Otherwise → **pick** one side per the criterion below.
4. **Custom escape.** Only if pick cannot produce a result that fits the surrounding code AND combine does not apply → **custom**. Use tokens from sides `a` and `b` first. If those alone cannot produce a coherent resolution, use tokens from the surrounding code as a secondary source. Do not invent tokens that appear nowhere.

Do not jump to *custom*. Most conflicts are *pick*.

## Resolution strategy by pattern

### Pick

Choose the side whose content is consistent with the surrounding code, in priority order:

1. **Symbol references.** If one side defines or imports a symbol used by the surrounding code, pick that side. Picking the other side breaks the file.
2. **Import / dependency consistency.** If one side adds an import that its own body needs, picking the other side strands the import or strands the use.
3. **Local style.** If 1 and 2 do not decide, prefer the side that matches naming and indentation in the surrounding 5–10 lines.

If both sides are valid alternatives that the criterion above cannot discriminate, commit to one side without inventing. Do not concatenate as a hedge.

### Combine

Concatenate both sides when they add *independent* content. For Python imports, preserve alphabetical order within each group; otherwise preserve existing source order.

Do not combine sides that modify the same construct differently — that is *pick*, not *combine*.

### Empty

Produce no content for the chunk. Use only when both sides remove the same code.

### Custom

If even the surrounding code does not provide the tokens needed, prefer a *pick* of the more self-contained side over fabrication.

## Worked examples

### Pick — symbol references decide

```
<<<<<<< a
from collections import OrderedDict
=======
from collections import defaultdict
>>>>>>> b

class Counter:
    def __init__(self):
        self.counts = defaultdict(int)
```

Pick side `b`. The class body uses `defaultdict`; picking side `a` would strand the import.

### Pick — identifier divergence

```
<<<<<<< a
j_tf = K.placeholder(shape=(None, 32), dtype=K.floatx())
=======
j_tf = tf.placeholder(dtype=K.floatx())
>>>>>>> b
```

The surrounding code uses `K.` prefixes (`K.int_shape`, `K.floatx`). Pick a — its API style matches the rest of the file. Do not pick b just because it is shorter.

### Pick — completeness over brevity

```
<<<<<<< a
if isinstance(field_name, str):
    item_field, output_field = field_name, field_name
else:
    item_field, output_field = field_name
if item_field in item:
    field = ... item.fields[item_field]
=======
if field_name in item:
    field = ... item.fields[field_name]
>>>>>>> b
```

Pick a. Side a encodes a real semantic distinction: it handles `field_name` being either a string or a tuple, with `item_field` and `output_field` as separately-named variables. Side b flattens this away. Completeness encodes the distinction; conciseness erases it. Surrounding-code consistency is the tiebreaker, not output length.

### Combine — independent additions

```
class Cache:
    def get(self, key):
        return self.store.get(key)
<<<<<<< a
    def set(self, key, value):
        self.store[key] = value
=======
    def delete(self, key):
        self.store.pop(key, None)
>>>>>>> b
```

Combine. Both methods are independent; concatenation produces coherent code.

### Custom — rearrange existing tokens

```
<<<<<<< a
def fetch(url):
    return requests.get(url, timeout=10).json()
=======
def fetch(url):
    return requests.get(url, headers=AUTH_HEADERS).json()
>>>>>>> b
```

Resolution:

```
def fetch(url):
    return requests.get(url, timeout=10, headers=AUTH_HEADERS).json()
```

Both sides modify the same call. Pick loses information; naive combine emits two return statements. Reconcile using existing tokens (`timeout=10`, `headers=AUTH_HEADERS`); do not introduce new identifiers.

## Edge cases

- **Both sides identical:** emit side `a` and stop. Do not look for a hidden distinction.
- **Imports — same symbol, different module:** *pick*; surrounding-code use decides.
- **Broken syntax:** the resolution must parse. If neither side parses on its own, escape to *custom*. Use tokens from sides `a` and `b` first; surrounding-code tokens are a secondary source.
- **Comments:** if only comments differ, pick the better one and do not combine. If code also differs, the comment must match the picked code, not the discarded one.
- **File-level resolutions:** some conflicts have ground-truth resolutions that depend on file-level patterns invisible from the conflict region alone (e.g. an architectural decision the rest of the file encodes but the conflict snippet does not). The skill cannot solve these. If neither pick, combine, empty, nor custom produces a result that fits the surrounding code, your best bet is the closest pick — the metric will reward it more than over-confident invention.

## Output format

Return the complete resolved file in a single fenced code block.

Do not include any text before or after the code block. Do not include explanations, reasoning, or commentary inside the code block.

After producing the output, ask: is this longer than the union of side `a` and side `b`? If so, you have likely added unnecessary content.

No prose. Code only.
