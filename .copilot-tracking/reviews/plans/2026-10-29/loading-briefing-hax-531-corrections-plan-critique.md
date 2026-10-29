---
title: Loading and briefing correction plan critique
description: Independent final-candidate assessment for task 531-corrections-2026-10-29
ms.date: 2026-10-29
---

## Metadata

* Task ID: 531-corrections-2026-10-29
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-corrections-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/loading-briefing-hax-531-corrections-phase-details.md
* Critique execution status: Complete
* Assessment: one independent final-candidate critique; no agents launched.

## Inputs and Criterion Boundary

* Caller requirements: four surgical corrections, each with a regression;
  source-first core/API units; existing browser/axe checks; nonblocking heavy
  lock for full suites and targeted-only validation on contention.
* Research: .copilot-tracking/research/2026-10-29/loading-briefing-hax-531-corrections-research.md,
  including C1-C6 and the recorded W1 guidance summary.
* Supplied evidence pointers inspected: the draft-review and queue-search
  sections of src/api/src/zava_forward/api/web/app.js;
  src/api/src/zava_forward/api/web/async-action.js;
  src/api/src/zava_forward/api/web/panels.js;
  the statement_sources implementation in src/core/src/zava_forward/core/ai_tasks.py;
  src/api/tests/test_loading_feedback.py; and the relevant existing assertions
  in src/api/checks/loading_briefing_browser_check.py.
* Decisions and dependencies: retain feat/loading-briefing-hax-531 and PR 538,
  reference issue 531 without closing language, preserve original evidence,
  make local-only commits, and perform one post-implementation independent
  Review. No push, Azure operations or publication are authorized.
* Boundary: assess proposed corrections, acceptance/test ownership, execution
  ordering and stated constraints. This is not implementation Review, a fresh
  web-guidelines audit, dependency verification or execution of any test suite.
  Repository context documents were consulted for standing constraints, not
  as additional technical research.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Cancel focus; C1; P01-T01 | Covered | Explicit choice/opener identity avoids relying on the focused textarea or disabled edit control. Browser acceptance covers ordinary edit/reject cancellation and unavailable-draft rejection without enabling stale edit. |
| Editable search; C2; P01-T01 | Covered | Null-control feedback avoids both disabling search and control-keyed deduplication. Retained sequence guard and reverse-response browser assertions cover overlapping debounced reads. |
| Busy snapshot; C3, C5; P01-T02 | Covered | Capture before task invocation matches synchronous actForm busy ownership. Helper regression specifies recoverable failure, finally cleanup, retry and absent/false restoration while retaining disable ownership. |
| Citation separation; C4; P01-T02 | Covered | Separator after relocated punctuation restores the whitespace split boundary. Exact statement-object assertions cover source association, sentence terminators, newlines and adjacent references without a parser rewrite. |
| Regression ownership; C6; P01/P02-T01 | Partial | Appropriate helper, core and browser owners are named, but failing-regression execution is ordered after runtime fixes: PC-001. |
| Source-first units and existing browser/axe; P02-T01 | Covered | Both unit components and the existing relevant browser suites are named. Nonblocking admission, no polling, targeted-only contention fallback and recorded skips are explicit. |
| Environment prerequisite; research readiness; P02-T01 | Covered with limitation | Requested interpreter is absent. Alternative interpreter version is recorded, but dependency/import readiness must still be checked before execution; it is not established by this critique. |
| Local persistence and independent Review; P02-T02 | Covered | Original outcomes remain immutable; commits stay local and the publication/human acceptance boundary remains separate. |
| Scenario pins and change budget | Covered | Pin updates are conditional on changing either pinned workbench input; extending the separate loading check does not itself require changing them. |

## Verdict

* Verdict: Revise
* Rationale: the four minimal corrections and regression owners are credible.
  One execution-order contradiction prevents following the planned
  before-fix regression reproduction as written. A direct planner correction
  resolves it without changing scope or requiring a user decision.
* Severity counts: Critical 0; High 0; Medium 1; Low 0.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Before-fix regression reproduction is scheduled after the fixes

