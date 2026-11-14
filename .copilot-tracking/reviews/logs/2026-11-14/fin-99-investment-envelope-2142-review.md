<!-- markdownlint-disable-file -->
# Review: Issue #99 Investment Envelope, Liquidity and Downside Tolerance Controls

## Scope and Evidence

* Task ID: fin-99-investment-envelope-2142
* Review date: 2026-11-14
* Review scope: Full task (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02`)
* Assessed boundary: Locally verifiable `src/core` acceptance criteria for Issue #99 (`BG-008`, `RULE-011`, `RULE-012`, `OD-12`, `OD-15`) covering human-approved recording of investment envelope, optional `annual_plan`, optional `liquidity`/`covenant` minimum headroom floors, and six downside tolerances without invented defaults, deterministic human-decision `pause_signal` emission (`automatic_cut=False`), worktree-isolated test verification under bare `mypy`/`ruff`/`unittest`, and `src/core/README.md` documentation.
* Plan: .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-plan.md
* Phase details: .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/fin-99-investment-envelope-2142-plan-critique.md
* Changes: .copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-changes.md
* Other evidence considered: .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-research.md, `src/core/src/zava_forward/core/exposure_limits.py`, `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py`, `src/core/README.md`, and downstream compatibility verification on `src/api/tests/test_finance_exposure_*.py`.

## Opening Review State

* Interpreted review goal: Verify once, from committed-ready workspace evidence, that the delivered `src/core` implementation satisfies all planned Issue #99 functional, non-functional, critique-disposition, governance, and verification requirements without defects or invented company thresholds.
* Review scope: Full task (`P01` and `P02`)
* Evidence readiness: Ready; research, plan, phase details, single-pass plan critique, and changes record are present and reconciled.
* Acceptance basis: User prompt acceptance criteria, Issue #99 (`BG-008`, `RULE-011`, `RULE-012`, `OD-12`, `OD-15`), approved plan acceptance criteria, and dispositions of `PC-001` through `PC-004`.
* First comparison boundary: Compare `P01-T01` and `P01-T02` in `src/core/src/zava_forward/core/exposure_limits.py` against approved functional requirements and critique dispositions `PC-001`..`PC-003`.
* Active read-only boundaries: This review creates only `.copilot-tracking/reviews/logs/2026-11-14/fin-99-investment-envelope-2142-review.md` and mutates no source or prior RPI artifacts.
* Initial blockers: none

## Execution Status

* Execution status: Complete
* Review execution evidence: Full task boundary reviewed on 2026-11-14 across `exposure_limits.py`, `test_issue_99_acceptance.py`, `test_exposure_limits.py`, `src/core/README.md`, all prior `.copilot-tracking/` artifacts, and local verification outputs.

## Plan-to-Change Reconciliation

| Current plan scope | Descriptive changes-record summary | Current-state reconciliation | Gap or rationale |
|--------------------|------------------------------------|------------------------------|------------------|
| `P01`, `P01-T01` | Human-approved envelope, annual plan, and liquidity/covenant floor recording | Reconciled | `[x]` in plan, `completed` in phase details, evidenced in `exposure_limits.py`. |
| `P01`, `P01-T02` | Canonical `assess` validation and ceiling/floor breach pause-signal emission | Reconciled | `[x]` in plan, `completed` in phase details, evidenced in `exposure_limits.py`. |
| `P02`, `P02-T01`, `P02-T02` | Worktree-isolated Issue #99 acceptance tests, unit regressions, and documentation | Reconciled | `[x]` in plan, `completed` in phase details, `8` new tests (`<= 12` cap, `0` removed), `src/core/README.md` updated. |
| `Follow-Up Items` | Web Finance workbench UI floor-finding display (`src/api`) | Reconciled | Kept outside active `src/core` completion claims and mirrored in changes record. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Validation | Assessment |
|----------------|-------|----------------------|---------------------|------------|------------|
| `P01-T01` | `src/core/src/zava_forward/core/exposure_limits.py` | Enforced strict allowed-key validation, overflow-safe `_number()`, `YYYY-MM-DD` date + `T` timestamp validation, alias-agreement checks (`approved_by`/`approver`, `approved_at`/`approved_on`), optional `envelope["annual_plan"]`, and optional `liquidity`/`covenant` minimum floor recording with zero invented defaults. | Code diff and passing unit/acceptance tests for attribution, round-trip `load_limits`, and malformed/conflicting input refusal. | Passed (`mypy`, `ruff`, `unittest`) | Reconciled |
| `P01-T02` | `src/core/src/zava_forward/core/exposure_limits.py` | Re-validated `limits` inside `assess()`, normalized non-dict `exposure`, enforced `_non_negative_finite_observation` on upper ceilings and signed `_finite_observation` on minimum floors (`< minimum` -> `Breach`), required explicit `covenant_unit`, preserved `"Over approved limit: ..."` for upper-only breaches, and emitted `pause_signal` (`automatic_cut=False`). | Code diff and passing breach/unknown/held/within-limits tests (including negative cash/covenant deficits and downstream `src/api` tests). | Passed (`mypy`, `ruff`, `unittest`) | Reconciled |
| `P02-T01` | `src/core/tests/test_issue_99_acceptance.py`, `src/core/tests/test_exposure_limits.py` | Added PEP 420 namespace-safe, Ruff `E402`-clean worktree `src/` bootstrap in both test files, verified module origin inside this worktree, retained all 24 existing tests (`0` removed), and added `8` focused semantic/boundary tests (`<= 12` budget). | `11` acceptance tests in `test_issue_99_acceptance.py` and `21` unit/integration tests in `test_exposure_limits.py` all pass. | Passed (`mypy`, `ruff`, `unittest`) | Reconciled |
| `P02-T02` | `src/core/README.md` | Added concise `## Investment envelope, liquidity and downside tolerance controls (#99)` section documenting human-approval inputs, ceiling/floor checks, `pause_signal` non-decision semantics, and `OD-12`/`OD-15` boundaries. | Diff review and Markdown formatting check in `src/core/README.md` with zero `.copilot-tracking/` leaks. | Passed (`git diff`, bare verification suite) | Reconciled |

## Implementation-Time Plan and Detail Update Assessment

| Affected area or marker | What changed and why | Triggering evidence and user decision | Reconciliation performed | Planning and critique state | Assessment |
|-------------------------|----------------------|---------------------------------------|--------------------------|-----------------------------|------------|
| None during implementation | No implementation-time plan revisions were needed after pre-implementation reconciliation of `PC-001`..`PC-004`. | Single-pass critique resolved before entering Implement; no new user decision required. | Plan markers, phase details statuses, handoff prose, and changes record reconciled at close of Implement. | Plan `ready`; `PC-001`..`PC-004` applied directly. | Reconciled |

## Critique and Material Revision Assessment

* Latest critique dispositions: All four critique findings (`PC-001` [High], `PC-002` [High], `PC-003` [Medium], `PC-004` [Medium]) are explicitly recorded in `## Critique Disposition` and verified in the delivered code and tests.
* Material revisions: None required a divergent user decision; every critique adjustment strengthened compliance with confirmed user requirements and existing test contracts.
* Dependent-work pause assessment: `P01` completed and passed static checks before `P02` finalized test and documentation verification; no premature resumption occurred.
* Justification assessment: Supported by concrete codebase and test execution evidence.

## Plan Follow-Up Assessment

| Follow-up item | Why outside immediate scope | Owner or next action | Assessment and route |
|----------------|-----------------------------|----------------------|----------------------|
| Surface `liquidity` / `covenant` minimum floor findings (`f.minimum ?? f.maximum` in `panels.js` `exposureNotice`) and `pause_signal.decision_owner` in the web Finance workbench UI (`src/api`) | User task explicitly scoped engineering delivery and verification to `src/core`. | Subsequent `src/api` Finance workbench UI slice under Issue #99. | Distinct non-blocking follow-up route (`follow_up`). |
| Record actual Zava North Homes Board-ratified capital envelope, liquidity/covenant thresholds, and downside tolerances (`OD-12`, `OD-15`) | Organizational governance inputs owned by Zava North Homes Board and Finance Lead; repository code must never invent company figures. | Zava North Homes Board / Finance Lead outside repository code (`Refs #99`). | External human-governance dependency (`follow_up`). |

Unresolved plan follow-up items remain distinct follow-up work. Do not treat them as defects or add them to active `Pxx` or `Pxx-Txx` implementation, completion, or acceptance scope.

## Findings

No material or minor defects (`RV-xxx`) were found within the assessed `src/core` task boundary.

## Defects

* none

## Routed Findings

| Finding | Destination | Owner or next action | Reason for route |
|---------|-------------|----------------------|------------------|
| none | none | No `rpi-implement`, `rpi-plan`, or `rpi-research` rework required for the delivered `src/core` scope. | Conformant delivery |

Later implementation of a routed finding does not require another Review.

## Residual Work

* `src/api` Finance workbench UI update (`panels.js` `exposureNotice` rendering `f.minimum ?? f.maximum` for floor findings and surfacing `pause_signal.decision_owner`): distinct follow-up work outside `src/core`.
* External human ratification of Zava North Homes `OD-12` and `OD-15` limits by Board and Finance Lead: distinct governance prerequisite (`Refs #99`, preventing issue closure from engineering tests alone).

## Blockers and Remaining Work

* Blockers: none for `src/core` task completion (external `OD-12`/`OD-15` Board ratification blocks full organizational closure of Issue #99, so commits must use `Refs #99`).
* Remaining active work: none

## Validation Evidence

| Command | Scope | Status | Summary |
|---------|-------|--------|---------|
| `python3 -m mypy` | `src/core` | Passed | `Success: no issues found in 308 source files` |
| `python3 -m ruff check .` | `src/core` | Passed | `All checks passed!` |
| `python3 -m ruff format --check .` | `src/core` | Passed | `255 files already formatted` |
| `python3 -m unittest discover -s tests -p 'test_*99*.py' -v` | `src/core` | Passed | `Ran 11 tests in 0.003s — OK` (verified worktree `exposure_limits.py` origin) |
| `python3 -m unittest tests/test_exposure_limits.py tests/test_issue_99_acceptance.py -v` | `src/core` | Passed | `Ran 32 tests in 0.015s — OK` (verified alphabetical multi-file bare discovery) |
| `PYTHONPATH=../core/src:../core/tests:../agents/src:../agents/tests:src:tests python3 -m unittest discover -s tests -p 'test_finance_exposure_*.py' -v` | `src/api` (read-only compatibility check) | Passed | `Ran 7 tests in 4.385s — OK` |

## Outcome

* Outcome: Conformant
* Outcome rationale: Both locally verifiable Issue #99 acceptance criteria in `src/core` are completely implemented, documented, and verified under bare `mypy`, `ruff check`, `ruff format --check`, and `unittest discover -s tests -p 'test_*99*.py' -v`, with all four critique items (`PC-001`..`PC-004`) resolved, zero downstream `src/api` regressions, and zero invented company thresholds.

## Closeout Routing Record

<!-- Persist outcome and route facts only. The rpi-review reference owns rendered closeout prose. -->

| Finding class | Destination | Owner or next action |
|---------------|-------------|----------------------|
| Implementation defect | none | none |
| Decision gap or invalid assumption | none | none |
| Material evidence gap | none | none |
| Non-blocking residual work | distinct follow-up | Subsequent `src/api` UI slice (`panels.js` floor finding display) and external Board `OD-12`/`OD-15` ratification |

* Execution status: Complete
* Outcome: Conformant
* Validation coverage: Bare `mypy` (308 files), `ruff check`, `ruff format --check` (255 files), `test_*99*.py` (11 tests), `test_exposure_limits.py` (21 tests), and downstream `src/api` exposure tests (7 tests) all passed.
* Blockers: none
