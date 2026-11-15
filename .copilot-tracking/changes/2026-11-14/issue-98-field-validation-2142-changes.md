<!-- markdownlint-disable-file -->
# RPI Changes: Issue 98 Deterministic Approved-Rule Validation, Version-Linked Review Pack, and Stale Propagation

## Metadata

* Task ID: issue-98-field-validation-2142
* Related plan: .copilot-tracking/plans/2026-11-14/issue-98-field-validation-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/issue-98-field-validation-2142-phase-details.md
* Implementation date: 2026-11-14

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: Every phase and task in the approved plan has verified completion evidence across `form_validation.py`, `test_issue_98_field_validation.py`, `src/core/README.md`, and local static/unit/regression checks.

## Execution Summary

Delivered `src/core/src/zava_forward/core/form_validation.py`, `src/core/tests/test_issue_98_field_validation.py`, and `src/core/README.md` documentation updates for Issue #98 (`feat/fin-98-field-validation-2142`) without modifying `forms.register_schema` approval behavior, `form_export.draft_export` public keys, or `src/core/pyproject.toml` overrides.

## Completed Work

### Deterministic Approved-Rule Validation and Pack Freshness Engine (`P01`, `P01-T01`)

* Implemented `src/core/src/zava_forward/core/form_validation.py` with full `mypy --strict` typing:
  * `_check_rules`: Enforces exact key sets (`SET_KEYS`, `APPROVAL_KEYS`, `BOUND_KEYS`, `RULE_KEYS`, `SUM_PARAM_KEYS`), closed-vocabulary deterministic kinds (`min`, `max`, `max_length`, `pattern`, `equals`, `one_of`, `sum`), unique `rule_id`s, `Decimal`-safe numeric equality, at most one `sum` rule per field, and `ValueError` rejection of `forms.HUMAN_ONLY` targets or addends while allowing nullable `approver`/`evidence_ref` on `Unapproved` rule sets so `_approval_gaps` returns `Not evaluated`.
  * `_approval_gaps` and `DocumentUnavailable` isolation: Verifies registered schema `approval == "Approved"` + nonblank `approval_evidence`, `source_policy_status == "Approved"`, `Evidenced` funding route for `funding` forms, matching `schema_digest`, `(rules["id"], rules["version"])` membership in `schema["rule_refs"]`, and exact `rules["approval"]`/`rules["bound"]` alignment; returns controlled `status="Unavailable"` payloads when retained documents are missing, pending, or quarantined.
  * `_provenance_confirmed` and `_confirmed`: Evaluates rules exclusively over reviewer-confirmed inputs (`form_review._reviewer_confirmed`, matching `accept`/`correct` history decision, registered reviewer via `forms._registered`, intact source/locator provenance, valid schema type, nonblank string), recording `Fail` (`Value lacks reviewer confirmation.`) on tampered or unregistered history while keeping unreviewed, rejected, stale, or blank-string fields `Unknown` and aggregating `Fail > Conflict > Unknown > Pass`.
  * `review_pack`: Executes one `_report` pass (hashing each distinct document at most once), stamps deterministic `attachment_id = "{id}:v{version}"` on detached `attachments`, links deduplicated `evidence` entries with `attachment_id`, `template_version`, and max bound-field `input_version`, computes `content_sha256` via `form_export._digest`, and keeps `reviewed=False`, `submission="Not submitted"`, and `eligibility="Not assessed"` (`pack_status="Ready for Finance review"` iff `validation["status"] == "Pass"` and `stale_fields` is empty, else `"Held"`).
  * `pack_freshness`: Validates `PACK_BODY_KEYS`, `case_id`, and `content_sha256` (`Invalid` on mismatch/cross-case, `Unavailable` on unavailable source or missing draft), compares fields, `open_issues`, and `validation["results"]` across `(field_id, kind, param, message, status, reason)` so even Pass-preserving rule edits mark affected fields stale, runs fixed-point transitive propagation across `required_when` (`c["field_id"]`) and `sum` (`addends -> target`), and guarantees non-empty `reasons` whenever `status == "Stale"`.

### Dual-Store Behavioral Unit Test Suite (`P01`, `P01-T02`)

