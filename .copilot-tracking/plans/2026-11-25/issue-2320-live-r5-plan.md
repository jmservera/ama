---
title: Issue 2320 live r5 plan
ms.date: 2026-11-25
---

* [x] Phase 1 Research: live probe on 0000069 and root cause (done).
* [ ] Phase 2 Implement: in `Store.briefing`, catch a write-lock-busy error from the recording step and return a stale cached or read-only template answer naming that it was not recorded; add one test in `src/api/tests/test_assistant_release.py`; run src/core and src/api targeted tests, mypy, ruff.
* [ ] Phase 3 Review: single review; record criteria table. Live re-proof of the fix is not possible without deployment (no push).

Details: [details](../../details/2026-11-25/issue-2320-live-r5-details.md). Critique: [critique](../../critique/2026-11-25/issue-2320-live-r5-critique.md).
