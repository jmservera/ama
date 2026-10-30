---
title: Chat widget fix cycle 3 independent implementation review
description: Bounded post-implementation RPI Review for issue 550 and PR 556
ms.date: 2026-10-29
---

## Scope and Evidence

* Task ID: issue-550-pr-556-fix-cycle-3.
* Review date: 2026-10-29.
* Scope: one independent Review of the six-file working-tree source diff against
  34f7f8fc843d00c66fc277ea831ea9a978897db6, canonical dated artifacts and supplied
  external validation evidence. No whole-issue or whole-PR acceptance.
* Canonical artifact slug: chat-widget-550-fix-cycle-3.

## Opening Review State

* Interpreted goal: assess current-intent preservation through delayed loading,
  status and error geometry changes, without overriding upward reading or
  history focus; verify the unmasked two-site regression and PC-001 disposition.
* Scope: P01/P02 implementation and validation; P03 Review only. Local commit
  remains the parent's pending P03 action.
* Evidence readiness: named research, plan, details, original Revise critique,
  changes and state exist. Six source modifications match the supplied boundary.
  External evidence is supplied and awaits inspection, not presumed passing.
* Acceptance basis: current bottom/focus sampling, shared predicate, 200 ms
  lifecycle preservation, bottom-before-send positive regression with no later
  repositioning, retained negative cases, test budgets and fresh scoped Web
  Interface Guidelines review.
* First comparison boundary: reconcile plan/details/changes and PC-001, then
  inspect only the six changed files and necessary immediate context.
* Active read-only boundaries: only this review record may be written; no
  source or other artifact edits, subagents, publication, full gate, push,
  Azure operation or latest.json change.
* Initial blockers: none identified. Active topic feat/chat-widget-550 matches
  open PR 556 targeting main; existing dirty work is supplied review input.
* Guidelines freshly fetched successfully on 2026-10-29 from
  https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
  before changed-web inspection.

## Compared Artifacts

* Research: .copilot-tracking/research/2026-10-29/chat-widget-550-fix-cycle-3-research.md.
* Plan: .copilot-tracking/plans/2026-10-29/chat-widget-550-fix-cycle-3-plan.md.
* Phase details: .copilot-tracking/details/2026-10-29/chat-widget-550-fix-cycle-3-phase-details.md.
* Original critique: .copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-fix-cycle-3-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-10-29/chat-widget-550-fix-cycle-3-changes.md.
* State: .copilot-tracking/rpi-sessions/2026-10-29/chat-widget-550-fix-cycle-3-state.json.
* External evidence root, relative to this worktree:
  ../../../.copilot/session-state/84897398-9719-4cb4-b217-1a3237c9cbe4/files/fix-cycle-3.
  Inspected chat-tests.log, chat-tests-browser-enabled.log, static-final.log,
  browser-attempt1.log, browser-attempt2.log, browser-attempt2/results.json,
  negative-controls.log and negative_checks.py.
* Source boundary: src/api/README.md;
  src/api/src/zava_forward/api/web/chat-widget.js;
  src/api/src/zava_forward/api/web/chat.js;
  src/api/src/zava_forward/api/resident_demo/web/assistant.js;
  src/api/tests/test_chat_widget_focus.py;
  src/api/checks/chat_widget_browser_check.py.
* Immediate context: widget CSS, shared browser lifecycle and existing focus
  harness; original case study, relevant addendum resident-service boundary,
  reference index, owner memory, and Fluent/WCAG/plain-content baselines.
  Memory was context only. Unrelated callback/regulatory implementations were
  not audited.

## Execution Status

* Execution status: Complete.
* Exactly one independent bounded post-implementation Review executed.
  All six changed files, supplied artifacts and named validation evidence were
  assessed. Focused tests and three JavaScript syntax checks also ran directly.
* This is Review execution status, not completion of the parent's pending
  local commit, publication gates or whole issue #550.

## Plan-to-Change Reconciliation

| Current plan scope | Changes evidence | Current-state reconciliation | Gap or rationale |
| --- | --- | --- | --- |
| P01 / P01-T01 | P01 Implementation | Reconciled | Shared predicate and guarded loading/status/error mutations implemented; scoped adapters use the setter. |
| P01 regression contract | P01 Implementation and Sensitivity | Reconciled | One seven-mode unit method and two browser modes; no test removal or new test owner. |
| P02 / P02-T01 | P02 Validation | Reconciled | Requested discovery, final browser-enabled discovery, static/type checks, both sites and three negative controls have supplied results. |
| PC-001 disposition | Amendments and Divergences | Reconciled | Resident empty-status predecessor handled before loading sampling, with explicit send/status assertion. |
| P03 / P03-T01 | P03 Review and Persistence | Reconciled pending work | Pre-Review pending markers were accurate; this record completes Review only. Parent still owns local persistence and subsequent marker/state updates. |
| Follow-Up Items | P03 publication boundary | Reconciled | Separate publication, exact-head and hosted/human gates remain outside this local correction. |

