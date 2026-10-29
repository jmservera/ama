---
title: Case journey round eight independent plan critique
description: Sole final-candidate assessment for task 526-round8, PR 529
ms.date: 2026-10-29
---

## Metadata

* Task ID: 526-round8, PR #529, Refs #526.
* Critique date: 2026-10-29.
* Plan: .copilot-tracking/plans/2026-10-29/case-journey-526-round8-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/case-journey-526-round8-phase-details.md.
* Critique execution status: Complete.
* This is exactly one independent final-candidate critique, with one complete
  actionable finding set. Plan, details, research and historical Review remain
  unchanged.

## Inputs and Criterion Boundary

* Caller requirements: Persistent action/target exclusion for every employee
  mutation, including fieldless and rebuilt forms; shared-queue unsubmitted
  review draft retention; unit and actual journey/assistants browser checks
  with axe; no Azure, secrets, environment files or push.
* Research: .copilot-tracking/research/2026-10-29/case-journey-526-round8-research.md,
  C1-C6 and W1.
* Prior independent evidence:
  .copilot-tracking/reviews/logs/2026-10-29/case-journey-526-round7-review.md,
  especially RV-001 High and RV-002 Medium. Their original findings and
  Not accepted outcome are not superseded by this plan assessment.
* Relevant shipped source inspected: app.js transport, navigation, shared field
  capture/reconciliation/recovery; assistants.js proposal and queue lifecycle;
  panels.js resident/challenge handlers; chat.js mutation entry points.
  Mutation call sites in ops.js and timecapture.js were also inspected.
  All source paths are under src/api/src/zava_forward/api/web/.
* Existing regression evidence inspected:
  src/api/tests/test_case_journey.py and
  src/api/checks/assistants_browser_check.py.
* Project framing: Original case study, relevant opening addendum and reference
  index sections, owner memory and sector-primer context. Memory is context,
  not correctness evidence. No new regulatory assessment was needed.
* Decisions and dependencies: Existing topic feat/case-journey-ux-526;
  local correction only; P01 implementation/regressions precede P02 checks and
  independent Review. Publication, hosted checks and human acceptance remain
  coordinator-owned and unestablished.
* Locked test ownership: At most four added methods in test_case_journey.py;
  test_workspace_scripts.py unchanged unless its isolation fixture needs a
  shared global; at most one new helper in each existing browser check;
  extend existing matrices; no removals or golden replacement.
* Assessment boundary: Plan credibility and directly coupled source risks,
  not implementation acceptance, a fresh UI/accessibility review or publication
  readiness. Current execution forbids all temporary-directory file operations,
  not just generated evidence in temporary directories.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| RV-001; C1, C2, C4, C5; P01-T01 | Covered | Persistent transport ownership, action/target keys excluding mutable content, raw-handler consolidation, fieldless/rebuilt controls and complete sibling audit are explicitly planned. |
| Lock lifetime and independence; P01-T01/P01-T02 | Covered | GETs cannot release exclusion; body parsing is inside the lock; unrelated action/target may proceed; refusal/failure release and duplicate status feedback are required. |
| Raw-handler outcome preservation; P01-T01/P01-T02 | Partial | Consolidation changes the malformed-response behavior unless strict raw-form parsing is explicitly retained and exercised; PC-001. |
| RV-002; C3, C6; P01-T01 | Covered | Queue-owned session, capture immediately before replacement, ID/revision binding, copy-only recovery, failed-listing retention and explicit discard address the reported loss. |
| Queue success, later edits and session boundaries | Covered | Requirements retain unsubmitted JSON and later edits, consume only unchanged submitted values, include recovery-only warnings and reset on authentication/explicit departure. Implementation must preserve these requirements when adapting case-global helpers. |
| P01-T02; unit and actual browser acceptance | Covered | Shipped-JavaScript tests, held real journey requests and queue outcome/listing matrices with pinned axe are assigned within explicit addition/removal limits. PC-001 fits existing matrices. |
| P02-T01; shared admission and evidence | Partial | Worktree imports, Ruff, source hashes and preserved results are appropriate; the specified temporary lock path conflicts with execution constraints; PC-002. |
| P02-T02; independent Review and local commit | Covered | A fresh bounded reviewer, preserved outcome, separate correction routing, privacy-safe identity and no publication claim are explicit. |

## Verdict

* Verdict: Revise.
* Severity totals: 0 Critical, 1 High, 1 Medium, 0 Low.
* Rationale: The core architecture directly addresses both round-seven findings.
  Two bounded corrections are needed before execution: preserve raw-form
  uncertainty on invalid response JSON and make heavyweight-check admission
  compatible with the non-temporary-file boundary. Neither requires additional
  tests beyond the locked ownership/addition limits, a redesign or a new user
  decision.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Consolidating raw forms can silently change malformed-response outcomes

* Related IDs: C1, C2; P01-T01, P01-T02; acceptance criteria for malformed
  responses, retained drafts and existing history barriers.
* Evidence: src/api/src/zava_forward/api/web/app.js:43 catches response JSON
  failure and substitutes an empty object. With a successful HTTP status,
  api() then resolves successfully; with an unsuccessful status, it supplies
  the HTTP status but has no parsed outcome. In contrast,
  src/api/src/zava_forward/api/web/panels.js:171 and :371 await response.json()
  without that fallback, so parse rejection after dispatch reaches the
  raw-handler uncertainty/history path at :189 and :391.
* Concern: P01-T01 moves both raw families onto this shared transport without
  specifying how their existing strict parse behavior is retained. The plan
  requires lock release after malformed responses, but release alone does not
  preserve their outcome semantics. A malformed 2xx can become apparent success;
  a malformed 409/503 can become an ordinary correctable refusal rather than
  unconfirmed dispatch. This is a concrete migration hazard, not a claim that
  the unimplemented correction already fails.
