---
title: Resident AI activation 563b research
description: Root cause of the resident AI fallback and the safe activation path, Refs #563
ms.date: 2026-10-31
---

## Research Brief

* Task: 563b (`resident-ai-activation-563b`), branch ops/resident-ai-activation-563b, base origin/main 6ae70d43.
* Authority: owner "yes, approve" at 2026-10-31T21:52Z to diagnose, fix, redeploy and enable resident AI with at most two live AI attempts and rollback if no genuine AI answer.
* Research disposition: executed. Planning Readiness: Ready.

## Evidence

| ID | Finding | Source |
| --- | --- | --- |
| E1 | Prior fallback label (2026-10-30) was generic; current main labels each reason, so a live attempt names the failing stage | src/api/src/zava_forward/api/resident_demo/aoai.py FALLBACK_REASONS |
| E2 | Resident app redeployed from main 6ae70d43 at 18:03Z with assistant variables absent, min0/max1, jobs Manual | az containerapp show, 2026-10-31 |
| E3 | Enabling the two variables (ZF_DEMO_ASSISTANT_ENABLED, ZF_DEMO_ASSISTANT_ENDPOINT) and one consented pest question returned "AI unavailable: the AI usage check is unavailable" (accounting_unavailable, raised before any token or model call) | attempt1-sql-ledger-missing.json |
| E4 | Accounting runs `EXEC resident_ai.reserve`; infra/README.md says an Entra SQL admin must apply infra/sql/resident-assistant.sql first; no tracked evidence shows it was ever applied | infra/README.md, tracking search |
| E5 | SQL is private (public access Disabled); the only Entra admin is id-cutover-test-init, reachable through the existing Manual init job | az sql server show, ad-admin list |
| E6 | A read-only probe inside that job showed schema, tables and both procedures absent while the id-resident-demo user and SID matched | private-job-log.txt |

## Conclusion

Root cause is operational: the resident_ai accounting ledger was never applied to the retrofit database, so every enabled request failed closed at reservation. No source defect was found; the earlier 2026-10-30 fallback is consistent with this (the old label hid the stage). Alternatives not supported: timeout, role propagation, endpoint or deployment mismatch, payload size.

## Planning Readiness

Ready. Smallest safe action: apply the reviewed SQL once through a one-off run of the existing init job (no config change), then use the two permitted live attempts.
