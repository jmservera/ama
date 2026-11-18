<!-- markdownlint-disable-file -->
# Review: Issue #222 Cohort and Missing-Data Evaluation Record (`OQ-018`)

## Scope and Evidence

* Task ID: issue-222-cohort-eval-2330
* Review date: 2026-11-14
* Review scope: Full task (`P01`, `P02`, `P03`)
* Assessed boundary: Pre-live `OQ-018` human owner approval enforcement (`owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`), synthetic non-fairness provenance (`synthetic_not_fairness_evidence: True`, `non_fairness_provenance_notice`), tamper-evident `cohort_eval.export_record(...)`, runtime/API payload and CLI export propagation (`ai_eval.cohort_report()`, `ai_eval.cohort_evaluation_export()`, `GET /api/ai/report`, `GET /api/ai/cohort-evaluation`), paired-cohort/defect/reconciliation/subgroup-blocking invariants, component documentation, and Focused validation across `src/core`, `src/agents`, and `src/api`.
* Plan: .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/issue-222-cohort-eval-2330-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/issue-222-cohort-eval-2330-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/issue-222-cohort-eval-2330-research.md; exact worktree `git diff` across `src/core`, `src/agents`, and `src/api`; Focused validation output (`mypy`, `ruff check`, `ruff format --check`, and 274 focused unit/API/inventory tests).

## Opening Review State

