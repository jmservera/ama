<!-- markdownlint-disable-file -->
# RPI Plan Critique: Issue #93 Deterministic No-Automated-Finance-Authority Invariant

## Metadata

* Task ID: issue-93-finance-no-auto-path
* Critique date: 2026-11-15
* Plan: .copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md
* Critique execution status: Complete

## Inputs and Criterion Boundary

* Task context and caller requirements: Enforce and verify the unticked engineering acceptance criterion of issue `#93` (`No automated path submits a bid, approves match funding, certifies a claim or records cash`, `RULE-010`, `AC-035`) by adding `AutomatedFinanceAuthorityRefusedError(ValueError)`, `guard_no_automated_finance_authority`, and `verify_no_automated_finance_authority` in `src/core/src/zava_forward/core/finance.py` across all four protected operations, wiring operation-aware guards across core finance/grant/funding/form-review entry points, adding `src/core/tests/test_finance_no_automated_path_93.py`, updating `src/core/README.md`, running focused validation (`ruff`, `mypy`, `unittest` in `src/core` plus targeted `src/api` finance/grant tests), and committing locally with the Copilot trailer without pushing.
* Research and evidence considered: .copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md, .copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md, .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md, src/core/src/zava_forward/core/finance.py, src/core/src/zava_forward/core/grants.py, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/form_review.py, src/core/src/zava_forward/core/forms.py, src/core/src/zava_forward/core/form_export.py, src/core/src/zava_forward/core/change_provenance.py, src/core/src/zava_forward/core/identity.py, src/core/src/zava_forward/core/bounded_ai.py, src/core/src/zava_forward/core/controls.py, src/core/tests/test_dependency_rule.py, src/core/tests/test_funding_automation_boundary.py, src/core/tests/test_grant_lifecycle_controls.py, src/core/tests/test_finance_match_controls.py, src/core/tests/test_finance_signoffs.py, src/core/tests/test_form_review.py, src/core/tests/test_epic104_bounded_ai_invariants.py, src/core/pyproject.toml, src/core/README.md, src/api/src/zava_forward/api/server.py, src/api/tests/test_finance_match_api.py, src/api/tests/test_grant_lifecycle_api.py, src/api/pyproject.toml, and .github/workflows/src-ci.yml.
* Decisions, dependencies, and acceptance criteria considered: Confirmed caller decision that `AutomatedFinanceAuthorityRefusedError` subclasses `ValueError`, mapping missing prompt filenames (`funding_packs.py`, `routers/finance_grants.py`) to actual modules (`forms.py`, `form_review.py`, `form_export.py`, `store.py`, `api/server.py`), preserving `PermissionError` / `AuthorityGateError` on human staff RBAC/independence/grant-designation paths (`#94`, `#95`), keeping `src/core` package-dependency isolation (`ALLOWED = {"core"}`), and passing focused `src/core` and targeted `src/api` checks without pushing.
* Assessment boundary: Single-pass verification of the candidate plan and phase details against supplied research, repository source/test contracts, `pyproject.toml` lint/type configuration, and `.github/workflows/src-ci.yml`. Live Azure WORM/Monitor behavior and epic-wide stabilization checkpoint `#440` are outside this task's boundary.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
|------------------------------------------|----------|---------------------|
| Caller Req 1 / Q1-Q3 (`C1`-`C15` module mapping) | Covered | Missing filenames `funding_packs.py` and `routers/finance_grants.py` are accurately mapped to `forms.py`, `form_review.py`, `form_export.py`, `store.py`, and `src/api/src/zava_forward/api/server.py`. |
| FR-1 (`AutomatedFinanceAuthorityRefusedError(ValueError)`) | Covered | Structured attributes (`operation`, `actor_kind`, `reason`, `rule="RULE-010"`, `code="automated_finance_authority_refused"`, `as_record()`) satisfy caller and HTTP `400` contracts, subject to full type annotations (`PC-003`). |
| FR-2 / P01-T02 (Guard across 4 operations and proposal-apply paths) | Partial | Core guard coverage is strong and preserves Entra (`identity_source="entra"`) and human `PermissionError` contracts, but `grant_action` pre-check risks touching `SqlStore` state if `_case()` is used (`PC-002`), `server.py:1871` strips extra JSON keys before `Store.funding_step`, and `grant_action(..., to="Submitted")` classification diverges between `P01-T01` and `P02-T01` (`PC-004`). |
| FR-3 / P01-T01 (`verify_no_automated_finance_authority`) | Partial | Cloning `store.data` breaks on `SqlStore` (`KeyError: 'cases'`) (`PC-002`), and importing `zava_forward.agents` or `zava_forward.orchestrator` inside `src/core` violates `test_dependency_rule.py` and isolated `src-core` CI (`PC-001`). |
| FR-4 / P02-T02 (`src/core/README.md` documentation) | Covered | Concise `#93` invariant documentation without `.copilot-tracking/` references aligns with `src/core/README.md` conventions. |
| NFR-1 (`#94`, `#95`, `#104` regression compatibility) | Covered | Human-shaped unregistered, non-independent, and un-designated staff continue raising `PermissionError` / `AuthorityGateError` when `check_stored_human` is scoped strictly to `finance_action` (`PC-002`). |
| NFR-2 (Lint, formatting, and strict `mypy`) | Partial | New `finance.py` exports need explicit type annotations so strict-`mypy` `test_finance_no_automated_path_93.py` does not fail `disallow_untyped_calls`, and `ruff format --check .` is missing from planned validation (`PC-003`). |
| NFR-3 (Atomicity and zero partial writes) | Partial | Pre-`_finance_operation` guard placement prevents writes, provided `grant_action` pending-state inspection uses read-only `cases.get` rather than `_case()` (`PC-002`). |
| P02-T01 (`src/core/tests/test_finance_no_automated_path_93.py`) | Partial | Plan text includes HTTP `App` in `src/core/tests/test_finance_no_automated_path_93.py`, which violates `src/core/tests/test_dependency_rule.py` and fails in `src-core` CI (`deps=""`) (`PC-001`). |

