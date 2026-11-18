---
title: Issue 215 live demo proof research
description: Research record for the live proof of regulatory alert and home chat UX criteria
ms.date: 2026-11-18
---

## Disposition and readiness

Research disposition: executed. Planning Readiness: Ready.

## Scope

Issue #215 unticked criteria: (3) WCAG 2.2 AA behaviours (no colour-only status, keyboard operable, plain-language mode); (5) comprehension with staff. Targets: `ca-cutover-test-demo-api` and `ca-resident-demo`, desktop 1366x900, read-only Azure.

## Findings

* Demo `services.law_alerts` is false and `/api/law/alerts` returns 503 unknown, so no alert card can render live; only the explicit unknown state is observable.
* Alerts panel unknown state, hazard-first notice and doubt owner text observed; axe 0 violations on the panel and the chat dialog.
* Keyboard operation of the toggle, Refresh, chat launcher open (Enter) and close (Escape) observed.
* Deployed plain-language toggle has no visible effect in the unknown state and no announced state; the repository source has an announced state span, so the image predates repository head.
* Staff comprehension needs real participants; not provable on a synthetic demo.
* Source code under `src/` is not in scope; FOCUSED tier, documentation and evidence only.

## Evidence

Research note [issue-215-live-alert-chat-ux-evidence-2026-11-18.md](../../../docs/reference/research/issue-215-live-alert-chat-ux-evidence-2026-11-18.md); raw files in `.copilot-tracking/evidence/2026-11-18/issue-215-live/`.
