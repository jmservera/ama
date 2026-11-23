---
title: Research, issue 1259 live run 8
ms.date: 2026-11-23
---

Research disposition: executed. Planning Readiness: Ready.

Findings on main f87d86da00:

* The fix (`_require_creatable`, `_names` in `ranking_publication.py`) and `UnusableArchivePathTests` already exist; ACs 1-3 are ticked.
* Head: 110 tests pass. Pre-fix `cd687abadd^` with current tests: 7 failures.
* Gap: the stat-failure scenario only mocks `os.stat`; no real-filesystem permission denial test exists. A 0-mode parent makes `lstat` raise PermissionError, which must be unknown, not creatable.
* Pre-fix with the proposed real-permission test: `('due', True) != ('problem', None)` (fails, as required).
* Live Azure: ranking runner is an operator CLI, no deployed job; nothing to prove live. No Azure resource touched.
