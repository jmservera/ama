<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #222 Cohort and Missing-Data Evaluation Record (`OQ-018`)

## Metadata

* Task ID: issue-222-cohort-eval-2330
* Critique date: 2026-11-14
* Plan: .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Issue #222 requires explicit runtime, API, and export enforcement of the `OQ-018` pre-live owner-approval boundary and synthetic non-fairness disclaimer (`owner_approval_status` defaulting to pending/unapproved without dated human owner approval of cohorts, lawful analysis fields, and thresholds; `lawful_analysis_fields_approved: bool`; `synthetic_not_fairness_evidence: True`; and an explicit non-fairness provenance notice), verification of paired constructed cohort comparisons, seeded defect detection, per-cohort count/error/review-burden/uncertainty reconciliation, small/missing sample insufficiency, non-averaged subgroup threshold blocking, Focused-tier validation (`mypy`, `ruff check`, `ruff format --check`, focused unit/API tests), and a local commit with `Refs #222` (no push).
* Research and evidence considered: .copilot-tracking/research/2026-11-14/issue-222-cohort-eval-2330-research.md, .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md, .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md, src/core/src/zava_forward/core/cohort_eval.py, src/core/tests/test_cohort_eval.py, src/core/tests/test_rai_threshold_live_approval_guard.py, src/agents/src/zava_forward/agents/ai_eval.py, src/api/src/zava_forward/api/server.py, src/api/tests/test_role_endpoint_inventory.py.
* Decisions, dependencies, and acceptance criteria considered: `FR-1`..`FR-3`, `NFR-1`..`NFR-2`, `AC-1`..`AC-5`, worktree-isolated `PYTHONPATH` execution (avoiding shared `pip install -e` mutation), `OQ-018` remaining open (`Refs #222`), and backward compatibility with existing offline/live mechanics in `src/core/tests/test_cohort_eval.py` and `src/core/tests/test_rai_threshold_live_approval_guard.py`.
* Assessment boundary: Evaluates plan and phase-detail accuracy, contract completeness, and regression compatibility strictly against the supplied artifacts and six source/test files; modules not supplied for direct read (`projection.py`, `cohort_ranking_eval.py`, `cohort_ai_eval.py`, `test_ai_eval.py`, `test_ai_tasks.py`) are assessed only through supplied research citations and their call sites in `ai_eval.py`, `server.py`, and `test_role_endpoint_inventory.py`.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| FR-1 / AC-3 (core record `OQ-018` fields and hashing) | Partial | Covered in `P01-T01`, except `_valid_lawful_fields` reads `manifest.get("dimensions")` instead of `manifest.get("cohorts")` (`PC-001`) and `"pending_owner_approval"` lacks threshold/owner preconditions (`PC-003`). |
| FR-2 / AC-4 (`live=True` fail-closed guards, `fairness_evidence`, and `export_record`) | Partial | Covered in `P01-T01`, except `fairness_evidence` at `cohort_eval.py:313` is left ungated on live/lawful-field blockers, `live_activation_allowed` references nonexistent `NON_DISPOSITIONABLE`, and undated vs expired live-gap codes conflict (`PC-003`). |
| FR-3 / AC-3 (agents and HTTP API runtime/export propagation) | Partial | Covered in `P02-T01` and `P02-T02`, except `server.py:get_kind` and `test_role_endpoint_inventory.py` instructions do not match actual server role gating and inventory structure (`PC-002`). |
| AC-1 / AC-2 (paired cohorts, seeded defects, reconciliation, insufficiency, subgroup blocking) | Covered | Existing invariants in `cohort_eval.py` (`C3`, `C13`..`C15`) plus planned core, agents, and API regression assertions in `P01-T02`, `P02-T01`, and `P02-T02`. |
| NFR-1 / NFR-2 / AC-5 (Focused validation, worktree `PYTHONPATH`, READMEs, local `Refs #222` commit) | Covered | Explicitly planned across `P01`, `P02`, `P03`, and User Decisions and Requirements without mutating shared site-packages or pushing. |

## Verdict

