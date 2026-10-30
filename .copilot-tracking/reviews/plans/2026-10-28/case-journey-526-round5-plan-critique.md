---
title: Case journey round five independent plan critique
description: Single final-candidate credibility assessment for task 526-pr529-round5-20261028
ms.date: 2026-10-28
---

## Metadata

* Task ID: `526-pr529-round5-20261028`
* Critique date: 2026-10-28
* Plan: .copilot-tracking/plans/2026-10-28/case-journey-526-round5-plan.md
* Phase details: .copilot-tracking/details/2026-10-28/case-journey-526-round5-phase-details.md
* Critique execution status: Complete
* Assessment: the one independent final-candidate plan critique requested by the parent.

## Inputs and Criterion Boundary

* Caller requirements: PR 529 / issue 526 fifth-round correction of both chat
  submission lifecycles, restored proposal submission readiness, and polite,
  deduplicated always-visible count announcements; sibling dirty/live/readiness
  audit across PR-changed web files.
* Planning evidence: the supplied plan, phase details and
  .copilot-tracking/research/2026-10-28/case-journey-526-round5-research.md,
  including C1-C8 and W1-W2.
* Shipped evidence read: src/api/src/zava_forward/api/web/chat.js,
  src/api/src/zava_forward/api/web/assistants.js,
  src/api/src/zava_forward/api/web/case-workspace.js, and relevant lifecycle
  sections of src/api/src/zava_forward/api/web/app.js; focused unit files
  src/api/tests/test_case_journey.py and src/api/tests/test_workspace_scripts.py;
  existing journey and assistants browser harnesses under src/api/checks/.
* Context: repository case-study documents, knowledge-base index and owner memory;
  src/api/README.md validation and shared-lock guidance.
* Dependencies and limits: retain the existing branch and parent-owned lifecycle;
  at most three new unit methods, extend existing browser harnesses, no removals,
  keep 38 journey axe scans, pinned axe in both browsers, no intended tools edits.
  Heavy validation requires the caller's shared nonblocking lock and bounded
  retry policy. No Azure, secrets, .env access or remote writes. Local identity,
  Conventional Commit, required trailer and original evidence remain required;
  az-dependent publication remains blocked, not waived.
* Boundary: assess implementation credibility and validation coverage, not
  implement, execute checks, certify accessibility, perform the later independent
  Review, or authorize publication. The local diff-name inspection identified
  app.js, assistants.js, case-workspace.js, chat.js, index.html, ops.js, panels.js
  and style.css as the web audit boundary against the existing origin/main ref.
  No remote freshness or hosted result is inferred.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Chat exact raw equality, success/failure, unrelated dirtiness; C1/C2/C5; P01-T01 | Partial | Dispatch snapshots and deferred-response tests cover retained controls, but not replacement controls and cached drafts during a pending chat. PC-001. |
| Pending keyboard resubmission; P01-T01 | Partial | Disabled-control entry guard is planned, but a same-case redraw creates new enabled controls while the original request remains pending. PC-001. |
| Restored proposal ready/own-verification guards; C3/C7; P01-T02 | Covered | Identical predicate, state matrix, same-revision restoration, copyable text and no-request browser assertion are explicit. Existing successful review flow remains. |
| Polite count text and unchanged-update deduplication; C4/C6; P01-T03 | Covered | Dedicated atomic polite span, preserved semantic dd/navigation, text-write measurement, hidden-panel and delayed pagination/unavailable coverage are explicit. |
| Sibling dirty/live/readiness audit; C8; P01-T03 | Covered with correction required | Named audit paths and intentional manual-draft retention are credible; the pending-chat redraw scenario must be included rather than assumed covered. PC-001. |
| Focused units and both browsers with pinned axe; P02-T01 | Covered | Existing harness extension and assistants checksum support are planned; no duplicate harness or journey scan-count increase is proposed. |
| Three-method ceiling, no removals, no tools edits | Covered | One executable lifecycle method per defect leaves room for subcases and existing browser extensions. PC-001 needs no additional method. |
| Shared heavy lock and 40-minute retry ceiling; P02-T01 | Covered | Nonblocking admission and absolute 2400-second deadline are explicit; the exact shared lock is supplied by caller context and src/api/README.md. No heavy operation was performed here. |
| Independent Review, local commit, original adverse evidence and publication block; P02-T02 | Covered | Single later Review, privacy-safe identity, trailer, no az/full-gate invocation and coordinator-owned publication are explicit. Local checks do not replace the complete gate. |

## Verdict

* Verdict: Revise
* Severity summary: 0 Critical, 0 High, 1 Medium, 0 Low.
* Rationale: the proposed fixes map well to the three reported failures, but
  the chat implementation/test contract assumes the submitted DOM control stays
  current. Shipped same-case refresh and cached-field restoration invalidate
  that assumption. Correct this bounded lifecycle gap before implementation.
  No significant or divergent user decision is necessary.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [Medium]: Cover pending chat completion across same-case redraw

