---
title: Per-user chat epic (#157) live criteria proof, 2026-11-21
description: Fresh live probe and focused local tests for the per-user chat epic, with a proven or unproven verdict for every acceptance criterion
author: AMA programme
ms.date: 2026-11-21
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Head `f0b278d13`. Issue body and child states read with `gh` on 2026-11-21. Credentials were read at runtime and never printed; the probe redacts they are absent from its output. No Azure resource was created or changed, no model turn ran, and no source changed (focused tier).

## Live observations

Probe: [live_probe.py](../../../.copilot-tracking/evidence/2026-11-21/issue-157-live-20261121T074915Z/live_probe.py), output [live_probe.json](../../../.copilot-tracking/evidence/2026-11-21/issue-157-live-20261121T074915Z/live_probe.json) (owner pseudonym redacted), screenshot [app-signed-in.png](../../../.copilot-tracking/evidence/2026-11-21/issue-157-live-20261121T074915Z/app-signed-in.png). Employee test user signed in through Entra on `ca-cutover-test-demo-api` at 1440 by 900.

| Request | Result |
| --- | --- |
| `/api/chat/status` | 200; special-category warning, retention `30 days`, `storage_approved` true |
| `/api/chat/threads` | 200; one thread, owned by the signed-in pseudonym, 8 messages, from 2026-11-18 |
| `/api/chat/threads/not-my-thread-0000` | 404 `Not found.` |
| `/api/chat/memory` | 200, empty list (memory off) |
| `/api/chat/regulatory/usage` | 403, separate capability required |
| `POST /api/chat/breakglass` | 403 `policy not decided or role not named` |
| `/api/audit-check` before and after | intact; 2687 then 2688 entries (one chain entry for the refusal) |

## Focused local tests

| Command | Result |
| --- | --- |
| `src/core`: `test_chat_memory`, `test_chatthreads`, `test_chat_privacy`, `test_chat_isolation_single_model_route` | 87 tests, OK |
| `src/api`: `test_chat_isolation`, `test_chat_consent_boundary`, `test_home_chat_api`, `test_chat_fixture_roles` | 71 tests, OK |

## Per-criterion verdicts

| Criterion | State on issue | Verdict | Basis |
| --- | --- | --- | --- |
| Complete the #440 stabilization checkpoint | Unticked | Unproven | #440 is open with criteria 7 (triage with owner approval) and 8 (PR artifacts, independent non-worker review, behavior tests of the coordinator) unticked. A local-only run has no PR and no independent reviewer ([#440 verdict](./issue-440-live-criteria-verdict-2026-11-21.md)) |
| If accepted, child features are accepted | Unticked | Partly proven, not provable as a whole | #159, #162, #163 and #164 are all CLOSED. Isolation, retention, consent, bounded calls, refusal and audit are observed live and locally above. Remainders were moved to production trackers #2129, #2142, #2150 and #619 and need person-run assistive-technology testing, DPO and Legal approval, real model checks or competent human exercises, all excluded for the demo. Moved is not proven |
| Decision accepted or epic closed | Ticked | Not reopened | ADR 0004, 2026-10-15 |
| No memory used as evidence for a controlled decision | Ticked | Not reopened | Merged #1552; the memory list is empty live |
| Chat consumption bounded and reported | Ticked | Not reopened | Merged #1547 and #1558 |

## Limits

* Only one staff test account exists, so cross-user denial on a real thread is proven by the local isolation tests, not live; the live 404 shows non-disclosure for an unknown id.
* No model turn ran, so grounding quality and token use are not refreshed.
* Epic stays open; the two unticked criteria are left to the owner.
