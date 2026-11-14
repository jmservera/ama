---
title: Issue 146 live threshold approval details
ms.date: 2026-11-14
---

* `NON_HUMAN_TOKENS` match whole tokens of the approver string (system, agent, bot, automation, copilot, assistant, ai, llm, service).
* Live codes: `constructed_thresholds_live`, `live_approval_not_named_human`, `live_approval_expired`; none are in `DISPOSABLE`, so a human disposition cannot clear them.
* `expires` is an epoch in the approval block and `now` is caller-supplied; missing `now` fails closed.