* Related IDs: C1, C2, C5, C8; P01-T01; P01-T03; P02-T01; chat cleanup and
  pending-resubmission acceptance criteria.
* Evidence: src/api/src/zava_forward/api/web/chat.js captures input and send
  controls in each panel's handler closure. The planned snapshot helper likewise
  holds a particular field object. In
  src/api/src/zava_forward/api/web/app.js, caseView at lines 585-608 captures
  dirty fields with rememberCaseFields and constructs new panels; lines 752-755
  restore saved fields after rendering. snapshotCaseFields/caseFieldUnchanged
  at lines 777-784 compare the captured object, not its replacement.
  rememberCaseFields at lines 798-804 retires cached entries only when the
  corresponding live field is clean. P01-T01 specifies deferred requests and
  exact-value cleanup, but no refresh/replacement scenario or request-state
  ownership that survives that refresh.
* Concern: when an ordinary case save or Refresh proposals redraws the case
  while Ask is pending, the submitted question can be restored into a new dirty
  textarea. Successful completion can clear only the old detached textarea,
  leaving the submitted text and dirty guard on the replacement. The replacement
  send control also starts enabled, so checking only the old control's disabled
  state does not prevent another submission during the original request.
  This is a source-backed planning gap, not an observed result from running a
  proposed implementation.
* Impact: a successful submission can still leave a false unsaved-change
  warning, and a pending request can be submitted again after an otherwise
  ordinary same-case refresh. A naive correction that clears the replacement
  unconditionally would instead discard newer in-flight text.
* Smallest useful change: extend the existing P01-T01 lifecycle contract to
  cover pending requests across same-case redraw and live/cached field
  reconciliation. Require completion to retire only the matching submitted raw
  value in the still-current case session, preserve later replacement-field
  text and unrelated drafts, and preserve pending submission exclusion across
  the redraw. Do not prescribe a framework or broad state rewrite.
* Action owner: planning parent; implementation parent executes the revised
  lifecycle contract.
* Exact resolving evidence: revised P01-T01 and acceptance wording explicitly
  include same-case redraw during each chat's pending request. Extend the one
  planned chat unit method with subcases, and the existing browser harness with
  held actual asks followed by an unrelated case save or Refresh proposals.
  For both chats, assert unchanged successful text becomes empty and clean in
  the replacement control and no cached chat draft remains; later raw or
  whitespace edits remain dirty; failure preserves text; pending replacement
  controls cannot dispatch another ask; unrelated drafts and unload warnings
  remain intact. Record execution later under P02-T01, without adding a fourth
  unit method or changing the journey's 38 scans.
* Decision route: direct planner correction. Existing user direction already
  requires the relevant dirty/readiness sibling lifecycle audit.

## Strengths and Residual Risk

* The plan correctly rejects trimmed-only comparison and dispatch-time clearing.
* Proposal restoration stays revision-bound and editable/copyable while the
  submission button shares the existing readiness and verifier predicate.
* Live count wording is isolated from navigation and availability detail, with
  unchanged DOM writes tested rather than relying solely on axe.
* Test scope, original failure preservation, single later Review and local-only
  handoff respect the caller's constraints.
* Actual screen-reader speech, staff acceptance, complete az-dependent gate
  execution and hosted approval remain separate evidence, not promised outcomes.

## Questions or Blocking Evidence Gaps

* No user question. PC-001 is resolvable by the planning parent using the
  supplied lifecycle evidence.

## Limitations

* Read-only source assessment; no unit, browser, scanner, heavy-lock or full-gate
  execution. No current-source guidelines retrieval or fresh UI conformance
  review is claimed.
* W1/W2 retrieval and thread inventory are supplied research evidence, not
  independently refetched here.
* This is the complete actionable finding set for the supplied planning
  boundary. It is not the later exact-head implementation Review.
* Existing untracked parent planning/state files were left untouched. Only this
  critique artifact was written; no implementation, commit or remote write.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: incorporate the redraw/pending-state subcases into
  P01-T01 and dispose PC-001 explicitly, then continue the parent-owned lifecycle
  without another final-candidate critique.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-28/case-journey-526-round5-plan.md](.copilot-tracking/plans/2026-10-28/case-journey-526-round5-plan.md) | Assessed plan |
| [.copilot-tracking/details/2026-10-28/case-journey-526-round5-phase-details.md](.copilot-tracking/details/2026-10-28/case-journey-526-round5-phase-details.md) | Assessed task contracts |
| [.copilot-tracking/research/2026-10-28/case-journey-526-round5-research.md](.copilot-tracking/research/2026-10-28/case-journey-526-round5-research.md) | Supplied evidence |
| [.copilot-tracking/reviews/plans/2026-10-28/case-journey-526-round5-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-28/case-journey-526-round5-plan-critique.md) | Single independent critique |

## Next Steps

Active parent: resolve PC-001 by direct plan/detail correction, preserve this
original verdict, and continue implementation only after explicit disposition.
No user action or second critique is required. Publication remains blocked until
the coordinator can satisfy the complete exact-head gate.
