---
title: Issue 159 live research
ms.date: 2026-11-18
---

Research disposition: executed. Planning Readiness: Ready.

## Scope and findings

Issue #159 has one unticked criterion, "Panel is keyboard operable, screen-reader tested, and announces new messages"; the other six criteria are ticked. Owner decisions of 2026-11-18 make the demo desktop-only and waive person-run assistive-technology testing.

Primary evidence: [docs/reference/research/issue-159-live-chat-experience-evidence-2026-11-18.md](../../docs/reference/research/issue-159-live-chat-experience-evidence-2026-11-18.md) with the Playwright driver, JSON and screenshot under `.copilot-tracking/evidence/2026-11-18/issue-159-live/`.

* Source read: `chat-widget.js` and `chat.js` set `role="log"`, polite live regions, `role="status"`, `role="alert"`, Enter to send, Escape to close with focus return.
* Live probe (keyboard only): launcher reachable, panel opens with focus on heading, question box reachable by Tab, Enter sends, Shift+Enter newline, Escape closes and returns focus, axe 0 violations, announcements recorded in log and status regions.
* Not provable: actual screen-reader speech (waived). Two turns, both workflow-only (0 model calls).

## Open items

Combined criterion stays unticked. Residue: threads deleted; no Azure resource created.
