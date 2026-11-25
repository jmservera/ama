---
title: Issue 2320 live r5 details
ms.date: 2026-11-25
---

Phase 2 details: in `src/core/src/zava_forward/core/store.py` wrap the `ai_tasks.run_text_task` call and the following `self.audit` in `try/except Exception as exc`; if `mssqlstore.is_write_lock_busy(exc)` is false, re-raise. Otherwise return the cached entry for `key` (any version) with `reason` replaced and `recorded=False`, or a template answer built from `tmpl`, `top` and `candidates` with `recorded=False`. Do not cache the fallback. Test: busy error on `store.audit` and a version bump; assert source `template`, `recorded` False, no raise, and that a later call without the fault records normally.
