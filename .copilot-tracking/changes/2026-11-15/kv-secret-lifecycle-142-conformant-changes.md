<!-- markdownlint-disable-file -->
# Changes Log: Conformance Closure for Key Vault Secret Lifecycle (#142 Child Loop 4)

## Metadata

* Task ID: issue-142-conformant
* Task slug: kv-secret-lifecycle-142-conformant
* Plan path: `.copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-conformant-plan.md`
* Phase details path: `.copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-conformant-phase-details.md`
* Date: 2026-11-15
* Status: completed

## P01: Core, CLI, and Runbook Conformance Fixes (`P01-T01`)

* Updated `src/core/src/zava_forward/core/secret_lifecycle.py`:
  * Added Key Vault version `created` timestamp parsing (`_parse_kv_version_created`), enforced Azure Key Vault newest-version semantics on versionless `keyVaultUrl` in `post_switchover`, `post_retire`, and `rollback` (rejecting versionless in-place rollback), and guarded all metadata timestamp/numeric parses into structured `problems`.
  * Enforced event-bound stage probe floors (`overlap_start_dt`, `next_ver_created_dt`, `containerApp.switchoverAt` bound into `receipt["switchoverAt"]`, `effective_retired_at` from `retiredPriorCredential.retiredAt` or `credentials.priorRetiredAt`, and `containerApp.rollbackAt` evaluated before `pre_rollback_hold_problems`).
  * Rejected paginated ARM/Graph list envelopes (`nextLink` / `@odata.nextLink`) in `unwrap_arm_list_envelope` after `assert_no_secret_material`.
  * Sanitized all remaining `!r` / string-interpolated reflections of untrusted payload fields and rejected non-finite floats (`NaN`, `Infinity`, `-Infinity`) across `assert_no_secret_material`, `_validate_probe_batch`, `_parse_non_negative_float`, and `audit_keyvault_data_plane_access`.
* Updated `infra/scripts/secret_lifecycle.py`:
  * Routed `load`, `_load_verification_keys`, and both `load_ledger_entries` JSON parse paths through `_strict_json_loads(..., parse_constant=...)` while preserving `__all__` exports `load` and `load_ledger_entries`.
  * Validated `--signing-key-env` identifier syntax without echoing untrusted values and enforced `_KEY_ID_RE` on `--keys-file` entries.
* Updated `infra/README.md`:
  * Aligned step 1 to `--years 1`, step 2 to `containerApp.switchoverAt` (`firstSampleAt >= switchoverAt`), step 3 to `firstSampleAt >= retiredAt` + `credentials.priorRetiredAt` + `containerApp.switchoverAt`, and step 4 to version-pinned `priorVersionId` `keyVaultUrl` (or two-name `priorSecretName`) + `containerApp.rollbackAt`.

## P02: Focused Conformance Regression Tests & Validation (`P02-T01`)

* Updated `src/core/tests/test_secret_lifecycle.py`:
  * Updated `_rotation_fixture` and rollback assertions for version-pinned in-place rollback (`keyVaultUrl` pinned to `priorVersionId`), Key Vault `secretVersions.entries[].created` metadata, `containerApp.switchoverAt`, `containerApp.rollbackAt`, and `credentials.retiredPriorCredential.retiredAt` / `credentials.priorRetiredAt`.
  * Added 4 semantic regression tests covering Key Vault version-resolution semantics on rollback and switchover (`AC-C1`), event-bound probe floors and guarded metadata parsing (`AC-C2`), paginated ARM/Graph envelope rejection (`AC-C3`), and unlabelled canary sanitization + non-finite float rejection (`AC-C4`, `AC-C5`).
* Updated `infra/tests/test_secret_lifecycle.py`:
  * Updated `_rotation_payload` and inline `retire_payload` (`priorRetiredAt`, `switchoverAt`, `rollbackAt`, `created`, pinned rollback `keyVaultUrl`).
  * Added 2 semantic CLI/runbook regression tests covering strict `NaN`/`Infinity` JSON rejection across `load`, `_load_verification_keys`, and `load_ledger_entries` plus `--signing-key-env` sanitization (`AC-C4`, `AC-C5`) and `infra/README.md` `--years 1` + steps 2..4 contract parity (`AC-C6`).
* Validation executed (Focused tier):
  * `PYTHONPATH=src/core/src python3 -m unittest src/core/tests/test_secret_lifecycle.py src/core/tests/test_dependency_rule.py infra/tests/test_secret_lifecycle.py -q` -> `Ran 62 tests ... OK`.
  * `PYTHONPATH=src/core/src python3 -m unittest discover -s infra/tests -p 'test_*.py' -q` -> `Ran 640 tests ... OK (skipped=4)`.
  * `PYTHONPATH=src/core/src python3 infra/scripts/bicep_inventory.py --check` -> verified (`29 architecture rows, 20 Bicep modules, 12 from-empty steps`).
  * `(cd src/core && python3 -m ruff check && python3 -m ruff format --check && python3 -m mypy)` -> `All checks passed!`, `310 files already formatted`, `Success: no issues found in 363 source files`.
  * `python3 -m ruff check --isolated --line-length 100 infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && python3 -m ruff format --isolated --line-length 100 --check infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && MYPYPATH=src/core/src python3 -m mypy --strict --explicit-package-bases infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py` -> `All checks passed!`, `2 files already formatted`, `Success: no issues found in 2 source files`.
  * Diff scan on modified/added `src/` and `infra/` files (`git --no-pager diff src/ infra/` and untracked `src/core` files) -> `0` `.copilot-tracking` references (`tools/rpi-checks.py --all` intentionally not run per Focused validation tier; full `src/core/tests` discovery skipped per user instruction because it exceeds 600s).

## Reconciled Blockers, Remaining Work, and Follow-Up Items

* Blockers: none.
* Remaining active-plan work: none (`P01`, `P01-T01`, `P02`, `P02-T01`, and `AC-C1`..`AC-C6` complete).
* Follow-up items (outside offline scope):
  1. Execute live Azure test-environment staged Entra client-secret rotation drill and archive sanitized signed rotation receipt.
  2. Export live quarterly Log Analytics `AzureDiagnostics` + RBAC snapshot via `rbac-merge` and sign inaugural live access-review ledger entry.
