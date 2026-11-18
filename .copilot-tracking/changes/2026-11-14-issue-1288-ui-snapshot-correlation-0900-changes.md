---
title: Issue 1288 UI and snapshot correlation changes (0900)
ms.date: 2026-11-14
---

## Changes

* Added `src/api/tests/test_quality_sensors_correlation.py` (11 focused tests; 18 run including inherited base cases).
* No production source changed.

## Validation (local)

* New module: 18 tests OK. Existing `test_quality_sensors` 191 OK (94 MSSQL skipped); c7/e1/e2 239 OK (85 skipped).
* `ruff check --no-cache` and `ruff format --check --no-cache` clean; `mypy --cache-dir /tmp/mypy-1288` from `src/api`: no issues in 264 files; cache removed.
* Not run: Chromium browser check (profile socket path too long in this worktree), MSSQL variants, live walkthrough (criterion 8 remains a separate gate).
