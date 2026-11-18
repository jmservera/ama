<!-- markdownlint-disable-file -->
# RPI Changes: Issue #222 Cohort and Missing-Data Evaluation Record (`OQ-018`)

## Metadata

* Task ID: issue-222-cohort-eval-2330
* Related plan: .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan (`P01`, `P02`, `P03`)
* Completed scope markers: `P01` (`P01-T01`, `P01-T02`), `P02` (`P02-T01`, `P02-T02`), `P03` (`P03-T01`)
* All remaining active-plan markers: None
* Status basis: All three phases (`P01`..`P03`) and five tasks (`P01-T01`..`P03-T01`) implemented and validated at the Focused tier (`mypy`, `ruff check`, `ruff format --check`, and 274 focused unit/API/inventory tests across `src/core`, `src/agents`, and `src/api`).

## Execution Summary

Implemented fail-closed `OQ-018` pre-live dated real-human owner approval enforcement and synthetic non-fairness provenance across `src/core`, `src/agents`, and `src/api`, updated component READMEs, and verified all Focused checks cleanly.

## Completed Work

### P01: Core Cohort Evaluator `OQ-018` Enforcement and Export Guard (`P01-T01`, `P01-T02`)

* `src/core/src/zava_forward/core/cohort_eval.py`:
  * Added `OWNER_APPROVAL_APPROVED` (`"approved"`), `OWNER_APPROVAL_PENDING` (`"pending_owner_approval"`), `OWNER_APPROVAL_UNAPPROVED` (`"unapproved"`), `FICTIONAL_OWNER_TOKENS` (`fictional`, `placeholder`, `mock`, `synthetic`, `example`, `todo`, `tbd`, `unapproved`, `unknown`), and explicit `SYNTHETIC_NON_FAIRNESS_NOTICE` / `NON_SYNTHETIC_UNAPPROVED_NOTICE` / `APPROVED_PROVENANCE_NOTICE` strings referencing `OQ-018`.
  * Added `_valid_lawful_fields(manifest)` validating explicit `lawful_analysis_fields` (requiring exact set equality with declared `cohorts` dimension keys) or deriving declared keys from `manifest.get("cohorts")`, emitting `unapproved_lawful_analysis_fields` (non-disposable measurement blocker) when invalid.
  * Added `_real_human_owner(...)`, `_valid_approval_stamp(...)`, and `_date_key_gaps(...)` validating ISO-8601 date/datetime (`approved_at`/`approved_on`) and epoch (`expires`) approval windows.
  * Computed and hashed `owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence: True`, and `non_fairness_provenance_notice` in `evaluate(...)`.
  * Tightened `_live_gaps(...)` to reject fictional/placeholder owners (`live_approval_not_named_human`), missing/malformed approval dates (`live_approval_undated`), expired approvals (`live_approval_expired`), invalid lawful fields (`unapproved_lawful_analysis_fields`), and synthetic manifests (`constructed_thresholds_live`).
  * Added `export_record(record)` verifying `record_version`, `record_hash`, `synthetic_not_fairness_evidence is True`, non-empty `non_fairness_provenance_notice`, `owner_approval_status` membership, and consistency of `fairness_evidence` and `live_activation_allowed` (rejecting any tampered/forged record with `ValueError`).
* `src/core/tests/test_cohort_eval.py` and `src/core/tests/test_rai_threshold_live_approval_guard.py`:
  * Added 6 focused unit tests verifying unapproved/pending/approved `OQ-018` states, dated real-human approval on synthetic vs non-synthetic manifests, lawful-field binding and post-approval invalidation, fictional-owner rejection on `live=True`, undated/malformed approval-date blocking, and `export_record` tamper rejection.

### P02: Agents Harness Propagation and HTTP API Runtime/Export Surfaces (`P02-T01`, `P02-T02`)

* `src/agents/src/zava_forward/agents/cohort_ranking_eval.py` and `src/agents/src/zava_forward/agents/cohort_ai_eval.py`:
  * Wrapped evaluated records in `cohort_eval.export_record(...)` so programmatic callers and CLI `--json` exports enforce hash/provenance/non-fairness invariants.
* `src/agents/src/zava_forward/agents/ai_eval.py`:
  * Enriched `cohort_report()` with `record_version`, `owner_approval_status`, `lawful_analysis_fields`, `lawful_analysis_fields_approved`, `live_activation_allowed`, `synthetic_not_fairness_evidence`, `non_fairness_provenance_notice`, and `authority_gap`.
  * Added `cohort_evaluation_export()` bundling `export_record`-verified deterministic-ranking (`ranking-policy`) and AI-priority (`ai-priority-recommendation`) cohort records with explicit `OQ-018` status and manual-path notice.
