<!-- markdownlint-disable-file -->
# RPI Plan: Issue #93 Deterministic No-Automated-Finance-Authority Invariant

## Task Metadata

* Task ID: issue-93-finance-no-auto-path
* Task slug: finance-93-no-auto-path
* Planning status: Ready
* Plan date: 2026-11-15
* Phase details: .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/finance-93-no-auto-path-plan-critique.md

## Executive Summary

This plan proves and enforces the unticked engineering acceptance criterion of issue `#93` (*Epic: Finance, grants and form-assisted funding evidence*): **no automated path submits a bid, approves match funding, certifies a claim, or records cash** (`RULE-010`, `AC-035`). Although Zava Forward already separates draft proposals (`funding_draft`, `funding-evidence`) from named-staff state changes (`finance_action`, `grant_action`, `funding_step`, `form_review.action`), contrarian research identified three hardening gaps: non-dict or unauthenticated callers hit `AttributeError` or unstructured errors, `finance_action` budget/commitment/disposition/payment-status approvals lack a deterministic automated-actor refusal and stored non-human designation check, and no single deterministic invariant verifier audits all four protected operations across core, AI proposal-apply, and agent/orchestrator surfaces.

The implementation introduces fully type-annotated `AutomatedFinanceAuthorityRefusedError(ValueError)` with structured refusal metadata (`operation`, `actor_kind`, `reason`, `rule="RULE-010"`, `code="automated_finance_authority_refused"`, `.as_record()`), wires `guard_no_automated_finance_authority` across `finance.py`, `grants.py`, `store.py` (`funding_step`), `form_review.py`, and the `/api/cases/{cid}/funding` `body` pass-through in `api/server.py`, adds AST-and-probe invariant verifier `verify_no_automated_finance_authority(...)` in `finance.py`, proves all four operations end to end in `src/core/tests/test_finance_no_automated_path_93.py` (strictly honoring `src/core`'s `ALLOWED = {"core"}` package-isolation rule), and documents the invariant in `src/core/README.md`.

### User Decisions and Requirements Highlights

* **Enforce structured refusal (`AutomatedFinanceAuthorityRefusedError` / `ValueError`)**: Any attempt by an automated, system, agent, worker, orchestrator, unauthenticated, or non-human caller, or an AI proposal-apply payload, to submit a bid, approve match funding, certify a claim, or record cash is deterministically rejected before any state or audit mutation.
* **Preserve existing human RBAC and exercise-designation contracts**: Ordinary registered or unregistered human-shaped staff who lack role membership, independence, or active grant exercise designation continue raising `PermissionError` / `AuthorityGateError` (HTTP `403`), preserving compatibility with `#94` and `#95` tests while `AutomatedFinanceAuthorityRefusedError(ValueError)` maps cleanly to HTTP `400` at the API boundary.
* **Prove all four operations across core, proposal-apply, and orchestrator/agent boundaries**: A dedicated test module `src/core/tests/test_finance_no_automated_path_93.py` exercises both JSON `Store` and `SqlStore`, AI proposal generation/acceptance (`funding_draft`, `funding-evidence`), AST-verified `src/agents` and `src/orchestrator` module boundaries (without importing non-`core` packages inside `src/core`), and `verify_no_automated_finance_authority`, complemented by targeted `src/api` regression checks.
* **Focused validation and frozen HEAD**: Validate with `ruff check`, `ruff format --check .`, `mypy`, and `unittest` in `src/core` (plus `ruff check`, `mypy`, and targeted finance/grant API regression tests in `src/api`) and commit locally with the Copilot trailer without pushing.

### What You May Not Know

* Two filenames named in the epic prompt (`funding_packs.py` and `src/api/src/zava_forward/api/routers/finance_grants.py`) do not exist in the repository; form-assisted funding/claim pack staging, review, and draft export live in `forms.py`, `form_review.py`, `form_export.py`, and `store.py`, and HTTP finance/grant/funding routes live in `src/api/src/zava_forward/api/server.py` (where `/api/cases/{cid}/funding` previously dropped extra `body` keys before calling `s.funding_step`, fixed via a one-line `body=body` pass-through).
* `src/core/tests/test_dependency_rule.py` enforces `ALLOWED = {"core"}` via AST inspection and `.github/workflows/src-ci.yml` runs `src-core` with `deps: ""` (`ruff check . && ruff format --check .` and `mypy --strict`). Therefore, `finance.py` and `test_finance_no_automated_path_93.py` never import `zava_forward.{api,agents,orchestrator,importer}`, inspect automation boundaries via `ast.parse`, and carry full type annotations on all new `finance.py` symbols.

### Unresolved Decisions or Blockers

* None.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`), writing dated artifacts under `.copilot-tracking/` (`research`, `plans`, `details`, `changes`, `reviews`) under `2026-11-15/` for issue `#93` on branch `feat/finance-93-no-auto-path` (parent branch `feat/demo-164-chat-grounding-provenance-0900`, `PR #1641`).
* Prove the unticked engineering acceptance criterion of `#93`: `No automated path submits a bid, approves match funding, certifies a claim or records cash` (issue `#93`; `docs/brds/agentic-retrofit-programme-brd.md` `RULE-010`, `AC-035`).
* Add or strengthen a deterministic guard and invariant verification function (`verify_no_automated_finance_authority` in `src/core/src/zava_forward/core/finance.py`) and ensure any attempt by an automated, system, agent, worker, orchestrator, unauthenticated, or non-human caller, or AI proposal-apply path, to perform any of the four protected operations is deterministically rejected with `AutomatedFinanceAuthorityRefusedError` (`ValueError` subclass).
* Add a comprehensive end-to-end invariant test `src/core/tests/test_finance_no_automated_path_93.py` covering all four protected operations across core, agent/proposal apply, and orchestrator/automated actors.
* Update `src/core/README.md` to document the `#93` invariant check.
* Use the Focused validation tier (`ruff check`, `mypy`, and `unittest` in `src/core`, plus targeted `src/api` finance/grant regression tests).
* Commit all code, tests, and `.copilot-tracking/` artifacts with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and do NOT push; leave a clean frozen HEAD.

## Goals

* Enforce a deterministic, structured `RULE-010` refusal (`AutomatedFinanceAuthorityRefusedError(ValueError)`) across every core finance, grant, funding-application, and form-pack mutation boundary before any state or audit write can occur.
* Provide a deterministic runtime and structural verifier `verify_no_automated_finance_authority` in `src/core/src/zava_forward/core/finance.py` proving that AI capabilities remain `propose-only`, agent/orchestrator modules hold no finance/grant execution paths, and automated/non-human/proposal-apply probes fail closed across all four protected operations.
* Prove end-to-end invariant enforcement across JSON `Store`, `SqlStore`, AI proposal review/apply boundaries, agent/orchestrator actors, and HTTP API handlers with zero regressions in existing `#93`, `#94`, `#95`, and `#104` suites.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/finance.py`: Fully type-annotated `PROTECTED_FINANCE_OPERATIONS`, `AutomatedFinanceAuthorityRefusedError(ValueError)`, `classify_finance_operation`, `guard_no_automated_finance_authority`, stored non-human `financial_authority` check scoped to `finance_action` (`check_stored_human=True` in `_finance_operation` and `validate_sql`), and AST-and-disposable-fixture `verify_no_automated_finance_authority`.
* `src/core/src/zava_forward/core/grants.py`, `src/core/src/zava_forward/core/store.py` (`funding_step` accepting optional `body=None`), `src/core/src/zava_forward/core/form_review.py` (`action`), and `src/api/src/zava_forward/api/server.py` (`/api/cases/{cid}/funding` `body=body` pass-through): pre-operation invocation of `guard_no_automated_finance_authority` with read-only operation classification and proposal-apply rejection.
* `src/core/tests/test_finance_no_automated_path_93.py`: comprehensive end-to-end invariant test suite using only `zava_forward.core` imports and AST boundary inspection.
* `src/core/README.md`: documentation of the `#93` deterministic guard, error contract, verifier, and focused test command.

### Non-Goals

* Creating unused placeholder modules (`funding_packs.py` or `routers/finance_grants.py`) that are absent from the codebase architecture.
* Modifying web UI assets under `src/api/src/zava_forward/api/web/`, Bicep templates under `infra/`, or closing epic `#93` before stabilization checkpoint `#440`.
* Pushing commits to `origin` or opening/updating remote pull requests in this session.

## Functional Requirements

* **FR-1 (Structured refusal error)**: `finance.py` defines `AutomatedFinanceAuthorityRefusedError(ValueError)` carrying `operation` (one of `submit_bid`, `approve_match_funding`, `certify_claim`, `record_cash`, or `finance_authority`), `actor_kind`, `reason`, `rule="RULE-010"`, `code="automated_finance_authority_refused"`, and `as_record() -> dict[str, str]`.
  * Observable acceptance criteria: Catching either `AutomatedFinanceAuthorityRefusedError` or `ValueError` succeeds and `.as_record()` returns deterministic structured refusal fields.
* **FR-2 (Automated/non-human/unauthenticated actor & proposal-apply guard)**: `guard_no_automated_finance_authority(user, *, operation=..., body=None, store=None, action=None)` deterministically rejects:
  1. `None`, non-`dict`, or blank/unauthenticated actor payloads lacking both `email` and `code`.
  2. Actor payloads carrying `human is False`, `automated` / `is_automated` / `is_agent` / `is_system` / `service_principal` truthy flags, caller `financial_authority.human is False`, automated `actor_type` / `kind` / `principal_type` / `identity_source` / `auth_provider` / `caller_type` values (`automated`, `system`, `agent`, `worker`, `orchestrator`, `bot`, `service`, `service_principal`, `managed_identity`, `ai`, `assistant`, `cron`, `job`, `scheduler`, `unauthenticated`, `anonymous`), automated role names, or automated email/code prefixes (`system@`, `agent@`, `worker@`, `orchestrator@`, `bot@`, `noreply@`, `service-principal`, `managed-identity`, `AUTO-`, `BOT-`, `SYS-`, `AGENT-`, `WORKER-`, `ORCH-`).
  3. Request/action payloads attempting AI proposal auto-application (`proposal_id`, `recommendation_id`, `assistant_task_id`, `ai_proposal`, `from_proposal`, `apply_proposal`, `auto_apply`, `automated`, `envelope`, or `approved=True`) or direct automated shortcut actions (`submit_bid`, `approve_match_funding`, `certify_claim`, `record_cash`, `auto_submit`, `auto_approve`, `auto_certify`, `auto_record_cash`).
  4. Stored staff records on `finance_action` whose `financial_authority.human is False` or carry automated staff flags (while preserving `AuthorityGateError(PermissionError)` inside `grants.require_authority` for stored grant-designation mutations tested by `#95`).
  * Observable acceptance criteria: Every prohibited caller/payload across `finance_action`, `grant_action`, `funding_step`, and `form_review.action` raises `AutomatedFinanceAuthorityRefusedError` with zero mutation to case records or hash-chained audit entries.
* **FR-3 (Deterministic invariant verifier)**: `verify_no_automated_finance_authority(store=None)` returns a deterministic verification report (`ok=True`, `rule="RULE-010"`, `operations`, `actors_checked`, `ai_capabilities_checked`, `module_boundaries_checked`, `probes_executed`) and raises `AutomatedFinanceAuthorityRefusedError` if any of the four operations, AI funding capabilities (`funding-evidence`, `funding_draft`), or AST-inspected automation/agent/orchestrator modules permits an automated path. Probes always execute against a self-contained disposable synthetic `Store` in a `TemporaryDirectory` (never importing non-`core` packages or mutating any supplied `Store` / `SqlStore`, whose `cases` and audit chain are snapshotted before and after to assert zero caller mutation).
  * Observable acceptance criteria: `verify_no_automated_finance_authority()` and `verify_no_automated_finance_authority(store)` (for both `Store` and `SqlStore`) return `ok is True` covering all four `#93` operations without mutating `store`, and fail closed with `AutomatedFinanceAuthorityRefusedError` under simulated tampering.
* **FR-4 (Documentation)**: `src/core/README.md` documents `AutomatedFinanceAuthorityRefusedError`, `PROTECTED_FINANCE_OPERATIONS`, `verify_no_automated_finance_authority`, and the focused `#93` test command.
  * Observable acceptance criteria: `src/core/README.md` accurately matches exported symbols and test commands without internal tracking path references.

## Non-Functional Requirements

* **NFR-1 (Backwards compatibility with `#94`, `#95`, `#104`)**: Existing human staff authorization, independence, and exercise-designation tests continue passing without exception-class drift.
  * Objective threshold or evaluation condition: 100% pass rate on `src/core` unit tests and targeted `src/api` finance/grant tests (`test_finance_match_api.py`, `test_grant_lifecycle_api.py`).
  * Operating condition or verification approach, if needed: Run `unittest discover` in `src/core` and targeted `unittest` in `src/api`.
  * Observable acceptance criteria: Zero failures or regressions across existing core and API tests.
* **NFR-2 (Static type safety and lint cleanliness)**: All modified and added files satisfy repository lint, formatting, package-isolation, and type rules.
  * Objective threshold or evaluation condition: Zero errors from `python3 -m ruff check .`, `python3 -m ruff format --check .`, and bare `python3 -m mypy` inside `src/core` (and `python3 -m ruff check` + `PYTHONPATH=../core/src:../agents/src python3 -m mypy` inside `src/api`), with `test_dependency_rule.py` passing (`ALLOWED = {"core"}`).
  * Operating condition or verification approach, if needed: Run `ruff check`, `ruff format --check`, and `mypy` matching `.github/workflows/src-ci.yml`.
  * Observable acceptance criteria: Exit code `0` across all lint, format-check, and `mypy` commands.
* **NFR-3 (Atomicity and zero partial writes)**: Refused automated calls never mutate in-memory state, SQLite/SQL tables, or the hash-chained audit trail (`verify_audit() is True`).
  * Objective threshold or evaluation condition: Pre-call and post-call case/finance/grant/funding snapshots and audit entry counts are identical across both `Store` and `SqlStore`.
  * Operating condition or verification approach, if needed: Snapshot comparison and `store.verify_audit()` assertions in `test_finance_no_automated_path_93.py`.
  * Observable acceptance criteria: Snapshot equality and `verify_audit() is True` hold across every probe.

## Acceptance Criteria

* `AutomatedFinanceAuthorityRefusedError(ValueError)`, `PROTECTED_FINANCE_OPERATIONS`, `guard_no_automated_finance_authority`, and `verify_no_automated_finance_authority` are implemented in `src/core/src/zava_forward/core/finance.py` and enforced across `finance_action`, `_finance_operation`, `validate_sql`, `grant_action`, `funding_step`, and `form_review.action`.
* All four protected `#93` operations (`submit_bid`, `approve_match_funding`, `certify_claim`, `record_cash`) deterministically reject automated, system, agent, worker, orchestrator, unauthenticated, and non-human actors as well as AI proposal-apply attempts across both `Store` and `SqlStore` with `AutomatedFinanceAuthorityRefusedError` (`ValueError`) and zero state/audit mutation.
* Accepting or reviewing AI proposals (`funding_draft` via `Store.review_ai` and `funding-evidence` via `Assistants.review`) leaves `funding`, `grants`, and `finance` states unsubmitted, unapproved, uncertified, and without recorded cash, and passing accepted proposal artifacts into finance/grant/funding/form-review actions raises `AutomatedFinanceAuthorityRefusedError`.
* `src/agents` and `src/orchestrator` modules (plus core automation modules) are proven via AST boundary inspection in `verify_no_automated_finance_authority` and `src/core/tests/test_finance_no_automated_path_93.py` to contain no automated execution path for the four protected operations, without violating `src/core/tests/test_dependency_rule.py`.
* `src/core/README.md` documents the `#93` invariant check and test command.
* `python3 -m ruff check .`, `python3 -m ruff format --check .`, `python3 -m mypy`, and `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` in `src/core` (plus `ruff check`, `mypy`, and targeted API tests `test_finance_match_api.py` and `test_grant_lifecycle_api.py` in `src/api`) pass with exit code `0`.
* All code, tests, README updates, and `.copilot-tracking/` artifacts (`research`, `plans`, `details`, `changes`, `reviews`, `rpi-sessions`) are committed cleanly on `feat/finance-93-no-auto-path` with the Copilot trailer and not pushed.

## Test Ownership and Change Bounds

* Canonical semantic coverage owner: `src/core/tests/test_finance_no_automated_path_93.py` (new focused invariant suite testing all 4 operations x automated/agent/worker/orchestrator/system/unauthenticated/non-human/proposal-apply vectors across `Store`, `SqlStore`, `Assistants`, `form_review`, AST-inspected `agents`/`orchestrator` boundaries, and `verify_no_automated_finance_authority`, importing only `zava_forward.core`).
* Regression coverage owners: `src/core/tests/test_dependency_rule.py`, `src/core/tests/test_funding_automation_boundary.py`, `src/core/tests/test_grant_lifecycle_controls.py`, `src/core/tests/test_finance_match_controls.py`, `src/core/tests/test_finance_signoffs.py`, `src/core/tests/test_form_review.py`, `src/core/tests/test_epic104_bounded_ai_invariants.py`, `src/api/tests/test_finance_match_api.py`, and `src/api/tests/test_grant_lifecycle_api.py`.
* Exact file removals: `none`.
* Maximum new files added (excluding `.copilot-tracking/` artifacts): `1` (`src/core/tests/test_finance_no_automated_path_93.py`).
* Canonical modified production/doc targets: `src/core/src/zava_forward/core/finance.py`, `src/core/src/zava_forward/core/grants.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/form_review.py`, `src/api/src/zava_forward/api/server.py`, and `src/core/README.md` (`generated targets: none`).

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md                                                                       |
| Phase details                    | .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md                                                            |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-15/finance-93-no-auto-path-plan-critique.md with Revise disposition (PC-001..PC-004 all resolved) |
| Relevant research                | .copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md                                                                |
| Changes-record role              | .copilot-tracking/changes/2026-11-15/finance-93-no-auto-path-changes.md is created or continued by implementation as its evidence record |
| Planning execution and readiness | Complete; Ready for rpi-implement after resolving PC-001..PC-004                                                                         |
| Continuation context             | Active confirmed automatic RPI Agent continues directly to Implement (rpi-implement)                                                     |

## Sources

* `.copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md`: `C1`-`C20` codebase evidence mapping all four operations, actor validation, bounded-AI proposals, agent/orchestrator surfaces, and `#94`/`#95` test contracts.
* `docs/brds/agentic-retrofit-programme-brd.md`: `RULE-009`..`RULE-012`, `CON-005`, `CON-006`, and `AC-035` governing human financial and grant authority.
* `src/core/src/zava_forward/core/finance.py`, `grants.py`, `store.py`, `form_review.py`, `bounded_ai.py`: existing core control surfaces.
* `src/core/pyproject.toml` and `src/core/README.md`: strict `mypy`, `ruff`, and `unittest` conventions.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Deterministic No-Automated-Finance-Authority Guard and Verifier

* Intent: Implement `AutomatedFinanceAuthorityRefusedError(ValueError)`, `guard_no_automated_finance_authority`, operation mapping, SQL writer revalidation, and `verify_no_automated_finance_authority`, and wire the guard into `finance.py`, `grants.py`, `store.py`, and `form_review.py`.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Implement `AutomatedFinanceAuthorityRefusedError`, `guard_no_automated_finance_authority`, and `verify_no_automated_finance_authority` in `finance.py`

* Requirement and evidence: FR-1, FR-2, FR-3; `.copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md` (`C1`, `C2`, `C9`, `C10`, `C13`-`C18`)
* Expected result: `finance.py` defines `PROTECTED_FINANCE_OPERATIONS`, `AutomatedFinanceAuthorityRefusedError(ValueError)`, `classify_finance_operation`, `guard_no_automated_finance_authority`, SQL revalidation in `validate_sql`, stored non-human designation checks on finance approvals/payment status, and `verify_no_automated_finance_authority`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Wire operation-aware automated-authority guards into `grants.py`, `store.py`, `form_review.py`, and `api/server.py`

* Requirement and evidence: FR-2, NFR-1, NFR-3; `.copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md` (`C3`, `C5`, `C7`, `C8`, `C17`)
* Expected result: `GrantMixin.grant_action` (using read-only `cases.get` pending lookup), `Store.funding_step` (accepting optional `body=None` forwarded by `api/server.py:1871`), and `form_review.action` invoke `guard_no_automated_finance_authority` with consistent operation mapping before mutating state, while preserving `PermissionError` / `AuthorityGateError` for human RBAC and stored grant-designation checks.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: End-to-End Invariant Test Suite, Documentation, and Focused Validation

* Intent: Prove all four `#93` protected operations across core, AI proposal-apply, orchestrator/agent actors, and HTTP API routes, document the invariant in `src/core/README.md`, and pass focused `ruff`, `mypy`, and `unittest` checks.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Author `src/core/tests/test_finance_no_automated_path_93.py`

* Requirement and evidence: FR-1, FR-2, FR-3, NFR-1, NFR-2, NFR-3; `.copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md` (`C10`-`C19`), `PC-001`..`PC-004`
* Expected result: Strict-`mypy`-clean and `ruff format`-clean test suite importing only `zava_forward.core` that proves `submit_bid`, `approve_match_funding`, `certify_claim`, and `record_cash` refuse all automated, agent, worker, orchestrator, system, unauthenticated, non-human, and AI proposal-apply paths across `Store`, `SqlStore`, `Assistants`, `form_review`, AST-inspected `src/agents` and `src/orchestrator` modules, and `verify_no_automated_finance_authority`, while legitimate independent designated humans still succeed.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Document `#93` invariant check in `src/core/README.md` and run focused validation

* Requirement and evidence: FR-4, NFR-1, NFR-2; `.copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md` (`C19`, `C20`)
* Expected result: `src/core/README.md` documents `AutomatedFinanceAuthorityRefusedError` and `verify_no_automated_finance_authority`, and `ruff check`, `mypy`, `src/core` `unittest`, and targeted `src/api` finance/grant tests pass cleanly.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md

## Dependencies

* `zava_forward.core.bounded_ai` and `zava_forward.core.ai_registry`: reused by `verify_no_automated_finance_authority` to verify funding AI capabilities (`funding-evidence`, `funding_draft`) remain `propose-only`.
* `zava_forward.core.grants` and `zava_forward.core.store`: depend on `finance.py` guards without circular top-level import breakage (use existing local import pattern where needed).

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass `PC-001` [High] (`src/core` dependency-rule and isolated-CI breach from HTTP `App` / sibling imports) | Resolved | Removed all non-`core` imports (`zava_forward.{api,agents,orchestrator}`) from `finance.py` and `src/core/tests/test_finance_no_automated_path_93.py`; replaced sibling imports with AST source inspection compatible with `test_dependency_rule.py` and standalone `src-core` CI (`deps=""`). |
| Single-pass `PC-002` [High] (`SqlStore` incompatibility in `verify_no_automated_finance_authority(store)`, `grant_action` pre-check, and `validate_sql`) | Resolved | `verify_no_automated_finance_authority(store=None)` always runs live probes on a self-contained disposable synthetic `Store` while snapshotting caller `Store`/`SqlStore` `cases` + audit state read-only; `grant_action` inspects `self.cases.get(case_id)` without `_case()`/`_touch()`; `check_stored_human` in `_finance_operation` / `validate_sql` is scoped strictly to `finance_action`. |
| Single-pass `PC-003` [High] (Strict `mypy` `disallow_untyped_calls` annotations and `ruff format --check .` gate) | Resolved | Mandated complete parameter and return type annotations on all new `finance.py` definitions, `Any` wrappers for untyped legacy store helpers in `test_finance_no_automated_path_93.py`, and `python3 -m ruff format --check .` in validation gates. |
| Single-pass `PC-004` [Medium] (`/api/cases/{cid}/funding` proposal-key stripping and `to="Submitted"` operation mapping alignment) | Resolved | Added `body=body` forwarding at `src/api/src/zava_forward/api/server.py:1871` (preserving `"s.funding_step("`) with `src/api` `ruff` + `mypy` validation, and aligned `P01-T01`/`P02-T01` so `grant_open` / `to=="Opportunity"` / `funding_step("submit")` map to `submit_bid` while `Claimable -> Submitted` maps consistently to `certify_claim`. |

## Follow-Up Items

* Epic `#93` stabilization and full epic closure remain outside this branch's scope because `#93` lists open stabilization checkpoint `#440` and requires owner PR merge before ticking criteria on GitHub; owner/coordinator tracks after PR review.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-15/finance-93-no-auto-path-changes.md
* Ready phase or task: Complete (`P01`, `P02`); ready for `rpi-review`
* Remaining provisional question or blocker: none
