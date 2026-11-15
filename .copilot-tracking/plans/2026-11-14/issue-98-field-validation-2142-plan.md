<!-- markdownlint-disable-file -->
# RPI Plan: Issue 98 Deterministic Approved-Rule Validation, Version-Linked Review Pack, and Stale Propagation

## Task Metadata

* Task ID: issue-98-field-validation-2142
* Task slug: issue-98-field-validation-2142
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/issue-98-field-validation-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/issue-98-field-validation-2142-plan-critique.md

## Executive Summary

This plan delivers the remaining locally verifiable engineering mechanics for GitHub Issue #98 in `src/core` without fabricating external Finance or template-owner approvals (`FD-01` to `FD-14`). It completes `src/core/src/zava_forward/core/form_validation.py` with three deterministic operations — `validate`, `review_pack`, and `pack_freshness` — paired with JSON and SQLite tests in `src/core/tests/test_issue_98_field_validation.py` and updated component documentation in `src/core/README.md`.

First, **approved-rule and reviewer-confirmed-only validation** ensures rules run only when both the registered schema/source-policy record and the supplied rule set carry recorded approval metadata, an evidenced funding route (for funding forms), matching `schema_digest` and `template_version`, and a declared `(id, version)` entry in `schema["rule_refs"]`. Even when rules are approved, each rule and deterministic `sum` calculation evaluates strictly against current (`Accepted` or `Corrected`), schema-valid, nonblank values confirmed in audit history by a registered human reviewer with intact source evidence; staged unreviewed candidates, rejected fields, stale fields, and tampered draft entries never enter rule evaluation. Second, **version-linked review-pack assembly and exact stale propagation** connect every field, deduplicated evidence link, attachment, and history event with explicit `template_version` and `input_version` metadata under a canonical `content_sha256` digest, and compute the exact `stale_fields` versus `unaffected_fields` set when any bound source, schema field, approved rule, or confirmed input changes.

### User Decisions and Requirements Highlights

* **Bounded `src/core` delivery on `feat/fin-98-field-validation-2142`**: Implement the remaining locally verifiable Issue #98 acceptance criteria inside `src/core`, preserving `form_export` compatibility with `src/api` and leaving remote state untouched (no `git push`).
* **Strict bare `mypy`, `ruff`, and `test_*98*.py` verification**: Pass `python3 -m mypy`, `python3 -m ruff check .`, `python3 -m ruff format --check .`, and `python3 -m unittest discover -s tests -p 'test_*98*.py' -v` from `src/core` without modifying `pyproject.toml`.
* **Complete RPI tracking and clean local commit**: Persist all four `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`) under `issue-98-field-validation-2142` and commit cleanly with the Copilot trailer and `Refs #98` so `git status --short` is empty.

### What You May Not Know

* **Pre-existing untracked draft had 7 contrarian defects**: Our research audit of untracked `src/core/src/zava_forward/core/form_validation.py` found 3 strict `mypy` `no-any-return` errors plus missing `schema["rule_refs"]` and funding-route checks, missing `enum`/`boolean`/`date` and `sum` calculation rule kinds, `open_issues` status-precedence masking (`Fail`/`Conflict` downgraded to `Unknown`), pack-wide instead of per-evidence `input_version` stamping, double document hashing across `draft_export` + `_validate`, and no `pack_freshness` function for rule-level stale propagation. All 7 are addressed in Phase `P01`.
* **Human Finance authority remains intentionally unresolved**: `forms.register_schema` continues to register schemas as `Unapproved`, and assembled review packs always remain `reviewed=False`, `submission="Not submitted"`, and `eligibility="Not assessed"`. Commits must therefore use `Refs #98` rather than a closing keyword.

### Unresolved Decisions or Blockers

