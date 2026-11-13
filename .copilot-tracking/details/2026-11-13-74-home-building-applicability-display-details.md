---
title: Details for #74 home view building applicability display
ms.date: 2026-11-13
---

## Phase 1

In `app.js` home-case `shared()` row, after the status text, append when `x.case_ids !== undefined`:
`Affected homes: <Unknown | ids | None>. Packages: <Unknown | ids | None>.` Same wording and null/empty semantics as `buildingView`. Plain text, so the signal is not colour-based. Rows without scope fields (systems) render unchanged. Keep `h("li", {}, text)` structure; no new elements, styles or controls.

## Phase 2

* Unit: extend `test_screen_is_wired_with_manual_path` or add one test that asserts the API home-case payload gives `null` vs `[]` vs list scope unchanged for the building rows and that `app.js` contains the labels and the `=== null ? "Unknown"` branch (static, as the file does today).
* Browser check: with existing DEP-1/HOLD-1 data assert the building panel text contains `Affected homes: ZF-2` and `Packages: PKG-SHARED`, the home panel does not, and a second observation is not added.

## Phase 3

From `src/api`: `python3 -m unittest tests.test_home_case_api` with `PYTHONPATH=../core/tests:../agents/tests`; ruff and mypy as the API README directs for touched Python; `node --check` on `app.js`. Browser: `flock -n /tmp/ama-rpi-heavy.lock` nonqueued; stop if busy.