## Verdict

* Verdict: Revise
* Rationale: The architectural approach and `PermissionError` vs `AutomatedFinanceAuthorityRefusedError(ValueError)` boundary are well-grounded in codebase evidence, but four substantive implementation blockers (`PC-001` through `PC-004`) would cause deterministic test or CI failures (`test_dependency_rule.py` AST import failure, `SqlStore` `KeyError: 'cases'` and `_touch` mutation, strict `mypy` `[no-untyped-call]` / `ruff format --check` failures, and `/funding` body stripping plus `to="Submitted"` operation mismatch) unless corrected in the plan and phase details before implementation. All four findings are direct planner corrections requiring no user input.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: `src/core` dependency-rule and isolated-CI breach from planned HTTP `App` and sibling-package imports

* Related IDs: FR-3, NFR-1, NFR-2, P01-T01, P02-T01
* Evidence: src/core/tests/test_dependency_rule.py, .github/workflows/src-ci.yml, src/core/tests/test_funding_automation_boundary.py, .copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md, .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md
* Concern: `src/core/tests/test_dependency_rule.py` (`ALLOWED = {"core"}`) AST-parses every `.py` file under `src/core/src/` and `src/core/tests/` and fails if any `import` or `from ... import` references `zava_forward.api`, `zava_forward.agents`, `zava_forward.orchestrator`, or `zava_forward.importer`. Moreover, `.github/workflows/src-ci.yml` runs the `src-core` matrix job with `deps: ""` (`pip install -e ".[dev]"` inside `src/core` only), where `zava-forward-api`, `zava-forward-agents`, and `zava-forward-orchestrator` are not installed. However, the Plan (Executive Summary, Test Ownership and Change Bounds, and `P02-T01`) states that `src/core/tests/test_finance_no_automated_path_93.py` exercises HTTP `App` / HTTP API routes (contradicting Phase Details `P02-T01`), and Phase Details `P01-T01` instructs `verify_no_automated_finance_authority` in `finance.py` to inspect `zava_forward.agents` and `zava_forward.orchestrator` "when importable".
* Impact: Any static import of `zava_forward.api`, `zava_forward.agents`, or `zava_forward.orchestrator` in `finance.py` or `test_finance_no_automated_path_93.py` immediately fails `test_dependency_rule.py`, `mypy`, and `src-core` CI; runtime `importlib` imports of sibling packages are unexercised in `src-core` CI (`deps=""`) and risk module-import side effects.
* Smallest useful change: Update Plan (`Executive Summary`, `Test Ownership and Change Bounds`, `P02-T01`) and Phase Details (`P01-T01`, `P02-T01`) to forbid importing `zava_forward.{api,agents,orchestrator,importer}` inside `src/core`. Specify AST-based source inspection (matching `src/core/tests/test_funding_automation_boundary.py`) over installed `zava_forward.core` automation modules (`ai*.py`, `assistants.py`, `workflows.py`, `coordinator.py`) plus sibling `src/agents/src` and `src/orchestrator/src` paths when present in a repository checkout, and verify HTTP API error mapping via the targeted `src/api` test run rather than importing `App` into `src/core/tests/test_finance_no_automated_path_93.py`.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Revised `.copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md` and `.copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md` removing HTTP `App` / non-`core` imports from `src/core` files and specifying AST-only module-boundary checks compatible with `test_dependency_rule.py` and standalone `src/core` test execution.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: `SqlStore` incompatibility in `verify_no_automated_finance_authority(store)` cloning, `grant_action` pre-check lookup, and `validate_sql` scoping