* External governance item (non-blocking for `src/core`): Finance and template-owner sign-off on `FD-01` to `FD-14` (`src/core/evals/fictional_form_review_pack.json`) remains owned by Finance and Legal before live approved schemas exist or Issue #98 can be closed.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) for Issue #98 (Field review, deterministic validation and stale propagation) on branch `feat/fin-98-field-validation-2142` in worktree `/home/azureuser/source/ama-demo-wt/feat-98-field-validation-2142` (caller prompt).
* Deliver in `src/core`: validation uses approved rules and reviewer-confirmed inputs only (caller prompt; Issue #98; PRD `FR-041`, `AC-049`).
* Deliver in `src/core`: pack links fields, evidence, and attachments with template and input versions, propagating exact staleness on source, schema, rule, or input change (caller prompt; Issue #98; PRD `FR-042`, `FR-043`, `AC-050`, `AC-051`, `AC-054`).
* Write all 4 `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`) without overwriting prior committed #1705 artifacts (caller prompt; `.copilot-tracking/research/2026-11-14/issue-98-field-validation-2142-research.md`).
* Verify in `src/core` using exact command `cd /home/azureuser/source/ama-demo-wt/feat-98-field-validation-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*98*.py' -v` (caller prompt).
* Commit cleanly using repository-local privacy-safe GitHub noreply email, `Refs #98`, and `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push (`git status --short` must be empty) (caller prompt; repository instructions).

## Goals

* Enforce fail-closed deterministic rule and calculation validation in `src/core` so unapproved/unbound rules and unconfirmed, staged, rejected, stale, blank, or tampered field inputs are never evaluated.
* Assemble tamper-evident, version-linked Finance review packs in `src/core` connecting fields, deduplicated source evidence, attachments, review history, and validation diagnostics with explicit `template_version` and `input_version`.
* Compute exact dependent-only field staleness (`pack_freshness`) across document byte/version changes, schema revisions, approved-rule updates, and reviewer input changes across both JSON `Store` and SQLite `SqlStore`.
* Prove strict type safety, lint/format cleanliness, behavioral coverage (`test_*98*.py`), and backward compatibility with existing `forms`, `form_review`, and `form_export` suites.

## Scope and Non-Goals

### In Scope

* Completing and hardening `src/core/src/zava_forward/core/form_validation.py` (`validate`, `review_pack`, `pack_freshness`, closed-vocabulary deterministic rules including `sum` bound to `calculation_ref`).
* Creating `src/core/tests/test_issue_98_field_validation.py` running against both in-memory/JSON `Store` and SQLite `SqlStore`.
* Updating `src/core/README.md` to document `form_validation` APIs, invariants, and open human-approval boundaries.
* Producing the dated `.copilot-tracking/` research, plan, phase-details, plan-critique, changes, and review artifacts for `issue-98-field-validation-2142` and creating one clean local commit on `feat/fin-98-field-validation-2142`.

### Non-Goals

* Fabricating Finance, Board, Legal, or template-owner sign-off (`FD-01` to `FD-14`) or adding a runtime `approve_schema` / `approve_rules` endpoint.
* Changing `form_export.draft_export` `BODY_KEYS` or `src/api` HTTP endpoints.
* Modifying `src/core/pyproject.toml`, `infra/`, or private datasets, or pushing commits to `origin`.

## Functional Requirements

* FR-1: Fail-closed authority and binding check before rule evaluation (`FR-038`, `FR-041`, `AC-046`, `AC-049`).
  * Observable acceptance criteria: `form_validation.validate` returns `status="Not evaluated"`, `results=[]`, and explicit `reasons` whenever the registered schema row lacks `approval == "Approved"`, nonblank `approval_evidence`, `source_policy_status == "Approved"`, matching `digest == draft["schema_digest"]`, or `funding["status"] == "Evidenced"` (for `form_type == "funding"`), or whenever `rules` lacks `approval == {"status": "Approved", "approver": <nonblank>, "evidence_ref": <nonblank>}`, exact `bound` (`schema_id`, `schema_version`, `schema_digest`, `template_id`, `template_version`), or a matching `(id, version)` entry in `schema["rule_refs"]`.
* FR-2: Deterministic closed-vocabulary rule and calculation evaluation on reviewer-confirmed inputs only (`FR-040`, `FR-041`, `AC-049`).
  * Observable acceptance criteria: `validate` evaluates closed-vocabulary rules (`min`, `max`, `max_length`, `pattern`, `equals`, `one_of`, and `sum` bound to `field["calculation_ref"]` using exact `Decimal` arithmetic) exclusively against fields whose `effective_state` is `Accepted` or `Corrected`, whose value satisfies schema type constraints and is nonblank, and whose latest field audit event has a matching decision, registered nonblank human `reviewer`, matching value, and intact non-None `evidence`. Staged candidates, rejected fields, stale fields, and tampered draft entries never enter `confirmed`; rules targeting unconfirmed fields report `status="Unknown"` without reading unconfirmed values; overall validation status aggregates rule outcomes and remaining `open_issues` with precedence `Fail > Conflict > Unknown > Pass` (clearing `_report`'s generic `"Approved calculation is unavailable."` placeholder only for fields covered by an approved `sum` rule).
* FR-3: Version-linked Finance review-pack assembly without submission or eligibility claims (`FR-042`, `AC-050`, `AC-054`).
  * Observable acceptance criteria: `form_validation.review_pack` performs a single `_report` pass per call (returning controlled `status="Unavailable"` on missing/quarantined evidence via `DocumentUnavailable`) and returns a deterministic pack (`content_sha256` via `form_export._digest`) containing `draft_id`, `input_version`, `template`, `template_version`, `schema_id`, `schema_version`, `schema_digest`, `rule_refs`, `fields` (each with `field_id`, `value`, `state`, `source_id`, `source_version`, `document_hash`, `locator`, `template_version`, and per-field `input_version`), deduplicated `evidence` (each with `source_id`, `source_version`, `document_hash`, `attachment_id`, `field_ids`, `locators`, `template_version`, and `input_version` equal to the max `input_version` of its bound fields), `attachments` (each stamped with deterministic `attachment_id`, `template_version`, and `input_version`), `history`, `validation` (persisting `kind`, `param`, and `message` on each rule result), and `stale_fields`, while always preserving `reviewed=False`, `submission="Not submitted"`, `eligibility="Not assessed"`, and `pack_status="Ready for Finance review"` iff `validation["status"] == "Pass"` and `not stale_fields` (otherwise `"Held"`).
* FR-4: Integrity verification and exact dependent-only stale propagation (`FR-043`, `AC-051`).
  * Observable acceptance criteria: `form_validation.pack_freshness(store, user, case_id, saved, rules)` returns `status="Invalid"` when required keys, `case_id`, or `content_sha256` fail verification, `status="Unavailable"` when bound source bytes or `draft_id` are unavailable, `status="Current"` when pack digest and validation state match, and `status="Stale"` with non-empty `reasons` and exact sorted `stale_fields` and `unaffected_fields` when a bound source hash/version, schema definition, reviewer-confirmed input, or field-targeted approved rule changes — including Pass-preserving rule `param`/`message` updates — propagating transitively across `required_when` (`c["field_id"]`) and `sum`/`calculation_ref` dependents while leaving unrelated fields in `unaffected_fields`.

## Non-Functional Requirements

* NFR-1: Strict static typing and lint/format compliance without manifest overrides.
  * Objective threshold or evaluation condition: Zero errors from bare `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/core` with `pyproject.toml` unchanged.
  * Operating condition or verification approach, if needed: Run tools directly from `src/core` across all package and test modules.
  * Observable acceptance criteria: All three commands exit `0` with zero diagnostics.
* NFR-2: Dual-backend determinism and single-pass document hashing.
  * Objective threshold or evaluation condition: Identical behavior across JSON `Store` and SQLite `SqlStore` (`test_*98*.py` passes 100%), and `review_pack` reads/hashes each distinct bound document at most once per call.
  * Operating condition or verification approach, if needed: Execute `unittest` suite against both `Store` and `SqlStore` fixtures plus single-read spy assertion.
  * Observable acceptance criteria: `python3 -m unittest discover -s tests -p 'test_*98*.py' -v` and existing `test_form_*.py` exit `0`.

## Acceptance Criteria

* AC-1: Unapproved schemas, unapproved source policies, unknown funding routes on funding forms, unapproved rule sets, mismatched digests/template versions, and rule sets absent from `schema["rule_refs"]` return `validation["status"] == "Not evaluated"` and `pack_status == "Held"`.
* AC-2: Malformed rule sets (non-dict, invalid `kind` or `param` for field type, unknown `field_id`, unbound `sum` `calculation_ref` or non-numeric addends) raise `ValueError`.
* AC-3: Approved rules (`min`, `max`, `max_length`, `pattern`, `equals`, `one_of`, `sum`) evaluate strictly against registered-reviewer-confirmed, intact-evidence, current, valid inputs; staged candidates, rejected fields, stale fields, blank strings, and tampered draft entries are excluded from rule inputs, and overall status obeys `Fail > Conflict > Unknown > Pass`.
* AC-4: `review_pack` links every field, deduplicated evidence entry, and attachment with explicit `template_version` and `input_version`, preserves `reviewed=False`, `submission="Not submitted"`, `eligibility="Not assessed"`, hashes each distinct document at most once per call, and seals the payload with `content_sha256`.
* AC-5: `pack_freshness` rejects tampered packs (`status="Invalid"`) and reports exact `stale_fields` versus `unaffected_fields` across source updates, schema updates, field-targeted rule updates (including transitive `required_when` and `sum` dependents), and reviewer input updates on both `Store` and `SqlStore`.
* AC-6: `src/core/README.md` documents `form_validation`, all 4 `.copilot-tracking/` artifacts exist and reconcile, the required `mypy`/`ruff`/`unittest` command exits `0`, and all work is committed locally with the Copilot trailer and empty `git status --short` (unpushed).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/issue-98-field-validation-2142-plan.md                                                                |
| Phase details                    | .copilot-tracking/details/2026-11-14/issue-98-field-validation-2142-phase-details.md                                                     |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/issue-98-field-validation-2142-plan-critique.md with Revise verdict; all 3 planner-owned findings (`PC-001`–`PC-003`) resolved directly |
| Relevant research                | .copilot-tracking/research/2026-11-14/issue-98-field-validation-2142-research.md                                                         |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/issue-98-field-validation-2142-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete and Ready for implementation (`PC-001`–`PC-003` resolved; locked test ownership in `test_issue_98_field_validation.py`, 0 removals, max 16 test methods) |
| Continuation context             | Confirmed automatic RPI Agent parent return; transitions automatically to `Implement`                                                     |

## Sources

* `.copilot-tracking/research/2026-11-14/issue-98-field-validation-2142-research.md`: Grounded Cycle 1 codebase evidence (`C1`–`C12`), contrarian audit of untracked `form_validation.py`, and converged design decisions.
* `docs/prds/zava-forward-retrofit-programme-demonstrator.md`: Canonical requirements `FR-038`–`FR-043` and acceptance criteria `AC-046`–`AC-054`.
* `src/core/src/zava_forward/core/forms.py`: Schema registration (`Unapproved` default), `TYPES`, `HUMAN_ONLY`, `rule_refs`, `calculation_ref`, `required_when`, and `schema_impact`.
* `src/core/src/zava_forward/core/form_review.py`: Candidate staging, reviewer history, `_reviewer_confirmed`, `_report`, and single-pass document digest caching.
* `src/core/src/zava_forward/core/form_export.py`: Held draft export contract (`BODY_KEYS`, per-field `input_version`, attachment versioning) pinned by `src/api`.
* `src/core/evals/fictional_form_review_pack.json`: Fictional guardrail proving `FD-01`–`FD-14` remain unresolved human decisions.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement deterministic approved-rule validation, version-linked review pack, and exact stale propagation

* Intent: Deliver `form_validation.py` and dual-store behavioral tests in `src/core` satisfying AC-1 through AC-5 with strict typing.
* Dependencies: None

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Complete and harden `src/core/src/zava_forward/core/form_validation.py`

* Requirement and evidence: FR-1, FR-2, FR-3, FR-4, NFR-1, NFR-2 (`C1`–`C6`, `C10`, `C11`)
* Expected result: `validate`, `review_pack`, and `pack_freshness` enforce approved-rule + `rule_refs` + evidenced-funding gates, strict registered-reviewer confirmation checks, closed-vocabulary deterministic rules (`min`, `max`, `max_length`, `pattern`, `equals`, `one_of`, `sum`), `Fail > Conflict > Unknown > Pass` aggregation, single-pass `_report` version-linked `fields`/`evidence`/`attachments`/`history` assembly, `content_sha256` integrity, and exact dependent-only `stale_fields` across source, schema, rule, and input changes, with zero `mypy` errors.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/issue-98-field-validation-2142-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Create `src/core/tests/test_issue_98_field_validation.py` for JSON and SQLite stores

* Requirement and evidence: AC-1 through AC-5, NFR-1, NFR-2 (`C7`, `C8`, `C9`)
* Expected result: Up to 16 focused behavioral test methods (0 test removals; canonical target `src/core/tests/test_issue_98_field_validation.py`, generated targets `none`) exercising `Store` and `SqlStore` via `test_form_review.FormReview` without `pyproject.toml` edits, plus regression execution of existing `test_form_*.py`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/issue-98-field-validation-2142-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Update component documentation and pass local verification gate

* Intent: Synchronize `src/core/README.md` with `form_validation` capabilities and governance boundaries, and verify all static/unit/regression checks pass cleanly.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Document `form_validation` APIs and open `FD-01`–`FD-14` boundaries in `src/core/README.md`

* Requirement and evidence: AC-6 (`C1`, `C8`, `src/core/README.md`)
* Expected result: `src/core/README.md` documents `form_validation.validate`, `form_validation.review_pack`, `form_validation.pack_freshness`, supported deterministic rule kinds, version-linked `fields`/`evidence`/`attachments`, and the unchanged `Unapproved` registration / external human Finance authority boundary.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/issue-98-field-validation-2142-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Execute required `mypy`, `ruff`, `test_*98*.py`, and form regression checks

* Requirement and evidence: NFR-1, NFR-2, AC-6 (`C7`, `C9`, `C11`)
* Expected result: Exact caller command (`python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*98*.py' -v`) and regression `python3 -m unittest discover -s tests -p 'test_form*.py'` exit `0` in `src/core`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/issue-98-field-validation-2142-phase-details.md

## Dependencies

* `zava_forward.core.forms`, `zava_forward.core.form_review`, and `zava_forward.core.form_export`: Existing schema, staging/review, and held-export primitives consumed by `form_validation` without breaking `src/api` callers (`C1`–`C5`, `C12`).
* Python 3.12 toolchain in environment (`mypy`, `ruff`, `unittest` installed and verified in Wave 2): Required to run the exact local verification gate in `src/core` (`C7`, `C11`).

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1: `PC-001` [High]   | resolved    | Updated `FR-3`, `FR-4`, `P01-T01`, and `P01-T02` to persist `kind`, `param`, and `message` in `validation["results"]`, iterate `c["field_id"]` over `field["required_when"]` for transitive propagation, guarantee non-empty `Stale` `reasons`, and test Pass-preserving rule `param` changes. |
| Run 1: `PC-002` [High]   | resolved    | Updated `FR-3`, `FR-4`, `P01-T01`, and `P01-T02` to use typed `form_export._digest` + `form_review._visible` and enforce controlled `status="Unavailable"` / cross-case `Invalid` guards across `validate`, `review_pack`, and `pack_freshness`. |
| Run 1: `PC-003` [Medium] | resolved    | Updated `P01-T01`, `P01-T02`, and `P02-T01` to separate confirmation-provenance checks from blank/wrong-type checks, enforce exact rule key sets and `HUMAN_ONLY` rejection, allow nullable unapproved `approver` metadata, use `Decimal` `number` equality, stamp deterministic `attachment_id` on pack attachments, and reconcile `src/core/README.md` lines 668 and 692–693. |

## Follow-Up Items

* Finance and template-owner authority decisions `FD-01` to `FD-14` (`#96`, `#97`, `#98`): Outside immediate `src/core` engineering scope because only named Zava North Homes Finance, Legal, and template-owner roles can ratify real templates, source policies, and live funding rules; owned by Finance/template owner before closing `#98`.
* Employee API and UI routes for `form_validation.validate`, `review_pack`, and `pack_freshness`: Outside immediate `src/core`-bounded caller scope; candidate follow-up story once Finance rule-set persistence is ratified.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/issue-98-field-validation-2142-changes.md
* Ready phase or task: P01 / P01-T01
* Remaining provisional question or blocker: none
