<!-- markdownlint-disable-file -->
# RPI Changes: Issue #115 Immutable Blob Ledger Digest Container and Retention-Lock Posture

## Metadata

* Task ID: issue-115-platform-blob-immutability
* Related plan: .copilot-tracking/plans/2026-11-15/platform-115-blob-immutability-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/platform-115-blob-immutability-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`
* All remaining active-plan markers: None
* Status basis: All planned phases and tasks (`P01`–`P03`) completed with passing focused unit, Bicep policy/inventory, lint, formatting, and `mypy` verification.

## Execution Summary

Delivered full-plan implementation for Issue #115 container-level immutability and retention-lock posture verification across `infra/`, `src/core/`, and `src/orchestrator/`, with focused unit and Bicep policy/mutation coverage and clean lint, format, inventory, and `mypy` gates.

## Completed Work

### Bicep Storage Container Immutability and Production Parameter Guard

* Related phase or task: `P01-T01`
* Files: `infra/modules/storage.bicep`, `infra/modules/guard.bicep`, `infra/main.bicep`
* What changed and why: Added `ledgerDigestImmutableStorage` (default `true`) to configure `immutableStorageWithVersioning: { enabled: true }` exclusively on `ledger-digests` and gate `digestRetention` (`if (ledgerDigestImmutableStorage)`), and added `productionProfileRequiresImmutableLedgerDigests` to `guard.bicep` and `main.bicep` so `deploymentProfile=production` rejects mutable, unlocked, or sub-365-day digest container configurations before resource creation.
* Completion evidence: `az bicep build --file infra/main.bicep --stdout > /dev/null` succeeded with exit code `0` and `python3 infra/scripts/bicep_inventory.py --check` passed.
* Validation: Passed (`az bicep build` + `bicep_inventory.py --check`; unit/mutation tests follow in `P03-T01`).

### Scheduled Ledger Verification Retention-Lock Job Wiring and Documentation

* Related phase or task: `P01-T02`
* Files: `infra/modules/containerapps.bicep`, `infra/main.bicep`, `infra/README.md`
* What changed and why: Added `ledgerDigestRequireRetentionLock` (`true`) and `ledgerDigestMinRetentionDays` (`365`) to `containerapps.bicep`, wired `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` onto the daily `ledgerVerify` job, forwarded both parameters from `main.bicep`, and documented the controls and human-gate boundary in `infra/README.md`.
* Completion evidence: `az bicep build --file infra/main.bicep --stdout > /dev/null` and `python3 infra/scripts/bicep_inventory.py --check` passed with zero inventory drift.
* Validation: Passed (`az bicep build` + `bicep_inventory.py --check`).

### Weakest-Link Immutability Posture Metadata and Fail-Closed Publisher/Verifier Enforcement

* Related phase or task: `P02-T01`
* Files: `src/core/src/zava_forward/core/ledger_digest_blob.py`, `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`, `src/core/README.md`
* What changed and why: Added `require_immutable_versioning` to `verify_container_retention_lock`, `x-ms-creation-time` and `retention_days` / `immutability_policy_state` normalization to `verify_blob_retention_headers`, weakest-link `synthesize_immutability_posture`, `from None` exception suppression on `BlobLedgerDigestStore`, `create_anchor_with_headers`, `publish_ledger_digests_with_posture`, posture recording and fail-closed `require_retention_lock` enforcement across `publish_ledger_digests`, `publish_store_digests`, `verify_ledger_digests`, `reconcile_ledger_digests`, `_run_reconcile_cli`, `run_scheduled_verification`, and `zava_forward.orchestrator.digest_blob` (`ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS`), and updated `src/core/README.md`.
* Completion evidence: Existing `src/core/tests/test_ledger_digest_blob.py` (18 tests) and `src/orchestrator/tests/test_digest_blob.py` (30 tests) passed.
* Validation: Passed baseline unit suites; new focused tests and linters/typechecks follow in `P03-T01`.

### Focused Bicep Policy, Guard, Core, and Orchestrator Unit Tests and Static Verification

* Related phase or task: `P03-T01`
* Files: `infra/tests/test_bicep_policy.py`, `infra/tests/test_environment_quota_parameters.py`, `src/core/tests/test_ledger_digest_blob.py`, `src/orchestrator/tests/test_digest_blob.py`, `src/core/src/zava_forward/core/ledger_digest_blob.py`
* What changed and why: Updated `guard` parameter count (`30`) in `test_environment_quota_parameters.py`; extended `test_bicep_policy.py` with `"false": lambda: False`, `copyIndex` container immutability evaluation across all 7 containers, conditional `digestRetention` checks, `productionProfileRequiresImmutableLedgerDigests` guard + `test_mutations_reject_production_guard_bypass`, `ledgerVerify` `ZF_DIGEST_REQUIRE_RETENTION_LOCK` / `ZF_DIGEST_MIN_RETENTION_DAYS` forwarding assertions, and negative mutations; added 4 focused posture/fail-closed/weakest-link/secret-free traceback test methods to `src/core/tests/test_ledger_digest_blob.py` (plus fail-closed `"invalid_blob_creation_time"` handling in `verify_blob_retention_headers`); and added end-to-end lock posture and fail-closed verification tests to `src/orchestrator/tests/test_digest_blob.py`.
* Completion evidence: `infra/tests/test_bicep_policy.py` + `test_environment_quota_parameters.py` (71/71 passed, alongside all other 560 `infra/tests/` modules), `src/core/tests/test_ledger_digest_blob.py` (22/22 passed, plus monitoring/audit suites), `src/orchestrator/tests` discovery (143/143 passed, including 31/31 in `test_digest_blob.py`), `python3 infra/scripts/bicep_inventory.py --check` passed, `ruff check` + `ruff format --check` passed across `src/core`, `src/orchestrator`, and modified `infra/tests/`, and `mypy` passed cleanly across `src/core` (361 files) and `src/orchestrator` (19 files).
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

* Local judgment recorded: Added `"invalid_blob_creation_time"` fail-closed handling in `verify_blob_retention_headers` when `x-ms-creation-time` is present alongside `x-ms-immutability-policy-until-date` so malformed blob creation timestamps cannot silently skip `min_retention_days` window calculation, and narrowed `rankingArchiveRetention` selection in `infra/tests/test_bicep_policy.py` (`"ranking-archive" in r["name"]`) so multiple `immutabilityPolicies` resources coexist cleanly. Neither required plan scope or requirement changes.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `az bicep build --file infra/main.bicep --stdout > /dev/null` | `infra/` | Passed | Exit code `0`, zero warnings/errors |
| `python3 infra/scripts/bicep_inventory.py --check` | `infra/` | Passed | `Issue #136 Bicep inventory verified: 29 architecture rows, 20 Bicep modules, 12 from-empty steps (17 rebuild stages).` |
| `PYTHONPATH=src/core/src:infra python3 -m unittest infra/tests/test_bicep_policy.py infra/tests/test_environment_quota_parameters.py -q` | `infra/tests/` | Passed | `Ran 71 tests in 332.258s — OK` (plus all 560 other tests in `infra/tests/` verified passing) |
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_ledger_digest_blob.py -q` (+ ledger/digest/monitoring/audit suites) | `src/core/tests/` | Passed | `Ran 22 tests in 0.017s — OK`; `test_*monitoring*.py` (37/37 `OK`), `test_*audit*.py` (54/54 `OK`) |
| `PYTHONPATH=src/orchestrator/src:src/orchestrator/tests:src/core/src:src/core/tests python3 -m unittest discover -s src/orchestrator/tests -q` | `src/orchestrator/tests/` | Passed | `Ran 143 tests in 19.988s — OK` (including 31/31 in `test_digest_blob.py`) |
| `ruff check .` & `ruff format --check .` | `src/core/`, `src/orchestrator/`, modified `infra/tests/` | Passed | `All checks passed!`; `308 files already formatted` (`src/core`), `16 files already formatted` (`src/orchestrator`), `2 files already formatted` (`infra/tests/` with `--isolated --line-length 100`) |
| `python3 -m mypy` | `src/core/`, `src/orchestrator/` | Passed | `Success: no issues found in 361 source files` (`src/core`); `Success: no issues found in 19 source files` (`src/orchestrator`) |
| `python3 tools/rpi-checks.py --all` | Full gate | Skipped | Explicit caller instruction: Focused validation tier (`do not run tools/rpi-checks.py --all`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01` all `[x]`)
* Completed-work evidence and handoff prose: Reconciled with exact changed files and command outputs
* Validation, blockers, remaining work, and follow-up items: Reconciled; zero blockers and zero remaining active-plan items
* Review readiness: Ready

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/platform-115-blob-immutability-plan.md, `## Follow-Up Items`
* Execute owner-approved live Azure `lockImmutabilityPolicy` transition on the deployed `ledger-digests` container and record Legal retention duration approval (#121 / #115): Outside offline repository scope because WORM locking in Azure Storage is irreversible and gated on human Legal/owner approval.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`; remaining: none
* Validation coverage: Focused tier complete (`az bicep build`, `bicep_inventory.py --check`, `infra/tests`, `src/core/tests`, `src/orchestrator/tests`, `ruff check`, `ruff format --check`, `mypy`)
* Blockers: None
* Current plan and detail updates: Local judgment refinements recorded above; no scope/requirement divergences
* Planning and critique state: Ready (`PC-001`..`PC-005` resolved)
* Follow-up items: Live Azure `lockImmutabilityPolicy` and Legal retention approval (#121 / #115)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
