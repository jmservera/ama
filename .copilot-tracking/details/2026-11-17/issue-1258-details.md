---
title: Issue 1258 plan details
ms.date: 2026-11-17
---

## Phase 2: evidence outcome

* No file under `src/` changes.
* Record measurements in the changes file.

## Phase 3: validation

* From `src/core` with `PYTHONPATH=src`: `python3 -m unittest discover -s tests -p 'test_ranking_publication.py' -q`.
* `ruff format --isolated --line-length 100 --check src tests` and `mypy` from `src/core` (no source change; run for the record).
