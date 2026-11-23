---
title: Changes for issue 2245 round 2
ms.date: 2026-11-23
---

Planned: add `test_non_lock_driver_error_on_chat_thread_create_still_answers_500` to `src/api/tests/test_error_logging.py`. Focused tier (test only).

## Done

* Added `test_non_lock_driver_error_on_chat_thread_create_still_answers_500` in `src/api/tests/test_error_logging.py`. `unittest tests.test_error_logging` 13 OK, ruff check and format clean, mypy clean.
* Research note [docs/reference/research/issue-2245-live-r2-2026-11-23.md](../../docs/reference/research/issue-2245-live-r2-2026-11-23.md) with probes. No Azure changes, no throwaway resources.

## Per-criterion table

| Criterion | Status |
| --- | --- |
| No bare 500 on busy lock at thread create | Proven locally; live image lacks fix (500 reproduced) |
| 2026-11-22 cause identified | Partly: ProgrammingError beside a lock-busy 503; unnamed on old image |
| Visible "Model calls: 1" | Unproven: open SYN-221-PROBE suspension, human restart needed |
| Banner states rule-based plainly | Proven |
| Which skills and routes call the model | Proven |
