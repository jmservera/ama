---
title: Issue 1248 saved-call History readiness Review
description: Single post-implementation Review of the test-only readiness repair against every issue criterion
ms.date: 2026-11-07
ms.topic: reference
---

## Execution and Outcome

* Review executed once by the implementing agent, after implementation and before the final selected-tier checks. Independent exact-head assessment is separate and pending.
* Boundary: `src/api/checks/case_journey_browser_check.py` diff against base 0f420dc9 plus the `.copilot-tracking` records for #1248.
* Outcome: conformant for the test-only scope with the open items listed below. Final frozen-head check results are external and not asserted here.

## Criterion Disposition

| # | Criterion | Disposition |
| --- | --- | --- |
| 1 | Preserve R4 negative evidence; record correlated synthetic reproduction or bounded not-reproduced | Met locally. R4 log and receipt untouched. Unchanged base run passed (407 PASS), recorded as not reproduced. Held run recorded correlated POST then held case GET, cleared outcome, attached old workspace and stale History. |
| 2 | Prove cause and completion signal before fix; distinguish application from checker | Met for the controlled mechanism (phase 1 proof preceded the repair). Application renders the call once the read completes. R4 attribution and universal absence of an application defect are explicitly not claimed. |
| 3 | Focused regression with controlled delayed refresh fails under old condition, proves exact History under repair, without weakening other checks | Met by deterministic in-check scenario: the old one-shot read is asserted to lack the call while held; the repaired path waits for workspace replacement and expects the exact text. Evidence that the old condition fails is the held assertion plus phase 1 run, not a mutation run of the old check. Other draft, persistence, keyboard and axe checks unchanged. |
| 4 | Existing full case-journey browser check passes with strict checks retained; no retry, sleep or skip | Met at dev run (409 PASS); the frozen-head final run is reported externally. No retry, sleep, timeout or skip added. |
| 5 | Research, plan, details, critique, changes and Review committed with current focused evidence and independent exact-head assessment | Partly met. Records are committed. Independent exact-head assessment and hosted checks cannot be proven locally, so expect `Refs #1248`, not `Closes`. |

## Findings

* No open material defect in the repaired check.
* Low: the regression lives inside the monolithic journey check, so it runs only with the whole browser check. Accepted to reuse the established idiom and avoid a new abstraction; routed as an optional later follow-up.
* Low: the held read is released in-line, and a failure before release leaves the route removed by `finally` with the error surfacing unhidden.

## Routing

* Follow-up (optional): extract held-refresh helper if more checks need it.
* Issues #86 and #81 must cite the R4 failure and this outcome. Acceptance ticks await independent assessment.
