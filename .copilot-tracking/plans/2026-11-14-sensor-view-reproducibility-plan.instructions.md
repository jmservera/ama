---
title: Sensor view reproducibility plan (Refs #111)
ms.date: 2026-11-14
---

* [x] Add `ANALYSIS_VERSION`, `rows_digest`, `reproducibility` to `sensor_view.py`; wrap `view()`.
* [x] Trend carries its own `input_digest` so trend rows are covered by the input digest.
* [x] Core unit tests: `src/core/tests/test_sensor_view_reproducibility.py`.
* [x] API tests in `src/api/tests/test_sensor_trend_summary.py`: shuffled insertion order, repeats, changed readings and `as_of`, payload exposure.
* [x] Validate: per-project `ruff check`, `ruff format --check`, bare `mypy` (src/core, src/api); focused unittest including `test_accessibility_baseline`.
* Critique (single pass): compatible; output digest sorts reading lists, keeps `as_of` inside, excludes the digest block itself.
* Validation tier: focused (non-gate, additive read-model field, no web, workflow or dependency change).
