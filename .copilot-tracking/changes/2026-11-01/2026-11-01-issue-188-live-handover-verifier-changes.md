---
title: Issue 188 live handover verifier changes
ms.date: 2026-11-01
---

* Plan: ../../plans/2026-11-01/2026-11-01-issue-188-live-handover-verifier-plan.md
* Added `SensorConsumer.observed_series` (src/core `sensor_consumer.py`), `src/api/src/zava_forward/api/sensor_handover_verify.py`, test extensions in `src/api/tests/test_sensor_consistency.py`, API README section, research plan section and log entry.
* Critique (single pass, executed, verdict: proceed): home identifiers are lowercase for stock homes, so validation uses the printable-ASCII bound, not the uppercase identity rule (applied; first test run failed on this). Zero-tolerance default uses the `ZERO_TOLERANCE` singleton (ruff B008).
* Validation (local focused tier, venv with pip): api `test_sensor_consistency` + `test_sensor_ingestion` 81 tests OK; core `test_sensor_consumer` + `test_sensor_handover` 42 OK; ruff check and format --check clean for src/api and src/core; mypy src/core clean; src/api mypy shows only 33 pre-existing missing `playwright` stubs, none in touched files.
* Not run: SQL Server (`ZF_SENSOR_MSSQL`), Azure SQL, live Hub, full local RPI gate (CI is the evidence).
* Review-thread correction (PR 645): `observed_series` now accepts per-home inclusive windows, validates homes with `home_key` plus the 64 UTF-16-unit bound (non-ASCII canonical IDs accepted); the verifier opens the store without initialization (`open_existing_store`, SQLite `mode=ro`, writable only for `--replay-check`), bounds observed rows to the reference window, and replays the retained stored payloads in batches of 100 instead of the reference rows. Tests added for windows, non-ASCII/over-bound homes and the read-only connection. Validation: core 43 and api 83 focused tests OK, ruff clean.

## PR #645 Copilot review follow-up

* `SensorConsumer.observed_series` now returns the retained `sensor_delivery.observation_body` witness for consumer-managed readings, validated with `_accepted_witness` and `_retained_reading`, so accepted strings (for example `"20"`, seed `"-0"`) and the accepted calibration flag survive normalization and later calibration withdrawal. Witness loading is shared via `_witnesses`. A stored row that departs from its witness is refused as `SENSOR_OUTCOME_MALFORMED`.
* The verifier validates each reference row in `_windows`, so truncated CSV records give the JSON refusal and status 2 instead of a `TypeError`.
* Tests: retained-payload and withdrawn-calibration case in the core consumer tests; truncated CSV and witness-mismatch refusal in the API consistency tests. The mssql `src-namespace` CI failure was still in progress and its log unavailable at the time of this change.
