<!-- markdownlint-disable-file -->
# RPI Plan: Issue #115 Immutable Blob Ledger Digest Container and Retention-Lock Posture

## Task Metadata

* Task ID: issue-115-platform-blob-immutability
* Task slug: platform-115-blob-immutability
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/platform-115-blob-immutability-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/platform-115-blob-immutability-plan-critique.md

## Executive Summary

This plan closes the source-level and compiled-template gaps behind the remaining Issue #115 acceptance criterion (**Digests land in an immutable container with a retention lock**) across Azure Bicep infrastructure (`infra/`), the core audit ledger digest publisher/verifier (`src/core/`), and the scheduled job entrypoint (`src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`). Earlier baseline work in PR #1785 added the `ledger-digests` container, an unlocked ARM `immutabilityPolicies` child resource, and initial digest verification helpers, but left four gaps: (1) `ledger-digests` in `infra/modules/storage.bicep` did not enable container-level `immutableStorageWithVersioning` or gate `digestRetention` cleanly when `ledgerDigestImmutableStorage == false` in development, (2) `infra/main.bicep`, `infra/modules/guard.bicep`, and `infra/modules/containerapps.bicep` neither failed closed when a `production` profile attempted a mutable, sub-floor, or unlocked digest container configuration nor wired `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` into the scheduled `ledgerVerify` job, (3) `src/core/src/zava_forward/core/ledger_digest_blob.py` lacked weakest-link container immutability and retention-lock posture checking and recording (`immutability_policy_state`, `retention_days`, `locked`) across both the publisher and verifier paths, and (4) `ledgerVerify` runs `zava_forward.orchestrator.digest_blob`, which previously ignored `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` (`PC-001`).

Implementing **P01** through **P03** configures container-level `immutableStorageWithVersioning` and conditional `digestRetention` on `ledger-digests`, enforces fail-closed `production`-profile guard validation and runtime lock environment wiring in Bicep, adds unified weakest-link immutability posture evaluation and recording (`immutability_policy_state`, `retention_days`, `locked`, plus human-gate honesty flags) across `src/core` (`ledger_digest_blob.py`) and `src/orchestrator` (`digest_blob.py`), and validates everything with focused unit/policy tests, `ruff`, and `mypy`.

### User Decisions and Requirements Highlights

* **Full RPI loop with dated artifacts**: Execute `rpi-research`, `rpi-plan` (including independent critique), `rpi-implement`, and `rpi-review` under `.copilot-tracking/{research,plans,details,changes}/2026-11-15/` and `.copilot-tracking/reviews/logs/2026-11-15/`, committing cleanly on `feat/platform-115-blob-immutability` without pushing or opening a PR.
* **Container-level Bicep immutability and fail-closed `production` validation**: `infra/modules/storage.bicep` and `infra/main.bicep` must configure container-level immutability (`immutableStorageWithVersioning` + `immutabilityPolicies` with configurable retention days) and reject unlocked or mutable digest container configurations in `production` profile while keeping all `infra/tests/` green.
* **Explicit `src/core` publisher/verifier posture metadata and fail-closed lock enforcement**: Both publication and verification paths in `src/core` must check and record `immutability_policy_state`, `retention_days`, and `locked`, failing closed when a retention lock is required by policy (`require_retention_lock=True` / `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true`) yet absent, `Unlocked`, expired, or shorter than `min_retention_days`.
* **Focused validation tier**: Run targeted `src/core/tests/` and `infra/tests/`, `ruff check`, `ruff format --check`, and `mypy`; do not run `tools/rpi-checks.py --all`.

### What You May Not Know

