<!-- markdownlint-disable-file -->
---
title: Lazy map sensors implementation review
ms.date: 2026-11-23
---

# Review: Lazy map sensors

## Executive Summary

Review execution: Complete for full plan P01. Final outcome: Conformant within
the local implementation boundary. One Medium issue was found and corrected
with a regression before closeout; no unresolved finding remains. Evidence
includes the completed plan, critique, changes, 90 focused tests and API static
checks. Independent exact-head assessment and hosted CI remain publication
gates. Live latency and live deployment are not established.

## What You May Not Know

The owner retained the stale/offline checkbox as an explicit bulk-read
exception. Ordinary map reads must remain lightweight.

## Findings and Proposed Routes

### RV-001 [Medium]: Opt-in refresh can leave the selected card out of date

* Related scope: P01-T02, FR-002/003.
* Expected: opted-in map summaries and the selected card show the same reading.
* Observed: `showHome(current, false)` skips updating a retained selection, even
  when the new map response contains an explicitly requested sensor summary.
  An earlier single-home request can also remain pending after that refresh.
* Evidence: src/api/src/zava_forward/api/web/app.js, `showHome`, `renderView`.
* Impact: a stale/offline marker can disagree with its open card.
* Resolution condition: an opted-in refresh updates the card and cancels older
  selected-home reads; a delayed earlier response cannot overwrite it.
* Proposed destination: rpi-implement, bounded correction with a regression
  extending the existing filter test.
* Resolution evidence: the opted-in redraw now enters the sensor-render branch
  for retained selections and cancels older reads. The extended filter test
  holds a previous request across the bulk response and verifies the late
  response cannot overwrite it. Final 90-test suite passed in Node/Chromium
  and HTTP fixtures. Original finding and route remain recorded above.

## Parent Decision Record

### Current Disposition

Based on RD-001 through RD-006: agent-owned, walkthrough skipped-auto,
Review execution Complete, final outcome Conformant within the local scope.
RV-001 resolved against correction/test evidence; no implementation route
remains. Continue to independent exact-head assessment and approved PR
publication. Hosted/human approval and live acceptance are not implied.

### Decision History

| Event | Subject | Decision source | Status or value | Rationale |
| --- | --- | --- | --- | --- |
| RD-001 | Participation | User mode selection | agent-owned | End-to-end automatic work |
| RD-002 | RV-001 route | Agent | accepted, rpi-implement | Correct the retained-selection bulk refresh; no scope expansion |
| RD-003 | RV-001 resolution | Agent | resolved | Condition updated; delayed-request filter regression passes in Node/Chromium |
| RD-004 | Walkthrough | Automatic mode | skipped-auto | No user-owned review decision remains |
| RD-005 | Execution and outcome | Agent | Complete / Conformant | All local requirements covered; external publication gates remain distinct |
| RD-006 | Continuation | Owner publication consent | independent exact-head assessment then PR | Publish only after independent verdict; no merge or deployment |

## Validation Evidence

| Check | Status | Result |
| --- | --- | --- |
| Focused suite including `ZF_BROWSER_TESTS=1` | Passed | 90 tests; six interaction cases in both Node and Chromium with a Leaflet double |
| Existing role/sensor regressions | Passed with skips | 280 tests, 94 existing opt-in skips, 186 successful cases |
| API mypy | Passed | 373 source files |
| Changed Python ruff check and test format | Passed | All changed files clean; server uses existing format exclusion |
| Stabilized API-only regression rerun | Passed | 21 tests |
| Whitespace | Passed | `git diff --check` |
| Hosted CI | Not run yet | Not yet pushed at review closeout |
| Full local gate | Not run | Bounded focused-tier read scheduling change |
| Live performance/deployment and human accessibility | Not run | Outside local scope |
| Prose detector | Unavailable | Not installed in searched plugin locations |

Initial failed fixture runs and their corrections remain recorded in the
changes artifact. They are not represented as initially passing.

## Risks, Blockers, and Residual Work

No implementation blocker or unresolved active-plan work. Independent
exact-head assessment, approved publication and exact-head hosted results are
the next gates; owner retains merge. Browser tests use a Leaflet double, not
the deployed app or real datasets. No live performance magnitude is claimed.

## Review Record

### Scope and Evidence

* Task ID: lazy-map-sensors.
* Scope: P01, P01-T01 through P01-T03; FR-001 through FR-003 and NFR-001/002.
* Depth: standard, default.
* Review execution: Complete.
* Plan: .copilot-tracking/plans/2026-11-23/lazy-map-sensors-plan.md.
* Critique: .copilot-tracking/reviews/plans/2026-11-23/lazy-map-sensors-plan-critique.md.
* Changes: .copilot-tracking/changes/2026-11-23/lazy-map-sensors-changes.md.
* Research: .copilot-tracking/research/2026-11-23/lazy-map-sensors-research.md.

### Opening Review State

Completed markers and check results support a bounded source/test review.
Compare request boundaries, selected-card lifecycle and owner-selected filter
behavior. Read-only except this review record. No private data, live acceptance,
SQL or deployment assessment. Review parent owns findings and final decisions.

### Acceptance and Change Coverage

| Requirement or scope | Implementation and validation evidence | Assessment |
| --- | --- | --- |
| FR-001, P01-T01 | server.py default provider attaches fixed unloaded states; API tests raise on any eager provider call | Met |
| FR-002 | Explicit `sensors=1`, checkbox-triggered draw, bounded existing provider; API compatibility and UI filter tests | Met |
| FR-003, P01-T02 | `loadSensor`, existing badge/gauge helpers, polite status and retry guidance; delayed selection/error cases | Met |
| NFR-001 | Existing `map_sensors` reused unchanged; restricted role and consent regressions retained, no history returned | Met |
| NFR-002 | AbortController plus generation/selected-ID guards; close/reopen, route disposal and cross-home tests | Met |
| P01-T03 | Existing tests retained, six executed JS cases added, README request contract, static and web baselines | Met |
| RV-001 correction | Explicit bulk redraw updates retained card and cancels earlier read; extended test passes | Met |
| Scope and plan updates | No business-authority change, no unrelated PDF edit, standard critique Complete / Pass | Met |

### Web Interface Guidelines

Source refreshed 2026-11-23. Scoped changed map code checked against applicable
rules: live async feedback, native controls and links, keyboard selection,
unchanged focus handling, safe text insertion, explicit errors and no new
layout reads or animation. Changed behavior passes. Existing unrelated app-wide
issues and whole-app conformance were not assessed.

### Critique and Follow-Up Assessment

Standard critique Complete / Pass, no findings. The implementation correction
clarifies the same filter behavior and adds no scope or authority. No optional
follow-up was promoted into active work. No BRD/PRD/ADR authority was changed.

### Reviewer Self-Check

All task markers, local requirements, material plan updates, finding routes,
validation results and limits have evidence or an explicit not-run status.
No human or hosted approval is inferred. This parent comparison is not the
independent exact-head assessment required before publication.
