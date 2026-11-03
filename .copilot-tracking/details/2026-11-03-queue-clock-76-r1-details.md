---
title: Issue 76 round 1 details
ms.date: 2026-11-03
---

* `taskqueues.timing(due, done, now)` returns Completed, Overdue, Open or Unknown from recorded values only; it is not a statutory calculation.
* `owner_status` names no one when the owner is Unknown; it points to the case owner to record one through the existing hazard service.
* UI: `workSummary` in `src/api/src/zava_forward/api/web/app.js` appends the owner status and both states to the existing clock paragraph (plain text, no colour-only status).
* Human approval unchanged: nothing here assigns, classifies, closes or restarts work. AI is not involved, so no AI-unavailable path applies.
