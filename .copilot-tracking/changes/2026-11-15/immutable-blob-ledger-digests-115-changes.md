<!-- markdownlint-disable-file -->
# RPI Changes: Immutable Blob ledger digests and scheduled verification (Issue #115)

## Metadata

* Task ID: issue-115-immutable-blob-ledger-digests
* Related plan: .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (P01, P02, P03)
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01
* All remaining active-plan markers: None
* Status basis: All three phases (`P01`, `P02`, `P03`) completed and verified against the focused validation suite (`src/core` 3,582 unit tests, `ruff`, `mypy`; `az bicep build`/`lint`; `REQUIRE_AZ_BICEP=1` `infra/tests` 599 unit tests and `ruff`).

## Execution Summary

Delivered `zava_forward.core.ledger_digest_blob` (`src/core`) with deterministic ARM/container retention-lock and Blob WORM header verification, create-only `If-None-Match: *` Blob digest publication and reconciliation, and sanitized `LEDGER_DIGEST_OK` / `LEDGER_DIGEST_ALERT` scheduled CLI verification, alongside hardened Bicep wiring (`ledgerDigestImmutabilityDays` and `ledgerDigestContainer`) and positive/mutation policy tests across `infra/tests/`.

## Completed Work

### Core Immutable Blob Ledger Digest Verifier and Scheduled Alerting

* Related phase or task: `P01`, `P01-T01`, `P01-T02`
* Files: `src/core/src/zava_forward/core/ledger_digest_blob.py`, `src/core/pyproject.toml`, `src/core/README.md`, `src/core/tests/test_ledger_digest_blob.py`
* What changed and why: Implemented `verify_container_retention_lock` (distinguishing pre-lock ARM template inspection from runtime `state == "Locked"` WORM enforcement, enforcing `immutabilityPeriodSinceCreationInDays >= min_retention_days`, `allowProtectedAppendWrites is False`, ARM append-write flag mutual exclusivity, `publicAccess == "None"`, and storage lifecycle deletion prefix disjointness), `verify_blob_retention_headers`, create-only `BlobLedgerDigestStore` (`If-None-Match: *` with read-back logical digest equality on `409`/`412` and strict `<EnumerationResults>` XML listing), `publish_ledger_digests`, `verify_ledger_digests`, `reconcile_ledger_digests`, `run_scheduled_verification`, and `main()` emitting `LEDGER_DIGEST_OK` (`exit_code=0`) or sanitized `LEDGER_DIGEST_ALERT` (`exit_code=1`) via `monitoring_coverage.sanitize_diagnostic` with zero secret leakage. Added 18 focused unit tests covering all positive, negative, tamper, truncation, header, and CLI error paths.
* Completion evidence: `cd src/core && ruff check . && ruff format --check . && PYTHONPATH=src:tests mypy && python -m unittest discover -s tests -q` passed (3,582/3,582 tests including 18/18 in `test_ledger_digest_blob.py`; 344 files checked by `mypy`).
* Validation: Passed (`unittest`, `ruff check`, `ruff format --check`, `mypy`).

### Bicep Immutability Wiring and Scheduled Mismatch Alert Policy/Mutation Tests

