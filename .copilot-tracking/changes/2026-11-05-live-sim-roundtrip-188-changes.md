---
title: Changes for #188 live-sim retained round-trip repair
ms.date: 2026-11-05
---

* Modified `src/core/src/zava_forward/core/sensor_consumer.py`: new `retained_envelopes` (lossless; live rows are the original 16-field witness, no `calibrated`); `observed_series` now returns only indoor-contract rows and excludes live rows.
* Modified `src/core/src/zava_forward/core/sensor_analysis_store.py`: `analyse_retained` uses envelopes, drops live-sim rows from indoor analysis, and returns INSUFFICIENT with `WEATHER_INPUT_NOT_INDOOR_MEASUREMENT` when only such rows exist.
* Modified `src/api/src/zava_forward/api/sensor_handover_verify.py`: replay check re-ingests `retained_envelopes`; the report still uses `observed_series`.
* Tests: `test_sensor_consumer_live.py` (lossless round-trip and replay, mixed schemas, consent/calibration/mapping rejections, unwitnessed row diagnostic), `test_sensor_analysis_store.py` (mixed and weather-only windows), `test_sensor_consistency.py` (verifier replay with a live row). READMEs in core and api updated.
* Reproduction before the change (head 78ecffc95): replay of the old projection was `rejected/SCHEMA`; `analyse_retained` gave `SCHEMA_FIELDS` coverage reasons. Both now resolved.
* Validation run (no SQL Server, browser, build or gate): core `test_sensor_consumer_live`, `test_sensor_analysis_store`, `test_sensor_consumer`, `test_live_readings` (74 OK); api `test_iot_stream`, `test_live_simulator`, `test_sensor_consistency`, `test_sensor_ingestion` (153 OK); ruff check and format and mypy clean for src/core and src/api (cache /tmp/mypy-188).
* Divergence: none from plan. Behaviour change to note: `observed_series` no longer returns live rows (the prior slice's join test now uses `retained_envelopes`).
* Not changed: schema versions, sunlight, units, calibration logic, admission controls, hazard thresholds.
* Complete (FULL) gate: pending. Original failed receipt `/tmp/rpi188-full-20261105T0740/receipt.json` is preserved untouched. Prior gate/test mismatch is dependency-blocked on #1208; the heavy lock is held by #96. No gate, partial group pass or historical control is claimed as acceptance.
