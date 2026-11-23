---
title: Details issue 2237 live3
ms.date: 2026-11-23
---

Phase 1: in ErrorLoggingTests, reuse `busy_error`; patch `self.store.audit` with a function that raises once and then delegates to the real audit; request /api/retention as ProgrammeManager twice; expect 503 with Retry-After 5, then 200 with `records`.
Phase 2: copy live probe result and Log Analytics output into docs/reference/research/issue-2237-live3-2026-11-23/.
Phase 3: from src/api run unittest for test_error_logging, `python3 -m mypy`, `python3 -m ruff check` and `format --check`.
