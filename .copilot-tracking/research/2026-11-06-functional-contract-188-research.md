---
title: Research for #188 independent functional findings F1 and F2
ms.date: 2026-11-06
---

* Research disposition: executed (read-only reading of the independent artifact functional-findings.json, `sensor_consistency.py` `_index`, `_weather_index`, `weather_report`, `sensor_handover_verify.run`, `SensorConsumer._shape`/`_live_shape` seed regex, and `WeatherContinuityTests`). Planning Readiness: Ready. Written and committed before any reproduction or source edit.
* Intake: HEAD 505ad79950ee84e89561b73118b03e7bbcea0f2b, tree c6f6281d709116c49c8021f4479b8121af12cb02, ignored-clean. Main bb3a3b03, declared parent 2dc125f9; no branch movement.
* F1 (static, unreproduced): `_index` (indoor, public core `report`) calls `SensorConsumer._shape(row) is not None` as its schema gate. After the weather work `_shape` dispatches valid live-sim rows to the live shape and returns None, so a valid weather row passes the gate and `row["calibrated"]` raises KeyError instead of ValueError INVALID_HANDOVER_OBSERVATION. The API verifier classifies by schema first and does not reach `report` with weather rows, so the exposure is the direct public core call.
* F2 (static, unreproduced): `weather_report` excludes `scenario` and `seed` from metadata matching but never requires seeds to differ, though the docstring says the seed differs. A copy of the observed window relabelled with the reference scenario yields zero numeric error and passes. The verifier replay writes only after the report returns, so a refusal before replay prevents writes. Seed spellings: the existing regex allows `-0` and `0`, so equivalence must compare parsed integers.
* Limitation: distinct declared seeds do not authenticate independent generator provenance; this stays stated.
* Tier: FULL inherited (sensor/SQL ingestion). This continuation is light source diagnosis only; fresh FULL and independent assessment are coordinator-owned afterwards; the old r14 receipt is historical for the previous head.
* Preserved adverse records: original post-hoc ingest chronology, r13 65/13/3, r14 unauthorized `i188/x` deletion qualification, initial r15 no-run ambiguity, old image all-reports 39 unfixed (37 HIGH, 2 CRITICAL), not security clean.
