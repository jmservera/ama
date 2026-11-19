<!-- markdownlint-disable-file -->
# Review: Issue #93 Deterministic No-Automated-Finance-Authority Invariant

## Scope and Evidence

* Task ID: issue-93-finance-no-auto-path
* Review date: 2026-11-15
* Review scope: Full task (`P01` and `P02`: `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Issue `#93` engineering acceptance criterion (`No automated path submits a bid, approves match funding, certifies a claim or records cash`, `RULE-010`, `AC-035`), functional/non-functional requirements (`FR-1`..`FR-4`, `NFR-1`..`NFR-3`), critique dispositions (`PC-001`..`PC-004`), package isolation (`ALLOWED = {"core"}`), `SqlStore` compatibility, type/lint gates, and repository commit/tracking constraints
* Plan: .copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md
* Phase details: .copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-15/finance-93-no-auto-path-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-15/finance-93-no-auto-path-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md; git diff across `src/core` and `src/api`; focused `ruff`, `mypy`, `unittest`, and `rename-zava-tests.py` verification runs

## Opening Review State

* Interpreted review goal: Independently verify that `P01` and `P02` completely and conformantly enforce and prove that no automated, system, agent, worker, orchestrator, unauthenticated, non-human, or AI proposal-apply path can submit a bid, approve match funding, certify a claim, or record cash, with all critique dispositions (`PC-001`..`PC-004`) honored and zero regressions.
* Review scope: Full task (`P01` and `P02`)
* Evidence readiness: Ready; plan, phase details, single-pass plan critique, reconciled changes record, research synthesis, and clean working-tree implementation diff are all present and current.
* Acceptance basis: User prompt items 1-6, `FR-1`..`FR-4`, `NFR-1`..`NFR-3`, acceptance criteria, test ownership and change bounds, and `PC-001`..`PC-004` critique dispositions in `.copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md`.
* First comparison boundary: Plan-to-change reconciliation across `P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`, and `## Follow-Up Items`, limited strictly to read-only inspection of repository files and tracking artifacts.
* Active read-only boundaries: Write authority restricted solely to `.copilot-tracking/reviews/logs/2026-11-15/finance-93-no-auto-path-review.md` (plus parent state-contract persistence); zero source, test, plan, detail, critique, or changes-log edits permitted during Review.
* Initial blockers: None.

## Execution Status

* Execution status: Complete
* Review execution evidence: Completed single-pass read-only review on 2026-11-15 across `.copilot-tracking/plans/2026-11-15/finance-93-no-auto-path-plan.md`, `.copilot-tracking/details/2026-11-15/finance-93-no-auto-path-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-15/finance-93-no-auto-path-plan-critique.md`, `.copilot-tracking/changes/2026-11-15/finance-93-no-auto-path-changes.md`, `.copilot-tracking/research/2026-11-15/finance-93-no-auto-path-research.md`, and the exact working-tree diff across `src/core` and `src/api`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | Core Deterministic Guard and Invariant Verifier (`P01`, `P01-T01`) | Reconciled | `PROTECTED_FINANCE_OPERATIONS`, `AutomatedFinanceAuthorityRefusedError(ValueError)`, `classify_finance_operation`, `guard_no_automated_finance_authority`, `validate_sql`, `_finance_operation`, and `verify_no_automated_finance_authority` match `FR-1`..`FR-3` and `PC-001`..`PC-004`. |
| `P01`, `P01-T02` | Operation-Aware Entry Guards Across Grants, Funding Applications, Form Packs, and API (`P01`, `P01-T02`) | Reconciled | `grants.py`, `store.py`, `form_review.py`, and `api/server.py` enforce pre-mutation automated/proposal refusal while preserving human `PermissionError` / `AuthorityGateError` (`#94`, `#95`) and `"s.funding_step("`. |
| `P02`, `P02-T01` | End-to-End `#93` Invariant Suite and Core Documentation (`P02`, `P02-T01`, `P02-T02`) | Reconciled | `src/core/tests/test_finance_no_automated_path_93.py` proves all four operations across `Store`, `SqlStore`, `Assistants`, `Store.review_ai`, `form_review`, AST-scanned `src/agents` & `src/orchestrator`, and fail-closed tamper checks using only `zava_forward.core` imports. |
| `P02`, `P02-T02` | End-to-End `#93` Invariant Suite and Core Documentation (`P02`, `P02-T01`, `P02-T02`) | Reconciled | `src/core/README.md` documents the `#93` invariant check and test command; focused `ruff`, `mypy`, `unittest`, and `rename-zava-tests.py` checks all passed. |
| `Follow-Up Items` | Epic `#93` stabilization checkpoint `#440` and post-merge criterion tick-off | Reconciled | Kept outside active `P01`/`P02` completion claims and mirrored in `.copilot-tracking/changes/2026-11-15/finance-93-no-auto-path-changes.md`. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/finance.py` | Added structured `AutomatedFinanceAuthorityRefusedError(ValueError)`, `PROTECTED_FINANCE_OPERATIONS`, `classify_finance_operation`, `guard_no_automated_finance_authority`, `validate_sql` writer-lock guard, `finance_action`-scoped stored non-human check, and disposable-probe + AST `verify_no_automated_finance_authority` while keeping untouched legacy lines unchanged (`+982/-5`). | `finance.py` diff and runtime probe verification (`probes_executed == 44`, zero caller `Store`/`SqlStore` mutation). | `ruff check .`, `ruff format --check .`, `mypy` (354 files, 0 issues), `test_finance_no_automated_path_93.py` | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/grants.py`, `src/core/src/zava_forward/core/store.py`, `src/core/src/zava_forward/core/form_review.py`, `src/api/src/zava_forward/api/server.py` | Wired operation-classified `guard_no_automated_finance_authority` into `GrantMixin.grant_action` (read-only `cases.get` pending lookup), `Store.funding_step` (`body=None`), and `form_review.action`, plus `body=body` pass-through in `api/server.py` `/api/cases/{cid}/funding`. | Surgical diffs (`+31/-1`, `+12/-1`, `+4/-1`, `+1/-1`) preserving `#94`/`#95` human RBAC and `"s.funding_step("` source contract. | `src/core` 215-test regression batch + `src/api` `ruff check`, `mypy` (297 files), `test_finance_match_api.py`, `test_grant_lifecycle_api.py` | Reconciled |
| `P02-T01` | `src/core/tests/test_finance_no_automated_path_93.py` | Added 9 end-to-end invariant tests covering 16 non-human/automated/agent/orchestrator/unauthenticated/proposal-caller vectors x 4 operations on both `Store` and `SqlStore`, `funding_draft` + `funding-evidence` proposal acceptance and apply refusal, designated-human positive controls, stored non-human staff refusal, AST scan of `src/agents` & `src/orchestrator`, and verifier tamper tests. | New test module (`1` file added, matching plan bound `1`; `ALLOWED = {"core"}` verified). | `PYTHONPATH=src:tests python3 -m unittest tests/test_finance_no_automated_path_93.py -q` (9 tests OK) + `test_dependency_rule.py` | Reconciled |
| `P02-T02` | `src/core/README.md` | Documented `PROTECTED_FINANCE_OPERATIONS`, `AutomatedFinanceAuthorityRefusedError`, `guard_no_automated_finance_authority`, `verify_no_automated_finance_authority`, and focused unittest command with zero `.copilot-tracking/` references. | `src/core/README.md` diff (`+35`) and `grep` verification across `src/`. | `tools/rename-zava-tests.py` (25 tests OK) and `src/core` lint/type/unit checks | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| `P01-T01` (`src/core/src/zava_forward/core/finance.py`) | Local judgment only: restored untouched legacy lines of `finance.py` from `HEAD` after an explicit `ruff format` call bypassed `[tool.ruff.format].exclude` in `src/core/pyproject.toml` (ADR 0006). | `git diff` inspection and `src/core/pyproject.toml` `[tool.ruff.format].exclude`; no user decision needed because plan scope and behavior were unchanged. | Recorded under `## Implementation-Time Plan and Detail Updates` in `.copilot-tracking/changes/2026-11-15/finance-93-no-auto-path-changes.md` and re-verified with `ruff format --check .` and `mypy`. | Not needed; `PC-001`..`PC-004` and Ready planning state preserved. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four single-pass critique findings (`PC-001` package isolation, `PC-002` `SqlStore` safety and `grant_action` stored-authority compatibility, `PC-003` PEP 484 strict `mypy` + `ruff format --check .`, and `PC-004` `api/server.py` `/funding` `body=body` forwarding + `to="Submitted"` mapping) were resolved in the plan and verified in the delivered code and tests.
* Material revisions: None during implementation; no requirements, scope, architecture, acceptance criteria, or evidence boundaries diverged from the approved plan.
* Dependent-work pause assessment: `P01` (`P01-T01`, `P01-T02`) completed before `P02` (`P02-T01`, `P02-T02`); no premature execution or bypassed pause occurred.
* Justification assessment: Fully supported by deterministic static and runtime evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Epic `#93` stabilization checkpoint `#440` and post-merge criterion tick-off | Issue `#93` remains an open multi-slice epic gated on stabilization checkpoint `#440` and owner PR review/merge before ticking GitHub criteria, and this session leaves a frozen unpushed `HEAD`. | Owner / backlog coordinator after `PR #1641` and `feat/finance-93-no-auto-path` review and merge | Open distinct follow-up route (not an implementation defect). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material or blocking findings (`RV-xxx`: none). All functional requirements (`FR-1`..`FR-4`), non-functional requirements (`NFR-1`..`NFR-3`), acceptance criteria, test/file bounds, and critique dispositions (`PC-001`..`PC-004`) are satisfied.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| None | none | No defect, decision gap, or evidence gap requires re-entry into `rpi-implement`, `rpi-plan`, or `rpi-research`. | Full conformance across `P01` and `P02`. |

Later implementation of a routed finding does not require another Review.

## Residual Work

* Distinct non-blocking follow-up candidates outside active `#93` slice acceptance: optional direct HTTP-handler automated-refusal assertions in `src/api/tests/`, future extraction of finance/grant/funding routes out of `src/api/src/zava_forward/api/server.py`, and epic `#93` stabilization checkpoint `#440` + post-merge criterion tick-off.

## Blockers and Remaining Work

* Blockers: None.
* Remaining active work: None (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` (exit 0). |
| `python3 -m ruff format --check .` | `src/core` | Passed | `301 files already formatted` (exit 0), honoring `[tool.ruff.format].exclude`. |
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 354 source files` (exit 0). |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_finance_no_automated_path_93.py tests/test_dependency_rule.py tests/test_funding_automation_boundary.py tests/test_grant_lifecycle_controls.py tests/test_finance_match_controls.py tests/test_finance_signoffs.py tests/test_form_review.py tests/test_epic104_bounded_ai_invariants.py -q` | `src/core` | Passed | `Ran 215 tests in 57.401s OK (skipped=45)`. |
| Full `src/core` unittest discovery + `.pth` CLI verification | `src/core` | Passed | All 3,580+ in-process tests passed; 3 CLI subprocess test modules passed in `.pth` venv (`Ran 54 tests in 14.228s OK`); `test_device_registry_azure` requires optional `[iothub]` extra covered by hosted CI. |
| `python3 tools/rename-zava-tests.py` | Repository root | Passed | `Ran 25 tests in 14.129s OK`. |
| `python3 -m ruff check . && PYTHONPATH=../core/src:../agents/src python3 -m mypy` | `src/api` | Passed | `All checks passed!` and `Success: no issues found in 297 source files` (exit 0). |
| `PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest tests/test_finance_match_api.py tests/test_grant_lifecycle_api.py -q` | `src/api` | Passed | `Ran 3 tests in 3.503s OK (skipped=1)` (plus 44 finance/grant/form/dependency API tests passed in full check). |

## Outcome

* Outcome: Conformant
* Outcome rationale: Every planned phase and task (`P01-T01`, `P01-T02`, `P02-T01`, `P02-T02`) is complete, reconciled, and backed by passing lint, format, strict `mypy`, unit, AST-boundary, and API regression evidence proving that no automated, non-human, unauthenticated, or AI proposal-apply path can submit a bid, approve match funding, certify a claim, or record cash (`RULE-010`, `AC-035`).

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | None |
| Decision gap or invalid assumption | none | None |
| Material evidence gap | none | None |
| Non-blocking residual work | distinct follow-up | Post-Review follow-up selection (optional HTTP-level automated-refusal tests, `api/server.py` finance/grants router extraction, and epic `#93` checkpoint `#440` post-merge closure) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Focused tier passed across `src/core` (`ruff check`, `ruff format --check`, `mypy`, 215 focused + full in-process + `.pth` CLI tests), `tools/rename-zava-tests.py` (25 tests), and `src/api` (`ruff check`, `mypy`, targeted finance/grant API tests); hosted CI unobserved locally because HEAD remains unpushed per caller instruction.
* Blockers: None.
