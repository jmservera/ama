---
title: Issue 2304 round 2 details (2026-11-24)
ms.date: 2026-11-24
---

# Details

* Phase 2: `forecast_reads.py` gets `once(key, read)`; `Assistants.release_reference` uses it only when `db` is a `ForecastReads`.
* Phase 3: in `src/api/tests/test_assistants.py` `ForecastStatements`, patch `ai_registry.tasks` with a counting wrapper and compare 0 and 40 extra cases; assert the count is equal.
* Phase 4: `cd src/api && PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q`; mypy in src/core and src/api.
