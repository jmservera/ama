<!-- markdownlint-disable-file -->
---
title: Lazy map sensors implementation
ms.date: 2026-11-23
---

# RPI Changes: Lazy map sensors

Task ID: `lazy-map-sensors`. Scope: full plan P01. Execution: Complete.
Plan and standard critique are ready; no material decision is pending.

## Execution Status

Full plan `P01`, `P01-T01`, `P01-T02` and `P01-T03` completed. No active-plan
marker remains. Implementation is ready for scoped Review. Independent
exact-head assessment, push authorization, hosted CI and owner merge remain
separate publication gates.

## Completed Work

### P01-T01: Lightweight map and selected summary

Default map requests now attach unloaded states without invoking the sensor
provider. Explicit `sensors=1` retains bulk projection. A bounded single-home
`sensor-summary` endpoint reuses `map_sensors`, including its permission,
consent and logged unavailable states. Tests pending in P01-T03. Source:
[src/api/src/zava_forward/api/server.py](../../../src/api/src/zava_forward/api/server.py).

### P01-T02: Selected-home loading and explicit bulk filtering

The existing map card now loads a single summary on selection, reports loading
and errors, and cancels/ignores superseded reads. Redraws retaining the same
selection do not re-fetch it. The checkbox opts into `sensors=1`; normal draws
remain lightweight. Existing marker keyboard handling and layout are unchanged.
Source: [src/api/src/zava_forward/api/web/app.js](../../../src/api/src/zava_forward/api/web/app.js).
Executed regression checks follow in P01-T03.

### P01-T03: Request-boundary regression coverage

Updated existing map API/fullscreen contracts and added
[src/api/tests/test_map_lazy_sensors.py](../../../src/api/tests/test_map_lazy_sensors.py).
The six UI cases execute shipped map code with delayed reads in Node and,
with `ZF_BROWSER_TESTS=1`, Chromium using a small Leaflet double. Coverage
includes zero eager reads, selected-home scope, redraws, keyboard activation,
cross-home races, close/reopen, route disposal, errors, malformed replies and
explicit bulk filtering. API cases prove zero provider calls by raising on any
eager call; the selected endpoint returns no history and preserves restrictions.
Updated [src/api/README.md](../../../src/api/README.md) with the request contract.

## Validation

Focused tier: bounded read scheduling, no SQL, deployment, dependency or
authorization-control changes. The unrelated pre-existing PDF is excluded.

* Passed: 90 focused tests, including all six Node/Chromium cases, map API,
  fullscreen, status-locator, viewport-premise, accessibility and content
  baselines. Command from the repository root:
  `PYTHONPATH=src/api:src/api/src:src/api/tests:src/core/src:src/core/tests:src/agents/src:src/agents/tests ZF_BROWSER_TESTS=1 python3 -m unittest -q test_map_lazy_sensors test_map_sensors test_map_fullscreen test_map_status_locators test_map_viewport_premise test_accessibility_baseline test_content_standard`.
* Passed with explicit skips: the additional role-matrix, sensor-consistency,
  quality-sensors and home-sensors modules ran 280 tests, 94 skipped (their
  existing opt-in coverage was not enabled), leaving 186 successful cases.
  Logs include expected refusal and unavailable-service fixtures.
* Passed: changed Python `ruff check`, `ruff format --check` on the three
  changed test files, and bare API `python3 -m mypy` with the documented
  core/agents import path, 373 source files.
* Passed: `git diff --check`.
* Initial failed runs: default-map test used a bbox excluding synthetic homes;
  broader map tests lacked `src/api` on the test import path; the reused
  Node mini DOM lacked native string-append and detached-remove semantics;
  the new Python test needed formatting. These fixture/check-command issues
  were corrected without a production fallback. Final 90-test run passed.
* Unavailable: installed prose detector was not found. Prose rules were
  applied manually; no scoring result is claimed.
* Not run: live deployment/timing, human or assistive-technology acceptance,
  complete local gate (not this tier), hosted CI (branch not yet published).
* Original sensor-history tests and permission projection were retained.
  No browser-check recipe changed, so no scenario-manifest update applies.

## Implementation-Time Plan Updates

Review finding `RV-001` identified a missed retained-card refresh when the
opted-in map response supplies newer sensor summaries. Reopened `P01-T02/03`
for a bounded correction and extension of the existing filter test. The update
clarifies the same owner-selected filter contract, not scope or authority.
The standard critique remains Complete / Pass; no new critique is requested.
The correction is complete: opted-in redraws render the supplied summary even
for an unchanged selection and cancel older single-home reads. The existing
filter regression now holds an earlier read across that refresh and verifies
it is cancelled and cannot replace the bulk result. The final 90-test
Node/Chromium/API suite, changed-file lint/format and API mypy all passed again.

## Business Alignment

None: no cited business requirement changes. Owner selected the opt-in filter
exception to click-only loading.

## Remaining Work

No implementation work remains. Review and publication gates follow.