* Related phase or task: `P02`, `P02-T01`, `P02-T02`
* Files: `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep`, `infra/main.bicep`, `infra/README.md`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_monitoring_alerts.py`
* What changed and why: Exported `ledgerDigestContainer` (`containers[5]`, `'ledger-digests'`) from `infra/modules/storage.bicep`, added `@minValue(1) param ledgerDigestImmutabilityDays int = 365` in `infra/main.bicep` forwarded to `storage` (preserving `allowProtectedAppendWrites: false` without mutually exclusive `allowProtectedAppendWritesAll` or read-only ARM `state`), bound `storage.outputs.ledgerDigestContainer` to `infra/modules/containerapps.bicep` `ZF_DIGEST_CONTAINER` on `ledgerVerify`, documented parameter wiring in `infra/README.md`, and expanded `infra/tests/test_bicep_policy.py` and `infra/tests/test_monitoring_alerts.py` to feed compiled ARM `digestRetention` properties, container properties, and lifecycle `prefixMatch` rules through `zava_forward.core.ledger_digest_blob.verify_container_retention_lock`, enforce `ledgerVerify` + `ledgerDigestMismatch` + `ledgerVerifyMissing` contracts and runbook/coverage parity, and reject 30 targeted negative mutations (12 retention mutations + 18 job/alert mutations).
* Completion evidence: `az bicep build` and `az bicep lint` on `infra/main.bicep`, `infra/modules/storage.bicep`, and `infra/modules/containerapps.bicep` exited 0; `REQUIRE_AZ_BICEP=1 python -m unittest discover -s infra/tests -q` passed (599/599 tests); scoped `ruff check` and `ruff format --check` passed.
* Validation: Passed (`az bicep build`, `az bicep lint`, `unittest`, `ruff check`, `ruff format --check`).

### Focused Validation and Pre-Review Reconciliation

* Related phase or task: `P03`, `P03-T01`
* Files: `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md`, `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md`
* What changed and why: Ran the complete focused validation tier across `src/core` and `infra/` (explicitly omitting `tools/rpi-checks.py` per caller instruction), cleaned up temporary `/tmp/zf-115-venv` and `/tmp/zf-115-main.json` artifacts, verified zero `.copilot-tracking/` references in production diffs, and reconciled all plan markers (`P01`–`P03`) and changes evidence ahead of `rpi-review`.
* Completion evidence: Zero failures across 3,582 `src/core` tests, 599 `infra/tests` tests, `mypy`, `ruff`, and `az bicep build`/`lint`.
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

None; implementation matched the post-critique approved plan (`PC-001`–`PC-005`) without divergence.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `src/core` unit tests | `src/core/tests` (`unittest discover -s tests -q`) | Passed | 3,582 tests passed (including 18/18 in `test_ledger_digest_blob.py`, `test_device_registry_azure.py`, `test_live_doc_links.py`) |
| `src/core` lint & format | `src/core` (`ruff check .`, `ruff format --check .`) | Passed | All checks passed; 291 files formatted |
| `src/core` strict typing | `src/core` (`PYTHONPATH=src:tests mypy`) | Passed | `Success: no issues found in 344 source files` |
| Bicep build & lint | `infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep` | Passed | `az bicep build` and `az bicep lint` exited 0 with zero template diagnostics |
| `infra/tests` suite | `infra/tests` (`REQUIRE_AZ_BICEP=1 unittest discover -s tests -q`) | Passed | 599 tests passed (including positive controls + 12 retention mutations + 18 ledger job/alert mutations) |
| `infra/tests` lint & format | `infra/tests/test_bicep_policy.py`, `infra/tests/test_monitoring_alerts.py` | Passed | `ruff check` and `ruff format --check` (`--line-length 100 --target-version py312`) passed |
| Full local RPI gate (`tools/rpi-checks.py`) | Repository-wide | Skipped | Explicitly excluded by caller instruction (`Validation Tier: Focused`; do NOT run `tools/rpi-checks.py`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`, `P03`, `P03-T01` all `[x]`; zero drift from phase details)
* Completed-work evidence and handoff prose: Reconciled and complete
* Validation, blockers, remaining work, and follow-up items: Reconciled; zero blockers, zero remaining active-plan items
* Review readiness: Ready for `rpi-review`

## Blockers

* None.

## Remaining Work

* None in the active plan (`P01`–`P03` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md, `## Follow-Up Items`
* Live Azure subscription execution proof: After Legal sets retention duration and an authorized Azure owner deploys and locks `immutabilityPolicies/default` (`state == "Locked"`), execute live Container Apps Job `ledger-verify` and record observed `LEDGER_DIGEST_OK` and synthetic mismatch `LEDGER_DIGEST_ALERT` delivery against Issue #115.
* Optional orchestrator refactor: Delegate `zava_forward.orchestrator.digest_blob` internals to `zava_forward.core.ledger_digest_blob` in a separate orchestrator-scoped PR.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan; completed: P01, P01-T01, P01-T02, P02, P02-T01, P02-T02, P03, P03-T01; remaining: none
* Validation coverage: Focused tier complete (`src/core` 3,582 tests + `ruff` + `mypy`; `infra` `az bicep build`/`lint` + 599 `REQUIRE_AZ_BICEP=1` tests + `ruff`)
* Blockers: None
* Current plan and detail updates: All active plan markers checked (`[x]`)
* Planning and critique state: Ready (`PC-001`–`PC-005` resolved)
* Follow-up items: Live Azure lock/alert proof; optional orchestrator refactor
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Parent confirmed automatic RPI Agent
