---
title: Issue 891 chat demo plan
description: Plan for remaining #891 criteria
ms.date: 2026-11-07
---

## Phases

* [x] Phase 1: tests for gates with the demo switch on (suspension, privacy refs, retention, call cap).
* [x] Phase 2: make the disclaimer reliably visible; extend the employee chat browser check.
* [x] Phase 3: docs, log, RPI evidence.
* [x] Phase 4: validation (focused tests, browser check, full local gate when the heavy lock is free).
* [ ] Phase 5: live check (blocked, see details).

Critique (one pass, self): the change is minimal, no new dependency, no behaviour change to admission; risk is axe target-size on the composer when the note consumes height, mitigated by a compact 0.8rem note and verified by the browser check. Disposition: applied.
