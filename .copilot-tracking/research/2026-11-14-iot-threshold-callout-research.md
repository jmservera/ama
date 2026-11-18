---
title: IoT threshold advisory research
ms.date: 2026-11-14
---

Refs #165, #1288, #111. Disposition: executed. Planning Readiness: Ready.

* `sensor_view.view()` returns the bounded retained-reading read model (latest reading, freshness) used by the employee screen and Quality snapshot. Reading values are strings; no threshold or watch indicator was exposed.
* `sensor_analysis.AnalysisPolicy` already holds an exercise humidity threshold (75 %RH, label "EXERCISE VALUE"); it is not exposed in the view.
* `sensor_status_text` serves resident-facing text separately and is untouched.
* `capture_source` feeds the model digest, so an additive field belongs in `view()` only, keeping digests unchanged.
* Existing boundary tests (`test_sensor_non_authority_boundary.py`) prove sensors never change hazard or case state.
* Thresholds (75 %RH, 16 degC) are exercise values, not a sourced standard.
