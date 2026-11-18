<!-- markdownlint-disable-file -->
# RPI Changes: Issue #93 Deterministic No-Automated-Finance-Authority Invariant

## Metadata

* Task ID: issue-93-finance-no-auto-path
* Related plan: .copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md
* Implementation date: 2026-11-15

## Execution Status

* Status: Complete
* Declared invocation scope: full plan (`P01`, `P02`)
* Completed scope markers: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`
* All remaining active-plan markers: none
* Status basis: Implemented deterministic `RULE-010` automated-finance-authority guard and verifier across `src/core` and `src/api`, added comprehensive `#93` invariant test suite and `src/core/README.md` documentation, and verified `ruff check`, `ruff format --check`, strict `mypy`, and unit/API regression tests with zero errors.

## Execution Summary

Delivered full-plan implementation proving issue `#93`'s engineering acceptance criterion (`No automated path submits a bid, approves match funding, certifies a claim or records cash`, `RULE-010`, `AC-035`). Implemented `PROTECTED_FINANCE_OPERATIONS`, `AutomatedFinanceAuthorityRefusedError(ValueError)`, `classify_finance_operation`, `guard_no_automated_finance_authority`, SQL writer revalidation (`validate_sql`), and AST-plus-probe `verify_no_automated_finance_authority` in `src/core/src/zava_forward/core/finance.py`; wired pre-mutation guards into `grants.py`, `store.py` (`funding_step`), `form_review.py`, and `src/api/src/zava_forward/api/server.py` (`/api/cases/{cid}/funding` `body` forwarding); authored `src/core/tests/test_finance_no_automated_path_93.py`; and updated `src/core/README.md`.

## Completed Work

### Core Deterministic Guard and Invariant Verifier (`P01`, `P01-T01`)

* Updated `src/core/src/zava_forward/core/finance.py`:
  * Added `PROTECTED_FINANCE_OPERATIONS = ("submit_bid", "approve_match_funding", "certify_claim", "record_cash")` and `AutomatedFinanceAuthorityRefusedError(ValueError)` with structured metadata (`operation`, `actor_kind`, `reason`, `rule="RULE-010"`, `code="automated_finance_authority_refused"`, `as_record() -> dict[str, str]`).
  * Added `classify_finance_operation` and `guard_no_automated_finance_authority` rejecting `None`/non-`Mapping`/unauthenticated callers, automated/system/agent/worker/orchestrator/bot/service/managed-identity/AI actor flags, roles, principal types, and identity prefixes, AI proposal-apply payload keys (`proposal_id`, `recommendation_id`, `assistant_task_id`, `ai_proposal`, `from_proposal`, `apply_proposal`, `auto_apply`, `automated`, `envelope`, `approved=True`), automated shortcut action names, and stored non-human `financial_authority` staff designations on `finance_action`.
  * Wired `guard_no_automated_finance_authority` into `FinanceMixin.finance_action`, `FinanceMixin._finance_operation(..., operation=..., check_stored_human=...)`, and `validate_sql(store)` while preserving `PermissionError` / `AuthorityGateError` on `grant_action` stored staff exercises.
  * Added `verify_no_automated_finance_authority(store=None)` performing bounded-AI `propose-only` registry checks (`funding-evidence`, `funding_draft`), AST boundary scans across core automation modules plus `src/agents` and `src/orchestrator` (without importing sibling packages), read-only snapshot verification on any supplied `Store` / `SqlStore`, and disposable synthetic `Store` runtime refusal probes across all four protected `#93` operations (`probes_executed == 44`).
  * Preserved untouched legacy lines in `finance.py` (`[tool.ruff.format].exclude` per ADR 0006) for a pure surgical diff (`+982/-5`).

### Operation-Aware Entry Guards Across Grants, Funding Applications, Form Packs, and API (`P01`, `P01-T02`)

* Updated `src/core/src/zava_forward/core/grants.py`:
  * Performed read-only `self.cases.get(case_id)` lookup of `pending["to"]` (`SqlStore`-safe, no `_case()`/`_touch()` outside writer locks) to classify `grant_action` operations accurately (`submit_bid`, `certify_claim`, `record_cash`, or `finance_authority`) and invoke `guard_no_automated_finance_authority` before and after `refuse_bulk`.
* Updated `src/core/src/zava_forward/core/store.py`:
  * Extended `Store.funding_step(self, u, cid, act, text="", *, body=None, **extra)` to classify `funding_step` (`submit` -> `submit_bid`, `approve` -> `approve_match_funding`) and enforce `guard_no_automated_finance_authority` before `require_role` or case mutation.
* Updated `src/core/src/zava_forward/core/form_review.py`:
  * Wired `classify_finance_operation("form_review", act, body)` and `guard_no_automated_finance_authority` into `action(store, user, case_id, body)` before `staff_actor(store, user)`.
* Updated `src/api/src/zava_forward/api/server.py`:
  * Forwarded `body=body` in `s.funding_step(u, cid, body.get("action"), body.get("text", ""), body=body)` on `/api/cases/{cid}/funding` so AI proposal-apply keys on HTTP requests reach `guard_no_automated_finance_authority` (mapping cleanly to HTTP `400` via `except ValueError`) while preserving the `"s.funding_step("` string contract verified by `test_funding_automation_boundary.py`.

