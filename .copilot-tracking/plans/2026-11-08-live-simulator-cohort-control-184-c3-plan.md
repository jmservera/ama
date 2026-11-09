---
title: "Plan and details: #184 correction 3"
ms.date: 2026-11-08
---

Critique: executed once; compatible (formatting only, no behavior change).

* [ ] 1. Save pre-format AST dump hash of `src/api/checks/sensor_sql_check.py`.
* [ ] 2. `python3 -m ruff format --no-cache src/api/checks/sensor_sql_check.py` only.
* [ ] 3. Compare AST equality and diff (line-wrapping only); no other file edits.
* [ ] 4. Run the six-file `ruff format --check` and `ruff check`, focused unit
  tests, and prove other inputs unchanged with `git diff --name-only`.
* [ ] 5. Non-queued `flock -n /tmp/ama-rpi-heavy.lock` SQL selector after
  checking holder, CPU, memory and disk; defer if busy. Separate stdout,
  stderr and exit files.
* [ ] 6. Changes and Review artifacts, commit.

Out of scope: sensor_consumer.py, the Low test gap, Azure, models, push.
