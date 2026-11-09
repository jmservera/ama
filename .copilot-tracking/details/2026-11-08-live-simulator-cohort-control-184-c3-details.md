---
title: "Details: #184 correction 3"
ms.date: 2026-11-08
---

* Target: `src/api/checks/sensor_sql_check.py` only, Ruff 0.17.3 project config.
* Evidence: pre/post `ast.dump` hashes, `git diff` line-only review.
* Validation: six files `sensor_sql_check.py`, `live_receiver.py`, `sensor_sql.py`,
  `sensor_consumer.py`, `test_live_control.py`, `test_live_receiver_sql.py`.
* SQL selector: `src/api/checks/sensor_sql_check.py` via a temporary venv that
  points at this worktree; output to separate files under /tmp/c3-*.
