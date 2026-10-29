---
title: Loading and HAX briefing implementation plan
description: Issue 531 final candidate plan and critique dispositions
ms.date: 2026-10-28
---

## Task Metadata

Task #531, slug `loading-briefing-hax-531`. Stacked on PR #529,
base `feat/case-journey-ux-526`. Research readiness: Ready.

## Executive Summary

Make startup and async actions visible without replacing the native UI.
Restructure briefing into labelled output, declared sources and explicit draft
review choices. Retain all authority and manual paths.

### What You May Not Know

A server that has not returned HTML cannot display that HTML. The static shell
covers delayed scripts/API once delivered, not a platform-level unavailable
document. Recorded reviews cannot safely be undone; local dismissal can.
Full publication gate may be blocked by the explicit no-Azure restriction.

## Sources

`.copilot-tracking/research/2026-10-28/loading-briefing-hax-531-research.md`,
C1-C4 and W1-W7; issue and latest comment.

## User Decisions and Requirements

* Full dated RPI loop with committed evidence, stacked parent dependency.
* Immediate shell/action feedback; spinner after 200ms; pending control disabled;
  polite status and surfaced errors; preserve script/Leaflet recovery.
* Label AI/rules, show actual statement references, refresh and rationale.
* Plain outcome-labelled draft reviews; large fields only when needed.
* Fluent patterns only, no framework swap, preserve human/manual safeguards.
* Unit/browser/axe regression checks; nonblocking heavy lock with <=40m retries.
* No az, Azure, secrets or .env. Local commit if full gate cannot run.

## Goals

Remove silent waits and ambiguous draft review without broad UI changes.

## Scope and Non-Goals

Employee assets and shared AI-task output metadata, relevant tests/checks and
API guide. No resident redesign, authentication/backend authority changes,
dependency upgrades, deployment or platform ingress customization.

## Functional Requirements

Static main fallback, early watchdog with 4s slow message/15s retry, explicit
startup failure. Shared async helper through native event factory plus direct
listeners; preserve callback errors and existing local statuses. Initial route
and independent panels expose pending state. No automatic mutation retries.
Briefing has explicit mode selection (applies to AI requests), source-labelled
statement list, case references, actual generated-at time, explain ranking,
hide/show, and conditional edit/reject fields. Accept reviews a draft only.

## Non-Functional Requirements

Use Fluent tokens, native semantics, scoped polite regions, text with spinner,
reduced motion, reflow at 320/390/1280, safe cancellation/stale routes and
draft retention. ASCII/sentence case override generic fetched style conflicts.
Helper must not restore a disabled state changed by existing action logic.
No inference of provenance or model confidence.

## Acceptance Criteria

* Delayed/missing scripts and slow API show immediate + slow + retry messages.
* Controlled delayed action verifies no spinner before 200ms, spinner after,
  disabled duplicates, polite messages and error/recovery.
* Actual server briefing labels AI/rules and retains declared statement sources,
  unresolved citations, generated timestamp and unchanged role scope.
* Edit/reject reveal only needed fields, validate reason, preserve audit semantics;
  dismiss/show is local only; unverified accept stays disabled.
* Relevant unit and browser/axe checks pass, with no conformance/live claim.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Loading and action feedback

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Static shell and shared async lifecycle

<!-- rpi:phase id=P02 -->
### [x] P02: Briefing and review interaction

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Statement metadata and HAX interface

<!-- rpi:phase id=P03 -->
### [x] P03: Validation and handoff

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Unit/browser/axe evidence and documentation

## Test Ownership and Change Budget

Existing API/core unittest owns server semantics; browser checks own rendered
interaction, timing, axe and reflow. Exact removals: none. Maximum additions:
one JS helper, one early shell script, one unit test module and one browser check.
Canonical targets are `src/`; generated reports/screenshots stay external.
Update existing briefing check labels rather than leave obsolete selectors.
Migrate workbench mode/retry assertions to the native select and polite status.
Behavioral tests execute actual helper/server; source-string assertions alone
are not semantic coverage. Existing script and journey checks remain required.

## Critique Disposition

Executed once, original verdict Revise. All three findings are compatible
direct corrections, accepted and incorporated before implementation:

* PC-001: inventory includes standalone law viewer, appointment mutation,
  direct listeners and library-driven map refresh; real delayed checks required.
* PC-002: statements describe final published output only; quarantine has no
  abandoned AI attribution; timezone-bearing generation timestamp stays cached.
* PC-003: migrate journey reveal/submit flow, retaining delayed/later-edit
  safeguards, cancel/reopen and external resident draft consistency.

Dispositioned before implementation. No repeated critique and no user decision required.

## Follow-Up Items

* Human screen-reader, voice-control, staff usability and deployed employee-site
  cold-start verification remain owner tasks, outside local synthetic acceptance.
* Original Review RV-001: freeze rules statement metadata with its published
  snapshot; later `rpi-implement`, outside this task's one-pass boundary.
* Original Review RV-002: separate action-specific live announcers from busy
  subtrees; later `rpi-implement`, no AT acceptance inferred.
* Original Review RV-003: protect unsaved briefing correction/reason values and
  pending reviews from refresh; later `rpi-implement`.
* RV-004 retains distinct SQL/data-store, accessibility, product and operations
  acceptance owners. None of these follow-ups is an active P01-P03 task.

## Handoff

Details: `.copilot-tracking/details/2026-10-28/loading-briefing-hax-531-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-28/loading-briefing-hax-531-changes.md`.
P01/P02 implemented and evidenced by focused units and actual browser checks.
P03 complete: full API discovery passed 1178 tests with 316 environment-dependent
skips, required browser checks and additional assistants/design checks passed.
Original independent Review completed once: execution Complete, outcome
Not accepted, at
`.copilot-tracking/reviews/logs/2026-10-29/loading-briefing-hax-531-review.md`.
Completed markers represent performed implementation, not defect closure or
acceptance. Complete publication gate remains blocked by no-az; remote
parent ancestry now differs from the original local anchor and needs
coordinator reconciliation before publication. No rebase/merge was performed.
