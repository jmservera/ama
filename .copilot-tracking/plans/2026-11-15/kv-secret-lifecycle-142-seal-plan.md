<!-- markdownlint-disable-file -->
# RPI Plan: Verification Seal for Key Vault Secret Lifecycle (#142 Child Loop 2)

## Task Metadata

* Task ID: issue-142-seal
* Task slug: kv-secret-lifecycle-142-seal
* Parent task: issue-142-hardening (`kv-secret-lifecycle-142-hardening`)
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-seal-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-seal-plan-critique.md

## Executive Summary

This child plan seals all four findings (`RV-001`..`RV-004`) routed by `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-hardening-review.md` while keeping prior parent and first-child review artifacts immutable. It enforces `require_browser_mode=True` by default, strict boolean `enabled` parsing, redacted URI problem reporting, and HMAC-SHA256 authenticated `priorSwitchoverReceipt` verification in `verify_staged_entra_rotation`; enforces vault-versus-child-secret ARM RBAC scope boundaries from `infra/role-assignments.json` in `audit_keyvault_data_plane_access`; enforces review-window duration coverage, cross-entry continuity, and end-of-day UTC due-date evaluation in `create_signed_access_review_record` and `verify_access_review_ledger`; and replaces the stdout-printing `az ad app credential reset` runbook snippet in `infra/README.md` with a secret-safe pipeline.

### User Decisions and Requirements Highlights

* **Close `RV-001`..`RV-004` without weakening existing checks**: Eliminate rotation gate bypasses, RBAC scope escalation, 1-second/gapped review windows, and runbook credential stdout exposure before committing `feat/infra-142-kv-secret-lifecycle`.
* **Focused validation & immutable RPI trail**: Preserve all earlier `.copilot-tracking/` artifacts untouched, run Focused validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`, `bicep_inventory.py --check`), and do not run `tools/rpi-checks.py --all`, push, or open a PR.

### What You May Not Know

* **Child-secret RBAC scope parity**: In `infra/modules/authTokenStore.bicep` and `infra/resident-demo.bicep`, `token-maintenance` and `resident-demo` receive Key Vault RBAC on individual child `Microsoft.KeyVault/vaults/secrets` resources rather than the parent vault, so vault-wide RBAC on either identity is a true privilege escalation.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Deliver tested zero-downtime Entra client-secret rotation verification, scheduled recorded Key Vault data-plane access review, `infra/README.md` documentation, Focused validation, and a clean local commit on `feat/infra-142-kv-secret-lifecycle` without pushing or opening a PR (user prompt).
* Seal routed defects `RV-001`..`RV-004` from `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-hardening-review.md` while keeping prior review records untouched (RPI Agent flow; AMA Repository Instructions).

## Goals

* Ensure rotation verification, RBAC scope auditing, signed access-review ledgers, and `infra/README.md` CLI snippets fail closed against every bypass identified in `kv-secret-lifecycle-142-hardening-review.md`.
* Lock those invariants with deterministic unit and CLI regression tests and pass Focused validation cleanly.

## Scope and Non-Goals

### In Scope

* Updating `src/core/src/zava_forward/core/secret_lifecycle.py` and `infra/scripts/secret_lifecycle.py` for `RV-001`..`RV-003`.
* Updating `infra/README.md` (`### Rotate the Entra client secret` and `### Access review`) for `RV-001`, `RV-002`, and `RV-004`.
* Updating existingvault-wide `token-maintenance` test fixtures to child secret scope `/secrets/entra-token-store-sas` and adding negative regression tests in `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` (exact removals: `none`; bounded additions: targeted test methods in those 2 test files).

### Non-Goals

* Modifying Bicep templates, mutating prior `.copilot-tracking/` review artifacts, or running `tools/rpi-checks.py --all`.

## Functional Requirements

