---
title: Issue 111 correction cycle c1 changes
ms.date: 2026-11-14
---

Corrects the two findings of the independent review of commit 4e7f7a152 (Refs #111).

* Medium: `reproduce_sensor_analysis()` skips rows with missing or malformed `observed_at` when inferring the default window, and raises `ValueError("NO_VALID_OBSERVATIONS")` only when no row has a valid timestamp; `derive_signal()` then fails closed per row as before.
* Low: `_digest()` now also covers `calibrated`, `source_type` and `schema_version` per row, so flipping `calibrated` changes `input_digest`. `reading_tuples()` keeps its public 5-tuple shape.
* Tests added in `src/core/tests/test_sensor_analysis.py`.
* Validation (targeted only): `tests.test_sensor_analysis` 13 tests OK; ruff check and mypy clean in `src/core`. Full discover and the complete gate were not run.
