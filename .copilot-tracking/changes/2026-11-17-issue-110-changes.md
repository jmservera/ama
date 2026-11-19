---
title: Issue 110 changes
ms.date: 2026-11-17
---

# Changes

* Added `src/api/tests/test_no_public_ingestion_surface.py` (C4 guard).
* Added closure audit section to `docs/reference/research/iot-sensor-analytics-research-plan.md`; log entry in `docs/reference/log.md`.

## Validation (FOCUSED tier)

* Mutation: consumer import appended to `workbench.py` failed the guard; reverted, green. Initial run passed vacuously because the editable install resolved the main checkout; the test now derives its path from the test file (recorded adverse step).
* `PYTHONPATH=<wt>/src/{api,core,agents}/src:../core/tests:../agents/tests python3 -m unittest tests.test_iot_stream tests.test_iot_credential_hygiene tests.test_no_public_ingestion_surface -q`: 51 OK.
* `ruff format --isolated --line-length 100 --check` on new test: clean. `mypy` on new test: no issues.
* Core `test_device_registry_azure` / `test_iot_device_identity_enforcement`: 34F/16E `SDK_MISSING` (SDK extra absent); not counted.
* Not run: full gate, SQL/MSSQL, browser, live Azure (not applicable; no SQL/infra change).
