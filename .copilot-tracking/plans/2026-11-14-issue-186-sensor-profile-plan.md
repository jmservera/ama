---
title: Issue 186 plan
ms.date: 2026-11-14
---

## Scope

* Add `PortfolioProfileTests` to `src/core/tests/test_indoor_projection.py`: determinism (seed and config), envelope bounds for 24 homes, archetype and weather coupling, and domain rejection. No production code change.

## Validation

* `python3 -m ruff check`, `ruff format --line-length 100 --check`, `unittest tests.test_indoor_projection`, `test_sensor_backfill`, `test_synthetic_determinism`.
* Tier: focused (test-only). Commit locally, no push, no `.pyc`.
