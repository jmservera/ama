<!-- markdownlint-disable-file -->
# Review: Issue #115 Immutable Blob Ledger Digest Container and Retention-Lock Posture

## Scope and Evidence

* Task ID: issue-115-platform-blob-immutability
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Bicep container-level immutability (`immutableStorageWithVersioning`, conditional `digestRetention`), `production`-profile fail-closed guard (`productionProfileRequiresImmutableLedgerDigests`), `ledgerVerify` lock env wiring (`ZF_DIGEST_REQUIRE_RETENTION_LOCK`, `ZF_DIGEST_MIN_RETENTION_DAYS`), weakest-link container/blob immutability posture metadata (`immutability_policy_state`, `retention_days`, `locked`, plus human-gate honesty flags) and fail-closed enforcement across `src/core` and `src/orchestrator`, focused unit and Bicep policy/mutation coverage, and human/cloud-gated live Azure WORM boundary
* Plan: .copilot-tracking/plans/2026-11-15/platform-115-blob-immutability-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/platform-115-blob-immutability-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/platform-115-blob-immutability-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/platform-115-blob-immutability-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/platform-115-blob-immutability-research.md, working-tree `git diff`, independent bounded review lens (`rubber-duck`), and local validation runs

## Opening Review State

* Interpreted review goal: Verify once, from reconciled plan/details/critique/changes artifacts and exact repository diffs, whether `P01`–`P03` satisfy all functional and non-functional requirements, acceptance criteria, and critique dispositions (`PC-001`–`PC-005`) for Issue #115 without crossing the human/cloud-gated live Azure `lockImmutabilityPolicy` boundary.
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01`)
* Evidence readiness: Ready — plan, phase details, plan critique, changes log, and research artifacts are reconciled with all `P01`–`P03` markers checked `[x]` and focused validation recorded.
* Acceptance basis: `FR-1`–`FR-4`, `NFR`s, 6 plan Acceptance Criteria, Critique Dispositions `PC-001`–`PC-005`, and repository honesty/security rules (`sanitize_diagnostic` schema, secret-free exceptions, human-gated live WORM lock).
* First comparison boundary: `P01` Bicep storage immutability, `guard.bicep` `production` enforcement, and `containerapps.bicep` `ledgerVerify` env wiring against `FR-1`, `FR-2`, `PC-001`, `PC-002`, and `PC-003`.
* Active read-only boundaries: Read-only against source code, tests, research, plan, details, critique, and changes record; writes permitted only to `.copilot-tracking/reviews/logs/2026-11-15/platform-115-blob-immutability-review.md` (and parent RPI state JSON).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass post-implementation review on 2026-11-15 across reconciled `P01`–`P03` plan, phase details, plan critique (`PC-001`–`PC-005`), changes log, working-tree `git diff` (`infra/`, `src/core/`, `src/orchestrator/`), independent read-only `rubber-duck` lens, and passing focused validation outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01` | Bicep Storage Container Immutability and Production Parameter Guard | Reconciled | `[x]` in plan; `infra/modules/storage.bicep`, `infra/modules/guard.bicep`, and `infra/main.bicep` match `FR-1`, `FR-2`, and `PC-002`. |
| `P01` / `P01-T02` | Scheduled Ledger Verification Retention-Lock Job Wiring and Documentation | Reconciled | `[x]` in plan; `infra/modules/containerapps.bicep`, `infra/main.bicep`, and `infra/README.md` match `FR-2`, `PC-001`, and `PC-003` with zero `bicep_inventory.py --check` drift. |
| `P02` / `P02-T01` | Weakest-Link Immutability Posture Metadata and Fail-Closed Publisher/Verifier Enforcement | Reconciled | `[x]` in plan; `src/core/src/zava_forward/core/ledger_digest_blob.py`, `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`, and `src/core/README.md` satisfy `FR-3`, `FR-4`, and `PC-001`–`PC-005`. |
| `P03` / `P03-T01` | Focused Bicep Policy, Guard, Core, and Orchestrator Unit Tests and Static Verification | Reconciled | `[x]` in plan; `infra/tests/test_bicep_policy.py`, `infra/tests/test_environment_quota_parameters.py`, `src/core/tests/test_ledger_digest_blob.py`, and `src/orchestrator/tests/test_digest_blob.py` pass with `ruff` and `mypy`. |
| `Follow-Up Items` | Execute owner-approved live Azure `lockImmutabilityPolicy` transition and record Legal retention duration approval (`#121` / `#115`) | Reconciled | Kept outside active `Pxx` / `Pxx-Txx` scope in both plan and changes record, preserving the human/cloud-gate honesty boundary (`Refs #115`). |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `infra/modules/storage.bicep`, `infra/modules/guard.bicep`, `infra/main.bicep` | Added `ledgerDigestImmutableStorage` (`true`), configured `immutableStorageWithVersioning: { enabled: true }` exclusively on `ledger-digests`, gated `digestRetention` with `if (ledgerDigestImmutableStorage)`, and added `productionProfileRequiresImmutableLedgerDigests` guard. | Compiled ARM template (`az bicep build`) sets `immutableStorageWithVersioning` only on `ledger-digests` and enforces `production` fail-closed parameter guard across all 30 guard parameters. | Passed (`az bicep build`, `71/71` in `test_bicep_policy.py` + `test_environment_quota_parameters.py`) | Reconciled |
| `P01-T02` | `infra/modules/containerapps.bicep`, `infra/main.bicep`, `infra/README.md` | Added `ledgerDigestRequireRetentionLock` (`true`) and `ledgerDigestMinRetentionDays` (`365`), wired `ZF_DIGEST_REQUIRE_RETENTION_LOCK` and `ZF_DIGEST_MIN_RETENTION_DAYS` onto `ledgerVerify`, and documented the `#115` controls and human WORM lock boundary. | Compiled `containerapps.bicep` and `main.bicep` forward both env vars and pass `bicep_inventory.py --check`. | Passed (`bicep_inventory.py --check`, `test_bicep_policy.py` positive + negative mutation checks) | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/ledger_digest_blob.py`, `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py`, `src/core/README.md` | Added `require_immutable_versioning`, `x-ms-creation-time` + `min_retention_days` header checks, weakest-link `synthesize_immutability_posture` (with `live_worm_lock_human_gated=True` and `retention_schedule_human_gated=True`), `from None` secret-free exceptions, and fail-closed posture recording across `publish`, `verify`, `reconcile`, and `run_scheduled_verification`. | All publisher, verifier, reconcile, and scheduled CLI flows record `immutability_policy_state`, `retention_days`, `locked` and fail closed when lock enforcement is enabled. | Passed (`22/22` in `test_ledger_digest_blob.py`, `143/143` in `src/orchestrator/tests`, `ruff`, `mypy`) | Reconciled |
| `P03-T01` | `infra/tests/test_bicep_policy.py`, `infra/tests/test_environment_quota_parameters.py`, `src/core/tests/test_ledger_digest_blob.py`, `src/orchestrator/tests/test_digest_blob.py` | Added `copyIndex`/`false` policy evaluator support, `production` guard-bypass and `ledgerVerify` env mutations, and focused publisher/verifier/weakest-link/secret-free traceback tests. | Positive and negative mutation assertions cover container immutability, conditional `digestRetention`, guard bypass, `ledgerVerify` env vars, weakest-link posture, and fail-closed errors. | Passed (`71/71` `infra/tests`, `22/22` `test_ledger_digest_blob.py`, `31/31` `test_digest_blob.py`, `ruff`, `mypy`) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T01` / `P03-T01` | Added `"invalid_blob_creation_time"` fail-closed problem when `x-ms-creation-time` is present but unparseable, and narrowed `rankingArchiveRetention` filter (`"ranking-archive" in r["name"]`) in `infra/tests/test_bicep_policy.py`. | Triggered during `P03-T01` unit and Bicep test verification; local engineering judgment requiring no user decision. | Recorded under `## Implementation-Time Plan and Detail Updates` in `.copilot-tracking/changes/2026-11-15/platform-115-blob-immutability-changes.md`; preserved approved intent and acceptance criteria. | Not needed (`PC-001`–`PC-005` and `Ready` plan state preserved). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All 5 planner-owned critique findings (`PC-001` through `PC-005`) were resolved in `.copilot-tracking/plans/2026-11-15/platform-115-blob-immutability-plan.md` (`## Critique Disposition`) and verified in implementation (`orchestrator/digest_blob.py` lock env enforcement, conditional `digestRetention` + `require_immutable_versioning`, `copyIndex`/`false` evaluator + guard-bypass mutations, weakest-link posture synthesis + reconcile parity, and `from None` exception sanitization + `sanitize_diagnostic` schema preservation).
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No material plan-changing discovery occurred; sequential `P01` -> `P02` -> `P03` execution respected declared dependencies without early resumption.
* Justification assessment: Supported by direct code, Bicep compilation, and unit/mutation test evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Execute owner-approved live Azure `lockImmutabilityPolicy` transition on deployed `ledger-digests` container and record Legal retention duration approval (`#121` / `#115`) | Irreversible Azure Storage WORM policy locking and retention-duration approval are cloud/human-gated under ADR-0002 and Objective 3. | Repository owner and Legal (`#121` / `#115`) after live deployment verification. | Open operational gate; routed to distinct follow-up owner (never treated as an offline code defect; PR/commit remains `Refs #115`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Reset `blob.last_immutability_posture` at entry to `run_scheduled_verification` across in-process store reuse

* Related scope: `P02-T01`
* Evidence: `src/core/src/zava_forward/core/ledger_digest_blob.py` (`run_scheduled_verification` exception handlers read `blob.last_immutability_posture` when `report is None`; while the scheduled `ledgerVerify` Container Apps Job instantiates a fresh store per container run, an in-process caller reusing one `BlobLedgerDigestStore` across two runs could observe the prior run's posture if the second run fails with a pre-posture transport error).
* Impact: Non-blocking in production scheduled execution (fresh process per job run and `exit_code == 1` + `LEDGER_DIGEST_ALERT` still fire), but clearing `blob.last_immutability_posture = None` at the start of `run_scheduled_verification` prevents stale posture metadata under in-process store reuse.
* Destination: `follow_up` (`rpi-implement` optional hardening child task)
* Smallest useful next action: Clear `blob.last_immutability_posture = None` at the start of `run_scheduled_verification` and add a two-call store-reuse transport-failure unit test in `src/core/tests/test_ledger_digest_blob.py`.

<!-- rpi:review id=RV-002 -->
### RV-002 [Low]: Optional pre-`PUT` existing-anchor header probe and anchor `published_at` timestamp fallback when `x-ms-creation-time` is stripped

* Related scope: `P02-T01`
* Evidence: `src/core/src/zava_forward/core/ledger_digest_blob.py` and `src/orchestrator/src/zava_forward/orchestrator/digest_blob.py` (`verify_blob_retention_headers` treats `x-ms-creation-time` as optional per `P02-T01` detail spec so minimal two-header test stubs remain backward-compatible, and data-plane-only `publish` learns container WORM header state from the first anchor response rather than probing an existing blob via `GET` beforehand).
* Impact: Non-blocking on Azure Blob Storage `2024-08-04` (which always emits `x-ms-creation-time` on `GET` responses, while `ledgerVerify` holds data-plane-only `Storage Blob Data Contributor` RBAC without ARM control-plane permissions), but probing one existing remote anchor before `PUT` when the container is non-empty and falling back to anchor JSON `published_at` on `GET` when `x-ms-creation-time` is absent hardens non-empty unlocked containers against writing even one anchor before aborting.
* Destination: `follow_up` (`rpi-implement` optional hardening child task)
* Smallest useful next action: Probe the latest remote head anchor via `read_anchor_with_headers` before `PUT` when `require_retention_lock=True` and remote anchors exist, and pass `published_at` as fallback `created_at` in `verify_ledger_digests` / `reconcile_ledger_digests` when `x-ms-creation-time` is absent.

## Defects

* None against the accepted `P01`–`P03` plan requirements and acceptance criteria.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | `follow_up` (`rpi-implement` child task if selected) | Reset `blob.last_immutability_posture = None` at `run_scheduled_verification` entry + unit test | Non-blocking defensive hardening for in-process `BlobLedgerDigestStore` reuse |
| `RV-002` | `follow_up` (`rpi-implement` child task if selected) | Pre-`PUT` existing-anchor header probe + `published_at` fallback when `x-ms-creation-time` is absent | Non-blocking data-plane defensive hardening beyond `P02-T01` backward-compatibility spec |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Execute owner-approved live Azure `lockImmutabilityPolicy` transition on the deployed `ledger-digests` container and record Legal retention schedule approval (`#121` / `#115`), kept outside offline repository scope per ADR-0002 and Objective 3.
* Optional defensive hardening items `RV-001` and `RV-002` above if selected as follow-up child tasks.

## Blockers and Remaining Work

* Blockers: None for the offline repository implementation (`P01`–`P03`); human Legal/owner approval and live Azure `lockImmutabilityPolicy` remain external gates before closing `#115`.
* Remaining active work: None (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P03`, `P03-T01` are complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `az bicep build --file infra/main.bicep --stdout > /dev/null` | `infra/` | Passed | Exit code `0`, clean ARM compilation |
| `python3 infra/scripts/bicep_inventory.py --check` | `infra/` | Passed | `29 architecture rows, 20 Bicep modules, 12 from-empty steps (17 rebuild stages)` verified |
| `PYTHONPATH=src/core/src:infra python3 -m unittest infra/tests/test_bicep_policy.py infra/tests/test_environment_quota_parameters.py -q` | `infra/tests/` | Passed | `Ran 71 tests in 332.258s — OK` (plus all 560 other tests in `infra/tests/` verified passing) |
| `PYTHONPATH=src/core/src:src/core/tests python3 -m unittest src/core/tests/test_ledger_digest_blob.py -q` (+ monitoring/audit suites) | `src/core/tests/` | Passed | `Ran 22 tests in 0.017s — OK`; monitoring (`37/37 OK`) and audit (`54/54 OK`) suites passed |
| `PYTHONPATH=src/orchestrator/src:src/orchestrator/tests:src/core/src:src/core/tests python3 -m unittest discover -s src/orchestrator/tests -q` | `src/orchestrator/tests/` | Passed | `Ran 143 tests in 19.988s — OK` (including `31/31` in `test_digest_blob.py`) |
| `ruff check .` & `ruff format --check .` | `src/core/`, `src/orchestrator/`, modified `infra/tests/` | Passed | Zero lint or formatting issues across `src/core` (`308` files), `src/orchestrator` (`16` files), and modified `infra/tests/` (`2` files, `--isolated --line-length 100`) |
| `python3 -m mypy` | `src/core/`, `src/orchestrator/` | Passed | `Success: no issues found in 361 source files` (`src/core`); `Success: no issues found in 19 source files` (`src/orchestrator`) |
| `python3 tools/rpi-checks.py --all` | Full repository gate | Skipped | Explicit caller instruction: Focused validation tier (`do not run tools/rpi-checks.py --all`) |

## Outcome

* Outcome: Residual work
* Outcome rationale: All planned `P01`–`P03` tasks, functional/non-functional requirements (`FR-1`–`FR-4`), plan acceptance criteria, and critique dispositions (`PC-001`–`PC-005`) are implemented, reconciled, and verified under the Focused validation tier with zero blocking defects, while live Azure `lockImmutabilityPolicy` activation and Legal retention duration approval (`#121` / `#115`) plus optional low-severity hardening items (`RV-001`, `RV-002`) remain explicit non-blocking residual follow-ups.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | None | None |
| Decision gap or invalid assumption | None | None |
| Material evidence gap | None | None |
| Non-blocking residual work | Distinct follow-up (`#121` / `#115` owner & Legal; optional `RV-001` / `RV-002` child hardening) | Execute live Azure `lockImmutabilityPolicy` after Legal approves retention schedule; optionally select `RV-001` or `RV-002` at post-Review checkpoint |

* Execution status: Complete
* Outcome: Residual work
* Validation coverage: Focused tier passed (`az bicep build`, `bicep_inventory.py --check`, `infra/tests` `71/71`, `src/core` `22/22` + monitoring/audit suites, `src/orchestrator` `143/143`, `ruff check`, `ruff format --check`, `mypy`); full `tools/rpi-checks.py --all` intentionally skipped per caller instruction.
* Blockers: None for repository commit; live Azure WORM policy locking and Legal retention duration (`#121`) remain external human/cloud gates before closing `#115`.
