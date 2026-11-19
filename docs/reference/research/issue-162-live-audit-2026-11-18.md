---
title: Issue 162 Live Audit with Per-Criterion Table (2026-11-18)
description: Fresh live and local audit of #162 (chat and memory isolation), with retained raw output, a per-criterion proven or unproven table and the production-only items
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope

Issue #162 has criteria 1 to 5 ticked and criterion 6 (administrator and break-glass access audited with purpose, policy decided) unticked. Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). DPO and Legal approval, billing reconciliation and person-run assistive-technology testing are not needed for the demo. Sign-in credentials were read at runtime and never printed. No `src/` change; tier FOCUSED.

This note repeats, with retained raw output, the audit evidence in [chat-breakglass-live-proof-2026-11-18.md](./chat-breakglass-live-proof-2026-11-18.md) (whose counts had no raw output kept) and links the earlier user-isolation probes in [issue-162-live-isolation-evidence-2026-11-18.md](./issue-162-live-isolation-evidence-2026-11-18.md). Scripts and output are in [issue-162-live-audit-2026-11-18/](./issue-162-live-audit-2026-11-18/).

## Evidence

Live (staff test user, Retrofit Programme Manager, demo API container app, Running):

* Environment names only ([04-live-env-names.txt](./issue-162-live-audit-2026-11-18/raw/04-live-env-names.txt)): `ZF_AUTH`, `ZF_DEPLOYMENT_PROFILE` present; neither `CHAT_BREAKGLASS_ROLES` nor `CHAT_BREAKGLASS_REF` is set. By `ChatIsolation.break_glass`, every live request is refused.
* [03-live-breakglass-probe.txt](./issue-162-live-audit-2026-11-18/raw/03-live-breakglass-probe.txt): `/api/audit-check` intact with 2068 entries (head `1b005f021a32`); a break-glass POST with a 10-plus character purpose returned 403 "policy not decided or role not named" and the count went to 2069 (head `9c8f24745c44`); a POST with purpose `x` returned 403 with the same reason and the count went to 2070 (head `b2690e0f6dde`). Chain intact throughout. Each refusal adds exactly one hash-chained entry. The probe created no thread, memory item or other record, so nothing needed cleanup.

Local (real server route on synthetic data):

* [01-chat-isolation-tests.txt](./issue-162-live-audit-2026-11-18/raw/01-chat-isolation-tests.txt): `python3 -m unittest tests.test_chat_isolation` from `src/api`, 33 tests, OK. The logged `ValueError: The law store is not loaded` traceback above the result is background noise in the tests' fixtures; it did not fail a test.
* [02-breakglass-audit-rows.txt](./issue-162-live-audit-2026-11-18/raw/02-breakglass-audit-rows.txt) from [dump-breakglass-audit.py](./issue-162-live-audit-2026-11-18/dump-breakglass-audit.py): the stored audit rows after the real break-glass route ran with a named role and policy reference. Five refusals carry `basis` `demo-only`, the reason and the redacted purpose (an email in the purpose is replaced by `[email removed]`). Two grants carry actor-keyed target, purpose, `policy_ref`, `basis`, `expires` and thread and memory counts, and no message text.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| 1. Queries keyed by the authenticated user in the server | Proven (live and local) | Live forged-identity and client-owner-field probes in the [isolation note](./issue-162-live-isolation-evidence-2026-11-18.md); `server.py` derives the owner from the validated principal |
| 2. Role matrix covers every chat and memory endpoint and denies cross-user | Proven locally; live cross-user read of a real foreign thread unproven | 33 tests OK (raw output retained). Only one staff Entra identity exists, so a real second authenticated user cannot be tested live |
| 3. Retrieved context uses the same field projection | Proven locally; not exercised live | Local tests; live needs a model-backed answer and a second role |
| 4. Never shared into another user's prompt | Proven locally; not exercised live | Local tests; live needs two users and a model call |
| 5. Prompt injection cannot cause tool calls, exposure or writes | Proven locally (test set); not re-run live | `test_injection_cannot_cause_tool_calls_exposure_or_writes` in the 33 tests |
| 6. Admin and break-glass audited with purpose, policy decided | Partly proven; leave unticked | Refusals audited live (3 chain entries above). Grant with purpose proven only locally (rows above). Policy decided for the demo only (owner decision [2026-11-03](./chat-demo-breakglass-disclaimer-2026-11-03.md)); administrator Entra role, user notification and audit retention undecided |

## Why criterion 6 cannot be fully proven live

A live grant needs `CHAT_BREAKGLASS_ROLES` and `CHAT_BREAKGLASS_REF` on the deployed app. Setting them is a configuration change and a new revision on the shared demo, which the 2026-11-18 authorisation ("no production changes") does not cover. A throwaway second app was not created: the demo uses `ZF_AUTH=trusted-proxy`, which trusts identity headers from the ingress, and no API returns audit rows, so a throwaway app would add exposure without a readable audit trail. The owner can accept the combined evidence for the demo or authorise a temporary setting.

## Production-only items

* DPO and Legal approval of the break-glass policy (BRD OD-46), and any real-data use.
* Which Entra app role is the administrator, user notification after access and audit retention.
* Content access (option B), which stays refused and needs a separate DPO and Legal decision.
* A real two-user cross-account test on Entra with production identities.

## Limits

* The live audit counts come from one run and show the chain intact; audit row text is not readable live because no API returns rows.
* The earlier live note's over-broad "New chat" delete is not repeated here; this run created no records.
* The scratch sign-in state file was deleted after use. No Azure resource was created or changed; no cost-bearing action was taken.
