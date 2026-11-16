# Details: issue #1828

## Critique amendments (single critique, all accepted)

* `check_browser_shortcuts` gains a 400 ms post-key observation hold before the unchanged assertion (catches delayed
  key-triggered reads; makes the pending-resize regression fail deterministically with the old wait).
* Premise check `check_viewport_change_requests_map`: a real viewport width change issues a map read, so ordinary
  viewport refetch is proven kept.
* `settle_map_reads` starts observing first, resets on any request or busy state, one 10 s deadline, listener removed
  in `finally`.

## Phase 1: regression

Add `check_shortcuts_after_pending_resize(page)` after `check_browser_shortcuts` definition. It records the current
viewport, sets width minus 40 px (real window `resize`, Leaflet starts its 200 ms debounced `moveend`), calls
`check_browser_shortcuts(page, "embedded after pending resize")`, then restores the viewport and lets the same settle
finish. Call it in `run_browser` immediately before the existing `check_browser_shortcuts(page, "embedded")`.
Failing-first: with the old wait the first call observes the debounced `/api/map` read. Evidence from a scratch driver
that reuses the check's own setup (`/tmp/1828`).

## Phase 2: settle

`settle_map_reads(page)`: wait for `#leaflet` not busy; attach a temporary request recorder; loop until a quiet window
of 400 ms (twice the 200 ms Leaflet debounce) passes with no new `/api/map?` request and the map is not busy; bounded
at 10 s, then raise AssertionError with the observed requests. Use it in `check_browser_shortcuts` instead of the
networkidle wait. The observation listener, the keys and `check(...no map requests...)` remain unchanged.

## Phase 3: validation

* Regression: 5 repeated runs under the lock.
* Full: `python -m checks.map_fullscreen_browser_check --axe /tmp/1828/axe.js --out <dir>` with
  `PYTHONPATH=tests:../core/tests:../agents/tests`; count PASS, no FAIL, no skip.
* Targeted: API unit tests touching map (`tests/` discover with map pattern) and check module compile/ruff.
