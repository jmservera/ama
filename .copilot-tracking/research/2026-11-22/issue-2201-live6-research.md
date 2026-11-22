---
title: Issue 2201 live6 research
ms.date: 2026-11-22
---

Disposition: executed. Planning Readiness: Ready.

Task: confirm consecutive receiver successes since 15:00 UTC, capture the exception behind `IOT_CALLBACK_FAILED` if it recurs, re-probe map freshness. Read only; no Azure change, no push.

Findings (evidence in `.copilot-tracking/evidence/2026-11-22/issue-2201-live6/`):

* Receiver `29922660` (15:00) Succeeded; 14:00, 14:30, 15:00 are three consecutive scheduled successes.
* Simulator runs 15:00, 15:07, 15:15, 15:22 all Succeeded.
* No `IOT_CALLBACK_FAILED` since 13:53:41; the handler in `iot_stream.py` drops the exception type, so a capture needs a source change (out of scope).
* Map probe 15:28:56 UTC: 200, 443 items; cases ZF-2025-0030 and ZF-2025-0331 fresh to 15:20:00Z.

Deliverable: `docs/reference/research/issue-2201-live-receiver-streak-2026-11-22.md`.
