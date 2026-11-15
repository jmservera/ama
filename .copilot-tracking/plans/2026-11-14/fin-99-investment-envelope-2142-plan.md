<!-- markdownlint-disable-file -->
# RPI Plan: Issue #99 Investment Envelope, Liquidity and Downside Tolerance Controls

## Task Metadata

* Task ID: fin-99-investment-envelope-2142
* Task slug: fin-99-investment-envelope-2142
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/fin-99-investment-envelope-2142-plan-critique.md

## Executive Summary

This plan completes the locally verifiable `src/core` engineering controls for **Issue #99 (Investment envelope, liquidity and downside tolerance controls)** traced to BRD `BG-008`, `RULE-011`, `RULE-012`, `OD-12`, and `OD-15`. In `src/core/src/zava_forward/core/exposure_limits.py`, it adds optional human-approved **liquidity and covenant minimum headroom floor controls** and optional **annual plan ceiling (`annual_plan`)** alongside the existing investment envelope and six downside maximum tolerances, guarantees that zero company figures or approval attributes are ever defaulted or invented, enforces strict allowed-key sets across all control dictionaries, and closes contrarian validation bypasses (unvalidated raw `limits` dicts or non-dict `exposure` passed to `assess()`, negative finite ceiling observations, integer-float overflow in `_number()`, and malformed/compact ISO dates or conflicting attribution aliases). Every upper-ceiling breach, minimum-floor breach (including negative overdraft or underwater covenant deficits), missing record, stale approval, or incomparable observation emits a deterministic `pause_signal` (`paused=True`, `decision_required=True`, `automatic_cut=False`, naming the `restart_owner` when valid limits exist) so a human decision is required without automatically cutting or restarting live delivery.

### User Decisions and Requirements Highlights

* Deliver both locally verifiable Issue #99 acceptance criteria in `src/core`: envelope, liquidity/covenant headroom, and downside tolerances are recorded strictly as human-approved inputs (never invented), and any breach produces a pause signal for a human decision.
* Write all four `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`) in order across the full RPI loop on branch `feat/fin-99-investment-envelope-2142`.
* Verify in `src/core` using bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*99*.py' -v`, then commit cleanly with the required `Co-authored-by` trailer without pushing.

### What You May Not Know

* In this shared multi-worktree environment, `~/.local/lib/python3.12/site-packages` points `zava_forward.core` at `/home/azureuser/source/ama/src/core/src`. Using a PEP 420 namespace-safe, Ruff-clean worktree `src/` bootstrap in both `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py` ensures bare `unittest` discovery exercises this worktree's code regardless of test load order without modifying shared global site-packages.
* Liquidity and covenant headroom (`BG-008`, `RULE-011`, `OD-12`) are *minimum floor* limits where signed finite observations (including negative overdrafts or underwater headroom `< 0`) below `minimum` trigger `Breach`, whereas investment envelope, optional `annual_plan`, and the six `RULE-012` downside tolerances are *maximum ceiling* limits requiring non-negative finite observations (`observed > maximum` triggers `Breach`).
* Real Zava North Homes Board/Finance figures (`OD-12`, `OD-15`) remain external human governance inputs, so commit messages must use `Refs #99` rather than a closing keyword.

### Unresolved Decisions or Blockers

