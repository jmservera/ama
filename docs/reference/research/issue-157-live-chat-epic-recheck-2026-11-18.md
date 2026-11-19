---
title: Per-user chat epic (#157) live re-verification on the synthetic demo
description: Per-criterion record of the open acceptance criteria of epic #157, a fresh live probe of the chat endpoints, and what cannot be proven for the demo
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Synthetic demo, desktop only. Owner decisions of 2026-11-18: live Azure authorised in resource group `ama` (cap USD 700, no drills, no Key Vault rotation, no production change); billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. Credentials were read at runtime from the owner's files and never printed. Nothing was created on Azure; the only write was one refused break-glass request.

## Fresh live observations

Probe: [probe157.py](./issue-157-live-2026-11-18/probe157.py), output [probe157.out.json](./issue-157-live-2026-11-18/probe157.out.json) (owner pseudonym redacted); the signed-in staff app screenshot showed resident names and is not retained. Staff test user signed in through Entra with Playwright at 1440x900.

| Observation | Result |
| --- | --- |
| Running revisions (`az containerapp revision list`) | API `ca-cutover-test-demo-api--0000032` Running/Healthy; resident `ca-resident-demo--0000013` RunningAtMaxScale. Both newer than the 0000031/0000012 recorded earlier today |
| API chat env names | `CHAT_DPIA_REF`, `CHAT_LAWFUL_BASIS_REF`, `CHAT_NOTICE_REF`, `CHAT_RETENTION_REF`, `CHAT_RETENTION_DAYS`, `ZF_CHAT_DEMO_ACTIVATION`; no `CHAT_BREAKGLASS_*` |
| `GET /api/chat/status` | 200; special-category warning, retention `30 days`, `storage_approved` true |
| `GET /api/chat/threads` | 200; the list holds only threads whose owner is the signed-in user |
| `GET /api/chat/threads/not-my-thread-0000` | 404 `Not found.` (no existence leak) |
| `POST /api/chat/breakglass` with a 10+ character purpose | 403 `policy not decided or role not named` |
| `/api/audit-check` before and after that request | intact, 2197 then 2198 entries; one hash-chained entry per refusal |
| `GET /api/chat/regulatory/usage` as a non-assigned user | 403 capability required |
| `GET /api/time/status` | 500 again (draft D1 of the #440 triage, unchanged on revision 0000032; not a chat surface) |

## Per-criterion verdicts for #157

| Criterion | Verdict | Basis |
| --- | --- | --- |
| Complete the #440 stabilization checkpoint | Unproven | #440 has two unticked criteria: issue triage (the four drafts D1 to D4 exist in the [triage note](./stabilization-checkpoint-triage-440-live-2026-11-18.md) but filing them and owner approval of any requirement change, pivot or deferral is a human step) and PR artifacts with an independent review of the coordinator change (a PR step, not available to a local-only task). Merged children cannot satisfy it |
| If accepted, child features are accepted | Unproven | #162 and #164 are open; #159 and #163 are closed. Remaining unticked child items: #159 screen-reader testing (deferred by owner for the demo; keyboard and live-region behaviour recorded in the [#159 note](./issue-159-live-chat-experience-evidence-2026-11-18.md)); #162 granted break-glass with purpose (needs a deployed setting change outside the authorisation, local tests only; refusal and audit proven live above and in the [break-glass note](./chat-breakglass-live-proof-2026-11-18.md)); #164 thresholds approved and the chat task registered with an accountable reviewer (owner approval, no evidence can substitute) |
| Decision accepted or epic closed (ticked) | Not re-opened | ADR 0004 acceptance 2026-10-15 |
| No memory used as evidence for a controlled decision (ticked) | Not re-opened | Merged PR #1552 per the 2026-11-18 ticking comment |
| Chat consumption bounded and reported (ticked) | Not re-opened | Merged PRs #1547 and #1558 |

Result: both open #157 criteria stay unticked. Live evidence for the chat isolation, refusal and audit parts is consistent with the earlier notes; the blockers are owner and process actions, not defects found today.

## Limits

* Only the staff test user was signed in; the resident app was not probed.
* No model turn was run, so no tokens were spent and no grounding claim is refreshed here.
* The 404 on a made-up thread id shows non-disclosure for an unknown id, not a cross-user attempt on a real thread; cross-user denial rests on the earlier role-matrix tests.
