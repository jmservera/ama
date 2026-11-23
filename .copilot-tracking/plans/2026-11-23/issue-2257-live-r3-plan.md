---
title: Issue 2257 r3 plan
ms.date: 2026-11-23
---

* [x] Live re-probe, 10 fresh sessions (done).
* [ ] Tag the sensor overlay warning with `cause=sql-write-lock-busy` when `is_write_lock_busy` matches; add one test in `src/api/tests/test_map_sensors.py`.
* [ ] Run `src/api` map sensor tests, `test_error_logging`, and mypy/ruff for `src/core` and `src/api`.
* [ ] Research note, README index row, log entry, changes record with per-criterion table, review.

Details: `.copilot-tracking/details/2026-11-23/issue-2257-live-r3-details.md`. Tier: FULL (src change); no `--all` run here.