* Related IDs: P01-T02, P02, P02-T01; C3-C5; helper/parser regression acceptance.
* Evidence: .copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-corrections-plan.md
  assigns runtime fixes and regression additions to P01, then makes P02
  dependent on P01. In
  .copilot-tracking/details/2026-10-29/loading-briefing-hax-531-corrections-phase-details.md,
  P02-T01 instead says, "First reproduce helper/parser failures with new
  regressions before runtime edits."
* Concern: completing P01 first removes the unfixed runtime on which P02 is
  supposed to demonstrate those regression failures. The ordered tasks cannot
  all be followed literally without an unplanned rollback or reconstruction.
* Impact: validation can show the corrected code passes without preserving
  the promised evidence that the new helper/parser regressions detect the
  original defects. Reconstructing that evidence later adds avoidable work
  and risks disturbing the candidate.
* Smallest useful change: move the helper/parser failing-regression execution
  into P01-T02, before its runtime edits. Leave focused passing runs, admitted
  full suites and browser/axe checks in P02-T01. Reconcile both artifacts'
  task descriptions so no dependent phase claims pre-edit execution.
* Action owner: planning parent.
* Exact resolving evidence: revised P01-T02 in both plan and phase details
  orders regression addition, failing run against unchanged runtime, then
  runtime correction; revised P02-T01 requires passing validation rather
  than first reproduction. Subsequent implementation evidence records the
  actual expected failing assertions and corrected passing commands/exits.
* Decision route: direct planner correction. No significant or divergent
  user decision is required.

## Strengths and Residual Risk

* The selected changes address their causal defects without weakening stale
  draft safeguards, mutation duplicate suppression or handler-owned disable
  state. Explicit opener identity and null-control search feedback reuse
  existing mechanisms instead of broadening the helper API.
* Parser acceptance checks exact per-statement objects rather than aggregate
  citation totals, which would not detect accidental sentence merging.
* The alternative interpreter has not passed the pending import check.
  Treat "verified" in the executive summary as version/path evidence only,
  not proof of dependency readiness. Record the actual probe before using
  it; a missing prerequisite remains a disclosed validation limitation.
* Lock contention explicitly permits scoped validation, not a full-suite
  pass. Browser/axe output is not human accessibility acceptance, and no
  publication receipt or hosted acceptance follows from local checks.

## Questions or Blocking Evidence Gaps

* No unresolved user decision or decision-critical research gap within this
  assessment boundary. Environment readiness remains an execution prerequisite.

## Limitations

* No tests, dependency imports, browser sessions or lock operations were
  performed during critique. No operations were performed on the alternative
  interpreter or lock paths.
* W1 was considered only as supplied research evidence; no fresh external
  retrieval or web/accessibility conformance assessment is claimed.
* No source, plan, phase-details, research or historical review record was
  edited. Existing uncommitted inputs were left intact.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: reconcile regression reproduction ordering in the
  two planning artifacts, disposition PC-001, then continue the authorized
  implementation sequence without another critique.
* User response required: no.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-corrections-plan.md](.copilot-tracking/plans/2026-10-29/loading-briefing-hax-531-corrections-plan.md) | Assessed final-candidate plan |
| [.copilot-tracking/details/2026-10-29/loading-briefing-hax-531-corrections-phase-details.md](.copilot-tracking/details/2026-10-29/loading-briefing-hax-531-corrections-phase-details.md) | Assessed phase details |
| [.copilot-tracking/research/2026-10-29/loading-briefing-hax-531-corrections-research.md](.copilot-tracking/research/2026-10-29/loading-briefing-hax-531-corrections-research.md) | Supplied focused research |
| [.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-hax-531-corrections-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/loading-briefing-hax-531-corrections-plan-critique.md) | This independent critique |

## Next Steps

Planning parent: directly resolve and disposition PC-001, then continue within
the existing local-only authorization. No user action is required. This one
critique is complete; stop here without another critique or peer-stage launch.
