<!-- markdownlint-disable-file -->
# Review: Immutable Blob ledger digests and scheduled verification (Issue #115)

## Scope and Evidence

* Task ID: issue-115-immutable-blob-ledger-digests
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Offline deterministic `src/core` Blob ledger digest retention-lock/header verifier, create-only publication and scheduled mismatch alerting (`zava_forward.core.ledger_digest_blob`), hardened Bicep immutability and container wiring (`infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep`), positive and negative-mutation tests (`src/core/tests/test_ledger_digest_blob.py`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_monitoring_alerts.py`), and focused-tier validation evidence (`Refs #115`).
* Plan: .copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/immutable-blob-ledger-digests-115-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-research.md (`C1`–`C18`), independent read-only review lens on changed source/Bicep/test files, and focused validation suite outputs.

## Opening Review State

* Interpreted review goal: Verify whether completed full-plan implementation (`P01`–`P03`) satisfies FR-1 through FR-4, NFR-1, NFR-2, AC-1 through AC-5, and all five resolved plan-critique dispositions (`PC-001`–`PC-005`) while keeping live Azure WORM locking and live Azure Monitor firing explicitly bounded as follow-up operational work (`Refs #115`).
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; plan, phase details, plan critique, research, changes record, source diffs, and focused validation results are reconciled and available.
* Acceptance basis: FR-1..FR-4, NFR-1..NFR-2, AC-1..AC-5, and `PC-001`..`PC-005` in `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md`.
* First comparison boundary: Reconcile `P01`–`P03` markers, `PC-001`–`PC-005` resolutions, and changed `src/core` + `infra/` artifacts against the plan and phase details without mutating source or prior tracking records.
* Active read-only boundaries: This review creates and updates only `.copilot-tracking/reviews/logs/2026-11-15/immutable-blob-ledger-digests-115-review.md` (and parent RPI session state).
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single post-implementation `rpi-review` pass on 2026-11-15 across `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md`, `.copilot-tracking/details/2026-11-15/immutable-blob-ledger-digests-115-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/immutable-blob-ledger-digests-115-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md`, `.copilot-tracking/research/2026-11-15/immutable-blob-ledger-digests-115-research.md`, and all changed files in `src/core/` and `infra/`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Core Immutable Blob Ledger Digest Verifier and Scheduled Alerting | Reconciled | `zava_forward.core.ledger_digest_blob`, `src/core/pyproject.toml`, `src/core/README.md`, and `src/core/tests/test_ledger_digest_blob.py` (18 unit tests) match planned contracts and `PC-001`, `PC-002`, `PC-004`, `PC-005`. |
| `P02` (`P02-T01`, `P02-T02`) | Bicep Immutability Wiring and Scheduled Mismatch Alert Policy/Mutation Tests | Reconciled | `infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep`, `infra/README.md`, `infra/tests/test_bicep_policy.py`, and `infra/tests/test_monitoring_alerts.py` match planned contracts and `PC-001`, `PC-003`, `PC-004`. |
| `P03` (`P03-T01`) | Focused Validation and Pre-Review Reconciliation | Reconciled | Full focused validation tier (`src/core` 3,582 tests, `ruff`, `mypy`; `az bicep build`/`lint`; `REQUIRE_AZ_BICEP=1` `infra/tests` 599 tests and `ruff`) executed and recorded; local commit executes immediately after persisting final review and session-state artifacts so the single commit captures the review log. |
| `Follow-Up Items` | Live Azure WORM policy locking / Monitor execution proof; optional `src/orchestrator` delegation refactor | Reconciled | Preserved outside active `Pxx`/`Pxx-Txx` scope in both plan and changes record (`Refs #115`). |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01`, `P01-T01`, `P01-T02` | `src/core/src/zava_forward/core/ledger_digest_blob.py`, `src/core/pyproject.toml`, `src/core/README.md`, `src/core/tests/test_ledger_digest_blob.py` | Added strictly typed offline retention-lock/WORM header verifier, create-only `If-None-Match: *` Blob digest store, publication/verification/reconciliation helpers, sanitized `LEDGER_DIGEST_OK` / `LEDGER_DIGEST_ALERT` CLI runner, and 18 unit tests. | Module and 18 unit tests verified against `FR-1`..`FR-3`, `NFR-1`..`NFR-2`, `AC-1`, `AC-2`, `AC-4`. | Passed (`3,582` `src/core` tests, `ruff check`, `ruff format --check`, `mypy` across 344 files) | Reconciled |
| `P02`, `P02-T01`, `P02-T02` | `infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep`, `infra/README.md`, `infra/tests/test_bicep_policy.py`, `infra/tests/test_monitoring_alerts.py` | Exposed `@minValue(1) param ledgerDigestImmutabilityDays int = 365`, exported `storage.outputs.ledgerDigestContainer` (`ledger-digests`) into `containerapps` `ZF_DIGEST_CONTAINER`, fed compiled ARM properties into `verify_container_retention_lock`, verified `ledgerVerify` + `ledgerDigestMismatch` + `ledgerVerifyMissing` contracts and runbook anchors, and added 30 negative mutations (12 retention + 18 job/alert). | Compiled Bicep templates and 599 `infra/tests` checks verified against `FR-4`, `AC-3`, `AC-4`. | Passed (`az bicep build`/`lint` on 3 Bicep files, `599` `infra/tests` under `REQUIRE_AZ_BICEP=1`, scoped `ruff check`/`format --check`) | Reconciled |
| `P03`, `P03-T01` | `.copilot-tracking/plans/2026-11-15/immutable-blob-ledger-digests-115-plan.md`, `.copilot-tracking/changes/2026-11-15/immutable-blob-ledger-digests-115-changes.md` | Executed focused validation sweep, removed temporary `/tmp/zf-115-venv` and `/tmp/zf-115-main.json`, verified zero `.copilot-tracking/` leaks in `src/` and `infra/`, and reconciled plan/changes state. | Validation table and checklist markers complete. | Passed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None | No implementation-time plan or phase-detail revisions were needed; execution matched the post-critique approved plan. | None | Checklist completion markers `[x]` updated across `P01`–`P03` and mirrored in changes record. | Not needed (`PC-001`–`PC-005` remained authoritative). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All five `planner-direct` findings (`PC-001` ARM `allowProtectedAppendWrites` vs `allowProtectedAppendWritesAll` mutual exclusivity and read-only `state`; `PC-002` root `digest-XXXXXXXXXX.json`/`year-YYYY.json` grammar, `ZF_DIGEST_*` env names, markers, and `sanitize_diagnostic`; `PC-003` exact `main.bicep` and `containerapps.bicep` resource/env structure; `PC-004` `pyproject.toml` `disallow_untyped_calls = false` override and `src/core`-only `mypy`; `PC-005` scheduled alert emission on missing/invalid `ZF_DIGEST_*` configuration) were applied before implementation and verified in code and tests.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No pause required; `P01` -> `P02` -> `P03` executed in dependency order.
* Justification assessment: Supported by repository code, compiled ARM output, and test results.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Live Azure WORM policy locking (`lockImmutabilityPolicy`) and hosted `ledger-verify` / Azure Monitor alert execution proof (`Refs #115`) | Requires human Legal approval of retention duration (`#121`), deployed Azure subscription resources, and irreversible owner ARM lock action. | Project owner + Legal/Compliance + Digital service owner | Open distinct follow-up work; keeps PR correctly labeled `Refs #115` rather than `Closes #115`. |
| Delegate `zava_forward.orchestrator.digest_blob` internals to `zava_forward.core.ledger_digest_blob` | Caller scoped active code changes to `src/core` and `infra/` and `test_bicep_policy.py` pins the existing orchestrator module entrypoint. | Later `src/orchestrator` refactoring PR | Open distinct follow-up work; cross-module constant parity is already enforced in `infra/tests/test_bicep_policy.py`. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Suppress exception cause chaining on `BlobLedgerDigestStore` transport errors for library-caller traceback safety

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/ledger_digest_blob.py` (`BlobLedgerDigestStore._send` raises `LedgerDigestBlobError` / `LedgerDigestBlobUncertain` `from exc`). CLI `run_scheduled_verification` and `main()` catch `LedgerDigestBlobError` without printing tracebacks and emit only `monitoring_coverage.sanitize_diagnostic(...)` tokens (verified by `test_ledger_digest_blob.py`), so scheduled console logs do not leak secrets; however, a future library caller formatting an uncaught traceback would render `__cause__`.
* Impact: Defense-in-depth hardening if future callers log full Python tracebacks around `BlobLedgerDigestStore` methods when SAS tokens or URLs appear inside custom transport exceptions.
* Destination: follow-up
* Smallest useful next action: Replace `from exc` with `from None` (or sanitize exception causes) in `BlobLedgerDigestStore._send` when wiring `zava_forward.orchestrator.digest_blob` to `zava_forward.core.ledger_digest_blob`, and add a `traceback.format_exception` redaction assertion.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Optional `before_year` expected sealed-year completeness check and `Creation-Time` header duration check in `verify_ledger_digests`

* Related scope: `P01-T01`
* Evidence: `src/core/src/zava_forward/core/ledger_digest_blob.py` (`verify_ledger_digests` and `run_scheduled_verification`). Scheduled `--publish` mode requires a matching current-head anchor (`check_current_head = True`) and verifies every remote `year-YYYY.json` anchor via `ledger.verify_years`, while `verify_blob_retention_headers` supports `created_at` + `min_retention_days` when passed explicitly; however, read-only `verify_ledger_digests` without `retention_policy` does not automatically parse `x-ms-creation-time` headers to enforce `min_retention_days` or require every historical year `< before_year` to have a `year-YYYY.json` blob if all year blobs were omitted prior to initial publication.
* Impact: Non-blocking defense-in-depth improvement for header-only retention verification (without ARM policy JSON) and strict post-cutover sealed-year presence auditing.
* Destination: follow-up
* Smallest useful next action: Parse `x-ms-creation-time` in `verify_ledger_digests` when `retention_policy is None` and accept an optional `require_sealed_years_before: int | str | None = None` parameter during the orchestrator consolidation follow-up.

## Defects

* None blocking active plan scope (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-5`).

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow-up` | Engineering follow-up alongside orchestrator `digest_blob` consolidation | Non-blocking defense-in-depth traceback hardening beyond CLI console contract (`FR-3`). |
| `RV-002` | `follow-up` | Engineering follow-up alongside orchestrator `digest_blob` consolidation | Non-blocking defense-in-depth enhancement for header-only duration parsing and optional sealed-year presence enforcement. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001` and `RV-002`: Low-severity defense-in-depth hardening in `zava_forward.core.ledger_digest_blob` (suppressing `__cause__` on transport errors and parsing `x-ms-creation-time` / optional `require_sealed_years_before` in `verify_ledger_digests`), suitable to bundle with the `zava_forward.orchestrator.digest_blob` delegation follow-up.
* Live Azure operational closure for Issue #115: Legal retention-period sign-off (`#121`), owner execution of `lockImmutabilityPolicy` (`state == "Locked"`), and live Container Apps Job + Azure Monitor alert delivery evidence.
* Refactor `zava_forward.orchestrator.digest_blob` internals to call `zava_forward.core.ledger_digest_blob` so Container Apps `ledger-verify` executes one shared implementation path.

