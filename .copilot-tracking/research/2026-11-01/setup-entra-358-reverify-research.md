---
title: Issue 358 re-verification research
ms.date: 2026-11-01
---

Base: origin/main 81cf0c9e2. Task slug: setup-entra-358-reverify. Research disposition: executed. Planning Readiness: Ready.

## Findings per issue item

* Item 1 (expired stored-credential test): `infra/tests/test_setup_entra.py` `test_stored_credential_expiry_guards_generated_and_legacy_reuse` and `test_expired_credential_rotates_without_removing_in_use_old_credential` cover expired, boundary, missing and tz-offset endDateTime. `SecretPreservationMutationTests` mutates the expiry comparison and fails. Delivered by #374 and #583.
* Item 2 (Key Vault secret preservation): `preserve_app_secrets` in `infra/scripts/setup-entra.py` keeps keyVaultUrl and identity; `test_secret_rebuild_preserves_kv_and_app_references_across_response_shapes` and the mutation tests prove offline behaviour. #417 recorded a bounded real synthetic round-trip. Populated existing-app acceptance remains unmet: the 2026-10-19 issue comment found configuration.secrets null on all three production apps.
* Item 3 (#352 conflict): `infra/scripts/initialize-api-auth.py` `main()` delegates to setup-entra.py via runpy. Resolved.

## Constraint

The task forbids live Azure access, so the populated round-trip cannot be run here.

## Evidence

* `python3 -m unittest tests.test_setup_entra -q` from `infra`: 124 tests OK.
* Issue #358 comments; merged PRs #374, #417, #583, #683.
