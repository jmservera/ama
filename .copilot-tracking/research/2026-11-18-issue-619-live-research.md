---
title: Issue 619 live demo re-assessment research
ms.date: 2026-11-18
---

## Status

Research opened 2026-11-18. Disposition: executed. Scope: for each unticked criterion of #619 (screen reader, keyboard and zoom testing recorded by a person; resident consent step with a real resident journey; #550 consent before data use; #552 Fluent 2 and WCAG baselines preserved), prove what is provable on the live synthetic demo with the test sign-in, and state why the rest cannot be proven. Desktop only. Owner decisions 2026-11-18: no person-run AT testing, no DPO/Legal approval needed for the demo.


## Evidence gathered

* The protocol [production-ux-acceptance-protocol.md](../../docs/reference/research/ux/production-ux-acceptance-protocol.md) holds scripts A to C and blank record rows; all are `Not run`. Person-run rows stay unfilled by owner decision (not needed for the demo).
* Sibling live notes already cover chat keyboard and announcements (#159), WCAG axe on workbench screens (#151) and sign-in (#349). They are reused, not repeated.
* Live drivers for #619 are under `.copilot-tracking/evidence/2026-11-18/issue-619-live/`: employee case view and chat (keyboard, axe 4.10.3, 200 and 400 percent zoom-equivalent viewports, reduced motion) and the resident consent journey with the synthetic resident account.
* Adverse: the resident demo login limiter (HTTP 429) blocked the first resident runs after earlier cold-start timeouts; retried after the 600 second window.

## Planning Readiness

Ready. Docs and evidence only; no source change; Tier FOCUSED.
