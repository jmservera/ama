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

## Correction cycle 2 (PR 704, 2026-11-01)

* Research: one unresolved Copilot thread: the scan suffix allowlist omitted `.pem` and `.key`, so the private-key detector never read them. Valid.
* Plan/Changes: added `.pem` and `.key` to `SUFFIXES` and a `test_private_key_files_are_scanned` temp-directory regression test. Merged `origin/main` (log.md kept both sides; `role-screens.js` passes `node --check`).
* Review: ruff check and format clean; `test_iot_credential_hygiene` and `test_iot_stream` (36 tests) pass in a venv with the src projects installed; mypy shows only third-party stub errors (azure, playwright), none new. No Azure access.

## Correction cycle 3 (PR 704, 2026-11-01)

* Research: three unresolved Copilot threads on `src/api/tests/test_iot_credential_hygiene.py`, all valid: `.sh` and `.bicepparam` not scanned; fake SDK captured only `message.data`; failure test omitted formatted tracebacks (exception chaining).
* Plan/Changes: added `.sh` and `.bicepparam` to `SUFFIXES` with a temp-directory regression test; the fake SDK now records body, `message_id` and `custom_properties`; failure and timeout tests also check `traceback.format_exception` output. `origin/main` already merged (no changes).
* Review: ruff check and format clean; 37 `test_iot_credential_hygiene` and `test_iot_stream` tests pass in a venv; mypy shows only pre-existing errors in files this change does not touch. No Azure access.
