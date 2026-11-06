---
title: Details for #188 functional findings F1 and F2
ms.date: 2026-11-06
---

* Files: `src/core/src/zava_forward/core/synthetic/sensor_consistency.py`, `src/api/tests/test_sensor_consistency.py`, possibly `src/core/README.md` or `src/api/README.md` wording.
* Acceptance: F1 direct core indoor report refuses weather rows with ValueError INVALID_HANDOVER_OBSERVATION; F2 equal declared seeds refused before numeric acceptance and before replay writes; legacy and different-seed weather behavior unchanged; no tolerance, schema, consent, calibration or persistence change.
* Evidence: RED and GREEN raw logs under /tmp/188-functional-contract-r16-1106.
* Not claimed: independent generator provenance, live, indoor calibration, statistical or owner acceptance, FULL on the new head.
