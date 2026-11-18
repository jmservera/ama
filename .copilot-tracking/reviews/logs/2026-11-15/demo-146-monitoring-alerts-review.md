<!-- markdownlint-disable-file -->
# Review: Monitoring Alerts, Workbook, Runbooks, and Task/Release Harm Declarations (Issue #146)

## Scope and Evidence

* Task ID: issue-146
* Review date: 2026-11-15
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Bicep alert-to-runbook routing (`job-rank` / `job-rank-publish`), workbook boundary and cost-against-budget accuracy, 13-task and serving-release 6-indicator harm/quality/disparity/review-burden declarations, named-human live threshold approval enforcement, and Focused tier validation (`infra/tests`, `src/core/tests`, `src/api/tests/test_assistant_release.py`, `ruff`, `mypy`).
* Plan: .copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/demo-146-monitoring-alerts-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/demo-146-monitoring-alerts-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/demo-146-monitoring-alerts-research.md (`C1`-`C21`) and full `git diff` across 21 changed repository files (`infra/` and `src/`).

## Opening Review State

* Interpreted review goal: Independently verify that all planned `P01`, `P02`, and `P03` deliverables satisfy `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-5`, and `PC-001`..`PC-004` critique dispositions without regressions, governance overclaims, or privacy leaks.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready — reconciled plan, phase details, single-pass plan critique, changes log, research artifact, and Focused validation outputs are complete and aligned.
* Acceptance basis: `FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-5`, `PC-001`..`PC-004` dispositions, and Issue `#146` scope items.
* First comparison boundary: Plan-to-change reconciliation across `P01` (`infra/`), `P02` (`src/core/` and `src/api/tests/test_assistant_release.py`), `P03` (Focused validation), and `## Follow-Up Items`.
* Active read-only boundaries: `rpi-review` writes only `.copilot-tracking/reviews/logs/2026-11-15/demo-146-monitoring-alerts-review.md`; repository source and prior RPI stage artifacts remain read-only during Review.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed full read-only comparison on 2026-11-15 across all 21 changed repository files (`infra/` and `src/`), reconciled RPI artifacts, `az bicep build` compilation outputs, fresh Python module import-order verification, and Focused tier validation outputs (`598` `infra/tests`, `3,569` `src/core/tests`, `65` `src/api` release tests, `ruff`, and `mypy`).

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | Ranking Archive Job Alert Routing, Runbook Section, and Workbook Boundary Clarification | Reconciled | All planned Bicep, runbook, workbook, and `monitoring_coverage.ALERTS` changes match `FR-1` and `FR-2`. |
| `P01-T02` | Infrastructure Alert/Runbook Matrix Regression Tests and 100-Column Ruff Hygiene | Reconciled | All 7 `#146` `infra/tests/` monitoring modules pass 100-column `ruff` format/lint and `unittest`. |
| `P02`, `P02-T01` | Canonical 13-Task Harm Monitoring Declarations, Complete Review Effort, and Live Human Threshold Guards | Reconciled | All 13 registered AI tasks carry complete 6-indicator declarations with 4-stage `review_effort`, `approval_rate_is_safety: False`, and live human-approver guards. |
| `P02-T02` | Task Registration and Serving-Release Monitoring Contract Enforcement | Reconciled | `ai_registry`, `rai_release`, `assistant_release`, `assistants`, and `release_support` enforce task and serving-release declarations without import cycles or frozen-digest drift. |
| `P02-T03` | Focused Harm-Declaration and Live-Approval Unit Tests | Reconciled | `7` focused new unit tests added (`<= 14` bound) with `0` removals, plus `src/api/tests/test_assistant_release.py` fixture alignment. |
| `P03`, `P03-T01` | Focused Tier Full-Suite Execution and Temporary Venv Cleanup | Reconciled | Full `infra/tests`, `src/core/tests` (including `iothub` extra), `src/api/tests/test_assistant_release.py`, `ruff`, and `mypy` passed and `.venv-146-tmp` was removed cleanly. |
| `## Follow-Up Items` | External `OD-51`/`OQ-017`/`OQ-018` approvals, live KQL drills, Cost Management export, and optional `import-jobs-poison` producer | Reconciled | Kept outside active `Pxx`/`Pxx-Txx` completion claims and mirrored in changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `infra/modules/operationalMonitoring.bicep`, `infra/monitoring-runbooks.md`, `infra/monitoring-workbook.json`, `src/core/src/zava_forward/core/monitoring_coverage.py` | Routed `-rank` / `-rank-publish` job failures to `#job-rank` ahead of `'job-auth'`, added `### Job rank` runbook section, refreshed workbook candidate vs producerless-gap copy, and added `job-rank` (`CANDIDATE`) to `ALERTS`. | `az bicep build` on `main.bicep` and `operationalMonitoring.bicep` emits `#job-rank` with candidate rules disabled by default; `11` candidates align across Bicep, runbook, and `ALERTS`. | Passed (`598` `infra/tests`) | Reconciled |
| `P01-T02` | `infra/tests/test_monitoring_alerts.py`, `infra/tests/test_alert_runbook_signal_matrix.py`, `infra/tests/test_ai_alert_runbook_ownership.py`, `infra/tests/test_monitoring_workbook.py`, `infra/tests/test_monitoring_workbook_sla_budget.py`, `infra/tests/test_ai_observability_workbook_budget.py`, `infra/tests/test_diagnostic_log_privacy.py` | Added Bicep `#job-rank` routing test, added `job-rank` to signal and ownership matrices, added `strict=False` on `zip()`, and aligned 100-column `ruff` formatting. | `42` `#146` monitoring tests and isolated `ruff check` + `ruff format --isolated --line-length 100 --check` pass. | Passed | Reconciled |
| `P02-T01` | `src/core/src/zava_forward/core/monitoring_coverage.py` | Added `_named_human_approver`, `REVIEW_EFFORT_STAGES`, `live` enforcement and sequence-safe `effort_stages` / `approval_rate_is_safety` checks in `check_monitoring_declaration`, and `task_declaration(s)` for all 13 AI tasks. | All 13 task declarations evaluate `declared` (`offline_only=True`) offline and `blocked` when `live=True`. | Passed (`mypy` strict, `ruff`, `DeclarationTests`) | Reconciled |
| `P02-T02` | `src/core/src/zava_forward/core/ai_registry.py`, `src/core/src/zava_forward/core/rai_release.py`, `src/core/src/zava_forward/core/assistant_release.py`, `src/core/src/zava_forward/core/assistants.py`, `src/core/tests/release_support.py` | Bound `monitoring_declaration` to registered tasks and serving releases via cycle-safe lazy imports, enforced live named-human threshold approvals, and exposed `monitoring_status` in both `Assistants.registry` branches. | Fresh module import permutations succeed cycle-free; frozen `heldout_eval` digests remain untouched. | Passed (`test_heldout_eval.py`, `test_rai_release.py`, `test_assistant_release.py`) | Reconciled |
| `P02-T03` | `src/core/tests/test_monitoring_coverage.py`, `src/core/tests/test_ai_register_completeness.py`, `src/core/tests/test_rai_release.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py`, `src/api/tests/test_assistant_release.py` | Added focused tests for 13-task coverage, 4-stage review effort, bot/fictional approver rejection, weakened applicability denial, and live release threshold denial. | `7` focused test methods added (`0` removed); all edge cases verified. | Passed | Reconciled |
| `P03-T01` | `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md`, `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md`, `.copilot-tracking/changes/2026-11-15/demo-146-monitoring-alerts-changes.md` | Ran Focused validation in temporary `.venv-146-tmp` (`src/core[iothub]`, `src/agents`, `src/api`, `src/orchestrator`, `src/importer`), deleted `.venv-146-tmp`, and reconciled RPI records. | Clean `git status --short` with zero `.venv-146-tmp` or `.egg-info` artifacts left behind. | Passed | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `Test Ownership` and `P02-T03` (`src/api/tests/test_assistant_release.py`) | Updated `test_live_provider_needs_actual_release_with_serving_proof` and `test_contract_fields_required_on_authenticated_record_route` to reflect required `monitoring_declaration` and live human threshold approval on `evidence_class="actual"`. | Direct mutation of `constructed-fixture` dict to `evidence_class="actual"` properly failed live threshold validation; classified as an immediately-relevant current-state update requiring no new user decision. | Reconciled across plan `Test Ownership`, `P02-T03`, phase details `P02-T03`, and changes record `Implementation-Time Plan and Detail Updates`. | Critique `PC-001`..`PC-004` remained valid and Ready; repeat critique not needed. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four single-pass critique findings (`PC-001`..`PC-004`) were applied directly in `.copilot-tracking/plans/2026-11-15/demo-146-monitoring-alerts-plan.md` and `.copilot-tracking/details/2026-11-15/demo-146-monitoring-alerts-phase-details.md` before `P01` source edits began, and verified in implementation.
* Material revisions: None — the `src/api/tests/test_assistant_release.py` fixture update preserved approved intent and strengthened live fail-closed assertion coverage without altering requirements, scope, architecture, or acceptance criteria.
* Dependent-work pause assessment: No dependent work bypassed plan order or resumed prematurely.
* Justification assessment: Supported by concrete code, Bicep compilation, and test execution evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Appoint named human operational and RAI owners (`OD-51`, `OQ-017`, `OQ-018`) and execute live Log Analytics KQL drills before enabling candidate alerts | Requires customer governance appointment and live Azure workspace telemetry rather than repository source code | Programme Governance / Platform Engineering (`OD-51`) | Open external prerequisite; routed as distinct follow-up |
| Connect approved Azure Cost Management billing export before replacing `Unknown` / `Unreconciled` workbook cost columns | Requires live Azure billing export configuration | Finance Lead / Platform Operations | Open external prerequisite; routed as distinct follow-up |
| Add `import-jobs-poison` producer and alert rule only if `src/importer/` adopts queue dead-lettering instead of `quarantine`-only row isolation | Architectural choice per ADR 0001; no poison queue producer exists today | Data Import / Platform Engineering | Open conditional follow-up; routed as distinct follow-up |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Align word-token placeholder list in `monitoring_coverage.FICTIONAL_APPROVER_TOKENS` with `cohort_eval.FICTIONAL_OWNER_TOKENS`

