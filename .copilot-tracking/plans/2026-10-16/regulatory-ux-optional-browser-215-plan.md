---
title: Regulatory UX optional browser dependency plan
description: Bounded import-boundary repair and local validation
ms.date: 2026-10-16
---

Task ID: 215. Status: implementation-ready.

## Executive summary

Defer Playwright runtime imports until browser operations are invoked. Preserve
typed Page annotations and all pure tests, add one import-blocking regression,
and rerun the actual source CI browser command after the main merge.

## User Decisions and Requirements

* Reuse PR #354 and its existing branch; merge origin/main first, keeping both
  append-only log histories. Refs #215 only.
* Unit discovery and pure assertions must work with only runtime dependencies.
* Browser checks remain enabled in the existing Playwright-capable CI step.
* Validate full API suites without and with Playwright, Ruff, mypy and local app.
* Update READMEs, append the log, audit criteria without ticking issue boxes,
  record RPI evidence, commit with trailer and push without force.

## Goals

Restore runtime-only unit discovery without reducing browser regression coverage.

## Scope and Non-Goals

Touch the regulatory check, its tests, directly related docs and tracking only.
Resolve chat merge conflicts preserving privacy and accessibility features.
No legacy trees, actual data, Azure, legal rule changes or operational approval.

## Functional Requirements

All three existing pure checks remain runnable. Invoking actual browser
operations without Playwright raises an explicit missing dependency error.
CI continues calling the regulatory browser harness with real Chromium.

## Non-Functional Requirements

No runtime dependency addition, broad exception catch, missing-import suppression
or weakening of typing. Match existing Playwright types when dev tools exist.

## Acceptance Criteria

* Full API unittest discovery passes in `/tmp/v215c` before and after installing
  Playwright; explicitly verify module absence first.
* New subprocess regression rejects any import-time attempt to load Playwright.
* API Ruff/format and mypy pass, including strict isolated check lint.
* Actual loopback synthetic app/browser harness passes with pinned axe.
* Existing issue criteria remain honestly scoped; unmet human gates stay unmet.

## Phase Checklist

* [x] P01 / P01-T01: isolate browser imports and add import-blocking regression.
* [x] P02 / P02-T01: execute both unit environments, lint/type and browser checks.
* [ ] P03 / P03-T01: update documentation, review and publish existing PR branch.

## Test ownership and validation lock

Canonical code: `src/api/checks/regulatory_ux_check.py`.
Test owner: `src/api/tests/test_regulatory_ux_check.py`.
Exact removals: none. Maximum additions: one subprocess import-boundary test.
No generated code targets. Semantic coverage: pure size/hash assertions and
explicit import rejection. Regression coverage: full unit discovery, real
browser workflow, retained main privacy warning and branch live-log semantics.

## Critique Disposition

One final-candidate critique executed; verdict Revise with PC-001 (Medium).
Applied directly: explicitly import both expect and sync_playwright inside run,
as well as expect within each helper using it. No conflicting user decision,
remaining blocker or repeat critique.

## Follow-Up Items

Full WCAG/manual assistive-technology assessment, real staff comprehension,
paired chat-value measurement and real accountable owners/applicable sources
remain outside this repair, as already recorded on the PR.

## Handoff

Research: `.copilot-tracking/research/2026-10-16/regulatory-ux-optional-browser-215-research.md`.
Details: `.copilot-tracking/details/2026-10-16/regulatory-ux-optional-browser-215-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-16/regulatory-ux-optional-browser-215-changes.md`.