* Interpreted review goal: Verify once, with read-only source authority, that `P01`..`P03` satisfy all Issue #222 engineering requirements (`FR-1`..`FR-3`, `NFR-1`..`NFR-2`, `AC-1`..`AC-5`), resolved plan-critique findings (`PC-001`..`PC-003`), reconciled implementation-time updates, and Focused validation without introducing defects or claiming human `OQ-018` sign-off.
* Review scope: Full task (`P01`, `P02`, `P03`)
* Evidence readiness: Ready; plan, phase details, single plan critique, changes record, and research artifacts are present and reconciled.
* Acceptance basis: `FR-1`..`FR-3`, `NFR-1`..`NFR-2`, `AC-1`..`AC-5`, critique dispositions `PC-001`..`PC-003`, and repository Focused validation rules.
* First comparison boundary: Compare `src/core/src/zava_forward/core/cohort_eval.py`, `src/agents/src/zava_forward/agents/{ai_eval,cohort_ranking_eval,cohort_ai_eval}.py`, `src/api/src/zava_forward/api/server.py`, tests, and READMEs against `P01`..`P03` and `changes.md`.
* Active read-only boundaries: Write authority restricted exclusively to `.copilot-tracking/reviews/logs/2026-11-14/issue-222-cohort-eval-2330-review.md` (plus RPI Agent session state record).
* Initial blockers: None

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single post-implementation review on 2026-11-14 across all 15 changed files in `src/core`, `src/agents`, and `src/api`, reconciled tracking artifacts (`plan.md`, `phase-details.md`, `plan-critique.md`, `changes.md`, `research.md`), and Focused validation results.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` (`P01-T01`, `P01-T02`) | Core Cohort Evaluator `OQ-018` Enforcement and Export Guard | Reconciled | All `OQ-018` approval states, fictional-owner guards, ISO/epoch date checks, lawful-field checks, and `export_record(...)` tamper guards match plan and details. |
| `P02` (`P02-T01`, `P02-T02`) | Agents Harness Propagation and HTTP API Runtime/Export Surfaces | Reconciled | `cohort_report()`, `cohort_evaluation_export()`, CLI `--json` runners, `GET /api/ai/report` (`evaluation.cohorts`), `GET /api/ai/cohort-evaluation`, and `GET_ENDPOINTS` match reconciled plan and details. |
| `P03` (`P03-T01`) | Documentation Sync and Focused Validation | Reconciled | `src/core/README.md`, `src/agents/README.md`, and `src/api/README.md` updated and Focused validation passed across all 3 packages. |
| `Follow-Up Items` | Human owner governance ratification for `OQ-018` (`Refs #222`) | Reconciled | Preserved outside active `Pxx`/`Pxx-Txx` scope; commit appropriately uses `Refs #222` rather than a closing keyword. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/cohort_eval.py` | Added `OWNER_APPROVAL_*`, `FICTIONAL_OWNER_TOKENS`, `_real_human_owner`, `_valid_lawful_fields`, `_valid_approval_stamp`, `_date_key_gaps`, `owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence: True`, `non_fairness_provenance_notice`, tightened `_live_gaps`, and `export_record(...)`. | Exact diff inspected; hashes all new fields into `record_hash` and fails closed on synthetic/fictional/undated/expired/tampered records. | `src/core` `mypy` (327 files, 0 issues) + `ruff check` + `ruff format --check` Passed. | Reconciled |
| `P01-T02` | `src/core/tests/test_cohort_eval.py`, `src/core/tests/test_rai_threshold_live_approval_guard.py` | Added 6 focused unit tests covering unapproved/pending/approved `OQ-018` states, synthetic vs non-synthetic dated human approval, post-approval lawful-field edit invalidation, invalid lawful-field shapes, fictional-owner rejection on `live=True`, undated/malformed approval dates, and `export_record` forgery/tamper rejection. | Within locked core test budget (6 <= 8 max additions; 0 removals). | 69/69 tests in `test_cohort_eval.py`, `test_rai_threshold_live_approval_guard.py`, and `test_paired_equity.py` Passed. | Reconciled |
| `P02-T01` | `src/agents/src/zava_forward/agents/{ai_eval,cohort_ranking_eval,cohort_ai_eval}.py`, `src/agents/tests/{test_ai_eval,test_cohort_ranking_eval,test_cohort_ai_eval}.py` | Wrapped `cohort_ranking_eval` and `cohort_ai_eval` outputs in `cohort_eval.export_record(...)`, enriched `ai_eval.cohort_report()`, added `ai_eval.cohort_evaluation_export()`, and verified CLI `--json` and harness report invariants. | Within locked agents test budget (0 new methods, extended 3 existing methods <= 4 max; 0 removals). | `src/agents` `mypy` (66 files, 0 issues), `ruff`, and 56/56 focused unit tests Passed. | Reconciled |
| `P02-T02` | `src/api/src/zava_forward/api/server.py`, `src/api/tests/{test_ai_tasks,test_role_endpoint_inventory}.py` | Mapped `"/api/ai/cohort-evaluation": "ai_report"` in `get_kind`, exposed `OQ-018` fields on `GET /api/ai/report` (`evaluation.cohorts`), added read-only manager-only `GET /api/ai/cohort-evaluation`, and updated role-endpoint inventory + HTTP tests. | Within locked API test budget (1 new method + `GET_ENDPOINTS` registration <= 3 max; 0 removals). | `src/api` `mypy` (280 files, 0 issues), `ruff`, and 149/149 API/inventory/consumption tests Passed. | Reconciled |
| `P03-T01` | `src/core/README.md`, `src/agents/README.md`, `src/api/README.md` | Updated frontmatter `ms.date: 2026-11-14` and documented `OQ-018` pre-live enforcement, `export_record`, `cohort_evaluation_export`, and `GET /api/ai/cohort-evaluation`. | Markdown diff verified; no `.copilot-tracking/` references leaked into production code or READMEs. | Complete Focused validation matrix Passed across `src/core`, `src/agents`, and `src/api`. | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P02-T01` (`ai_eval.cohort_report()`) | Kept `cohort_report()` evaluating deterministic `cohort_ranking_eval.run()` only while `cohort_evaluation_export()` bundles both `ranking` and `ai_priority`. | `src/agents/tests/test_ai_eval.py` fault-injection tests patch `Store.ai_priority` and `Ai.run` and assert `run_eval()["passed"] is False` without raising inside `cohort_report()`. Local engineering judgment; no user decision needed. | Updated `plan.md` (`P02-T01`), `phase-details.md` (`P02-T01`), and `changes.md` (`## Implementation-Time Plan and Detail Updates`). | Not needed (preserves approved intent and `PC-002` `cohort_evaluation_export()` contract). | Reconciled |
| `P02-T02` (`GET /api/ai/report`) | Preserved `GET /api/ai/report` top-level keys `{"evaluation", "live", "registry", "consumption"}` (exposing `OQ-018` fields via `evaluation.cohorts`) while `GET /api/ai/cohort-evaluation` serves `cohort_evaluation_export()`. | `src/api/tests/test_ai_consumption_api.py` (`test_manager_report_local_http_and_bad_period`) asserts exact top-level key equality on `/api/ai/report`. Local engineering judgment; no user decision needed. | Updated `plan.md` (`In Scope`, `P02-T02`), `phase-details.md` (`P02`, `P02-T02`), and `changes.md` (`## Implementation-Time Plan and Detail Updates`). | Not needed (preserves approved intent and existing API contract). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All three planner-owned findings (`PC-001`, `PC-002`, `PC-003`) recorded in `plan.md` `## Critique Disposition` were faithfully implemented (`manifest.get("cohorts")` fallback + full non-approval `manifest_digest`; `server.py:get_kind` `"ai_report"` mapping + `GET_ENDPOINTS` registration + `cohort_evaluation_export()`; tightened `fairness_evidence`, `live_activation_allowed`, `pending_owner_approval`, and undated-vs-expired blocker codes).
* Material revisions: None. Both implementation-time adjustments were local compatibility preserves within approved architecture and acceptance criteria.
* Dependent-work pause assessment: No material revision occurred; sequential execution (`P01` -> `P02` -> `P03`) respected all dependencies.
* Justification assessment: Supported by concrete test evidence (`test_ai_eval.py` and `test_ai_consumption_api.py`).

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Human owner governance ratification for `OQ-018` (cohorts, lawful analysis fields, and thresholds) and custodian-held non-synthetic held-out split (`Refs #222`) | Requires named human Programme Owner, DPO, and RAI Owner sign-off plus non-synthetic operational data governance; cannot be fabricated in code. | Programme Owner, DPO, and RAI Owner review `docs/reference/research/evaluation/cohort-evaluation-review-pack.md` and ratify `OQ-018`. | Open external governance prerequisite; routed as distinct follow-up (`Refs #222`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Low]: Clarify `lawful_analysis_fields` parenthetical in `src/core/README.md` when `OQ-018` field mapping is ratified

