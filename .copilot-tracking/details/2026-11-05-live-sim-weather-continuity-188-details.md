---
title: Details for #188 synthetic weather continuity
ms.date: 2026-11-05
---

* Phase 1 tests: `src/core/tests/test_live_readings.py` (scenario default unchanged, reference scenario), `src/core/tests/test_sensor_handover.py` or new focused class for `weather_report` bounds and rejections, `src/api/tests/test_sensor_consistency.py` (verifier weather pass, rejects, idempotent rerun, legacy).
* Phase 2 code: `live_readings.py`, `sensor_consistency.py`, `sensor_handover_verify.py`.
* Phase 3: docs, lint/type, focused tests, changes and review artifacts, commit.
