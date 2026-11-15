# Changes: #358 (2026-11-13)

* infra/tests/test_setup_entra.py: two new tests. One covers an expired Key Vault credential and the `azure_credential_guard` branches. The other covers a new Key Vault credential rebuilt alongside mixed value and Key Vault-referenced secrets (full, names-only and omitted-kv listSecrets shapes, token-store SAS entry retained).
* No production script change (no defect found). initialize-api-auth.py unchanged.

## Mutation checks (all restored; scripts have no diff)

* `azure_credential_guard` condition replaced with `if False:`: 4 subtests fail (baseline: 0 failures).
* Expiry filter `> now` replaced with `True`: 8 failures.

## Validation

* `test_setup_entra.py`: 126 OK. `test_initialize_api_auth.py`: 17 OK.
* Full `infra/tests` with src core, agents, api, orchestrator and pyyaml installed in the venv: 516 run, 4 skipped, all pass after the missing dependencies were installed (initial errors were `ModuleNotFoundError` only).
* mypy on the three files: no issues.
* ruff check and format: the files already fail on main (18 errors, 3 files unformatted). The change adds one UP017 finding (`timezone.utc`, matching existing style) and no other new finding.
