# Issue 81 SQL main integration details, 2026-11-09

Plan: `.copilot-tracking/plans/2026-11-09/issue-81-sql-main-integration-plan.md`.

## P1 Commit prospective records

Commit research, plan, details and an in-progress state file alone, Conventional Commit, repository-local noreply identity, Copilot trailer. Success: clean tree, HEAD recorded.

## P2 Merge

* `git fetch origin`; confirm `8d6f029c` is an ancestor of `origin/main` and equals its tip.
* `git merge --no-ff 8d6f029cac004506953f36606862168bbe9d9412`.
* Inspect both sides of each conflict hunk against `git show 067d1b380:<path>` and main. Preserve: main's priority-order tests and SQL guard; this branch's resident-decision, gate and hold tests. Verify no hunk from either side is silently dropped.
* Check `store.py` and README auto-merges for semantic overlap.

## P3 Checks

* Fresh owned venv under `mktemp -d` or the owned `/mnt/ama-gates` path; editable installs of `src/core`, `src/agents`, `src/api`; verify `zava_forward.core.__file__` is in this worktree.
* Non-SQL: test_gates, test_resident_decisions, test_priority_order, test_quality_procurement, test_hazard_referral, test_handoff_lifecycle, test_grant_lifecycle_controls; API test_auth, role_matrix, hazard_api, handoff_api, grant_lifecycle_api, resident_api, entra_authoritative, role_endpoint_inventory, test_case_journey. ruff check, ruff format --check, mypy.
* SQL: one `flock -n /tmp/ama-rpi-heavy.lock`, one owned container (labelled, loopback, random port, generated password, removed on exit), `ZF_RESIDENT_MSSQL=1 ZF_SQL_AUTH=password ZF_SQL_TRUST_CERT=1`, manifest guard. Selectors: test_resident_decisions, test_priority_order, test_sqlstore, test_sqlreads, test_sqlqueues, test_taskqueues, ranking and quality SQL tests.
* Record exits, counts, skips, imports, container id and cleanup.

## P4 Review and handoff

One author Review; AC matrix (all four #81 criteria remain unproven or unmet; `Refs #81`); handoff `handoff-81-sql-main-integration.md`.
