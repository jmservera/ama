---
title: Case journey unsaved-edit correction plan
description: Implementation-ready child loop for seven PR 529 review threads
ms.date: 2026-10-28
---

Task: 526-correction. Parent: 526 / case-journey-ux-526.

## Executive Summary

Repair draft ownership and immutable mutation boundaries without changing
journey behaviour or API authority. Extend the existing two browser checks;
then run API tests, static checks and admitted Chromium/axe. Preserve original
RPI evidence. Publish only supported outcomes; human/live acceptance remains
pending.

## User Decisions and Requirements

* Fix all seven unresolved threads on PR #529, Refs #526, in this worktree.
* Keep stepper behaviour, use no az/Azure, secrets or .env, no force push.
* Fast-forward bot commits before committing; Conventional Commit with required
  Copilot trailer and authenticated privacy-safe identity.
* Commit dated RPI evidence; normal push, reply to and resolve addressed threads.
* Heavy checks acquire `/tmp/ama-rpi-heavy.lock` with flock -n; short retries,
  at most 40 minutes. Ruff line limit 100.

## Sources

Research: `.copilot-tracking/research/2026-10-28/case-journey-ux-526-correction-research.md`,
C1-C6 and seven GraphQL thread IDs. Clean branch matches upstream d3fbba58.

## Goals

Preserve unsubmitted edits and ensure visible text matches reviewed evidence.

## Scope and Non-Goals

Scope: app.js, assistants.js, ops.js, panels.js; focused regressions in existing
journey/assistant browser checks; related API guide and dated artifacts.
No domain/API schema, CSS, journey algorithm, visual redesign or deployment.

## Functional Requirements

* Retain complete document-review output with handlers through same-case redraw.
* Display the exact replacement successfully submitted by document Edit.
* Keep pending proposal snapshots across overlapping loads until restored or
  deliberately discarded, keyed by proposal/revision.
* Snapshot upload/handoff/resident submissions before any async mutation/file
  read; clear only unchanged submitted controls.
* Restore checklist evidence after construction, keyed by measure/version/item;
  never transplant it onto another measure/version.
* Bind funding drafts to AI record identity; preserve older edits copyably.
* Source verification never clears unsent proposal JSON.

## Non-Functional Requirements

Preserve permissions, approval/consent boundaries, native labels, dirty warnings,
keyboard access and reduced motion. Surface errors. No blanket panel retention
with stale case mutation closures.

## Acceptance Criteria

Each named thread has a deterministic browser reproduction and passing
regression. Existing journey six-step/tab/keyboard/reflow/zoom and pinned axe
contracts still pass. Relevant API unit/static tests pass. No journey file diff.
Review is independent, executed once and records actual outcome separately.

## Phase Checklist

<!-- P01 -->
### P01: Preserve draft models and mutation boundaries

* [x] P01-T01: Document output retention and submitted replacement display.
* [x] P01-T02: Session-owned proposal snapshots and action-aware dirty cleanup.
* [x] P01-T03: Immutable upload, handoff and resident dispatch snapshots.
* [x] P01-T04: Versioned asynchronous checklist and funding recovery.

<!-- P02 -->
### P02: Validate and publish

* [x] P02-T01: Extend two existing browser checks and API guide; run static,
  unit and locked Chromium/axe checks.
* [ ] P02-T02: One independent Review; reconcile artifacts; safe commit.
* [ ] P02-T03: Required local publication gate where permitted, normal push;
  reply/resolve seven addressed threads, verify remote head and thread state.

P01 complete. P02-T02 ready for the single independent Review and commit.
P02-T03 blocked by PC-002: full gate requires prohibited az. No remote write or
thread resolution may be represented as completed.

## Test Ownership and Coverage Lock

Canonical targets: existing `case_journey_browser_check.py` and
`assistants_browser_check.py`. Removals: none. Maximum additions: two helper
functions per existing browser file plus in-place scenarios; no new runner or
framework. Semantic coverage: real synthetic API operations and displayed
replacement text. Regression coverage: deliberately held responses, revision
and AI identity isolation, edits after dispatch, same-measure checklist restore.
Generated browser logs/screenshots stay external; dated evidence summarizes
actual commands, exits, skips and identities.

## Critique Disposition

One critique executed, original verdict Revise preserved at
`.copilot-tracking/reviews/plans/2026-10-28/case-journey-ux-526-correction-plan-critique.md`.

* PC-001 rejected: its claimed prohibition on /tmp is not present in the parent
  execution rules and conflicts with the user's explicit shared-lock path.
  The existing lock is owned by this user; bounded flock -n admission remains.
* PC-002 accepted: complete gate preflight invokes `az bicep version`, and its
  infrastructure checks invoke `az bicep build/lint`. User prohibits az.
  Do not launch --all, fabricate receipt or silently downgrade required gate.
  Implementation, permitted checks, independent Review and commit can proceed;
  push and thread resolution are blocked until compliant full-gate evidence.
* PC-003 accepted: unresolved in-scope Review findings block publication.
  After candidate/evidence commit, required gate must bind clean HEAD/current
  origin/main; fetch main, verify external receipt with --verify-receipt against
  current base, and obtain independent exact-head assessment before normal push.
  Any commit/base/tool/image/input change invalidates that gate.

## Follow-Up Items

Original Review executed once: Complete / Not accepted, RV-001/RV-002 High
checklist defects. Later implementation/tests are recorded in
`.copilot-tracking/plans/2026-10-28/case-journey-ux-526-checklist-findings-plan.md`.
They do not change the original verdict or establish independent acceptance.

Owner screen-reader, staff usability and postdeployment acceptance remain
outside the correction and are not represented by automated checks.

## Handoff

Original independent Review complete, Not accepted. Later checklist implementation
is locally verified in its distinct artifact set; local commit remains next.
Publication remains blocked by PC-002 and independent acceptance, not by lock
admission. Details:
`.copilot-tracking/details/2026-10-28/case-journey-ux-526-correction-phase-details.md`.
Changes path:
`.copilot-tracking/changes/2026-10-28/case-journey-ux-526-correction-changes.md`.
