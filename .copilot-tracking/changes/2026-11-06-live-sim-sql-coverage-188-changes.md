---
title: Changes for #188 real-SQL coverage correction
ms.date: 2026-11-06
---

* Plan clarifications recorded before the first edit (root): reuse the `consumer.mssql == (ZF_SENSOR_MSSQL == "1")` assertion right after consumer construction; do not run `tools/rpi-checks.py --changed` (deferred to the later actual FULL, not a pass); no SQL helper, Docker or gate; the existing `check=True` on `docker rm` already checks removal, so the plan's "unchecked" wording is withdrawn and the control flow is unchanged.
* `src/api/tests/test_sensor_consistency.py`: backend assertion in `LiveEnvelopeReplayTests.seeded` and `WeatherContinuityTests.seeded`, before configure and ingest writes.
* `src/core/tests/test_sensor_consumer_live.py`: `import os` and the same assertion in `LiveReadingTests.setUp`.
* `src/api/checks/sensor_sql_check.py`: three selectors added (`WeatherContinuityTests`, `LiveEnvelopeReplayTests`, `test_sensor_consumer_live`). Container, loopback, resources, password and `finally` lifecycle untouched.
* `src/api/README.md`: the two sensor SQL descriptions list the extended selectors; the existing constructed-local-only limitation text is retained.
* Original post-hoc ingest chronology and the later true weather chronology are unchanged.

## Focused execution (light, SQLite, bytecode off, external caches)

* Import proof with explicit PYTHONPATH (api/core/agents src and tests, no mvp): sensor_consumer, sensor_handover_verify, sensor_consumer_fixture and test_sensor_consistency all resolved under /home/azureuser/source/ama-wt/i188/src.
* `python3 -m unittest test_sensor_consistency test_sensor_consumer_live test_sensor_ingestion`: Ran 102 tests, OK, exit 0, no skip reported. One expected CLI refusal JSON line (absent.csv) is test output.
* `ruff check --no-cache src/api src/core`: all checks passed. `ruff format --no-cache --check` on the touched files: already formatted. `mypy --cache-dir=/tmp/i188-mypy-r9` on `sensor_sql_check.py`: no issues.
* Not run (pending): sensor SQL helper (zero-skip, backend proof, run count), `tools/rpi-checks.py --changed`, FULL, independent review, hosted checks. #185 owns the sole heavy slot.
