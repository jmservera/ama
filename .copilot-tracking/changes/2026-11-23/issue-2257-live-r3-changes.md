---
title: Issue 2257 r3 changes
ms.date: 2026-11-23
---

Classification: FULL tier (src change in `src/core` and a test in `src/api`). Local commit only; no `rpi-checks.py --all` (coordinator owns gates).

## Planned changes

* `src/core/src/zava_forward/core/assistants.py`: tag the sensor overlay warning with `cause=sql-write-lock-busy` when the write lock timed out.
* `src/api/tests/test_map_sensors.py`: one test for it.
* `docs/reference/research/issue-2257-live-r3-2026-11-23.md` and folder (probe result, console window), index row, log entry.

## Validation

* `src/api` unittest: test_map_sensors, test_error_logging (30 tests) and test_assistants, test_quality_sensors (339 tests, 157 skipped) pass. `src/api` mypy and ruff check pass. `src/core` mypy shows 3 errors that also occur without this change (missing OpenTelemetry stubs and an unused ignore). No `rpi-checks.py --all`; the coordinator owns the full gate.

## Per-criterion table

| Criterion | Proven or unproven | Evidence |
| --- | --- | --- |
| Map recovers from a dropped connection without reload | Proven live on 0000055 (r2); retry button in main, not deployed, so its live effect is unproven | r2 recovery-proof-result.json |
| Server-side overlay failure does not fail the map | Proven live (r2) | r2 console-window.txt |
| Fresh-session failures gone | Unproven as a rate: 18 of 18 passed (8 in r2, 10 in r3) | probe-result-114822.json |
| Cause found | Largely proven; lock inferred until the tagged log line (this change) is deployed | r3 note |
| Billing, DPO/Legal, person-run AT | Not needed for the demo (owner decision 2026-11-18) | brief |
| Azure estate unchanged | Proven: read-only az and browser probes | this record |
