<!-- markdownlint-disable-file -->
# Review: Issue 98 Deterministic Approved-Rule Validation, Version-Linked Review Pack, and Stale Propagation

## Scope and Evidence

* Task ID: issue-98-field-validation-2142
* Review date: 2026-11-14
* Review scope: full task (`P01`, `P02`)
* Assessed boundary: `src/core` deterministic approved-rule and reviewer-confirmed-input validation (`validate`), version-linked review pack assembly (`review_pack`), exact dependent-only staleness propagation (`pack_freshness`), dual-store (`Store`, `SqlStore`) behavioral tests (`test_issue_98_field_validation.py`), component guide (`src/core/README.md`), and local `mypy`/`ruff`/`unittest` verification while preserving open `FD-01` to `FD-14` human authority boundaries.
* Plan: .copilot-tracking/plans/2026-11-14/issue-98-field-validation-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-98-field-validation-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/issue-98-field-validation-2142-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/issue-98-field-validation-2142-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/issue-98-field-validation-2142-research.md; `src/core/src/zava_forward/core/form_validation.py`; `src/core/tests/test_issue_98_field_validation.py`; `src/core/README.md`

## Opening Review State

* Interpreted review goal: Verify that the completed `P01` and `P02` implementation satisfies all planned functional requirements (`FR-1` through `FR-4`), non-functional requirements (`NFR-1`, `NFR-2`), acceptance criteria (`AC-1` through `AC-6`), and critique dispositions (`PC-001` through `PC-003`) without defects or unauthorized scope expansion.
* Review scope: full task (`P01`, `P02`)
* Evidence readiness: Ready; plan, phase details, one-pass plan critique, reconciled changes record, research synthesis, and verification outputs are all present and synchronized.
* Acceptance basis: `FR-1`–`FR-4`, `NFR-1`–`NFR-2`, `AC-1`–`AC-6`, `PC-001`–`PC-003` dispositions, and Zava North Homes human-authority constraints (`FD-01`–`FD-14`).
* First comparison boundary: Plan-to-change marker reconciliation and code-level verification of `form_validation.py` against `FR-1`–`FR-4` and `PC-001`–`PC-003`.
* Active read-only boundaries: Read-only comparison across repository sources and tracking artifacts; write authority restricted solely to `.copilot-tracking/reviews/logs/2026-11-14/issue-98-field-validation-2142-review.md`.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass post-implementation comparison on 2026-11-14 across `.copilot-tracking/plans/2026-11-14/issue-98-field-validation-2142-plan.md`, `.copilot-tracking/details/2026-11-14/issue-98-field-validation-2142-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-14/issue-98-field-validation-2142-plan-critique.md`, `.copilot-tracking/changes/2026-11-14/issue-98-field-validation-2142-changes.md`, `.copilot-tracking/research/2026-11-14/issue-98-field-validation-2142-research.md`, and workspace diffs for `src/core/src/zava_forward/core/form_validation.py`, `src/core/tests/test_issue_98_field_validation.py`, and `src/core/README.md`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01` / `P01-T01` | Deterministic Approved-Rule Validation and Pack Freshness Engine (`P01`, `P01-T01`) | Reconciled | Checklist markers `[x]`, phase details, and `form_validation.py` match `FR-1` through `FR-4`, `NFR-1`, `NFR-2`, and `PC-001` through `PC-003`. |
| `P01` / `P01-T02` | Dual-Store Behavioral Unit Test Suite (`P01`, `P01-T02`) | Reconciled | Checklist markers `[x]`, 12 dual-store behavioral test methods (within `<= 16` cap, `0` removals), and local `sys.path` worktree judgment are recorded and verified. |
| `P02` / `P02-T01` | Component Guide Documentation and Local Gate Verification (`P02`, `P02-T01`, `P02-T02`) | Reconciled | Checklist markers `[x]` and `src/core/README.md` additions/reconciliations match `AC-6` and `PC-003` with plain ASCII and zero `.copilot-tracking/` references. |
| `P02` / `P02-T02` | Component Guide Documentation and Local Gate Verification (`P02`, `P02-T01`, `P02-T02`) | Reconciled | Exact caller `mypy`/`ruff`/`unittest` gate and 75-test `test_form*.py` regression pass recorded in `Validation Record`. |
| `Follow-Up Items` | Follow-Up Items (`FD-01`–`FD-14` human authority; future `src/api` exposure) | Reconciled | Preserved outside active `P01`/`P02` completion claims in both plan and changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/form_validation.py` | Implemented `validate`, `review_pack`, and `pack_freshness` with fail-closed schema/source-policy/funding/`rule_refs`/rule-set approval gates, registered-reviewer provenance confirmation, closed-vocabulary `Decimal`-exact rules (`min`, `max`, `max_length`, `pattern`, `equals`, `one_of`, `sum`), `Fail > Conflict > Unknown > Pass` precedence, single-pass `_report` version-linked `fields`/`evidence`/`attachments`/`history` assembly, `DocumentUnavailable` containment, and transitive `required_when`/`sum` stale propagation. | Complete module (`PACK_BODY_KEYS`, `_check_rules`, `_approval_gaps`, `_provenance_confirmed`, `validate`, `review_pack`, `pack_freshness`) verified against `FR-1`–`FR-4`. | Passed `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/core`. | Reconciled |
| `P01-T02` | `src/core/tests/test_issue_98_field_validation.py` | Added 12 dual-store (`Store` and `SqlStore`) behavioral tests covering `AC-1` through `AC-5`, single-read document hashing, `Invalid` tamper/cross-case guards, `Unavailable` quarantined-document/missing-draft handling, Pass-preserving rule-parameter tightening, and authorization boundaries. | Test module present with 12 `test_*` methods (`<= 16` bound, `0` test removals) and zero `pyproject.toml` changes. | Passed `python3 -m unittest discover -s tests -p 'test_*98*.py' -v` (`12` tests OK) and `test_form*.py` (`75` tests OK). | Reconciled |
| `P02-T01` | `src/core/README.md` | Documented `form_validation.validate`, `review_pack`, and `pack_freshness`, reconciled earlier statements on approved rule evaluation versus external `FD-01`–`FD-14` authority gates, and updated the local test command example. | Clean diff in `src/core/README.md` using plain ASCII and zero `.copilot-tracking/` references. | Passed diff inspection and `tools/test_epic_legacy_path_retirement.py` (`5` tests OK). | Reconciled |
| `P02-T02` | `.copilot-tracking/changes/2026-11-14/issue-98-field-validation-2142-changes.md`, `.copilot-tracking/plans/2026-11-14/issue-98-field-validation-2142-plan.md` | Executed the exact caller verification gate plus form regression tests and reconciled all plan checklist markers and changes evidence. | Recorded passing outputs in `Validation Record` and checked `[x]` markers for `P01` and `P02`. | Passed all static, unit, and regression checks with exit code `0`. | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T02` (`src/core/tests/test_issue_98_field_validation.py`) | Prepended worktree `src/core/src` to `sys.path` before `zava_forward` imports (`# noqa: E402`) as ordinary local judgment so bare `python3 -m unittest discover -s tests -p 'test_*98*.py' -v` imports this worktree's namespace package instead of another checkout's editable site-packages entry without mutating shared host packages. | Runtime observation in multi-worktree host environment; no user decision needed because approved scope, test boundary, and `pyproject.toml` invariance were preserved. | Recorded under `## Implementation-Time Plan and Detail Updates` and `P01-T02` completed-work summary in `.copilot-tracking/changes/2026-11-14/issue-98-field-validation-2142-changes.md`. | Not needed (ordinary local judgment; non-material). | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All three findings from `.copilot-tracking/reviews/plans/2026-11-14/issue-98-field-validation-2142-plan-critique.md` (`PC-001` [High], `PC-002` [High], `PC-003` [Medium]) were resolved in planning before implementation and are verified in code (`validation["results"]` persists `kind`/`param`/`message`, transitive propagation reads `c["field_id"]` on `required_when`, `Stale` guarantees non-empty `reasons`, `form_export._digest` and `DocumentUnavailable`/`Invalid` guards protect `validate`/`review_pack`/`pack_freshness`, `_provenance_confirmed` separates confirmation provenance from blank/wrong-type checks, `HUMAN_ONLY` targets/addends raise `ValueError`, `attachments` carry deterministic `attachment_id`, and `src/core/README.md` reconciles earlier prose).
* Material revisions: None occurred during implementation; no scope, requirement, architectural, or dependency change required returning to `rpi-plan` or repeating critique.
* Dependent-work pause assessment: No early resumption or dependency-order violation occurred; `P01` completed and verified before `P02` finalized documentation and full gate reconciliation.
* Justification assessment: Supported by code inspection and passing dual-store unit and static checks.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Finance and template-owner authority decisions `FD-01` to `FD-14` (`#96`, `#97`, `#98`) | Requires real Zava North Homes Finance, Legal, and template-owner human ratification of templates, source policies, and live funding rules (`src/core/evals/fictional_form_review_pack.json`); cannot be fabricated in code. | Zava North Homes Finance / Legal / template owner to ratify `FD-01`–`FD-14` before approving live schemas or closing `#98`. | Open outside active `src/core` scope; routed as distinct human-governance follow-up (`Refs #98` preserved). |
| Employee API and UI routes for `form_validation.validate`, `review_pack`, and `pack_freshness` | Caller explicitly bounded this delivery to `src/core` locally verifiable criteria. | Future `src/api` / employee workbench story once Finance rule-set persistence and UX workflow are scheduled. | Open outside active `src/core` scope; routed as distinct engineering follow-up item. |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

