---
title: IoT threshold advisory plan
ms.date: 2026-11-14
---

Tier: focused (additive read-model field, no gate-semantic change). Critique: executed once inline, verdict compatible, no conflicts.

* [x] Add `sensor_view.advisory()` and attach as `advisory` in `view()` only (not `capture_source`).
* [x] Text label "Sensor watch" plus framing "inspection required before changing case status"; no aria attributes, no state mutation.
* [x] Add `src/api/tests/test_iot_threshold_advisory.py` (7 unit tests).
* [x] Validate: targeted tests, accessibility baseline, quality sensor tests, mypy, ruff.