## Completed Work Assessment

| Related marker | Files | What changed and why | Completion evidence | Assessment |
| --- | --- | --- | --- | --- |
| P01-T01 geometry | src/api/src/zava_forward/api/web/chat-widget.js | following() preserves the existing <=1 CSS px and history-focus predicate; preserveBottom() samples immediately before each controlled synchronous layout mutation. | Loading reveal/hide, status setter and grouped inline error changes use the helper; message() uses the same predicate. | Conformant; no cached send-time intent, observer, new listener or smooth scrolling. |
| P01-T01 adapters | src/api/src/zava_forward/api/web/chat.js; src/api/src/zava_forward/api/resident_demo/web/assistant.js | All shared-widget status writes use setStatus(); resident status ID uses ui.status.id. | Scoped assignments inspected in both submit/success/setup/reset paths; unrelated callback/regulatory status remains unchanged. | Conformant; fixes PC-001 and the adverse startup failure without changing API or approval semantics. |
| P01-T01 regression | src/api/tests/test_chat_widget_focus.py | One added method models loading/status/error geometry and seven current-intent modes. | Covers following, upward before/after reveal, log focus before, Sources focus before/after, return to bottom, timer cancellation and disposal. | Conformant; existing four methods retained; five focused methods pass directly. |
| P01-T01 browser | src/api/checks/chat_widget_browser_check.py | Existing positive case now positions before send only; two added modes interact before reveal under a paused clock. | Both sites assert send/status and delayed-loading bottom distance, then final reply <=2 px; all six negative modes assert <=1 px reply displacement and exact active element. | Conformant; original five modes remain, and the positive path never writes scrollTop or refocuses after send. |
| P01-T01 guide | src/api/README.md | Documents geometry preservation and the unmasked delayed regression. | Matches implementation and owned browser behavior. | Conformant; no broader acceptance claim. |
| P02-T01 | Supplied external evidence | Validate behavior and regression sensitivity. | Final 109-test browser-enabled result has zero skips; final two-site browser result passes; three negative controls fail on bottom geometry as intended. | Conformant within synthetic/local limits. |

Current-state sampling means an upward scroll or history focus acquired during
the delay disables following at reveal and again at reply, while returning to
bottom with focus outside history enables following again. No helper moves
focus. Existing send-button-to-input handling, active/disposal guard, 200 ms
threshold, cancellation, disabled controls and aria-busy behavior are retained.
The browser's follow case fills the input, positions the overflowing log before
send, and relies on the existing busy focus behavior, not a compensating
post-loading action. Resident follow starts after a completed answer with empty
status and asserts eligibility after the synchronous send sequence.

## Implementation-Time Plan and Detail Update Assessment

| Affected scope | Update and reason | Trigger and user decision | Reconciliation | Assessment |
| --- | --- | --- | --- | --- |
| Functional Requirements / P01-T01 / six-file boundary | Include shared preserving status/error updates and both adapter owners. | PC-001 identified resident empty-to-nonempty status shrinking the log before loading sampling; preserves already confirmed two-site intent, no new user decision needed. | Current research explicitly supersedes initial status-API rejection; plan, details and changes describe the same correction. | Justified direct reconciliation, not an unaccepted divergence. |
| P01/P02 deterministic browser execution | Pause before reply_scroll, run exactly 200 ms after pre-loading actions, resume and reuse the clock later. | Timing must prove interactions preceded reveal rather than depend on machine speed. | Details and changes describe installed/paused clock and retained later 199/200 ms checks. | Compatible implementation detail, no scope expansion. |
| P01/P02 resident startup correction | Replace removed local alias reference with ui.status.id. | Original browser attempt failed at resident sign-in after the adapter change. | Changes preserve failure and identify correction; final source and attempt 2 agree. | Corrected coupled defect; no weakened assertion or hidden adverse outcome. |

## Critique and Material Revision Assessment

* Exactly one original critique remains preserved with verdict Revise and one
  High finding, PC-001. This Review does not relabel or replace that verdict.
* PC-001 is resolved by the reconciled status setter requirement, scoped adapter
  wiring, resident empty-status precondition and immediate post-send geometry
  assertion. Source, seven-mode unit geometry, two-site browser result and
  independent unguarded-status negative control support that disposition.
* Changes/state report reconciliation before source edits; current artifacts
  consistently reflect it. No contrary sequencing evidence was found.
