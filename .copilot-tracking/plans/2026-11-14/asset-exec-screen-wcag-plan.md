---
title: Asset executive and board view WCAG plan (#226)
ms.date: 2026-11-14
---

## Steps

* [x] Add a "Summary in words" panel with a three-column summary table (measure, state in words, meaning) covering KPIs, risk band, milestones, inputs and AI cohort.
* [x] Prefix investment-input and phase-check states with `State: Unknown.` and a reason.
* [x] Give each panel an id and a programmatically focusable heading, with a "Sections of this view" nav using `data-jump` links and one delegated click handler that focuses the heading instead of changing the hash.
* [x] Add `src/api/tests/test_asset_exec_screen_wcag.py` (unique name).
* [x] Run focused validation: targeted unittest, `test_accessibility_baseline`, mypy and ruff in `src/api` with /tmp caches.

## Critique

One pass: no new controls, no `aria-invalid`, no `role="status"`; existing assertions on section structure and read-only behaviour are kept.

## Cycle 1 correction

* [x] Remove `assetPanel`; `screenPanel` accepts an optional leading `{ anchor }` child so call sites keep the literal `screenPanel("Title"`.
* [x] Add "Summary in words" to `EXCLUDED["asset-board"]` (portfolio-level summary) and to `EXPECTED_REGIONS["asset-board"]`.
* [x] Critique: one pass, no new controls or ARIA; DOM output of the asset panels is unchanged.