### End-to-End `#93` Invariant Suite and Core Documentation (`P02`, `P02-T01`, `P02-T02`)

* Added `src/core/tests/test_finance_no_automated_path_93.py`:
  * 9 end-to-end invariant tests covering structured `AutomatedFinanceAuthorityRefusedError.as_record()`, all four protected operations x 10 automated/agent/worker/orchestrator/system/bot/service/unauthenticated/non-human callers across both JSON `Store` and `SqlStore` with case-snapshot equality and `verify_audit() is True`, stored non-human `financial_authority` rejection on `finance_action`, legitimate independent designated human positive controls for all four operations, `Store.funding_draft` + `Store.review_ai` proposal boundary refusal, `Assistants` `funding-evidence` proposal acceptance + apply refusal, `form_review.action` automated/proposal refusal, AST boundary inspection of `src/agents` and `src/orchestrator`, and `verify_no_automated_finance_authority` positive (`Store` + `SqlStore`) and negative tamper checks (`AI_CAPABILITIES`, `FUNDING_AI_CAPABILITY`, and AST direct-call tamper).
* Updated `src/core/README.md`:
  * Added `#93` section documenting `PROTECTED_FINANCE_OPERATIONS`, `AutomatedFinanceAuthorityRefusedError`, `guard_no_automated_finance_authority`, `verify_no_automated_finance_authority`, and the focused unittest command.

## Implementation-Time Plan and Detail Updates

* Local judgment only (restored untouched legacy lines of `finance.py` after running `ruff format` directly so `[tool.ruff.format].exclude` history purity per ADR 0006 is preserved without plan changes).

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` (exit 0) |
| `python3 -m ruff format --check .` | `src/core` | Passed | `301 files already formatted` (exit 0) |
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 354 source files` (exit 0) |
| Focused `#93` + finance/grant/funding/form/bounded-AI/dependency tests | `src/core` | Passed | `Ran 215 tests in 57.401s OK (skipped=45)` covering `test_finance_no_automated_path_93`, `test_dependency_rule`, `test_funding_automation_boundary`, `test_grant_lifecycle_controls`, `test_finance_match_controls`, `test_finance_signoffs`, `test_form_review`, `test_epic104_bounded_ai_invariants` |
| Full `src/core` unittest suite + CLI `.pth` verification | `src/core` | Passed | All 3,580+ in-process unit tests pass; 3 CLI subprocess modules (`test_discovery_assistant_demo`, `test_learning_test_bundles`, `test_stock_fabric`) verified in `.pth`-configured venv (`Ran 54 tests in 14.228s OK`); optional `[iothub]` extra test `test_device_registry_azure` covered by hosted CI |
| `python3 tools/rename-zava-tests.py` | Repository root | Passed | `Ran 25 tests in 14.129s OK` |
| `python3 -m ruff check .` + `PYTHONPATH=../core/src:../agents/src python3 -m mypy` | `src/api` | Passed | `All checks passed!` and `Success: no issues found in 297 source files` (exit 0) |
| Targeted finance/grant/form/dependency API tests | `src/api` | Passed | `test_finance_match_api.py` and `test_grant_lifecycle_api.py` (`Ran 3 tests in 3.503s OK (skipped=1)`), plus `test_form_review_api.py` and `test_dependency_rules.py` (44 tests OK in earlier full API pass) |

## Pre-Review Reconciliation

* Plan markers and phase details: Reconciled (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` all `[x]`)
* Completed-work evidence and handoff prose: Reconciled with surgical diffs and zero internal tracking references in `src/`
* Validation, blockers, remaining work, and follow-up items: Reconciled (`0` blockers, `0` remaining plan items)
* Review readiness: Ready

## Blockers

* None.

## Remaining Work

* None in declared plan scope (`P01` and `P02` complete).

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md, `## Follow-Up Items`
* Epic `#93` stabilization and full epic closure remain outside this branch's scope because `#93` lists open stabilization checkpoint `#440` and requires owner PR merge before ticking criteria on GitHub; owner/coordinator tracks after PR review.

## Return-to-Caller State

* Implementation execution status: Complete
* Declared scope and markers: full plan; completed: `P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`; remaining: none
* Validation coverage: `src/core` (`ruff check`, `ruff format --check`, `mypy`, 215 focused + full in-process + `.pth` CLI tests), `tools/rename-zava-tests.py` (25 tests), `src/api` (`ruff check`, `mypy`, targeted finance/grant API tests) all passed
* Blockers: None
* Current plan and detail updates: Local judgment only (`finance.py` legacy line preservation per ADR 0006)
* Planning and critique state: Ready (`PC-001`..`PC-004` resolved)
* Follow-up items: Epic `#93` checkpoint `#440` and post-merge tick-off
* Review readiness or no-handoff reason: Ready for `rpi-review`
* Continuation owner: parent (confirmed automatic RPI Agent)
