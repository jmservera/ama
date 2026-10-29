---
title: Chat widget fix cycle 3 independent plan critique
description: Final-candidate credibility assessment for issue 550 and PR 556
ms.date: 2026-10-29
---

<!-- markdownlint-disable-file -->

## Metadata

* Task ID: issue-550-pr-556-fix-cycle-3
* Critique date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-fix-cycle-3-plan.md
* Phase details: .copilot-tracking/details/2026-10-29/chat-widget-550-fix-cycle-3-phase-details.md
* Critique execution status: Complete
* Assessment: Exactly one independent final-candidate critique; no workers,
  implementation, validation execution, commit or publication.

## Inputs and Criterion Boundary

* Caller requirements: preserve bottom following across the 200 ms loading-row
  shrink without overriding upward reading or history focus; start the positive
  regression at bottom before sending and never reposition afterward.
* Reviewed the named plan, phase details and research; shared chat-widget.js;
  reply_scroll and its shared_ui caller; test_chat_widget_focus.py; necessary
  employee/resident submit handlers and shared layout CSS. Read the prior review
  excerpt identified by research C6 to distinguish historical test evidence.
* Repository context: original case study, addendum, reference index and owner
  memory. Memory was context only.
* Decisions and dependencies: current eligibility immediately before loading
  visibility changes, shared message predicate, <=1 CSS px tolerance, no cached
  send-time flag, unchanged focus/timer/disposal semantics, no test removals,
  at most two new unit methods and two browser modes, existing test ownership,
  at most five modified src files with an evidence-justified adapter exception.
* Validation/persistence boundary: supplied chat discovery and PYTHONPATH,
  Ruff check/format, Node syntax, two-site synthetic browser checks, original
  widget negative control, one independent implementation Review and local
  co-authored commit. No push, az, latest.json changes or publication gate.
* Only this critique artifact is authorized for editing. Existing untracked
  planning/state artifacts remain untouched.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Current eligibility, shared predicate; C1/C5; P01-T01 | Covered | Loading visibility snapshots avoid stale intent and retain the established message focus guard. |
| Two-site bottom-before-send positive case; C3/C4; P01-T01 | Partial | PC-001: resident status insertion can lose eligibility before the planned loading snapshot. |
| Upward/history interaction before and after delay; P01-T01 | Covered | Owned unit and browser extensions cover current intent, exact focus identity and returning to bottom within the locked budget. |
| Timer, cancellation, disposal and no new follow machinery; P01-T01 | Covered | Existing lifecycle is explicitly retained; controlled unit timers model the delayed shrink. |
| Test ownership, no removals and source scope; P01-T01 | Covered | Named existing files and explicit addition/file budgets prevent another harness or unrelated redesign. |
| Requested checks and sensitivity; P02-T01 | Covered | Targeted commands, two synthetic sites, original-widget negative control and preservation of adverse evidence are required. No execution is claimed here. |
| Independent Review, local commit and publication limits; P03-T01 | Covered | One later implementation Review, privacy-safe identity and co-author trailer are specified; publication remains separate. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 1; Medium 0; Low 0.
* Rationale: The loading-transition approach is credible for readers who are
  still eligible at that transition. The two-site acceptance promise also
  requires addressing the source-visible resident status-row transition that
  precedes it. A generic allowance for a later adapter change does not yet
  explain how that known prerequisite will preserve current intent.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Account for resident status shrink before loading eligibility is sampled

* Related IDs: C1, C3, C4; P01-T01; two-site bottom-before-send acceptance
  criterion; current-eligibility and no-stale-flag requirements.
* Evidence:
  * src/api/src/zava_forward/api/resident_demo/web/assistant.js:259-266
    calls busy(true), populates status with "Getting your advice", then appends
    the user message.
  * src/api/src/zava_forward/api/resident_demo/web/assistant.js:268-276
    clears status before inserting the successful reply, so the next send can
    start with an empty status row.
  * src/api/src/zava_forward/api/web/chat-widget.css:12,24-25
    makes the log flexible, status nonshrinking and empty status display:none.
  * src/api/src/zava_forward/api/web/chat-widget.js:75-85
    has the busy loading-hide before that adapter status assignment and computes
    message eligibility only when message() is entered.
  * The plan's Functional Requirements and phase details P01-T01 guard loading
    visibility mutations, not this preceding status mutation.