* The adapter exception stays within the reconciled six-file boundary. Preserving
  the confirmed two-site acceptance required no significant/divergent decision,
  no second critique and no expanded active scope.

## Plan Follow-Up Assessment

| Follow-up | Why outside immediate scope | Owner / next action | Assessment and route |
| --- | --- | --- | --- |
| Publication and complete local gate, exact-head assessment, hosted checks and owner authorization | Explicit local-only authorization; no push or publication/full-gate execution permitted. | Parent/publication owner executes separately if publication is later authorized. | Open distinct follow-up, not a local defect or part of P01/P02 completion. |
| Human/assistive-technology and live acceptance | Constructed loopback applications and intercepted answers cannot establish real-user, screen-reader, live model or deployed-service acceptance. | Relevant acceptance owners obtain direct evidence before making those claims. | Explicit evidence limitation, not newly added implementation scope. |

## Scoped Web Interface Guidelines Report

Fresh source retrieved successfully before reading changed web files. Reviewed
all fetched rule categories against the changed behavior and necessary immediate
context; no framework, stylesheet, copy or public-page redesign is proposed.

### src/api/src/zava_forward/api/web/chat-widget.js

✓ pass

### src/api/src/zava_forward/api/web/chat.js

✓ pass

### src/api/src/zava_forward/api/resident_demo/web/assistant.js

✓ pass

Changed-scope assessment:

* Accessibility, forms and focus: native controls, names, live log/status/error
  regions, existing validation focus and keyboard/IME semantics are retained.
  No new autofocus or focus theft. Exact history focus is independently guarded
  from geometric bottom eligibility.
* Animation, touch and layout: no new animation, transition, gesture or layout
  style; existing reduced-motion and overflow handling remain. Browser evidence
  includes reflow, visible focus and retained keyboard/manual paths.
* Performance: required geometry reads happen in event/timer-driven mutation
  helpers, not a framework render loop. Each helper reads eligibility before
  its grouped writes and performs one conditional bottom write; no per-frame
  observer/listener, polling or unbounded new list work.
* Content and state: existing labels, plain-language guidance, advisory/consent
  boundaries, errors, empty states and generation/session guards are preserved.
  No new date/number formatting, navigation, URL state or destructive action.
* Images/media, hydration, locale, font loading and theming rules have no new
  applicable surface in these changes. Immediate context retains long-text
  wrapping and existing >50-message content-visibility handling.
* No changed-scope file:line violations found. Existing untouched copy such as
  the loading literal, and broader baseline design/Fluent gaps, are not findings
  introduced by this bounded correction. Local scans and code review do not
  establish complete WCAG, Fluent adoption or human acceptance.

## Findings

No substantive defects, unaccepted decision gaps or material evidence gaps found
within this supplied boundary. Severity counts: Critical 0; High 0; Medium 0;
Low 0. No RV finding is fabricated for the explicitly pending local commit or
separately gated publication/acceptance work.

## Defects

* None.

## Routed Findings

| Finding | Destination | Owner / next action | Reason |
| --- | --- | --- | --- |
| None | No rpi-implement, rpi-plan or rpi-research handoff | Parent continues pending local persistence. | No actionable implementation, decision or evidence defect found. |

## Residual Work

* Distinct publication and live/human acceptance follow-ups remain as above.
  They do not change this bounded implementation verdict.

## Blockers and Remaining Work

* Review blockers: none.
* Remaining active work: parent completes P03 local co-authored commit with
  privacy-safe GitHub identity and persists implementation/original dated
  evidence plus this review, then reconciles its state/markers. Review did not
  edit those artifacts or claim the commit already exists.
* No correction or second Review is requested or performed.

## Validation Evidence

Supplied log names below are relative to the external evidence root recorded
under Compared Artifacts. They were read, not rerun unless explicitly stated.