* **FR-S1 (`RV-001` / `PC-003` - Rotation browser-mode default, strict boolean `enabled`, redacted URI errors, zero-problem `rollbackVerified`, and 32-byte HMAC-authenticated `priorSwitchoverReceipt`)**:
  * `verify_staged_entra_rotation` defaults `require_browser_mode: bool = True` (CLI `rotation-verify` exposes `--allow-non-browser-mode` to opt out explicitly), records a problem whenever `require_browser_mode=True` and `browserMode is not True`, forces `effective_browser_mode = True` for probe evaluation whenever `require_browser_mode=True`, and sets `rollbackVerified = True` only when zero pre-hold `problems` exist.
  * Entra `credentials.entries[*]` (`enabled` when present, default `True` when key omitted) and Key Vault `secretVersions.entries[*]` (`enabled` / `attributes.enabled`, default `True` when omitted) deterministically record structural `problems` (treating the entry as neither active nor confirmed-disabled) if `enabled` is non-boolean or conflicts with `attributes.enabled`, and active required Entra credentials (`priorKeyId`, `nextKeyId`) must have `enabled is True`.
  * `_parse_secret_versions`, `containerApp.secrets[*].keyVaultUrl`, `containerApp.revisions[*]`, and `verify_staged_entra_rotation` never interpolate raw untrusted `id`, `keyVaultUrl`, `secretName`, or `secretVersionId` strings into `problems` messages, reporting structural index-based diagnostics instead.
  * `verify_staged_entra_rotation` accepts optional `signing_key: str | bytes | bytearray | None = None` validated via `_normalize_rotation_signing_key` (`>= 32` stripped UTF-8 bytes, never `bool`, without echoing key material; CLI `rotation-verify` exposes mutually exclusive `--signing-key-env` / `--signing-key-file` via `_resolve_rotation_signing_key` using `_read_owner_only_key_bytes`): when `signing_key` is supplied, receipts include `"signatureAlgorithm": "HMAC-SHA256"` and 64-hex `"signature"` over canonical receipt payload fields (excluding `signature` and `signatureAlgorithm`); at `post_retire`, using `priorSwitchoverReceipt` requires `signing_key`, guards `isinstance(sig, str) and bool(_HEX64_RE.match(sig))` before `hmac.compare_digest`, and enforces `stage == "post_switchover"`, `ok is True`, `safeToRetirePriorCredential is True`, `elapsedOverlapMinutes >= min_overlap_minutes`, and 8-field rotation identity binding (`credentials.retiredPriorCredential` remains supported without `signing_key`).
  * Observable acceptance criteria: `"browserMode": false` (including at `rollback`), `"enabled": "false"`, `enabled: false` on active Entra credentials, unsigned/malformed-signature/wrong-key `priorSwitchoverReceipt`, and canary-bearing `secretVersions[*].id` or `containerApp.secrets[*].keyVaultUrl` all fail safely without echoing untrusted values.
* **FR-S2 (`RV-002` / `PC-001` - Case-normalized vault vs child-secret RBAC scope enforcement & valid boundary-safe runbook export)**:
  * `default_expected_caller_policy` fails closed with `SecretLifecycleError` on unmapped `roleId` or unrecognized Key Vault `scope` descriptors in `role_matrix`, and records `allowedRoleScopes: dict[str, list[str]]` per mapped identity with lowercase secret normalization (`"vault"` for `"Key Vault"` and `"secret:<name_lower>"` for `"Secret <name> only"`, matching case-insensitive `_secret_allowed`).
  * `_classify_arm_kv_scope` matches ARM resource prefixes case-insensitively (`re.IGNORECASE`), compares `<vault>.lower() == vault_name.lower()`, normalizes child secret tokens to `"secret:<secret.lower()>"`, classifies only true ARM ancestors (`/`, management group, subscription, resource group) as `"broader_parent"`, classifies foreign vaults or sibling non-KeyVault `/providers/...` resources as `"wrong_vault"`, and flags `wrong_vault_rbac_scope` or `excess_rbac_privilege` whenever an RBAC assignment scope is invalid, foreign, broader than, or outside `allowedRoleScopes[role_name]`.
  * `infra/README.md` (`### Access review`) uses a valid standard-Azure-CLI case-insensitive `/` segment-boundary Python filter over `az role assignment list --all -o json` (avoiding non-existent JMESPath `tolower()`) so ancestor, vault, and child-secret RBAC assignments are all captured accurately.
  * Observable acceptance criteria: Mixed-case `/providers/Microsoft.KeyVault/vaults/.../secrets/Entra-Token-Store-Sas` matches cleanly, whereas `token-maintenance` at vault scope, `api` at RG scope, or sibling/foreign-vault scopes emit RBAC anomalies.
