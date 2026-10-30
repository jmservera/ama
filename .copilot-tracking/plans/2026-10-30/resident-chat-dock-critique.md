---
title: Resident chat fallback and dock final-candidate critique
ms.date: 2026-10-30
---

## Metadata

* Task ID: resident-chat-dock-520-563
* Critique date: 2026-10-30
* Plan: .copilot-tracking/plans/2026-10-30/resident-chat-dock-plan.md
* Phase details: .copilot-tracking/details/2026-10-30/resident-chat-dock-phase-details.md
* Critique execution status: Complete
* Execution bound: one final-candidate critique; no subsequent critique requested.

## Inputs and Criterion Boundary

* Caller requirements: local-only fallback investigation/fix, tests, accessible
  resident resizing and full right-edge docking, ordered RPI, Refs #520 and
  Refs #563. No live AI, Azure, live sign-in, ledgers, credential inspection,
  push, heavy validation, source edits or additional artifacts.
* Evidence: supplied plan, phase details and
  .copilot-tracking/research/2026-10-30/resident-chat-dock-research.md,
  including C1-C7 and W1. Targeted source checks covered
  src/api/src/zava_forward/api/resident_demo/chat.py,
  src/api/src/zava_forward/api/resident_demo/aoai.py,
  src/api/src/zava_forward/api/resident_demo/app.py,
  src/api/src/zava_forward/api/resident_demo/web/assistant.js,
  src/api/src/zava_forward/api/web/chat-widget.js,
  src/api/src/zava_forward/api/web/chat-widget.css,
  src/api/tests/test_resident_chat_api.py,
  src/api/tests/test_resident_aoai.py,
  src/api/checks/resident_generated_answer_browser_check.py,
  tools/rpi-checks.py and relevant component validation guidance.
* Repository context: case-study original/addendum and knowledge-base index/
  memory read. Memory is context, not evidence. Existing untracked RPI inputs
  were left unchanged on feat/resident-chat-dock-520.
* Locked decisions: canonical test ownership, at most five added unit methods,
  no removals, at most one focused browser geometry/keyboard helper, no generated
  runtime sources, optional persistence resolved to none, resident-only opt-in,
  unchanged employee defaults, default-off activation and existing model limits.
* Assessment covers AC1-AC4 and P01-P03, their dependency ordering, safety,
  privacy, geometry, focus, regression evidence and completion boundaries.
  It assesses implementation credibility, not implementation success or live
  configuration. Supplied research findings are not new executed observations.

## Coverage Assessment

| Requirement, research, phase, or task ID | Coverage | Evidence or concern |
| --- | --- | --- |
| Local-only scope; Refs #520/#563; C1-C5 | Covered | No new retrieval, activation, model client, authority or live-readiness claim. |
| AC1; C1/C2; P01-T01 | Covered | Complete-message grammar, original-text hazard priority, exact envelopes and hostile prefix/suffix HTTP tests with no reservation/model call. |
| AC2; C3/C4; P01-T02 | Covered | Fixed known-reason mapping and generic unknown fallback; original rules/help, grounding, IDs, parsing, accounting and limits retained. |
| AC3; C6/W1; P02-T01 | Partial | Native controls, viewport bounds, full-edge dock and launcher restoration are specified; scroll-preservation transition contract needs PC-003. |
| AC3; P02-T02; locked test budget | Partial | Actual local HTTP/scripted adapter, external blocking, keyboard/pointer, viewport/text/short-window and latest-response coverage are credible; PC-003 adds assertions within the existing helper budget. |
| AC4; P03-T01/P03-T03 | Partial | Required checks and honest missing prerequisites are named, but the specified lock cannot be used under the current no-temporary-directory constraint: PC-002. |
| Ordered RPI; P03-T02 | Partial | Research, planning, critique, implementation and independent Review are ordered; unresolved material Review findings need a completion gate: PC-001. |
| Canonical/generated targets; removals; no widening | Covered | Canonical files are src/api/tests/test_resident_chat_api.py and src/api/tests/test_resident_aoai.py; browser harness is src/api/checks/resident_generated_answer_browser_check.py. No test removals or generated runtime edits are authorized. |

## Verdict

