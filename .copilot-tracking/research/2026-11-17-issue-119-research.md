---
title: Issue 119 research - tile provider decision record and accessible map alternative
description: Measured baseline for the map tile provider decision and list alternative
ms.date: 2026-11-17
---

## Disposition

Research disposition: executed (repository evidence read; no live vendor re-read, no keys). Planning Readiness: Ready.

## Measured baseline (2026-11-17, base eb51af5c9)

* `docs/reference/research/ux/map-tile-provider-options.md` holds options A-E, all vendor rows "draft, unverified" except OSM policy and Azure Maps free allowance.
* No decision record exists: `docs/design/` is absent; selection status, demo-only OSM scope (issue comments 2026-10-25), production rule and the accessible-list requirement are spread across ADR 0002, options doc, issue comments, wcag baseline.
* The options doc is listed in `UNTRACED_GAPS` of `src/api/tests/test_epic149_ux_journey_requirement_traceability.py` (no requirement ID plus journey).
* Code facts (server.py `tile_config`, app.js maplist, tests in test_ui_support.py and test_wcag_workbench_baseline_151.py): production without `ZF_TILE_URL` loads no tiles; list alternative and tile-error note exist; automated only, no human screen-reader run.
* Issue criteria: C1 provider licence/cost/coverage/processor terms recorded - unmet (no binding terms, owner/DPO/legal approval); C2 screen-reader test - unmet (needs human run).

## Smallest fix

Add `docs/design/map-tile-provider-decision-record.md` (status Proposed, no provider selected, demo-only OSM, production gate, accessible list as a standing requirement with FR-020, AC-023, AC-067 and journey wording), link it from the options doc and index, and add a focused regression test. No keys, no spend, no UI change.

## Unmet after this task

Both criteria remain unmet; Refs #119.
