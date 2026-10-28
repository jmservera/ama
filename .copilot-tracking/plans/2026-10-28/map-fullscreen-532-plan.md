---
title: Map fullscreen and home cards implementation plan
description: Issue 532 implementation-ready candidate
ms.date: 2026-10-28
---

Task ID: 532. Slug: map-fullscreen-532. Status: implemented and locally validated; Review pending.

## Executive Summary

Extend the existing native Leaflet map with a near-full-viewport native dialog.
A narrow left panel holds home summaries and map information. Embedded summaries
sit over the map with a named top-right close icon. Use only permitted map
payload fields, retain manual list links, and manage Escape/focus and route
cleanup explicitly. No framework swap, briefing edits or async-helper dependency.

## Sources

Research: `.copilot-tracking/research/2026-10-28/map-fullscreen-532-research.md`,
C1-C8 and W1-W4. Issue #532, parent PR #529, user instructions 2026-10-28.

## User Decisions and Requirements

* Full RPI loop with dated committed artifacts on `feat/map-fullscreen-532`.
* Stack on `feat/case-journey-ux-526`; PR base is that branch, dependency #529,
  and only `Refs #532`, not an issue-closing keyword.
* Expanded map has narrow left info panel; both modes have home summary and
  navigation. Embedded card has a top-right close icon and map-click dismissal.
* Keyboard operation, Escape, focus return, non-colour status, reduced motion,
  manual path, regression tests and browser axe checks are required.
* Pattern references only; no framework swap, briefing edits, Azure, secrets,
  `.env` or private datasets. Ruff maximum line length 100 for new Python.
* Heavy runs use nonblocking flock with retry bounded to 40 minutes. Commit
  locally if the full publication gate requires az; coordinator handles push.

## Goals

Expose useful home context before navigation while preserving existing filters,
cluster behavior, permissions, native styling and manual case navigation.

## Scope and Non-Goals

Canonical sources: `src/api/src/zava_forward/api/web/app.js`, `style.css`.
Tests: dedicated unit contract, dedicated browser check, existing marker browser
expectations. Documentation: API README. Generated browser evidence is external.
No backend/schema/payload changes, briefing work or generated runtime assets.

## Functional Requirements

FR1: Expand/exit toggle moves the same map into/out of a named native dialog.
FR2: Home pointer, Enter and Space activation open summary-first.
FR3: Summary includes case ID, available name/address, current stage, status
words and symbol, and native `Open home` link. Missing/withheld fields remain
explicitly unavailable; coordinator restrictions are preserved.
FR4: Embedded close icon, map background click and Escape dismiss the card.
Escape with no card exits expanded mode. Closing restores focus appropriately.
FR5: Preserve selection through mode changes and same-ID redraws; clear cards
excluded by filtering/viewport, close stale summaries on failure, dispose map
and dialog on route abort/session loss. Restore recreated-marker focus by ID.
FR6: Retain map area list and direct native case links. Expanded list shortcut
must close the modal before navigating/focusing an external record list.

## Non-Functional Requirements

Use Fluent tokens and native semantics. Native modal isolates the background;
background application controls cannot receive focus. Native browser-chrome
focus traversal remains available. No map animation (including pan/resize) so reduced
motion is safe. Constrain scrolling, overflow and safe-area insets. At 320/390px
retain a compact left panel and usable map without document horizontal overflow.
Text is escaped via the existing DOM helper; no HTML interpolation.

## Acceptance Criteria

AC1: Toggle gives near-full viewport map with left panel, correct size after exit.
AC2: Both modes show summary and native navigation link; marker activation does
not navigate immediately.
AC3: Card closes by icon, background click or Escape and focus returns to its
current marker; a second Escape exits dialog to toggle.
AC4: Keyboard/tab containment, manual links, status words/shapes, reduced motion,
mobile layouts and coordinator withheld fields have focused browser coverage.
AC5: Relevant API unit tests, new contracts, JS syntax, Ruff/mypy and pinned axe
run under the required lock; original failures and incompletes are retained.
AC6: Independent critique and one post-implementation Review are recorded.
Publication is separately blocked if required full gate cannot run without az.

## Test Ownership and Budget

Owning suite: `src/api`. Exact removals: none. Maximum additions: one unit test
module (up to six contracts) and one focused browser script. Update existing
`design_system_browser_check.py` marker assertions to summary-first navigation.
Semantic coverage: actual DOM keyboard, focus, geometry, modal cleanup, filtering,
error, coordinator, small viewport, navigation and axe. Static regression checks
guard lifecycle wiring, safe DOM construction and token/layout hooks; they do not
substitute for behavior. Canonical and generated targets are distinguished above.

## Phase Checklist

<!-- phase: P01 -->
### P01: Map interaction and lifecycle

* [x] P01-T01: Add native expanded surface, left panel and summary-first activation.
* [x] P01-T02: Wire dismissal, stable-ID focus, redraw/abort cleanup and motion.

<!-- phase: P02 -->
### P02: Regression coverage and documentation

* [x] P02-T01: Add focused contracts/browser check; update old marker expectations.
* [x] P02-T02: Document controls and honest evidence boundaries in API README.
* [x] P02-T03: Run locked targeted tests and browser/axe checks; correct defects.

<!-- phase: P03 -->
### P03: Review and local delivery

* [ ] P03-T01: Refresh web guidelines; execute one independent Review.
* [ ] P03-T02: Reconcile artifacts, privacy-safe identity and Conventional Commits.
* [x] P03-T03: Assess full-gate prerequisites without Azure; publish only if permitted.

## Critique Disposition

One independent critique executed, original verdict **Revise**, preserved in
`.copilot-tracking/plans/2026-10-28/map-fullscreen-532-critique.md`.

* PC-001 rejected: the worker asserted a `/tmp` prohibition that is not present
  in this caller's execution context. The user expressly requires the shared
  `/tmp/ama-rpi-heavy.lock`; keep that exact path and isolated external evidence.
  No alternate lock, unlocked execution or fabricated blocker is authorized.
* PC-002 applied: focus enters the summary heading on activation; expanded entry
  targets the exit toggle. If a marker disappears, use the named map region
  inside the active surface. Preserve focus during same-ID background redraws.
* PC-003 applied: derive commit email from the actual runtime `gh api user`
  response rather than hardcoding the observed identity.
* PC-004 applied: assign complete gate, fresh receipt/current-main verification
  and independent exact-head publication assessment to coordinator explicitly.

All findings have a disposition; no unresolved product choice or second critique.

## Follow-Up Items

Human assistive-technology and real-staff acceptance remain outside automated
coverage. Full exact-head publication gate and hosted checks remain mandatory;
no bypass, cloud fallback or protection change. The full runner invokes prohibited
az commands even though az is installed. No full receipt or PR publication exists.
The parent topic's remote ancestry diverged from the supplied local base during
execution; coordinator must reconcile the stack without unauthorized local
history rewriting, then rerun the gate at the actual publication candidate.

## Handoff

Phase details: `.copilot-tracking/details/2026-10-28/map-fullscreen-532-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-28/map-fullscreen-532-changes.md`.
Implementation and final validation complete after the tooltip ARIA correction.
Original one-time Review is next. P03-T01/T02 are remaining lifecycle work for
Review and local evidence commits, not unfinished source implementation.
Publication remains blocked independently.
