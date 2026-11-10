---
title: Quality sensor demo 1288 C7 changes
ms.date: 2026-11-08
---

Recorded 2026-11-08T23:30Z, after the C7 research and plan commit `4aed0c929`. Base `4a1b42b8`.

## Source

* `ai_consumption.py`, `ai.py`: gate context and gated `http.client` transport (send authorised after connect, before first byte; `suspended-before-dispatch`).
* `assistants.py`: per-attempt `assistant_dispatch_gate` fences; `_upgrade` migration of C5/C6 schemas (`replaced`, `dispatched`, index); bounded `ORDER BY dispatched` adoption using the task's own signature; frozen manual/proactive status; exhausted-slot pause in scan and claim with recovery; manual enqueue does not touch the slot; content-based cited comparison.
* `sensor_consumer.py`: per-home change set and per-home gate wait.
* `web/assistants.js`: wording separates changed or no-longer-retained cited readings from extra uncited ones. Web guidelines refreshed before the edit.
* `README.md`: C7 paragraph with residual limits.

## Tests

* New `test_quality_sensors_c7.py` (48 tests, 7 SQL Server variants skipped). Red `/tmp/c7-red-1.txt` (8 failures, 9 errors) then green.
* C6 tests updated for the gate rename and new semantics; the inherited guard test is now backend specific (1 trigger on SQL Server, 3 on SQLite); the T-SQL shape double in `test_assistants.py` answers `COL_LENGTH`.
* Ruff check and format exit 0 for both quality test files (`/tmp/c7-ruff-check-final.txt`, `/tmp/c7-ruff-fmt-final.txt`).

## Results (`/tmp/c7-green-final-*.txt`)

* quality_sensors_c7 OK (48, skip 7); quality_sensors OK (187, skip 92); assistants OK (120, skip 58, `/tmp/c7-green-final2-test_assistants.txt`); assistant_release, sensor_consumer, sensor_ingestion, iot_stream, regulatory_chat_api OK; core suite exit 0; `node --check` exit 0.
* All provider tests use a loopback or mock; none is live AI or SQL Server acceptance.

## Pending

Real SQL Server and query plans, browser and axe, #184/#1292 integration, FULL receipt, release, live walkthrough.
