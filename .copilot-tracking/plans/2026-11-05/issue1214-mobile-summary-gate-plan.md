---
title: Issue 1214 320px case-summary gate recovery plan
description: Plan for the smallest CSS correction that restores the existing 320x800 browser contract
ms.date: 2026-11-05
ms.topic: reference
---

## Task Identity

* Task ID and slug: issue1214-mobile-summary-gate. Issue #1214. Branch fix/mobile-summary-gate-1214, base main c6d5a8f3c3a35892322300be27b9747f7b11362d, target main.
* Research: .copilot-tracking/research/2026-11-05/issue1214-mobile-summary-gate-research.md. Details: .copilot-tracking/details/2026-11-05/issue1214-mobile-summary-gate-phase-details.md.
* Changes record (created by Implement): .copilot-tracking/changes/2026-11-05/issue1214-mobile-summary-gate-changes.md.

## Executive Summary

The 320x800 summary bound fails because the shell header above the summary is 527px tall: nine 42px nav links wrap into seven rows separated by 16px row gaps (96px). Reducing only the nav row gap to 2px at the existing max-width 600px breakpoint removes 84px, bringing the bottom to about 1592px under the unchanged 1600 bound, with no content hidden, clipped, removed or reordered. The existing exact browser check is the regression coverage. Validation tier is FOCUSED. Status: ready; one critique applied (see Critique Disposition). Residual risk: 7.6px margin and a small tighter nav rhythm at 390px.

## User Decisions and Requirements

* Smallest Fluent 2-preserving compact fix at 320; do not relax the 1600 bound or change viewport thresholds (issue #1214, coordinator brief).
* No hiding, clipping, removing or reordering of safety, hazard, approval or resident content; keep semantics, keyboard paths, non-colour meaning, reduced motion.
* Existing exact failing browser check is the coverage; add a regression only if necessary, never a trivial CSS constant test.
* FOCUSED tier; stop and report if scope expands. Heavy lock held for all browser work; candidate source paths asserted; no installs, no cleanup, no push or PR.

## Goals

* Existing `checks.case_journey_browser_check` exits 0 with the bound unchanged.

## Scope and Non-Goals

* In scope: one CSS rule in `src/api/src/zava_forward/api/web/style.css`; asset-cache/version impact review; documentation of the finding.
* Non-goals: JS, check script, tools/rpi-checks.py, source-bytecode discovery, header redesign, summary content, full gate.

## Functional Requirements

* FR1 Nav links stay visible, same order, same 42px target height, same labels.
* FR2 At 390 and 1280 the existing reflow assertions pass; 1280 geometry unchanged.

## Non-Functional Requirements

* NFR1 No layout overflow at 320 (existing scrollWidth assertion). NFR2 axe, keyboard, forced-colour and reduced-motion checks in the existing browser check still pass.

## Acceptance Criteria

* AC1 Existing check process exit 0 with candidate module paths asserted, loaded from the candidate checkout.
* AC2 Recorded before and after geometry at 320, 390, 1280 (nav height, summary bottom).
* AC3 Relevant existing API tests (`test_design_system`, `test_static_assets`, `test_case_journey`, `test_accessibility_baseline`) pass with candidate paths; rpi-checks focused tier passes.
* AC5 A focused nav link ring is visible in 320 and 390 screenshots.
* AC4 Independent review and hosted checks are not claimed.

## Phase Checklist

### [x] P01 Apply nav row-gap correction

* [x] P01-T01 Add one rule inside the existing `@media(max-width:600px)` block (style.css:317) setting `.top nav` row-gap only.
* [ ] P01-T02 (completed in Review phase with refreshed guidelines) Review changed lines against fetched web-interface guidelines and the Fluent 2, WCAG and content standards.

### [ ] P02 (open: P02-T02 runner portion, P01-T02) Focused validation

* [x] P02-T01 Run the existing browser check under the heavy lock; record process exit and geometry at 320, 390, 1280.
* [ ] P02-T02 Run existing API static and layout tests (done, 72 tests OK) and `python3 tools/rpi-checks.py --changed` (NOT run: blocked by constraints, see changes record).
* [x] P02-T03 Record durable finding in the changes record and the KB log if a knowledge-base page is changed (decision in details).

## Critique Disposition

Critique executed once (fresh worker, read-only, verdict Revise, no user decision needed): .copilot-tracking/reviews/2026-11-05/issue1214-mobile-summary-gate-critique.md. No second critique runs.

| ID | Disposition |
|---|---|
| PC-001 | Applied: `row-gap` only, placed in the existing `@media(max-width:600px)` block (style.css:317), relying on `.top nav` specificity over `nav{gap}` (P01-T01). |
| PC-002 | Applied: P02-T01 captures 320 and 390 screenshots of a focused nav link, including the 24-by-24 target spacing note; a visible ring is an acceptance condition (AC5). |
| PC-003 | Applied: 390 and 1280 pass criteria are existing reflow assertions plus 1280 nav/summary geometry equal before and after (AC2). The dump hook stays external and uncommitted. |
| PC-004 | Applied: cache impact closed from source: `static_assets.py` hashes content and rewrites `?v=`; no manual bump. |
| PC-005 | Applied: stop rule added; if the measured bottom exceeds 1600 after the edit, record the adverse result, do not change the bound or hide content, and report. PR wording `Refs #1214` unless every criterion is proven. |

## Follow-Up Items

* Separate tooling investigation: source bytecode created during API discovery (issue-owned, out of scope).
* Header/account row packing at 320 (about 58px more headroom) if a later change needs it.
