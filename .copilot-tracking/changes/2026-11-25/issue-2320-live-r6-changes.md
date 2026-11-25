---
title: Issue 2320 live r6 changes
ms.date: 2026-11-25
---

Planned (implement-start): edit `src/core/src/zava_forward/core/mssqlstore.py` and `store.py` (bounded write-lock wait for the briefing recording step); add tests; add research note. Tier FULL (src change); `rpi-checks.py --all` not run here.

Done:

* `mssqlstore.py`: `_Conn.write_wait`, `_begin_sql`, `LOCK_WAIT_MS`; `MssqlStore.write_wait`.
* `store.py`: `BRIEFING_WRITE_WAIT_MS = 2000`, `write_wait` no-op, briefing recording wrapped.
* Tests: `core/tests/test_mssql_startup_lock.py` (1), `api/tests/test_assistant_release.py` (1).
* Research note `docs/reference/research/issue-2320-live-r6-2026-11-25.md` with probe, JSON and screenshot.

Validation: `test_assistant_release` 83 OK (15 skipped); `test_mssql_startup_lock` 26 OK; `ruff check` clean; `mypy` in src/core 3 errors identical to baseline. Tier FULL (src change); full gate not run here, the coordinator owns it.

| Criterion | Status |
| --- | --- |
| 1 Profile briefing time | Proven (ticked) |
| 2 Within 5 s, never 503 on a quiet system | Quiet system proven live on 0000070; contention bound proven by code and test only, not live |
| 3 Test proves read path does not take the write lock | Proven for cached read; cache-miss recording takes the lock by design, wait capped at 2 s |
| 4 Live re-check with elapsed times | Proven (ticked) |
