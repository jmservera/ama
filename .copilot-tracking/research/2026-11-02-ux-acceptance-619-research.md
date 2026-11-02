---
title: Research for issue 619 production UX acceptance
ms.date: 2026-11-02
---

## Disposition

Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Issue 619 requires screen reader, keyboard and zoom testing recorded by a person and a consent step proven with a real resident journey (production phase). These cannot be produced by an agent.
* Engineering coverage exists: `chat_widget_browser_check` (320/390/1280 reflow, focus, axe, consent, reduced motion), `case_view_ux_browser_check`, `test_accessibility_baseline`, resident consent gate in `resident_demo/app.py` and `assistant.js`.
* `wcag-conformance-baseline.md` records all manual rows as Not run and gap G-1; no protocol covered the chat widget, the case view or the resident consent journey.

## Slice

Document-only: protocol, blank human record and criterion status; a guard test that record cells stay Not run or name tester and date; index, log and baseline links. No web files change, so web-design-guidelines fetch was not applicable.

## Follow-ups

1. Person-run rows (owner names testers, O-3).
2. DPO and Legal approval for real-resident testing.
3. Owner confirms target level (O-1).
