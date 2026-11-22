---
title: Issue 2243 live probe plan and findings for the resident AI chat (2026-11-22)
description: Read-only live check of the demo API and resident revisions, the resident chat outcome after the expiry fix, and the post-merge probe plan for issue 2243
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop 1440x900 only, resource group `ama`, owner decisions of 2026-11-18. Research only: no Azure change, no throwaway resource and no source change. Sign-in values were read from the owner files at run time and never printed; each probe asserts they are absent from its saved output. The fix branch `test/aichat-live-20261122T141030Z` (commit `a9c6fe4fe3`, a local branch with unpushed work from another worker) was not reviewed here.

## Current revisions (read 2026-11-22 14:47 UTC)

| App | Latest and ready revision | Created | Health | Image digest |
| --- | --- | --- | --- | --- |
| `ca-resident-demo` | `0000022` (100% traffic) | 14:30 UTC | Healthy | `45b51718...` (revision 0000021 held `3066f408...`, created 04:43 UTC) |
| `ca-cutover-test-demo-api` | `0000050` (100% traffic) | 13:55 UTC | Healthy | `541068a6...` |

Resident environment read today: `ZF_DEMO_EXPIRES_AT=2028-01-01T00:00:00Z`, `ZF_DEMO_ASSISTANT_ENABLED=true`, `ZF_DEMO_ASSISTANT_ENDPOINT=https://aif-cutover-test-rzsrg.openai.azure.com`. The API app carries `AI_DEPLOYMENT=standard` (model `gpt-4.1-nano-2025-04-14`). The container registry refuses this client (firewall), so image tags and the commit behind each digest cannot be read.

## Resident AI chat probe

Probe: [probe_resident_ai.py](./issue-2243-live-probe-2026-11-22/probe_resident_ai.py), result [probe-resident-ai-baseline-result.json](./issue-2243-live-probe-2026-11-22/probe-resident-ai-baseline-result.json), screenshots in [screens](./issue-2243-live-probe-2026-11-22/screens/resident-chat-baseline.png). Sign-in returned 200.

| Question | Reply label | Reading |
| --- | --- | --- |
| Which documents are missing from my case? | Summary by rules - AI unavailable: the AI usage limit was reached | Rules only |
| How is my case going? | Summary by rules - AI unavailable: the AI usage limit was reached | Rules only |

Two other questions that the rules answer without trying the model (a safety question and an unmatched one) were labelled "workflow only, no AI used", as designed.

The label moved from "the AI exercise has ended" (the 2026-11-22 smoke, revision 0000021) to "the AI usage limit was reached" on revision 0000022. The container console confirms the reason: `resident_assistant outcome=rules_fallback reason=usage_limit` (two lines at 14:48:34 and 14:48:36 UTC, matching the two probe questions).

Interpretation (inferred, not proven by an image-to-commit link): revision 0000022 reads its expiry from the environment, so the code check in `aoai.py` no longer returns `expired`. The next gate is `SqlAccounting.reserve`, which calls `resident_ai.reserve` and returns `usage_limit` when it does not accept. That procedure refuses when the budget row is spent (`reserved_cents >= 2000`), when the resident has 5 attempts in the last hour, or when `now >= expires_at` in `resident_ai.budget` ([infra/sql/resident-assistant.sql](../../../infra/sql/resident-assistant.sql) lines 27 to 50). The same file states that expiry is data and that existing rows keep the default `2026-11-01T00:00:00`. Today is after that date, so the stored expiry is the most likely cause; the hourly count is unlikely (at most 2 attempts by this probe) and the spent-budget cause cannot be excluded.

Not provable now: the SQL server `sql-cutover-test-rzsrg` has public network access disabled, so the `resident_ai.budget` row cannot be read from this client without changing the estate, which the brief forbids.

## Employee chat check (API 0000050)

[probe_staff_chat.py](./issue-2243-live-probe-2026-11-22/probe_staff_chat.py), result [probe-staff-chat-result.json](./issue-2243-live-probe-2026-11-22/probe-staff-chat-result.json), screenshot [employee-chat-2243.png](./issue-2243-live-probe-2026-11-22/screens/employee-chat-2243.png). `POST chat/threads` returned 500 once then 200, and one `ask` returned 500 then 200; the answer seen is labelled deterministic. This is the separate defect 2245 and is unchanged.

## Post-merge probe plan

Run after the fix merges and the resident image is rebuilt and rolled. Read-only except for the one authorised roll.

1. Record `az containerapp show` for both apps: latest and ready revision, traffic, health, image digest, `ZF_DEMO_EXPIRES_AT`.
2. Map the resident digest to the merge commit through the build record (the registry is firewalled; use the build workflow output or the roll receipt).
3. Run `probe_resident_ai.py` (copy it with a new result name). Pass: a model-backed reply labelled "AI suggestion, not approved" for the two non-safety questions, HTTP 200, no sign-in value in the output.
4. Read `az containerapp logs show -n ca-resident-demo --type console`: expect no `reason=usage_limit` or `reason=expired` for the probe window.
5. If the label stays "usage limit reached", the SQL row is the cause: the owner-authorised SQL path (inside the private network) sets `resident_ai.budget.expires_at` to the demo expiry and confirms `reserved_cents` below 2000; re-run step 3.
6. Confirm the model call hit the cap-controlled path: the ledger and `reserved_cents` increase by the number of answered questions, and the Azure OpenAI deployment stays within the USD 700 cap.
7. Screenshot the chat at 1440x900 for the record.

## Acceptance criteria of issue 2243

The issue has no checklist; the criteria are its stated fix and expected outcome.

| Criterion | Status | Basis |
| --- | --- | --- |
| Derive EXPIRES from `ZF_DEMO_EXPIRES_AT` | Unproven here | Implemented on the unmerged local branch (`expires_at()` in `assistant.py`); the label change on revision 0000022 is consistent with it but no image-to-commit link is readable. `main` at `6a5e8299d0` still hard-codes 2026-11-01. |
| Add a test | Unproven here | Belongs to the fix branch; not reviewed in this task. |
| Rebuild and roll the resident image | Partly proven | Revision 0000022 (14:30 UTC) has a new digest and is Healthy at 100% traffic; its source commit is not readable. |
| Resident chat answers with the model within the budget caps | Not met | Both model-eligible questions fall back with reason `usage_limit` today. The probable SQL expiry row cannot be read or changed from this client. |
