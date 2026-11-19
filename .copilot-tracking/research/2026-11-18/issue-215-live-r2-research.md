---
title: Issue 215 live demo research (regulatory alert and home chat UX)
ms.date: 2026-11-18
---

## Opening

Research disposition: executed. Scope: unticked criteria of #215 (WCAG 2.2 AA; staff comprehension) on the live synthetic demo, desktop only. Owner decisions of 2026-11-18 apply (no billing reconciliation, no DPO/Legal approval, no person-run assistive-technology testing).
UI under test: `regulatoryAlertsPanel` and `regulatoryChatPanel` in `src/api/src/zava_forward/api/web/chat.js`. Prior related notes: `docs/reference/research/issue-151-live-wcag-axe-evidence-2026-11-18.md`.
Planning Readiness: Ready. Method: Playwright sign-in as test employee, axe 4.10.3, keyboard walk, plain-language toggle test, no-source and doubt-route observation.

## Findings

* Deployed app `ca-cutover-test-demo-api` has `services.law_alerts` false; `/api/law/alerts` returns 503 unknown. Only the coverage-unknown state is live.
* Regulatory chat is role-gated; the one test employee (Programme Manager) is refused, so the form is disabled live.
* The deployed image predates the repository head for the plain-language announced state.
* A first #215 live run already exists on main (`issue-215-live-alert-chat-ux-evidence-2026-11-18.md`, #1933). Its artifacts were preserved; this run adds a mocked-response proof of populated states.
* Unticked criteria: WCAG 2.2 AA (3a no colour-only, 3b keyboard, 3c plain-language) and staff comprehension.

Planning Readiness: Ready. Source changes: none planned (docs and evidence only, focused tier).
