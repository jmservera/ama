---
title: Map browser shortcuts correction plan
description: Focused correction candidate for PR 539, Refs 532
ms.date: 2026-10-29
---

## Task Metadata

Task: 532-map-browser-shortcuts-2026-10-29. Slug: map-browser-shortcuts-532.
Branch: feat/map-fullscreen-532. Baseline: f4a6bed44ff5891c4edd0455dabcff3ea39492bf.
Status: implementation-ready; single critique Revise, PC-001 applied.

## Executive Summary

Leave browser Ctrl/Meta/Alt shortcuts uncancelled while preserving ordinary
map pan/zoom and Shift plus. Extend the existing real-app browser check rather
than introducing a test framework or changing unrelated map behavior.

### What You May Not Know

The requested issue-526-journey venv and parent directory are absent. The
existing /tmp/ama-532-venv is a disclosed validation substitute, with this
worktree's src packages first on PYTHONPATH. Nonblocking heavy-lock contention
means targeted-only checks, never an unlocked full suite. No publication or
human accessibility acceptance is claimed.

## Sources

* .copilot-tracking/research/2026-10-29/map-browser-shortcuts-532-research.md, C1-C7/W1.
* .copilot-tracking/reviews/logs/2026-10-28/map-fullscreen-532-review.md, RV-001.
* User correction request 2026-10-29.

## User Decisions and Requirements

* Complete Research, Plan, Implement and Review; date and commit original evidence.
* Ignore Ctrl/Meta/Alt map key events without preventing defaults; retain Shift plus.
* Add regression assertions to the existing map browser check.
* Run local API units, map check and axe; hold flock -n /tmp/ama-rpi-heavy.lock
  for full suites, use targeted checks only when busy.
* Work on this branch, source in src/, Refs #532 without closing keywords.
* No push, az, force-push or merge. Conventional commits with requested trailer.

## Goals

Restore native shortcut ownership and prevent map movement from browser commands.

## Scope and Non-Goals

Only app.js modifier guard, existing map browser check and directly related
src/api README. Evidence under dated .copilot-tracking paths. No redesign,
private datasets, new helpers/modules, source fixture changes or cloud calls.

## Functional Requirements

* FR1: return before map commands for ctrlKey, metaKey or altKey.
* FR2: continue honoring defaultPrevented and Leaflet-control exclusions.
* FR3: leave Shift-only "+" active and ordinary arrow/equals/minus controls intact.

## Non-Functional Requirements

* NF1: no dependency additions or remote writes; synthetic loopback fixtures only.
* NF2: explicitly distinguish automated engineering evidence from human acceptance.

## Acceptance Criteria

* AC1: focused map and home marker, embedded and expanded, leave Ctrl+=,
  Meta+-, Alt+ArrowLeft uncancelled and do not move or zoom the map.
* AC2: matrix also covers all recognized arrows and +/=/- with each protected
  modifier, including combined modifiers/Shift; page route/focus remain stable.
* AC3: trusted Shift-generated "+" and unmodified "=" / "-" produce exact
  +1/+1/-1 zoom deltas; existing trusted 80px pan check remains.
* AC4: required local tests pass, or exact blockers/lock contention are recorded.
* AC5: independent critique and one post-implementation Review are preserved;
  original adverse evidence remains unchanged; local commits only.

## Test Ownership and Change Budget

Owner: src/api/checks/map_fullscreen_browser_check.py. Removals: none.
Maximum additions: one local helper and two call sites plus one positive zoom
sequence in this existing check; no new test files or generated source targets.
Canonical production target: src/api/src/zava_forward/api/web/app.js.
Semantic coverage: uncancelled modifier events and unchanged map state/request
count. Regression coverage: exact reported shortcuts in both modes/focus
targets, trusted Shift plus and ordinary zoom/pan. Generated evidence: external
map output, screenshots and axe JSON. Manifest pins unaffected (research C6).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct handler and regression coverage

<!-- rpi:task id=P01-T01 -->
* [x] P01-T01: Extend assertions, prove pre-fix failure, then add early modifier guard.
<!-- rpi:task id=P01-T02 -->
* [x] P01-T02: Document browser/map key ownership in API README.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate and preserve local correction

<!-- rpi:task id=P02-T01 -->
* [x] P02-T01: Run requested post-fix local checks.
<!-- rpi:task id=P02-T02 -->
* [ ] P02-T02: Record one independent Review and create local commits.

## Critique Disposition

Single critique executed: Revise. PC-001 (planning parent, direct) applied:
P01-T01 now explicitly orders assertions, pre-fix failure, then source guard;
P02-T01 owns post-fix checks only. Resolving evidence: current phase checklist
and phase details. No user decision needed and no repeat critique.

## Follow-Up Items

* Human assistive-technology and staff acceptance remain with the owner.
* Publication requires a later authorized exact-head gate; prohibited here.

## Handoff

Phase details: .copilot-tracking/details/2026-10-29/map-browser-shortcuts-532-phase-details.md.
Critique: .copilot-tracking/reviews/plans/2026-10-29/map-browser-shortcuts-532-plan-critique.md.
Changes record (implementation-owned):
.copilot-tracking/changes/2026-10-29/map-browser-shortcuts-532-changes.md.

Source and requested local checks complete: API 1214 tests, 316 existing skips;
extended map check and nine axe states passed with contrast incompletes retained.
P02-T02 is explicitly Review/local-commit closeout, not remaining implementation.