* Verdict: Revise
* Rationale: Overall architecture, scope, and validation strategy are sound, but three direct code-contract mismatches in `P01-T01` and `P02-T02` (`manifest["cohorts"]` vs `manifest["dimensions"]`, `server.py:get_kind` / `test_role_endpoint_inventory.py` wiring, and `fairness_evidence` / `live_activation_allowed` / `_live_gaps` predicates) would cause immediate test regressions and HTTP 403 denials for managers unless corrected before implementation.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `_valid_lawful_fields` reads `manifest.get("dimensions")` instead of `manifest.get("cohorts")`, breaking existing live manifests

* Related IDs: FR-1, FR-2, AC-3, AC-4, NFR-2, P01, P01-T01, C2, C3, C17
* Evidence: .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md (`P01-T01` Context and Intent step 3); src/core/src/zava_forward/core/cohort_eval.py (lines 51-53, 167, 241, 321); src/core/tests/test_cohort_eval.py (lines 77, 249, 272-280); src/core/tests/test_rai_threshold_live_approval_guard.py (lines 22-27, 40-44)
* Concern: `P01-T01` step 3 derives default `lawful_analysis_fields` from `manifest.get("dimensions")` when `"lawful_analysis_fields"` is omitted, returning `([], False)` otherwise. In `cohort_eval.py`, `"dimensions"` is an output record key (`cohort_eval.py:241, 321`), whereas input manifests declare cohort dimensions under `"cohorts"` (`declared: Mapping[str, Sequence[str]] = manifest.get("cohorts", {})` at `cohort_eval.py:167`; `m["cohorts"]` at `test_cohort_eval.py:77, 249`). Additionally, `P01-T01` Context describes `manifest_digest(manifest)` as hashing six specific keys, whereas `cohort_eval.py:51-53` hashes `{k: v for k, v in manifest.items() if k != "approval"}`, which already binds `"lawful_analysis_fields"` automatically when present alongside `"cases"` and `"cohorts"`.
* Impact: Falling back to `manifest.get("dimensions")` yields `([], False)` for every existing manifest without an explicit `"lawful_analysis_fields"` key, triggering `"unapproved_lawful_analysis_fields"` on `live_manifest()` and breaking `LiveCohortThresholds.test_valid_named_human_approval_is_accepted` (`test_rai_threshold_live_approval_guard.py:40-44`) while emitting empty `lawful_analysis_fields: []` on runtime cohort exports. Narrowing `manifest_digest` to six keys would weaken case-content digest binding.
* Smallest useful change: Update `P01-T01` so `_valid_lawful_fields(manifest)` derives default field names from `manifest.get("cohorts")` (requiring a non-empty `Mapping` with `named` keys) when `"lawful_analysis_fields"` is absent, and state explicitly that `manifest_digest(manifest)` remains `{k: v for k, v in manifest.items() if k != "approval"}`.
* Action owner: Planning parent
* Exact resolving evidence: `P01-T01` in .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md specifies fallback to `manifest.get("cohorts")` and preserves full-manifest `manifest_digest` excluding `"approval"`.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `GET /api/ai/cohort-evaluation` route-kind mapping and role-inventory registration in `P02-T02` cause HTTP 403 for managers and break `test_role_endpoint_inventory.py`

