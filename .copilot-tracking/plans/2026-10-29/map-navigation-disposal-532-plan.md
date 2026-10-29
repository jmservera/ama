<!-- markdownlint-disable-file -->
# RPI Plan: Map navigation disposal correction

## Task Metadata

* Task ID: issue-532-pr-539-map-navigation-disposal
* Task slug: map-navigation-disposal-532
* Plan date: 2026-10-29
* Planning status: Ready; single independent critique Complete / Pass.
* Implementation status: Complete; all requested strict/unit/browser checks
  and exact old-JS negative control passed.
* Review status: single independent Review Complete / Conformant, zero findings.
* Phase details: .copilot-tracking/details/2026-10-29/map-navigation-disposal-532-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-29/map-navigation-disposal-532-plan-critique.md

## Executive Summary

Remove disposed map slots immediately and prevent their obsolete controls from
reopening a modal while All open cases waits for facets. Extend the existing
real-app map browser check at that exact pending boundary, and reload before
each session-expiry scenario so the full check reaches enlarged-font coverage.
Retain all existing map semantics, native controls and bounded fixture data.

### What You May Not Know

A synthetic 401 invalidates client me but not the server cookie. Reloading
recovers initialization without mocking application authentication. Same-document
navigation alone cannot do this or clear Overview filters and instrumentation.
The heavy lock was acquired nonblocking for every heavy run. Full API/core
units and complete browser coverage passed after correcting test readiness,
component import precedence, strict-CSP wait predicates and failure cleanup.
Original failed-run logs are preserved. Local commits are not publication.

## User Decisions and Requirements

* Correct both supplied Copilot findings on feat/map-fullscreen-532 / PR #539,
  Refs #532, using src/, not mvp/.
* Run Research, Plan, Implement and Review with dated committed artifacts.
* Run git pull --rebase first; completed from a clean worktree.
* Run API/core mypy, ruff check ., ruff format --check ., units with this
  worktree's src/test paths, and the relevant browser check.
* Hold flock -n /tmp/ama-rpi-heavy.lock for full suites. If busy, use targeted
  tests and explicitly report the restriction.
* Update scenario-manifest SHA-256 pins only when pinned inputs change.
* Conventional local commits with the supplied Copilot coauthor; no push, az,
  force-push, closing keywords or merge.

## Goals

* Prevent post-disposal map interaction before asynchronous destination rendering.
* Make the complete map browser check independently repeatable across scenarios.
* Preserve original evidence and record exact local verification limitations.

## Scope and Non-Goals

In scope: mapPanel disposal/expand guard, map browser check, focused source
contracts, API README and dated RPI records. No schema, backend authority,
authentication behavior, CSS redesign, fixtures, private data or remote change.

## Functional Requirements

* Disposal makes obsolete controls inert/disabled, removes their slot, retains
  modal/body-lock cleanup, and prevents retained expand callbacks reopening it.
* Pending-facets regression must attempt pointer activation at the former Expand
  position and retained toggle activation before releasing the request, then
  assert clean destination rendering.
* Each session-expiry iteration reloads the document before Coordinator
  navigation and installs instrumentation only in the initialized new document.

## Non-Functional Requirements

* Preserve keyboard/manual navigation, native dialog focus, session-expiry
  sequence invalidation after collapse and no late Leaflet mutation.
* All changed Python remains within strict API typing, without suppressions.
* Real loopback browser uses public constructed data and integrity-pinned axe;
  no external app requests, private working data or cloud dependency.

## Acceptance Criteria

* With facets held, the previous Overview remains but its map slot is
  disconnected/inert and the toggle disabled; pointer and retained event
  activation cannot create a dialog/body lock.
* After facets release All open cases renders with zero map slot/dialog and
  no body lock or uncaught JavaScript error.
* Both embedded/expanded session-expiry checks and 640px/32px-font coverage
  finish, retaining their current late-response assertions.
* Requested strict tooling passes for API and core. Full API/core units and
  browser run under one nonblocking lock if admitted; otherwise targeted units
  pass and unperformed checks remain explicitly blocked.
* Negative control restores only original app.js in an isolated served response
  (not the worktree), and the new pending-navigation regression fails. Run under
  admitted lock; do not weaken positive assertions to pass.
* Dated plan/details/critique/changes/Review reconcile actual execution. Original
  Review outcomes are preserved; later findings are routed, not re-reviewed.

## Implementation Context Record

| Item | Artifact |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-29/map-navigation-disposal-532-research.md |
| Plan | .copilot-tracking/plans/2026-10-29/map-navigation-disposal-532-plan.md |
| Details | .copilot-tracking/details/2026-10-29/map-navigation-disposal-532-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-29/map-navigation-disposal-532-plan-critique.md |
| Changes record, created by Implement | .copilot-tracking/changes/2026-10-29/map-navigation-disposal-532-changes.md |
| Readiness | Research Ready; critique Complete / Pass; implementation-ready |
| Continuation | Bounded explicit four-phase request; local-only stop after Review/commits |

## Sources

Research C1-C7/W1 establish lifecycle ordering, runner reuse, reset semantics,
strict check commands and unchanged manifest pin scope.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct disposal and browser isolation

* Intent: eliminate both named defects without broad route changes.
* Dependencies: completed Research and disposed critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Harden obsolete map cleanup

Make slot inert and toggle disabled before collapse, retain collapse then seq++
ordering, remove slot, and guard expand using the inert state. Extend the
existing source cleanup contract and API documentation.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Cover pending facets and reset session iterations

Add one browser helper holding facets and probing pointer/stale controls.
Reload at the start of each expiry iteration before hash navigation, so filters,
me and wrappers reset. Preserve existing coverage and error collection.

<!-- rpi:phase id=P02 -->
### [x] P02: Verify the correction

* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute local validation with lock discipline

Run API/core strict tools and admitted full units/browser; if busy, targeted
map/design/accessibility/Coordinator units only and disclose the blocker.
Use /tmp/mv; its editable namespace paths already resolve to this worktree.
Capture external logs and browser assets in a new task-owned directory.

## Test Ownership and Change Budget

* Canonical targets: src/api/src/zava_forward/api/web/app.js,
  src/api/checks/map_fullscreen_browser_check.py,
  src/api/tests/test_map_fullscreen.py, src/api/README.md.
* Generated targets: none. Exact removals: none. Maximum additions: one
  browser helper and at most two source-contract test methods; extend existing
  source contract where possible. No new dependencies or tooling.
* Semantic evidence: real-server browser pending state, pointer and retained
  control interaction, destination/modal/body checks, both expiry modes and
  real browser default font. Regression evidence: old-JS negative control.
  Source-string assertions alone are supporting evidence, not acceptance.
* Owner: implementation parent; independent reviewer assesses the final diff
  and evidence once. No test deletion, skipped check or swallowed error.
* Manifest's four pinned inputs are unchanged; verify their hashes read-only.

## Dependencies

* Existing /tmp/mv Python 3.12 tooling, installed editable packages, Chromium,
  pinned axe and uncontended shared lock. Missing tools must be reported or
  restored only after an actual missing-dependency failure.

## Critique Disposition

Single fresh critique executed: Complete / Pass, zero PC findings. No residual
critique risk or user decision. Original artifact retained at the metadata path.

## Follow-Up Items

* None.

## Handoff

All P01/P02 markers have completion evidence in the changes record and matching
details. Single independent Review completed Complete / Conformant, zero
findings or routed follow-ups. Parent performs local-only commit and stops.
Publication/full local receipt and human/hosted approval are
not implied by targeted local evidence; no push is authorized.
