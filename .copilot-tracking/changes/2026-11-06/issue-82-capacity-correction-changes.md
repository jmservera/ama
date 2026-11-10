# Issue 82 capacity-at-booking correction changes

Date: 2026-11-06 (UTC). Branch `feat/remaining-gate-family-readiness-82`, base `8cae59ec8`, parent81 `d4d33c7ec`, main `bb3a3b03c`. Refs #82. The r1 plan, changes and review (RV-001/002/003) are unchanged.

## Order

1. Correction research, plan and details supplements written before any test or source edit.
2. Tests added; RED: 4 errors (plain `ValueError` on Json and Sql for no order and unbooked order), exit 1 (`/tmp/ama82-corr-red2.log`). A first RED run also showed a test-snapshot `KeyError` on the absent procurement key (a test bug, kept in `/tmp/ama82-corr-red.log`); an empty procurement skeleton is lazily created by reading on the JSON store, so the snapshot now normalises absent versus empty. This is a test fix only.
3. Source corrected; a first GREEN attempt failed on that snapshot bug (`/tmp/ama82-corr-green1.log`), then passed.

## Source (src/ only)

* `procurement.py`: the single-evidenced-order refusal raises `gates.CapacityGateError(same text, None)` (Unknown); class remains a `ValueError`; same position and order. Closes RV-001.
* `appointments.py`: `_appointment_assessment` returns the typed capacity error only when it is the sole missing item (`len(missing) == 1`); `require_appointment_commitment` rethrows structurally. The `str()` equality is gone. Message text, mixed-failure behavior and the `appointment_status` shape are unchanged. No runtime defect is claimed; this fixes the discriminator.

## Tests

Two shared `Flows` cases (inherited by Json, Sql, MssqlProcurement): no work order, and an issued but unbooked order. Both assert `CapacityGateError`, Unknown, the unchanged text, and no case, procurement or audit change.

## Light evidence (real exits)

* Targeted `-k unknown_and_changes_nothing` Json and Sql: exit 0, 6 tests OK.
* `test_gates test_quality_procurement test_consultation_controls`: exit 0, 197 tests, OK (skipped=16). Skips are not SQL Server evidence.
* `ruff check`, `ruff format --check`, mypy (266 files): all exit 0. Import path asserted as the worktree.

## Remaining

RV-002 (Pass is server-internal, not persisted) is intentionally out of scope. RV-003: real MSSQL execution is pending the FULL run. The rule stays an unreviewed exercise rule. Whole #82 is unmet. Heavy admission belongs to #188; nothing was queued.
