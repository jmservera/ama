---
title: Issue 1288 live r15 research
description: Opening research record for the fifteenth Quality sensor evidence pass
ms.date: 2026-11-26
---

## Scope

Synthetic demo, desktop only. Goal: prove each unticked criterion (3 to 8) with recorded evidence or record why not. Research disposition: executed (reuses r12 to r14 audits; new fact since r14 is that #107 recorded five release records in force on 2026-11-25).

## Opening questions

* Do the Quality release record and call allowance now permit a bounded live model call?
* Does the retained source still hold for criteria 3, 5, 6, 7 locally?

Planning Readiness: pending (updated below after the live probe).

## Findings (2026-11-26, live read-only probe, evidence in evidence/2026-11-26/issue-1288-live15/)

* Revision `ca-cutover-test-demo-api--0000079`. `GET /api/assistants`: all assistants `release: "in force"` (five records from #107 r14), binding deployment `standard`, model `gpt-4.1-nano-2025-04-14`.
* App env carries `ZF_ASSIST_QUALITY_DEMO_HOMES` (five exact homes), `ZF_ASSIST_RELEASE_APPROVERS` and `ZF_DEMO_AI_SUSPENSION_OVERRIDE` (owner-directed 2026-11-23). It carries none of `ZF_ASSIST_AUTHORITY`, `ZF_ASSIST_EXPIRES`, `ZF_ASSIST_CALL_ALLOWANCE`, `ZF_ASSIST_TOKEN_ALLOWANCE`, `ZF_ASSIST_PROACTIVE`. So the release blocker of r14 is gone; the remaining blocker is the finite operator allowance, a documented environment setting (src/agents/README.md).
* `rai-metrics`: invocation 3, tokens 0, fallback 20 (no real model consumption). `forecast` returned 503 (timeout) on this probe.

## Decision

The allowance is a finite-cost control inside the USD 700 live authorisation of 2026-11-18, so a minimal one (10 calls, 200000 tokens, expiry now+3h, proactive on, scoped to the five demo homes) is set on the demo API, used for one bounded walkthrough, then removed (new revision). No role, network, key or budget change.

Planning Readiness: Ready.