* None for local `src/core` delivery. External Board ratification of Zava North Homes' actual capital envelope, liquidity/covenant thresholds, and downside tolerances (`OD-12`, `OD-15`) remains an organizational prerequisite outside repository code.

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (research, plan, implement, review) for Issue #99 on branch `feat/fin-99-investment-envelope-2142` in `/home/azureuser/source/ama-demo-wt/feat-99-investment-envelope-2142` (source: user prompt).
* Deliver in `src/core` that envelope and tolerances (including liquidity/covenant headroom per Issue #99 and BRD `BG-008`, `RULE-011`, `RULE-012`, `OD-12`, `OD-15`) are recorded as human-approved inputs, never invented (source: user prompt, Issue #99).
* Deliver in `src/core` that a breach produces a deterministic pause signal for a human decision and never approves, accelerates, cuts, or restarts live activity (source: user prompt, Issue #99).
* Preserve untracked `src/core/tests/test_issue_99_acceptance.py` and expand focused tests without inventing company numbers (source: repo dirty-worktree safeguard and research `C8`).
* Write all four `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`), verify in `src/core` using `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*99*.py' -v`, commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`, and do not push (source: user prompt).

## Goals

* Ensure investment envelope, optional liquidity/covenant minimum headroom floors, and downside maximum tolerances exist only when supplied with complete, non-conflicting human approval attribution.
* Emit a structured, deterministic human-decision pause signal whenever any upper ceiling (`envelope` or `RULE-012` downside tolerance) or lower floor (`liquidity` or `covenant` headroom) is breached, held, stale, or incomparable.
* Guarantee worktree-local, side-effect-free verification under bare `mypy`, `ruff`, and `unittest discover -s tests -p 'test_*99*.py' -v`.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/exposure_limits.py`: additive `liquidity` / `covenant` minimum floor and optional `envelope["annual_plan"]` ceiling recording and assessment, strict `YYYY-MM-DD` ISO date/timestamp and alias-consistency checks in `_approval()`, strict allowed-key checking across all input dicts, overflow-safe `_number()`, canonical `limits` and non-dict `exposure` validation in `assess()`, and non-negative ceiling vs signed finite floor observation checks.
* `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py`: PEP 420 namespace-safe worktree-isolated acceptance and unit regression coverage for human-approved recording, refusal of unattributed/conflicting/malformed/unknown-key inputs, upper-ceiling breaches (`envelope`, `annual_plan`, `tolerances`), liquidity/covenant floor breaches (including negative deficits), forged-dict/negative-ceiling anti-bypass guards, and non-acceleration within limits.
* `src/core/README.md`: concise documentation of `exposure_limits` controls, approval boundaries, and test command.

### Non-Goals

* Inventing Zava North Homes company figures, Board minutes, or default thresholds (`OD-12`, `OD-15`).
* Changing `src/api`, web workbench screens, infrastructure, or shared `~/.local` Python site-packages.
* Automatically halting, cutting, resuming, or accelerating live retrofit case workflows.
* Pushing to remote or closing Issue #99.

## Functional Requirements

* `record_limits(approval, envelope, tolerances, *, liquidity=None)` and `load_limits(path)` shall record limits only when supplied with complete human approval metadata (`approved_by`/`approver`, valid `YYYY-MM-DD` ISO date or `YYYY-MM-DDTHH:MM...` timestamp `approved_at`/`approved_on`, `role`, `evidence_ref`, `restart_owner`) and strict allowed keys on every input dictionary, rejecting missing, blank, malformed, overflowed, unknown-key, or conflicting alias inputs with `LimitsError`.
  * Observable acceptance criteria: Calling `record_limits` or `load_limits` with any missing attribution field, malformed/compact/week ISO date or timestamp (such as `"2026-01-01T99:99:99"` or `"2026-W01-1"`), unknown control key, huge integer overflow in `_number`, or disagreeing `approved_by`/`approver` or `approved_at`/`approved_on` values raises `LimitsError`; `assess(None, ...)` returns `status="Held"` and `signal="Pause for human decision"` with empty `findings`.
* `record_limits` and `load_limits` shall optionally record human-approved `envelope["annual_plan"]` ceiling (`RULE-011` `AC-037`) and `liquidity` minimum headroom controls (`minimum`, `currency`, and optional paired `covenant_minimum` + `covenant_unit`) without inventing defaults or altering the 3-argument return shape when optional fields are omitted.
  * Observable acceptance criteria: Omitting `liquidity` and `annual_plan` preserves existing 3-argument behavior; supplying malformed, negative, non-finite, unattributed, or unknown-key `liquidity` or `annual_plan` inputs raises `LimitsError`; valid inputs are preserved on the returned record.
* `assess(limits, exposure, today=None)` shall re-validate `limits` structure (including top-level keys), guard non-dict `exposure`, reject negative or non-finite upper-ceiling observations as `"Unknown"`, evaluate signed finite minimum-floor observations (`liquidity`, `covenant` with explicit unit matching) so deficits `< minimum` (including `< 0`) report `"Breach"`, evaluate upper ceilings (`envelope`, optional `annual_plan`, `RULE-012` downside `tolerances`), and emit `signal="Pause for human decision"` plus `pause_signal` (`paused=True`, `decision_required=True`, `decision_owner=restart_owner`, `automatic_cut=False`) on any breach or unknown, while never approving acceleration when within limits.
  * Observable acceptance criteria: Envelope ceiling breach, `annual_plan` breach, downside tolerance ceiling breach, liquidity minimum floor breach (positive or negative available balance), and covenant headroom floor breach each return `status="Breach"`, `signal="Pause for human decision"`, `pause_signal["paused"] is True`, `pause_signal["decision_owner"] == restart_owner`, and `pause_signal["automatic_cut"] is False`; forged raw `limits` dicts return `status="Held"`; negative upper-ceiling or non-dict `exposure` observations return `status="Unknown"`; within-limits exposure returns `signal="No pause signal"` with `"not approval to accelerate"` in `reason`.

## Non-Functional Requirements

* Static type safety, lint cleanliness, formatting compliance, and worktree-local test isolation in `src/core`.
  * Objective threshold or evaluation condition: Zero `mypy --strict` errors across all 308+ `src/core` files, zero `ruff check .` diagnostics, zero `ruff format --check .` diffs, and 100% pass rate on `test_*99*.py` and `test_exposure_limits.py` against this worktree's `exposure_limits.py`.
  * Operating condition or verification approach, if needed: Run `cd /home/azureuser/source/ama-demo-wt/feat-99-investment-envelope-2142/src/core && python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*99*.py' -v` without modifying `~/.local`.
  * Observable acceptance criteria: All four verification commands exit `0` and an assertion in `test_issue_99_acceptance.py` confirms `limits.__file__` resolves inside this worktree's `src/core/src`.

## Acceptance Criteria

* Envelope, optional liquidity/covenant headroom floors, and downside tolerances are recorded strictly from attributed human-approved inputs with zero invented company defaults; missing, malformed, or conflicting attribution is refused (`LimitsError`) and unrecorded/forged/stale limits return `Held` with a pause signal.
* Breaches of the investment envelope, any `RULE-012` downside tolerance ceiling, or any recorded liquidity/covenant minimum floor return `status="Breach"`, `signal="Pause for human decision"`, escalation action text, and `pause_signal` (`paused=True`, `decision_required=True`, `decision_owner=restart_owner`, `automatic_cut=False`), while within-limits assessments explicitly state they are not approval to accelerate.
* Test ownership and scope lock: canonical test targets are `src/core/tests/test_issue_99_acceptance.py` and `src/core/tests/test_exposure_limits.py` (no generated test targets; test removals: `none`; maximum new test methods added: `<= 12` focused semantic and boundary regression tests).
* Bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*99*.py' -v` pass in `src/core`, all four `.copilot-tracking/` artifacts exist, the branch is committed cleanly with the `Co-authored-by` trailer, not pushed, and `git status --short` is empty.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/fin-99-investment-envelope-2142-plan.md                                                               |
| Phase details                    | .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md                                                    |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/fin-99-investment-envelope-2142-plan-critique.md (`Revise`; `PC-001`..`PC-004` applied directly) |
| Relevant research                | .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-research.md                                                        |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-changes.md is created by implementation as its evidence record      |
| Planning execution and readiness | Complete and implementation-ready (`ready`); all single-pass critique findings resolved                                                  |
| Continuation context             | Confirmed automatic RPI Agent continuation to `rpi-implement`                                                                            |

## Sources

* .copilot-tracking/research/2026-11-14/fin-99-investment-envelope-2142-research.md: Codebase evidence `C1`-`C8` covering BRD rules, `exposure_limits.py` gaps, contrarian bypass vectors, and worktree `sys.path` isolation.
* docs/brds/agentic-retrofit-programme-brd.md: Upstream requirements `BG-008`, `RULE-011`, `RULE-012`, `OD-12`, and `OD-15`.
* src/core/src/zava_forward/core/exposure_limits.py: Existing core limits and pause-signal implementation.
* src/core/tests/test_issue_99_acceptance.py: Existing untracked Issue #99 acceptance test file in worktree.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden `exposure_limits` approval, liquidity/covenant floor, and breach pause controls

* Intent: Deliver complete human-approved envelope, liquidity/covenant minimum headroom, and downside tolerance recording and breach pause-signal assessment without breaking existing callers.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden `_approval`, `record_limits`, and `load_limits` with optional liquidity/covenant floors

* Requirement and evidence: Issue #99 AC1; BRD `BG-008`, `RULE-011`, `RULE-012`, `OD-12`, `OD-15`; Research `C1`-`C4`, `C6`.
* Expected result: Strict ISO date/timestamp validation and alias consistency in `_approval`, plus optional `liquidity` (`minimum`, `currency`, optional paired `covenant_minimum` + `covenant_unit`) in `record_limits` and `load_limits` with zero invented defaults and 100% 3-arg compatibility.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Harden `assess` with canonical limits validation, non-negative observation checks, and floor breach pause signals

* Requirement and evidence: Issue #99 AC1 & AC2; BRD `BG-008`, `RULE-011`, `RULE-012`; Research `C1`, `C2`, `C5`, `C6`.
* Expected result: `assess` re-validates raw `limits` dicts (returning `Held` on invalid/unattributed dicts), marks negative finite observations as `Unknown`, evaluates recorded `liquidity` and `covenant` minimum floors alongside upper ceilings, and emits `pause_signal` (`automatic_cut=False`, naming `restart_owner`) on every breach/unknown while preserving existing upper-breach wording.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Expand worktree-isolated Issue #99 acceptance tests, unit regressions, and `src/core` documentation

* Intent: Prove both Issue #99 acceptance criteria and contrarian edge cases locally in `src/core` under bare verification commands and document the module contract.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Isolate worktree imports and expand `test_issue_99_acceptance.py` and `test_exposure_limits.py`

* Requirement and evidence: Issue #99 AC1 & AC2; Research `C4`, `C5`, `C8`.
* Expected result: `test_issue_99_acceptance.py` prepends worktree `src/`, verifies module origin inside this worktree, and covers approved envelope/liquidity/covenant/tolerance recording, unattributed/conflicting/malformed refusal, ceiling and floor breach pause signals, forged-dict/negative-observation anti-bypass behavior, and `load_limits` JSON round-trip; `test_exposure_limits.py` covers complementary unit cases.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Document `exposure_limits` controls and boundaries in `src/core/README.md` and run verification gate

* Requirement and evidence: Repo documentation and focused-tier validation rules; Research `C3`, `C6`, `C7`, `C8`.
* Expected result: `src/core/README.md` documents `exposure_limits` human-approval, liquidity/covenant floor, downside ceiling, and non-decision pause-signal boundaries; bare `mypy`, `ruff check .`, `ruff format --check .`, `unittest discover -s tests -p 'test_*99*.py' -v`, and `PYTHONPATH=src:tests python3 -m unittest tests/test_exposure_limits.py -v` all exit `0`.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-14/fin-99-investment-envelope-2142-phase-details.md

## Dependencies

* Python 3.12 toolchain (`mypy`, `ruff`, `unittest`) installed in the environment: required to run the bare `src/core` verification suite.
* Backward-compatible `record_limits(approval, envelope, tolerances)` 3-argument contract: required by `src/core/src/zava_forward/core/finance.py` and `src/api/tests/test_finance_exposure_api.py`.

## Critique Disposition

Record the latest critique findings, their disposition, and any explicitly accepted residual risk. Keep this section outside user decisions and current planning synthesis.

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Single-pass critique `PC-001` [High] | Applied directly | Enforced strict `YYYY-MM-DD` date prefix + `T` timestamp `datetime.fromisoformat` parsing in `P01-T01` and aligned `test_exposure_limits.py` canonical-attribution test alongside dedicated conflicting-alias refusal tests in `P02-T01`. |
| Single-pass critique `PC-002` [High] | Applied directly | Kept `>= 0` for upper ceilings while accepting signed `_finite_observation` for `liquidity`/`covenant` minimum floors so negative deficits report `Breach`, required explicit `covenant_unit` on scalar covenant inputs, guarded non-dict `exposure`, and caught `OverflowError` in `_number()`. |
| Single-pass critique `PC-003` [Medium] | Applied directly | Added optional `envelope["annual_plan"]` ceiling validation/assessment (`RULE-011` `AC-037`) and strict allowed-key checking (`LimitsError`) across top-level `limits`, `approval`, `envelope`, `tolerances[name]`, and `liquidity`. |
| Single-pass critique `PC-004` [Medium] | Applied directly | Added PEP 420 namespace-safe, Ruff `E402`-compliant worktree `src/` bootstrap in both `test_issue_99_acceptance.py` and `test_exposure_limits.py`. |

## Follow-Up Items

* Surface `liquidity` / `covenant` minimum floor findings (`f.minimum ?? f.maximum` in `panels.js` `exposureNotice`) and `pause_signal.decision_owner` in the web Finance workbench UI (`src/api`): outside the `src/core`-scoped brief for this task; owned by a subsequent UI slice under Issue #99.

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/fin-99-investment-envelope-2142-changes.md
* Ready phase or task: Complete (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`, `P02-T02` verified; ready for `rpi-review`)
* Remaining provisional question or blocker: none
