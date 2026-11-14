---
title: Issue 104 approval claim filter plan
ms.date: 2026-11-14
---

## Plan

* [x] Phase 1: extend `FORBIDDEN` with first-person and passive approve/update/change claims; keep plain past-tense recorded status allowed.
* [x] Phase 2: add focused tests in `src/agents/tests` (filter and `Ai.run` fallback) and `src/api/tests` (no meter, no token, no socket).
* [x] Phase 3: validate with ruff, mypy, targeted agents, api and core tests.

Details: [details](../details/2026-11-14-104-approval-claim-filter-0003-details.md). Critique: single pass, no conflicts; tightening is narrowly worded to protect grounded status reports.