* **ARM `immutabilityPolicies` `state` is read-only on `PUT`**: Azure Resource Manager creates time-based `immutabilityPolicies` in `Unlocked` state (`test_bicep_policy.py` explicitly forbids setting read-only `state` on `digestRetention`). Therefore, Bicep guarantees container-level `immutableStorageWithVersioning: { enabled: true }`, `immutabilityPeriodSinceCreationInDays >= 365`, `allowProtectedAppendWrites: false`, compile-time `production` guard enforcement, and `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true` on `ledgerVerify`, while irreversible live Azure `lockImmutabilityPolicy` execution and Legal retention duration approval (#121) remain explicit human/cloud gates (`Refs #115`).
* **Existing test invariants constrain `storage.bicep` and `guard.bicep` shapes**: `infra/tests/test_staff_azure.py` asserts literal `'ledger-digests', 'staff-results']`, `parent: blobContainers[4]`, `parent: blobContainers[5]`, and `publicAccess: 'None'`; `infra/tests/test_bicep_policy.py` mutates `container_copy["properties"]["publicAccess"]` as a JSON dict; and `infra/tests/test_environment_quota_parameters.py` asserts the exact parameter count and `"Empty means"` description prefix on `infra/modules/guard.bicep`.

### Unresolved Decisions or Blockers

* None for offline source, Bicep, and unit-test delivery. Live Azure WORM policy lock transition (`lockImmutabilityPolicy`) and Legal sign-off on retention duration (#121) remain explicit post-merge human/cloud gates preserved by honesty-boundary metadata and `Refs #115` commit attribution.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`rpi-research`, `rpi-plan` with independent critique, `rpi-implement`, `rpi-review`) writing dated `2026-11-15` artifacts for Issue #115 in worktree `/home/azureuser/source/ama-demo-wt/feat-115-blob-immutability` on branch `feat/platform-115-blob-immutability` (caller prompt).
* Configure container-level immutability (`immutableStorageWithVersioning` and `immutabilityPolicies` with configurable retention days) for `ledger-digests` in `infra/modules/storage.bicep` and `infra/main.bicep`, with fail-closed validation against unlocked or mutable digest containers in `production` profile, updating Bicep inventory only if needed so all `infra/tests/` pass (caller Objective 2; ADR-0002).
* Ensure the `src/core` ledger digest publisher and verifier explicitly check and record container immutability and retention-lock posture metadata (`immutability_policy_state`, `retention_days`, `locked`), failing closed when an immutable retention lock is required by policy but absent or unlocked, while preserving the honesty boundary that live Azure WORM lock activation and owner-approved retention duration remain human/cloud-gated (caller Objective 3; ADR-0002).
* Add focused unit tests in `src/core/tests/` and `infra/tests/`, run focused validation (`unittest`, `ruff check`, `ruff format --check`, `mypy`; do not run `tools/rpi-checks.py --all`), and commit all changes plus `.copilot-tracking/` artifacts cleanly on `feat/platform-115-blob-immutability` with the `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` trailer without pushing or opening a PR (caller Objective 4).

## Goals

* Provision container-level versioned immutable storage (`immutableStorageWithVersioning`) alongside `immutabilityPolicies` on `ledger-digests` in Bicep, with fail-closed `production`-profile parameter-guard enforcement and runtime `ZF_DIGEST_REQUIRE_RETENTION_LOCK` / `ZF_DIGEST_MIN_RETENTION_DAYS` job wiring.
* Enforce and record canonical container immutability and retention-lock posture metadata (`immutability_policy_state`, `retention_days`, `locked`, plus human-gate honesty flags) across `src/core` digest publication, verification, reconciliation, and scheduled verification paths.
* Prove fail-closed rejection of unlocked, absent, mutable, or under-retained digest container configurations in both `infra/tests/` and `src/core/tests/` without regressing existing suites or Bicep inventory checks.

## Scope and Non-Goals

### In Scope

* `infra/modules/storage.bicep`, `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/modules/containerapps.bicep`, and directly coupled `#115` parameter documentation in `infra/README.md`.
* `src/core/src/zava_forward/core/ledger_digest_blob.py`, `src/core/README.md`, and `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` (the `ledgerVerify` job entrypoint, `PC-001`).
* Focused unit and policy tests in `src/core/tests/test_ledger_digest_blob.py`, `src/orchestrator/tests/test_digest_blob.py`, `infra/tests/test_bicep_policy.py`, and `infra/tests/test_environment_quota_parameters.py` (for the updated `guard.bicep` parameter count).
* Verification of `python3 infra/scripts/bicep_inventory.py --check`, `infra/tests/`, `src/core/tests/`, `src/orchestrator/tests/`, `ruff check`, `ruff format --check`, and `mypy`, followed by a local commit on `feat/platform-115-blob-immutability`.

### Non-Goals

* Executing live Azure CLI `az storage container immutability-policy lock` (`lockImmutabilityPolicy`), `az deployment group what-if/create`, or claiming Legal approval of the 365-day default retention period (#121).
* Running `python3 tools/rpi-checks.py --all`, pushing to `origin`, or opening/updating a GitHub pull request.
* Modifying unrelated web UI, API, agents, or legacy tracking artifacts (`immutable-blob-ledger-digests-115*`).

## Functional Requirements

* **FR-1 (Bicep container-level `immutableStorageWithVersioning` and gated `digestRetention`)**: `infra/modules/storage.bicep` exposes `param ledgerDigestImmutableStorage bool = true`, configures `blobContainers` so `ledger-digests` (`containers[5]`) sets `immutableStorageWithVersioning: { enabled: true }` when enabled (`null` on all other containers or when explicitly disabled in development), and gates `digestRetention` with `if (ledgerDigestImmutableStorage)` (`PC-002`) while preserving `publicAccess: 'None'`, `isVersioningEnabled: true`, and `immutabilityPeriodSinceCreationInDays: ledgerDigestImmutabilityDays` / `allowProtectedAppendWrites: false`.
  * Observable acceptance criteria: Compiled ARM JSON for `infra/modules/storage.bicep` and `infra/main.bicep` evaluates `blobContainers[5].properties` to `{"publicAccess": "None", "immutableStorageWithVersioning": {"enabled": True}}` and `digestRetention["condition"] == True` by default, and evaluates `immutableStorageWithVersioning` to `None` with `digestRetention["condition"] == False` when opted out in development (`indices 0..4, 6` always `None`).
* **FR-2 (Bicep fail-closed `production` guard and `ledgerVerify` lock wiring)**: `infra/main.bicep` exposes `ledgerDigestImmutableStorage` (`bool = true`), `ledgerDigestRequireRetentionLock` (`bool = true`), and `ledgerDigestImmutabilityDays` (`@minValue(1) int = 365`), forwarding `ledgerDigestImmutableStorage` to `storage` and `ledgerDigestRequireRetentionLock` + `ledgerDigestMinRetentionDays` to `containerapps`; `infra/modules/guard.bicep` adds `@minLength(1) param productionProfileRequiresImmutableLedgerDigests string` rejecting `ledgerDigestImmutableStorage == false`, `ledgerDigestRequireRetentionLock == false`, or `ledgerDigestImmutabilityDays < 365` whenever `deploymentProfile == 'production'`; and `infra/modules/containerapps.bicep` wires `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` on `ledgerVerify`.
  * Observable acceptance criteria: `parameter-guard` passes under default parameters and all three `.bicepparam` files, fails with `productionProfileRequiresImmutableLedgerDigests` on any mutable/unlocked/sub-365-day override in `production` profile, allows explicit opt-out in `development` profile, verifies module forwarding in `main.bicep`, and renders `ZF_DIGEST_REQUIRE_RETENTION_LOCK='true'` and `ZF_DIGEST_MIN_RETENTION_DAYS='365'` on `ledger-verify`.
* **FR-3 (`src/core` container/blob weakest-link posture metadata schema and honesty boundary)**: `verify_container_retention_lock` (with `require_immutable_versioning: bool = False`, `PC-002`) and `verify_blob_retention_headers` (plus a deterministic weakest-link posture aggregator, `PC-004`) produce canonical posture metadata containing `immutability_policy_state` (`"Locked"`, `"Unlocked"`, `"Absent"`, or raw unexpected state string), `retention_days` (`int | None`), `locked` (`bool`), and explicit honesty flags (`live_worm_lock_human_gated: True`, `retention_schedule_human_gated: True`), resolving multi-blob and policy-vs-header inputs by weakest link (`locked=True` only when every evaluated source is `"Locked"` with zero retention/container problems, `retention_days` taking `min` across configured policy days and `x-ms-creation-time`-bounded blob windows, or remaining whole days only when neither policy nor creation header is present).
  * Observable acceptance criteria: Unit tests assert exact `immutability_policy_state`, `retention_days`, `locked`, and human-gate flags across `Locked`, `Unlocked` (including ARM pre-lock policies without `state`), `Absent`, mixed multi-blob headers, policy-vs-header conflicts, and disabled/missing `immutableStorageWithVersioning` inputs.
* **FR-4 (`src/core` & `src/orchestrator` fail-closed publisher/verifier posture checking and recording)**:
  * `BlobLedgerDigestStore` adds `create_anchor_with_headers(name, digest) -> tuple[bool, dict[str, str]]`, stores `last_immutability_posture: dict[str, Any] | None`, and chains `from None` in `__init__`, `_send`, `read_anchor_with_headers`, and `_parse_listing_page` (`PC-005`) to prevent secret URL/SAS traceback leakage.
  * `publish_ledger_digests(entries, blob, *, ...)` (preserving its keyword-only `*` signature and `list[str]` return, alongside `publish_ledger_digests_with_posture -> dict[str, Any]` and `publish_store_digests`) validates container policy before broken-chain or zero-anchor returns (`PC-004`), checks each uploaded or conflict-read anchor immediately (failing closed on the first non-compliant anchor when `require_retention_lock=True`), records posture metadata on `blob.last_immutability_posture` and `posture_out` across normal, zero-anchor, and broken-chain paths, and raises `LedgerDigestBlobError` when `require_retention_lock=True` and posture is not locked/compliant.
  * `verify_ledger_digests`, `reconcile_ledger_digests` (`+ _run_reconcile_cli`), and `run_scheduled_verification` always inspect and record `immutability_policy_state`, `retention_days`, `locked` (decoupled from unrelated ledger hash-chain mismatches, `PC-004`), and `immutability_posture` across all return branches (using `blob.last_immutability_posture` when `report is None`, `PC-005`), keeping `_emit_ok` / `_emit_alert` compliant with `monitoring_coverage.sanitize_diagnostic` (`ALLOWED_FIELDS`) while failing closed (`intact=False` / `exit_code=1` / `LEDGER_DIGEST_ALERT`) when `require_retention_lock=True` and posture is not locked/compliant.
  * `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` (`PC-001`) honors `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` via `zava_forward.core.ledger_digest_blob` posture/header verification while preserving `put_digest` / `read_digest` monkeypatch hooks, `enforce_from_env`, and exit-code `2` contracts, recording `immutability_policy_state`, `retention_days`, and `locked` in `verify()` and `reconcile()` reports and failing closed with `LEDGER_DIGEST_ALERT` / `RECONCILE_ALERT_MARKER` (`exit 1`) on unlocked/absent/invalid retention lock.
  * Observable acceptance criteria: Focused unit tests in `src/core/tests/test_ledger_digest_blob.py` and `src/orchestrator/tests/test_digest_blob.py` verify posture metadata recording on both publish and verify, fail-closed rejection when absent/unlocked/short-retention/mixed-header under `require_retention_lock=True` / `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true`, and zero secret leakage.

## Non-Functional Requirements

* **Zero secret or URL leakage in diagnostics and exceptions**
  * Objective threshold or evaluation condition: Zero occurrences of storage account hostnames, SAS tokens, or bearer tokens in `LEDGER_DIGEST_OK` / `LEDGER_DIGEST_ALERT` outputs or `LedgerDigestBlobError.__cause__` chains.
  * Operating condition or verification approach: `monitoring_coverage.sanitize_diagnostic` scrubbing and `raise LedgerDigestBlobError(...) from None` verified by negative transport fault unit tests.
  * Observable acceptance criteria: Transport fault and alert unit tests confirm `exc.__cause__ is None` and zero secret substrings in captured output.
* **Compile-time Bicep cleanliness and architecture inventory stability**
  * Objective threshold or evaluation condition: `az bicep build` and `az bicep lint` exit `0` with zero diagnostics; `python3 infra/scripts/bicep_inventory.py --check` exits `0`.
  * Operating condition or verification approach: Run `bicep_inventory.py --check` and full `infra/tests/` discovery.
  * Observable acceptance criteria: All `infra/tests/` suites pass without regenerating resource-count drift unless legitimately required.
* **Static typing and lint conformance**
  * Objective threshold or evaluation condition: Zero findings from `mypy`, `ruff check`, and `ruff format --check` across modified `src/core/` and `infra/` Python files.
  * Operating condition or verification approach: Match `.github/workflows/src-ci.yml` commands locally (`python3 -m mypy` in `src/core`; `ruff check` and `ruff format --check` on `src/core` and modified `infra/tests` files with `--isolated --line-length 100` for `infra/`).
  * Observable acceptance criteria: Commands exit `0`.

## Acceptance Criteria

* `infra/modules/storage.bicep` configures `immutableStorageWithVersioning: { enabled: true }` (default `ledgerDigestImmutableStorage = true`) and `immutabilityPolicies` (`immutabilityPeriodSinceCreationInDays = ledgerDigestImmutabilityDays`, `allowProtectedAppendWrites: false`) on `ledger-digests`, preserving index 5, `publicAccess: 'None'`, and `test_staff_azure.py` / `bicep_inventory.py` invariants.
* `infra/main.bicep` and `infra/modules/guard.bicep` fail closed in `production` profile (`productionProfileRequiresImmutableLedgerDigests`) when `ledgerDigestImmutableStorage == false`, `ledgerDigestRequireRetentionLock == false`, or `ledgerDigestImmutabilityDays < 365`, and `infra/modules/containerapps.bicep` sets `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` on `ledgerVerify`.
* `src/core/src/zava_forward/core/ledger_digest_blob.py` checks and records `immutability_policy_state`, `retention_days`, `locked` (plus human-gate honesty metadata) in both publisher and verifier flows, failing closed when `require_retention_lock=True` and the container/blob retention lock is absent, `Unlocked`, expired, or `< min_retention_days`.
* Focused unit/policy tests in `src/core/tests/test_ledger_digest_blob.py`, `infra/tests/test_bicep_policy.py`, and `infra/tests/test_environment_quota_parameters.py` pass alongside full `src/core` and `infra` test suites, `bicep_inventory.py --check`, `ruff check`, `ruff format --check`, and `mypy`.
* All source, doc, test, and `.copilot-tracking/` artifacts are committed cleanly on `feat/platform-115-blob-immutability` with `Refs #115` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, with no push and no PR opened.

## Test Ownership and Validation Lock

* **Canonical test targets**:
  * `src/core/tests/test_ledger_digest_blob.py` (semantic unit coverage for publisher/verifier/reconcile weakest-link posture metadata `immutability_policy_state`, `retention_days`, `locked`, mixed multi-blob headers, policy-vs-header conflicts, zero-anchor/broken-chain publish posture, fail-closed absent/unlocked/short-retention publish & verify behavior, `require_immutable_versioning`, honesty flags, and `_send`/`__init__` `exc.__cause__ is None`).
  * `src/orchestrator/tests/test_digest_blob.py` (semantic unit coverage for `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` fail-closed publish/verify/reconcile behavior and posture metadata in `orchestrator.digest_blob`).
  * `infra/tests/test_bicep_policy.py` (semantic + negative-mutation policy coverage for `blobContainers[5]` `immutableStorageWithVersioning` via `copyIndex`/`false` in `evaluate()`, conditional `digestRetention`, `main.bicep` -> `storage`/`containerapps` parameter forwarding, `productionProfileRequiresImmutableLedgerDigests` guard matrix + guard-bypass mutation, and `ledgerVerify` `ZF_DIGEST_REQUIRE_RETENTION_LOCK` / `ZF_DIGEST_MIN_RETENTION_DAYS` env wiring).
  * `infra/tests/test_environment_quota_parameters.py` (regression alignment for `len(self.guard["parameters"]) == 30`).
* **Generated/checked inventory targets**: `infra/README.md` verified via `python3 infra/scripts/bicep_inventory.py --check`.
* **Exact test removals**: `none`.
* **Maximum new test methods**: At most 8 focused test methods across `src/core/tests/test_ledger_digest_blob.py` (up to 4), `src/orchestrator/tests/test_digest_blob.py` (up to 2), and `infra/tests/test_bicep_policy.py` (up to 2, plus extending existing `assert_retention_controls`, `assert_ledger_verification_controls`, `assert_parameter_controls`, `test_mutations_reject_production_guard_bypass`, and negative-mutation tables).
* **Planned validation commands**:
  * `python3 infra/scripts/bicep_inventory.py --check`
  * `python3 -m unittest discover -s infra/tests -p 'test_*.py' -q`
  * `cd src/core && PYTHONPATH=src:tests python3 -m unittest discover -s tests -p 'test_*.py' -q`
  * `cd src/orchestrator && PYTHONPATH=src:tests:../core/src:../core/tests python3 -m unittest discover -s tests -p 'test_*.py' -q`
  * `cd src/core && python3 -m mypy`
  * `cd src/orchestrator && PYTHONPATH=../core/src python3 -m mypy`
  * `python3 -m ruff check src/core src/orchestrator` and `python3 -m ruff format --check src/core src/orchestrator`
  * `python3 -m ruff check --isolated --line-length 100 infra/tests/test_bicep_policy.py infra/tests/test_environment_quota_parameters.py` and `python3 -m ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py infra/tests/test_environment_quota_parameters.py`

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/platform-115-blob-immutability-plan.md                                                                |
| Phase details                    | .copilot-tracking/details/2026-11-15/platform-115-blob-immutability-phase-details.md                                                     |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/platform-115-blob-immutability-plan-critique.md with Revise verdict; PC-001..PC-005 resolved  |
| Relevant research                | .copilot-tracking/research/2026-11-15/platform-115-blob-immutability-research.md                                                         |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/platform-115-blob-immutability-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for implementation                                                                                                    |
| Continuation context             | Active confirmed automatic RPI Agent session continues automatically to `rpi-implement`                                                  |

## Sources

* `.copilot-tracking/research/2026-11-15/platform-115-blob-immutability-research.md`: Three-wave codebase evidence (`C1`–`C19`) and convergence on Option A.
* `docs/adrs/0002-pilot-readiness-architecture.md`: Architectural mandate for immutable Blob ledger digests with retention lock and open Legal retention decision (#121).
* `infra/modules/storage.bicep`, `infra/main.bicep`, `infra/modules/guard.bicep`, `infra/modules/containerapps.bicep`: Current storage container, parameter guard, and `ledgerVerify` job definitions.
* `src/core/src/zava_forward/core/ledger_digest_blob.py`: Current ledger digest publisher, container/blob WORM retention verifier, and scheduled verification CLI.
* `infra/tests/test_bicep_policy.py`, `infra/tests/test_staff_azure.py`, `infra/tests/test_environment_quota_parameters.py`, `infra/tests/test_bicep_architecture_inventory_136.py`, `src/core/tests/test_ledger_digest_blob.py`: Existing policy, inventory, and unit test contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden Bicep Container-Level Immutability, Production Guard, and Job Lock Wiring

* Intent: Configure container-level `immutableStorageWithVersioning` on `ledger-digests`, enforce fail-closed `production`-profile rejection of unlocked/mutable/sub-floor digest container settings in `guard.bicep`, and wire `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` into `ledgerVerify`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Configure `immutableStorageWithVersioning` and conditional `digestRetention` on `ledger-digests` in `infra/modules/storage.bicep`

* Requirement and evidence: FR-1; Research `C1`, `C2`, `C3`, `C15`, `C16`; Critique `PC-002`
* Expected result: `storage.bicep` accepts `param ledgerDigestImmutableStorage bool = true`, configures `blobContainers` with object-literal `properties` preserving `publicAccess: 'None'` and setting `immutableStorageWithVersioning: container == 'ledger-digests' && ledgerDigestImmutableStorage ? { enabled: true } : null`, and gates `digestRetention` with `if (ledgerDigestImmutableStorage)` while retaining `'ledger-digests'` at index 5.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/platform-115-blob-immutability-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Enforce `production`-profile fail-closed digest immutability guard and wire `ledgerVerify` lock env vars

* Requirement and evidence: FR-2; Research `C5`, `C6`, `C13`, `C17`, `C18`; Critique `PC-001`, `PC-003`
* Expected result: `main.bicep` adds `ledgerDigestImmutableStorage` (`bool = true`) and `ledgerDigestRequireRetentionLock` (`bool = true`), passes `productionProfileRequiresImmutableLedgerDigests` into `guard.bicep` (`isDev || (ledgerDigestImmutableStorage && ledgerDigestRequireRetentionLock && ledgerDigestImmutabilityDays >= 365) ? 'ok' : ''`), forwards `ledgerDigestImmutableStorage` to `storage` and `ZF_DIGEST_REQUIRE_RETENTION_LOCK` + `ZF_DIGEST_MIN_RETENTION_DAYS` into `containerapps.bicep` `ledgerVerify`, and updates `#115` parameter documentation in `infra/README.md` without breaking `bicep_inventory.py --check`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/platform-115-blob-immutability-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Check and Record Container Immutability Posture Across `src/core` and `src/orchestrator` Publisher and Verifier

* Intent: Ensure `src/core/src/zava_forward/core/ledger_digest_blob.py` and `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` compute, enforce, and record canonical weakest-link container immutability and retention-lock posture metadata (`immutability_policy_state`, `retention_days`, `locked`, plus human-gate honesty flags) across both publication and verification flows, failing closed when a lock is required by policy (`require_retention_lock=True` / `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true`) but absent, `Unlocked`, expired, or under-retained.
* Dependencies: None (can execute sequentially after `P01`)

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add canonical weakest-link posture metadata and fail-closed checks across `src/core/ledger_digest_blob.py` and `src/orchestrator/digest_blob.py`

* Requirement and evidence: FR-3, FR-4; Research `C7`–`C13`, `C19`; Critique `PC-001`, `PC-002`, `PC-004`, `PC-005`
* Expected result: `verify_container_retention_lock` (`+ require_immutable_versioning`), `verify_blob_retention_headers`, `BlobLedgerDigestStore` (`__init__`/`_send` `from None`), `publish_ledger_digests` (`+ publish_ledger_digests_with_posture` / `publish_store_digests`), `verify_ledger_digests`, `reconcile_ledger_digests` (`+ _run_reconcile_cli`), `run_scheduled_verification`, and `zava_forward.orchestrator.digest_blob` all check and record weakest-link `immutability_policy_state`, `retention_days`, `locked` (plus human-gate honesty flags), fail closed when `require_retention_lock=True` / `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true` and posture is absent/unlocked/expired/under-retained, keep `sanitize_diagnostic` intact, and update `#115` notes in `src/core/README.md`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/platform-115-blob-immutability-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Unit/Policy Tests and Static/Runtime Verification

* Intent: Add focused unit and Bicep policy/mutation tests across `infra/tests/`, `src/core/tests/`, and `src/orchestrator/tests/`, and pass all targeted test, inventory, lint, format, and type-check gates.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Extend `infra/tests/`, `src/core/tests/`, and `src/orchestrator/tests/` and run focused validation suite

* Requirement and evidence: FR-1 through FR-4, NFRs; Research `C15`–`C18`; Critique `PC-001`–`PC-005`
* Expected result: Focused assertions and negative mutations in `infra/tests/test_bicep_policy.py` (with `copyIndex`/`false` support in `evaluate()`, `main.bicep` module forwarding, and `test_mutations_reject_production_guard_bypass`), `guard` parameter count update in `infra/tests/test_environment_quota_parameters.py`, and focused publisher/verifier/reconcile posture & fail-closed tests in `src/core/tests/test_ledger_digest_blob.py` and `src/orchestrator/tests/test_digest_blob.py` pass alongside full `infra/tests/`, `src/core/tests/`, `src/orchestrator/tests/`, `bicep_inventory.py --check`, `ruff check`, `ruff format --check`, and `mypy`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/platform-115-blob-immutability-phase-details.md

## Dependencies

* Azure CLI with Bicep (`az bicep build` / `az bicep lint`): Required locally for `infra/tests/test_bicep_policy.py`, `test_environment_quota_parameters.py`, and `test_bicep_architecture_inventory_136.py` (verified available in baseline research).
* `src/core` and `src/orchestrator` distributions and toolchain (`unittest`, `mypy`, `ruff`): Verified available in current Python environment.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [Critical] (`orchestrator.digest_blob` ignored `ZF_DIGEST_REQUIRE_RETENTION_LOCK` / `ZF_DIGEST_MIN_RETENTION_DAYS`) | Resolved | Added `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` and `src/orchestrator/tests/test_digest_blob.py` (plus `src/orchestrator` `unittest`, `mypy`, `ruff`) into Scope, `FR-4`, `P02-T01`, and `P03-T01` so the scheduled `ledgerVerify` job enforces lock requirements and records posture metadata end-to-end. |
| `PC-002` [High] (Unconditional `digestRetention` when `ledgerDigestImmutableStorage == false` and permissive `immutableStorageWithVersioning` check) | Resolved | Gated `digestRetention` in `infra/modules/storage.bicep` with `if (ledgerDigestImmutableStorage)`, updated `P03-T01` retention assertions/mutations, and added `require_immutable_versioning: bool = False` to `verify_container_retention_lock`. |
| `PC-003` [High] (`test_bicep_policy.py:evaluate()` missing `copyIndex`/`false`, missing module forwarding and guard-bypass coverage) | Resolved | Added `"false": lambda: False` and `copyIndex` context evaluation to `P03-T01` for `infra/tests/test_bicep_policy.py`, plus explicit `main.bicep` -> `storage`/`containerapps` forwarding assertions and `"productionProfileRequiresImmutableLedgerDigests"` in `test_mutations_reject_production_guard_bypass`. |
| `PC-004` [High] (Weakest-link multi-blob headers, policy-vs-header conflicts, zero-anchor/broken-chain publish, and `reconcile_ledger_digests` parity) | Resolved | Specified weakest-link posture aggregation, immediate fail-closed publish abort on first non-compliant anchor, `min` retention-days conflict resolution, decoupled `locked` vs hash-chain `intact`, preserved keyword-only `*` signature, pre-return zero-anchor/broken-chain posture recording, and `reconcile_ledger_digests` / `_run_reconcile_cli` parity in `FR-3`, `FR-4`, and `P02-T01`. |
| `PC-005` [Medium] (Non-existent `_urlopen_transport`, `sanitize_diagnostic` `ALLOWED_FIELDS`, and `report=None` posture on fail-closed publish alerts) | Resolved | Targeted `BlobLedgerDigestStore.__init__`, `_send`, `read_anchor_with_headers`, and `_parse_listing_page` (`from None`), preserved strict `monitoring_coverage.sanitize_diagnostic` schema in `_emit_ok` / `_emit_alert`, and populated `run_scheduled_verification` posture fields from `blob.last_immutability_posture` when `report is None`. |
| Residual risk: Live Azure `lockImmutabilityPolicy` and Legal retention duration (#121) | Accepted with risk | Explicitly human/cloud-gated per ADR-0002 and caller Objective 3 (`Refs #115`); runtime `ZF_DIGEST_REQUIRE_RETENTION_LOCK=true` fails closed until applied live. |

## Follow-Up Items

* Execute owner-approved live Azure `lockImmutabilityPolicy` transition on the deployed `ledger-digests` container and record Legal retention duration approval (#121 / #115): Outside offline repository scope because WORM locking in Azure Storage is irreversible and gated on human Legal/owner approval.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/platform-115-blob-immutability-changes.md
* Ready phase or task: Complete (`P01`, `P02`, `P03` implemented and validated; ready for `rpi-review`)
* Remaining provisional question or blocker: None