* Verdict: Revise
* Severity counts: Critical 0; High 2; Medium 1; Low 0.
* Rationale: the technical scope is bounded and source-supported. Three direct
  planner corrections are needed to prevent unsafe completion claims,
  prohibited validation execution and an untested scroll-intent regression.
  None requires reopening the locked test targets, removals or change budget.

## Findings

<!-- rpi:critique id=PC-001 -->
### PC-001 [High]: Review findings lack a material-defect completion gate

* Related IDs: AC4, P03-T02, full ordered RPI requirement.
* Evidence: phase details P03-T02 says "Findings route to later work, not
  repeated Review", followed by the local commit; the plan supplies no
  disposition rule distinguishing blocking defects from optional follow-up.
* Concern: this permits a fail-closed routing, privacy, geometry or keyboard
  defect identified by the one independent Review to be deferred while the
  task proceeds as complete. Preserving an original failed Review is correct;
  treating its material defects as automatically deferrable is not.
* Impact: passing tests or a gate receipt could be presented as completion
  despite contrary independent evidence.
* Smallest useful change: retain the single Review and its original outcome.
  Require material in-scope findings to be corrected with targeted regression
  evidence and explicit disposition, or leave the candidate Not accepted/
  Blocked. Only nonblocking improvements may move to later work. Do not
  silently convert the original Review to a pass or schedule a critique loop.
  A local evidence commit, if made with unresolved findings, must remain
  explicitly an unaccepted candidate rather than completion evidence.
* Action owner: planning parent; implementing parent owns later dispositions.
* Exact resolving evidence: revised P03-T02 and completion criteria state the
  rule above; the later Review/change records retain each finding and original
  outcome, cite its fix/test or blocking status, and make no acceptance claim
  for unresolved material defects.
* Decision route: direct planner correction. No user decision is needed to
  enforce existing correctness/privacy/accessibility requirements. An eventual
  proposal to accept a material deviation is outside automatic authorization.

<!-- rpi:critique id=PC-002 -->
### PC-002 [High]: Planned validation writes a prohibited temporary-directory lock

* Related IDs: AC4, P03-T01, P03-T03, local-only validation boundary.
* Evidence: phase details P03-T01 requires flock on a temporary-directory
  shared lock. P03-T03 requires the gate's native lock. In tools/rpi-checks.py,
  heavy_lock fixes that same lock location at line 2273. Current execution
  instructions prohibit temporary-directory file operations. Existing tests
  also use tempfile.TemporaryDirectory, for example
  src/api/tests/test_resident_chat_api.py.
* Concern: the planned command path is not executable as written under the
  current restriction. A fresh external output directory alone does not
  relocate the native lock or default test scratch directories.
* Impact: implementation could attempt prohibited writes or falsely report
  that required validation was attempted/completed within authority.
* Smallest useful change: make the conflict an explicit pre-execution
  prerequisite. Specify permitted project-relative scratch/cache settings for
  commands that support them, without committing generated outputs. Preserve
  the coordinated shared-lock requirement: do not substitute a private lock,
  bypass locking or patch the gate as part of this feature. Since the native
  gate lock cannot be redirected by its current CLI, mark that gate Blocked
  before invocation under present restrictions. Do not infer cloud authority
  or invent a successful receipt.
* Action owner: planning parent.
* Exact resolving evidence: revised P03-T01/P03-T03 name the permitted scratch
  policy, identify the immutable native-lock blocker and state that no
  prohibited command will execute. Later validation records distinguish
  performed checks from unperformed blocked checks and do not claim a complete
  gate or verified final receipt.
* Decision route: direct planner correction to honor the current restriction.
  Changing the execution restriction or shared gate implementation would be a
  significant separate decision and is not required or authorized here.

<!-- rpi:critique id=PC-003 -->
### PC-003 [Medium]: Resize/dock tests do not establish preservation of scroll intent

* Related IDs: functional sizing requirement, AC3, C6, P02-T01/P02-T02.
* Evidence: the plan promises retained "scroll intent"; details test long-reply
  readability by scrolling and draft/thread preservation, but not log position
  across resizing/docking. Existing chat-widget.js determines following from
  scroll geometry in following(), preserves it around selected mutations in
  preserveBottom(), and unconditionally calls bottom() on open().
