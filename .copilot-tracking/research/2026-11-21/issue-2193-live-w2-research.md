---
title: Issue 2193 research, wave 2
ms.date: 2026-11-21
---

## Scope

Issue #2193 (OPEN): dual-axis chart in the employee Home sensors tab, readings or gauges in the map card. The issue body has no checkboxes; criteria are read from its sentences. Owner decisions 2026-11-18: synthetic demo, desktop only, no person-run assistive-technology test, no production change.

## Findings so far

* Implementation is on main (#2196, af49ce81a6). A sibling local branch `test/code-live-20261121T215055Z` (43c03d6f0f, unmerged) holds a gauge reorder fix, its test and a live probe script. It is the baseline for this wave.
* Prior live proof covered chart, table, cues, reduced motion on `ca-cutover-test-demo-api`. Unproven earlier: offline and withheld states live, reorder live (needs deployment).
* Deployment is not authorised by this goal (no production change), so the reorder stays test-only.

Research disposition: executed. Planning Readiness: Ready.

## Plan inputs

1. Cherry-pick 43c03d6f0f.
2. Re-run the live probe; scan all homes for stale, offline and withheld sensor states.
3. Run web tests, mypy, ruff.