* Related scope: `P02-T01`
* Evidence: `src/core/src/zava_forward/core/monitoring_coverage.py` (`FICTIONAL_APPROVER_TOKENS`) checks `{"fictional", "placeholder", "mock", "tbd", "synthetic", "fixture"}` (plus `rai_release.named()` exact-string rejection of `"unknown"` and `"unapproved"`), whereas `src/core/src/zava_forward/core/cohort_eval.py` (`FICTIONAL_OWNER_TOKENS`) also rejects `"example"`, `"todo"`, `"unapproved"`, and `"unknown"` at individual word-token granularity (for example `"TODO: appoint OD-51"` or `"Unknown Appointee"`).
* Impact: Non-blocking hardening opportunity; production tasks exclusively declare `constructed: True` thresholds (`live=False` only), and standard bot/placeholder strings (`system`, `agent`, `bot`, `copilot`, `fictional`, `placeholder`, `mock`, `tbd`, `synthetic`, `fixture`, exact `unknown`/`unapproved`) already fail closed.
* Destination: Distinct follow-up item
* Smallest useful next action: Unify `FICTIONAL_APPROVER_TOKENS` with `cohort_eval.FICTIONAL_OWNER_TOKENS` (and optionally `"pending"`) in a small shared helper in `rai_release.py` during a follow-up cleanup slice.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` | Distinct follow-up item | Core RAI / Monitoring cleanup slice: share unified word-level placeholder token tuple across `cohort_eval` and `monitoring_coverage` | Non-blocking token-list parity hardening; all Issue `#146` acceptance criteria and tests pass |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001`: Unify `monitoring_coverage.FICTIONAL_APPROVER_TOKENS` and `cohort_eval.FICTIONAL_OWNER_TOKENS` word-token sets in `rai_release.py`.
* Plan follow-up items (`OD-51` / `OQ-017` / `OQ-018` named human appointments and live KQL alert drills, Azure Cost Management billing export ingestion, and conditional `import-jobs-poison` producer) remain tracked outside this source slice (`Refs #146`).

