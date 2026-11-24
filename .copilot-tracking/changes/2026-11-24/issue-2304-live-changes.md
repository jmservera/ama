---
title: Issue 2304 live changes (2026-11-24)
ms.date: 2026-11-24
---

# Changes

The opening record was persisted before any source edit (witness implement-start).

## Files

* `src/core/src/zava_forward/core/assistants.py`: `forecast` runs a background job per identity and period, waits at most 8 s from request start, serves the last good answer marked `stale_seconds` (up to 900 s) when the fresh one is late, else raises `ForecastTimeout`; `_forecast_compute` holds the former body; `_ForecastJob`.
* `src/api/tests/test_assistants.py`: three new tests in `ForecastStatements`.
* `docs/reference/research/issue-2304-live-2026-11-24.md`, `issue-2304-live-2026-11-24/` (probe, baseline JSON and PNG), README index row, log entry.

## Validation

* `test_assistants`, `test_quality_sensors`, `_e1`, `_e2`, `test_role_endpoint_inventory`, `test_progress_report_api`, `test_epic149_child_ux_contracts`: 605 tests OK (247 skipped for missing SQL Server), run sequentially. A first design (TTL cache that skipped recomputation) failed four existing freshness tests and was replaced by stale-while-slow, which never delays a fresh answer.
* `ruff check` clean; `mypy` in `src/core` reports the same 3 errors as the base (OpenTelemetry stubs, one unused ignore). `ruff format` was not applied to the already unformatted `assistants.py`.
* Tier FULL by classification (src change); `rpi-checks.py --all` not run; hosted CI not observed; nothing deployed or pushed.

## Per-criterion table (Refs #2304)

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Profile where time goes | Proven for the 13 to 17 s cause (code and live timings); live statement trace unproven, SQL private |
| 2 | Within 10 s on a quiet system or from a cache, or a named state | Proven in tests; live timing unproven (not deployed) |
| 3 | Counting-connection test, no per-case growth | Proven |
| 4 | Live re-check after deployment | Unproven: deployment reserved for the owner; baseline on 0000061 recorded |
