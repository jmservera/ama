---
title: Employee loading and briefing final-candidate plan critique
ms.date: 2026-10-30
---

## Metadata

* Task ID: 531
* Task slug: employee-loading-feedback-531
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/employee-loading-feedback-531-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/employee-loading-feedback-531-phase-details.md
* Critique execution status: Complete
* Assessment: one independent final-candidate critique; no implementation or gate execution.

## Inputs and Criterion Boundary

* Caller requests the ordered research, plan, implement and review loop on
  supplied main baseline 5634f9a077d175a931c15e3400114665d8c071ee, a local
  commit only, and no push, Azure activity, live sign-in or secrets.
* Read the canonical plan, phase details and
  .copilot-tracking/research/2026-10-30/employee-loading-feedback-531-research.md.
  Inspected its supplied evidence in src/api/README.md,
  src/api/checks/loading_briefing_browser_check.py,
  src/api/src/zava_forward/api/web/index.html and the historical UX
  participation statement in
  .copilot-tracking/research/2026-10-28/loading-briefing-hax-531-research.md.
* Followed the named runner ownership into
  src/api/checks/design_system_browser_check.py, checked the exact timing
  selector in src/api/tests/test_loading_feedback.py and read the local-gate
  instructions in src/README.md. Read the required project context documents.
  No broad repository audit or new external design research was performed.
* Read issue #531 and its supplied owner-extension/merge comments with gh.
  Their checked boxes are historical dispositions, not fresh execution proof.
  The merge comment explicitly leaves live verification outstanding after #538.
* Read-only git inspection confirms HEAD is the supplied baseline on
  feat/employee-loading-feedback-531. The plan, details, research and workflow
  state are existing untracked parent inputs; this critique does not move,
  stage, commit or modify them.
* Boundary: assess adequacy and executability of the two-file evidence
  improvement, inherited local coverage, test ownership, limitations and
  handoff. Do not establish live acceptance, full accessibility conformance,
  current test results or specialist-authored UX approval.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Baseline and dependency; C2-C5 | Covered | Exact HEAD verified; #531 comments and supplied research support preserving merged #538 rather than redesigning it. Research records #529 merged. |
| AC1; P01-T01 static shell | Covered | index.html:14-20 has startup text, polite status, hidden retry and noscript help before scripts. Proposed disabled-script context, markup ordering and two viewport checks add distinct evidence. |
| AC1; inherited loading/retry | Covered | Browser shell, watchdog, required/optional companion and helper scenarios already exercise bounded retry, persistent failure and recovery. No replacement scenarios are needed. |
| AC2; simulated cold start | Covered | Existing shell_check holds app.js and checks the empty app plus immediate/4s/15s states. Added no-JS coverage complements this; neither proves visibility before HTML arrives. |
| Owner extension; immediate/200 ms feedback | Partial | Exact threshold is tested by the Node-backed API unit test, not the browser suite as the plan currently states; PC-002. Existing browser checks exercise real pending controls and duplicate suppression. |
| AC3; C5/C7; HAX and Fluent | Covered with disclosed limitation | Existing README mapping separates labels, mode, dismissal, correction, rationale and feedback. UX agent intake-only response is disclosed, not upgraded into a specialist note or human approval. |
| AC4; conditional review and authority | Covered | Existing browser checks exercise conditional editor/reason, required reason, cancel/focus, failed refresh, pending/uncertain review barriers and actual review payloads. Draft review remains distinct from works approval and resident consent. |
| AC5; provenance/time/unverified | Covered | Existing browser assertions exercise rules and AI labels, timestamp presence, source links and unverified output. API discovery retains related source/review regressions. |
| AC6; browser/axe/reduced motion | Covered as planned, not executed | Script-enabled browser scenarios retain pinned axe verification and reduced-motion assertions. Excluding axe injection from the no-page-script scenario is appropriately explicit. |
| AC7; live verification | Intentionally unmet | Live check is prohibited in this run; Refs #531 and no closure claim are correct. |
| Locked test ownership and targets | Covered | One added browser scenario with two viewport assertions; no removals. Existing runner owns synthetic fixture, health readiness and process termination. No package test duplication or production rewrite is justified. |
| P01-T02; tool/lock/output dependencies | Partial | Commands prescribe forbidden temporary paths and do not reconcile the active file-operation restriction; PC-001. |
| RPI evidence, Review, commit and exact-head gate | Covered with prerequisite risk | Original evidence, one Review, local commit, immutable gate inputs and publication blockers are explicit. No push or live fallback is authorized. |

## Verdict

* Verdict: Revise
* Rationale: The proposed implementation and regression boundary are credible
  and appropriately narrow. Before execution, the planner must reconcile the
  prohibited temporary-path commands and correct the exact-timing evidence
  owner. Neither finding calls for redesign, more tests, another critique or
  a routine user question.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Execution commands conflict with the active temporary-path restriction

* Related IDs: User Decisions and Requirements; P01-T01; P01-T02; Dependencies;
  Handoff.
* Evidence: The plan requires flock against a lock under /tmp and explicitly
  directs use of /tmp/mv tools. Phase details prescribe that executable PATH
  and an existing /tmp axe asset. The active execution instructions prohibit
  /tmp file operations and require newly created scratch files to be
  project-relative. Both artifacts also require fresh external output but
  leave its permitted location unresolved.
* Concern: The candidate is not executable as written under this session's
  constraints. The obsolete README wording should not be replaced with a
  claimed runnable command that this execution cannot use. The conflict
  includes lock creation and asset access, not only redirected logs.
