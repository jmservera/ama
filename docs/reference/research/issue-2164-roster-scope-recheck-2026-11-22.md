---
title: "Issue 2164 roster scope for Entra staff: re-proof on main (2026-11-22)"
description: Evidence that the fix merged in 6a03928ccb satisfies the issue 2164 criteria, with the one live item that stays unproven.
ms.date: 2026-11-22
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
