---
title: Plan for #99 slice 2, Finance queue shows the exposure pause signal
ms.date: 2026-11-04
---

* Research: [research](../../research/2026-11-04-investment-envelope-99-research.md) (reused; slice 1 merged as #1078).
* Details: [details](../../details/2026-11-04/issue-99-exposure-screen-details.md).
* Critique: one compatible-findings pass, no conflicts with confirmed decisions (a signal view only; no limits invented, no approval or resume control).
- [x] Phase 1: add `exposureNotice` and call `GET /api/finance/exposure` in the Finance queue view.
- [x] Phase 2: node-executed tests for breach, Held and unavailable states; ruff, mypy, focused unit tests.
* Later slices (not this PR): Board-supplied limits file (human), store persistence of approved limits (needs approval route).
