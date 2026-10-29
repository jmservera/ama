<!-- markdownlint-disable-file -->
# RPI Plan Critique: Nonblocking regulatory usage refresh

## Metadata

* Task ID: reg208-pr506-usage-refresh-2026-10-29
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/regulatory-usage-refresh-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/regulatory-usage-refresh-phase-details.md
* Critique execution status: Complete
* Candidate context: feat/regulatory-assistant-208, PR #506, Refs #208.
* Assessment count: One independent final-candidate critique.

## Inputs and Criterion Boundary

* Caller requirements: display the answer, clear only unchanged submitted
  input and release lookup without awaiting the secondary usage GET; contain
  refresh failure without an unhandled rejection or stuck disable; demonstrate
  focused red/green coverage using existing API test conventions.
* Additional requirements: relevant tests, Node syntax, Ruff for touched Python,
  dated Research/Plan/Implementation/Review evidence and a local Conventional
  Commit with the Copilot trailer. No push, az, other worktrees, rubric edits,
  test removals or generated targets.
* Supplied evidence: the named plan, phase details and
  .copilot-tracking/research/2026-10-29/regulatory-usage-refresh-research.md.
* Supporting evidence inspected: shipped chat lifecycle, shared field helpers,
  async-action ownership, existing case-journey DOM and executable-JavaScript
  regression, the owning API usage paragraph and existence of the selected
  adjacent test modules. Repository context documents were consulted without
  extending this task into regulatory research.
* Decisions: reuse the existing caught usage helper and raw-field guard;
  separate answer completion from advisory usage completion; preserve existing
  answer/thread error behavior and manual/human boundaries.
* Dependencies: a disposed critique and usable local dependencies precede
  implementation; P01-T02 follows red evidence; P01-T03 follows the fix.
  Independent implementation Review and local commit remain parent-owned
  completion obligations, not actions authorized to this critique.
* Assessment boundary: planning credibility for the targeted local change only.
  No execution result, browser acceptance, accessibility conformance, hosted
  check, publication gate or human approval is established.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Answer completion independent of usage; C1/C5; P01-T02 | Covered | chat.js:388-398 renders the answer before the blocking await. Moving cleanup before a nonawaited refresh allows finally and the handler promise to complete. async-action.js:40-80 ties shared busy recovery to that promise. |
| Refresh error containment; C2; P01-T01/T02 | Covered | chat.js:326-329 catches request and usage-render errors in its own live-text owner. Details require delayed success and rejection under strict Node unhandled-rejection behavior. |
| Unchanged versus edited input; C4; P01-T01/T02 | Covered | chat.js:140-144 and app.js:994-1007 preserve the raw-field comparison. Details test unchanged cleanup and edited-field dirty-state preservation; existing whitespace coverage remains unchanged. |
| Deterministic focused regression; C3; P01-T01 | Covered | test_case_journey.py supplies DOM and shipped_helpers; its existing both-chat regression executes real chat.js. Details defer the answer and usage independently, inspect completion before usage settles, bound the subprocess and require a baseline assertion failure. |
| Pending duplicate and answer/thread failure behavior; P01-T01 | Covered | Existing test_both_chat_submissions_clear_only_successful_unchanged_raw_questions covers these paths; the plan retains it and reruns the module. |
| Exact change ownership; P01-T01/T02 | Covered | Exactly one new test method, no removals, no new fixture library or test file; canonical production/documentation targets are chat.js and src/api/README.md; generated targets are none. |
| Owning documentation; C6; P01-T02 | Covered | src/api/README.md:3388-3395 owns the audit-only usage description. The planned addition explains latency independence and explicit failure without changing regulatory or approval claims. |
| Targeted validation; P01-T03 | Covered | Details name test_case_journey, test_chat_panel, test_regulatory_chat_api and test_regulatory_ux_check, Node syntax and touched-file Ruff check/format check, with installed current-worktree distributions. |
| Dated full RPI evidence and local commit | Covered | Plan metadata identifies dated research, plan, details, critique and changes paths; P01-T03 requires independent Review. User Decisions and Requirements explicitly retains all four stages, local Conventional Commit and specified coauthor trailer. Completion evidence remains to be produced by the parent. |
| Scope and acceptance boundary | Covered | Plan and details explicitly exclude unrelated behavior, visuals, API changes, cloud operations, publication and browser/human acceptance; dependency failures must be recorded rather than called success. |

## Verdict

* Verdict: Pass
* Rationale: the proposed ordering change addresses both input/control recovery
  and handler-promise completion while preserving the existing independent
  error owner. The deferred regression can expose the original defect without
  copying implementation logic, and the task sequence requires red evidence
  before the fix. Scope, validation and local-only delivery match the caller.
* Severity counts: Critical 0; High 0; Medium 0; Low 0.

## Findings

None. There are no actionable PC-xxx findings within the supplied criterion
boundary. No discoverable finding is withheld for a later critique.

## Strengths and Residual Risk

* The plan tests the observable state while usage is unresolved rather than
  accidentally waiting for the condition whose independence it must prove.
  Requiring the submit promise to settle also addresses the shared action
  wrapper's lifecycle without expanding production scope.
* Existing success, whitespace-edit, duplicate and failure coverage is retained.
  The single additional method can cover the delayed usage outcome matrix
  using native promises and current fixtures.
* Research explicitly accepts possible out-of-order overlapping usage reads
  as advisory audit-text risk outside this finding. The critique does not
  elevate usage text into control authority or require request sequencing.
* Targeted tests do not establish browser, assistive-technology, staff
  comprehension, operational or whole-project acceptance. Those limitations
  are explicit, not silently waived.
* Dependency availability remains an implementation prerequisite. A blocked
  validation command must remain blocked evidence, not a passing result.

## Questions or Blocking Evidence Gaps

* None for this planning decision. No significant or divergent user decision
  is required.

## Limitations

* Source was inspected read-only; no tests, syntax checks, Ruff, dependency
  restoration or implementation Review were run by this critique.
* Local branch/status inspection confirmed the named branch and existing
  untracked planning inputs. Remote PR lifecycle and research dependency
  probes were not independently repeated.
* A passing plan critique is not completion evidence. The parent still owns
  red/green results, dated changes and independent Review, reconciliation and
  the privacy-safe local commit required by repository instructions.
* Only this critique artifact was written. Plan, details, research, source and
  tests were not edited.

## Recommended Next Action

* Highest-impact finding: None.
* Action owner: Planning parent.
* Smallest next action: record this Pass disposition, finalize the candidate
  and proceed to P01-T01 under the caller's targeted local-only boundary.
* Exact completion evidence: baseline assertion failure and fixed passing
  result for the new method, selected test results, Node syntax and Ruff
  results, dated implementation/independent Review records, and the local
  Conventional Commit with the required trailer. These are future execution
  obligations, not unresolved plan findings.
* Decision disposition: no direct planner correction and no significant or
  divergent user decision; no repeat critique is requested.
* User response required: No.

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-29/regulatory-usage-refresh-plan.md | Assessed final-candidate plan |
| .copilot-tracking/details/2026-10-29/regulatory-usage-refresh-phase-details.md | Assessed task sequence and validation details |
| .copilot-tracking/research/2026-10-29/regulatory-usage-refresh-research.md | Supplied evidence and accepted residual boundary |
| .copilot-tracking/reviews/plans/2026-10-29/regulatory-usage-refresh-plan-critique.md | This independent critique |

## Next Steps

No user action is required. Return Complete / Pass to the active planning
parent for disposition and authorized continuation. This critique stops here;
it does not implement, commit, invoke another review or start a workflow.
