---
title: Issue 79 r27 plan, score-only merge of main f0afa8d7
ms.date: 2026-11-07
---

* Commit this plan and the details before the merge. Then one `git merge --no-ff origin/main`. No rebase, squash, amend or rewrite.
* Prove: parents are the planning head and f0af; score blob equals main; JSON parses; every other path (src, tools, workflows, tests, old RPI, log) is byte and mode equal to the planning head; `git diff --check`.
* Stop with evidence on any conflict or main movement.

## Critique (author, one pass, not independent)

* A merge adds a merge commit; accepted because it avoids another 37-commit rewrite and keeps ancestry for the gate. The score file is generated and adopted exactly, not regenerated.
* Disposition: proceed.