| Command / evidence | Scope | Status | Summary |
| --- | --- | --- | --- |
| Exact requested chat discovery; chat-tests.log | Existing chat tests | Passed with disclosed skip | 109 tests, OK, one existing opt-in browser skip. |
| ZF_BROWSER_TESTS=1 chat discovery; chat-tests-browser-enabled.log | Existing chat tests with browser opt-in | Passed | 109 tests, OK, zero skips. Expected synthetic fail-closed trace output is not an outcome failure. |
| Ruff check/format and isolated harness checks; static-final.log | API and browser harness | Passed, supplied evidence | All checks passed; 59 project files and one isolated harness file already formatted. |
| node --check, three changed JavaScript files | Widget and adapters | Passed directly | All three return success; independent syntax execution corroborates the changes record's static claim. |
| Existing mypy; static-final.log | API typing | Passed, supplied evidence | No issues in 112 source files. |
| Browser attempt 1; browser-attempt1.log | Constructed two-site browser run | Failed, preserved | Employee passed; resident startup remained Loading and sign-in stayed hidden. Changes attribute it to stale status.id after alias removal; final ui.status.id corrects that source path. |
| Browser attempt 2; browser-attempt2.log and results.json | Constructed employee/resident applications, intercepted edge cases, axe | Passed, supplied evidence | Both sites pass delayed following and retained focus/history checks; Chromium 156.0.8078.4. Final status passed. |
| negative-controls.log and negative_checks.py | Original 34f7f8fc widget, unguarded loading reveal, unguarded status mutation | Passed sensitivity assessment | All three fail with bottom-follow assertion; loading mutant fails at reveal, original/status mutant after status insertion. Compatibility fallback avoids a missing-setter error masking geometry sensitivity. |
| PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -p test_chat_widget_focus.py -q | From src/api, existing focus test owner | Passed directly | Five tests in 0.231 s, OK. No dependency installation. |
| git diff --check | Supplied working-tree diff | Passed directly | No whitespace errors. |
| Fresh Web Interface Guidelines source and three changed web files | Scoped changed-web review | Passed by inspection | No introduced scoped rule violation; not a whole-app conformance claim. |
| Complete publication gate / exact-head receipt / hosted approval | Publication | Not run, intentionally out of scope | Explicit prohibition for this Review/local cycle; no publication claim. |
| Live deployment/model, human/assistive technology and other browser engines | Operational/user acceptance | Not run / not established | Final browser receipt explicitly says live_model and human_assistive_technology not run; synthetic Chromium evidence cannot substitute. |

Review created no scratch copy, reran no negative-control script, started no
server, installed no dependencies and changed no source or other task artifact.

## Outcome

* Outcome: Conformant.
* Rationale: P01/P02 implementation and evidence satisfy the bounded delayed
  bottom-follow correction, preserve current upward/history-focus intent and
  resolve PC-001 without masking the regression. Pending P03 persistence is
  accurately disclosed, not misrepresented as implementation failure.
* This verdict does not close #550, approve all of PR #556, authorize deployment
  or replace human, hosted or complete local publication gates.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defect | None | No correction needed within reviewed scope. |
| Decision gap or invalid assumption | None | PC-001 direct disposition supported. |
| Material evidence gap | None | Sufficient local evidence for bounded verdict. |
| Non-blocking follow-up | Separate publication and acceptance work | Publication/acceptance owners when separately authorized. |

* Review execution: Complete.
* Outcome: Conformant.
* Validation coverage: supplied 109-test zero-skip final run, static/type checks,
  two-site Chromium/axe and three negative controls; direct five-test focus run,
  three JS syntax checks, diff check and fresh scoped guidelines review.
* Blockers: none for this Review. Parent's local commit remains pending.

## Artifacts

| Artifact | Description |
| --- | --- |
| [.copilot-tracking/research/2026-10-29/chat-widget-550-fix-cycle-3-research.md](.copilot-tracking/research/2026-10-29/chat-widget-550-fix-cycle-3-research.md) | Compared research and decision disposition |
| [.copilot-tracking/plans/2026-10-29/chat-widget-550-fix-cycle-3-plan.md](.copilot-tracking/plans/2026-10-29/chat-widget-550-fix-cycle-3-plan.md) | Compared current plan |
| [.copilot-tracking/details/2026-10-29/chat-widget-550-fix-cycle-3-phase-details.md](.copilot-tracking/details/2026-10-29/chat-widget-550-fix-cycle-3-phase-details.md) | Compared implementation and validation contracts |
| [.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-fix-cycle-3-plan-critique.md](.copilot-tracking/reviews/plans/2026-10-29/chat-widget-550-fix-cycle-3-plan-critique.md) | Preserved original Revise critique |
| [.copilot-tracking/changes/2026-10-29/chat-widget-550-fix-cycle-3-changes.md](.copilot-tracking/changes/2026-10-29/chat-widget-550-fix-cycle-3-changes.md) | Compared implementation and adverse/final evidence |
| [.copilot-tracking/rpi-sessions/2026-10-29/chat-widget-550-fix-cycle-3-state.json](.copilot-tracking/rpi-sessions/2026-10-29/chat-widget-550-fix-cycle-3-state.json) | Compared parent's pre-Review state |
| [.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-fix-cycle-3-review.md](.copilot-tracking/reviews/logs/2026-10-29/chat-widget-550-fix-cycle-3-review.md) | This single independent Review |

## Next Steps

Return this record to the parent for pending P03 local persistence and artifact
state reconciliation, without a second Review or publication. No user action or
corrective RPI command is required. Publication and human/live acceptance remain
separate later-owner actions, not defects in this correction.
