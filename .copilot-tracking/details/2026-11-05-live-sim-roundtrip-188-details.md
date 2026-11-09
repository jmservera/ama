---
title: Details for #188 live-sim retained round-trip repair
ms.date: 2026-11-05
---

* Phase 1, tests first: `src/core/tests/test_sensor_consumer_live.py` (lossless envelope, replay, mixed schemas, projection excludes live, controls still reject), `src/core/tests/test_sensor_analysis_store.py` (weather-only and mixed windows), `src/api/tests/test_sensor_consistency.py` (verifier replay with a live row).
* Phase 2, code: `sensor_consumer.py` (`retained_envelopes`, `observed_series` filter), `sensor_analysis_store.py` (partition and reason), `sensor_handover_verify.py` (replay source).
* Phase 3: ruff, mypy, focused tests; write changes and review artifacts; commit with evidence.
