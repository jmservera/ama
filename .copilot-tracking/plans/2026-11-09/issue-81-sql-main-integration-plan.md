# Issue 81 SQL main integration plan, 2026-11-09

Refs #81 only. Research: `.copilot-tracking/research/2026-11-09/issue-81-sql-main-integration-research.md`. Details: `.copilot-tracking/details/2026-11-09/issue-81-sql-main-integration-details.md`. Local only: no push, PR/issue/board change, merge to main, deploy, model calls, live or private data, credentials.

## Phases

* P1: commit these prospective records before any merge, edit or check.
* P2: `git merge --no-ff 8d6f029cac004506953f36606862168bbe9d9412` (normal merge, no rebase/reset/force). Resolve `test_resident_decisions.py` (and review `store.py`, README auto-merges) keeping both intents. Stop and report on any unresolved intent conflict.
* P3: worktree-bound owner-demo-targeted checks: non-SQL core/API selectors from the forward-preparation set, ruff, format, mypy; then one nonqueued `flock -n` heavy-lock admission for owned disposable loopback SQL Server running test_resident_decisions, test_priority_order and the SQL selectors (sqlstore, sqlreads, sqlqueues, taskqueues, ranking, quality) with manifest guard. Record each producer exit, import paths and counts.
* P4: Review once; commit changes, review, state; write the coordinator handoff.

## Constraints

* Busy lock: do independent light work, record the exact blocker, return a resume plan; no queueing, waiver, loop or cloud fallback.
* Full `rpi-checks --all` is not required by the owner demo tier and is not run. Hosted CI and independent exact-head review stay mandatory.
* Correction budget: nothing consumed or reset. A newly confirmed defect needs a scoped budget decision, not blind coupled source expansion.

## Critique (author, once, before changes)

* Verdict: proceed. Applied directly: merge the exact SHA, not a moving ref; resolve the conflict by taking main's structure and re-applying this branch's resident-decision tests only where they still pass; verify imports resolve to this worktree; do not infer results from earlier summaries; keep SQL admission single-shot.
* No finding conflicts with confirmed owner decisions. No repeat critique.
