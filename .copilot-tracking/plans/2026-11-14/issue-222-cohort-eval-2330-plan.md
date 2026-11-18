<!-- markdownlint-disable-file -->
# RPI Plan: Issue #222 Cohort and Missing-Data Evaluation Record (`OQ-018`)

## Task Metadata

* Task ID: issue-222-cohort-eval-2330
* Task slug: issue-222-cohort-eval-2330
* Planning status: Ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/issue-222-cohort-eval-2330-plan-critique.md

## Executive Summary

This plan closes the engineering enforcement gap on Issue #222 (`OQ-018`) so every cohort and missing-data evaluation record, runtime AI report, CLI JSON export, and HTTP evaluation export explicitly carries and enforces pre-live human owner approval (`owner_approval_status`, `lawful_analysis_fields_approved`) and explicit synthetic non-fairness provenance (`synthetic_not_fairness_evidence: True`, `non_fairness_provenance_notice`, `live_activation_allowed: False` until dated real-human owner sign-off on non-synthetic inputs). Existing paired cohort contrast, seeded-defect detection, count/error/review-burden/uncertainty reconciliation, small-sample insufficiency, and non-averaged subgroup threshold-blocking invariants remain intact and gain focused regression tests across `src/core`, `src/agents`, and `src/api`.

### User Decisions and Requirements Highlights

* Run the full automatic RPI loop (`research`, `plan`, `implement`, `review`) on `feat/ai-222-cohort-eval-2330` stacked on `origin/feat/demo-164-chat-grounding-provenance-0900`, validating at the Focused tier (`mypy`, `ruff check`, `ruff format --check`, focused unit/API tests) and committing locally with `Refs #222` without pushing.
* Expose and enforce `owner_approval_status` (defaulting to `"unapproved"` / `"pending_owner_approval"` when no dated human owner approval record for cohorts, lawful analysis fields, and thresholds is supplied), `lawful_analysis_fields_approved: bool`, and `synthetic_not_fairness_evidence: True` plus an explicit non-fairness provenance notice across runtime/API payloads and evaluation exports.

### What You May Not Know

* `rai_release.NON_HUMAN_TOKENS` omits `"fictional"`, `"placeholder"`, `"mock"`, and `"synthetic"`, so developer fixture strings like `"Data lead (fictional)"` would pass `named_human(...)` if given a future timestamp unless `cohort_eval` explicitly blocks fictional/placeholder tokens on dated/live owner approval.
* `src/core/tests/test_cohort_eval.py` exercises offline disposition and measurement mechanics using an undated fictional fixture (`approved(m)`), while `src/core/tests/test_rai_threshold_live_approval_guard.py` exercises `live=True` with named human owners and `expires = NOW + 3600`. Separating `owner_approval_status`, `lawful_analysis_fields_approved`, and `live_activation_allowed` from offline test-fixture mechanics preserves 100% backward compatibility while strictly blocking live fairness clearance and live activation without dated real-human owner approval.
* Python's shared user editable install on this VM points to `/home/azureuser/source/ama/src/...`; all Focused test runs must set explicit worktree-relative `PYTHONPATH` rather than mutating shared site-packages.

### Unresolved Decisions or Blockers

