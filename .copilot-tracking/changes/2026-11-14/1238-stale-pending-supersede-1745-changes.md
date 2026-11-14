---
title: Issue 1238 F3 stale Pending supersede changes
ms.date: 2026-11-14
---

## Changes

* `src/core/src/zava_forward/core/resident_decisions.py`: `_supersede_stale_pending` marks earlier idle `Pending` attempts `Superseded` (`superseded_from`, `superseded_at`, `superseded_by`) when a later attempt is `Acknowledged`.
* `src/core/tests/test_resident_decisions.py`: updated one expectation, added three tests.

## Validation

* `PYTHONPATH=src:tests TMPDIR=/dev/shm/zf-tmp python3 -m unittest test_resident_decisions -k pending -k supersede -k forward -k retry -k outcome`: 128 tests OK (44 opt-in SQL Server skipped).
* `ruff check` and `mypy` on the changed module: clean.
* Not run: full gate and `unittest discover` (excluded by instruction); hosted CI not observed; nothing pushed.
