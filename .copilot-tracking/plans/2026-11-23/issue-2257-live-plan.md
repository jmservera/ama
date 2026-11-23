---
title: Issue 2257 live plan
ms.date: 2026-11-23
---

1. Guard `AssistantService.map_sensors` so a transaction failure returns `fixed("unavailable")` per home and logs the exception class (src/core `assistants.py`).
2. Add one test in `src/api/tests/test_map_sensors.py`: a failing transaction keeps `/api/map` 200 with sensor state `unavailable`.
3. Run `test_map_sensors`, mypy for core, ruff for changed files; record the per-criterion table.
4. Tier: FULL by rule (src change); coordinator runs the gate, not this worker.
