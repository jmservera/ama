<!-- markdownlint-disable-file -->
# Changes Record: Verification Seal for Key Vault Secret Lifecycle (#142 Child Loop 2)

## Metadata

* Task ID: issue-142-seal
* Task slug: kv-secret-lifecycle-142-seal
* Plan: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-seal-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-seal-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-seal-plan-critique.md
* Declared scope: Full plan (`P01`, `P02`)
* Execution status: completed

## Summary

Completed `P01` (`P01-T01`) and `P02` (`P02-T01`) across `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md`, `src/core/tests/test_secret_lifecycle.py`, and `infra/tests/test_secret_lifecycle.py`, sealing `RV-001`..`RV-004` and `PC-001`..`PC-004` and passing full Focused validation (`51` targeted lifecycle/dependency tests, all `637` `infra/tests`, `bicep_inventory.py --check`, `ruff check`, `ruff format --check`, and `mypy` / `mypy --strict`).

## Phase Evidence

### P01: Seal rotation verification, child-secret RBAC scope checks, ledger window continuity, and runbook commands

* `P01-T01` (`src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md`):
  * Sealed `verify_staged_entra_rotation`: enforced `require_browser_mode: bool = True` by default (forcing `effective_browser_mode = True` and rejecting `browserMode: False` unless explicitly overridden via `require_browser_mode=False` or CLI `--allow-non-browser-mode`), validated strict boolean `enabled` / `attributes.enabled` via `_parse_strict_enabled` across Entra `credentials.entries` and Key Vault `secretVersions.entries`, redacted untrusted URI/secret/version strings from `problems`, required zero pre-hold validation problems for `rollbackVerified=True`, and added 32-byte HMAC-SHA256 signing/verification (`signatureAlgorithm: "HMAC-SHA256"`, constant-time `hmac.compare_digest` after `_HEX64_RE` guard) for `priorSwitchoverReceipt` via `signing_key` and mutually exclusive CLI `--signing-key-env` / `--signing-key-file` (`0600`, non-symlink, outside repository).
  * Sealed Key Vault RBAC scope verification: `default_expected_caller_policy` fails closed on unmapped `roleId` or unrecognized `keyvault` scope descriptors and records lowercase `allowedRoleScopes` (`"vault"` vs `"secret:<name>"`); `_classify_arm_kv_scope` classifies case-insensitive ARM scopes (`"vault"`, `"secret:<name>"`, ancestor-only `"broader_parent"`, `"wrong_vault"`, `"invalid_scope"`); and `audit_keyvault_data_plane_access` flags `wrong_vault_rbac_scope` on foreign/invalid scopes and `excess_rbac_privilege` when an allowed workload holds a data-plane role at vault/subscription/RG/wrong-secret scope beyond `role-assignments.json`. Also passed `max_window_days=max(95, args.window_days)` from CLI `access-audit` so late catch-up reviews (`> 95` days) can bridge contiguous windows cleanly (ordinary local judgment preserving approved intent).
  * Sealed scheduled review window coverage, continuity, and due-date semantics: `create_signed_access_review_record` and `verify_access_review_ledger` enforce initial window coverage (`review_interval_days` unless `min_window_days` is set), gapless cross-entry continuity (`w_start <= prev_w_end < w_end`, `>= 1` day) alongside strict `reviewedAt` monotonicity, end-of-day UTC due-date evaluation (`now_utc.date() > due_date`, with matching parity in `review_status`), and an explicit `"overdue": bool` field in `verify_access_review_ledger`.
  * Updated `infra/README.md` with the newline-stripped stdout-free `az ad app credential reset ... --query password -o tsv | tr -d '\r\n' | az keyvault secret set ... --file /dev/stdin --output none` pipeline, `--signing-key-file` / `--signing-key-env` documentation, boundary-safe Python RBAC scope filter over `az role assignment list --all -o json`, and `auditDigest` SHA-256 checksum wording.

### P02: Update fixtures, add negative regression tests, and execute Focused validation

* `P02-T01` (`src/core/tests/test_secret_lifecycle.py`, `infra/tests/test_secret_lifecycle.py`):
  * Updated existing positive fixtures to match least-privilege child-secret scope (`<vault>/secrets/entra-token-store-sas` for `token-maintenance`), `signing_key=SIGNING_KEY_A` for `priorSwitchoverReceipt`, `90`-day initial coverage on `future_audit`, and contiguous `window_start=t1` (`max_window_days=120`) on the `107`-day late review fixture (`audit_late`).
  * Added focused regression tests (`test_seals_browser_mode_strict_enabled_uri_redaction_rollback_and_hmac_receipt`, `test_enforces_child_secret_rbac_scope_window_continuity_and_eod_due_date`, and `test_cli_signing_flags_browser_gate_and_runbook_command_safety`) covering `FR-S1`..`FR-S4` (`24` unit tests in `src/core/tests/test_secret_lifecycle.py` and `25` tests in `infra/tests/test_secret_lifecycle.py`, `49` total).

## Implementation Discoveries and Decisions

* Ordinary local judgment: updated `audit_late` in `test_hash_chained_ledger_verifies_key_rotation_and_detects_tampering_or_overdue_gap` to cover the contiguous `107`-day catch-up window (`window_start=t1, window_end=t_late, max_window_days=120`) and wired `max_window_days=max(95, args.window_days)` in CLI `access-audit`, ensuring late catch-up reviews satisfy gapless window continuity at signing time while still being flagged for `schedule gap 107d exceeds 90d cadence` during `verify_access_review_ledger`.

## Validation Evidence

* `PYTHONPATH=src/core/src python3 -m unittest src/core/tests/test_secret_lifecycle.py src/core/tests/test_dependency_rule.py infra/tests/test_secret_lifecycle.py -q`: `51` tests `OK` (`2.288s`).
* `PYTHONPATH=src/core/src python3 -m unittest discover -s infra/tests -q`: `637` tests `OK (skipped=4)`.
* `python3 infra/scripts/bicep_inventory.py --check`: `OK` (`29` architecture rows, `20` Bicep modules, `12` from-empty steps).
* `cd src/core && python3 -m ruff check src/zava_forward/core/secret_lifecycle.py tests/test_secret_lifecycle.py && python3 -m ruff format --check src/zava_forward/core/secret_lifecycle.py tests/test_secret_lifecycle.py && python3 -m mypy`: `All checks passed!`, `2 files already formatted`, `Success: no issues found in 363 source files`.
* `python3 -m ruff check --isolated --target-version py312 --line-length 100 --select E,F,I,B,UP infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && python3 -m ruff format --isolated --line-length 100 --check infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && MYPYPATH=src/core/src python3 -m mypy --strict --python-version 3.12 infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py`: `All checks passed!`, `2 files already formatted`, `Success: no issues found in 2 source files`.
* `! git --no-pager diff src/ infra/ | grep -q '\.copilot-tracking'`: `CLEAN_DIFF` (`0` `.copilot-tracking` strings in production/test/doc diff).
* Skipped intentionally per caller requirement: `python3 tools/rpi-checks.py --all` (Focused validation tier explicitly requested).

## Blockers and Remaining Work

* Blockers: none.
* Remaining active-plan markers: none (`P01`, `P01-T01`, `P02`, `P02-T01` complete).
* Follow-up items: live operator-attended staged Entra client-secret rotation drill in `ama` and inaugural live 90-day `AzureDiagnostics` + RBAC review ledger entry (`@jmservera`).
