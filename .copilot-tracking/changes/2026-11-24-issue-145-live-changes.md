---
title: Issue 145 live changes (2026-11-24)
description: Changes record and per-criterion table for issue 145.
ms.date: 2026-11-24
---

Refs #145. Plan: [plan](../plans/2026-11-24-issue-145-live-plan.md).

## Changes

* `src/core/src/zava_forward/core/recovery.py`: `_release_changes` register, `record_release_change`, `reapply_release_changes`.
* `src/core/src/zava_forward/core/assistants.py`: record before `rel.change` in `change_release` and the serving-attestation suspension.
* `src/core/tests/test_recovery.py`: three regression tests (reapply, no-write cases, unwritable register).
* Docs: `src/core/README.md`, `infra/sql-recovery-runbook.md`, `docs/reference/research/issue-145-live-20261124-2026-11-24.md`, index and log.

## Validation (tier FULL by classification: release-authority source)

* `src/core` `tests.test_recovery`: 23 OK. `src/api` release, assistants, call-site, suspension and mssql suites: 496 OK (SQL Server cases skipped, no server). `infra` `test_sql_tier`: 8 OK. ruff check clean on changed core files. mypy: 3 pre-existing environment errors (opentelemetry stub, `device_provision.py`), none in changed files.
* Not run: `rpi-checks.py --all` (coordinator owns the gate), hosted CI, independent review, live Azure restore (no drills authorised).

## Per-criterion table

| # | Criterion | Status | Reason |
| --- | --- | --- | --- |
| C1 | SKU, auto-pause, redundancy parameters | Proven (ticked) | Bicep parameters, unchanged |
| C2 | PITR performed, ledger result | Proven (ticked) | 2026-11-18 restore evidence |
| C3 | Objectives stated or undecided | Proven (ticked) | Runbook |
| C4 | Backup redundancy and retention match #121 | Unproven | Observed Local and 14 days; #121 retention deferred to #1906, nothing approved to match |
| R1 | Actual backup restored with document and audit state | Partly proven | SQL restore earlier; no blob PITR; no drill authorised |
| R2 | Reconcile, reapply tombstones and holds | Partly proven | Erasure proven; no legal-hold state in demo |
| R3 | No resurrection of revoked, suspended, erased, spent state | Partly proven | Release reapply added (SQLite emulation); erasure earlier; spent allowance has no outside-SQL record |
| R4 | DPO and record-owner approval | Waived | Owner decision 2026-11-18 |
| R5 | Independent qualified witness | Unproven | Worker is not independent |
| R6 to R8 | Disposable limits, lower-tier label, counts only | Proven (ticked) | No resource created |
