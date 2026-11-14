---
title: Issue 74 Criterion 2 research (building versus home separation)
ms.date: 2026-11-14
---

## Scope

Issue #74, sole unticked Criterion 2: building-level dependencies, holds, works and costs are shown apart from each home's evidence, decision, cost allocation and outcome. Base `origin/main` 61e1917dd075a8307f0fd436c42cc41f47906846. Research disposition: reused (prior investigation #1513) plus direct re-inspection. Planning Readiness: Ready.

## Evidence

* `src/api/src/zava_forward/api/web/app.js` `homeCaseView`: section `hc-home` ("This home only: ...") renders only `home.*` (documents, quality, decision, cost_allocation); section `hc-building` ("Shared at building level, ...") renders only `b.*` through `shared("dependencies"|"holds"|"works"|"systems")` and `b.costs`. No UI defect found.
* `src/api/checks/home_case_browser_check.py` already asserted building tokens absent from the home region, but not the reverse direction, sub-heading placement, or non-nesting of regions.
* `src/api/tests/test_home_case_api.py` asserted only that the two labels exist in `app.js`; it did not assert payload or render-source separation.
* Heavy-resource lock: `tools/rpi-checks.py` `HEAVY_LOCK_PATH = /tmp/ama-rpi-heavy.lock`, taken with `fcntl.flock(LOCK_EX | LOCK_NB)` (queued retry only inside the gate's own `--lock-timeout` loop).
* Scenario manifest: `scenario-manifest.json` and `scenario_manifest.py` track `workbench_browser_check.py` as the recipe and do not reference `home_case_browser_check.py` (0 matches in both), so no recipe SHA applies to this change.

## Gaps closing Criterion 2

* (a) Explicit two-way negative region-separation assertions in unit and browser checks.
* (b) A recorded execution of `home_case_browser_check.py` under the canonical lock.
