---
title: Issue 358 close-out research (setup-entra expiry and Key Vault preservation)
ms.date: 2026-11-13
---

## Scope

Issue #358 three items: (1) expired `endDateTime` credential-guard test, (2) Key Vault-referenced secret preservation test plus read-only live inspect, (3) delegating `main()` in `initialize-api-auth.py`.

## Findings

* Research disposition: executed. Planning Readiness: Ready.
* Item 1: `infra/tests/test_setup_entra.py` has `test_expired_credential_rotates_without_removing_in_use_old_credential` and `test_stored_credential_expiry_guards_generated_and_legacy_reuse`. The guard is `setup-entra.py` lines 1484-1486 (`c.get("endDateTime") and ... > now`). Mutation: replacing the `c.get("endDateTime") and` clause with `False and` made 58 of 124 `test_setup_entra` tests fail, so the guard is test-proven. The source was restored.
* Item 2: `mixed_secret_inventory` and related tests preserve `keyVaultUrl` plus `identity` entries and app references. Live read-only inspect of `ca-cutover-test-api` (resource group `ama`), projecting only name and boolean flags, returned zero secrets (`secrets` null). No secret values were read and nothing was written. There is no populated baseline, so the live round-trip stays unmet; this matches the issue's 2026-10-19 note and the real synthetic evidence in #417.
* Item 3: `initialize-api-auth.py` `main()` runs `setup-entra.py` `main` through `runpy` (delegating, no conflicting old implementation). `infra/tests/test_initialize_api_auth.py` passes.
* Validation (venv `/tmp/venv-358-1554`): `unittest infra.tests.test_setup_entra infra.tests.test_initialize_api_auth` 141 OK. mypy on `initialize-api-auth.py` clean. Full `infra/tests` discovery in this host shows pre-existing environmental failures (49 failures, 32 errors, unrelated to these files, no source changed). Ruff with the CI isolated rule set reports pre-existing findings in files outside the CI ruff scope.

## Decision

No source or test change is needed. Deliver evidence only.

## Addendum: stronger mutation (critique-driven)

Appending `or True` to the `> now` comparison (expired credentials accepted) fails `test_expired_credential_rotates_without_removing_in_use_old_credential` and every expired and null-expiry subcase of `test_stored_credential_expiry_guards_generated_and_legacy_reuse`. The existing mutation test near `test_setup_entra.py:2235` also covers this. Source restored; tree clean.