* **FR-S3 (`RV-003` / `PC-002` - Initial vs chained review window coverage, strict continuity, `"overdue"` return field, and end-of-day UTC due date)**:
  * `create_signed_access_review_record` accepts `min_window_days: int | None = None`: when `prev_entry is None`, default minimum window coverage is `review_interval_days` (`min_window_days >= 1` when explicitly passed); when `prev_entry is not None`, it parses `prev_entry["windowEnd"]`, enforces contiguous `w_start <= prev_w_end < w_end`, strict `reviewed_at > prev_reviewed_at`, and `(w_end - w_start) >= dt.timedelta(days=1 if min_window_days is None else min_window_days)` so compliant pre-deadline follow-up reviews remain valid without unreviewed gaps.
  * `verify_access_review_ledger` enforces matching initial (`idx == 0`) and chained (`idx >= 1`, including strict `reviewed_at > prev_reviewed_at` and `w_start <= prev_w_end < w_end`) window rules, evaluates `nextReviewDue` (`YYYY-MM-DD`) overdue status at end-of-day UTC (`check_now.date() > due_date`, with matching end-of-day UTC semantics in `review_status`), and includes `"overdue": overdue` (`False` when empty) in its returned dictionary alongside the overdue `problems` entry.
  * Observable acceptance criteria: 1-second initial review windows and gapped chained entries fail, compliant 82-day contiguous follow-up reviews pass, and `now` at `18:00:00Z` on `nextReviewDue` returns `overdue=False` while `00:00:00Z` the next day returns `overdue=True`.
* **FR-S4 (`RV-004` / `PC-004` - Newline-stripped stdout-free credential reset pipeline & `auditDigest` checksum semantics)**:
  * `infra/README.md` (`### Rotate the Entra client secret`, step 1) replaces bare `az ad app credential reset --id <app-id> --append ...` with a newline-stripped stdout-free pipeline (`az ad app credential reset ... --query password -o tsv | tr -d '\r\n' | az keyvault secret set ... --file /dev/stdin --output none`, retrieving `keyId` metadata via `az ad app credential list --id <app-id>`), and steps 2-3 document both `--signing-key-env` and `--signing-key-file` (`chmod 0600` outside the repository) for signed switchover receipts.
  * `infra/README.md` and `secret_lifecycle.py` docstrings clarify that `auditDigest` is a canonical SHA-256 integrity checksum bound under the human reviewer's `HMAC-SHA256` signature while preserving `rotation_plan()` step strings tested by `NoDowntimeRotationTests`.
  * Observable acceptance criteria: `infra/README.md` contains no bare stdout-printing `az ad app credential reset` command or invalid JMESPath `tolower()`, strips `\r\n` before Key Vault secret storage, and documents `--signing-key-env`/`--signing-key-file` and `auditDigest` checksum semantics.

## Non-Functional Requirements

* **NFR-S1 (Focused validation & static hygiene)**: All modified files pass `unittest` (`src/core/tests/test_secret_lifecycle.py`, `src/core/tests/test_dependency_rule.py`, `infra/tests/test_secret_lifecycle.py`), `ruff check` (project and isolated `E,F,I,B,UP`), `ruff format --check`, `mypy` (`src/core` + `mypy --strict` on `infra`), and `bicep_inventory.py --check` with zero `.copilot-tracking/` leaks in `src/` or `infra/`.
  * Objective threshold or evaluation condition: Exit code `0` across all Focused validation commands.
  * Observable acceptance criteria: Zero errors or warnings across Focused validation commands.

## Acceptance Criteria

