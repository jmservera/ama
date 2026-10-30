---
title: Employee expanded-map filters changes
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Metadata

* Task ID: 551; task slug: employee-map-filters-551
* Plan: .copilot-tracking/plans/2026-10-30/employee-map-filters-551-plan.md
* Details: .copilot-tracking/details/2026-10-30/employee-map-filters-551-phase-details.md
* Implementation date: 2026-10-30

## Execution Status

Complete; full plan P01/P01-T01/P01-T02. Approved writes: existing browser
check, API guide, dated artifacts. No runtime duplication. Existing delivered
UI remains canonical.

## Execution Summary

Strengthen exact-home and per-flag header round-trip checks, then run requested
API/static and actual loopback browser/axe validation with shared heavy lock.

## Implementation-Time Plan and Detail Updates

No product changes. Original critique Revise retained; sole PC-001 rejected
because it incorrectly asserts a /tmp prohibition contradicting caller's
explicit /tmp shared-lock instruction. Plan Ready without second critique.
Mandatory az invocations in full runner conflict with conservative no-Azure
execution boundary; publication gate remains unavailable, never substituted.

## Completed Work

### Exact-home and header round-trip regression

P01-T01 complete: existing check_expanded_filters loop now opens each marker
with Enter, reads case ID and Open home link, closes with Space and confirms
marker focus. Exact IDs must match the actual API response, including empty
sets. Every flag round-trips through original header controls; a header-side
alternate updates markers/state before the original flag is restored in the
expanded map. Existing filters.json retains IDs and alternate selections.
API guide describes this stronger coverage. No runtime source edits.
Validation passed under P01-T02; see below.

## Validation Record

External evidence root:
/home/azureuser/.copilot/session-state/59a1feef-9efd-445e-ac90-6fffba7ac869/files/issue-551/

| Check | Result | Evidence |
| --- | --- | --- |
| Requested full API unittest discovery | Passed; 1379 tests, 320 existing skips, 485.737s; skips are not execution | api-unit.log |
| ruff check . | Passed | static.log |
| ruff format --check . | Passed; 61 files formatted | static.log |
| mypy | Passed; 117 source files | static.log |
| Actual loopback Chromium and pinned axe | Passed; Chromium 156.0.8078.4, no uncaught JS errors | browser.log, browser/browser.json |
| Exact homes/header round trips | Passed all six flags including zero-result funding/support | browser/filters.json |
| Reflow and minimum map space | Passed 320x900, 390x900, 1280x900, 390x568 and 640px with 32px default font | browser/filters.json, browser/enlarged-font.json |
| axe 4.10.3 | 14 states, zero violations; 14 incomplete color-contrast results | browser/axe-results.json |
| git diff --check | Passed | Local command |

Commands ran from src/api with PATH=/tmp/mv/bin:$PATH and the exact caller
PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests.
Full discovery ran under flock -w 600 /tmp/ama-rpi-heavy.lock. No missing
dependencies, installs or manifest changes. Browser command uses the same
lock and check-owned constructed-data application lifecycle.

Fresh full Web Interface Guidelines source retrieved again before review.
No changed runtime web files; scoped web-file diff review is not applicable.
No claim of a whole-app audit or WCAG conformance.

Screenshots visually inspected: browser/expanded-filters-320x900.png,
browser/expanded-filters-390x568.png, browser/expanded-filters-1280x900.png.
Labels wrap; the bounded filter region scrolls at small sizes, separate from
the map/list. Existing focus tests scroll every filter into view. Third-party
tiles are intentionally blocked; symbols and application behavior are local.
Harness starts a responsive constructed-data loopback server and stops its
owned server/browser on completion. No persistent app process was launched.

## Acceptance Evidence

| Criterion | Local result | Evidence |
| --- | --- | --- |
| Compact header filters at map top | Proven | Original nodes, smaller count text, top-edge geometry and inspected screenshots |
| Consistent markers/header state | Proven | All six exact API/rendered summary ID sets; header alternate and expanded restore; original nodes and area retained |
| Keyboard, non-colour, narrow readability | Proven for focused local Chromium checks | Enter/Space, pressed/text Selected state, focus, wrapping/scroll, measured viewports/enlarged text; existing reduced-motion/race/error checks |
| Browser or unit coverage | Proven | Extended actual browser harness plus full API tests |

No issue criterion remains unproven within this bounded local engineering
scope. Human screen-reader, voice-control, live employee site, cross-browser,
full contrast/WCAG and operational acceptance are not established.

## Pre-Review Reconciliation

All P01 markers complete; details, evidence, remaining work and handoff aligned.
Ready for one independent implementation Review with full-gate publication
blocker explicit; no hosted/human approval inferred.

## Blockers

Full publication gate cannot be admitted under no-Azure boundary; no push is
authorized. Targeted local acceptance checks remain admissible.

## Remaining Work

None in implementation scope. Original implementation Review and local commit
remain parent lifecycle actions.

## Follow-Up Items

Coordinator owns full exact-head publication gate and hosted/human approval.
