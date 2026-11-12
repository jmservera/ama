---
title: Issue 521 rollback-fixture diagnostic D1 changes
ms.date: 2026-11-11
task_id: 521-rollback-d1-1111
---

## Changes

* `src/core/tests/test_resident_showcase_sql.py`: import `timedelta`; the rollback test's invalid row now ends `rs.AUTHORITY_END + timedelta(seconds=1)` instead of the literal cap. Nothing else changed.
* `infra/README.md`: one dated subsection "Rollback test fixture correction (2026-11-11, Refs #521)".
* RPI artifacts under `.copilot-tracking/` (research, plan, details, critique, changes, review, state). No product, SQL template, JSON, Bicep, helper, cap, guard or permission change.

## Raw validation (session files, outside the repo)

Outputs in `/home/azureuser/.copilot/session-state/38e61c82-3c44-4b97-af59-9eed5c151ac7/files/`: `521-d1-red-1111/`, `521-d1-green-1111/`, `521-d1-probe-1111/`, `521-d1-units-*-1111.log`; runner `run-521-d1-sql-1111.sh`.

* RED (unchanged fixture, real SQL, container `4f8af259e465`, 127.0.0.1:32768): 1 test, FAIL `AssertionError: Error not raised` at the `assertRaises` line.
* GREEN (same test, new SQL container): 1 test OK; full `test_resident_showcase_sql` module 40 tests OK, 0 skipped.
* Probe on the corrected data: `IntegrityError ... ALTER TABLE statement conflicted with the CHECK constraint "ck_allowed_case_window"`.
* Units (no SQL env): core `test_resident_showcase` plus `test_resident_showcase_sql` 81 tests OK, 27 SQL opt-in skips. Infra `test_resident_demo_deploy` plus `test_resident_demo_secrets` 33 tests OK.
* `ruff check`, `ruff format --check` (changed file), `mypy` (297 files, strict): no issues; no inherited findings appeared.
* Lock: non-queued `flock -n` held per run, holder probe refused a second admission; image cached id `sha256:cf8f0ab2ebe6...`, no pull; own containers removed, none left labelled `ama.rpi.owner=521-d1-1111`.

## Divergences and boundaries

None from the plan. D1 consumed. AC1 and AC4 unmet. Not run: complete gate, hosted CI, live SQL. No push or PR.
