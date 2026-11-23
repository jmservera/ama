<!-- markdownlint-disable-file -->
---
description: Map sensor browser regression research
ms.date: 2026-11-23
---

# Task Research: Map sensor browser regression

## Executive Summary

The merged lazy-loading change added a nested sensor status inside the home
card. The employee acceptance observer selects the first descendant status,
which is now that hidden card's status after expanding the map, not the count.
The failed check does not demonstrate eager sensor reads or an application
failure. Correct the observer's target without changing its acceptance criteria.

## What You May Not Know

The hosted unit, lint and type steps passed; the later real-app Chromium
employee acceptance stage failed before the remaining browser/image checks.
Earlier small Leaflet-double tests did not exercise this observer.

## Findings

### C5: Hosted employee map acceptance failed

Evidence-backed: run 45216338816 job 137838807298 failed
`test_chromium_rosterless` and `test_chromium_map_contract` with map stage
failed and later stages blocked. Source: official job log, 2026-11-23.

### C6: The observer selects the wrong status

Evidence-backed, high source confidence: `MAP_RENDERED` queries
`.map-info [role=status]`, while `mapPanel.expand` prepends the home card,
whose nested `sensorFeedback` now has `role=status`. DOM selectors include
hidden descendants. The count notice remains a direct child of the sidebar.

## Recommendation and Alternatives

Use the direct-child map status selector and retain exact expected-count,
list, marker, alert and busy checks. Add positive/negative DOM regression
coverage. Do not remove the sensor live region or relax count equality.

## Scope and Questions

Q4: Which hosted step failed? Answered by C5.
Q5: Can the selector be corrected without weakening acceptance? C6 supports
the direct-child target; negative-control tests must prove wrong counts fail.
Scope: employee observer and directly related tests/documentation. No app,
workflow, identity, authorization, SQL, deployment or gate-criteria change.

## Decisions and Feedback

Owner requested correction after merging failed PR 2327. Automatic
agent-owned decisions inherited. Clean main checkout permits a new
main-based topic branch; merged branch must not be reused.

## Risks and Open Questions

The full hosted browser sequence must run, not only the previous lazy-loading
unit tests. Browser-check edits require scenario-manifest/needs-inventory
integrity tests; the hashed workbench recipe itself will remain unchanged.

## Planning Readiness and Next Step

Research disposition executed; Planning Readiness Ready. Reproduce the exact
employee-browser failure and prove the corrected selector. No material user
decision is needed. Publication remains separately authorized.

## Research Record

Focused posture for a bounded CI regression. Default research root and date
2026-11-23 from the current user timestamp. Continues C1-C4/Q1-Q3 from the
parent research. No helpers. Relevant skills: existing RPI research/plan/
implementation contracts; frontend aesthetic skills skipped, no app UI edit.

Cycle 2:
* Wider: read hosted job steps and exact failures; reflection: later browser
  observer failed, not unit/lint/type checks.
* Deeper: traced `MAP_RENDERED`, expanded home-card reparenting and nested
  sensor live status; reflection: direct count target is unchanged.
* Contrarian: inspected existing count-locator helper and negative map
  contracts; reflection: preserve exact status matching, malformed-response
  rejection and identity admission. Removing live feedback is unnecessary.
* Synthesis: select direct-child targeting. No broader investigation required.

Evidence: C5, official log at
https://github.com/jmservera/ama/actions/runs/45216338816/job/137838807298;
C6, src/api/checks/employee_acceptance_check.py `MAP_RENDERED` and
src/api/src/zava_forward/api/web/app.js `mapPanel`/`expand`.

Self-check: bounded scope, failure evidence, counter-checks, alternatives,
source locations and readiness recorded. Local rosterless Chromium reproduced
the hosted failure in 124.5 seconds before correction. A focused DOM regression
also failed before correction in 0.461 seconds.
