---
title: Issue 1238 F3 stale Pending supersede review
ms.date: 2026-11-14
---

## Review

Execution: one pass, self-review of the diff. Outcome: conformant for the F3 criterion, with the open items below routed later.

* Only earlier `Pending` attempts are changed, only on a recorded `Acknowledged` outcome; history, receipt and key are retained.
* In-flight attempts are protected; non-acknowledged retries change nothing.
* The change sits inside the existing outcome operation, so audit and rollback behave as before.

## Routed follow-ups

* Independent exact-head review, human approval and hosted CI remain required.
* Tick F3 on #1238 only after review; PR should use `Closes #1238` only if reviewers agree all criteria are proven.