* [x] `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, and `infra/README.md` implement `FR-S1`..`FR-S4`.
* [x] `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` cover all `FR-S1`..`FR-S4` positive and negative cases and pass Focused validation (`NFR-S1`).

## Implementation Context Record

| Context item | Current artifact or record |
|--------------|----------------------------|
| Plan | .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-seal-plan.md |
| Phase details | .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-seal-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-seal-plan-critique.md with `Revise` resolved (`PC-001`..`PC-004` applied) |
| Relevant research | .copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-seal-research.md (`SE-1`..`SE-4`); prior review `RV-001`..`RV-004` |
| Changes-record role | .copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-seal-changes.md is created by `rpi-implement` |
| Planning execution and readiness | Complete; Ready (`Planning status: ready`, all 4 critique findings applied directly) |
| Continuation context | Confirmed automatic RPI Agent child loop |

## Sources

* `.copilot-tracking/reviews/logs/2026-11-15/kv-secret-lifecycle-142-hardening-review.md`: Source `RV-001`..`RV-004` findings.
* `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-seal-research.md`: Reused evidence `SE-1`..`SE-4`.
* `infra/role-assignments.json`: Canonical Key Vault vs child-secret RBAC scope matrix.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Seal rotation verification, child-secret RBAC scope checks, ledger window continuity, and runbook commands

* Intent: Implement `FR-S1`..`FR-S4` across `src/core/src/zava_forward/core/secret_lifecycle.py`, `infra/scripts/secret_lifecycle.py`, and `infra/README.md`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update `secret_lifecycle.py` (core + CLI) and `infra/README.md` for `RV-001`..`RV-004`

* Requirement and evidence: `FR-S1`..`FR-S4`, `NFR-S1`; `SE-1`..`SE-4`.
* Expected result: `require_browser_mode=True` default, strict bool `enabled`, redacted URI problems, HMAC-signed `priorSwitchoverReceipt`, vault vs `/secrets/<name>` RBAC scope enforcement, review window coverage + cross-entry continuity + end-of-day UTC due dates, and stdout-free `az ad app credential reset` + full-scope RBAC export in `infra/README.md`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-seal-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Update fixtures, add negative regression tests, and execute Focused validation

* Intent: Align existing `token-maintenance` scope and signed-receipt fixtures with `infra/role-assignments.json` and HMAC receipt signing, add negative tests for `RV-001`..`RV-004`, and pass Focused validation.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Extend `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` and run Focused validation

* Requirement and evidence: `FR-S1`..`FR-S4`, `NFR-S1`.
* Expected result: All unit, CLI, dependency-rule, `bicep_inventory.py --check`, `ruff`, and `mypy` checks pass with zero errors.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-seal-phase-details.md

## Dependencies

* Python 3.12 stdlib, `ruff`, and `mypy` in current worktree.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` (`High`, planner) | resolved | Replaced invalid JMESPath `tolower()` in `FR-S2`, `P01-T01`, and `infra/README.md` with a boundary-safe case-insensitive Python filter over `az role assignment list --all -o json`; specified `re.IGNORECASE` ARM/vault/secret normalization, ancestor-only `"broader_parent"` classification, `wrong_vault_rbac_scope` anomaly emission, fail-closed `roleId` validation in `default_expected_caller_policy`, and mixed-case scope tests in `P02-T01`. |
| `PC-002` (`High`, planner) | resolved | Distinguished initial (`prev_entry is None`, default `review_interval_days`) vs chained (`prev_entry is not None`, contiguous `w_start <= prev_w_end < w_end` and `>= 1` day) windows in `create_signed_access_review_record`, preserved strict `reviewed_at > prev_reviewed_at`, added `"overdue"` return field to `verify_access_review_ledger` + end-of-day UTC parity in `review_status`, and added the `days=90` `future_audit` fixture update to `P02-T01`. |
| `PC-003` (`High`, planner) | resolved | Enforced 32-byte `_normalize_rotation_signing_key` and mutually exclusive CLI `_resolve_rotation_signing_key` (via `_read_owner_only_key_bytes`), `_HEX64_RE` signature guard before `hmac.compare_digest`, `effective_browser_mode=True` + zero-pre-hold-problem gate on `rollbackVerified`, active Entra `enabled is True` + conflicting `attributes.enabled` checks, and `containerApp` URI/version redaction. |
| `PC-004` (`Medium`, planner) | resolved | Added `tr -d '\r\n' \| az keyvault secret set ... --file /dev/stdin --output none` to `infra/README.md` step 1, documented `--signing-key-file` (`0600` outside repo) alongside `--signing-key-env`, and preserved `rotation_plan()` step strings. |

## Follow-Up Items

* Execute live operator-attended staged Entra client-secret rotation drill in `ama` test environment and archive sanitized `rotation-verify` receipt (owner: `@jmservera`).
* Export first live 90-day Log Analytics `AzureDiagnostics` + vault/child-secret RBAC snapshot from `ama` and record inaugural `review-sign` ledger entry (owner: `@jmservera`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-seal-changes.md
* Ready phase or task: Complete (`P01`, `P02`); ready for `rpi-review`
* Remaining provisional question or blocker: none
