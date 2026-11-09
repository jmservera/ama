---
title: Issue 1292 priority recommendation creation order review
description: Single independent post-implementation review outcome, evidence boundary and routed work
ms.date: 2026-11-08
---

## Execution and boundary

Review executed once (independent read-only code-review agent) on 2026-11-08 against implementation commit 656bacb56fbf90b89f76b75420e1c19dd593e79f (diff from 0fbd4058b), branch fix/priority-reload-1292, base 6354b13f7abf1441a815e92f2b01dc184ce0b0ac. It reran `test_priority_order` on SQLite (24 ran, OK, 10 skipped) and read the T-SQL paths; it could not run SQL Server. It is an agent review, not the independent exact-head human or hosted assessment, which the coordinator still owns. No later Review is run in this task.

## Outcome

Conformant, no high-confidence findings. Checked and found sound: T-SQL compatibility of the column add, `COL_LENGTH` check and guarded index (read only); ordinal assignment under the exclusive write lock; rollback and `_discard` recovery (`_rec_ord` updated only after commit, reload re-sorts); incremental sync with stable sort so edits never move a row; transactional backfill after any existing maximum with a `seq` bump; tests not vacuous (ids sort against creation order); no change to review, approval, consent or ranking boundaries.

## Residual and routed work (not fixed in this task)

* Native SQL Server execution of the new class and of the two original `MssqlResidentControls` selectors, plus a native red on base source, is PENDING coordinator admission to the heavy lock. Route: coordinator resumes this session. Blocking for any closing keyword.
* Ledger-enabled database variant of the migration is unproven. Route: native SQL run on a ledger-enabled database if the deployment uses one.
* Legacy ordering heuristic and older-writer rolling-deployment limit are documented, not removed. Route: named data owner decision for a live database; deployment runbook to stop older writers.
* Independent exact-head review, hosted CI and human approval remain required.
