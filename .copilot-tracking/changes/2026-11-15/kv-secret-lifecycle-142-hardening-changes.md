---
title: Changes Record - Key Vault Secret Lifecycle Verification Hardening (#142)
description: Implementation evidence for resolving parent rpi-review findings RV-001..RV-005 on Key Vault secret lifecycle verification and access review recording
author: Copilot
ms.date: 2026-11-15
ms.topic: reference
---

## Metadata

* Plan: .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan-critique.md
* Declared scope: Full plan (`P01`, `P02`)
* Execution status: completed

## Summary

Resolving parent `rpi-review` findings `RV-001`..`RV-005` and child plan critique findings `PC-001`..`PC-003` across `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, `infra/README.md`, `src/core/tests/test_secret_lifecycle.py`, and `infra/tests/test_secret_lifecycle.py`.

## Phase Evidence

### P01: Harden Core Verification, Access Review Integrity & CLI Ledger Guard

* Status: completed (`P01-T01` complete)
* Files modified:
  * `src/core/src/zava_forward/core/secret_lifecycle.py`:
    * `RV-001` / `PC-002`: Normalized `windowStart`/`windowEnd` to UTC, deduplicated emitted `anomalyId` and identical RBAC tuples, extracted `_compute_audit_digest`, and added type/uniqueness validation plus canonical `auditDigest` recomputation inside `create_signed_access_review_record`.
    * `RV-002` / `PC-002`: Populated `allowedRoles` per mapped identity in `default_expected_caller_policy`, added `excess_rbac_privilege` detection when a mapped identity holds a data-plane RBAC role outside its `allowedRoles`, and added `_validate_diag_row_vault` prior to `PLATFORM_NOTIFICATION_OPS` skipping to reject missing, non-KeyVault, or foreign-vault diagnostic identifiers (`wrong_vault_diagnostic`).
    * `RV-003` / `PC-001` / `PC-003`: Added boolean `browserMode` validation, `elapsedOverlapMinutes` computation and `post_switchover` failure enforcement, `retiredAt <= now` and pre-retirement overlap validation on `retiredPriorCredential`, mandatory versioned Key Vault `id` URI validation without `row["secretName"]` masking (setting `before_kv_problems` before `secretVersions` parsing), post-`secretVersions` 8-field identity binding on `priorSwitchoverReceipt`, and `freshTokenExchangeVerified is True` enforcement on `post_switchover`/`post_retire` probes when `browserMode=True` (keeping `rollback` compatible).
    * `RV-004` / `PC-003`: Added `assert_no_secret_material` scalar guards on `validate_human_reviewer`, `access_review`, `rotation_plan`, `audit_keyvault_data_plane_access`, and `verify_access_review_ledger`, and added safe `reviewIntervalDays` and `windowStart < windowEnd <= reviewedAt <= now` + `nextReviewDue` freshness/derivation checks.
  * `infra/scripts/secret_lifecycle.py`:
    * `RV-005` / `PC-003`: Added `_ensure_jsonl_ledger_target` in `review-sign` and `_append_jsonl_entry` to refuse appending to `[...]` JSON array files (`exit 2`), and preserved JSONL line framing when an existing non-empty file lacks a trailing newline.
  * `infra/README.md`:
    * Documented `elapsedOverlapMinutes >= 60` and `"freshTokenExchangeVerified": true` in step 2 under `### Rotate the Entra client secret`.

### P02: Add Negative Regression Tests & Focused Validation

* Status: completed (`P02-T01` complete)
* Files modified:
  * `src/core/tests/test_secret_lifecycle.py` (22 tests):
    * Added negative regression tests covering forged `auditDigest` (`RV-001`), duplicate RBAC/anomaly IDs (`RV-001`/`PC-002`), `excess_rbac_privilege` when `api` holds `Key Vault Secrets Officer` (`RV-002`), `wrong_vault_diagnostic` on foreign-vault, non-KeyVault, and stripped-URI diagnostic rows (`RV-002`/`PC-002`), insufficient `elapsedOverlapMinutes` at `post_switchover` (`RV-003`/`PC-001`), future `retiredAt` at `post_retire` (`PC-001`), missing `freshTokenExchangeVerified` on `post_switchover`/`post_retire` while preserving `rollback` (`RV-003`/`PC-003`), missing/conflicting versioned Key Vault URIs without `secretName` masking (`RV-003`/`PC-001`), unbound cross-rotation `priorSwitchoverReceipt` (`RV-003`/`PC-001`), canary tokens in scalar `reviewer`/`vault`/`app_id` parameters (`RV-004`/`PC-003`), and future `reviewedAt`, stale `windowEnd`, malformed/boolean `reviewIntervalDays`, and forged `nextReviewDue` (`RV-004`/`PC-003`).
  * `infra/tests/test_secret_lifecycle.py` (24 tests):
    * Updated rotation CLI probe fixtures for `freshTokenExchangeVerified`, added CLI regression tests for `[...]` JSON array `--ledger` refusal (`exit 2`) and newline-preserving JSONL append when an existing ledger file lacks a trailing newline (`RV-005`/`PC-003`).

## Implementation Discoveries and Decisions

* Local judgment (`NFR-H1` lint alignment): Simplified `parse_time`, `_secret_allowed`, and `firstSeen`/`lastSeen` clamping in `src/core/src/zava_forward/core/secret_lifecycle.py` so both `src/core` `ruff check .` and isolated `ruff` rule sets pass with zero warnings.

## Validation

* `PYTHONPATH=src/core/src python3 -m unittest src/core/tests/test_secret_lifecycle.py src/core/tests/test_dependency_rule.py infra/tests/test_secret_lifecycle.py -q`: `Ran 48 tests in 2.441s - OK`.
* Expanded targeted suite (`test_secret_lifecycle` core + infra, `test_dependency_rule`, `test_identity_rbac`, `test_diagnostic_log_privacy`, `test_bicep_architecture_inventory_136`, `test_bicep_policy`): `Ran 138 tests in 91.329s - OK`.
* `PYTHONPATH=src/core/src python3 -m unittest discover -s infra/tests -q`: `Ran 636 tests in 233.297s - OK (skipped=4)`.
* `python3 infra/scripts/bicep_inventory.py --check`: `Issue #136 Bicep inventory verified: 29 architecture rows, 20 Bicep modules, 12 from-empty steps (17 rebuild stages)`.
* `(cd src/core && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m mypy)`: `All checks passed!`, `310 files already formatted`, `Success: no issues found in 363 source files`.
* `python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && python3 -m ruff format --isolated --line-length 100 --check infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py && MYPYPATH=src/core/src python3 -m mypy --strict infra/scripts/secret_lifecycle.py infra/tests/test_secret_lifecycle.py`: `All checks passed!`, `2 files already formatted`, `Success: no issues found in 2 source files`.
* `git --no-pager diff -U0 -- src/ infra/ | grep -i "copilot-tracking"`: `ZERO_MATCHES_IN_DIFF`.
* `tools/rpi-checks.py --all`: Skipped by explicit user instruction (Focused validation tier).

## Blockers and Remaining Work

* Blockers: none
* Remaining work in declared scope: none (`P01` and `P02` completed)

## Follow-Up Items

* Execute live operator-attended staged Entra client-secret rotation drill in `ama` test environment and archive sanitized `rotation-verify` receipt (owner: `@jmservera`).
* Export first live 90-day Log Analytics `AzureDiagnostics` + vault RBAC snapshot from `ama` and record inaugural `review-sign` ledger entry (owner: `@jmservera`).

## Review Readiness

* Reconciled and ready for independent `rpi-review`.
