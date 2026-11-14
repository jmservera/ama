---
title: "RPI Plan: nomination-challenge-130-2142"
description: "Implementation plan for Issue 130 locally verifiable nomination readiness, challenge retention, dependent re-review, and immediate hazard routing controls in src/core"
ms.date: 2026-11-14
---

## Task Metadata

* Task ID: nomination-challenge-130-2142
* Task slug: nomination-challenge-130-2142
* Planning status: ready
* Plan date: 2026-11-14
* Phase details: .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-14/nomination-challenge-130-2142-plan-critique.md

## Executive Summary

This plan delivers the four remaining locally verifiable acceptance criteria of Issue #130 (`FR-037`, `AC-065`, `RULE-005`) in `src/core` without changing SQL DDL or shared Python site-packages. It consolidates store-independent nomination and hazard-routing domain rules in `src/core/src/zava_forward/core/nomination_route.py`, wires `src/core/src/zava_forward/core/resident_decisions.py` to enforce pre-review route and named-owner readiness (including a `nomination_acknowledge` completion path for unready referrals), enables both residents and confirmed representatives (`Communicate` authority) to raise nomination corrections and formal challenges while retaining competing evidence, challenged reviewer, and outcome, triggers exact transitive dependent re-review without automatic acceptance or sanction, and routes emergency or unknown hazard concerns immediately to the independent hazard intake (#85) across all nomination and challenge actions. Finally, it isolates worktree module resolution in `src/core/tests/test_nomination_route.py` so bare `mypy`, `ruff`, and `unittest discover -s tests -p 'test_*nomination*.py' -v` verify both pure domain logic and `Store`/`SqlStore` persistence end-to-end.

### User Decisions and Requirements Highlights

* Deliver all four locally verifiable Issue #130 acceptance criteria in `src/core` on branch `feat/safety-130-nomination-challenge-2142`.
* Verify in `src/core` with bare `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*nomination*.py' -v`.
* Write all canonical `.copilot-tracking/` RPI artifacts (`research/`, `plans/`, `changes/`, `reviews/`), commit cleanly with `Refs #130` and the Copilot `Co-authored-by` trailer, and do not push.

### What You May Not Know

* Shared user-site `zava-forward-core` in `/home/azureuser/.local/lib/python3.12/site-packages` points to `/home/azureuser/source/ama/src/core/src`; `tests/test_nomination_route.py` must prepend this worktree's `src` directory and evict cached `zava_forward` namespace modules so bare `unittest discover` tests this worktree without mutating shared global packages.
* Existing regression assertions in `src/core/tests/test_resident_decisions.py` require `_res_nomination_correct` not to add case keys outside `nomination_records` and to keep the default `correction["re_review"]` key set unchanged when optional graph `dependencies` are omitted.

### Unresolved Decisions or Blockers

* None for `src/core` implementation. Governance decisions `OD-41` and `OD-42` and `src/api` authoring forms remain outside scope and keep Issue #130 open (`Refs #130`).

