<!-- markdownlint-disable-file -->
# RPI Plan: Immutable Blob Ledger Digests and Scheduled Verification (Issue #115)

## Task Metadata

* Task ID: issue-115-immutable-blob-ledger-digests
* Task slug: immutable-blob-ledger-digests-115
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/immutable-blob-ledger-digests-115-plan-critique.md

## Executive Summary

This plan strengthens deterministic offline and Bicep enforcement for Issue #115 (`Immutable Blob ledger digests and scheduled verification`) across `src/core` and `infra/`. Today, `src/core` has only local JSONL hash-chain functions in `ledger.py` with zero Blob container immutability/retention-lock verification or scheduled mismatch alert contract, while `infra/main.bicep` omits top-level `ledgerDigestImmutabilityDays` parameter forwarding, `infra/modules/storage.bicep` omits a `ledgerDigestContainer` output for `containerapps.bicep`, and `infra/tests/test_bicep_policy.py` lacks full contract and mutation-rejection assertions for append-write immutability overrides (including ARM mutual-exclusivity between `allowProtectedAppendWrites` and `allowProtectedAppendWritesAll`) and scheduled ledger mismatch/missing alert rules.

We will add a strictly typed (`mypy --strict`), Ruff-clean `zava_forward.core.ledger_digest_blob` module and focused unit test suite in `src/core/tests/test_ledger_digest_blob.py`, harden Bicep parameter/output/immutability wiring in `infra/main.bicep`, `infra/modules/storage.bicep`, and `infra/modules/containerapps.bicep`, and add deterministic Bicep policy and mutation tests in `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py`.

### User Decisions and Requirements Highlights

