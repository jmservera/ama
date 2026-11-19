---
title: Research, issue 344 seventh live pass
ms.date: 2026-11-19
---

Refs #344. Disposition: executed (new live probes). Planning Readiness: Ready.

Prior evidence: r5 and r6 notes. Remaining unticked criteria: 1, 3, 4, 5. Candidate buildable item: criterion 4 (SQL private) and the non-browser halves of 1 and 3 can be re-proven live read-only; Return401 for browsers is an infra change (FULL tier, owner decision) and the `/api/time/status` fault is SQL-scope (FULL tier). No src change is planned.
