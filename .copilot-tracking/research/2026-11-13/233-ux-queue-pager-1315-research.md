# Research: programme queue row links (#233) and pager range-end disabled state (#230)

Planning Readiness: Ready. Disposition: executed.

* Base dafed6a270 lacks the connected-home row link: `screenTable(label, headings, rows, limit)` has no cell renderer and `programmeHeadings` has 7 columns.
* Prior candidate 837da4fde (chain aebd381d9 row link, 30f1da646 page context) adds a cell renderer, final "Connected view" column, `screenPageSize`, `programmeCell(scope, items, offset)` and a `start` offset for `programmeQueue`; plus tests, browser-check steps and atlas-screen-trace text. Port role-screens.js, test_programme_screen.py, browser check and atlas row; skip its docs/log.md edits (conflict avoidance).
* Pager: role-screens.js `#programme-prev` / `#programme-next` are always enabled; onclick guards only. Add `disabled` when offset<=0 and offset+items.length>=total, refreshed after each page load.
* mypy: src/api/pyproject strict, files = src, tests, checks. Typed test helpers must be annotated; check 15 errors in d790b6b45 by running mypy after port.
* Browser check edit requires scenario-manifest recipe SHA sync and Core test_scenario_manifest / test_needs_inventory.
* Plain-language rule: no banned jargon in UI strings.
