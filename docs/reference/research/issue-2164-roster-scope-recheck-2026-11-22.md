---
title: "Issue 2164 roster scope for Entra staff: re-proof on main (2026-11-22)"
description: Evidence that the fix merged in 6a03928ccb satisfies the issue 2164 criteria, with the one live item that stays unproven.
ms.date: 2026-11-23
---

Scope: synthetic demo, desktop only. Source reads and unit tests only; no credentials were used and no Azure resource was created or changed.

## Findings

* Main at fetch time (`origin/main` 3219004e90) already contains 6a03928ccb, which changes `Assistants.authorize` in `src/core/src/zava_forward/core/assistants.py` so a roster-bound Entra principal is re-read from its roster row (email from `bound`, oid and tid must match) and then checked for role, `disabled`, `active`, `case_ids` and `areas`. View-only Entra principals are refused. Unbound Entra principals keep the earlier behaviour.
* `python3 -m unittest` in `src/api` for `ReviewTests.test_bound_entra_staff_inherit_roster_scope_and_revocation` and `ReviewTests.test_unbound_and_view_only_entra_principals`: 2 tests, OK.
* `python3 -m unittest test_assistants_identity` in `src/core`: 5 tests, OK.
* Deployed `ca-cutover-test-demo-api` (resource group `ama`) runs `crcutovertestrzsrg.azurecr.io/zava-forward-api@sha256:065628c9...467eed`, revision `ca-cutover-test-demo-api--0000053` (read-only `az containerapp show`). The digest cannot be mapped to a commit without the build record, so the deployed behaviour is not proven here.
* Re-check at 2026-11-22T23:56Z (r3): the app is now on revision `ca-cutover-test-demo-api--0000054`, digest `sha256:3f2be664...faf945`. `az acr repository show-tags` for `crcutovertestrzsrg` is refused by the registry network rules, so the new digest is still not traceable to a commit and the deployed behaviour stays unproven.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Decide whether roster-bound Entra staff inherit the bound row scope | Proven | Decision implemented in 6a03928ccb; read on main |
| Test for scope bypass | Proven | First test above passes |
| Test for view_only with an eligible role | Proven | Second test above passes |
| Deployed image carries the fix | Unproven | Digest not traceable to a commit; not required by the issue |

## Re-check on 2026-11-23 (main b11b8259bd)

* Read-only `az containerapp show` in resource group `ama`: `ca-cutover-test-demo-api--0000054` (created 2026-11-22T23:14Z, digest `sha256:3f2be664...faf945`) and `ca-resident-demo--0000026`. The registry reports `publicNetworkAccess` Disabled, so the digest still cannot be mapped to a commit.
* Timing argument, circumstantial only: 6a03928ccb merged at 2026-11-22T21:26:50Z, the last later `src/api` or `src/core` commit before the revision is a6ba1956db (23:05:25Z), and the revision was created at 23:14Z. A build from main at that point would contain the fix, but no build record was available to confirm it.
* Tests re-run: `src/api` two #2164 tests OK; `src/core` `test_assistants_identity` 5 tests OK. No source change.
* A live behavioural proof needs a roster-bound Entra principal with a restricted `case_ids` list, which means editing a roster row on live data. The owner decisions of 2026-11-18 exclude production changes, so this stays unproven; the issue does not require it.

## Re-check r5 on 2026-11-23 (HEAD 9dbfab6f56)

* 6a03928ccb remains an ancestor of HEAD. The same two `src/api` tests and the five `src/core` `test_assistants_identity` tests pass.
* Read-only `az containerapp` in resource group `ama`: `ca-cutover-test-demo-api--0000055` (created 2026-11-23T03:25Z, 100% traffic, digest `sha256:b628e067...`) and `ca-resident-demo--0000027`. The registry is network-restricted, so the digest still cannot be mapped to a commit; the revision post-dates the fix, which is circumstantial only.
* Criteria table above is unchanged: three proven, the deployed-image item unproven and not required. No source or estate change.