* Related IDs: FR-2, FR-3, NFR-1, NFR-3, P01-T01, P01-T02, P02-T01
* Evidence: src/core/src/zava_forward/core/sqlstore.py, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/finance.py, src/core/tests/test_grant_lifecycle_controls.py, .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md
* Concern: Three `SqlStore` execution details in `P01-T01` and `P01-T02` are unsafe as written: (1) `P01-T01` item 3 builds a disposable JSON `Store` by "cloning `store.data` if `store` is passed", and `P02-T01` calls `verify_no_automated_finance_authority(self.store)` on `SqlStore`; however, `SqlStore.__init__` sets `self.data = dict(staff=[], recommendations=[])` with no `"cases"` key, so passing that dict into `Store(seed)` raises `KeyError: 'cases'` at `store.py:106` (and an arbitrary caller store may lack prepared budget/invoice/grant/form fixtures ready for all four probes); (2) `P01-T02` instructs `GrantMixin.grant_action` to inspect `pending["to"]` before `_finance_operation`, where calling `self._case(case_id)` invokes `self._touch(case_id)` (`sqlstore.py:1062`), mutating thread-local `SqlStore` touched state and raising `KeyError` on unknown `case_id` before `AutomatedFinanceAuthorityRefusedError`; and (3) `_finance_operation` sets `self.local.finance_validation` for `finance_action`, `grant_action`, and `funding_step` alike, so `validate_sql` must only set `check_stored_human=True` when `context.get("check_stored_human")` was set by `finance_action` (preserving `PermissionError` in `test_grant_lifecycle_controls.py:165`).
* Impact: `verify_no_automated_finance_authority(sql_store)` crashes with `KeyError: 'cases'`, refused `grant_approve` calls dirty `SqlStore` thread-local state or leak `KeyError`, and unscoped `validate_sql` stored-human checks risk regressing `#95` SQL grant tests.
* Smallest useful change: Revise `P01-T01` and `P01-T02` so that: (1) `verify_no_automated_finance_authority(store=None)` snapshots any caller-supplied `Store` or `SqlStore` via `_sync()` + `store.cases` / audit state solely to assert zero caller mutation while always executing its live 4-operation probes on a self-contained disposable synthetic `Store` fixture in `TemporaryDirectory`; (2) `GrantMixin.grant_action` resolves `pending["to"]` read-only via `self.cases.get(case_id)` (after `self._sync()` under `self.lock` when `hasattr(self, "_sync")`, never `self._case(case_id)`); and (3) `_finance_operation` accepts/records `check_stored_human: bool = False` in `context` (enabled only by `finance_action`) for `validate_sql`.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated `P01-T01` and `P01-T02` in `.copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md` specifying self-contained disposable probe fixture construction, backend-safe caller non-mutation checks for both `Store` and `SqlStore`, read-only `self.cases.get(case_id)` pending lookup, and `context["check_stored_human"]` scoping in `_finance_operation` / `validate_sql`.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-003 -->
### PC-003 [High]: Strict `mypy` `disallow_untyped_calls` annotations and `ruff format --check` CI gate missing from `P01`/`P02`

