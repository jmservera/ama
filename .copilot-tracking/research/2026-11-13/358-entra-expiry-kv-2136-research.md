# Research: #358 credential expiry and Key Vault secret preservation (2026-11-13)

Base: origin/main ee068a4b. Disposition: executed. Planning readiness: Ready.

## Findings

* Item 1: the expiry filter in `secret_reference` (setup-entra.py, `valid` list) is already covered on main (`test_stored_credential_expiry_guards_generated_and_legacy_reuse`; replacing the filter with `True` fails 6 tests). The uncovered guard was `azure_credential_guard` (Azure mode, Key Vault only): mutating its condition to `if False:` passed all 124 tests.
* Item 2: `preserve_app_secrets` merges GET `configuration.secrets` with `listSecrets`, keeps `keyVaultUrl` and `identity` for references (no `value`), requires both fields, and rejects conflicts and malformed inventories. Existing tests cover this for an app-store new secret. Not covered: a new Key Vault-backed credential rebuilt alongside mixed existing entries. No production defect found; every PATCH payload retained the exact reference entries.
* Item 3: `infra/scripts/initialize-api-auth.py` on main already has a delegating `main()` (runpy to setup-entra.py `main`); no conflict markers; no change needed. Existing 17 tests pass.
* Live Azure non-production execution was not performed (deferred).
