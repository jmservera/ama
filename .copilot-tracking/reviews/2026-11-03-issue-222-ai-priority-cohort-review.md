---
title: Issue 222 AI priority cohort review
ms.date: 2026-11-03
---

## Review

Executed once. Outcome: conformant for the bounded slice; no material findings open.

* The runner never approves; record stays blocked on OQ-018 and synthetic results are not fairness evidence.
* The AI task stays Proposed and leaves ranking unchanged (asserted); the AI-unavailable path falls back to the manual ranking.
* No UI or ranking change; human approval and consent boundaries unchanged.

## Acceptance criteria status

* 1 Unmet: no owner-approved manifest exists.
* 2 Mechanics proven for ranking and AI task (3 seeded exclusions detected); not against an approved manifest, so unmet.
* 3 Mechanics proven (counts reconcile per cohort); not on approved data.
* 4 Mechanics proven (small cohorts insufficient); not on approved data.
* 5 Mechanics proven; approved thresholds and human disposition absent.
* 6 Unmet: OQ-018 owner and DPO approval absent.

## Routed follow-ups

1. Owner approves manifest, fields and thresholds (OQ-018).
2. Held-out, approved AI-task cohort manifest once a live model is authorised.