* Keep changes scoped to `src/core`, `src/core/tests/`, `infra/`, and `infra/tests/` on branch `feat/demo-115-blob-ledger` (stacked child targeting `feat/demo-164-chat-grounding-provenance-0900`, PR #1641).
* Enforce both Issue #115 criteria deterministically offline: (1) digests land in an immutable container with a verified time-based retention lock (`allowProtectedAppendWrites: false`, `allowProtectedAppendWritesAll` absent/not enabled per Azure Storage ARM mutual exclusivity, locked policy / `x-ms-immutability-policy-mode: locked` when lock verification is required); and (2) scheduled verification emits a sanitized mismatch alert (`LEDGER_DIGEST_ALERT`, exit code 1, suppressing `LEDGER_DIGEST_OK`) on any chain tamper, truncation, head/year anchor mismatch, missing/malformed remote anchor, configuration failure, or retention-lock violation, backed by verified Azure Monitor alert rules.
* Run focused validation (`src/core` unit tests, `infra/tests` unit tests, `mypy`, and `ruff check` / `ruff format --check` plus `az bicep build` / `az bicep lint`); do not run `tools/rpi-checks.py` and do not push.
* Commit all code and `.copilot-tracking/` artifacts with `Refs #115` and the required `Co-authored-by` trailer because live Legal retention-period sign-off, irreversible Azure `lockImmutabilityPolicy` execution, live hosted alert delivery, and second-person initial reconciliation remain human/live gates.

### What You May Not Know

* Azure Storage ARM (`Microsoft.Storage/storageAccounts/blobServices/containers/immutabilityPolicies@2024-01-01`) treats `properties.state` as read-only (`Unlocked` on `PUT`; locking requires the irreversible `lockImmutabilityPolicy` POST action after Legal approves retention duration), and `infra/tests/test_bicep_policy.py:2032` explicitly asserts `state` is absent from Bicep `properties`. Our `src/core` verifier therefore distinguishes template-time unlocked configuration from runtime/control-plane `Locked` enforcement rather than fabricating `state: 'Locked'` in Bicep.
* `src/core` enforces a strict architectural dependency rule (`ALLOWED = {"core"}` in `src/core/tests/test_dependency_rule.py`), so canonical Blob ledger digest constants (`ALERT_MARKER`, `OK_MARKER`, `CONTAINER_VAR`, `DEFAULT_CONTAINER`) and retention-lock/mismatch verification belong in `src/core` rather than importing from `src/orchestrator`.

### Unresolved Decisions or Blockers

* None for offline/Bicep implementation and focused validation. Human/live operational prerequisites (Legal retention duration approval under #121, irreversible Azure policy lock execution, live scheduled job and alert delivery, and second-person reconciliation) remain explicitly open under `Refs #115`.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop continuously without pausing (`rpi-research`, `rpi-plan`, `rpi-plan-critique`, `rpi-implement`, `rpi-review`) with dated artifacts under `.copilot-tracking/` (User prompt).
* Inspect and strengthen ledger digest publication, immutable container retention-lock enforcement, and scheduled mismatch alerting in `src/core` and `infra/` for Issue #115 criteria (`Digests land in an immutable container with a retention lock` and `Scheduled verification alerts on mismatch`) (User prompt; Issue #115; `docs/adrs/0002-pilot-readiness-architecture.md:83`).
* Enforce and test deterministic offline/Bicep retention-lock policy checks and scheduled mismatch alert behavior in `src/core/tests/` and `infra/tests/` (User prompt).
* Use the focused validation tier (`src/core` and `infra/tests` unit tests, `ruff`, `mypy`) and do not run `tools/rpi-checks.py` (User prompt).
* Commit all code and `.copilot-tracking/` artifacts on `feat/demo-115-blob-ledger` with `Refs #115` and trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push (User prompt; `.github/copilot-instructions.md`).

## Goals

* Provide a strictly typed (`mypy --strict`), dependency-clean `src/core` module (`zava_forward.core.ledger_digest_blob`) that deterministically enforces create-only Blob ledger digest publication, container/ARM and Blob-header time-based retention-lock verification, and scheduled verification mismatch alerting (`LEDGER_DIGEST_ALERT` vs `LEDGER_DIGEST_OK`) without leaking credentials or storage endpoints.
* Close Bicep immutability-policy and scheduled-verification wiring gaps across `infra/main.bicep`, `infra/modules/storage.bicep`, and `infra/modules/containerapps.bicep` without violating Azure ARM read-only `state` semantics or existing `ledgerVerify` job command contracts.
* Prove both Issue #115 contracts offline via focused positive, negative, fault-injection, and Bicep-mutation unit tests in `src/core/tests/` and `infra/tests/`.

## Scope and Non-Goals

### In Scope

* New typed module `src/core/src/zava_forward/core/ledger_digest_blob.py` (plus narrow `disallow_untyped_calls = false` entry in `src/core/pyproject.toml` for `zava_forward.core.ledger_digest_blob`, `test_ledger_digest_blob`, and `tests.test_ledger_digest_blob` calling legacy untyped `zava_forward.core.ledger` and `zava_forward.core.documents`, preserving full `mypy --strict` checking on `ledger_digest_blob` and its tests).
* New unit test module `src/core/tests/test_ledger_digest_blob.py` (max 1 new test file in `src/core/tests/`, exact test removals: `none`).
* Targeted Bicep hardening in `infra/modules/storage.bicep`, `infra/main.bicep`, and `infra/modules/containerapps.bicep` (preserving `allowProtectedAppendWrites: false` without mutually-exclusive `allowProtectedAppendWritesAll` on `digestRetention`, top-level `@minValue(1) param ledgerDigestImmutabilityDays int = 365` forwarded to `storage`, `output ledgerDigestContainer` wired through `main.bicep` to `containerapps.bicep` `ZF_DIGEST_CONTAINER`).
* Expanded Bicep policy, provider-alignment, and mutation-rejection tests in `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py` (0 new test files in `infra/tests/`, exact test removals: `none`), plus concise accuracy updates in `src/core/README.md` / `infra/README.md` if directly describing module exports or `ledgerDigestImmutabilityDays`.

### Non-Goals

* Modifying `src/api`, `src/agents`, `src/importer`, web UI files, or `.github/workflows/*.yml` (whose SHA hashes are pinned in `tools/rpi-checks.py`).
* Setting a fabricated `state: 'Locked'` property on ARM `immutabilityPolicies` in Bicep or claiming live irreversible Azure lock execution / Legal retention sign-off.
* Running `tools/rpi-checks.py` or pushing commits to `origin`.

## Functional Requirements

* **FR-1 (Container & ARM Retention-Lock Policy Verification)**: `zava_forward.core.ledger_digest_blob.verify_container_retention_lock` evaluates container public-access settings, `immutabilityPolicies/default` existence, `state == "Locked"` (when `require_locked=True`, the default), `immutabilityPeriodSinceCreationInDays >= min_retention_days` (strict integer `>= 1`), `allowProtectedAppendWrites is False`, `allowProtectedAppendWritesAll` absent (rejecting both simultaneous `allowProtectedAppendWrites` + `allowProtectedAppendWritesAll` per ARM mutual exclusivity and any `True` append-write setting), and optional account-level lifecycle deletion rule prefixes (`ledger-digests`, `ledger-digests/...`, or empty account-wide prefix) so unlocked, missing, shortened, append-writable, mutually-exclusive invalid ARM, or lifecycle-deleted policies fail deterministically.
  * Observable acceptance criteria: `src/core/tests/test_ledger_digest_blob.py` proves locked compliant policies pass while unlocked, missing, zero/short retention, `bool` retention, `allowProtectedAppendWrites=True`, `allowProtectedAppendWritesAll` present/True, public containers, and overlapping `ledger-digests/` lifecycle rules each fail with explicit non-secret problem codes.
* **FR-2 (Blob REST Response Retention-Lock Header Verification & Create-Only Digest Store)**: `BlobLedgerDigestStore` performs HTTPS-only create-only JSON uploads (`If-None-Match: *`) at root canonical names (`digest-{count:010d}.json` and `year-{YYYY}.json`, matching `digest_blob.py` and ignoring volatile `"at"` timestamps on `409`/`412` logical-anchor verification), strict `<EnumerationResults>` paginated XML listing validation, and `GET` reads with header capture; `verify_blob_retention_headers` verifies `x-ms-immutability-policy-mode == "locked"` (case-insensitive) and a valid timezone-aware `x-ms-immutability-policy-until-date` strictly after `as_of` UTC (and `>= created_at + min_retention_days` when `created_at` is supplied), rejecting unlocked or missing headers when `require_retention_lock=True`.
  * Observable acceptance criteria: `src/core/tests/test_ledger_digest_blob.py` proves create-only idempotency (including differing `"at"` timestamps), conflict refusal on divergent logical anchor fields, strict malformed-XML listing rejection, no overwrite/delete surface, and immediate rejection of missing, `unlocked`, or expired `x-ms-immutability-policy-*` headers when `require_retention_lock=True`.
* **FR-3 (Scheduled Verification & Sanitized Mismatch Alerting)**: `publish_ledger_digests`, `verify_ledger_digests`, `reconcile_ledger_digests`, and `run_scheduled_verification` (plus `python -m zava_forward.core.ledger_digest_blob` CLI entrypoint using `ZF_DIGEST_*` env vars and `LEDGER_DIGEST_RECONCILE_*` markers) verify local hash-chain integrity, remote `digest-{count:010d}.json` head anchors, remote `year-{YYYY}.json` year anchors, and optional retention-lock requirements; on any mismatch, tamper, truncation, stale/missing/malformed anchor, missing/invalid scheduled env configuration, retention-lock failure, or transport error, `run_scheduled_verification` / CLI returns `exit_code == 1`, emits `LEDGER_DIGEST_ALERT` with diagnostic metadata sanitized via `monitoring_coverage.sanitize_diagnostic` (`runbook="ledger-digest-mismatch"`, `proposed_owner="Digital service owner"`), and suppresses `LEDGER_DIGEST_OK`.
  * Observable acceptance criteria: `src/core/tests/test_ledger_digest_blob.py` proves clean runs emit `LEDGER_DIGEST_OK` (`exit_code == 0`, no `LEDGER_DIGEST_ALERT`) and every tamper, truncation, head/year mismatch, malformed anchor/XML, missing/invalid `ZF_DIGEST_*` configuration, unlocked retention policy/header, and secret-bearing transport exception emits `LEDGER_DIGEST_ALERT` (`exit_code == 1`, no `LEDGER_DIGEST_OK`, zero secret/URL/SAS leakage).
* **FR-4 (Bicep Immutability, Container Wiring & Scheduled Alert Mutation Enforcement)**: `infra/modules/storage.bicep` enforces `allowProtectedAppendWrites: false` (without `allowProtectedAppendWritesAll`) on `digestRetention` and exports `ledgerDigestContainer`; `infra/main.bicep` exposes `@minValue(1) param ledgerDigestImmutabilityDays int = 365`, passes it to `storage`, and wires `storage.outputs.ledgerDigestContainer` to `infra/modules/containerapps.bicep` (`ZF_DIGEST_CONTAINER`); `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py` enforce full retention, provider-constant alignment, scheduled job (`0 2 * * *`, `replicaRetryLimit: 0`), and `ledgerDigestMismatch` (`severity: 1`, `PT1H`/`PT1H`, `GreaterThan 0`) / `ledgerVerifyMissing` (`severity: 1`, `PT1H`/`P1D`, `PT26H`, `LessThan 1`) alert contracts with mutation rejection.
  * Observable acceptance criteria: `REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -v`, `az bicep build`, and `az bicep lint` pass with zero warnings/errors, and mutations toggling `allowProtectedAppendWrites`, adding `allowProtectedAppendWritesAll`, breaking `ledgerDigestImmutabilityDays` forwarding or `ledgerDigestContainer` wiring, overlapping `staffResultsLifecycle` with `ledger-digests/`, altering `ledgerVerify` retry/schedule, or weakening `ledgerDigestMismatch` / `ledgerVerifyMissing` alert thresholds/markers/enabled states/action groups are deterministically rejected.

## Non-Functional Requirements

* **NFR-1 (Strict Typing, Linting, and Dependency Isolation)**
  * Objective threshold or evaluation condition: Zero errors under `mypy` (`strict = true` in `src/core`), zero violations under `ruff check` and `ruff format --check` (`E,F,I,B,UP`, line-length 100, py312) in `src/core` and touched `infra/tests/*.py` files, and `imported_projects <= {"core"}` in `src/core/tests/test_dependency_rule.py`.
  * Operating condition or verification approach: Run `ruff`, `mypy`, and `unittest` directly in `src/core` and `ruff` + `unittest` in `infra/tests` against editable workspace installs of `src/core` and `src/orchestrator`.
  * Observable acceptance criteria: All lint, format, type-check, and dependency-rule checks exit 0.
* **NFR-2 (Secret Redaction & Honest Governance Boundaries)**
  * Objective threshold or evaluation condition: Zero SAS signatures, bearer tokens, storage hostnames, or raw connection strings in exceptions, logs, or alert lines; zero false claims of live Azure `Locked` state on Bicep-authored `Unlocked` ARM policies.
  * Operating condition or verification approach: Sentinel-secret assertions across all error and alert paths in `src/core/tests/test_ledger_digest_blob.py` and ARM `state`-absence assertions in `infra/tests/test_bicep_policy.py`.
  * Observable acceptance criteria: Sentinel assertions and Bicep policy assertions pass 100%.

## Acceptance Criteria

* [ ] AC-1: `src/core/src/zava_forward/core/ledger_digest_blob.py` implements typed create-only Blob digest publication/verification, ARM + Blob-header retention-lock verification, and sanitized scheduled mismatch alert evaluation (`LEDGER_DIGEST_ALERT` / `LEDGER_DIGEST_OK`) without importing any workload outside `zava_forward.core`.
* [ ] AC-2: `src/core/tests/test_ledger_digest_blob.py` deterministically verifies retention-lock enforcement (locked vs unlocked/missing/short/append-writable/expired headers and policies), create-only idempotency and conflict refusal, chain/head/year mismatch alerting, malformed listing/anchor alerting, and secret redaction.
* [ ] AC-3: `infra/main.bicep`, `infra/modules/storage.bicep`, and `infra/modules/containerapps.bicep` wire `ledgerDigestImmutabilityDays` (`@minValue(1)`, default `365`), `allowProtectedAppendWrites: false` (without `allowProtectedAppendWritesAll`), and `storage.outputs.ledgerDigestContainer` -> `ZF_DIGEST_CONTAINER`, compiling cleanly under `az bicep build` and `az bicep lint`.
* [ ] AC-4: `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py` verify `src/core` provider constant alignment, retention controls, `ledgerVerify` job schedule/retry/env wiring, `ledgerDigestMismatch` / `ledgerVerifyMissing` alert properties, and reject targeted mutations to each control.
* [ ] AC-5: Focused validation (`src/core` unit tests, `infra/tests` unit tests with `REQUIRE_AZ_BICEP=1`, `src/core` `mypy`, `ruff check`, `ruff format --check`) passes cleanly, and all code + `.copilot-tracking/` artifacts are committed on `feat/demo-115-blob-ledger` with `Refs #115` and trailer `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` without pushing.

## Test Ownership and Validation Lock

* **Canonical test targets**:
  * `src/core/tests/test_ledger_digest_blob.py` (new, max 1 new test file added; semantic unit + fault-injection + secret-redaction coverage for `zava_forward.core.ledger_digest_blob`).
  * `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py` (existing files extended in place; policy-as-code + mutation-rejection coverage for `infra/main.bicep`, `infra/modules/storage.bicep`, and `infra/modules/containerapps.bicep`).
* **Exact test removals**: `none`.
* **Maximum new test files**: `1` (`src/core/tests/test_ledger_digest_blob.py`).
* **Generated targets**: `none` (Bicep ARM JSON is compiled ephemerally in memory via `az bicep build --stdout` during tests).
* **Validation commands (focused tier, after editable install of `src/core` and `src/orchestrator`)**:
  * `src/core`: `python3 -m unittest discover -s tests -v`, `ruff check .`, `ruff format --check .`, `mypy`
  * `infra`: `az bicep build --file infra/main.bicep --stdout > /dev/null`, `az bicep lint --file infra/main.bicep`, `REQUIRE_AZ_BICEP=1 python3 -m unittest discover -s infra/tests -v`, `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 infra/tests/test_bicep_policy.py infra/tests/test_monitoring_alerts.py`, `ruff format --isolated --line-length 100 --check infra/tests/test_bicep_policy.py infra/tests/test_monitoring_alerts.py`

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md                                                             |
| Phase details                    | .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md                                                  |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/immutable-blob-ledger-digests-115-plan-critique.md with Revise disposition (PC-001..PC-005 resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-research.md                                                      |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md is created by implementation as its evidence record    |
| Planning execution and readiness | Complete and Ready for implementation (all 5 planner-direct critique findings applied)                                                   |
| Continuation context             | Confirmed automatic RPI Agent session continues directly to `rpi-implement` and `rpi-review`                                             |

## Sources

* `.copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-research.md`: Primary research evidence (`C1`–`C18`) and convergence selection (Option A).
* `docs/adrs/0002-pilot-readiness-architecture.md`: Decision 2 and DH-007 immutable Blob ledger digest and scheduled verification architecture.
* `src/core/src/zava_forward/core/ledger.py`, `documents.py`, `ranking_archive_blob.py`, `monitoring_coverage.py`: Core hash-chain, Blob REST, strict XML listing, and diagnostic sanitization patterns.
* `infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_monitoring_alerts.py`: Infrastructure immutability policy, scheduled job, Azure Monitor alert rules, and policy/mutation tests.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Immutable Blob Ledger Digest & Scheduled Alerting Contract

* Intent: Introduce `zava_forward.core.ledger_digest_blob` and `src/core/tests/test_ledger_digest_blob.py` so `src/core` deterministically enforces immutable container retention-lock policies/headers, create-only digest publication/verification, and sanitized scheduled mismatch alerting under `mypy --strict` and `ruff`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `zava_forward.core.ledger_digest_blob` and `pyproject.toml` typing boundary

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1, NFR-2 (`C1`–`C6`, `C16`).
* Expected result: `src/core/src/zava_forward/core/ledger_digest_blob.py` provides canonical markers/env constants, `verify_container_retention_lock`, `verify_blob_retention_headers`, `BlobLedgerDigestStore`, `publish_ledger_digests`, `verify_ledger_digests`, `run_scheduled_verification`, and CLI `main`, passing `mypy --strict` and `ruff`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add unit, fault-injection, retention-lock, and mismatch-alert tests in `src/core/tests/test_ledger_digest_blob.py`

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1, NFR-2 (`C2`–`C6`, `C17`); update `src/core/README.md` module list if needed (`C18`).
* Expected result: `src/core/tests/test_ledger_digest_blob.py` covers ARM/policy lock checks, Blob immutability headers, create-only publication/idempotency/conflict refusal, chain/head/year tamper and truncation mismatch alerts, malformed listing/anchor alerts, CLI exit codes, and sentinel secret redaction.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Bicep Immutability Wiring & Scheduled Mismatch Alert Policy/Mutation Tests

* Intent: Harden `infra/modules/storage.bicep`, `infra/main.bicep`, and `infra/modules/containerapps.bicep` for `ledger-digests` immutability retention and container wiring, and enforce full retention + scheduled mismatch alert contracts with mutation rejection in `infra/tests/`.
* Dependencies: P01 (`zava_forward.core.ledger_digest_blob` constants used for cross-layer alignment assertions in `infra/tests/test_bicep_policy.py`).

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Harden `storage.bicep`, `main.bicep`, and `containerapps.bicep` ledger digest immutability and container wiring

* Requirement and evidence: FR-4, NFR-2 (`C7`–`C10`, `C14`); update `infra/README.md` parameter reference if needed (`C18`).
* Expected result: `digestRetention` keeps `allowProtectedAppendWrites: false` without mutually-exclusive `allowProtectedAppendWritesAll` or read-only ARM `state`; `storage.bicep` outputs `ledgerDigestContainer`; `main.bicep` exposes `@minValue(1) param ledgerDigestImmutabilityDays int = 365`, forwards it to `storage`, and wires `storage.outputs.ledgerDigestContainer` to `containerapps.bicep` `ZF_DIGEST_CONTAINER`.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Expand `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py` with retention-lock and scheduled mismatch alert mutation tests

* Requirement and evidence: FR-4, NFR-1, NFR-2 (`C10`–`C15`).
* Expected result: Policy tests assert `src/core` constant alignment, `digestRetention` properties/wiring/lifecycle isolation, `ledgerVerify` schedule/retry/command/env wiring, and `ledgerDigestMismatch` / `ledgerVerifyMissing` operators, thresholds, severities, windows, scopes, and action groups, plus deterministic mutation rejection for each control.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Focused Validation, Tracking Reconciliation, Review & Local Commit

* Intent: Run focused unit tests, Bicep build/lint, `mypy`, and `ruff` across `src/core` and `infra/`, reconcile tracking artifacts, complete `rpi-review`, and commit with `Refs #115` without pushing.
* Dependencies: P01, P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute focused validation suite and reconcile implementation evidence

* Requirement and evidence: AC-1 through AC-5, NFR-1, NFR-2 (`C16`, `C18`).
* Expected result: All `src/core` tests, `infra/tests` (`REQUIRE_AZ_BICEP=1`), `az bicep build`/`lint`, `mypy`, and `ruff check`/`ruff format --check` pass with zero errors, recorded in `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md

## Dependencies

* Editable local install of `src/core` (and `src/orchestrator` where `infra/tests/test_bicep_policy.py` imports `zava_forward.orchestrator.digest_blob`): required so `unittest` and `mypy` resolve workspace sources cleanly.
* Azure CLI with Bicep (`az bicep`): verified present (`/usr/bin/az`, Python 3.12.3, `ruff`, `mypy`) for `REQUIRE_AZ_BICEP=1` compilation tests.

## Critique Disposition

Single final-candidate `rpi-plan-critique` executed (`.copilot-tracking/reviews/plans/2026-11-15/immutable-blob-ledger-digests-115-plan-critique.md`, verdict `Revise`, 5 `planner-direct` findings). All five findings were resolved directly in this plan and phase details without re-running critique.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` (Critical): ARM mutual exclusivity of `allowProtectedAppendWrites` and `allowProtectedAppendWritesAll` | Resolved | Removed `allowProtectedAppendWritesAll: false` from `storage.bicep` `digestRetention`; updated `verify_container_retention_lock` and `test_bicep_policy.py` to enforce `allowProtectedAppendWrites is False` and `"allowProtectedAppendWritesAll" not in props`. |
| `PC-002` (High): Root anchor names, `"at"` idempotency, `ZF_DIGEST_*` env vars, reconcile markers, lifecycle prefixes, and `sanitize_diagnostic` | Resolved | Aligned `ledger_digest_blob.py` with `digest-{count:010d}.json` and `year-{YYYY}.json` root names, logical anchor comparison ignoring `"at"`, `ZF_DIGEST_*` env constants, `LEDGER_DIGEST_RECONCILE_*` markers, `ledger-digests/` lifecycle prefix detection, and `monitoring_coverage.sanitize_diagnostic`. |
| `PC-003` (High): Exact `main.bicep` / `containerapps.bicep` alert and job property assertions in `P02-T02` | Resolved | Updated `P02-T02` to assert `ledgerDigestMismatch` (`PT1H`/`PT1H`), `ledgerVerifyMissing` (`severity == 1`, `PT1H`/`P1D`, `overrideQueryTimeRange == "PT26H"`), `ZF_DIGEST_ACCOUNT_URL == parameters('blobEndpoint')`, evaluated `concat(...)` `env`, and `evaluate(...)` on ARM `immutabilityPeriodSinceCreationInDays`. |
| `PC-004` (Medium): `pyproject.toml` test overrides, `mypy` scope, and editable workspace package install | Resolved | Added `test_ledger_digest_blob` and `tests.test_ledger_digest_blob` to `src/core/pyproject.toml`, scoped `mypy` to `src/core`, and locked editable workspace install of `src/core` and `src/orchestrator` prior to focused tests. |
| `PC-005` (Medium): Scheduled CLI missing/invalid env configuration alerting | Resolved | Updated FR-3 and `P01-T01` so scheduled runs emit sanitized `LEDGER_DIGEST_ALERT` (`exit_code == 1`) when `ZF_DIGEST_*` settings are missing or invalid. |

## Follow-Up Items

* Execute owner/Legal retention-duration sign-off (#121 / ADR-0002 Decision 2) and run the irreversible Azure `lockImmutabilityPolicy` operation on the live `ledger-digests` container, followed by live hosted `ledgerVerify` / Azure Monitor alert delivery verification and second-person initial-publication reconciliation (human/live operational gate outside offline scope; owned by Digital service owner & Legal).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None