* Related IDs: NFR-2, Acceptance Criteria, P01-T01, P02-T01, P02-T02
* Evidence: src/core/pyproject.toml, .github/workflows/src-ci.yml, src/core/tests/test_epic104_bounded_ai_invariants.py, .copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md, .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md
* Concern: First, `src/core/pyproject.toml` sets `strict = true` (`disallow_untyped_calls = true`) globally and is excluded from the plan's modified files, so `src/core/tests/test_finance_no_automated_path_93.py` runs under full `strict = true`. Even though `zava_forward.core.finance` has `ignore_errors = true`, `mypy` still rejects calls from `test_finance_no_automated_path_93.py` to `AutomatedFinanceAuthorityRefusedError`, `.as_record()`, `classify_finance_operation`, `guard_no_automated_finance_authority`, or `verify_no_automated_finance_authority` with `[no-untyped-call]` unless all new `finance.py` definitions carry complete parameter and return type annotations (and untyped `Store`/`SqlStore`/`Assistants` fixtures are wrapped as `Any`, matching `test_epic104_bounded_ai_invariants.py`). Second, `.github/workflows/src-ci.yml` (`Lint` step) runs `ruff check . && ruff format --check .`; neither `src/zava_forward/core/form_review.py` nor `tests/test_finance_no_automated_path_93.py` is excluded from `ruff format`, yet the plan and phase details omit `python3 -m ruff format --check .`.
* Impact: Code that passes `ruff check` and untyped helper calls in unit tests will fail `python3 -m mypy` (`[no-untyped-call]`) or hosted `src-core` CI (`ruff format --check .`).
* Smallest useful change: Require complete type annotations on every new class, method, and function added to `finance.py` in `P01-T01`, specify `Any`-typed store/helper wrappers in `P02-T01`, and include `python3 -m ruff format --check .` alongside `python3 -m ruff check` in `NFR-2`, `Acceptance Criteria`, and `P01`/`P02` validation expectations.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated `.copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md` and `.copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md` requiring typed public signatures on new `finance.py` symbols and `python3 -m ruff format --check .` in `src/core` validation commands.
* Decision route: direct planner correction

<!-- rpi:critique id=PC-004 -->
### PC-004 [Medium]: `POST /api/cases/{cid}/funding` drops proposal-apply keys before `Store.funding_step`, and `P01-T01` vs `P02-T01` conflict on `grant_action(..., to="Submitted")` operation mapping