* Concern: On a resident turn beginning at bottom with empty status, adding
  status can reduce clientHeight before message() samples eligibility. The
  later loading-show snapshot can consequently see an already displaced reader
  and correctly decline to follow, despite no reader scroll or history focus.
  This is a source-backed failure mechanism, not a newly executed browser
  result; the plan needs to resolve it rather than assume eligibility survives.
* Impact: The primary two-site regression can still fail after implementing
  exactly the planned loading-only fix. Repositioning after send would conceal
  this and violate the user's regression requirement.
* Smallest useful change: Amend P01-T01 and the research disposition to explicitly
  account for empty-to-nonempty resident status geometry. Require the existing
  resident positive mode to start after a completed reply with empty status and
  record eligibility after the synchronous send sequence, before loading.
  Specify a bounded correction if that transition loses eligibility, sampling
  current geometry/focus immediately before the relevant mutation rather than
  retaining a send-time flag across the delay. Use the existing conditional
  adapter allowance if needed; retain the shared loading/message predicate,
  all existing negative cases, no-removal policy and locked test/file budgets.
* Action owner: Planning parent; implementation owner executes the reconciled
  geometry regression and bounded correction.
* Exact resolving evidence: Reconciled plan/details/research explicitly cover
  this predecessor transition and assign its owner. Implementation evidence
  subsequently shows the resident empty-status bottom-before-send case remains
  eligible through send and loading, reaches <=2 CSS px after the long reply
  with no post-send repositioning, and still preserves upward/history focus
  within the existing tolerance. Original-widget negative evidence and existing
  employee/resident negative modes remain preserved.
* Decision route: Direct planner correction. No significant/divergent user
  decision; preserving the two-site positive case is already required.

## Strengths and Residual Risk

* Immediate current-state sampling avoids overriding genuine interaction during
  the 200 ms delay. Shared eligibility prevents message/loading guard drift.
* The positive-mode change directly removes the prior masking reposition;
  existing after-loading cases and focus identity assertions remain mandatory.
* Controlled unit timing, original-widget sensitivity and preserved adverse
  logs provide complementary evidence without expanding test ownership.
* Live deployment, human/assistive-technology acceptance and complete publication
  gates remain explicitly outside this local correction, not claimed complete.

## Questions or Blocking Evidence Gaps

* No user question is required. PC-001 is resolvable within the authorized
  source scope and existing conditional adapter budget.

## Limitations

* Read-only source/plan assessment, not an executed reproduction or implementation
  Review. No Python, Ruff, Node, browser, Azure or GitHub mutation was performed.
* Supplied environment paths and dependency availability were not tested.
  This critique created no scratch copy or temporary-directory output.
* No fresh Web Interface Guidelines review or accessibility-conformance claim:
  this is a plan critique, with the fresh changed-web review assigned to P03.
* No open-ended research or whole-issue/whole-PR acceptance assessment.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Reconcile the resident status-transition prerequisite
  directly in the existing artifacts, then continue the authorized implementation
  and checks. Preserve this original critique and record its disposition; do not
  commission another plan critique.
* User response required: No.

## Artifacts

| Artifact | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-29/chat-widget-550-fix-cycle-3-plan.md | Reviewed final-candidate plan |
| .copilot-tracking/details/2026-10-29/chat-widget-550-fix-cycle-3-phase-details.md | Reviewed task and evidence contracts |
| .copilot-tracking/research/2026-10-29/chat-widget-550-fix-cycle-3-research.md | Supplied focused research |
| .copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-fix-cycle-3-plan-critique.md | This original independent critique |

## Next Steps

Planning parent resolves PC-001 directly and continues within the existing
authorization. No user action is required. This reviewer stops after the single
critique; implementation and publication are not authorized in this assessment.
