---
title: Issue 358 Live Pass 3 - Retained Evidence per Criterion
description: Third per-criterion record for issue 358 retaining the raw outputs the earlier notes lacked
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Builds on [issue-358-live-evidence-2026-11-18.md](./issue-358-live-evidence-2026-11-18.md) and
[issue-358-live-recheck-2026-11-18.md](./issue-358-live-recheck-2026-11-18.md). Owner decisions of
2026-11-18 apply: synthetic demo, desktop only, live Azure in resource group `ama`, no Key Vault
rotation, no production change. This pass made no Azure write, no source change and read no credential.
Raw outputs are in `issue-358-live3-2026-11-18/`.

## Evidence

* `baseline-tests.txt`: `infra.tests.test_setup_entra`, 126 tests, OK.
* `mutation-expiry-filter-always-true.txt`: on a temporary copy of `infra/`, the expiry comparison in
  `secret_reference` (line 1486) was made always true. Nine failures across three expiry tests; the worktree
  source was untouched.
* `azure-list-and-throwaway-absent.txt`: `az containerapp list -g ama` shows four apps and
  `ca-358-throwaway` returns `ResourceNotFound`, so the earlier throwaway app is deleted.
* `demo-api-kv-reference-readonly.json`: read-only ARM GET of `ca-cutover-test-demo-api` shows provisioning
  `Succeeded` and one Key Vault-referenced secret with `keyVaultUrl` and user-assigned `identity` intact
  (subscription id redacted; no secret value requested).
* `delegating-main-source.txt` and `delegation-test.txt`: `initialize-api-auth.py` `main()` runs `setup-entra.py`
  via `runpy`; the delegation test passes.

## Per-criterion status

| Criterion | Status | Basis |
| --- | --- | --- |
| 1. Test covering the stored-but-expired credential guard | Proven | Tests exist and pass; disabling the guard on a scratch copy fails nine subtests (retained) |
| 2. Non-production run shows the secrets rebuild preserves Key Vault-referenced secrets | Proven for the rebuild component | First-pass retained live round trip (`issue-358-live-2026-11-18/roundtrip-output-run2-polled.txt`); throwaway now confirmed deleted; demo API reference confirmed intact |
| 2b. Same through a full `setup-entra.py` run on the deployed demo app | Unproven for the demo | Needs Graph `addPassword`, tenant administrator authority and a Key Vault write; the owner decision excludes Key Vault rotation |
| 3. Conflict with #352 resolved, delegating `main()` kept | Proven | Source lines and passing delegation test retained |

## Needed follow-up

No `src` or `infra` change is needed for criteria 1 to 3. Criterion 2b, if ever wanted, is a full-tier
follow-up (security and infrastructure scope) outside this demo's authority.

## Limits

The demo API reference proves the reference exists now, not that a particular deployment preserved it.
