<!-- markdownlint-disable-file -->
# RPI Plan: Verification Hardening for Key Vault Secret Lifecycle (#142 Child Loop)

## Task Metadata

* Task ID: issue-142-hardening
* Task slug: kv-secret-lifecycle-142-hardening
* Parent task: issue-142 (`kv-secret-lifecycle-142`)
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan-critique.md

## Executive Summary

This child plan resolves all five verification-hardening defects (`RV-001`..`RV-005`) routed by `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-review.md` while preserving the original parent critique and review records untouched. It tightens canonical `auditDigest` recomputation before signing, per-identity allowed RBAC role and vault-scope checks during `access-audit`, elapsed overlap + fresh OAuth token exchange + versioned URI + receipt-identity binding during `rotation-verify`, non-future/fresh timestamp bounds and scalar secret guards, and JSONL append safety in `infra/scripts/secret_lifecycle.py`, followed by regression tests and Focused validation.

### User Decisions and Requirements Highlights

* **Resolve `RV-001`..`RV-005` completely**: Close every verification bypass found during independent review of `issue-142` without expanding scope into Bicep or live Azure mutations.
* **Preserve original RPI evidence & Focused validation boundary**: Keep `kv-secret-lifecycle-142-review.md` untouched, run Focused validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `bicep_inventory.py --check`), and do not run `tools/rpi-checks.py --all`, push, or open a PR.

### What You May Not Know

* **Receipt identity binding**: Binding `{vaultName, appId, secretName, priorSecretName, priorKeyId, nextKeyId, priorVersionId, nextVersionId}` into `rotation-verify` output makes `priorSwitchoverReceipt` self-verifying during `post_retire` without requiring raw secret material.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Complete the full RPI loop for Issue #142 with deterministic unit tests, `ruff`, and `mypy`, and commit cleanly on `feat/infra-142-kv-secret-lifecycle` without pushing or opening a PR (user prompt).
* Resolve routed findings `RV-001`..`RV-005` from `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-review.md` via child RPI loop while preserving original review outcomes (RPI Agent flow; AMA Repository Instructions).

## Goals

* Eliminate forged-digest, excess-RBAC, wrong-vault diagnostic, premature-retirement, stale-cookie auth-probe, missing-URI, unbound-receipt, future-timestamp, scalar-leak, and JSON-array append edge cases across `zava_forward.core.secret_lifecycle` and `infra/scripts/secret_lifecycle.py`.
* Add focused negative regression tests for all five `RV-xxx` classes and keep documentation and Focused validation 100% synchronized.

## Scope and Non-Goals

### In Scope

* Updating `src/core/src/zava_forward/core/secret_lifecycle.py` and `infra/scripts/secret_lifecycle.py` to resolve `RV-001`..`RV-005`.
* Updating `infra/README.md` (`### Rotate the Entra client secret`) to document `freshTokenExchangeVerified` and elapsed overlap gating accurately.
* Adding focused regression tests in `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` (exact test removals: `none`; bounded additions: targeted methods in those 2 test files) and running Focused validation.

### Non-Goals

* Mutating parent `kv-secret-lifecycle-142-*` artifacts, modifying Bicep templates, or running `tools/rpi-checks.py --all`.

## Functional Requirements

* **FR-H1 (`RV-001` - Canonical `auditDigest` recomputation & unique IDs)**: `audit_keyvault_data_plane_access` normalizes `windowStart`/`windowEnd` to UTC and deduplicates emitted `anomalyId` and identical RBAC tuples, while `create_signed_access_review_record` validates `callerSummaries` (`list`) and `systemNotificationCount` (non-boolean `int >= 0`), rejects non-mapping rows or duplicate `assignmentId` / `anomalyId` entries in `audit`, and recomputes canonical `auditDigest` over `{vaultName, windowStart, windowEnd, rbacAssignments, callerSummaries, anomalies, systemNotificationCount}`, raising `SecretLifecycleError` if `audit["auditDigest"]` does not match.
  * Observable acceptance criteria: Removing or altering an anomaly or RBAC row in an `audit` payload while retaining the prior `auditDigest` raises `SecretLifecycleError`, whereas multi-row foreign-vault diagnostics produce deduplicated signable anomalies.
