---
title: "Research: #135 Cycle 2 Register audit_entries CI failure"
ms.date: 2026-11-14
task_slug: 135-cycle2-audit-entries
research_disposition: executed
planning_readiness: Ready
---

## Evidence

* CI `src-api` failure: `test_data_operator_ai_state.DataOperatorAiState` raised `AttributeError: 'Register' object has no attribute 'audit_entries'` at `exception_register.py` `_recovery_requests`. The check builds `Register(ai.ai_records())` directly, without a store mixin that provides `audit_entries` (`store.py:127`, `sqlstore.py:1413`).
* The same check expected the old read-only note; the recovery feature changed the screen copy to "Recovery is a recorded, audited human request; nothing is replayed, corrected, re-sent or released automatically."
* `src/api` mypy failed on `tests/test_exception_register.py:184` (no-any-return).
* `src/core/tests/test_exception_register.py` does not exist; core checks use `test_exception_queue.py` and `test_exception_feeds.py` (need `PYTHONPATH=src`, otherwise a stale installed package is imported).