## Blockers and Remaining Work

* Blockers: None for the scoped offline/Bicep `Refs #115` deliverable (live Issue #115 closure remains gated on human Legal retention sign-off and live Azure subscription execution).
* Remaining active work: Complete final local Git commit on `feat/demo-115-blob-ledger` containing all code, test, documentation, and `.copilot-tracking/` artifacts (`Refs #115`, no push).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python -m unittest discover -s tests -q` | `src/core` | Passed | 3,582 unit tests passed (including 18/18 in `test_ledger_digest_blob.py`, `test_device_registry_azure.py`, `test_monitoring_coverage.py`, `test_live_doc_links.py`). |
| `ruff check . && ruff format --check .` | `src/core` | Passed | Zero lint violations; 291 files formatted. |
| `PYTHONPATH=src:tests python -m mypy` | `src/core` | Passed | `Success: no issues found in 344 source files` (`mypy --strict` active). |
| `az bicep build` & `az bicep lint` | `infra/main.bicep`, `infra/modules/storage.bicep`, `infra/modules/containerapps.bicep` | Passed | All 3 Bicep entry/module files compiled and linted with zero template warnings or errors. |
| `REQUIRE_AZ_BICEP=1 python -m unittest discover -s tests -q` | `infra/tests` | Passed | 599 tests passed, including compiled ARM retention-lock verification via `verify_container_retention_lock`, `ledgerVerify` + `ledgerDigestMismatch` + `ledgerVerifyMissing` assertions, and 30 negative mutations. |
| `ruff check` & `ruff format --check` (`--isolated --line-length 100 --target-version py312`) | `infra/tests/test_bicep_policy.py`, `infra/tests/test_monitoring_alerts.py` | Passed | Zero lint or formatting issues. |
| `python3 tools/rpi-checks.py` | Repository-wide | Skipped | Explicitly skipped per user instruction (`Validation Tier: Focused`; do NOT run `tools/rpi-checks.py`). |

## Outcome

* Outcome: Residual work
* Outcome rationale: All planned `P01`–`P03` tasks, functional/non-functional requirements (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`), acceptance criteria, and critique dispositions (`PC-001`..`PC-005`) passed focused validation without blocking defects, while two Low-severity defense-in-depth items (`RV-001`, `RV-002`), orchestrator delegation, and live Azure WORM lock / Monitor alert execution proof (`Refs #115`) remain explicit follow-up work.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Bundle `RV-001` and `RV-002` with `zava_forward.orchestrator.digest_blob` delegation to `zava_forward.core.ledger_digest_blob`; complete owner/Legal live Azure WORM lock and Monitor proof for full Issue #115 closure. |

* Execution status: Complete
* Outcome: Residual work
* Validation coverage: Focused tier passed (`src/core` 3,582 tests, `ruff`, `mypy`; `az bicep build`/`lint`; `infra/tests` 599 tests under `REQUIRE_AZ_BICEP=1`, `ruff`); `tools/rpi-checks.py` skipped by explicit caller direction.
* Blockers: None for `Refs #115` local commit; full Issue #115 closure awaits human Legal retention approval (`#121`) and live Azure WORM lock/alert verification.