* **FR-H2 (`RV-002` - Per-identity allowed RBAC roles & diagnostic vault scope)**: `default_expected_caller_policy` records `allowedRoles` per mapped identity from `infra/role-assignments.json`, and `audit_keyvault_data_plane_access` flags `excess_rbac_privilege` when an allowed workload holds a data-plane RBAC role outside its `allowedRoles` (for example `api` with `Key Vault Secrets Officer`) and validates diagnostic vault scope prior to `PLATFORM_NOTIFICATION_OPS` skipping—requiring at least one vault-identifying field (`id_s`, `requestUri_s`, `ResourceId`, `_ResourceId`, `resourceId`) and verifying every present URI (`https://<vault>.vault.azure.net/...`) and ARM resource ID (`.../providers/Microsoft.KeyVault/vaults/<vault>...`) matches `vault_name` (`wrong_vault_diagnostic`).
  * Observable acceptance criteria: Unit tests assert `excess_rbac_privilege` for `api` with `Key Vault Secrets Officer` and deduplicated `wrong_vault_diagnostic` for foreign-vault, non-KeyVault URI, and stripped-URI rows.
* **FR-H3 (`RV-003` - Elapsed overlap, fresh OAuth exchange, mandatory versioned URIs, and bound `post_retire` receipts)**: `verify_staged_entra_rotation` includes `elapsedOverlapMinutes` in receipts and appends a `problems` failure (keeping `ok=False` and CLI exit `1`) whenever `elapsedOverlapMinutes < min_overlap_minutes` at `post_switchover`, enforces `retiredAt <= now` and capped pre-retirement overlap on `retiredPriorCredential`, requires boolean `browserMode` and `freshTokenExchangeVerified is True` alongside `authenticatedApiStatus == 200` on `post_switchover` and `post_retire` when `browserMode=True` (without breaking `rollback` probe validation), sets `before_kv_problems` before parsing `secretVersions.entries` while requiring versioned `https://<vault>.vault.azure.net/secrets/<secret>/<version>` `id` URIs without `row["secretName"]` masking, and validates `priorSwitchoverReceipt` after `secretVersions` IDs are parsed against `{vaultName, appId, secretName, priorSecretName, priorKeyId, nextKeyId, priorVersionId, nextVersionId}` plus `elapsedOverlapMinutes >= min_overlap_minutes`.
  * Observable acceptance criteria: 1-second elapsed overlap at `post_switchover`, future `retiredAt` at `post_retire`, missing `freshTokenExchangeVerified`, missing/conflicting version URI, and cross-rotation `priorSwitchoverReceipt` each fail verification with `ok=False` and `safeToRetirePriorCredential=False`.
* **FR-H4 (`RV-004` & `RV-005` - Scalar secret guards, review freshness bounds, and JSONL append guard)**: `access_review` (`reviewer` without rejecting short legacy `"R"`), `rotation_plan` (`vault`, `app_id`), `validate_human_reviewer`, and vault-name inputs run `assert_no_secret_material`; `create_signed_access_review_record` and `verify_access_review_ledger` safely validate non-boolean integer `reviewIntervalDays` (`1..max_interval_days`) and enforce `windowStart < windowEnd <= reviewedAt`, `(reviewedAt - windowEnd) <= max_interval_days`, `reviewedAt <= now` (in `verify_access_review_ledger`), and `nextReviewDue == (reviewedAt + reviewIntervalDays).date().isoformat()`; and `infra/scripts/secret_lifecycle.py` (`main()` `review-sign` + `_append_jsonl_entry`) rejects JSON `[...]` array `--ledger` files for append and preserves newline framing when an existing JSONL file lacks a trailing `\n`.
  * Observable acceptance criteria: Canary tokens in `reviewer`/`vault`/`app_id` raise `SecretExposureError`; future `reviewedAt`, stale `windowEnd`, malformed `reviewIntervalDays`, forged `nextReviewDue`, and `[...]` array `--ledger` append all fail deterministically.

## Non-Functional Requirements

* **NFR-H1 (Strict static typing, lint cleanliness, and inventory stability)**: All modified files pass `ruff check` (default and isolated `E,F,I,B,UP`), `ruff format --check`, `mypy` (`src/core` + `mypy --strict` on `infra`), `test_dependency_rule.py`, and `bicep_inventory.py --check`.
  * Objective threshold or evaluation condition: Exit code `0` across all Focused validation checks.
  * Observable acceptance criteria: Zero errors or warnings across Focused validation commands.

## Acceptance Criteria

