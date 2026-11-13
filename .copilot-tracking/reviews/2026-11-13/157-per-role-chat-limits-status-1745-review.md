---
title: Issue 157 per-role chat limits review
ms.date: 2026-11-13
---

Independent code-review executed once. One medium finding: the turn count was read before the lock, so concurrent asks could pass the cap. Fixed by re-reading the thread inside `store.lock`; chat_panel tests, ruff and mypy re-run clean. Outcome: conformant after fix; no open findings.
