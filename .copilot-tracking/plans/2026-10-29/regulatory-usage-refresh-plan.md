<!-- markdownlint-disable-file -->
# RPI Plan: Nonblocking regulatory usage refresh

## Task Metadata

* Task ID: reg208-pr506-usage-refresh-2026-10-29
* Task slug: regulatory-usage-refresh
* Planning status: Ready; independent critique Complete / Pass
* Plan date: 2026-10-29
* Phase details: .copilot-tracking/details/2026-10-29/regulatory-usage-refresh-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/regulatory-usage-refresh-plan-critique.md

## Executive Summary

Release the lookup form when its answer is displayed, rather than waiting for
the secondary audit-usage GET. Reuse the existing caught usage helper and
raw-field cleanup guard. Add a deferred-response regression in the existing
shipped-JavaScript test module, update the API usage guide, and commit locally.

### What You May Not Know

The usage helper already reports errors independently. The current regression
returns usage immediately, hiding the delay. The shared async-action wrapper
also follows the submit handler promise, so merely enabling the button before
an awaited refresh would leave the form busy. System Python lacks installed
project distributions; restore dependencies only after a failed chosen test.

### Unresolved Decisions or Blockers

No scope decision is unresolved. Dependency restoration is a local prerequisite,
not authority for cloud access, publication, or operational acceptance.

## User Decisions and Requirements

* Fix the single Copilot finding on PR #506, Refs #208, in the named branch/worktree.
* Answer display must release lookup controls and clear unchanged submitted text
  without waiting for usage; refresh rejection must be handled.
* Add a focused regression that fails without the fix; run relevant tests,
  Node syntax, and Ruff when Python changes.
* Complete all four RPI phases with dated artifacts and a local Conventional
  Commit containing the specified Copilot coauthor trailer.
* Do not push, use az, touch other worktrees, or hand-edit rubric scores.

## Goals

* Separate answer completion from advisory usage latency without changing
  storage, authorisation, wording, dirty-field protection or human boundaries.

## Scope and Non-Goals

In scope: chat.js handler, test_case_journey.py regression, the existing API
usage paragraph, and dated tracking evidence. No CSS, templates, API behavior,
new framework, broader review finding, cloud command, publication or merge.

## Functional Requirements

* On answer success, retain rendered answer/status, clear only the submitted
  unchanged field, launch existing caught refresh without awaiting, and execute
  existing finally cleanup for button/focus recovery.
* Usage success updates its own live text; usage failure reports there without
  changing the successful answer status or disabling lookup.
* Pending answer still suppresses duplicate submit; answer/thread failure
  preserves input and recovers controls.

## Non-Functional Requirements

* No timer-based production workaround or new dependency.
* Deterministic deferred promises, not wall-clock sleeps, prove nonblocking
  completion; a bounded subprocess timeout prevents hung tests.
* Node strict unhandled rejection behavior makes escaped rejection fail.
* Existing source distributions must be installed before application tests;
  no legacy PYTHONPATH workaround or private dataset is permitted.

## Acceptance Criteria

* Before usage settles, the answer is present, submission has settled,
  button is enabled, focus is back on input, and unchanged input/dirty marker
  have cleared.
* Changed input and dirty marker survive answer success.
* Both delayed usage success and failure preserve available controls and the
  successful answer; failure is explicit and no unhandled rejection occurs.
* Regression fails against baseline and passes after the fix.
* Relevant existing chat/journey/regulatory tests, Node syntax and focused Ruff
  pass, or exact blockers are recorded without a false acceptance claim.

## Implementation Context Record

| Item | Record |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-29/regulatory-usage-refresh-research.md; executed, Ready; C1-C7, W1 |
| Details | .copilot-tracking/details/2026-10-29/regulatory-usage-refresh-phase-details.md |
| Critique | One fresh independent final-candidate assessment, Complete / Pass |
| Changes | .copilot-tracking/changes/2026-10-29/regulatory-usage-refresh-changes.md |
| Continuation | Explicit full-loop parent orchestration; local commit only |

## Sources

* Research C1/C2: handler/helper lifecycle and existing error owner.
* Research C3/C4/C5: executable JS conventions, field guard and action wrapper.
* Research C6/C7: owning guide and missing system dependencies.
* Caller request: exact scope and validation/commit boundaries.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Prove and fix answer-completion lifecycle

* Dependencies: one final-candidate critique, required local dependencies.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add deferred usage regression and capture red result

* Owner: src/api/tests/test_case_journey.py, existing DOM/shipped_helpers.
* Add exactly one Python unittest method with success/failure and edited-field
  scenarios; remove none. Maximum additions: one test method, no new test file,
  fixture library or generated checked-in test.
* Exercise shipped chat.js and shipped field helpers, not a copied implementation.
* Keep existing semantic/raw-field regression unchanged.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Decouple refresh and update owning guide

* Clear submitted unchanged input before nonawaited refreshUsage; retain its
  catch and the handler's finally. Update only the API usage paragraph.
* Canonical targets: chat.js and src/api/README.md. Generated targets: none.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Validate and reconcile implementation evidence

* Run focused unittest plus relevant existing chat/regulatory/journey modules;
  node --check chat.js; Ruff check/format check on touched Python.
* Capture red/green commands/results and reconcile all plan/detail markers.
* One independent post-implementation Review follows, without looping back
  to implementation inside this task.

## Dependencies

* Native Node available. Project distributions and Ruff absent from system
  environment; use a new local venv after missing-dependency test failure.
* Existing DOM fixture is sufficient for the handler and field helper.

## Critique Disposition

The single independent critique completed with verdict Pass and no PC findings.
No plan correction or significant user decision was required. Passing critique
does not establish execution, publication or human approval.

## Follow-Up Items

* None.

## Handoff

Implementation record: .copilot-tracking/changes/2026-10-29/regulatory-usage-refresh-changes.md.
All P01 tasks completed. Implementation evidence is reconciled and ready for
the single independent Review. Publication gate, hosted checks and required
human approvals remain unperformed because this is local-only work.