## Blockers and Remaining Work

* Blockers: None.
* Remaining active work: None in RPI implementation/review scope; local git commit (`Refs #146`, no push) executes at closeout per caller instruction.

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `.venv-146-tmp/bin/python -m unittest discover -s infra/tests -q` | `infra/tests` (`main.bicep`, `operationalMonitoring.bicep`, workbook, runbooks, policy) | Passed | `Ran 598 tests in 227.927s — OK (skipped=4)` |
| `.venv-146-tmp/bin/python -m unittest discover -s tests -q` (`src/core` + `src/core[iothub]`) | `src/core/tests` (`3,569` unit tests) | Passed | `3,569` passed, `0` failed, `0` errors |
| `PYTHONPATH=src/core/tests:src/agents/tests .venv-146-tmp/bin/python -m unittest discover -s src/api/tests -p 'test_assistant_release.py' -q` | `src/api/tests/test_assistant_release.py` | Passed | `Ran 65 tests in 106.901s — OK (skipped=7)` (`ZF_TEST_MSSQL=1` skipped in Focused tier) |
| `ruff format --check . && ruff check . && mypy` (`src/core`) | `src/core` (`289` formatted files, `342` `mypy` strict files) | Passed | `289 files already formatted`, `All checks passed!`, `Success: no issues found in 342 source files` |
| `ruff check` & `ruff format --isolated --line-length 100 --check` (`infra/tests` `#146` suites + `src/api/tests/test_assistant_release.py`) | `7` `#146` `infra/tests` modules + updated `src/api` test | Passed | `All checks passed!`, `7 files already formatted` |
| `python3 tools/rpi-checks.py` | Full repository gate | Skipped | Excluded per caller instruction (`Validation Tier: Focused`; do NOT run `tools/rpi-checks.py`) |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every Issue `#146` source requirement and plan acceptance criterion (`FR-1`..`FR-4`, `NFR-1`..`NFR-2`, `AC-1`..`AC-5`, and `PC-001`..`PC-004` dispositions) is satisfied with verified Focused validation evidence, zero substantive defects, intact frozen evaluation digests, and honest separation of external live-environment prerequisites (`Refs #146`).

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | `RV-001` placeholder-token unification in `rai_release.py`, plus external `OD-51` live drills and Cost Management export connection |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed (`598` `infra/tests`, `3,569` `src/core/tests`, `65` `src/api` release tests, `ruff`, `mypy`; `tools/rpi-checks.py` skipped per caller instruction)
* Blockers: None
