# Merge Conflicts Glossary

A quick-reference glossary of terms and concepts you'll encounter when dealing with merge conflicts in version control (Git).

---

## Verbatim

Taking a section of code exactly as it appears — character for character — with no modifications, rewording, or reformatting. When resolving a conflict, "keep theirs verbatim" means accepting the incoming version precisely as written.

## Conflict Markers

The special lines Git inserts into a file to show where a conflict exists. They follow this pattern:

- `<<<<<<< HEAD` — marks the start of your current branch's version.
- `=======` — separates the two conflicting versions.
- `>>>>>>> branch-name` — marks the end of the incoming branch's version.

You must remove all three markers (and choose or combine the code between them) to resolve the conflict.

## Ours vs. Theirs

Two labels Git uses to distinguish the conflicting sides:

- **Ours** — the version on the branch you are currently on (the one you're merging *into*).
- **Theirs** — the version from the branch being merged *in*.

Note: during a rebase, these labels are swapped, which is a common source of confusion.

## Three-Way Merge

The default merge strategy in Git. It considers three snapshots: the common ancestor (base), the tip of your branch, and the tip of the incoming branch. Conflicts arise only when both branches modified the same lines relative to the base.

## Base (Common Ancestor)

The most recent commit that both branches share before they diverged. Git uses this as the reference point to determine what changed on each side. Many merge tools show the base alongside "ours" and "theirs" for clearer resolution.

## Fast-Forward Merge

A merge where the target branch has no new commits since the source branch diverged. Git simply moves the pointer forward — no merge commit is created and no conflicts are possible.

## Merge Commit

A special commit with two (or more) parents that records the point where branches were combined. It is created automatically after all conflicts are resolved and the merge is completed.

## Hunk

A contiguous block of changed lines within a diff. When a conflict occurs, each conflicting hunk is wrapped in conflict markers. You resolve conflicts hunk by hunk.

## Diff

A representation of the differences between two versions of a file, shown as added (`+`), removed (`-`), and unchanged lines. Understanding diffs is essential for interpreting what each side of a conflict changed.

## Rebase

An alternative to merging that replays your commits on top of another branch. Conflicts during a rebase are resolved one commit at a time rather than all at once. The "ours/theirs" labels are inverted compared to a regular merge.

## Cherry-Pick

Applying a single commit from one branch onto another. If the picked commit touches lines that differ between the two branches, a conflict will occur — resolved the same way as a merge conflict.

## Stage / Index

Git's staging area. After resolving a conflict in a file, you run `git add <file>` to mark it as resolved (staged). Once all conflicted files are staged, you can complete the merge with `git commit`.

## Abort

Canceling a merge (or rebase) in progress and returning to the state before it started:

- `git merge --abort` — cancels a merge.
- `git rebase --abort` — cancels a rebase.

Useful when conflicts are too complex and you need to rethink your approach.

## Merge Tool

An external application (e.g., VS Code, IntelliJ, Beyond Compare, Meld) that provides a visual interface for comparing and resolving conflicts. Launched with `git mergetool`.

## Recursive Strategy

Git's default merge strategy for two branches. It can handle cases where the common ancestor is ambiguous by recursively merging ancestor candidates first, then using the result as the base.

## Octopus Merge

A merge strategy for combining more than two branches simultaneously. It does not handle conflicts — if any arise, Git aborts and asks you to merge branches individually.

## Squash Merge

Combining all commits from a branch into a single commit on the target branch. The result is a clean history but loses individual commit granularity. Conflicts are resolved once, against the squashed diff.

## Rerere (Reuse Recorded Resolution)

A Git feature (`git rerere`) that remembers how you resolved a particular conflict and automatically applies the same resolution if the identical conflict appears again. Especially useful during long-running rebases.

---

*Tip: When in doubt, use `git status` to see which files are in conflict and `git diff` to inspect what changed on each side.*