None inside the assessed `src/core` task boundary (`P01`, `P02`). All functional requirements (`FR-1`–`FR-4`), non-functional requirements (`NFR-1`, `NFR-2`), acceptance criteria (`AC-1`–`AC-6`), and critique dispositions (`PC-001`–`PC-003`) are satisfied with direct static and behavioral test evidence.

## Defects

* None

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | none | No `rpi-implement`, `rpi-plan`, or `rpi-research` rework required for the assessed `src/core` scope. | Zero defects, decision gaps, or evidence gaps in `P01`–`P02`. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* External human governance follow-up (`#98` / `FD-01`–`FD-14`): Named Finance, Legal, and template-owner sign-off remains required outside `src/core` before live approved schemas/rule sets exist or Issue `#98` can be closed (`Refs #98` applies to this branch).
* Downstream `src/api` integration follow-up: Exposing read-only HTTP routes and Finance workbench views over `form_validation.validate`, `review_pack`, and `pack_freshness` once rule-set storage is ratified.

## Blockers and Remaining Work

* Blockers: none for the bounded `src/core` delivery (external human ratification `FD-01`–`FD-14` blocks full Issue `#98` closure, tracked via `Refs #98`).
* Remaining active work: none (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` (309 source files) | Passed | `Success: no issues found in 309 source files` (strict mode, `pyproject.toml` unchanged). |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!`. |
| `python3 -m ruff format --check .` | `src/core` (256 files) | Passed | `256 files already formatted`. |
| `python3 -m unittest discover -s tests -p 'test_*98*.py' -v` | `src/core/tests/test_issue_98_field_validation.py` | Passed | `Ran 12 tests — OK` across both JSON `Store` and SQLite `SqlStore`. |
| `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_form*.py' -q` | `src/core/tests/test_form*.py` | Passed | `Ran 75 tests — OK` across `test_form_staging`, `test_form_review`, `test_form_dependencies`, `test_form_export`, and `test_issue_98_field_validation`. |
| `python3 -m unittest tools/test_epic_legacy_path_retirement.py -q` | Repository legacy-path guard | Passed | `Ran 5 tests — OK`. |
| Hosted GitHub Actions CI | Branch `feat/fin-98-field-validation-2142` | Skipped | Caller explicitly instructed `Do NOT push`; hosted CI runs only after branch publication. |

## Outcome

* Outcome: Conformant
* Outcome rationale: Planned phases `P01` and `P02` executed completely, resolved every `PC-001`–`PC-003` critique disposition, preserved `form_export` and `FD-01`–`FD-14` human-authority invariants, and passed bare `mypy`, `ruff check`, `ruff format --check`, and dual-store `unittest` verification in `src/core` with zero defects.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | Distinct follow-up items (`FD-01`–`FD-14` human sign-off; `src/api` route integration) | Finance/Legal/template owner for `FD-01`–`FD-14`; engineering follow-up task for `src/api` Finance workbench exposure |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused local tier passed in `src/core` (`mypy`, `ruff check .`, `ruff format --check .`, `test_*98*.py` 12 tests, `test_form*.py` 75 tests, `test_epic_legacy_path_retirement.py` 5 tests); hosted CI skipped per caller `Do NOT push` instruction.
* Blockers: none

