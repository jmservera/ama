---
title: Issue 2202 live details 2026-11-25
ms.date: 2026-11-25
---

Phase 2: in `src/core/src/zava_forward/core/assistants.py`, replace `with self.transaction() as db:` in `sensors` and `map_sensors` with `with self._read_connection() as db:`. `authorize`, `now`, `sensor_view.view` and `sensor_map.summaries` only read. Test: in `src/api/tests/test_map_sensors.py`, patch `transaction` to raise and assert both calls still answer.
