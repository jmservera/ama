# Research: issue 2204 rule actions live (2026-11-22)

Status: opened. Disposition: executed (new investigation).

Goal: find why the demo API law store returns 503, load or enable it with repo synthetic or public text via az, then prove RuleAuthor and RuleOwner actions with the one-at-a-time role technique.

Opening facts (from earlier notes and `az containerapp show`, no secrets): revision 0000047; env has no ZF_LAW_DB and no ZF_LAW_STORE; `LawStore.from_env` returns None, so `/api/law*` and `/api/law/cards*` return 503.

## Findings (observed 2026-11-22)

* Cause of 503: revision 0000047 had neither `ZF_LAW_DB` (sqlite double) nor `ZF_LAW_STORE=mssql`, so `LawStore.from_env()` returned None and `app.law is None` gives 503 "The law store is not loaded." at `server.py` `/api/law*` and `_rulecards`.
* `/state` is an EmptyDir (ephemeral, per replica, scale 0 to 4), so the sqlite double would lose cards on idle scale-to-zero. The mssql backend persists cards in the existing Azure SQL database and snapshot blobs in a container; the app's user-assigned identity already holds Storage Blob Data Contributor on the account.
* Rule actions do not need regulatory snapshots: `LawStore` seeds two labelled draft exercise cards itself. The image carries no `docs/reference/regulatory` tree, so snapshot loading is not available in the image and is not needed for the actions.
* Trial 1 (az containerapp update with `ZF_LAW_STORE=mssql`, `ZF_LAW_BLOB_ACCOUNT_URL`, `ZF_LAW_BLOB_CONTAINER=law-snapshots` after creating that container with az): revision 0000048 ended ActivationFailed (first start also creates the law tables); the env vars were removed (0000049) and the API answered /healthz 200 again. An in-replica `LawStore.from_env()` then succeeded in 1.4 s and created the tables. Trial 2 (revision 0000050) is Running and Healthy, /healthz 200. Log Analytics is closed to this client (network perimeter), so the exact trial 1 error could not be read; the probable cause is first-start DDL exceeding the 120 s startup probe (inference, not observed).
* Authority gates in `server.py` `_rulecards`: write needs provider trusted-proxy, `rule_author` for POST `/api/law/cards`, `rule_owner` for POST `/api/law/cards/<id>/<version>/<action>`, plus staff role allowed the `law` view, `X-ZF-CSRF: 1`.
* Domain gates in `rulecards.py`: propose needs an `approver` that is a provisioned staff email or an Entra-derived identity; approve needs actor equal to the approver and demonstrably distinct from the author (`identity.distinct`); activate needs an approved version inside its effective dates and the source-monitor activation guard; hold needs active; release needs held; retire needs approved, active or held.
* Consequence: with one test account the same person cannot be author and approver. A second Entra identity is needed as author. Plan: create a throwaway Entra user with az and a random password never printed, delete it afterwards.

Planning Readiness: Ready.
