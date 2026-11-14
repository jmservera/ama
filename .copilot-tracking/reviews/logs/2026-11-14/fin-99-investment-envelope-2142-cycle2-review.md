<!-- markdownlint-disable-file -->
# Review: Cycle-2 Fix for Issue #99 / PR #1739 `sys.modules` Test Bootstrap

## Scope and Evidence

* Task ID: fin-99-investment-envelope-2142-cycle2
* Review date: 2026-11-14
* Review scope: Full task (`P01`: `P01-T01`, `P01-T02`)
* Assessed boundary: Module-import bootstrap in `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py`, `zava_forward.core.store` / `ConflictError` class-identity regression test, `src/core` static analysis (`mypy`, `ruff`), ordered multi-module and full-suite `unittest` validation, critique dispositions (`PC-001`..`PC-003`), and carried-forward plan follow-ups
* Plan: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-cycle2-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-cycle2-research.md, src/core/tests/test_issue_99_acceptance.py, src/core/tests/test_exposure_limits.py, git diff on `src/core/`

## Opening Review State

* Interpreted review goal: Verify once with direct repository and validation evidence that Cycle-2 eliminates bulk `zava_forward.*` `sys.modules` eviction across both Issue #99 test modules, preserves `zava_forward.core.store` / `ConflictError` identity across `unittest discover`, retains worktree-local `exposure_limits` resolution, and satisfies all `mypy`, `ruff`, and `unittest` gates without scope drift.
* Review scope: Full task (`P01`: `P01-T01`, `P01-T02`)
* Evidence readiness: Complete and reconciled across research, plan, phase details, single-pass plan critique, changes record, and source diff
* Acceptance basis: User prompt Requirements 1-4, synthesized Functional/Non-Functional Requirements and Acceptance Criteria in `.copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan.md`, and critique dispositions `PC-001`..`PC-003`
* First comparison boundary: Plan markers (`P01`, `P01-T01`, `P01-T02`) and test-scope lock against `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py`
* Active read-only boundaries: Read-only inspection of source, plan, details, critique, research, and changes artifacts; write access restricted exclusively to this canonical review record
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Full single-pass comparison executed on 2026-11-14 across `.copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan.md`, `.copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-cycle2-phase-details.md`, `.copilot-tracking/reviews/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan-critique.md`, `.copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-cycle2-changes.md`, `src/core/tests/test_issue_99_acceptance.py`, and `src/core/tests/test_exposure_limits.py`.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|---|---|---|---|
| `P01` / `P01-T01` | `P01-T01: Targeted exposure_limits Bootstrap and Store Identity Regression Test` | Reconciled | `[x]` checked in plan, `completed` in phase details, exact file changes and local typing judgment recorded in changes record. |
| `P01` / `P01-T02` | `P01-T02: Static Analysis, Multi-Module Ordered unittest, Bare Worktree Isolation, and Full src/core Discovery` | Reconciled | `[x]` checked in plan, `completed` in phase details, all six commands and exit `0` outputs recorded in changes record. |
| `Follow-Up Items` | `Blockers and Follow-Ups` | Reconciled | Both out-of-scope follow-ups (`src/api` Finance workbench UI rendering and external Board `OD-12`/`OD-15` ratification) remain outside active `P01` completion claims and are mirrored accurately. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|---|---|---|---|---|---|
| `P01-T01` | `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py` | Replaced bulk `zava_forward.*` `sys.modules` deletion loop in both files with `_ensure_local_exposure_limits()` and added `test_bootstrap_preserves_store_identity_and_evicts_only_foreign_module` (1 new test method `<= 2` max; `0` removals). | `grep "del sys.modules" src/core/tests` returns zero matches; `_ensure_local_exposure_limits()` leaves `sys.modules` untouched when `loaded is None` or inside `_CORE_SRC`, and evicts only `zava_forward.core.exposure_limits` plus `core_pkg.exposure_limits` when external. | `mypy`, `ruff check .`, `ruff format --check .`, 95-test ordered `unittest`, 33-test bare worktree `unittest` all passed. | Reconciled and conformant |
| `P01-T02` | `src/core` test and static-check suite | Verified static types, lint/formatting, CI reproduction order (`test_bulk_edits` -> `test_issue_99_acceptance` -> `test_exposure_limits` -> `test_taskqueues`), bare worktree isolation, and full `src/core` `unittest discover -s tests -q`. | All commands exited `0` with zero errors and zero failures. | `mypy` (308 files), `ruff` (255 files), ordered `unittest` (95 tests), bare `unittest` (33 tests), full `unittest discover` (exit `0`). | Reconciled and conformant |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|---|---|---|---|---|---|
| `P01-T01` local typing detail | Used `: Any` annotations (`store_before: Any`, `core_pkg: Any`) with direct attribute access (`store_before.ConflictError`, `core_pkg.exposure_limits`, `del core_pkg.exposure_limits`) rather than `getattr`/`setattr` with constant literal attribute names. | Ruff `B009`/`B010` forbid `getattr`/`setattr` with constant attribute strings while `mypy --strict` forbids untyped dynamic attributes on `ModuleType`; ordinary local implementation judgment, no user decision needed. | Documented in `.copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-cycle2-changes.md` under `P01-T01` and `Amendments and Divergences`. | Preserves `PC-002` intent (strict `mypy` + Ruff clean without `# type: ignore` or `# noqa` suppression); no plan revision or repeat critique needed. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All three single-pass critique findings (`PC-001` [High], `PC-002` [Medium], `PC-003` [Medium]) in `.copilot-tracking/reviews/plans/2026-11-14/fin-99-investment-envelope-2142-cycle2-plan-critique.md` have explicit dispositions in `## Critique Disposition` of the plan and were honored during implementation and review sequencing.
* Material revisions: None occurred during implementation.
* Dependent-work pause assessment: No dependent-work pause was triggered; `P01-T01` completed and passed targeted checks before `P01-T02` full-suite verification completed.
* Justification assessment: Fully supported by repository code, Python 3.12 PEP 420 import semantics, and passed tool outputs.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|---|---|---|---|
| Surface `liquidity` / `covenant` minimum floor findings (`f.minimum ?? f.maximum` in `panels.js` `exposureNotice`) and `pause_signal.decision_owner` in the web Finance workbench UI (`src/api`) | Cycle-1 and Cycle-2 are scoped strictly to `src/core` and its CI `src-core` test suite. | Separate `src/api` web UI follow-up task (with web design and browser harness checks). | Open distinct follow-up route (not a Cycle-2 defect). |
| Record actual Zava North Homes Board-ratified capital envelope, liquidity/covenant thresholds, and downside tolerances (`OD-12`, `OD-15`) | Requires external human governance approval by Zava North Homes Board and Finance Lead; agents must never fabricate company figures (`Refs #99`). | Zava North Homes Finance and Grants Lead / Board governance action outside repository code. | Open distinct governance follow-up route (`Refs #99`, never `Closes #99`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No defects, decision gaps, or material evidence gaps were identified in the Cycle-2 implementation boundary (`0` Critical, `0` High, `0` Medium, `0` Low findings).

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---|---|---|---|
| none | none | No corrective RPI stage required for `fin-99-investment-envelope-2142-cycle2` | All Cycle-2 requirements and validation checks are conformant |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `src/api` Finance workbench UI enhancement (`pause_signal.decision_owner` and `f.minimum ?? f.maximum` rendering in `panels.js`): distinct `src/api` follow-up item carried forward from Cycle-1.
* External Board ratification of Zava North Homes `OD-12` and `OD-15` financial envelope and tolerance values: external human governance prerequisite keeping PR #1739 linked via `Refs #99`.

## Blockers and Remaining Work

* Blockers: none for Cycle-2 `src/core` local commit. External Zava North Homes Board ratification of `OD-12` and `OD-15` remains an organizational prerequisite before Issue #99 itself can close (`Refs #99`).
* Remaining active work: none (`P01`, `P01-T01`, and `P01-T02` are complete).

## Validation Evidence

| Command | Scope | Status | Summary |
|---|---|---|---|
| `python3 -m mypy` | `src/core` (308 source & test files) | Passed | `Success: no issues found in 308 source files` (exit `0`). |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` (exit `0`). |
| `python3 -m ruff format --check .` | `src/core` (255 files) | Passed | `255 files already formatted` (exit `0`). |
| `PYTHONPATH=src:tests python3 -m unittest tests/test_bulk_edits.py tests/test_issue_99_acceptance.py tests/test_exposure_limits.py tests/test_taskqueues.py -q` | `src/core` multi-module CI load-order suite | Passed | `Ran 95 tests in 12.613s — OK` (exit `0`; confirms `test_bulk_edits` -> `test_issue_99_acceptance` -> `test_exposure_limits` -> `test_taskqueues` preserves `store` / `ConflictError` identity). |
| `python3 -m unittest tests/test_issue_99_acceptance.py tests/test_exposure_limits.py -q` | `src/core` bare worktree import isolation | Passed | `Ran 33 tests in 0.044s — OK` (exit `0`; confirms local `_CORE_SRC` resolution without `PYTHONPATH=src`). |
| `PYTHONPATH=src:tests python3 -m unittest discover -s tests -q` | Full `src/core` discovery suite | Passed | Completed with exit code `0` across all `src/core` test modules. |

## Outcome

* Outcome: Conformant
* Outcome rationale: Both `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py` replace bulk `zava_forward.*` `sys.modules` deletion with `_ensure_local_exposure_limits()`, preserving `zava_forward.core.store` and `ConflictError` identity across `unittest discover` while safely evicting only foreign `zava_forward.core.exposure_limits` entries (`sys.modules` + `zava_forward.core` attribute + cache invalidation). Focused regression coverage and all six static/unit test checks pass 100% within the approved scope.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---|---|---|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Optional `src/api` Finance UI follow-up (`panels.js` `decision_owner` + minimum floor wording) and external Board `OD-12`/`OD-15` ratification (`Refs #99`) |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: `mypy`, `ruff check`, `ruff format --check`, ordered 4-module `unittest`, bare 2-module `unittest`, and full `src/core` `unittest discover` all passed (`0` failures)
* Blockers: none for Cycle-2 `src/core` local commit (`OD-12`/`OD-15` Board ratification remains external to repository code under `Refs #99`)
