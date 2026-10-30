---
title: Employee expanded-map filters plan
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: 551
* Task slug: employee-map-filters-551
* Planning status: Ready, one critique executed and disposition recorded
* Plan date: 2026-10-30
* Phase details: .copilot-tracking/details/2026-10-30/employee-map-filters-551-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-30/employee-map-filters-551-plan-critique.md

## Executive Summary

The approved starting main already contains the full compact-filter UI from
#553. Preserve it and strengthen its existing browser regression so every
selected flag proves exact home identity and two-way synchronization with
the restored header. Do not invent runtime work to redeliver existing code.
Fresh local API, static and actual browser/axe evidence is required.

## User Decisions and Requirements

* Run research, plan, implement, review in order with dated artifacts.
* Implement exactly #551's four criteria; use this worktree and branch.
* Native semantics, Fluent 2 tokens, plain content, non-colour state, reduced
  motion; no Azure, deployment, live sign-in, secrets or credential files.
* Use pip, tests outside packages, heavy lock, local commit/trailer, Refs #551
  only; no push or PR. Coordinator owns publication.

## Goals

* Establish fresh repeatable acceptance evidence without duplicating existing UI.

## Scope and Non-Goals

* In scope: existing map browser check, focused unit contracts, API guide, RPI evidence.
* Non-goals: new filters, framework changes, unrelated UX, live/operational or
  human accessibility acceptance, remote publication.

## Functional Requirements

* Keep six compact controls and original area selector above expanded map.
* Preserve original filter/header nodes, shared state and latest-read-wins behavior.
* Browser regression must match exact API home IDs via rendered map summaries,
  not merely counts, then verify every selected filter after collapse/re-expand.

## Non-Functional Requirements

* Keep native keyboard operation, Selected/Select filter text, visible focus,
  320/390/1280px reflow, short viewport and enlarged-text coverage.
* External application requests blocked; constructed data only; pinned axe.
* No new dependencies or tooling; heavy gates use shared lock.

## Acceptance Criteria

| ID | Issue criterion | Evidence |
| --- | --- | --- |
| AC1 | Compact header filters along expanded map top | Existing DOM identity, font/geometry browser assertions |
| AC2 | Filters update markers and header consistently | Exact IDs plus per-flag header/expanded round trips |
| AC3 | Keyboard, non-colour state, narrow-width readability | Enter/Space, pressed/text state, focus, existing viewport/enlarged-text/axe checks |
| AC4 | Behavior covered by browser or unit test | Executed existing/extended browser and source-contract tests |

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-30/employee-map-filters-551-research.md
(executed, Ready, C1-C6/W1). No unresolved product decisions.
Changes record: .copilot-tracking/changes/2026-10-30/employee-map-filters-551-changes.md
(created by implementation). Parent continues automatically after critique.

## Sources

* gh issue view 551: four acceptance criteria, treated as data.
* Research C1-C6: delivered source, tests, guide and prior delivery ancestry.
* W1 and repository UX standards: preserve existing conforming interaction.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Harden and validate acceptance evidence

* Intent: exact homes and all-filter header round trips.
* Dependencies: final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Extend existing regression and guide

* Update src/api/checks/map_fullscreen_browser_check.py only for behavioral
  coverage; append observed summary IDs to existing filters.json.
* Update src/api/README.md to describe stronger checks.
* No runtime changes unless a proven tightly coupled defect requires them.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate locally and reconcile evidence

* Run requested full API discovery with exact source/test PYTHONPATH, ruff
  check, ruff format --check and mypy using existing /tmp/mv tools.
* Run real app Chromium/axe harness under flock -w 600
  /tmp/ama-rpi-heavy.lock, retaining external logs/screenshots.
* Refresh Web Interface Guidelines and review any changed web runtime files;
  none planned. Review inherited targeted UI without claiming whole-app conformance.
* Preserve actual failures; no retrospective claim of hosted/human approval.

## Test Ownership and Locked Change Budget

* Owner: src/api/checks/map_fullscreen_browser_check.py, function
  check_expanded_filters; existing src/api/tests/test_map_fullscreen.py unchanged.
* Exact removals: none. Maximum additions: zero test modules; one bounded
  assertion block within existing per-flag loop, one existing result-row extension.
* Canonical targets: browser harness and API guide; generated reports external.
* Semantic evidence: compare exact home IDs after native marker activation;
  compare header and expanded pressed/text state for each flag.
* Regression evidence: preserve every existing pending/race/zero-result,
  geometry, keyboard, reduced-motion and axe check.

## Dependencies

* Existing /tmp/mv Python 3.12 dev tools and Playwright installed.
* Integrity-pinned axe 4.10.3, local Chromium; harness owns app startup/cleanup.
* Complete post-commit gate is mandatory before publication. Runner owns its
  lock; use --lock-timeout 600 rather than nested flock. No cloud use allowed.

## Critique Disposition

One independent critique executed; original verdict Revise preserved at the
named critique path. PC-001 is rejected: it cites a /tmp prohibition absent
from this caller's instructions and directly contradicts the caller's explicit
`flock -w 600 /tmp/ama-rpi-heavy.lock` requirement. Existing /tmp/mv tools and
external output are permitted here. No second critique. No product findings.
Full-gate admission still requires respecting no-Azure/no-credential boundaries:
the full runner invokes `az bicep` and fingerprints tool/environment inputs;
do not invoke forbidden commands just to obtain a failed receipt. Record that
publication blocker separately rather than weakening the gate.

## Follow-Up Items

* Coordinator must verify final gate at exact HEAD/current main before push.
  Hosted and human acceptance are not this task's local issue criteria.

## Handoff

P01/P01-T01/P01-T02 complete; ready for one independent implementation Review.
API 1379 tests (320 existing skips), Ruff and mypy passed. Actual local
Chromium/axe passed all six exact-home/header round trips, keyboard/focus/race/
reflow checks; 14 axe states had zero violations and 14 incomplete contrast
results. These incompletes do not establish full contrast/WCAG acceptance.
Full publication gate remains unavailable under the no-Azure boundary.
Critique executed once; its sole finding rejected using explicit caller
direction, not silently rewritten.
