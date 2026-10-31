---
title: Resident AI activation 563b changes
description: Ledger applied, resident AI enabled and proven live, Refs #563
ms.date: 2026-10-31
---

## Changes

| Change | Detail |
| --- | --- |
| Azure, resident app | New revision ca-resident-demo--0000004 with ZF_DEMO_ASSISTANT_ENABLED=true and ZF_DEMO_ASSISTANT_ENDPOINT=https://aoai-resident-469.openai.azure.com; min0/max1 unchanged; health 200; anonymous assistant call 403 |
| Azure, SQL ledger | resident_ai schema, budget, attempt, reserve and complete created in retrofit by one-off execution job-cutover-test-init-f9vcmzo (Succeeded); budget row started at 0 cents; first execution job-cutover-test-init-yvnsgsp failed before connecting because the override dropped env (no effect) |
| Docs | infra/README.md: ledger apply route and verification note |
| Source | None; no code defect found |

## Live evidence (sanitized, in resident-ai-activation-563b-evidence/)

* Sign-in 1: pest question returned the explicit fallback "AI unavailable: the AI usage check is unavailable" (accounting stage, before any model call).
* Sign-in 2 (after ledger): both questions returned HTTP 200, label "AI-generated", sources collapsed (Sources (3) and (2)), grounded and honest about not confirming the cause. Screenshots attached.
* Live AI attempts to the model: two. Sign-ins used: two of two. Credentials never printed or stored.

## Invariants after the change

Min replicas 0; 8 of 8 jobs Manual; RG ama exists; no new private endpoint, public access or RBAC; employee estate not touched. AI is left enabled: genuine AI answers were observed.

## Not proven

* Human content acceptance (HUMAN-563) and the pre-existing #563 acceptance by a person remain with the owner.
* The full local gate was not run (owner instruction); CI is the evidence.
