---
title: Issue 2304 changes
ms.date: 2026-11-23
---

# Changes

Process note: a source prototype was drafted before the witness boundaries, then set aside (git stash) so plan-done and implement-start saw a clean source tree and restored afterwards. The witness recorded the qualification that source edits predate implement-start. A key-bounded revision followed the first full test run, which failed the existing no-history-scan guard.

## Files

* `src/core/src/zava_forward/core/forecast_reads.py` (new): read-through view, bulk reads, `ForecastTimeout`.
* `src/core/src/zava_forward/core/assistants.py`: forecast uses the view, two-pass loop, 10 s budget.
* `src/api/src/zava_forward/api/server.py`: `ForecastTimeout` becomes 503 `state: unavailable` with `Retry-After`.
* `src/api/tests/test_assistants.py`: `ForecastStatements` (flat statement count, named state).
* `src/api/tests/test_quality_sensors.py`: scan guard allows the explicit `WHERE id IN` primary key read.
* `docs/reference/research/issue-2304-forecast-live-2026-11-23.md`, its evidence folder, README index row, log entry.

## Validation

`test_assistants`, `test_quality_sensors`, `test_quality_sensors_e2` (419 tests OK, 196 skipped); ruff clean on new module; mypy unchanged in core (3 pre-existing errors) and clean in api. Output equality old versus new on two data sets. Tier FULL by classification (src change); `rpi-checks.py --all` not run; hosted CI not observed.

## Per-criterion table (Refs #2304)

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Profile where time goes | Proven on equivalent SQLite run (422 and 3622 statements before, 20 after); live trace unproven, SQL private |
| 2 | Answers within 10 s or named state | Proven in tests only; live timing unproven |
| 3 | Counting-connection test, no per-case growth | Proven |
| 4 | Live re-check after deployment | Unproven: ACR login 403 (public access disabled), no deployment made; baseline hang of 200 s recorded on revision 0000055 |
