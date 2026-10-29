---
title: Case journey round five correction research
description: Focused evidence for PR 529 chat dirtiness, proposal readiness and summary announcements
ms.date: 2026-10-28
---

## Brief and controls

* Task: `526-pr529-round5-20261028`; slug: `case-journey-526-round5`.
* Purpose: correct the three unresolved Copilot threads in PR #529, Refs #526.
* Scope: changed employee web files and their dirty-state, live-region and
  readiness/disabled siblings; focused unit and real-browser regressions.
* Output mode: convergence; posture: focused, selected from named failure evidence.
* No Azure, secrets, private data, framework redesign, closing issue keywords,
  thread replies/resolution or remote publication without the complete gate.
* Heavy checks require nonblocking flock admission, at most 40 minutes.
* Evidence root: `.copilot-tracking/research/2026-10-28/`.
* No interaction required: explicit full-loop direction continues the parent's
  automatic session on the same workstream.

## Extensions and participation

Repository case-study, knowledge-base and branch guidance selected; original,
addendum, index and owner memory read. `rpi-research` selected for phase protocol;
`web-design-guidelines` selected and current source retrieved before web edits.
Design-overhaul skills skipped: bounded behavioral fixes preserve Fluent.
Inline research selected because all uncertainties share the same state lifecycle;
no separate researcher claimed. Independent critique and final Review remain
separate later gates.

## Opening evidence

* C1: `src/api/src/zava_forward/api/web/app.js:210`: shared navigation and unload
  dirty guard includes live controls and session pending fields.
* C2: `src/api/src/zava_forward/api/web/chat.js:45`: ordinary Ask clears input at
  dispatch; regulatory Ask clears on success using trimmed comparison. Neither
  removes the dirty marker.
* C3: `src/api/src/zava_forward/api/web/assistants.js:42`: ready and own-verification
  predicates guard Accept/Edit but not Save edited proposal.
* C4: `src/api/src/zava_forward/api/web/case-workspace.js:67`: asynchronous summary
  value has no live semantics and counts replaces unchanged content repeatedly.
* W1: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
  retrieved 2026-10-28: asynchronous updates need polite live announcements,
  native semantics, preserved unsaved changes and disabled request controls.
* W2: GitHub GraphQL `repository.pullRequest(529).reviewThreads`, retrieved
  2026-10-28: exactly three unresolved IDs `PRRT_kwDOUU8JX86xWl_S`,
  `PRRT_kwDOUU8JX86xWmAC`, `PRRT_kwDOUU8JX86xWmAa`.

## Questions and cycle one

1. How can both question paths retire only submitted text and retain later edits?
2. Which proposal guards must apply to restored editor submission?
3. How can the always-visible summary announce transitions without repeat updates?
4. Do sibling paths in changed web files share these defects?

### Wider wave

Initial sources identify shared dispatch snapshots, cached-draft reconciliation,
retained tabs and proposal revision-bound recovery as the existing contracts.
Inspect both question handlers (located in chat.js, not app.js), all proposal
actions, async count publishers and related review controls before selecting
changes. No source changes during this phase.

### Deeper wave

* C5: `src/api/src/zava_forward/api/web/app.js:777`: immutable snapshots and
  caseFieldUnchanged already compare raw values; reuse them, not trimmed text.
  rememberCaseFields retires cached entries when their live field becomes clean.
* C6: `src/api/checks/case_journey_browser_check.py:811`: deferred proposal
  pagination and unavailable variants already cover the summary transitions.
  Preserve the 38-scan gate contract and add assertions within these states.
* C7: `src/api/checks/assistants_browser_check.py:95`: real verified proposal
  editor, revision recovery and overlap fixtures exist; extend rather than add
  another harness. Add opt-in pinned axe scans without breaking no-argument use.
* C8: `src/api/src/zava_forward/api/web/panels.js:143` and
  `src/api/src/zava_forward/api/web/ops.js:32`: mutation paths use shared
  snapshot-based refresh; challenge drafts retain their complete form and
  compare dispatched values separately.
* Reflection: all three defects are confirmed. Fix handlers in chat.js and use
  shared snapshot primitives rather than changing app.js's dirty event listener.

### Contrarian wave

* Clearing dirty flags unconditionally loses edits during requests. A trimmed
  comparison also loses a later whitespace edit. Retain raw dispatch snapshots
  and clear only after success, preserving input on thread-create/ask failure.
* Only hiding the stale editor loses recovery; disable submission, not the
  textarea. Check all ready predicates and other-person verification, not stale
  alone. Reject intentionally remains available when readiness is false.
* A live dd containing the navigation button would announce/reinsert the button
  on every count event. Keep a dedicated atomic polite text span inside the
  semantic dd, outside the button, and update it only when text changes.
* Counts fires both from MutationObserver and explicit ai-review-change. Equal
  text must not trigger a new live mutation. AI panel status communicates
  availability separately; summary should announce only counts, not repeat that
  entire status text. Existing local-document count and hidden-tab paths remain.
* Sibling review includes app.js review/refresh/recovery, assistants actions,
  both chat forms and their logs/statuses, ops quality/checklist and panels
  finance/resident/challenge paths. External resident/funding wording remains a
  separate unsaved manual draft after reviewing AI, intentionally not consumed
  by the review action. No new unrelated workflow/approval change is justified.

## Disposition

Research disposition: executed. Planning Readiness: Ready.
Accepted: shared exact-value cleanup after success, identical proposal button
guard, dedicated deduplicated count live text. Rejected: dispatch-time clearing,
trim-only equality, readonly/hidden restored editor, whole-summary live wrapping.
Questions 1-4 answered by C1-C8/W1-W2. No further cycle needed: complete in-scope
lifecycle inspected and alternatives tested against failure contracts.
Residuals: actual screen-reader speech and human staff acceptance cannot be
established by DOM/axe checks. Complete publication gate requires prohibited az.
Self-check: sources, constraints, waves, alternatives, readiness and handoff
recorded; inline work accurately distinguished from independent later review.
