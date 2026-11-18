---
title: Sensor view reproducibility research (Refs #111)
ms.date: 2026-11-14
---

## Scope

Issue #111 criterion 1, "Outputs are reproducible from retained readings", stacked on #1641 at `eb1c3f35e`.
Disposition: executed. Planning Readiness: Ready.

## Findings

* `sensor_analysis.py` already exposes `ANALYSIS_VERSION` and a row-order-independent `input_digest`; `test_sensor_analysis_reproducibility.py` proves it for the analysis and review-task candidate.
* The employee/API read model `sensor_view.view()` (served by `Assistants.sensors` and the `/sensors` route in `server.py`) exposed no analysis version or digest, so summary, advisory watch and trend outputs were not provably reproducible.
* `capture_source` feeds quality snapshot digests and must not change; only `view()` output may gain a key.
* Retained `_select` sorts rows, but ties and storage order are not documented guarantees, so digests canonicalise by `(sensor_id, reading_id)`.

## Decision

Add a `reproducibility` block (`analysis_version`, `as_of`, `input_digest`, `output_digest`, `reading_count`) to `view()` only. Exercise values, not an operational rule; R1 to R3 approval and SQL Server flow remain unproven.
