<!-- markdownlint-disable-file -->
# RPI Plan: Key Vault Secret Lifecycle Rotation Verification and Scheduled Access Review (#142)

## Task Metadata

* Task ID: issue-142
* Task slug: kv-secret-lifecycle-142
* Planning status: ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-plan-critique.md

## Executive Summary

This plan delivers the engineering verification harnesses, CLI workflows, deterministic unit tests, and operational documentation required for the two remaining acceptance criteria on **Issue #142** (*Key Vault secret lifecycle: rotation, expiry and access review*). While earlier work (`PR #265`) introduced `infra/secret-inventory.json`, Bicep alerts in `infra/modules/keyvault.bicep`, a static 5-token ordering simulator, and an unsigned pending RBAC review template, closure audits kept #142 open because string-order assertions do not verify dual-secret overlap windows, Key Vault version switchover, zero-downtime probe continuity, or rollback safety, and RBAC-only snapshots do not audit data-plane operations, detect unexpected callers, or persist signed scheduled review ledger records.

We will add a strictly typed, zero-dependency domain module `src/core/src/zava_forward/core/secret_lifecycle.py` and wire its workflows into `infra/scripts/secret_lifecycle.py`, backed by deterministic unit tests in `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` plus updated procedures and contracts in `infra/README.md`.

### User Decisions and Requirements Highlights

* **Dual-secret zero-downtime Entra rotation verification**: Verify Entra `passwordCredentials` overlap windows, Key Vault secret version metadata and Container Apps revision secret-reference switchover (including staged two-name `priorSecretName` -> `secretName` handoffs), continuous health/auth probes (`/healthz` `200`, anonymous `/api/me` `401`, `/sign-in` `302`, and mandatory post-switchover authenticated session/callback `200` proving live `entra-client-secret` token exchange), and rollback blocking of old-credential deletion without ever reading or printing secret values.
* **Scheduled Key Vault data-plane access review recording**: Audit caller principal IDs and operations across RBAC assignments and Log Analytics `AzureDiagnostics` events against fail-closed expected-principal mappings (`infra/role-assignments.json`) and `infra/secret-inventory.json`, separate OID-less platform Event Grid notifications from `<anonymous>` secret access, flag unexpected callers, out-of-scope operations, any `403` and `>= 5` `401` bursts, and record vault-bound, audit-digest-bound HMAC-SHA256 signed, SHA-256 hash-chained review ledger entries attested by a named human reviewer on a 90-day schedule using non-symlink `0600` key files outside the repository.
* **Focused validation & local commit boundary**: Run unit tests (`src/core` and `infra`), `ruff check`, `ruff format --check`, and `mypy` without running `tools/rpi-checks.py --all`, and commit cleanly on `feat/infra-142-kv-secret-lifecycle` without pushing or opening a PR.

### What You May Not Know

* **Bicep & inventory guardrails**: `infra/tests/test_diagnostic_log_privacy.py` forbids explicit `AuditEvent` category toggles while allowing `keyvault.bicep`'s existing `categoryGroup: 'allLogs'`, and `infra/scripts/bicep_inventory.py` parses structured Markdown tables in `infra/README.md`. Keeping `keyvault.bicep` and the `#136` Markdown tables untouched avoids collateral regressions.
* **Shared-worktree Python isolation**: In this shared environment, global site-packages resolves `zava_forward.core` to `/home/azureuser/source/ama/src/core/src`. Prepending the local worktree's `src/core/src` inside `infra/scripts/secret_lifecycle.py` and `PYTHONPATH` during validation keeps tests hermetic without altering shared host packages.
* **Honest operational boundary**: Offline deterministic verification proves overlap, switchover, rollback gating, caller anomaly detection, and cryptographic ledger integrity without claiming that a live Azure tenant/vault mutation was executed during repository CI.

### Unresolved Decisions or Blockers

