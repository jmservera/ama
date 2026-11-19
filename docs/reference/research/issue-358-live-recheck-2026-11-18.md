---
title: Issue 358 Live Recheck - Deletion, Delegating main and Demo App Baseline
description: Second-pass per-criterion record for issue 358 closing the evidence gaps left by the first live note
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Follows [issue-358-live-evidence-2026-11-18.md](./issue-358-live-evidence-2026-11-18.md).
Owner decisions of 2026-11-18 apply: synthetic demo, desktop only, live Azure in
resource group `ama`, no drills, no Key Vault rotation, no production change.
This pass made no Azure write and no source change. No credential was read or printed.

## Evidence limits

The Azure reads, the 126-test run and the source read below were observed during this pass; raw output not retained. They are repeatable observations, not stored evidence, and the status rows say so.

## Observations (2026-11-18)

Observed; raw output not retained:

* `az containerapp show -g ama -n ca-358-throwaway` returns `ResourceNotFound`,
  and `az containerapp list -g ama` lists only `ca-cutover-test-api`,
  `ca-cutover-test-agents`, `ca-cutover-test-demo-api` and `ca-resident-demo`.
  This closes the gap that the earlier `post-delete-check.txt` was empty.
* A read-only ARM GET (API 2025-07-01) of `ca-cutover-test-demo-api` shows
  provisioning `Succeeded` and one Key Vault-referenced secret
  (`entra-0dbb...-7a8a02692e5a`) whose `keyVaultUrl` and user-assigned
  `identity` are intact. This is the real secret that earlier rebuilds left in place;
  it is not a new rebuild run.
* `python3 -m unittest infra.tests.test_setup_entra`: 126 tests, OK. The tests
  `test_expired_credential_rotates_without_removing_in_use_old_credential` and
  `test_expired_keyvault_credential_is_never_reused_and_azure_guard_blocks_app_store`
  cover the expired stored credential guard.
* `test_legacy_cli_delegates_public_url_without_reimplementing_setup` passes, and
  `infra/scripts/initialize-api-auth.py` (180 lines) has `main()` at line 171
  that runs `setup-entra.py` through `runpy`, so the delegating `main()` is kept.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| 1. Test for the stored-but-expired credential guard | Observed; raw output not retained (test pass) | Existing tests pass; the earlier mutation run (guard disabled, 8 failures) is retained in the first note |
| 2. Rebuild preserves Key Vault-referenced secrets in a non-production run | Proven for the rebuild component by the first note's retained round-trip; the deletion check here is observed; raw output not retained | Throwaway live ARM round-trip in the first note; deletion now observed absent (not retained); the demo API still carries its Key Vault reference |
| 2b. Same through a full `setup-entra.py` run on the deployed demo app | Not proven | Needs Graph `addPassword` and tenant administrator authority (#349/#360), outside demo authority for this pass |
| 3. #352 conflict, delegating `main()` kept | Observed; raw output not retained (source read, test pass) | Source read plus passing delegation test |

## Limits

* The baseline GET proves the reference exists now, not that a particular
  deployment preserved it.
* The first note's retained mutation output remains tail-only; this pass did not repeat the mutation.