* Related scope: `P03-T01`
* Evidence: `src/core/README.md` states `lawful analysis fields (exact-set matched to the manifest dimensions)` whereas `src/core/src/zava_forward/core/cohort_eval.py` (`_valid_lawful_fields`) implements the `phase-details.md` `P01-T01` rule: an explicit `lawful_analysis_fields` sequence may name underlying case fields (any non-empty sequence of named strings, cryptographically bound via `manifest_digest`), defaulting to `manifest["cohorts"]` dimension keys only when omitted.
* Impact: Non-blocking documentation nuance; runtime safety and digest binding are unaffected because any unapproved or post-approval-edited `lawful_analysis_fields` fails closed.
* Destination: `follow-up`
* Smallest useful next action: Align the parenthetical in `src/core/README.md` (or add an explicit dimension-to-source-field mapping check if DPO `OQ-018` ratification requires 1-to-1 dimension binding) in a future follow-up pass.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| `RV-001` [Low] | `follow-up` | Engineering / DPO follow-up alongside `OQ-018` schema ratification | Non-blocking documentation wording nuance; code matches `P01-T01` specification and all `FR-1`..`FR-3` / `AC-1`..`AC-5` invariants pass. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `RV-001` [Low]: Align the parenthetical description of `lawful_analysis_fields` in `src/core/README.md` (or add a dimension-to-field mapping constraint once DPO `OQ-018` sign-off defines the production schema).
* External human governance follow-up (`Refs #222`): Named Programme Owner, DPO, and RAI Owner approval of production cohorts, lawful analysis fields, and thresholds (`OQ-018`) plus custodian-held non-synthetic evaluation data before live activation.

## Blockers and Remaining Work

* Blockers: None for the engineering scope of this task (external human `OQ-018` approval remains an intentional live-activation gate on Issue #222, tracked via `Refs #222`).
* Remaining active work: None (`P01`, `P02`, and `P03` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` | Passed | 327 source files checked with 0 issues; ruff lint and format checks clean (274 files formatted). |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_cohort_eval.py tests/test_rai_threshold_live_approval_guard.py tests/test_paired_equity.py -q` | `src/core` | Passed | 69/69 unit tests passed (0.113s). |
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/agents` | Passed | 66 source files checked with 0 issues; ruff lint and format checks clean (62 files formatted). |
| `PYTHONPATH=../core/src:src:tests:../core/tests python3 -m unittest tests/test_cohort_ranking_eval.py tests/test_cohort_ai_eval.py tests/test_ai_eval.py tests/test_cohort_manifest_draft.py -q` | `src/agents` | Passed | 56/56 unit tests passed (2.067s). |
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` | Passed | 280 source files checked with 0 issues; ruff lint and format checks clean (196 files formatted). |
| `PYTHONPATH=../core/src:../agents/src:src:tests:../core/tests:../agents/tests python3 -m unittest tests/test_ai_tasks.py tests/test_role_endpoint_inventory.py tests/test_list_export_inventory.py tests/test_ai_consumption_api.py -q` | `src/api` | Passed | 149/149 HTTP API, role-matrix endpoint inventory, export inventory, and consumption report tests passed. |

## Outcome

* Outcome: Conformant
* Outcome rationale: All planned phases (`P01`, `P02`, `P03`), functional requirements (`FR-1`..`FR-3`), non-functional requirements (`NFR-1`..`NFR-2`), acceptance criteria (`AC-1`..`AC-5`), and plan-critique dispositions (`PC-001`..`PC-003`) are implemented, reconciled, and proven by Focused static and runtime validation (274 passing tests, zero `mypy`/`ruff` findings). No material defects or unresolved engineering decision gaps exist; `RV-001` [Low] and external `OQ-018` human governance ratification are non-blocking follow-up items.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | `RV-001` (`src/core/README.md` parenthetical / optional `OQ-018` field-map check) + Programme Owner / DPO / RAI Owner ratification of `OQ-018` (`Refs #222`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier complete (`mypy`, `ruff check`, `ruff format --check`, and 274 unit/API/inventory tests across `src/core`, `src/agents`, and `src/api`)
* Blockers: None