* Impact: Unconfirmed resident/challenge writes may consume drafts or permit
  resubmission without the previously required history check.
* Smallest useful change: Amend P01-T01 to require the guarded transport to
  expose JSON parse failure to the migrated raw handlers, retaining their
  uncertainty classification and drafts while releasing the transport lock
  in finally. A strict parsing option or equivalent shared error contract is
  sufficient; do not broaden unrelated GET semantics. Amend P01-T02 to extend
  the existing raw-form outcome matrix with malformed response JSON for 2xx
  and status-bearing non-2xx responses for both raw families.
* Action owner: Planning parent specifies the contract; implementation owner
  applies it within P01-T01/P01-T02.
* Exact resolving evidence: Revised plan/details explicitly separate transport
  lock release from history-barrier clearance. Existing shipped-handler tests
  assert retained input, uncertainty/history feedback, no second POST before
  authoritative recovery, and a released transport lock after parse rejection;
  ordinary structured refusal still permits correction. Extend an existing
  browser outcome matrix for migrated raw-handler malformed-response behavior,
  with axe on its new reachable feedback state. Use existing methods/helpers
  or the already authorized additions; no additional test budget or removals.
* Decision route: Direct planner correction. Existing requirements already
  demand preservation of raw refusal/history behavior; no user decision.

<!-- rpi:critique id=PC-002 -->
### PC-002 [Medium]: The planned heavyweight lock uses a prohibited temporary path

* Related IDs: P02-T01; nonblocking shared admission, 40-minute retry limit and
  execution filesystem constraints.
* Evidence: P02-T01 explicitly prescribes flock admission using
  /tmp/ama-rpi-heavy.lock. The supplied execution instructions forbid any file
  operations in /tmp or other temporary directories. The plan's external
  evidence requirement does not make the lock-file operation permissible.
* Concern: Following the phase literally would violate the execution boundary.
  Merely selecting a new per-worktree lock would also fail to serialize with
  other workers using the existing shared admission protocol.
* Impact: Validation either cannot legally start or may overlap another heavy
  run if an isolated replacement lock is treated as shared admission.
* Smallest useful change: Replace the forbidden path with an established,
  permitted non-temporary shared lock location/protocol used by all relevant
  contenders. Preserve nonblocking acquisition and the maximum 40-minute
  admission retry. State explicitly that, if interoperable permitted admission
  cannot be established, heavy checks remain Blocked and no passing evidence
  is claimed. Do not silently relocate only this worker's lock or fall back to
  Azure, skipped checks or a publication claim.
* Action owner: Planning parent, coordinating shared admission with the owning
  validation coordinator if necessary.
* Exact resolving evidence: P02-T01 records the permitted common admission
  location/protocol and its interoperability basis, or an explicit blocked
  validation condition. Later evidence records actual acquisition or the
  admission blocker without temporary-directory operations.
* Decision route: Direct planner correction to comply with existing constraints;
  no new user decision or expanded authorization is required.

## Strengths and Residual Risk

* Lock ownership below replaceable DOM and capture at replacement time address
  the actual reproduced failures rather than merely disabling another button.
* Immutable proposal identity/revision recovery and copy-only orphan drafts
  preserve human review boundaries without applying stale evidence.
* Action/target independence must include non-path discriminators at sibling
  callers, such as chat proposal capability and regulatory turn identifiers;
  the existing action/resource-identifier requirement covers these, so they
  are implementation audit obligations rather than an additional finding.
* Queue helper reuse must genuinely pass queue session ownership through
  snapshot, reconciliation and discard, rather than relying on caseSession
  being present. This is already required by the explicit queue-session plan.
* No automated browser or axe result establishes human usability, complete
  accessibility conformance or deployed acceptance. Those limitations and
  publication gates remain explicitly retained.

## Questions or Blocking Evidence Gaps

* No significant or divergent user decision is outstanding.
* Permitted interoperable heavy-check admission is not established by the
  supplied materials; PC-002 requires resolution or honest blocking before
  those checks, not a new research cycle or another critique.

## Limitations

* No tests, browser, scanner, heavy gate, external fetch or nested agent ran.
  Source observations are static evidence, not fresh reproductions.
* No secrets, environment files, private datasets or Azure were accessed.
  No remote writes, commits or source/plan edits were performed.
* Supplied W1 retrieval was treated as supplied research provenance, not a fresh
  independent Web Interface Guidelines review. The later implementation Review
  retains its planned fresh-fetch obligation.
* Only this critique artifact was intentionally written. Existing untracked
  round-eight inputs were read in place and left untouched.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: Planning parent.
* Smallest next action: Apply the strict raw-response parse contract and
  regression matrix extension, then reconcile PC-002's shared admission
  prerequisite. Preserve all locked test/removal/addition constraints.
* User response required: No.
* This sole critique is complete; revise directly and retain its original
  Revise outcome. Do not launch another critique for these direct corrections.

## Artifacts

| Path | Description |
| --- | --- |
| .copilot-tracking/plans/2026-10-29/case-journey-526-round8-plan.md | Candidate plan assessed |
| .copilot-tracking/details/2026-10-29/case-journey-526-round8-phase-details.md | Candidate execution details assessed |
| .copilot-tracking/research/2026-10-29/case-journey-526-round8-research.md | Supplied C1-C6/W1 evidence |
| .copilot-tracking/reviews/logs/2026-10-29/case-journey-526-round7-review.md | Preserved prior independent Review |

## Next Steps

Planning parent applies PC-001 and PC-002 directly, records disposition without
rewriting this critique, and continues the authorized implementation and
independent Review subject to permitted admission. No user action is required.
