<!-- markdownlint-disable-file -->
---
title: Issue 349 remote-history reconciliation plan
description: Non-rewriting merge of the owned remote branch plus ancestry correction
ms.date: 2026-10-25
---

Research: ../../research/2026-10-25/issue349-tenant-readiness-preflight-remote-reconcile-research.md
Details: ../../details/2026-10-25/issue349-tenant-readiness-preflight-remote-reconcile-phase-details.md

* [x] Phase 1: Research.
* [x] Phase 2: Critique executed once before merge: Revise, no blocking issues. Applied: proof also asserts merged latest.json, test file and log.md equal the candidate (d78373a5) blobs. No repeat critique.
* [ ] Phase 3: git merge --no-ff 44ba5b77; resolve per research; new dated changes record correcting the ancestry claim; session-only proposed PR body.
* [ ] Phase 4: Focused tests, independent scoped assessment, commit, full gate only if the lock is free.

Constraints: local only; no push, force-push, PR or issue edit; draft; no
criteria ticked; earlier reviews, plans and the 2026-10-25 integration changes
record are not edited (the correction is a new record).