* [x] `src/core/src/zava_forward/core/secret_lifecycle.py` and `infra/scripts/secret_lifecycle.py` enforce `FR-H1`..`FR-H4`.
* [x] `src/core/tests/test_secret_lifecycle.py`, `infra/tests/test_secret_lifecycle.py`, and `infra/README.md` cover all hardened invariants and pass Focused validation (`NFR-H1`).

## Implementation Context Record

| Context item | Current artifact or record |
|--------------|----------------------------|
| Plan | .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-hardening-plan-critique.md with `Revise` resolved (`PC-001`..`PC-003` applied) |
| Relevant research | .copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-hardening-research.md (`HE-1`..`HE-5`); parent review `RV-001`..`RV-005` |
| Changes-record role | .copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-hardening-changes.md is created by `rpi-implement` |
| Planning execution and readiness | Complete; Ready (`Planning status: ready`, all 3 critique findings resolved directly) |
| Continuation context | Confirmed automatic RPI Agent child loop |

## Sources

* `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-review.md`: Source `RV-001`..`RV-005` findings.
* `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-hardening-research.md`: Reused symbol-level design notes (`HE-1`..`HE-5`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden domain verifiers, CLI ledger append guard, and operator documentation

* Intent: Resolve `RV-001`..`RV-005` across `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, and `infra/README.md`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `RV-001`..`RV-005` hardening in `secret_lifecycle.py` (core + CLI) and `infra/README.md`

* Requirement and evidence: `FR-H1`..`FR-H4`, `NFR-H1`; `HE-1`..`HE-5`.
* Expected result: Canonical `auditDigest` recomputation, `allowedRoles` + `wrong_vault_diagnostic` checks, elapsed overlap + `freshTokenExchangeVerified` + strict versioned URI + bound `priorSwitchoverReceipt` verification, review freshness/due-date bounds, scalar secret guards, JSONL append guard, and synchronized `infra/README.md` wording.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Add negative regression tests and run Focused validation

* Intent: Prove every `RV-001`..`RV-005` bypass fails closed and re-verify `unittest`, `ruff`, `mypy`, and `bicep_inventory.py --check`.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Extend `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` and execute Focused validation

* Requirement and evidence: `FR-H1`..`FR-H4`, `NFR-H1`.
* Expected result: Regression tests cover every `RV-001`..`RV-005` failure mode and all Focused validation checks exit `0`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-hardening-phase-details.md

## Dependencies

* Python 3.12 stdlib, `ruff`, and `mypy` in current worktree.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` (`High`, planner) | resolved | Updated `FR-H3`, `P01-T01`, and `P02-T01` to include `elapsedOverlapMinutes` in receipts, append a `problems` failure on insufficient elapsed overlap at `post_switchover`, enforce `retiredAt <= now` on `retiredPriorCredential`, validate `priorSwitchoverReceipt` after `secretVersions` IDs are parsed (including `elapsedOverlapMinutes >= min_overlap_minutes`), and move `before_kv_problems` before `secretVersions.entries` parsing. |
| `PC-002` (`High`, planner) | resolved | Updated `FR-H1`, `FR-H2`, `P01-T01`, and `P02-T01` to deduplicate `anomalyId` and identical RBAC tuples, validate diagnostic vault scope before `PLATFORM_NOTIFICATION_OPS` skipping across all URI/ARM fields (rejecting missing/non-KeyVault identifiers), normalize `windowStart`/`windowEnd` to UTC, and validate `callerSummaries`/`systemNotificationCount` types before `_compute_audit_digest`. |
| `PC-003` (`Medium`, planner) | resolved | Updated `FR-H3`, `FR-H4`, `P01-T01`, and `P02-T01` to separate `require_fresh_token_exchange` from `rollback`, validate boolean `browserMode`, update CLI `_rotation_payload` fixtures, guard `validate_human_reviewer` and vault-name scalars while keeping legacy `"R"` compatibility in `access_review`, safely parse non-boolean integer `reviewIntervalDays`, and enforce `[` array rejection + missing-newline handling in `main()`/`_append_jsonl_entry`. |

## Follow-Up Items

* Execute live operator-attended staged Entra client-secret rotation drill in `ama` test environment and archive sanitized `rotation-verify` receipt (outside offline repository CI scope; owner: `@jmservera`).
* Export first live 90-day Log Analytics `AzureDiagnostics` + vault RBAC snapshot from `ama` and record inaugural `review-sign` ledger entry (outside offline repository CI scope; owner: `@jmservera`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-hardening-changes.md
* Ready phase or task: Review (`P01` and `P02` completed)
* Remaining provisional question or blocker: none
