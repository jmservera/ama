---
title: Research for #188 real-SQL coverage correction (forward corrective RPI)
ms.date: 2026-11-06
---

* Research disposition: executed (read-only source, log and artifact reading; no SQL service, gate, install, network or private data). Planning Readiness: Ready.
* Start: clean head 2d269590d91fe290040e54ccfe33369366a47c57, tree bdc2110d8defa70a61e811954fcfd715077d548f, ignored-inclusive status empty. Main and declared parent 184 are bb3a3b03cb94eef6c06ae4b12d07cfe7bbdef43f. PR 1203 public head c9a14573d is older than this candidate and is no evidence for it.

## Original chronology failure (preserved, not rewritten)

* The original native log `/tmp/rpi-188.log` line 224 starts "Implement live schema in consumer" (source editing). More implementation and tests follow through line 378. Line 388 "Write RPI artifacts" is the first write of the original Research, Plan and related records. The original ingest implementation was therefore post-hoc, not prospective.
* The later weather Research and Plan (`2026-11-05-live-sim-weather-continuity-188-*`) did precede that slice's changes. That is a separate, true distinction and is not proof that the original ingest was prospective. The original artifacts are not edited, backdated or regraded here. This record and its plan are a genuine forward corrective loop: Research and Plan are committed before any new test or source edit.

## Contract surface (existing, read-only)

* Ingest and roundtrip: `live-sim-reading-v1` envelopes are admitted by the consumer's `_live_shape`, retained losslessly as `retained_envelopes`, and replayed idempotently. Duplicate delivery returns replay receipts without changing readings, deliveries, DQ, cases or audit.
* Legacy versus weather: `observed_series` is indoor-only. `sensor_handover_verify.run` classifies observed and reference rows. Both indoor uses the unchanged legacy path. Both live uses `weather_report` (`synthetic-weather-continuity-v1`). Any other mix is refused with `HANDOVER_SCHEMA_UNSUPPORTED` before statistics or replay writes. Non-zero explicit tolerances on the weather path give `HANDOVER_TOLERANCE_NOT_APPLICABLE`.
* Evidence class so far: SQLite and constructed data only. The weather and live-envelope classes have never run on a real SQL Server.

## Coverage gap (verified by reading)

* `src/api/checks/sensor_sql_check.py` runs only `test_sensor_ingestion` and `test_sensor_consistency.SqlHandoverTests.test_composed_joint_query_statistics_and_reopened_window_replay`. It sets `ZF_SENSOR_MSSQL=1` and a task-owned loopback container (name `ama-sensor110-*`, 3g, 2 CPUs, random process-only password, cleanup in `finally`).
* `WeatherContinuityTests` (5 tests) and `LiveEnvelopeReplayTests` in `src/api/tests/test_sensor_consistency.py`, and `LiveReadingTests` in `src/core/tests/test_sensor_consumer_live.py`, all obtain their store from `store_at(..., reset=True)`. Under `ZF_SENSOR_MSSQL=1` that is an `MssqlStore` after `DELETE FROM cases` on the configured database. They are not selected by the maintained helper, so the documented SQL route does not run them.
* Backend assertion exists only in `SqlHandoverTests` (`consumer.mssql == (ZF_SENSOR_MSSQL == "1")`). The weather, envelope and live classes have none, so a SQLite run could not be told apart from an SQL run in their output.
* `tools/rpi-checks.py` SQL selectors do not include sensor or weather suites and never set `ZF_SENSOR_MSSQL`. `--extra-test` runs under the SQLite unit environment. The maintained FULL gate therefore does not close this gap either. The API README (about lines 1872 and 2068) states that the complete gate does not implicitly include the sensor SQL selector, and its helper description lists only ingestion plus the handover selector.
* A smaller existing versioned route that already covers these classes was looked for and not found.
* The external r6 to r8 wrapper proposals (about 400 lines, never executed) are orchestration evidence only. They are not a substitute for maintainable, versioned regression coverage in the repository.

## Findings and limits

* This is a reproducibility and coverage gap. No runtime bug is claimed or invented. The SQL behaviour of the weather path is simply unobserved.
* Constructed SQL Server evidence, when it exists, would still not be witnessed Azure continuity, calibration, indoor evidence, an approved tolerance, or C1/C2 acceptance.
* Out of scope: schema, consent, calibration, thresholds, new APIs or UI, architecture change, reimplementing working features, new frameworks or constant-only tests.
* Heavy ownership: #188 released it. #185 owns the sole heavy preparation and execution. No heavy run is queued or prepared here, and a free lock grants no permission.
