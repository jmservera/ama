---
title: Chat Break-Glass Live Proof on the Synthetic Demo (#162 criterion 6)
description: Live evidence that break-glass access on the demo API is default-deny and audited, which parts of criterion 6 are proven, and which cannot be proven for the demo
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope

Criterion 6 of #162 is the only unticked item: "Administrator and break-glass access is audited, with purpose, and the policy is decided". Criteria 1 to 5 are ticked and were not re-opened. Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). DPO and Legal approval is not needed for the demo. No source code changed.

## Live configuration (read-only)

`az containerapp show -g ama -n ca-cutover-test-demo-api`: revision `ca-cutover-test-demo-api--0000031`, state Running, `ZF_AUTH=trusted-proxy`, `ZF_DEPLOYMENT_PROFILE=demo`, `ZF_CHAT_DEMO_ACTIVATION=approved-2026-11-03`. The environment list contains `CHAT_DPIA_REF`, `CHAT_NOTICE_REF`, `CHAT_RETENTION_REF`, `CHAT_LAWFUL_BASIS_REF` and `CHAT_RETENTION_DAYS`, but neither `CHAT_BREAKGLASS_ROLES` nor `CHAT_BREAKGLASS_REF`. By the rule in `ChatIsolation.break_glass`, the deployed demo therefore refuses every break-glass request.

## Live probes

The signed-in staff test user (role Retrofit Programme Manager, credentials read at runtime and never printed) posted to `POST /api/chat/breakglass` from the browser with `X-ZF-CSRF: 1`. See [probe-breakglass-refusal.py](./chat-breakglass-live-proof-2026-11-18/probe-breakglass-refusal.py) and the [desktop screenshot](./chat-breakglass-live-proof-2026-11-18/app-after-breakglass-probe.png).

| Step | Result |
| --- | --- |
| `/api/audit-check` before | intact true, 1517 entries, head `f82b51a50716` |
| Refused request with a purpose of 10 or more characters | 403 "Break-glass access is refused: policy not decided or role not named." |
| `/api/audit-check` after | intact true, 1518 entries, head `5abbabe501fa` |
| Refused request with purpose `x` | 403, same reason (policy check comes first) |
| `/api/audit-check` after | intact true, 1519 entries, head `82502c3f8998` |

Each refused attempt added exactly one hash-chained audit entry and the chain stayed intact. The earlier unscripted probe run (first count 1487, later 1517) also showed the chain growing with other activity; only the table above is a controlled before and after.

## Criterion 6 verdict for the demo

| Part | Verdict | Basis |
| --- | --- | --- |
| Break-glass is audited (refusals) | Proven live | One audit entry per refused attempt, chain intact (table above) |
| Break-glass is audited with purpose (grants) | Not provable live | The grant path needs `CHAT_BREAKGLASS_ROLES` and `CHAT_BREAKGLASS_REF` set on the app. That is a deployed configuration change and a new revision, outside the 2026-11-18 authorisation (no production change). Proven locally instead: `src/api/tests/test_chat_isolation.py` (33 tests, OK) covers default deny, short purpose, self-target, wrong role, two audited grants with `basis` `demo-only`, metadata-only output and the minutes cap |
| Audit entry text readable live | Not provable live | No API returns audit entries, only `/api/audit-check` integrity and count. Reading rows needs direct SQL access, which was not used |
| Policy decided | Decided for the demo only | Owner decision of 2026-11-03, [demo-only disclaimer](./chat-demo-breakglass-disclaimer-2026-11-03.md): option A, counts only, purpose of 10 or more characters, named role, audited, content access refused. Which Entra role is the administrator, user notification and audit retention remain undecided |
| DPO and Legal approval | Not needed for the demo | Owner decision 2026-11-18; the policy is not approval for real personal data |

Result: criterion 6 is partly proven. The refusal and audit behaviour is proven live; the granted path is proven by tests only; the policy is decided for the demo only. The issue box should stay unticked unless the owner accepts that evidence as sufficient for the demo, or authorises a temporary app setting.

## Side effect and disclosure

Opening a chat from the probe created a thread, and my cleanup then deleted every thread titled "New chat" for the staff test user, not only the one I created. About 15 empty synthetic demo threads of that test user were removed. No other user's data was touched, and the user's non-default threads were not affected. The over-broad delete was an error in the cleanup filter.
