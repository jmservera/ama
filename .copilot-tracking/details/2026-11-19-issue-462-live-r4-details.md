---
title: Issue 462 live r4 details
ms.date: 2026-11-19
---

## Phase 1

File `src/core/src/zava_forward/core/resident_preview.py`, `safe_start`. Add `marker_id = dataset_marker.get("fixture_id")` and `fixture_id = fixture_meta.get("id")`; refuse unless both are `str`, non-blank, and equal. Keep the same `PreviewConfigError` message. Reject before touching other state; no behaviour change for valid pairs.

## Phase 2

File `src/core/tests/test_resident_preview.py`, class `SafeStart`: new test mutating a copy of the dataset marker and the fixture file so ids are absent, null, empty, whitespace or non-string, including both sides missing together (the reviewed case).

## Phase 3

`cd src/core && python3 -m unittest` for the module; `python3 -m mypy` in `src/core`; `ruff check` and `ruff format --isolated --line-length 100 --check` on touched files; run `src/api/tests/test_resident_preview_api.py` as a consumer check.
