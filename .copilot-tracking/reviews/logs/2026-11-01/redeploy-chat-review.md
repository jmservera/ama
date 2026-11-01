---
title: Redeploy chat changes from main 398e846fd, review
ms.date: 2026-11-01
---

Review executed once (parent, evidence read-back). Outcome: Deployment conformant; one functional defect routed.

* Deployment gates met: backups taken first, constraints kept, registry restored identically, `CHAT_*` preserved and applied, health green, no rollback.
* Open finding routed to later work: #749 (stored employee chat has no rules-based case grounding when AI is unavailable). Not fixed in this task.
* Observations not filed: resident sensors card is empty because the sensor tables hold no rows; employee `GET /api/chat/regulatory/status` 403 for the test role; the chat reply never says "saved/stored".
* Human review boxes remain unchecked: owner review of this PR is required.

## Follow-ups (ranked)

1. Fix #749 by adding the rules-based grounding to the stored ask path (high value, small change, reuses #743 code).
2. Make the employee chat reply or status say when a turn is saved with retention (low effort, clarity).
3. Decide whether synthetic sensor rows should be loaded for the demo resident (owner decision, data change).
