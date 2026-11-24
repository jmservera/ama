---
title: Research for issue 2245 (2026-11-24 live run)
ms.date: 2026-11-24
---

Research disposition: executed. Planning Readiness: Ready.

## Findings

* Live revision `ca-cutover-test-demo-api--0000059` (created 2026-11-24T00:14Z, two replicas, Healthy) sets `ZF_DEMO_AI_SUSPENSION_OVERRIDE=owner-directed-2026-11-23`, `ZF_DEPLOYMENT_PROFILE=demo`, `ZF_CHAT_DEMO_ACTIVATION` and `ZF_ENV=production` (names and non-secret values only).
* Live probe (Playwright, desktop 1440x900, Retrofit Programme Manager): 8/8 thread creations 200 (162 to 2283 ms), five asks 200 with `model: workflow-only`, no generative answer; `/api/chat/status` disclaimer says AI answers are on hold; `GET /api/continuity` still lists the open `SYN-221-PROBE` suspension.
* Root cause of the still-rules-only chat: `continuity.demo_owner_override()` in HEAD returns False when `ZF_ENV=production`, and the live demo sets `ZF_ENV=production`. A fix exists only on the sibling local branch (commit `a45523fa7a`, not an ancestor of this branch). Real defect, fix in this run.
* Evidence: `docs/reference/research/issue-2245-live-2026-11-24/`.
