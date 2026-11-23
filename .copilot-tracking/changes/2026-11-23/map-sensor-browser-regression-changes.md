---
description: "RPI Changes: Map sensor browser regression"
ms.date: 2026-11-23
---

# RPI Changes: Map sensor browser regression

## Metadata

* Task ID: `map-sensor-browser-regression`.
* Related plan: [.copilot-tracking/plans/2026-11-23/map-sensor-browser-regression-plan.md](../../plans/2026-11-23/map-sensor-browser-regression-plan.md).
* Implementation date: 2026-11-23.

## Execution Status

Complete, full-plan scope. `P02`, `P02-T01` and `P02-T02` complete.
No remaining active-plan marker. Publication gates remain separate.

## Execution Summary

Local Chromium reproduced the hosted rosterless failure in 124.5 seconds.
The corrected observer reads the count rather than the hidden sensor status.
All planned local checks passed, including the exact failed entry point and
the later synthetic browser stages that the failed job never reached.
Application code, lazy loading, identity admission and acceptance semantics
are unchanged.

## Completed Work

### Count notice targeting

* Related task: `P02-T01`.
* [src/api/checks/employee_acceptance_check.py](../../../src/api/checks/employee_acceptance_check.py)
  now reads direct sidebar status children, excluding the nested home-card
  sensor status. Exact status/list/marker comparisons remain unchanged.
* [src/api/tests/test_employee_acceptance_check.py](../../../src/api/tests/test_employee_acceptance_check.py)
  adds one native DOM regression: nested sensor feedback cannot shadow a
  correct count or impersonate a mismatched count.
* Regression failed before correction in 0.461 seconds; corrected positive
  and negative controls pass. Application code and the hosted test entry
  point are unchanged.

### Employee browser acceptance restored

* Related task: `P02-T02`.
* Exact employee CLI passed all three real Chromium tests with zero skips.
  Correct and malformed points/clusters/empty maps, stale responses, HTTP
  failures, fit/viewport follow-ups and mismatched rendering remain covered.
* Combined focused suite passed 123 tests, zero skips, including the new
  nested-status controls, lazy-sensor Node/Chromium cases and both manifest/
  needs-inventory integrity modules.
* The manifest's workbench recipe is unchanged; its existing SHA-256 remains
  correct. No employee-observer hash entry exists to update.
* [src/api/README.md](../../../src/api/README.md) documents count targeting.
* API mypy passed all 373 source files; changed Python lint and format passed.

## Implementation-Time Plan Updates

* None.

## Business Alignment

* None.

## Validation Record

| Check | Scope | Status | Evidence or reason |
| --- | --- | --- | --- |
| Original rosterless Chromium | Pre-change | Failed | Same authenticated map-stage failure as hosted run, 124.5 seconds. |
| Positive/negative DOM controls | P02-T01 | Passed | Nested feedback cannot shadow the count or impersonate a mismatched count. |
| Focused suite | P02-T02 | Passed | 123 tests, zero skips, including employee, lazy map, accessibility/content guards and manifest/inventory tests. |
| `python3 -m checks.employee_acceptance_check` | P02-T02 | Passed | Three real Chromium tests, zero skips, 24.348 seconds. |
| `python3 -m checks.design_system_browser_check` | P02-T02 | Passed | Includes synthetic workbench and real >500-home map clustering. |
| `python3 -m checks.regulatory_ux_check` | P02-T02 | Passed | 21 browser states; axe 4.10.3 executed, pinned SHA-256 verified. |
| `python3 -m checks.case_journey_browser_check` | P02-T02 | Passed | Existing synthetic browser entry point exited zero with pinned axe. |
| Chat warning/failure/keyboard/refusal/live-log Chromium | P02-T02 | Passed | Exact later workflow test, one test, zero skips. |
| API bare mypy | P02-T02 | Passed | 373 source files. |
| Changed Python ruff check/format | P02-T02 | Passed | Both files pass. |
| Prose detector | Authored Markdown | Unavailable | Installed sloptrim detector not found; manual prose review used. |
| Independent exact-head assessment | Publication | Unavailable | Awaiting an independent reviewer; not claimed by implementation checks. |
| Hosted exact-head CI | Publication | Unavailable | Corrective PR 2328 published; new hosted results awaited. Original failed run is not passing evidence. |
| Complete local gate and image/security stages | Broader integration | Not run | Bounded focused-tier observer repair; no release/deploy or security/gate-criteria change. |

## Pre-Review Reconciliation

Plan markers, task context, completed-work entries and local validation are
current. Ready for independent exact-head assessment. Child RPI review
skipped by default, not reported as passed.

## Blockers

* Owner authorized committing, pushing the corrective branch and opening an
  origin PR. Independent assessment and hosted exact-head checks remain
  required; no merge or deployment authorized.

## Remaining Work

* No implementation marker remains. Publication and external review pending.

## Follow-Up Items

* None.

## Return-to-Caller State

Implementation complete, full-plan scope. No business-alignment change.
Focused validation tier: observer targeting changes, not acceptance semantics.
Child changes are validated but have not had an independent review.
Owner authorized publication. Independent exact-head review and hosted checks
remain; later status will be recorded on the PR without rewriting original
evidence or claiming pending checks passed.

## Publication

Corrective PR: https://github.com/jmservera/ama/pull/2328, targeting `main`.
The shared GraphQL quota prevented `gh pr create`; REST creation succeeded
after confirming no duplicate PR existed. Subsequent exact-head hosted status
and independent review belong on that PR. No merge or deployment performed.