* Created `src/core/tests/test_issue_98_field_validation.py` with 12 behavioral test methods executing across both JSON `Store` and SQLite `SqlStore`:
  * Covers unapproved/unbound/unknown-funding `Not evaluated` gates, malformed/human-only `ValueError` checks, strict confirmed-input gating (staged, rejected, blank-string `Unknown`), tampered/unregistered history `Fail` blocking, all 6 scalar types + exact `Decimal` `0.1 + 0.2 == 0.3` `sum` rules, `Fail > Conflict > Unknown > Pass` precedence, version-linked `fields`/`evidence`/`attachments`/`history` assembly + single-pass document reads + reopen persistence, `Invalid` tamper/cross-case rejection, `Unavailable` quarantined-document and missing-draft handling, exact dependent-only staleness across source/input/schema changes, Pass-preserving rule-parameter tightening propagation, and resident/missing/out-of-scope caller authorization checks.
  * Prepends the worktree's `src/core/src` to `sys.path` before `zava_forward` imports (ordinary local judgment) so bare `python3 -m unittest discover -s tests -p 'test_*98*.py' -v` resolves the local worktree package cleanly even when global user site-packages points at another checkout.

### Component Guide Documentation and Local Gate Verification (`P02`, `P02-T01`, `P02-T02`)

* Updated `src/core/README.md` to document `form_validation.validate`, `form_validation.review_pack`, and `form_validation.pack_freshness`, reconcile earlier statements on approved rule evaluation versus open human authority gates (`FD-01` to `FD-14`), and include `test_form_export` and `test_issue_98_field_validation` in the local test example.
* Executed the exact caller verification gate (`mypy`, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*98*.py' -v`) plus full `test_form*.py` regression coverage (`75` tests across JSON and SQLite stores).

## Implementation-Time Plan and Detail Updates

* Retained ordinary local judgment in `src/core/tests/test_issue_98_field_validation.py` to prepend `Path(__file__).resolve().parents[1] / "src"` to `sys.path` before importing `zava_forward`, ensuring bare `python3` in a git worktree always imports the worktree's `zava_forward.core` namespace package without altering shared site-packages or approved plan scope.

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m mypy` | `src/core` (309 source files) | Passed | `Success: no issues found in 309 source files` (strict mode, zero `pyproject.toml` overrides added) |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` (256 formatted files) | Passed | `256 files already formatted` |
| `python3 -m unittest discover -s tests -p 'test_*98*.py' -v` | `src/core/tests/test_issue_98_field_validation.py` | Passed | `Ran 12 tests in 9.039s — OK` (both JSON `Store` and SQLite `SqlStore`) |
| `PYTHONPATH=src python3 -m unittest discover -s tests -p 'test_form*.py' -q` | `src/core/tests/test_form*.py` | Passed | `Ran 75 tests in 46.473s — OK` (zero regressions across `test_form_staging`, `test_form_review`, `test_form_dependencies`, `test_form_export`) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all checked with matching evidence)
* Completed-work evidence and handoff prose: Synchronized in this changes artifact
* Validation, blockers, remaining work, and follow-up items: Current (`0` blockers, `0` remaining active-plan markers)
* Review readiness: Ready for one-pass `rpi-review`

## Blockers

* None

## Remaining Work

* None inside active plan scope (`P01` and `P02` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-14/issue-98-field-validation-2142-plan.md, `## Follow-Up Items`
* Finance and template-owner authority decisions `FD-01` to `FD-14` (`#96`, `#97`, `#98`): External human authority gate owned by Zava North Homes Finance, Legal, and template owner before live schemas are approved or `#98` checkboxes are closed.
* Employee API and UI routes for `form_validation.validate`, `review_pack`, and `pack_freshness`: Outside `src/core`-bounded caller scope; candidate follow-up story once Finance rule-set persistence is ratified.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: `mypy` (309 files), `ruff check .`, `ruff format --check .` (256 files), `test_*98*.py` (12 dual-store tests), `test_form*.py` (75 regression tests) all passed
* Blockers: none
* Current plan and detail updates: All `P01` and `P02` checklist markers checked in `.copilot-tracking/plans/2026-11-14/issue-98-field-validation-2142-plan.md`
* Planning and critique state: Ready (`PC-001`–`PC-003` resolved)
* Follow-up items: `FD-01`–`FD-14` human authority decisions; optional `src/api` route exposure
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent for confirmed automatic RPI Agent
