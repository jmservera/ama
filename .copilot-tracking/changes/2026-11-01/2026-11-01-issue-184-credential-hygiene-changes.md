---
title: Issue 184 credential hygiene changes
ms.date: 2026-11-01
---

## Changes

* Added `src/api/tests/test_iot_credential_hygiene.py` (6 tests).
* `src/api/pyproject.toml`: module added to the existing mypy untyped-call override.
* `docs/reference/research/iot-sensor-analytics-research-plan.md`: #184 row; `docs/reference/log.md`: entry.

## Validation (focused tier, pip venv outside the repo)

* New plus `test_iot_stream`: 34 tests OK.
* `ruff check .` and `ruff format --check .` clean in src/api.
* `mypy`: two errors in tests/scale_load.py and tests/test_scale_load.py, identical on main without this change.
* No heavy gate, no Azure, no credentials, no source behaviour change.

## Unmet

Criterion 1 (owner acceptance of child deferrals); real credential lifecycle and Hub-side telemetry evidence for criterion 3.

## Correction cycle 1 (PR 704, 2026-11-01)

* Research: two unresolved Copilot threads on `src/api/tests/test_iot_credential_hygiene.py`, both valid: dotenv files (`.env`, `.env.local`) skipped by the suffix filter; `run_publisher` swallowed `StreamError` when no failure was injected.
* Plan/Changes: added `is_scanned` and `scan_directory` helpers plus a temp-directory dotenv regression test; re-raise `StreamError` unless a failure was injected.
* Review: ruff check and format clean; mypy shows the same 14 pre-existing `azure.iot.device` stub errors as before the change; 35 `test_iot*` tests pass in a local venv. No Azure access.
