---
title: Progress dashboard correction4 independent plan critique
description: Single final-candidate assessment of lifecycle semantics and persisted regression planning
ms.date: 2026-10-29
---

## Metadata

* Task ID: 533-correction4.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction4-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/progress-dashboard-533-correction4-phase-details.md.
* Critique execution status: Complete.
* Assessment count: exactly one independent final-candidate critique.
* Branch: feat/progress-dashboard-533; continuing PR #540, Refs #533.

## Inputs and Criterion Boundary

* Assessed the supplied plan, phase details and matching research C1-C8, including the initial-event row and complete five-by-five transition table.
* Assessed the user counterexamples, event identity, conservative unknown handling, genuine duplicate preservation, persisted JSON/SQLite coverage, observable counters/archive behavior, compatibility, test ownership/removals/budgets and validation feasibility.
* Read relevant evidence in src/api/src/zava_forward/api/progress.py, src/api/tests/test_progress_dashboard.py, src/core/src/zava_forward/core/workflows.py, src/core/src/zava_forward/core/appointments.py, src/core/src/zava_forward/core/sqlstore.py, support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_flow_b.py, API/core package manifests, src/api/checks/progress_browser_check.py and component guidance.
* Read correction3 changes and original Review to distinguish previous blocked validation from this round's planned admission. Read required case-study and knowledge-base context.
* Current instructions authorize the full RPI correction and local commits, not push, force-push, Azure operations or publication. Rebase-first completion is supplied research evidence, not independently rerun.
* Assessment is a plan credibility review, not implementation acceptance. No heavy checks, browser execution, lock probe, dependency installation or remote operation was performed.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| User counterexamples; C1-C2; P01-T02 | Covered | Typed event replay before date/bool projection directly addresses false reopen and swallowed incomplete history. |
| C4-C6; research transition table | Covered for distinct evidence | Initial I only; A/C require open; R requires closed; T requires open without starting an episode. Repeated distinct T remains legal. |
| Exact duplicate and same-instant corroboration rules; P01-T01/T02 | Partial | Global unconditional instant/kind deduplication is not reconciled with ordered zero-day transitions; PC-001. |
| Five initial cells and 25 pair cells; P01-T01 | Covered | Independent literal outcomes, valid R/T prefixes, successive dates and final-state-consistent illegal cases are specified for each backend. |
| Persisted endpoint and archive assertions; P01-T01 | Partial | Reopening and exact results are required, but the backend-specific fixture write/readback mechanism needs specification; PC-002. |
| Compatibility and conservative unknown handling | Covered | Existing guards, UTC normalization, synthetic admission, ignored controlled advance, legacy recognized flags, output shape, access controls and read-only behavior remain explicit. |
| Test ownership, removals and budget | Covered | One canonical test file; no removals; at most four inherited methods and two local fixture helpers; no generated dataset. Findings can be resolved within that budget. |
| P02-T01 static checks | Covered | API/core mypy plus Ruff lint/format use existing configured scope and tools, worktree source/test paths and no new overrides. Existing manifest exemptions are not whole-repository strictness claims. |
| P02-T01 full units/browser and fallback | Covered with execution risk | One nonblocking admission holds the shared lock through setup and heavy checks; busy means existing-runtime targeted fallback and explicit unperformed validation, not success. |
| P02-T02 original Review and local closeout | Covered | Source candidate is committed before the single independent Review; original outcomes remain intact; no fix/re-review loop or publication is authorized. |

## Verdict

* Verdict: Revise.
* Rationale: the distinct-event transition table is credible and the validation constraints are feasible as an execution plan. The duplicate rule can nevertheless discard meaningful same-instant transitions, and SQLite matrix persistence needs an explicit fixture recipe and readback assertion. Both are direct planner corrections within confirmed user intent.
* Severity summary: 0 Critical, 1 High, 1 Medium, 0 Low.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Unconditional duplicate removal can erase same-instant intervening episodes

* Related IDs: research Q2 and Full Transition Table; Functional Requirements; duplicate/zero-day acceptance criteria; P01-T01; P01-T02.
* Evidence: research calls identical normalized instant/kind an "unconditional duplicate" and says the table applies after that deduplication. The plan repeats exact instant/kind deduplication while requiring stable same-instant source order and legal zero-day/multi-episode histories. Current history extraction preserves list order before the stable timestamp sort in src/api/src/zava_forward/api/progress.py. The generator and controlled workflow evidence establish that closure and reopening are meaningful opposing transitions, not interchangeable observations.
* Concern: the pair matrix deliberately uses successive dates, so it cannot detect loss caused by deduplication across an intervening transition at one instant. For example, place I before instant t and put A, R, A, R in that history order at t, with closed=False. These are legal ordered transitions under the proposed preconditions. Global instant/kind removal reduces them to A, R and returns a known history with one completed episode instead of two. Similarly, A/C corroboration at t must not suppress a closing event after an intervening R merely because an earlier closing event also occurred at t.
* Impact: a known result can silently undercount completed episodes, openings, reopenings and zero-day duration samples despite every distinct-date transition cell passing. This recreates the central failure mode of boolean deduplication under a different key.
* Smallest useful change: bound duplicate/corroboration suppression to evidence that does not cross an intervening lifecycle-changing transition. Specify ordered same-instant replay explicitly: preserve legal alternating close/reopen transitions; do not reduce an ambiguous sequence into a smaller known history. Retain true adjacent/redundant observations and timezone-equivalent duplicates. Add literal expected controls for I followed by A,R,A,R at t and for closing aliases separated by R at t, alongside the genuine duplicate controls.
* Action owner: planning parent, then P01 implementation owner.
* Exact resolving evidence: reconciled plan/details specify the intervening-transition boundary; persisted and reopened JSON/SQLite controls assert the complete lifecycle result and independently expected daily/weekly opened, closed, reopened, backlog and duration samples. Existing genuine duplicate controls remain green. No global membership rule may silently collapse the supplied alternating example.
* Decision route: direct planner correction. The user already requires preserved event kinds, no fabricated known history and genuine duplicate preservation; legal zero-day replay is already in this candidate. No significant/divergent user decision is required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The persisted matrix lacks the backend-specific fixture write and readback contract