* None blocking implementation. Live Azure execution of the documented Entra rotation runbook and inaugural live quarterly Log Analytics export remain post-merge operator actions owned by `@jmservera` (recorded in [Follow-Up Items](#follow-up-items)).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Deliver engineering implementation, deterministic tests, and documentation for Issue #142 (*Key Vault secret lifecycle: rotation, expiry and access review*) on branch `feat/infra-142-kv-secret-lifecycle` stacked onto `feat/demo-164-chat-grounding-provenance-0900` (user prompt; Issue #142).
* Research and align with existing Key Vault helpers, `infra/modules/keyvault.bicep`, `infra/scripts/`, `infra/README.md`, and `src/core` modules (user prompt; `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-research.md`).
* Implement and test zero-downtime dual-secret / staged Entra client-secret rotation verification covering overlap window, secret reference version switchover, and rollback / zero-downtime health validation without secret exposure (user prompt; Issue #142 criterion 2).
* Implement and test scheduled Key Vault data-plane access review recording covering principal ID auditing, operation auditing, unexpected caller detection, and signed review ledger records (user prompt; Issue #142 criterion 3).
* Document the zero-downtime Entra client secret rotation procedure and scheduled Key Vault data-plane access review contract in `infra/README.md` (user prompt).
* Add deterministic unit tests in `infra/tests/` and `src/core/tests/`, validate under the Focused tier (`unittest`, `ruff check`, `ruff format --check`, `mypy`; do not run `tools/rpi-checks.py --all`), and commit all code + `.copilot-tracking/` artifacts locally with the Copilot `Co-authored-by` trailer without pushing or opening a PR (user prompt).

## Goals

* Provide a pure, strictly typed lifecycle verification and signed access-review ledger module in `zava_forward.core.secret_lifecycle` usable by both `src/core` and `infra/scripts/secret_lifecycle.py`.
* Verify staged zero-downtime Entra client-secret rotations end-to-end across Entra credential overlap windows, Key Vault version metadata, Container Apps secret-reference/revision switchover, health/auth probe continuity, and rollback safety while failing closed on any raw secret material.
* Audit Key Vault data-plane principal IDs, operations, target secrets, and status codes against the repository's least-privilege RBAC contract and record tamper-evident, HMAC-SHA256 signed, SHA-256 hash-chained quarterly review ledgers with named human accountability.
* Document clear, honest operator procedures and CLI contracts in `infra/README.md` without breaking existing `#136` inventory or `#141`/`#146` Bicep tests.

## Scope and Non-Goals

### In Scope

* Creating `src/core/src/zava_forward/core/secret_lifecycle.py` with staged Entra rotation verification, data-plane access auditing, unexpected-caller detection, signed hash-chained review ledger creation/verification, and fail-closed secret-exposure guards.
* Extending `infra/scripts/secret_lifecycle.py` with `rotation-verify`, `access-audit`, `review-sign`, and `ledger-verify` CLI subcommands while preserving 100% compatibility with existing `check`, `review`, `rotation-plan`, `rotation-simulate`, and `review-status` functions and subcommands.
* Adding deterministic unit tests in `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` (exact test removals: `none`; bounded additions: 1 new core test file + targeted test classes in existing `infra/tests/test_secret_lifecycle.py`).
* Updating `infra/README.md` (`Layout` and `## Key Vault secret lifecycle`) with the staged zero-downtime Entra client-secret rotation procedure, rollback rules, and scheduled 90-day data-plane access review & signed ledger contract.

### Non-Goals

* Modifying `infra/modules/keyvault.bicep`, `infra/role-assignments.json`, or structured `#136` Markdown inventory tables in `infra/README.md`.
* Executing live Azure CLI commands against the `ama` subscription or Entra tenant, reading or storing real secrets, or fabricating live cloud execution claims.
* Running `tools/rpi-checks.py --all`, mutating global host `pip` installations, pushing to `origin`, or opening a pull request.

## Functional Requirements

* **FR-1 (Fail-closed zero-secret guard)**: Lifecycle rotation and access-review functions (including `verify_access_review_ledger`) reject any input mapping, list, or URI containing raw secret keys (`value` outside top-level ARM `{"value": [...]}` metadata list envelopes, `secretText`, `password`, `clientSecret`, `secretValue`, `cookie`, `token`, `accessToken`, `refreshToken`, `sas`, `connectionString`) or targeted credential-bearing strings (`?sig=`, `&sig=`, `?sv=`, `Bearer `, `Basic `, 3-segment JWT `eyJ...`, `sk-`, `SharedAccessSignature`, `AccountKey=`) by raising `SecretExposureError` without echoing the secret material and without colliding with 32/64-hex version IDs or SHA-256 digests.
  * Observable acceptance criteria: Unit tests pass canary secret literals in forbidden fields and query strings across rotation, audit, sign, and ledger-verify paths and assert `SecretExposureError` is raised (`CLI exit 2`) while the canary substring appears nowhere in exception text, stdout, stderr, or output JSON.
* **FR-2 (Zero-downtime dual-secret Entra rotation verification)**: `verify_staged_entra_rotation` and `secret_lifecycle.py rotation-verify` validate Entra `passwordCredentials` overlap (`overlap_minutes >= min_overlap_minutes`, default `60`, bounded new secret lifetime `<= 366` days), Key Vault prior/next version metadata (`enabled`, `expires`, versioned secret URI match across in-place `secretName` or staged `priorSecretName` -> `secretName` handoffs), Container Apps active revision secret binding (`keyVaultUrl`, API managed identity, `clientSecretSettingName`, serving revision health and replica readiness, presented version transition), continuous probe results (`/healthz == 200`, anonymous `/api/me == 401`, browser `/sign-in == 302`, mandatory `authenticatedApiStatus == 200` on `post_switchover` and `post_retire` when `browserMode=True` to prove live Entra `client_secret` exchange, zero `5xx` or auth-drop samples), rollback restoration when post-switchover fails, strict `safeToRetirePriorCredential` gating (`True` if and only if `stage == "post_switchover"` and `ok is True`), and `post_retire` cleanup (`prior_key_id` deleted after verifiable pre-retirement overlap metadata or matching `post_switchover` receipt digest, `prior_version_id` disabled).
  * Observable acceptance criteria: Valid overlap/switchover/post-retire fixtures pass with `zeroDowntimeVerified=True` and sanitized `evidenceDigest`; omitting `authenticatedApiStatus == 200` at `post_switchover`, premature deletion, insufficient overlap, unrefreshed revision, `302`/`200` on anonymous `/api/me`, or `5xx` probe failures fail forward verification, validate clean rollback when `prior_key_id`/`prior_version_id` remain active, and keep `safeToRetirePriorCredential=False` across `dual_secret_overlap`, failed `post_switchover`, `rollback`, and `post_retire`.
* **FR-3 (Key Vault data-plane access auditing & unexpected caller detection)**: `audit_keyvault_data_plane_access` and `secret_lifecycle.py access-audit` correlate RBAC assignments and Log Analytics `AzureDiagnostics` data-plane events over the review window against fail-closed expected caller rules derived from `infra/role-assignments.json` + explicit `principal_map` (`api`, `token-maintenance`, `resident-demo`, and forbidden `agents`/`orchestrator`/`import`, never auto-trusting unmapped OIDs from live `assignments`), separate OID-less platform Event Grid notifications (`SecretNearExpiryEventGridNotification`, `SecretExpiredEventGridNotification`) from `<anonymous>` data-plane secret operations, and summarize per-principal operations, secret names, and HTTP status codes while flagging `unexpected_caller`, `unmapped_rbac_principal`, `forbidden_workload_caller`, `unexpected_operation`, `out_of_scope_secret`, `denied_access_activity` (any `403` or `401` count `>= denied_401_threshold`, default `5`), and `unclassified_rbac_role`.
  * Observable acceptance criteria: Deterministic fixtures verify clean authorized traffic (including OID-less Event Grid expiry notifications and isolated `< 5` OAuth preflight `401`s) yields zero caller anomalies, while unlisted/unmapped OIDs, `<anonymous>` `SecretGet`, `agents` identity calls, `api` write/purge operations, `token-maintenance` reads of `entra-client-secret`, any `403`, `>= 5` `401` bursts, and broad `Contributor` RBAC assignments each emit typed anomaly records.
* **FR-4 (Signed, hash-chained scheduled review ledger)**: `create_signed_access_review_record`, `verify_access_review_ledger`, `secret_lifecycle.py review-sign`, and `secret_lifecycle.py ledger-verify` enforce non-placeholder, non-automated human reviewer naming, bind `vaultName`, `windowStart`, `windowEnd`, and canonical `auditDigest`, require 1-to-1 keyed `keep`/`remove` assignment decisions and anomaly dispositions (`remediated`/`revoked`/`accepted_exception`) with rationale covering every audited item, chain records via SHA-256 (`prevHash` -> `entryHash` from `GENESIS_HASH`), sign records with HMAC-SHA256 (`signingKeyId`, `signature`) from a non-symlink, outside-repository owner-only (`0600`) key file never stored in the ledger, and verify chain integrity, cross-entry `vaultName` continuity, constant-time signature validity against a `0600` non-symlink outside-repo `--keys-file` (`{"<key_id>": "<key>"}`), 90-day schedule cadence across consecutive reviews, and non-overdue `nextReviewDue`.
  * Observable acceptance criteria: Multi-entry signed ledgers verify cleanly (`intact=True`, exit code `0`), whereas placeholder/bot reviewers, missing/unmatched assignment or anomaly IDs, mismatched `vaultName`, tampered payload bytes, broken `prevHash`, wrong HMAC key, >90-day inter-review schedule gaps, overdue `nextReviewDue`, symlinks, repo-resident key paths, or world-readable signing/verification key files fail deterministically with non-zero exit status.
* **FR-5 (Backward-compatible CLI & accurate documentation)**: `infra/scripts/secret_lifecycle.py` retains all existing functions and subcommands (`check`, `review`, `rotation-plan`, `rotation-simulate`, `review-status`), and `infra/README.md` documents both the staged zero-downtime Entra rotation workflow (including rollback and verification commands) and the scheduled 90-day data-plane access review & signed ledger contract while preserving honest live-Azure vs offline boundaries.
  * Observable acceptance criteria: All 19 pre-existing tests in `infra/tests/test_secret_lifecycle.py` and all 8 tests in `infra/tests/test_bicep_architecture_inventory_136.py` continue to pass unchanged alongside the new test suites.

## Non-Functional Requirements

* **NFR-1 (Zero credential exposure & key-file hygiene)**: No secret value, bearer token, SAS signature, or HMAC signing key may appear in return payloads, ledger files, stdout/stderr, or exception messages; CLI `review-sign` and `ledger-verify` read keys only from regular, non-symlink, outside-repository owner-restricted (`0600`) files (refusing CLI flag literals, symlinks, repository-resident paths, and world/group-readable key files on POSIX).
  * Objective threshold or evaluation condition: `0` occurrences of canary secret/key strings across all outputs and raised exceptions; symlinks, paths inside repository root, or POSIX mode `(st_mode & 0o077) != 0` rejected for `--key-file` and `--keys-file`.
  * Operating condition or verification approach, if needed: Verified via negative unit tests in both `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py`.
  * Observable acceptance criteria: Secret-canary and insecure-key-mode tests pass with 100% redaction/refusal.
* **NFR-2 (Strict static typing, lint cleanliness, and dependency isolation)**: All new and modified Python files satisfy Python 3.12 `ruff check` (`E,F,I,B,UP`, line-length 100), `ruff format --check`, `mypy --strict` (without adding `ignore_errors` overrides in `src/core/pyproject.toml`), and `src/core/tests/test_dependency_rule.py` (stdlib + `zava_forward.core` imports only).
  * Objective threshold or evaluation condition: Exit code `0` on `ruff check`, `ruff format --check`, `mypy`, and `test_dependency_rule.py`.
  * Operating condition or verification approach, if needed: Executed from worktree directories using worktree-isolated `PYTHONPATH` without modifying shared global site-packages.
  * Observable acceptance criteria: Focused validation commands exit `0` with zero warnings or errors.

## Acceptance Criteria

* [x] `src/core/src/zava_forward/core/secret_lifecycle.py` implements zero-secret guards, staged Entra rotation verification (overlap, version switchover, probes, rollback, retirement gating), `AzureDiagnostics` + RBAC data-plane access auditing with unexpected-caller detection, and HMAC-SHA256 signed, SHA-256 hash-chained scheduled review ledgers (`FR-1`..`FR-4`, `NFR-1`, `NFR-2`).
* [x] `infra/scripts/secret_lifecycle.py` exposes `rotation-verify`, `access-audit`, `review-sign`, and `ledger-verify` while keeping existing `check`, `review`, `rotation-plan`, `rotation-simulate`, and `review-status` interfaces backward compatible (`FR-2`..`FR-5`, `NFR-1`, `NFR-2`).
* [x] Deterministic unit tests in `src/core/tests/test_secret_lifecycle.py` and `infra/tests/test_secret_lifecycle.py` pass and cover overlap/switchover/rollback, secret-exposure refusal, unexpected/forbidden callers, human reviewer validation, ledger tampering/signature/schedule enforcement, and CLI exit codes (`FR-1`..`FR-5`, `NFR-1`).
* [x] `infra/README.md` documents the zero-downtime staged Entra client-secret rotation procedure and scheduled Key Vault data-plane access review & signed ledger contract accurately without breaking `bicep_inventory.py --check` (`FR-5`).
* [x] Focused validation (`src/core` unit tests + `test_dependency_rule.py`, `infra/tests` suite, `ruff check`, `ruff format --check`, and `mypy --strict`) passes cleanly, ready for `rpi-review` and local commit on `feat/infra-142-kv-secret-lifecycle` with the Copilot trailer and without pushing or opening a PR (`NFR-2`).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                                 |
|----------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/kv-secret-lifecycle-142-plan.md                                                                         |
| Phase details                    | .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-phase-details.md                                                              |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/kv-secret-lifecycle-142-plan-critique.md with `Revise` resolved (`PC-001`..`PC-005` applied) |
| Relevant research                | .copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-research.md (`C1`-`C17`)                                                     |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-changes.md is created or continued by implementation as its evidence record   |
| Planning execution and readiness | Complete; Ready (`Planning status: ready`, all 5 critique findings resolved directly)                                                      |
| Continuation context             | Confirmed automatic RPI Agent parent return; transitions automatically to `rpi-implement`                                                  |

## Sources

* `.copilot-tracking/research/2026-11-15/kv-secret-lifecycle-142-research.md`: Complete three-wave codebase research (`C1`-`C17`) establishing existing capabilities, closure-audit gaps, Bicep/RBAC invariants, and shared-worktree Python isolation.
* `infra/scripts/secret_lifecycle.py` & `infra/tests/test_secret_lifecycle.py`: Existing CLI subcommands, inventory/expiry validators, and 19 regression tests that must remain compatible (`C3`, `C4`).
* `infra/secret-inventory.json` & `infra/role-assignments.json`: Authoritative 90-day review interval, 4 inventoried vault secrets, and least-privilege Key Vault data-plane caller matrix (`C2`, `C12`).
* `infra/modules/containerapps.bicep`, `infra/scripts/credential_arm.py`, & `infra/scripts/setup-entra.py`: Container Apps Key Vault secret URI binding, EasyAuth `clientSecretSettingName`, `/healthz` + `/sign-in` + `/api/me` auth contracts, and metadata-only secret handling (`C6`, `C7`).
* `src/core/src/zava_forward/core/ledger.py`, `diagnostic_logging.py`, & `restart_authority.py`: Canonical SHA-256 hash-chaining, sensitive-pattern redaction, and non-placeholder/non-automated human authority checks (`C8`, `C10`, `C11`).
* `infra/README.md` & `infra/scripts/bicep_inventory.py`: Target documentation section (`## Key Vault secret lifecycle`) and `#136` Markdown table parser constraints (`C5`, `C15`).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Author pure Key Vault secret lifecycle verification and signed review ledger module in `src/core`

* Intent: Create `zava_forward.core.secret_lifecycle` with fail-closed zero-secret guards, staged zero-downtime Entra rotation verification, `AzureDiagnostics` + RBAC data-plane access auditing, and HMAC-SHA256 signed, SHA-256 hash-chained review ledgers under strict typing.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `src/core/src/zava_forward/core/secret_lifecycle.py`

* Requirement and evidence: `FR-1`, `FR-2`, `FR-3`, `FR-4`, `NFR-1`, `NFR-2`; research `C2`-`C4`, `C6`-`C12`, `C16`, `C17`.
* Expected result: Strictly typed module providing inventory/expiry helpers, `assert_no_secret_material`, `verify_staged_entra_rotation` (overlap, switchover, health/auth probes, rollback, retirement gating, sanitized receipt), `default_expected_caller_policy`, `audit_keyvault_data_plane_access`, `create_signed_access_review_record`, and `verify_access_review_ledger`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Extend `infra/scripts/secret_lifecycle.py` CLI and backward-compatible operator commands

* Intent: Expose `rotation-verify`, `access-audit`, `review-sign`, and `ledger-verify` in `infra/scripts/secret_lifecycle.py` with owner-only key-file checks and worktree-hermetic `zava_forward.core` resolution while preserving existing public functions and subcommands.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Update `infra/scripts/secret_lifecycle.py` with staged rotation and signed ledger CLI subcommands

* Requirement and evidence: `FR-2`, `FR-3`, `FR-4`, `FR-5`, `NFR-1`, `NFR-2`; research `C3`, `C4`, `C12`, `C16`.
* Expected result: `infra/scripts/secret_lifecycle.py` delegates cleanly to `zava_forward.core.secret_lifecycle`, enforces `0600` POSIX permissions on `--key-file`, never accepts secret/key values on argv, and passes `ruff` and `mypy --strict`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Add deterministic unit and CLI regression tests in `src/core/tests/` and `infra/tests/`

* Intent: Prove semantic correctness and negative/mutation refusal across rotation overlap, switchover, rollback, secret non-exposure, data-plane caller/operation anomalies, human reviewer validation, cryptographic ledger integrity, and 90-day schedule enforcement.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Create `src/core/tests/test_secret_lifecycle.py` for domain invariants and edge cases

* Requirement and evidence: `FR-1`..`FR-4`, `NFR-1`, `NFR-2`; research `C6`-`C12`, `C16`, `C17`.
* Expected result: Comprehensive deterministic unit suite covering valid staged rotation, insufficient overlap, unrefreshed Container Apps revision, anonymous `/api/me` auth regression, failed-probe rollback blocking `safeToRetirePriorCredential`, post-retirement validation, canary secret refusal, unexpected/forbidden callers, out-of-scope secret access, placeholder/automated reviewer refusal, HMAC/hash tampering, and >90-day schedule gaps.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-phase-details.md

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Extend `infra/tests/test_secret_lifecycle.py` for CLI workflows and repository contract alignment

* Requirement and evidence: `FR-2`..`FR-5`, `NFR-1`, `NFR-2`; research `C2`, `C3`, `C4`, `C12`.
* Expected result: All 19 existing tests remain intact and passing, plus new CLI tests exercise `rotation-verify`, `access-audit` (wired to real `infra/role-assignments.json` and `infra/secret-inventory.json`), `review-sign` (chaining entries and rejecting insecure key-file modes), and `ledger-verify`.
* Detail section: P03-T02 in .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-phase-details.md

<!-- rpi:phase id=P04 -->
### [x] P04: Update `infra/README.md` lifecycle contracts, run Focused validation, and commit cleanly

* Intent: Document the zero-downtime staged Entra client-secret rotation procedure and scheduled Key Vault data-plane access review & signed ledger contract in `infra/README.md`, execute all Focused validation checks, and commit code + tracking artifacts after `rpi-review`.
* Dependencies: P01, P02, P03

<!-- rpi:task id=P04-T01 -->
#### [x] P04-T01: Document staged Entra rotation and scheduled signed data-plane access review in `infra/README.md`

* Requirement and evidence: `FR-5`; research `C5`, `C13`, `C14`, `C15`.
* Expected result: `infra/README.md` (`Layout` and `## Key Vault secret lifecycle`) documents exact zero-downtime rotation stages, `rotation-verify` overlap/switchover/rollback checks, 90-day `AzureDiagnostics` + RBAC `access-audit` / `review-sign` / `ledger-verify` workflow, signed ledger schema, and honest live-Azure operational boundaries while keeping `bicep_inventory.py --check` green.
* Detail section: P04-T01 in .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-phase-details.md

<!-- rpi:task id=P04-T02 -->
#### [x] P04-T02: Run Focused validation suite (`unittest`, `ruff`, `mypy`) and verify clean repository state

* Requirement and evidence: `NFR-2`; user prompt Focused validation tier; `.github/workflows/src-ci.yml` (`C16`, `C17`).
* Expected result: `src/core` unit tests, `infra/tests` suite, `ruff check`, `ruff format --check`, and `mypy --strict` all exit `0` using worktree-local `PYTHONPATH` without running `tools/rpi-checks.py --all` or mutating shared global packages.
* Detail section: P04-T02 in .copilot-tracking/details/2026-11-15/kv-secret-lifecycle-142-phase-details.md

## Dependencies

* Python 3.12 stdlib (`hashlib`, `hmac`, `json`, `datetime`, `re`, `stat`, `argparse`, `dataclasses`, `pathlib`, `urllib.parse`): Available in workspace (`Python 3.12.3`), keeping `zava-forward-core` zero-external-dependency (`C16`, `C17`).
* Existing repository contracts `infra/secret-inventory.json`, `infra/role-assignments.json`, `infra/modules/keyvault.bicep`, and `infra/modules/containerapps.bicep`: Read-only authoritative inputs for tests and default expected-caller policies (`C1`, `C2`, `C6`, `C12`).
* Local validation tools `ruff` (`0.17.3`) and `mypy` (`2.4.1`): Verified installed in workspace.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` (`High`, planner) | resolved | Updated `FR-2`, `P01-T01`, and `P03-T01` to require `authenticatedApiStatus == 200` on `post_switchover` and `post_retire` when `browserMode=True` (proving live `entra-client-secret` exchange), gate `safeToRetirePriorCredential = True` strictly to `stage == "post_switchover" and ok is True`, and require verifiable `priorCredential` `[startDateTime, endDateTime]` overlap metadata or a matching `postSwitchoverEvidenceDigest` in `post_retire`. |
| `PC-002` (`High`, planner) | resolved | Updated `FR-3`, `P01-T01`, `P02-T01`, and `P03-T01` so `default_expected_caller_policy` fails closed on unmapped OIDs (`unexpected_caller` / `unmapped_rbac_principal`) without auto-trusting live `assignments`, separates OID-less platform Event Grid notifications (`SecretNearExpiryEventGridNotification`, `SecretExpiredEventGridNotification`) from `<anonymous>` secret operations, and defines `denied_access_activity` as any `403` or `401` count `>= denied_401_threshold` (default `5`). |
| `PC-003` (`Medium`, planner) | resolved | Updated `FR-1`, `P01-T01`, and `P02-T01` so `assert_no_secret_material` raises `SecretExposureError` consistently across all domain functions including `verify_access_review_ledger` (`ledger-verify` exit `2`), unwraps top-level ARM `{"value": [...]}` metadata list envelopes cleanly, and uses targeted credential patterns (`?sig=`, `&sig=`, `?sv=`, `Bearer `, `Basic `, 3-segment JWT, `sk-`, `SharedAccessSignature`, `AccountKey=`) without 32/64-hex hash collisions. |
| `PC-004` (`Medium`, planner) | resolved | Updated `FR-4`, `NFR-1`, `P01-T01`, and `P02-T01` to bind `vaultName`, `windowStart`, `windowEnd`, and canonical `auditDigest` with 1-to-1 keyed RBAC/anomaly coverage, enforce cross-entry `vaultName` continuity, reject symlinks and inside-repository paths on `--key-file` / `--keys-file`, and specify `--keys-file` as a `0600` JSON `{"<key_id>": "<key>"}` map. |
| `PC-005` (`Low`, planner) | resolved | Updated `FR-2`, `P01-T01`, and `P03-T02` to support optional `priorSecretName` alongside `secretName` for staged two-name secret handoffs (`setup-entra.py` / `credential_arm.py`) and to type-annotate existing helpers/methods in `infra/tests/test_secret_lifecycle.py` for `mypy --strict` without altering any existing assertion. |

## Follow-Up Items

* Execute a live operator-attended staged Entra client-secret rotation drill in the `ama` test environment and archive the sanitized `rotation-verify` receipt (outside offline repository CI scope; owner: `@jmservera`).
* Export the first live 90-day Log Analytics `AzureDiagnostics` + vault RBAC snapshot from `ama` and record the inaugural live `review-sign` entry in operations evidence (outside offline repository CI scope; owner: `@jmservera`).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/kv-secret-lifecycle-142-changes.md
* Ready phase or task: P01 (`P01-T01`)
* Remaining provisional question or blocker: none