* `src/api/src/zava_forward/api/server.py`:
  * Mapped `"/api/ai/cohort-evaluation": "ai_report"` in `get_kind` and added read-only manager-only `GET /api/ai/cohort-evaluation` (HTTP 403 for non-managers, HTTP 400 on query parameters, HTTP 404 on POST) returning `ai_eval.cohort_evaluation_export()`, while `GET /api/ai/report` surfaces all `OQ-018` fields under `evaluation.cohorts`.
* `src/agents/tests/{test_cohort_ranking_eval,test_cohort_ai_eval,test_ai_eval}.py` and `src/api/tests/{test_ai_tasks,test_role_endpoint_inventory}.py`:
  * Added CLI `--json` export assertions, `cohort_evaluation_export()` assertions, `GET /api/ai/report` + `GET /api/ai/cohort-evaluation` HTTP tests, and registered `"/api/ai/cohort-evaluation"` in `GET_ENDPOINTS` and contractor denial assertions.

### P03: Documentation Sync and Focused Validation (`P03-T01`)

* Updated `src/core/README.md`, `src/agents/README.md`, and `src/api/README.md` (`ms.date: 2026-11-14`) documenting the `OQ-018` fields, `cohort_eval.export_record(...)`, `ai_eval.cohort_evaluation_export()`, and `GET /api/ai/cohort-evaluation`.

## Implementation-Time Plan and Detail Updates

* Local judgment / immediately relevant current-state updates (preserving approved intent; reconciled in `plan.md` and `phase-details.md`):
  1. Kept `ai_eval.cohort_report()` evaluating only deterministic `cohort_ranking_eval.run()` (rather than invoking `cohort_ai_eval.run("faithful")` inside `run_eval()`), because `test_ai_eval.py` fault-injection tests patch `Store.ai_priority` and `Ai.run` to break validation and assert `run_eval()["passed"] is False` rather than raising inside `cohort_ai_eval._group_rows`. Full paired deterministic + AI priority cohort records are exported via `ai_eval.cohort_evaluation_export()`.
  2. Preserved `GET /api/ai/report`'s exact 4-key top-level schema (`{"evaluation", "live", "registry", "consumption"}`) locked by `src/api/tests/test_ai_consumption_api.py:2089`, exposing the new `OQ-018` fields at `evaluation.cohorts` on `GET /api/ai/report` and serving the full `cohort_evaluation_export()` bundle at `GET /api/ai/cohort-evaluation`.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/core` | Passed | 327 files type-checked (0 errors); ruff lint & format clean (274 files formatted) |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_cohort_eval.py tests/test_rai_threshold_live_approval_guard.py tests/test_paired_equity.py -q` | `src/core` | Passed | 69/69 tests passed in 0.113s |
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/agents` | Passed | 66 files type-checked (0 errors); ruff lint & format clean (62 files formatted) |
| `PYTHONPATH=../core/src:src:tests:../core/tests python3 -m unittest tests/test_cohort_ranking_eval.py tests/test_cohort_ai_eval.py tests/test_ai_eval.py tests/test_cohort_manifest_draft.py -q` | `src/agents` | Passed | 56/56 tests passed in 2.067s |
| `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check .` | `src/api` | Passed | 280 files type-checked (0 errors); ruff lint & format clean (196 files formatted) |
| `PYTHONPATH=../core/src:../agents/src:src:tests:../core/tests:../agents/tests python3 -m unittest tests/test_ai_tasks.py tests/test_role_endpoint_inventory.py tests/test_list_export_inventory.py tests/test_ai_consumption_api.py -q` | `src/api` | Passed | 149/149 tests passed |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P02`, `P03`, `P01-T01`..`P03-T01` all `[x]`; `phase-details.md` synchronized)
* Completed-work evidence and handoff prose: Reconciled
* Validation, blockers, remaining work, and follow-up items: Reconciled
* Review readiness: Ready for `rpi-review`

## Blockers

* None

## Remaining Work

* None

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md, `## Follow-Up Items`
* Human owner governance ratification for `OQ-018` (cohorts, lawful analysis fields, and thresholds) plus creation of a custodian-held non-synthetic held-out split before any live reliance (`Refs #222`, owned by Programme Owner, DPO, and RAI Owner).

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: Full plan (`P01`, `P02`, `P03`); all markers `[x]`, none remaining
* Validation coverage: Focused tier complete (`mypy`, `ruff check`, `ruff format --check`, and 274 focused unit/API/inventory tests across `src/core`, `src/agents`, and `src/api`)
* Blockers: None
* Current plan and detail updates: Reconciled two local-judgment compatibility preserves (`ai_eval.cohort_report()` fault-injection isolation and `GET /api/ai/report` 4-key contract)
* Planning and critique state: Ready (`PC-001`..`PC-003` resolved)
* Follow-up items: Human governance ratification of `OQ-018` (`Refs #222`)
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: Confirmed automatic RPI Agent parent
