---
title: Sensor view reproducibility changes (Refs #111)
ms.date: 2026-11-14
---

## Changes

* `src/core/src/zava_forward/core/sensor_view.py`: `ANALYSIS_VERSION`, `rows_digest`, `reproducibility`; `view()` adds `reproducibility`; trend adds `input_digest`.
* `src/core/tests/test_sensor_view_reproducibility.py`: new unit tests.
* `src/api/tests/test_sensor_trend_summary.py`: shuffled-arrival, repeat and API-payload tests.

## Validation (PYTHONDONTWRITEBYTECODE=1, stdin from /dev/null, no uv)

* `ruff check`, `ruff format --check`, bare `mypy` in `src/core` and `src/api`: clean.
* Worktree sources were selected with PYTHONPATH for unittest only because editable installs point at another checkout; mypy ran unmodified.
* Unittest: core view reproducibility and analysis reproducibility; api trend summary, consistency, accessibility baseline, non-authority boundary, quality sensors, ingestion: all pass (skips are SQL Server only).
* Not run: full local RPI gate, hosted CI, SQL Server.
