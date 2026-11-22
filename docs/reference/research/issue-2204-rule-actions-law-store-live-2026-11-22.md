---
title: Law Store Enabled and RuleAuthor and RuleOwner Actions Exercised Live (Issue 2204)
description: Why the demo API returned 503 for the law store, how it was enabled with az, and what the RuleAuthor and RuleOwner capability roles did live when assigned one at a time to the demo test account
author: AMA programme
ms.date: 2026-11-22
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only, live Azure authorised (resource
group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Azure CLI
only, no Bicep. This note continues the
[contractor and capability note](./issue-2204-contractor-capability-combos-live-2026-11-22.md),
which could not run a rule action because the law store returned 503. Evidence is in
`.copilot-tracking/evidence/2026-11-22/issue-2204-rules-live/` (script
`live_rule_actions.py`, machine record `live-rule-actions.json`, two screenshots with emails
masked).

## Why the law store returned 503

`LawStore.from_env()` returns nothing unless `ZF_LAW_STORE=mssql` or `ZF_LAW_DB` is set. Revision
0000047 of `ca-cutover-test-demo-api` had neither, so `app.law` was empty and every `/api/law*` and
rule-card route answered 503 "The law store is not loaded." (`server.py`). Observed, from
`az containerapp show` environment names (values not secret).

## How it was enabled

* The `/state` volume is an EmptyDir, per replica, with scale between 0 and 4, so the sqlite test double would lose cards when idle. The mssql backend keeps cards in the existing Azure SQL database.
* `az storage container create -n law-snapshots` on `stcutovertestrzsrg`, then `az containerapp update --set-env-vars ZF_LAW_STORE=mssql ZF_LAW_BLOB_ACCOUNT_URL=... ZF_LAW_BLOB_CONTAINER=law-snapshots`. The app identity already holds Storage Blob Data Contributor on the account. No Bicep, no SQL or Key Vault change.
* First attempt, revision 0000048: ActivationFailed and the API unreachable (504) for about eight minutes. The env vars were removed (revision 0000049) and the API answered `/healthz` 200 again. An in-replica test (`az containerapp exec`) then built `LawStore` in 1.4 s and created the law tables. The same update retried as revision 0000050 became Running and Healthy. Log Analytics is closed to this client by a network perimeter, so the first failure's message could not be read; first-start table creation exceeding the 120 s startup probe is an inference, not an observation.
* Regulatory snapshots were not loaded: the image has no `docs/reference/regulatory` tree and rule cards do not need them (the store seeds two labelled draft exercise cards itself). Loading snapshots would need a new image, which is a source or deployment change and out of scope.
* The change is kept: revision 0000050 with the three env vars is the live state; `law-snapshots` stays. Revert with `az containerapp update --remove-env-vars ...`.

## Result by role (one at a time, account restored to Programme Manager only)

Each row signed in with Playwright after Graph confirmed the app roles in the token, then called the
API from the signed-in page with the CSRF header.

| Assignment | Observed |
| --- | --- |
| Programme Manager only | GET `/api/law/cards` 200 (was 503); POST propose 403 |
| Programme Manager + RuleAuthor | `rule_roles` = `rule_author`; POST `/api/law/cards` 201, version 1 in state `draft`, event role `rule_author`; POST approve 403 (wrong role) |
| Programme Manager + RuleOwner | `rule_roles` = `rule_owner`; POST propose 403 (wrong role); approve own authored card 409 "an author cannot approve their own card"; approve a seed card 409 "only the named owner role of this card can do this"; activate, hold and retire a draft each 409 with the state rule; card stays `draft` |

## Acceptance criteria

| # | Criterion | Status for the demo | Basis |
| --- | --- | --- | --- |
| 1 | Each role signs in and sees only its permitted views; admin sees all | Partly proven: RuleAuthor is proven to perform its permitted action live (201, recorded role). RuleOwner is proven to reach the domain rules and be refused by them. A successful RuleOwner action (approve, activate, hold, release, retire) is **unproven** | Table above. The approval gate requires an owner distinct from the author. A second Entra identity was needed: a throwaway user was created and deleted, but the tenant blocks multifactor registration ("You cannot access this right now"), a Temporary Access Pass is refused (403) and the resident test account sits in another tenant. No further identity is available without the owner |
| 2 | One wrong-role denial shown; no credentials printed or stored | Proven | 403 for propose without RuleAuthor, approve with only RuleAuthor, propose with only RuleOwner; literal scan of the evidence folder for each credential found no match; the throwaway user password was random and never printed |
| 3 | Evidence recorded | Proven | This note, index, log, evidence folder, changes record |

The 503 cause, the enablement and the RuleAuthor action are new. The persistent synthetic draft
`exercise-rules-live-2204` version 1 now exists in the demo SQL database; the table is append-only, so it
cannot be deleted. Throwaway resources: the Entra user was deleted (a Graph query finds none); no other
throwaway was created.

## Follow-ups

* Owner decision: provide a second MFA-registered synthetic staff identity, or a conditional-access exclusion for a test group, so the distinct-owner approval, activation, hold, release and retire can be proven live.
* Investigate why the first mssql start exceeded the probe (consider a longer startup probe for first start).
* Build an image that carries the regulatory snapshots if the owner wants the law watch views populated live.
