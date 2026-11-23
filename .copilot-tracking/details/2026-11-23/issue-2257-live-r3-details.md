---
title: Issue 2257 r3 details
ms.date: 2026-11-23
---

* `src/core/src/zava_forward/core/assistants.py`: import `is_write_lock_busy`; in the `sensors_for_map`-style except block append ` cause=sql-write-lock-busy` to the warning when it matches.
* `src/api/tests/test_map_sensors.py`: a transaction that raises a `pyodbc` `ProgrammingError` containing the lock text yields state `unavailable`, the cause tag, and no driver text in the log.
