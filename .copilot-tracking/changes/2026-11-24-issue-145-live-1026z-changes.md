---
title: Issue 145 live changes (2026-11-24 10:26Z run)
ms.date: 2026-11-24
---

Status: implemented. Tier FULL (src change); the coordinator runs the gate, `rpi-checks.py --all` was not run.

## Files

* `src/core/src/zava_forward/core/recovery.py`: `close_allowance_after_restore`.
* `src/core/tests/test_recovery.py`: `test_restore_does_not_resurrect_spent_allowance`.
* `infra/sql-recovery-runbook.md`, `src/core/README.md`: reapply step documented.
* `docs/reference/research/issue-145-live-20261124T1026Z-2026-11-24.md`, `docs/reference/README.md`, `docs/reference/log.md`.

## Validation

* `src/core` `test_recovery`: 24 tests OK. `ruff check` passes. `mypy` shows 3 pre-existing errors (missing opentelemetry stubs, one unused ignore in `device_provision.py`), identical without the change.
* No full test-suite run, no live restore; admission code is untouched.

## Per-criterion table

| # | Criterion | Status |
| --- | --- | --- |
| C1 to C3 | Parameters, PITR with ledger result, objectives | Proven (ticked) |
| C4 | Backup redundancy and retention match #121 | Unproven: Local, 14 days, no LTR; #121 retention deferred to #1906 |
| R1 | Actual backup restore with document and audit state | Partly proven: SQL only; no blob PITR; no drill authorised |
| R2 | Reconcile and reapply tombstones and holds | Partly proven: erasure yes; no legal-hold state |
| R3 | No resurrection (release, erasure, allowance) | Proven in SQLite emulation only (allowance fixed this run) |
| R4 | DPO approval | Waived for the demo |
| R5 | Independent witness | Unproven: worker not independent |
| R6 to R8 | Disposable limits, lower-tier label, counts only | Proven (ticked) |

Artifact hygiene: earlier same-day artifacts (no suffix) were restored untouched; this run uses the `1026z` suffix.
