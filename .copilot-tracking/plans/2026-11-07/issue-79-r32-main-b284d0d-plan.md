---
title: Issue 79 r32 plan
ms.date: 2026-11-07
---

* Commit research, plan and details first. Re-fetch main and require `b284d0d3`; stop and record the delta if different.
* One normal `git merge --no-ff origin/main`. No rebase, amend, reset, stash, cherry-pick, takeours or theirs.
* Prove: merge parents are 9dad2aba and b284d0d3; latest.json blob and mode equal main; every other non-tracking path equals 9dad2aba; JSON parses; `git diff --check`; ignored-clean.
* Metadata-only checks. No FULL, browser, SQL, Docker, scanner, child or lock.

## Critique (author, one pass, not independent)

* Risk: assuming auto-merge. Disposition: verify the actual diff and blobs after the merge, stop on any conflict.
* Risk: score JSON read as candidate approval. Disposition: recorded as main provenance only.
* Disposition: proceed.