* Related IDs: C3; persisted-regression acceptance criteria; P01-T01; two-helper test budget.
* Evidence: phase details require "save and reopen the actual store" without identifying how constructed histories reach each backend. SqlStore.save() in src/core/src/zava_forward/core/sqlstore.py:665 writes cases from its touched set, not every modified self.cases entry, and the outer lock exit performs recovery. The existing malformed persistence matrix in src/api/tests/test_progress_dashboard.py deliberately writes constructed SQLite case bodies directly before opening a fresh SqlStore; JSON uses Store.save(). That established fixture mechanism is relevant evidence, not a production persistence API change.
* Concern: a new helper that directly changes self.store.cases and calls save() can fail to persist the intended SQLite case or encounter normal controlled-mutation validation. Reopening alone does not demonstrate which raw fixture was retained. Endpoint assertions should be preceded by proof that the supplied event kinds, order, timestamps and final closed flag actually survived storage, particularly for legal controls that could otherwise resemble the baseline.
* Impact: the required two-backend coverage may be incomplete or misleading, or implementation may need an avoidable harness redesign under the fixed helper budget. This is a missing planning detail, not a demonstrated defect in code that has not yet been written.
* Smallest useful change: name the existing backend-specific fixture pattern in P01-T01: JSON save/reopen and test-only SQLite constructed-body injection/reopen, or fresh-store seeding of each complete constructed fixture. Do not weaken production validators. Require exact reopened payload equality for the lifecycle-bearing fields and closed flag before replay and report assertions. Use the existing two-helper allowance.
* Action owner: planning parent, then P01 test owner.
* Exact resolving evidence: phase details identify the fixture injection method, new-reader ownership/closure and raw roundtrip assertions. Both inherited matrix runs demonstrate that each of the 30 intended cell fixtures, plus duplicate/tie controls, was read from the persisted backend before lifecycle/dashboard/archive expectations were evaluated.
* Decision route: direct planner correction; no new dependency, schema, production bypass or significant/divergent user decision.

## Strengths and Residual Risk

* The supplied table correctly distinguishes repeated returns from reopening and forbids identification after a prior episode. Its independent literal expectations are preferable to deriving test outcomes from production logic.
* Explicit synthetic admission, known siblings and exact aggregate/archive assertions protect against a malformed case disappearing rather than becoming unknown.
* Four inherited methods can contain parameterized tables and positive controls without fragmenting ownership. No test removal or generated-data change is proposed.
* The one-attempt nonblocking lock and targeted fallback match current user direction. A busy result must leave full API/core discovery and browser validation explicitly incomplete, including in the original Review outcome; local lifecycle closeout is not acceptance.
* Existing /tmp/mv tools, authorized parent output paths and the shared lock are not parent filesystem blockers. This reviewer imposed no replacement paths or tool restrictions on the parent's authorized execution.
* Same-instant event identity remains intrinsically limited without stable event IDs. Conservative treatment must not become silent loss of ordered, otherwise valid transitions.

## Questions or Blocking Evidence Gaps

* No unresolved user question or decision-critical external research gap. Resolve PC-001 and PC-002 directly before implementation.
* Current availability of the heavy runtime/lock is intentionally not assessed. The plan already specifies an honest busy/missing-prerequisite outcome.

## Limitations

* No candidate implementation exists in this round; this assessment does not claim failing or passing new regressions.
* Producer semantics and existing harness/configuration were inspected, not executed. Prior correction outcomes are historical evidence only.
* Only this critique artifact was written. Plan, phase details, research, source and durable state were not edited.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: reconcile duplicate/corroboration boundaries and same-instant controls, specify the backend roundtrip recipe, then proceed through the authorized Implement and single independent Review.
* User response required: no.
* Do not repeat this critique. Preserve this Complete / Revise original and record dispositions in the parent-owned plan.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction4-plan.md | Assessed final-candidate plan |
| .copilot-tracking/details/2026-10-29/progress-dashboard-533-correction4-phase-details.md | Assessed phase details |
| .copilot-tracking/research/2026-10-29/progress-dashboard-533-correction4-research.md | Supplied evidence and transition table |
| .copilot-tracking/reviews/plans/2026-10-29/progress-dashboard-533-correction4-plan-critique.md | Original single-pass critique |

## Next Steps

The active planning parent applies both direct corrections without another critique, records their dispositions, and continues the already authorized RPI loop. No user action is required. Keep all commits local and preserve any validation blockers and original Review outcome.
