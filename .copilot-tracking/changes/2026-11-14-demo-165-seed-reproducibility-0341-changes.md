---
title: Epic 165 seed reproducibility changes
ms.date: 2026-11-14
---

## Added

* `src/core/tests/test_epic165_deterministic_reproducibility.py` (9 tests).

## Validation

* unittest: 9 tests OK. ruff check and format check: pass. mypy: no issues.
* Not run: full local gate and hosted CI (Focused tier).

## Divergence

* No PAS 2035 generator exists; the scale fixture case events stand in (see research).
