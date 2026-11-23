---
title: Issue 2253 live r6 plan
ms.date: 2026-11-23
---

Refs #2253. Single phase: add the node-executed geometry test to `src/api/tests/test_epic149_child_ux_contracts.py`; no `src` change; focused tier.

Critique (executed once, verdict proceed): the test slices `el` and the sensor helpers out of the demo.js IIFE with a regex, which couples to function order; accepted because the existing tests already read the file by pattern and `shutil.which("node")` skip guards missing node. A mutation (`markerGap = 1`) must fail the test. Compatible findings applied; none conflict with owner decisions.
Refs #2253. Tier: focused (test file only; no `src` change).

## Plan

* Phase 1: add a unittest in `src/api/tests/test_epic149_child_ux_contracts.py` that slices the real `sensorChart` and helpers out of `demo.js`, runs them under node with a stub DOM, and asserts (a) dense 5-minute history yields no two circles closer than 9 user units and always keeps a circle at the latest reading, (b) with a forecast the "Latest stored" label is end-anchored left of the divider when room allows and start-anchored right of it when the latest reading is near the left edge, (c) forecast squares are drawn for every forecast point. Skip when node is absent.
* Phase 2: run the new test and the existing file; run ruff and mypy per the repo instructions.
* Phase 3: write the per-criterion table in the changes record; commit.

## Critique (executed once)

* Risk: slicing demo.js by function names is brittle. Mitigation: slice from `function svgEl` through the line before `function renderConsent`-equivalent boundary found by regex on `function sensorChart` and the next top-level `function`, and fail with a clear message if the markers are missing.
* Risk: false pass if the stub DOM drops nodes. Mitigation: assert circle count is greater than 0 and include a mutation check in validation (temporarily set `markerGap = 0`, expect failure).
* Verdict: proceed. No conflict with confirmed owner decisions.
