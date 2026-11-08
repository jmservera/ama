---
title: Issue 79 r30 plan
ms.date: 2026-11-07
---

* Commit this plan, then one normal `git merge --no-ff origin/main`; no rebase, amend, reset or peer-branch merge. Stop on any conflict whose intent is not both-sides-preservable.
* Prove: parents, incoming blobs and modes equal main, root-owned source blobs equal 8010a486, log keeps the root prefix and both appends, `git diff --check`.
* Light own-source checks only; no FULL, browser, SQL, Docker, child or lock.

## Critique (author, one pass, not independent)

* The log is the only overlap; a textual auto-merge could reorder chronology, so the merged log is checked for both prefixes. Disposition: proceed.
