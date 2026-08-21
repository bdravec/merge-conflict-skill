---
name: merge-conflict-resolve-v2
description: Resolves Git merge conflicts in source code files. Use when given a file containing Git conflict markers (<<<<<<< a, =======, >>>>>>> b) and asked to produce a resolved version.
metadata:
  version: "2"
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

## Identify the resolution pattern

There are four patterns: **empty**, **combine**, **pick**, **custom**. Apply the following tests in order — the first match decides.

1. **Empty test.** Both sides are deletions or whitespace-only → **empty** (produce no content).
2. **Combine test.** Sides add *independent*, non-overlapping content → **combine** (concatenate them).
3. **Pick (default).** Otherwise → **pick** one side per the criterion below.
4. **Custom escape.** Only if pick cannot produce a coherent file AND combine does not apply → **custom** (smallest reconciliation from existing tokens).

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

Produce the smallest reconciliation of the two intents using only tokens already present in sides `a` and `b`. Do not introduce new identifiers, new functions, or new abstractions. If neither side has the tokens needed, prefer a *pick* of the more self-contained side over fabrication.

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
- **One side empty:** take the non-empty side (this is *pick*, not the *empty* pattern — that one needs both sides to be deletions).
- **Imports — same symbol, different module:** *pick*; surrounding-code use decides.
- **Broken syntax:** the resolution must parse. If neither side parses on its own, escape to *custom* and reconcile using only tokens from sides `a` and `b`.
- **Comments:** if only comments differ, pick the better one and do not combine. If code also differs, the comment must match the picked code, not the discarded one.

## Output format

Return the complete resolved file in a single fenced code block.

The output must be no longer than `|a| + |b|` characters (the combined length of side `a` and side `b`).

Do not include any text before or after the code block. Do not include explanations, reasoning, or commentary inside the code block. Do not introduce identifiers that did not appear in side `a`, side `b`, or the surrounding code, unless the pattern is *custom*.

No prose. Code only.
