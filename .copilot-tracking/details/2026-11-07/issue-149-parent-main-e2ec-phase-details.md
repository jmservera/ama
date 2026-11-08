---
title: Issue 149 parent main e2ec integration phase details
ms.date: 2026-11-08
---

## Phase 1: normal merge

* Plan commit first, then `git merge --no-ff` of origin/main e2ecee25 into f8c1be6c. No conflicts, no manual edits.
* Main-relative delta after the merge: operator and atlas checkers, their tests, three UX and index docs, `src/api/README.md`, the Core `doc_controls.py` rejection wording (message only, legal-hold and retention predicates unchanged) and tracking records. The log shows 0 removed lines.