* Impact: An implementer could violate the active restriction or silently
  replace the shared lock with an independent lock, losing cross-task
  serialization. An unresolved output location can also prevent a valid
  external exact-head receipt.
* Smallest useful change: Reconcile permitted tool, pinned-asset, scratch and
  evidence locations in both planning artifacts before execution. Preserve
  wait-600 serialization and the single shared-lock identity; do not silently
  introduce a different lock. Distinguish the requested lock policy from what
  this execution can actually run. If a compliant shared lock or external
  receipt location cannot be established, explicitly mark that validation
  blocked and retain the local-only/no-fallback boundary rather than execute
  the conflicting command. Do not expand source/test scope to solve this.
* Action owner: Planning parent/execution coordinator.
* Exact resolving evidence: Revised plan and P01-T02 contain mutually
  consistent permitted locations and command preconditions, or explicitly
  identify the affected gate as blocked by the path restriction. No command
  may be presented as executed or passing while that blocker remains.
* Decision route: Direct planner correction. Existing instructions already
  resolve the prohibition; no significant or divergent user decision and no
  routine user response are required.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Low]: Exact 199/200 ms evidence is assigned to the wrong runner

* Related IDs: Non-Functional Requirements; owner comment; P01-T02; AC1/AC6.
* Evidence: The plan says existing browser checks verify 199/200 ms timing.
  src/api/tests/test_loading_feedback.py:73-76 advances the actual-helper
  Node test to 199 ms and then 200 ms. The supplied browser runner checks
  pending controls/spinners and reduced motion, but has no corresponding
  199/200 ms threshold assertion.
* Concern: The behavior is already covered by planned API discovery, but its
  evidence attribution would incorrectly imply a browser-timed measurement.
* Impact: The acceptance matrix or final report could overstate what the
  browser run proves and obscure which existing test protects the threshold.
* Smallest useful change: Attribute exact helper timing to the existing
  actual-helper test in test_loading_feedback.py and attribute real-control
  pending behavior, reduced motion and axe to the browser runner. No new test
  is needed.
* Action owner: Planning parent.
* Exact resolving evidence: The plan's non-functional requirements and planned
  acceptance reporting name
  src/api/tests/test_loading_feedback.py::test_actual_helper_timing_duplicates_errors_and_state_ownership
  as the exact-threshold evidence and
  src/api/checks/loading_briefing_browser_check.py as the real-browser evidence.
  The existing one-scenario/two-viewport addition ceiling remains unchanged.
* Decision route: Direct planner correction; no user decision required.

## Strengths and Residual Risk

* No duplicate redesign is warranted by the supplied baseline or issue
  comments. The disabled-script scenario closes a precise evidence gap
  without altering delivered runtime behavior.
* Test ownership, no removals, maximum additions, script-enabled axe ownership,
  finally-based context cleanup and synthetic server lifecycle are bounded.
* The no-JS assertion must prove readable static content, not successful case
  work without JavaScript. Checking DOM geometry through browser automation
  does not imply page-authored scripts ran.
* Live cold start, staff usability, screen-reader/voice-control acceptance and
  full Fluent adoption remain explicitly outside this run. The unavailable
  specialist contribution is an accepted disclosed limitation, not a reason
  to repeat the UX delegation or invent approval.
* Missing full-gate prerequisites remain blockers, not permission to skip,
  deploy, use cloud substitutes or close the issue.

## Questions or Blocking Evidence Gaps

* No user question is required. PC-001 requires a planner-owned executable
  path/precondition correction or an explicit blocked validation disposition.
* There is sufficient supplied evidence to complete this plan assessment;
  unexecuted tests are not treated as missing research or current passes.

## Limitations

* No tests, browser sessions, axe runs, heavy gates, deployment, sign-in or
  commits were performed. Historical checked criteria are not fresh evidence.
* Source inspection was limited to the supplied evidence and its directly
  named runner/test ownership. This is not a full inherited implementation
  audit or a fresh UI/accessibility review.
* The only written file is this critique. Plan, phase details, research,
  workflow state and runtime/test source remain unchanged.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent/execution coordinator.
* Smallest next action: Correct execution path preconditions or mark the
  affected validation blocked; also repair PC-002's evidence attribution.
* Severity summary: 0 Critical, 1 High, 0 Medium, 1 Low.
* User response required: No.
* Return this complete finding set to the active parent for direct
  reconciliation, with no second critique.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/employee-loading-feedback-531-plan.md](.copilot-tracking/plans/2026-10-30/employee-loading-feedback-531-plan.md) | Assessed canonical candidate; unchanged. |
| [.copilot-tracking/details/2026-10-30/employee-loading-feedback-531-phase-details.md](.copilot-tracking/details/2026-10-30/employee-loading-feedback-531-phase-details.md) | Assessed execution details; unchanged. |
| [.copilot-tracking/research/2026-10-30/employee-loading-feedback-531-research.md](.copilot-tracking/research/2026-10-30/employee-loading-feedback-531-research.md) | Supplied evidence and accepted boundaries. |
| [.copilot-tracking/reviews/plans/2026-10-30/employee-loading-feedback-531-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-30/employee-loading-feedback-531-plan-critique.md) | This independent final-candidate assessment. |

## Next Steps

The active planning parent should resolve PC-001 and PC-002 directly, preserve
this original Revise verdict, and continue the ordered loop only within the
resolved execution constraints. No further critique or user action is required.