* Related IDs: FR-1, FR-2, P01-T01, P01-T02, P02-T01
* Evidence: src/api/src/zava_forward/api/server.py, src/core/src/zava_forward/core/store.py, src/core/src/zava_forward/core/grants.py, src/core/tests/test_funding_automation_boundary.py, .copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md, .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md
* Concern: Two operation-boundary mismatches exist between the plan and phase details: (1) whereas `/finance`, `/grant`, and `/form-reviews` forward the full request `body` dict to core, `src/api/src/zava_forward/api/server.py:1871` calls `s.funding_step(u, cid, body.get("action"), body.get("text", ""))`, silently stripping AI proposal-apply keys (`proposal_id`, `auto_apply`, `ai_proposal`, `envelope`) sent over HTTP before `Store.funding_step` sees them; and (2) in `P01-T01`, `classify_finance_operation` maps `grant_action` with `to in ("Claimable", "Submitted", "Accepted")` to `"certify_claim"` (matching `GRANT_FLOW`, where `Claimable -> Submitted` is eligibility-verified claim submission after `Award`, while `funding_step("submit")` and `grant_open` / `to == "Opportunity"` cover bid/opportunity stage), yet `P02-T01` places `grant_action(..., grant_propose/grant_approve to="Submitted")` under both `submit_bid` and `certify_claim`, causing per-operation `.as_record()["operation"]` assertions to conflict.
* Impact: HTTP proposal-apply payloads targeting `/api/cases/{cid}/funding` lose their proposal metadata before reaching `funding_step`, and `P02-T01` operation-matrix assertions will contradict `P01-T01`'s classifier for `to="Submitted"`.
* Smallest useful change: Reconcile `P01-T01` and `P02-T01` so `submit_bid` asserts `err.operation == "submit_bid"` on `funding_step(..., "submit")`, `grant_open` / `to == "Opportunity"` / `action="submit_bid"`, and `form_review.action(..., "submit_bid")`, while `grant_action(..., to="Submitted")` from `Claimable` is asserted under `certify_claim`; and either add the one-line `s.funding_step(u, cid, body.get("action"), body.get("text", ""), body=body)` pass-through in `src/api/src/zava_forward/api/server.py:1871` (keeping `"s.funding_step("` intact for `test_funding_automation_boundary.py:76` and running `ruff check` + `PYTHONPATH=../core/src:../agents/src python3 -m mypy` in `src/api`) or explicitly record `src/api` unmodified bounds so HTTP `/funding` proposal-key stripping is not over-claimed.
* Action owner: planning parent (`rpi-plan`)
* Exact resolving evidence: Updated `.copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md` and `.copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md` with consistent `err.operation` mappings across `P01-T01`/`P02-T01` and an explicit disposition for `server.py:1871` `body` forwarding.
* Decision route: direct planner correction

## Strengths and Residual Risk

* Accurate architecture grounding: Research and plan correctly identify that `funding_packs.py` and `routers/finance_grants.py` do not exist and target the real core choke points (`_finance_operation`, `finance_action`, `grant_action`, `funding_step`, `form_review.action`) rather than adding dead shims.
* Regression-safe exception taxonomy: Keeping `AutomatedFinanceAuthorityRefusedError` as a `ValueError` subclass while preserving `PermissionError` / `AuthorityGateError` for registered/unregistered human staff RBAC, independence, and grant-designation checks (`#94`, `#95`) and avoiding false positives on Entra principals (`identity_source="entra"`, `auth_provider="trusted-proxy"`) and human `grant_open(..., source="SYN")` text citations is well designed.
* Accepted residual scope boundary: Epic `#93` remains open pending stabilization checkpoint `#440` and owner PR review/merge; local engineering proof covers `RULE-010` / `AC-035` in codebase controls and synthetic fixtures without claiming live production delegation.

## Questions or Blocking Evidence Gaps

* None. All four findings have unambiguous codebase evidence and direct planner resolutions.

## Limitations

* Critique is static and read-only against repository source, test suites, `pyproject.toml`, and `.github/workflows/src-ci.yml`; runtime execution of the new suite occurs during `rpi-implement` after the plan revisions above are applied.

## Recommended Next Action

* Highest-impact finding: PC-001
* Action owner: planning parent (`rpi-plan`)
* Smallest next action: Directly revise `.copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md` and `.copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md` in one pass to resolve `PC-001` through `PC-004`, record their disposition in `Critique Disposition`, and finalize planning readiness for `rpi-implement`.
* User response required: no
