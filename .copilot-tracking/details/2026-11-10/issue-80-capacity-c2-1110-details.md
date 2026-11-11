---
title: Issue 80 capacity browser check aftercare route, details
description: Exact edit and validation steps for C2
ms.date: 2026-11-10
---

## Edit locations in `src/api/checks/capacity_browser_check.py`

* `MANAGER_ROUTES`: add `"#/aftercare": ("Aftercare concerns", ("/api/aftercare/concerns", "/api/aftercare/evaluator"), "#app section[aria-labelledby='ac-list-title']")` between `#/time` and `#/screens`.
* After `expected_failures` and `origins` are defined: `form_denials: list[Response]`, a `request` listener that registers the exact expected request, and a `response` listener that records responses for that exact URL.
* `verify_route` branch `elif href == "#/aftercare"`: assert one denial with status 403 and the exact error JSON; status line text; `#ac-form` count 0; `#app button[type=submit]` count 0.
* Route loop: for `#/aftercare` assert the POST count is unchanged across the route.

## Commands (from `src/api`, `PYTHONPATH` as in earlier loops)

`ruff check`, `ruff format --check`, `node --check ops.js`, `unittest tests.test_list_export_api`, the five related static modules (60 tests), then one `python -m checks.capacity_browser_check --axe /tmp/axepk/package/axe.min.js` (self-taken heavy lock, outputs to `ROOT/phase80-capacity-c2-evidence-1110/browser-run3.log` and `.exit`).

## Success criteria

Run exits 0 after reaching both downloads, corrected `#/time`, `#/aftercare`, `empty capacity` zero-anchor assertion and later scenarios. Otherwise report the exact failing stage.