* Concern: CSS size changes alter log.clientHeight without the existing
  mutation helper. Unchanged message content and a scrollable log do not prove
  that a reader remains on the same passage or that a following reader stays
  at the latest reply. Merely scrolling to a screenshot target can hide this.
* Impact: a resident reading earlier guidance may lose position when enlarging
  or docking; a resident following replies may no longer see the latest text.
* Smallest useful change: define the transition contract for range input,
  docking and undocking: preserve the visible historical passage for a reader
  who is not following, and keep a following reader at the bottom, within a
  stated browser-layout tolerance. Keep focus on the operated native control.
  Explicitly distinguish reopen's existing bottom behavior if it is retained.
  Add both reader-state assertions to the already-budgeted geometry/keyboard
  helper; no new helper, suite, unit method or runtime-generated file is needed.
* Action owner: planning parent; implementing parent owns helper assertions.
* Exact resolving evidence: P02 details specify both reader states and reopen
  semantics; the existing browser harness records before/after passage or
  offset/anchor evidence, bottom-distance checks and focused-control assertions
  across size/dock/undock transitions, alongside unchanged draft/thread checks.
* Decision route: direct planner correction implementing the already-confirmed
  scroll-intent requirement; no significant or divergent user decision.

## Strengths and Residual Risk

* Admission remains finite and whole-message matched. Hazard detection on
  original text, protected intent priority and hostile-envelope HTTP tests
  avoid broadening the model's authority to solve a wording problem.
* The adapter already supports real generated prose using limited projected
  grounding. Reusing its schema/source/finish/usage/expiry checks is preferable
  to new retrieval or an independent client.
* Fixed diagnostics must remain an allowlisted code-to-label mapping on both
  answer entry points. Unknown reason strings and exception payloads must
  never become labels or logs. Existing sentinel/privacy and invalid-output
  tables provide suitable extension points within the locked budget.
* Native range controls avoid drag-only resizing. Full top/right/bottom dock,
  disabled docked-height control, launcher restoration before focus return,
  employee opt-in isolation, safe-area padding and no resize animation form a
  credible implementation direction.
* Final geometry evidence must check control/composer reachability and internal
  scrolling with sizing details expanded at short heights/enlarged text, not
  just the outer panel box. The existing P02 short-window/readability
  commitments support this without widening scope.
* Local scripted HTTP/browser evidence does not establish actual-model
  quality, live configuration repair, human usability, AT conformance or legal/
  operational approval. The plan expressly retains these boundaries.

## Questions or Blocking Evidence Gaps

* No unresolved user choice prevents these direct corrections.
* The native gate lock is a known execution blocker, not evidence that the
  feature itself fails. No gate success can be inferred while it remains.
* No additional research cycle is required by the supplied evidence.

## Limitations

* No tests, linters, browser sessions, scanners, gate or live service calls
  were executed during this critique.
* No credential, ledger or private dataset files were inspected.
* W1 was considered as supplied research evidence, not freshly retrieved web
  guidance. Fresh web-rule retrieval remains an implementation/review duty.
* Proposed changes do not exist yet; this is a plan critique, not exact-head
  implementation acceptance. Only the named critique artifact was written.

## Recommended Next Action

* Highest-impact finding: PC-001.
* Action owner: planning parent.
* Smallest next action: dispose PC-001-PC-003 directly in the plan/details,
  preserve this original critique, then continue only within authorized local
  implementation and validation boundaries.
* User response required: no.

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/plans/2026-10-30/resident-chat-dock-plan.md](.copilot-tracking/plans/2026-10-30/resident-chat-dock-plan.md) | Reviewed final-candidate plan |
| [.copilot-tracking/details/2026-10-30/resident-chat-dock-phase-details.md](.copilot-tracking/details/2026-10-30/resident-chat-dock-phase-details.md) | Reviewed phase details |
| [.copilot-tracking/research/2026-10-30/resident-chat-dock-research.md](.copilot-tracking/research/2026-10-30/resident-chat-dock-research.md) | Supplied research evidence |
| [.copilot-tracking/plans/2026-10-30/resident-chat-dock-critique.md](.copilot-tracking/plans/2026-10-30/resident-chat-dock-critique.md) | Complete one-pass critique; Revise |

## Next Steps

The active planning parent should make the three direct corrections and record
their dispositions without requesting another critique. No user action is
required. This bounded critique stops here; it does not invoke another stage.
