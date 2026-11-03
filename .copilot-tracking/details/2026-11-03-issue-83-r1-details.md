---
title: Issue 83 r1 details
ms.date: 2026-11-03
---

* P01: `src/core/src/zava_forward/core/workflows.py`; visible to sender, recipient and managers as `pending_handoffs`.
* P02: `src/core/src/zava_forward/core/exception_feeds.py`; kind `stranded_task`, ref `handoff:<case>:<date>`.
* P03: `tests/test_handoff_lifecycle.py` (JSON and SQLite), `tests/test_exception_feeds.py`.
* AI-unavailable and manual paths: no AI involved; escalation remains the existing manual manager action.
