---
title: Issue 2191 live pass 4 research
ms.date: 2026-11-23
---

Refs #2191 (closed; PR 2259, 2262, 2268 merged). Read the three earlier research, changes and review records first.

## Findings

* Covered earlier: cohort cap 500, seeded `failure_rate`, core `MAX_CONTROLS`, consent mix, live 222 of 443 cohort, SQL S3 re-proof.
* Uncovered code angle: `infra/live-simulator-job.bicep` param `failureRate` feeds `ZF_SIM_FAILURE_RATE`, but no test pins that wiring or that its default stays inside the simulator's accepted range (`MAX_FAILURE_RATE` 0.9). A rename or a default above 0.9 would make the job refuse to start (`SIM_CONFIG_INVALID`) with no test failing.
* Skip owner-only items; image rebuild and live reprove are not needed for this angle.
* Disposition: Research executed, Planning Readiness Ready.
