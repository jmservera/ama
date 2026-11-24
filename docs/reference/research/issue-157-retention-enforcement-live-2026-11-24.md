---
title: Per-user chat epic (#157) retention enforcement and live recheck, 2026-11-24
description: Live probe, a retention enforcement defect fixed in core, and a proven or unproven verdict for every acceptance criterion
author: AMA programme
ms.date: 2026-11-24
ms.topic: reference
---

## Scope

Synthetic demo, desktop only. Owner decisions of 2026-11-18 apply. Head `3adf3f4698`. Issue and child states read with `gh` on 2026-11-24. Credentials were read at runtime and never printed; the probe redacts them. No Azure resource was created or changed and no model turn ran. Full tier applies because `src/core` changed; the coordinator runs the gate.

## Live observations

Probe: [live_probe.py](../../../.copilot-tracking/evidence/2026-11-24/issue-157-live-20261124T035902Z/live_probe.py), output [live_probe.json](../../../.copilot-tracking/evidence/2026-11-24/issue-157-live-20261124T035902Z/live_probe.json), screenshot [app-signed-in.png](../../../.copilot-tracking/evidence/2026-11-24/issue-157-live-20261124T035902Z/app-signed-in.png). Employee test user signed in through Entra on `ca-cutover-test-demo-api`, revision `--0000059`, Healthy, traffic 100, at 1440 by 900.

| Request | Result |
| --- | --- |
| `/api/chat/status` | 200; special-category warning, retention `30 days`, `storage_approved` true |
| `/api/chat/threads` | 200; threads owned by the signed-in pseudonym only |
| `/api/chat/threads/not-my-thread-0000` | 404 `Not found.` |
| `/api/chat/memory` | 200, empty list (memory off) |
| `/api/chat/regulatory/usage` | 403, separate capability required |
| `POST /api/chat/breakglass` | 403 `policy not decided or role not named` |
| `/api/audit-check` before and after | intact; 8891 then 8892 entries |

## Defect found and fixed

The advertised 30-day retention was never enforced while the app ran: `ChatPrivacy.purge_retention` had no caller outside tests (`grep -rn purge_retention src tools infra .github`), and the [storage approval](./chat-demo-storage-approval-2026-11-01.md) recorded that no scheduler runs it. Separately, `add_memory` counted expired but unpurged memory toward the 50-item limit while `list_memory` hid it, so a user could be refused with fewer than 50 visible items.

Fix: `ChatPrivacy.sweep_retention` runs the purge at most once an hour per process (run time recorded first, failure logged and never blocking chat), triggered from `ChatIsolation.current_user`, which every chat route passes through; `add_memory` counts live items only. Tests: three in `src/core/tests/test_chat_privacy.py` (each on the in-memory and SQL stores) and one in `test_chat_memory.py`; all failed before the fix (6 errors in the first run). The sweep only applies after the next deployment; the live app was not changed.

## Local checks

| Command | Result |
| --- | --- |
| `src/core`: `test_chat_privacy`, `test_chat_memory`, `test_chatthreads`, `test_chat_isolation_single_model_route` | 98 tests, OK |
| `src/api`: `test_*chat*.py` | 550 tests, OK (1 skipped) |
| `ruff check` on the four changed files | clean |
| `mypy` in `src/core` | 3 errors, all in `telemetry.py` (missing OpenTelemetry stubs) and `device_provision.py`; none in changed files |

## Per-criterion verdicts

| Criterion | State on issue | Verdict | Basis |
| --- | --- | --- | --- |
| Complete the #440 stabilization checkpoint | Unticked | Unproven | #440 criteria 7 (triage with owner approval) and 8 (PR artifacts, independent non-worker review) need a PR and an owner; no PR may be opened here. One bug was dispositioned and fixed locally toward it |
| If accepted, child features are accepted | Unticked | Partly proven, not provable as a whole | All seven children are closed. Isolation, retention (now enforced in code), consent, bounded calls, refusal and audit are observed live or locally. Screen-reader testing, DPO and Legal approval and real-model checks are excluded for the demo; closed is not accepted |
| Decision accepted or epic closed | Ticked | Not reopened | ADR 0004, 2026-10-15 |
| No memory used as evidence for a controlled decision | Ticked | Not reopened | Merged #1552; memory list empty live |
| Chat consumption bounded and reported | Ticked | Not reopened | Merged #1547 and #1558 |

## Limits

* One staff test account exists, so cross-user denial on a real thread is proven locally, not live.
* The retention sweep is not yet deployed; live proof needs a new image and revision. An idle app does not sweep; a scheduled job stays outstanding.
* The epic stays open; the two unticked criteria are left to the owner.