* None for engineering implementation. Human owner approval of production cohorts, lawful analysis fields, and thresholds (`OQ-018`) remains intentionally open outside code (`Refs #222`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Execute the full RPI loop (`research`, `plan`, `implement`, `review`) in order under `.copilot-tracking/` (`2026-11-14`) on branch `feat/ai-222-cohort-eval-2330` in `/home/azureuser/source/ama-demo-wt/feat-222-cohort-eval-2330` (user prompt).
* Enforce the pre-live owner-approval boundary (`OQ-018`) and synthetic non-fairness disclaimer in runtime/API payloads and evaluation exports: expose `owner_approval_status` (defaulting to pending/unapproved when no dated human owner approval record for cohorts, lawful analysis fields, and thresholds is supplied), `lawful_analysis_fields_approved: bool`, and `synthetic_not_fairness_evidence: True` with an explicit non-fairness provenance notice (user prompt; `.copilot-tracking/research/2026-11-14/issue-222-cohort-eval-2330-research.md`).
* Verify paired constructed cohort comparisons (sensor/source completeness, accessibility/contact need, appointment history), seeded unjustified exclusion/deprioritisation defect detection, per-cohort count/error/review-burden/uncertainty reconciliation, small/missing sample insufficiency, and threshold-breach blocking without averaging across subgroups (user prompt; Issue #222).
* Validate at the Focused tier (`python3 -m mypy`, `python3 -m ruff check . && python3 -m ruff format --check .`, and focused unit/API tests in modified project directories) without mutating shared global site-packages (user prompt; repository instructions).
* Configure repo-local `user.email` via `gh api user` (`{id}+{login}@users.noreply.github.com`), commit source, tests, docs, and `.copilot-tracking/` artifacts cleanly with `Refs #222` and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push (user prompt; repository instructions).

## Goals

* Make `OQ-018` pre-live dated real-human owner approval status and lawful-field approval explicit, machine-checkable, tamper-evident, and fail-closed on every cohort evaluation record and export.
* Guarantee synthetic cohort runs always emit `synthetic_not_fairness_evidence: True`, `fairness_evidence: False`, `live_activation_allowed: False`, and an explicit `OQ-018` non-fairness provenance notice across `core`, `agents`, CLI exports, and `api` endpoints.
* Prove all six Issue #222 invariants through focused unit and HTTP API tests while preserving every existing regression check.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/cohort_eval.py`: dated real-human owner approval validation, `owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, `non_fairness_provenance_notice`, `live=True` enforcement, and `export_record(...)`.
* `src/agents/src/zava_forward/agents/ai_eval.py`, `cohort_ranking_eval.py`, and `cohort_ai_eval.py`: propagation of new `OQ-018` approval/provenance fields in `cohort_report()` and canonical `export_record(...)` JSON CLI exports.
* `src/api/src/zava_forward/api/server.py`: `OQ-018` approval/provenance fields in `GET /api/ai/report` (`evaluation.cohorts`, preserving top-level `{"evaluation", "live", "registry", "consumption"}` contract) and manager-only `GET /api/ai/cohort-evaluation` endpoint serving `ai_eval.cohort_evaluation_export()`.
* Focused unit/API tests (`src/core/tests/`, `src/agents/tests/`, `src/api/tests/`) and directly coupled component README updates (`src/core/README.md`, `src/agents/README.md`, `src/api/README.md`).

### Non-Goals

* Inventing or recording production human owner sign-off for `OQ-018` (which remains open under human governance).
* Changing deterministic ranking order (`ranking.py`) or live AI activation policy (`ai_registry.py`).
* Running unrelated browser/SQL full-tier release gates or pushing to `origin`.

## Functional Requirements

* FR-1: `cohort_eval.evaluate(...)` computes and hashes `owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, and `non_fairness_provenance_notice`.
  * Observable acceptance criteria: Unapproved manifests emit `owner_approval_status == "unapproved"` and `lawful_analysis_fields_approved is False`; undated/fictional/synthetic-manifest approvals emit `owner_approval_status == "pending_owner_approval"`, `lawful_analysis_fields_approved is False`, and `live_activation_allowed is False`; only non-synthetic manifests with bound valid thresholds, non-empty lawful analysis fields, three real named human owners, and a valid approval date/unexpired window emit `owner_approval_status == "approved"` and `lawful_analysis_fields_approved is True`.
* FR-2: `cohort_eval.evaluate(..., live=True)` and `cohort_eval.export_record(...)` fail closed on synthetic inputs, fictional/placeholder/non-human owners, missing/malformed approval dates, expired approvals, invalid lawful analysis fields, or tampered provenance/digest fields.
  * Observable acceptance criteria: `live=True` adds explicit blocker codes (`constructed_thresholds_live`, `live_approval_not_named_human`, `live_approval_undated`, `live_approval_expired`, `unapproved_lawful_analysis_fields`) and forces `activation_allowed is False` and `live_activation_allowed is False`; `export_record(...)` raises `ValueError` on tampered `record_hash`, `synthetic_not_fairness_evidence != True`, or inconsistent live/fairness claims.
* FR-3: Runtime/API payloads (`ai_eval.cohort_report()`, `GET /api/ai/report`, and manager-only `GET /api/ai/cohort-evaluation`) and CLI `--json` exports surface the enforced `OQ-018` approval status and non-fairness provenance notice for both deterministic ranking and AI priority cohort runs.
  * Observable acceptance criteria: Manager `GET /api/ai/report` and `GET /api/ai/cohort-evaluation` return HTTP 200 with `owner_approval_status == "unapproved"`, `lawful_analysis_fields_approved is False`, `synthetic_not_fairness_evidence is True`, non-empty `non_fairness_provenance_notice` citing `OQ-018`, `fairness_evidence is False`, and `live_activation_allowed is False`; non-manager roles receive HTTP 403.

## Non-Functional Requirements

* NFR-1: Static type safety and lint/format cleanliness in all touched packages.
  * Objective threshold or evaluation condition: Zero errors from `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/core`, `src/agents`, and `src/api`.
  * Operating condition or verification approach: Run directly inside each modified package directory using worktree-local sources.
  * Observable acceptance criteria: All three commands exit 0 in each modified package directory.
* NFR-2: Deterministic canonical hashing and full regression preservation.
  * Objective threshold or evaluation condition: Identical inputs produce identical SHA-256 `record_hash`, and 100% of targeted core, agents, and API test modules pass under worktree-isolated `PYTHONPATH`.
  * Operating condition or verification approach: Focused `unittest` suites covering `cohort_eval`, `rai_threshold_live_approval_guard`, `cohort_ranking_eval`, `cohort_ai_eval`, `ai_eval`, `ai_tasks`, and `role_endpoint_inventory`.
  * Observable acceptance criteria: Zero test failures or errors across all targeted suites.

## Acceptance Criteria

* AC-1: Paired constructed cohorts differing in sensor completeness, source completeness, accessibility/contact (`support_need`), and appointment history evaluate deterministically against expected-outcome manifests, detecting all seeded unjustified exclusion and deprioritisation defects.
* AC-2: Per-cohort denominators (`n`, `missing`, `excluded`), errors, review burden, and Wilson 95% intervals reconcile across all dimensions; small or empty samples remain `sufficient: False`; threshold breaches block activation pending human disposition without subgroup averaging.
* AC-3: `cohort_eval.evaluate(...)`, `cohort_eval.export_record(...)`, `ai_eval.cohort_report()`, `GET /api/ai/report`, and `GET /api/ai/cohort-evaluation` expose and enforce `owner_approval_status`, `lawful_analysis_fields_approved: bool`, `live_activation_allowed: bool`, `synthetic_not_fairness_evidence: True`, and `non_fairness_provenance_notice` citing `OQ-018`.
* AC-4: Synthetic runs cannot claim `fairness_evidence: True`, `owner_approval_status: "approved"`, `lawful_analysis_fields_approved: True`, or activate live prioritisation (`live_activation_allowed: False`, `evaluate(..., live=True)["activation_allowed"] == False`); undated/fictional/unapproved runs never claim `owner_approval_status: "approved"`, `lawful_analysis_fields_approved: True`, or `live_activation_allowed: True`, and never claim `fairness_evidence: True` when `live=True` or when `lawful_analysis_fields` are invalid (preserving offline `live=False` measurement-fixture compatibility at `test_cohort_eval.py:246`).
* AC-5: Focused validation (`mypy`, `ruff check`, `ruff format --check`, and focused unit/API tests) passes in `src/core`, `src/agents`, and `src/api`, with documentation and `.copilot-tracking/` artifacts committed locally with `Refs #222` (no push).

## Test Ownership, Targets, and Coverage Lock

* Canonical source targets (no generated code targets):
  * `src/core/src/zava_forward/core/cohort_eval.py`
  * `src/agents/src/zava_forward/agents/ai_eval.py`
  * `src/agents/src/zava_forward/agents/cohort_ranking_eval.py`
  * `src/agents/src/zava_forward/agents/cohort_ai_eval.py`
  * `src/api/src/zava_forward/api/server.py`
* Documentation targets:
  * `src/core/README.md`, `src/agents/README.md`, `src/api/README.md`
* Test ownership and budgets:
  * `src/core/tests/test_cohort_eval.py` and `src/core/tests/test_rai_threshold_live_approval_guard.py`: semantic invariants for `owner_approval_status`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, `non_fairness_provenance_notice`, fictional-token rejection, ISO/epoch date validation, `export_record` tamper rejection, and paired/defect/reconciliation/subgroup-blocking regression checks. Exact removals: `none`. Maximum new test methods across core tests: `8`.
  * `src/agents/tests/test_ai_eval.py`, `src/agents/tests/test_cohort_ranking_eval.py`, and `src/agents/tests/test_cohort_ai_eval.py`: propagation and CLI JSON export verification for ranking and AI priority cohort records. Exact removals: `none`. Maximum new test methods across agents tests: `4`.
  * `src/api/tests/test_ai_tasks.py` and `src/api/tests/test_role_endpoint_inventory.py`: HTTP API payload/export verification on `GET /api/ai/report` and `GET /api/ai/cohort-evaluation` plus role-matrix inventory registration (`"/api/ai/cohort-evaluation"` in `GET_ENDPOINTS` and contractor denial list). Exact removals: `none`. Maximum new test methods across API tests: `3` (plus string entry in `GET_ENDPOINTS`).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md                                                                    |
| Phase details                    | .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md                                                         |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/issue-222-cohort-eval-2330-plan-critique.md with Revise disposition (PC-001..PC-003 resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-14/issue-222-cohort-eval-2330-research.md                                                             |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/issue-222-cohort-eval-2330-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for `rpi-implement`                                                                                                   |
| Continuation context             | Confirmed automatic RPI Agent parent continues to `Implement`                                                                            |

## Sources

* `.copilot-tracking/research/2026-11-14/issue-222-cohort-eval-2330-research.md`: Codebase evidence `C1`-`C17`, contrarian compatibility analysis, and convergence architecture.
* `docs/reference/research/evaluation/cohort-evaluation-review-pack.md`: `OQ-018` governance boundary and synthetic non-fairness rule.
* `src/core/src/zava_forward/core/cohort_eval.py`, `src/agents/src/zava_forward/agents/ai_eval.py`, `src/api/src/zava_forward/api/server.py`: Canonical implementation modules.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Cohort Evaluation `OQ-018` Boundary and Export Contract

* Intent: Enforce dated real-human owner approval, lawful-field approval, live activation gating, synthetic non-fairness provenance, and tamper-checked record export in `zava_forward.core.cohort_eval`.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `owner_approval_status`, `lawful_analysis_fields_approved`, non-fairness provenance, and `export_record` in `cohort_eval.py`

* Requirement and evidence: FR-1, FR-2, AC-1, AC-2, AC-3, AC-4 (`C1`-`C4`, `C13`, `C16`, `C17`)
* Expected result: `cohort_eval.evaluate(...)` and `cohort_eval.export_record(...)` expose and enforce all `OQ-018` approval and synthetic non-fairness fields fail-closed while preserving existing offline/live mechanics.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Add focused core unit tests for `OQ-018` approval states, fictional/undated/synthetic rejection, and export tamper checks

* Requirement and evidence: FR-1, FR-2, NFR-1, NFR-2, AC-1..AC-4 (`C13`, `C17`)
* Expected result: Focused tests in `src/core/tests/test_cohort_eval.py` and `src/core/tests/test_rai_threshold_live_approval_guard.py` verify every approval state, blocker code, export check, and Issue #222 invariant.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Agents Harness Propagation and HTTP API Runtime/Export Surfaces

* Intent: Surface enforced `OQ-018` approval status and non-fairness provenance across `agents` cohort reports/CLI exports and `api` HTTP endpoints (`GET /api/ai/report` and `GET /api/ai/cohort-evaluation`).
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Propagate `OQ-018` fields and `export_record` in `ai_eval.py`, `cohort_ranking_eval.py`, and `cohort_ai_eval.py` with tests

* Requirement and evidence: FR-3, NFR-1, NFR-2, AC-3, AC-4 (`C6`, `C7`, `C8`, `C14`, `C15`)
* Expected result: `ai_eval.cohort_report()` and CLI `--json` exports include `owner_approval_status`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, `non_fairness_provenance_notice`, and `ai_eval.cohort_evaluation_export()` bundles verified deterministic-ranking and AI-priority cohort records.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Expose `OQ-018` cohort fields on `GET /api/ai/report` (`evaluation.cohorts`) and manager-only `GET /api/ai/cohort-evaluation` in `server.py` with API and role-inventory tests

* Requirement and evidence: FR-3, NFR-1, NFR-2, AC-3, AC-4 (`C9`, `C10`)
* Expected result: Manager HTTP requests receive verified `cohort_eval.export_record(...)` payloads for deterministic ranking and AI priority tasks with `OQ-018` non-fairness enforcement; non-managers receive 403; `test_role_endpoint_inventory.py` covers the new route.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md

<!-- rpi:phase id=P03 -->
### [x] P03: Documentation Sync, Focused Validation, and Local Commit Prep

* Intent: Update directly coupled component READMEs and verify clean Focused validation across `src/core`, `src/agents`, and `src/api`.
* Dependencies: P01, P02

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Update `src/core/README.md`, `src/agents/README.md`, and `src/api/README.md` and run Focused validation (`mypy`, `ruff`, unit/API tests)

* Requirement and evidence: NFR-1, NFR-2, AC-5 (user prompt; repository instructions)
* Expected result: Documentation accurately describes the `OQ-018` fields and `/api/ai/cohort-evaluation` export; `mypy`, `ruff check`, `ruff format --check`, and focused unit/API test suites exit 0 under worktree-isolated `PYTHONPATH`.
* Detail section: P03-T01 in .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md

## Dependencies

* Worktree-local `PYTHONPATH` isolation (`src:tests` in `core`; `../core/src:src:tests:../core/tests` in `agents`; `../core/src:../agents/src:src:tests:../core/tests:../agents/tests` in `api`): prevents importing stale modules from `/home/azureuser/source/ama/src/...` without modifying shared user site-packages.
* `src/api/src/zava_forward/api/server.py` (`get_kind`) and `src/api/tests/test_role_endpoint_inventory.py`: requires mapping `"/api/ai/cohort-evaluation": "ai_report"` in `get_kind` and appending `"/api/ai/cohort-evaluation"` to `GET_ENDPOINTS` (and contractor denial list) alongside adding the route in `server.py`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| `PC-001` [High]: `_valid_lawful_fields` fallback key & `manifest_digest` | Resolved | Updated `P01-T01` to derive default `lawful_analysis_fields` from `manifest.get("cohorts")` (matching input manifest schema) and keep `manifest_digest(manifest)` hashing `{k: v for k, v in manifest.items() if k != "approval"}`. |
| `PC-002` [High]: `server.py:get_kind`, `GET_ENDPOINTS`, & `cohort_evaluation_export()` | Resolved | Updated `P02`/`P02-T01`/`P02-T02` and Plan Dependencies to map `"/api/ai/cohort-evaluation": "ai_report"` in `server.py:get_kind`, append string `"/api/ai/cohort-evaluation"` to `GET_ENDPOINTS` in `test_role_endpoint_inventory.py`, and standardize on `ai_eval.cohort_evaluation_export()`. |
| `PC-003` [Medium]: `fairness_evidence`, `live_activation_allowed`, `"pending_owner_approval"`, & undated/expired codes | Resolved | Updated `AC-4` and `P01-T01` so `fairness_evidence` checks `fields_valid` and `(not live or owner_approval_status == "approved")`, `live_activation_allowed` binds `activation_allowed` (`not open_blockers`), `"pending_owner_approval"` requires `_thresholds_approved` + `fields_valid` + `named_human`, and `_live_gaps` cleanly separates `"expires" in approval` (`live_approval_expired`) from missing/invalid `approved_at`/`approved_on` (`live_approval_undated`). |

## Follow-Up Items

* Human owner governance ratification for `OQ-018` (cohorts, lawful analysis fields, and thresholds) plus creation of a custodian-held non-synthetic held-out split before any live reliance (`Refs #222`, owned by Programme Owner, DPO, and RAI Owner).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/issue-222-cohort-eval-2330-changes.md
* Ready phase or task: P01-T01
* Remaining provisional question or blocker: None
