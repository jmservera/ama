---
title: Research 358 setup-entra credential tests
ms.date: 2026-11-01
---

Disposition: reused and re-verified against current main (efebfc6d).

* AC1 expired stored credential test: present, `infra/tests/test_setup_entra.py` `test_stored_credential_expiry_guards_generated_and_legacy_reuse` and mutation test `test_expiry_and_secret_field_mutations_fail_behavioral_assertions` (delivered by #583).
* AC2 Key Vault secret preservation: `secret_reference` in `infra/scripts/setup-entra.py` keeps listSecrets entries including `keyVaultUrl` and `identity`; offline tests and synthetic component evidence (#374, #417) cover it. A live, originally populated non-production run is NOT performed here (no Azure or credential access).
* AC3 #352 conflict: `infra/scripts/initialize-api-auth.py` retains the delegating `main()`.
* Re-run: `infra/tests/test_setup_entra.py` 124 tests pass.

Planning Readiness: Ready (evidence-only slice).