For current user input, see [User Decisions and Requirements](#user-decisions-and-requirements). The planner keeps the synthesized sections below current as evidence and user direction evolve.

## User Decisions and Requirements

* Run the full RPI loop in order (`research`, `plan`, `implement`, `review`) for Issue #130 on branch `feat/safety-130-nomination-challenge-2142` in worktree `/home/azureuser/source/ama-demo-wt/feat-130-nomination-challenge-2142`.
* Ensure each referral has an acknowledged route and a named owner before review (`FR-037`, `AC-065`).
* Ensure a resident or representative can raise a challenge or correction and that competing evidence, reviewer, and outcome are retained (`FR-037`, `FR-043`, `RULE-005`).
* Ensure a correction triggers re-review of dependent decisions without automatic acceptance or sanction (`FR-037`, `FR-052`, `AC-065`).
* Ensure emergency or hazard concerns route to the independent hazard intake (#85) immediately, not through this queue (`FR-037`, `AC-065`).
* Write all four `.copilot-tracking/` artifacts (`research/`, `plans/`, `changes/`, `reviews/`).
* Verify in `src/core` using bare `python3 -m mypy && python3 -m ruff check . && python3 -m ruff format --check . && python3 -m unittest discover -s tests -p 'test_*nomination*.py' -v`.
* Commit cleanly with `Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>` and do not push (`git status --short` must be empty).

## Goals

* Establish one strict-typed source of truth in `nomination_route.py` for pre-review readiness, immediate `#85` hazard routing, retained challenge/correction trails, and transitive dependent re-review calculation.
* Enforce those domain rules consistently across `Store` (JSON) and `SqlStore` (SQLite) resident actions in `resident_decisions.py` without SQL schema changes or regressions.
* Prove all four acceptance criteria under bare `mypy`, `ruff`, and `unittest discover -s tests -p 'test_*nomination*.py' -v` as well as existing resident, challenge, hazard, and queue suites.

## Scope and Non-Goals

### In Scope

* `src/core/src/zava_forward/core/nomination_route.py`: strict-typed domain rules, `HazardRouted` exception, whitespace/role-label readiness checks, complete `challenge_trail`, and version-bounded `re_review_set`.
* `src/core/src/zava_forward/core/resident_decisions.py`: integration of `nomination_route` across `nomination_record`, `nomination_acknowledge`, `nomination_review`, `nomination_correct`, `challenge_open`, `_refuse_hazard`, `_raiser`, `nomination_follow_up`, and `followup_view`.
* `src/core/tests/test_nomination_route.py` and `src/core/tests/test_resident_decisions.py`: worktree-isolated bare `unittest discover` bootstrap plus unit and `Store`/`SqlStore` integration coverage across all four acceptance criteria.

### Non-Goals

* Modifying `sqlstore.py` or `mssqlstore.py` DDL/migrations.
* Modifying `src/api` UI panels or claiming ratification of `OD-41` or `OD-42`.
* Running `pip install -e .` into shared user site-packages or pushing commits to `origin`.

## Functional Requirements

* Pre-review route and named-owner readiness (`FR-037`, `AC-065`):
  * Observable acceptance criteria: `missing_before_review` rejects missing, whitespace-only, or role-label-only owners, blank acknowledgement references, and blank non-digital routes; `_res_nomination_review` refuses review until all three exist with a known staff owner; `nomination_acknowledge` records named owner, staff acknowledgement (`delivery="Not verified by this system"`), staffed non-digital route, and `next_update` on unready referrals so subsequent independent review succeeds.
* Resident and representative challenge or correction with retained trail (`FR-037`, `FR-043`, `RULE-005`):
  * Observable acceptance criteria: both `nomination_correct` and `challenge_open` accept `raised_by` in `("Resident", "Representative", "Officer")` and validate confirmed in-date `Communicate` representative authority (with whitespace-trimmed `representative_ref` across case measures); original referral, competing evidence versions, raiser identity, linked challenge, challenged reviewer, and review outcomes remain intact and visible in `challenge_trail` and `followup_view`.
* Dependent decision re-review without automatic acceptance or sanction (`FR-037`, `FR-052`, `AC-065`):
  * Observable acceptance criteria: `nomination_correct` marks prior nomination reviews (`record_version <= expected_version`) stale with `stale_from_version`, computes transitive dependent decisions via `nomination_route.re_review_set` when `dependencies` are supplied while preserving unrelated decisions and prior versions, keeps default `re_review` shape compatible with existing callers when `dependencies` are omitted, and leaves `automatic_acceptance=False`, `automatic_sanction=False`, priority ranking, and resident consent unchanged.
* Immediate routing of emergency or hazard concerns to `#85` (`FR-037`, `AC-065`):
  * Observable acceptance criteria: `nomination_record` (required `hazard_concern`) and `nomination_acknowledge`, `nomination_review`, `nomination_correct`, and `challenge_open` (optional `hazard_concern`, fail-closed when supplied and not `False`, including `None`) immediately raise `HazardRouted` pointing to `#85` (`/api/cases/{case_id}/hazard-raise` / `raise_hazard`) with `queue_item_created=False`, creating zero nomination/challenge records, queue items, or audit mutations.

## Non-Functional Requirements

* Static type safety and lint cleanliness:
  * Objective threshold or evaluation condition: zero errors from `python3 -m mypy`, `python3 -m ruff check .`, and `python3 -m ruff format --check .` in `src/core`.
  * Operating condition or verification approach, if needed: `nomination_route.py` and `test_nomination_route.py` checked under full `mypy` `strict = true`.
  * Observable acceptance criteria: all three commands exit `0` from `src/core`.
* Worktree-isolated bare test execution and store parity:
  * Objective threshold or evaluation condition: bare `python3 -m unittest discover -s tests -p 'test_*nomination*.py' -v` loads modules from `<worktree>/src/core/src` without `PYTHONPATH` or global editable-install changes, and passes on both `Store` and `SqlStore`.
  * Operating condition or verification approach, if needed: assert `Path(module.__file__).resolve().is_relative_to(worktree_src)` inside the test suite and run targeted regression suites (`test_resident_decisions`, `test_challenges`, `test_hazard_referral`, `test_taskqueues`).
  * Observable acceptance criteria: all targeted unit and store-backed tests pass with zero regressions.

## Acceptance Criteria

* Reviewing any referral lacking a named owner, staff-recorded acknowledgement, or staffed non-digital route fails closed; completing them via `nomination_acknowledge` allows an independent human reviewer to record `nomination_review`.
* Both a resident and a confirmed representative (`Communicate` authority) can raise `nomination_correct` and `challenge_open`; unconfirmed, revoked, expired, or wrong-task representatives are rejected; original account, competing evidence, reviewer, and outcome remain retained in `Store` and `SqlStore`.
* Recording a correction stales prior nomination reviews and exact transitive dependent decisions (`ChallengeRegister`) while leaving unrelated decisions, prior versions, case priority, and resident consent unchanged, with `automatic_acceptance=False` and `automatic_sanction=False`.
* Supplying `hazard_concern=True` or unknown `hazard_concern=None` (or non-boolean truthy flags) across nomination and challenge actions raises `HazardRouted` (`issue="#85"`, `route="independent_hazard_intake"`, `queue_item_created=False`) immediately with zero queue items created, while `store.raise_hazard` handles the hazard independently.
* Bare `mypy`, `ruff check .`, `ruff format --check .`, and `unittest discover -s tests -p 'test_*nomination*.py' -v` all exit `0` in `src/core`.

## Implementation Context Record

| Context item                     | Current artifact or record                                                                                                               |
|----------------------------------|------------------------------------------------------------------------------------------------------------------------------------------|
| Plan                             | .copilot-tracking/plans/2026-11-14/nomination-challenge-130-2142-plan.md                                                                 |
| Phase details                    | .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md                                                      |
| Latest critique                  | .copilot-tracking/reviews/plans/2026-11-14/nomination-challenge-130-2142-plan-critique.md with Revise disposition (PC-001..PC-005 resolved directly) |
| Relevant research                | .copilot-tracking/research/2026-11-14/nomination-challenge-130-2142-research.md                                                          |
| Changes-record role              | .copilot-tracking/changes/2026-11-14/nomination-challenge-130-2142-changes.md is created by implementation as its evidence record        |
| Planning execution and readiness | Complete and Ready for implementation                                                                                                    |
| Continuation context             | Confirmed automatic RPI Agent session transitions directly to rpi-implement                                                              |

## Sources

* `.copilot-tracking/research/2026-11-14/nomination-challenge-130-2142-research.md`: `C1`..`C12` codebase findings and `D1`..`D5` contrarian discoveries.
* `docs/brd/business-requirements.md` (`FR-037`, `AC-065`, `RULE-005`, `OD-41`, `OD-42`): authority, non-inference, representative, and hazard separation rules.
* `docs/prd/product-requirements.md` (`FR-037`, `FR-043`, `FR-052`, `AC-071`): nomination, challenge, and transitive dependent re-review specifications.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Core Nomination, Challenge, Re-Review, and Hazard Domain Controls

* Intent: Harden `nomination_route.py` and integrate it cleanly across `resident_decisions.py` for both `Store` and `SqlStore`.
* Dependencies: None.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden `nomination_route.py` strict-typed rules and unified `HazardRouted`

* Requirement and evidence: `FR-037`, `AC-065`, `RULE-005`; research `C1`, `C4`, `C8`, `C11`.
* Expected result: `nomination_route.py` exports `HAZARD_ROUTING_MESSAGE`, `HAZARD_INTAKE`, `HazardRouted`, whitespace- and role-label-safe `missing_before_review` and `require_ready_for_review`, case-aware `hazard_routing`, complete `challenge_trail`, and version-bounded `re_review_set` passing `mypy --strict`.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Integrate `nomination_route` across `resident_decisions.py` actions and read views

* Requirement and evidence: `FR-037`, `FR-043`, `FR-052`, `AC-065`; research `C2`..`C10`.
* Expected result: `resident_decisions.py` re-exports `HazardRouted`/`HAZARD_ROUTING_MESSAGE`, fixes `_refuse_hazard` for explicit `None` across `nomination_record`, `nomination_acknowledge`, `nomination_review`, `nomination_correct`, and `challenge_open`, adds `nomination_acknowledge`, fixes `_raiser` whitespace and multi-measure lookup and enables it on `challenge_open`, supports optional `dependencies` in `nomination_correct` via `nomination_route.re_review_set` without breaking existing `re_review` shape, and unifies `nomination_follow_up`/`followup_view` with `nomination_route`.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Worktree-Isolated Bare Test Suite and Verification Gate

* Intent: Prove all four acceptance criteria across pure helpers, `Store`, and `SqlStore` under bare `unittest discover`, `mypy`, and `ruff`, plus adjacent regression suites.
* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Bootstrap worktree `sys.path` and expand `test_nomination_route.py` and `test_resident_decisions.py`

* Requirement and evidence: User bare verification command; research `C9`, `C11`, `C12`.
* Expected result: `tests/test_nomination_route.py` resolves `<worktree>/src/core/src` cleanly under bare `unittest discover`, passes `mypy --strict` and `ruff`, tests pure `nomination_route` helpers and full JSON `Store` + SQLite `SqlStore` flows across all four acceptance criteria (max 12 focused test methods in `test_nomination_route.py` and max 3 focused additions in `test_resident_decisions.py`, 0 test removals), and all targeted regression tests pass.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-14/nomination-challenge-130-2142-phase-details.md

## Dependencies

* `src/core/src/zava_forward/core/challenges.py` (`ChallengeRegister`, `Node`, `stamp_assurance`): existing transitive graph and non-detriment assurance helper reused without modification.
* `src/core/src/zava_forward/core/workflows.py` (`raise_hazard`): existing `#85` independent hazard intake verified alongside `HazardRouted`.

## Critique Disposition

| Critique run and finding | Disposition | Plan response or residual risk |
|--------------------------|-------------|--------------------------------|
| Run 1 `PC-001` [High]    | resolved    | Updated `P01-T01`, `P01-T02`, and `P02-T01` so `Node` versions stay `str` (`f"v{expected_version}"` / normalized string tokens), `re_review_set` parses integer suffixes (`"v1"` or `"1"`) before bounding `record_version <= cutoff`, `re_review_set` retains `"review_versions"` alongside `"dependent_review_versions"`, and `_res_nomination_correct` validates optional `dependencies` fail-closed with `ValueError`. |
| Run 1 `PC-002` [High]    | resolved    | Updated `P01-T02` and `P02-T01` so `authority_for` remains unchanged for measure-scoped bindings while `_raiser` strips `representative_ref` and checks the latest authority entry per measure against all `authority_for` invariants (`Communicate`), and `delete_resident_records` scrubs `representative_ref` from `affected_challenges`. |
| Run 1 `PC-003` [Medium]  | resolved    | Updated `P02` and `P02-T01` so `tests/test_nomination_route.py` evicts `zava_forward*` from `sys.modules` only when an imported module `__file__` or namespace `__path__` resolves outside `<worktree>/src`, preserving class identities in multi-file runs. |
| Run 1 `PC-004` [Medium]  | resolved    | Updated `P01-T01`, `P01-T02`, and `P02-T01` so `missing_before_review` compares `owner["name"]` and `owner.get("role")` with stripped `.casefold()`, `_res_nomination_acknowledge` checks `_owner_rights` when an existing owner is `"Known"`, enforces pre-review readiness completion while incrementing `record["version"]` under `challenges.protected_snapshot`, and `SqlStore` tests persist unready fixtures via `reseed`/`save` before replay. |
| Run 1 `PC-005` [Low]     | resolved    | Updated `P01-T01` and `P01-T02` to retain `"endpoint"` on `HAZARD_INTAKE` and re-export `HAZARD_INTAKE_ROUTE` in `resident_decisions.py`, keep string `"original_account"` alongside `"original"` metadata in `challenge_trail`, and pass `case.get("affected_challenges", ())` from `followup_view` so live resolved challenge reviewer/outcome details appear in `challenge_trail`. |

## Follow-Up Items

* Author interactive UI forms in `src/api` for `nomination_record`, `nomination_acknowledge`, `nomination_correct`, and `nomination_review` (outside `src/core` scope; owner: web/API slice for `#130`).
* Ratify `OD-41` and `OD-42` operational policy thresholds with housing operations and compliance leads (outside engineering scope; owner: governance).

## Handoff

* Implementation artifact: .copilot-tracking/changes/2026-11-14/nomination-challenge-130-2142-changes.md
* Ready phase or task: All planned phases and tasks completed (`P01`, `P01-T01`, `P01-T02`, `P02`, `P02-T01`); ready for `rpi-review`
* Remaining provisional question or blocker: None