* Related IDs: FR-3, AC-3, AC-5, NFR-2, P02, P02-T01, P02-T02, C9, C10
* Evidence: .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md (Test Ownership, Targets, and Coverage Lock; Dependencies); .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md (`P02`, `P02-T01`, `P02-T02`); src/api/src/zava_forward/api/server.py (lines 265-311, 563-564, 902-932); src/api/tests/test_role_endpoint_inventory.py (lines 17-37, 72-76, 147-150)
* Concern: First, `server.py:563-564` enforces `if not projection.allowed(u, get_kind(url.path)): return self._json(403, ...)` before reaching `/api/ai/...` route handlers (`server.py:902`). `P02-T02` instructs registering `"/api/ai/cohort-evaluation": "ai_cohort_evaluation"` "if applicable" while keeping `projection.py` out of scope. Because `"ai_cohort_evaluation"` and `"unknown"` are not allowed kinds in `projection.allowed(...)`, `server.py:563` will deny `GET /api/ai/cohort-evaluation` with HTTP 403 for all roles including `MANAGER_ROLES` unless `get_kind` maps it to `"ai_report"` (matching `"/api/ai/report": "ai_report"` at `server.py:311`) or dispatches before line 563. Second, the plan and `P02-T02` instruct adding a tuple `("GET", "/api/ai/cohort-evaluation", None, PM_ONLY)` to `src/api/tests/test_role_endpoint_inventory.py`, whereas that file uses a flat `list[str]` `GET_ENDPOINTS` (`lines 17-37`, with no `PM_ONLY` symbol) plus `test_contractor_audit_view_and_export_are_denied` (`lines 147-150`). Third, `P02` and `P02-T01` alternate between `cohort_evaluation_bundle()` and `cohort_evaluation_export()` for the function called by `server.py`.
* Impact: Implementing `P02-T02` as written causes `GET /api/ai/cohort-evaluation` to return HTTP 403 for `Retrofit Programme Manager`, breaks `test_role_endpoint_inventory.py` with `NameError` or type mismatch, and risks `AttributeError` between `ai_eval.py` and `server.py`.
* Smallest useful change: Update .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md and `P02`/`P02-T01`/`P02-T02` in .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md to map `"/api/ai/cohort-evaluation": "ai_report"` in `server.py:get_kind` (retaining the handler's explicit `u["role"] not in MANAGER_ROLES` 403 check), register `"/api/ai/cohort-evaluation"` as a string in `GET_ENDPOINTS` (and `test_contractor_audit_view_and_export_are_denied`) in `src/api/tests/test_role_endpoint_inventory.py`, and use `ai_eval.cohort_evaluation_export()` consistently.
* Action owner: Planning parent
* Exact resolving evidence: Plan Dependencies/Test Ownership and `P02`/`P02-T01`/`P02-T02` in phase details specify `"/api/ai/cohort-evaluation": "ai_report"` in `server.py:get_kind`, string entry `"/api/ai/cohort-evaluation"` in `GET_ENDPOINTS`, and `ai_eval.cohort_evaluation_export()`.
* Decision route: Direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: `P01-T01` omits `fairness_evidence` live/lawful-field gating, misstates `live_activation_allowed` rejection/disposition logic, and conflates undated vs expired approvals

* Related IDs: FR-1, FR-2, AC-3, AC-4, NFR-2, P01, P01-T01, P01-T02, C2, C3, C13, C17
* Evidence: .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md (`FR-1`, `FR-2`, `AC-4`); .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md (`P01-T01` steps 4-8); src/core/src/zava_forward/core/cohort_eval.py (lines 19-20, 92-107, 286-315); src/core/tests/test_cohort_eval.py (lines 241-246, 263-270); src/core/tests/test_rai_threshold_live_approval_guard.py (lines 54-75)
* Concern: Four coupled logic mismatches appear across `AC-4` and `P01-T01` steps 4-8:
  1. `P01-T01` never updates `fairness_evidence` at `cohort_eval.py:313-315` (`not synthetic and _thresholds_approved(manifest) and not any(b["code"] in MEASUREMENT_BLOCKERS for b in blockers)`), so non-synthetic `live=True` runs blocked by `live_approval_not_named_human`, `live_approval_expired`, `live_approval_undated`, or `unapproved_lawful_analysis_fields` (and offline runs with invalid `lawful_analysis_fields`) still return `fairness_evidence: True`. Meanwhile, `AC-4` broadly states undated/fictional runs can never claim `fairness_evidence: True`, which contradicts `test_cohort_eval.py:241-246` (`live=False` with `m["synthetic"] = False` and undated fictional `approved(m)`) unless `AC-4` preserves that offline measurement-fixture test while `cohort_eval.py:313` gates `fairness_evidence` on `fields_valid` and `(not live or owner_approval_status == OWNER_APPROVAL_APPROVED)`.
  2. `P01-T01` step 7 defines `live_activation_allowed` using a nonexistent `NON_DISPOSITIONABLE` set and `human` without checking `not open_blockers` (`activation_allowed`). In `cohort_eval.py:19, 286-305`, `DISPOSABLE` is an allowlist and `human` is `True` on `"reject"` dispositions (`test_cohort_eval.py:263-270`), so omitting `activation_allowed` (`not open_blockers`) can leave `live_activation_allowed: True` when a human reviewer rejects activation.
  3. `P01-T01` step 5 sets `owner_approval_status = "pending_owner_approval"` for any bound non-empty `approval` mapping without requiring `_thresholds_approved(manifest)` and `fields_valid`, which misclassifies bound manifests with blank/`"unapproved"`/`None` owners (`test_rai_threshold_live_approval_guard.py:54-60`) or invalid thresholds as `"pending_owner_approval"` instead of `"unapproved"`.
  4. `P01-T01` step 6 emits `live_approval_expired` whenever `approved_at`/`approved_on` is absent (preventing truly undated approvals lacking `expires`, `approved_at`, and `approved_on` from ever emitting `live_approval_undated` as required by `FR-2` and `P01`), and skips validating `approved_at`/`approved_on` in `_live_gaps` when `expires` is also present; meanwhile `test_rai_threshold_live_approval_guard.py:67-69` supplies `"expires": None` (key present) and asserts `"live_approval_expired"`.
* Impact: Without tightening these four predicates, `live=True` runs with failed owner approval can emit `fairness_evidence: True`, rejected runs can report `live_activation_allowed: True`, invalid bound approvals report `"pending_owner_approval"`, and either planned `live_approval_undated` tests or existing `live_approval_expired` tests fail.
* Smallest useful change: Update `AC-4` in .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md and `P01-T01` steps 4-8 in .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md so: (a) `fairness_evidence` requires `not synthetic and _thresholds_approved(manifest) and fields_valid and not any(b["code"] in MEASUREMENT_BLOCKERS for b in blockers) and (not live or owner_approval_status == OWNER_APPROVAL_APPROVED)`, with `AC-4` matching `test_cohort_eval.py:246` offline compatibility; (b) `live_activation_allowed = bool(activation_allowed and owner_approval_status == OWNER_APPROVAL_APPROVED and lawful_analysis_fields_approved and not _live_gaps(manifest, now))` derived from `open_blockers`/`DISPOSABLE`; (c) `"pending_owner_approval"` requires `_thresholds_approved(manifest) and fields_valid and all(named_human(approval.get(k)) for k in owners)` and no malformed/expired date key; and (d) `_live_gaps` emits `live_approval_expired` when `"expires" in approval` fails `(now is not None and finite and expires > now)` and emits `live_approval_undated` when `"approved_at"` or `"approved_on"` is present and invalid/future or when none of `("expires", "approved_at", "approved_on")` is in `approval`.
* Action owner: Planning parent
* Exact resolving evidence: `AC-4` in .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md and `P01-T01` steps 4-8 in .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md record these exact predicates.
* Decision route: Direct planner correction

## Strengths and Residual Risk

* Contrarian check on `rai_release.NON_HUMAN_TOKENS` omitting `"fictional"`, `"placeholder"`, `"mock"`, and `"synthetic"` prevents developer fixture strings (`"Data lead (fictional)"`) from ever satisfying dated real-human owner approval or `live=True`.
* Worktree-local `PYTHONPATH` isolation avoids mutating the shared VM's editable site-packages while testing worktree changes across `src/core`, `src/agents`, and `src/api`.
* `cohort_eval.export_record(...)` provides a single tamper-evident enforcement choke point across programmatic runners, CLI `--json` exports, `GET /api/ai/report`, and `GET /api/ai/cohort-evaluation`.
* Residual risk (explicitly accepted by task scope): `OQ-018` human governance approval of production cohorts, lawful analysis fields, and thresholds remains intentionally open (`Refs #222`), so runtime evaluation exports will remain fail-closed (`owner_approval_status: "unapproved"`, `live_activation_allowed: False`) until external owner ratification.

## Questions or Blocking Evidence Gaps

* None. All three findings are direct planner corrections fully resolved by the supplied codebase evidence.

## Limitations

* Direct source verification was bounded to the supplied research, plan, phase details, and six named Python files (`cohort_eval.py`, `test_cohort_eval.py`, `test_rai_threshold_live_approval_guard.py`, `ai_eval.py`, `server.py`, `test_role_endpoint_inventory.py`); `projection.py`, `cohort_ranking_eval.py`, `cohort_ai_eval.py`, `test_ai_eval.py`, and `test_ai_tasks.py` were assessed via their call sites in the supplied files and citations `C6`..`C15` in the research artifact.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: Planning parent
* Smallest next action: Apply direct planner corrections for `PC-001`, `PC-002`, and `PC-003` in .copilot-tracking/plans/2026-11-14/issue-222-cohort-eval-2330-plan.md and .copilot-tracking/details/2026-11-14/issue-222-cohort-eval-2330-phase-details.md, record their disposition in `Critique Disposition`, and finalize the plan for implementation without another critique pass.
* User response required: no
