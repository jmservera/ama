---
title: Research for #188 live-sim retained round-trip
ms.date: 2026-11-05
---

* Research disposition: executed (source reading plus a focused reproduction at head 78ecffc95). Planning Readiness: Ready.
* Trigger: independent #110 same-audit review found a source-visible incompatibility after the live-sim-reading-v1 admission (c9a14573d). Admission is not duplicated here.
* Reproduced (SQLite, worktree sources, `SensorConsumer` plus `sensor_analysis_store`): a live row is accepted; `observed_series` returns it as a 15-key hybrid (live schema_version, `calibrated=true`, sunlight, no `label`, no `injected_fault`); feeding that row back to `process` is `rejected/SCHEMA` (`_live_shape` needs the exact 16 fields); `analyse_retained` over a window holding only that row returns INSUFFICIENT with the non-diagnostic reasons `DAY_COVERAGE`, `NIGHT_COVERAGE`, `SCHEMA_FIELDS`, `WINDOW_COVERAGE`.
* Consumers of `observed_series`: `sensor_handover_verify.run` (report plus `--replay-check` re-ingestion) and `sensor_analysis_store.analyse_retained` (indoor hourly comparator). `sensor_consistency._index` also needs `calibrated` and the closed 13-field shape, so a live row cannot enter the backfill comparison either.
* Defects in the projection: it drops `label` and `injected_fault`, and it invents `calibrated=true` for a schema that has no calibration flag. The latter makes a logical marker look like calibration evidence.
* Domain boundary: live-sim rows carry temperature, humidity and sunlight from a climate-shaped outdoor source tied to a home. They are not indoor measurements, so the indoor hourly analysis must not use them and must say why. A weather-to-indoor model needs separate versioned approval and is excluded.
* Unchanged controls: consent, mapping interval, clock window and configured calibration interval are enforced in `_retained_reading`/`_decide` for live rows already and the replay negative cases stay.
* Not run: full gate (dependency-blocked, see plan), SQL Server, browser, any Azure resource. No private dataset was read.
