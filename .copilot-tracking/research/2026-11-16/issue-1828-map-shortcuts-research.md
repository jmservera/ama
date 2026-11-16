# Research: issue #1828 embedded map browser shortcuts refetch

* Date: 2026-11-16
* Base: main 18d3de459f20018e91fab3af87ab0d89123661c6, branch fix/map-browser-shortcut-refetch-1828
* Research disposition: executing (opening record; findings follow below)
* Tier: FOCUSED, subject to reclassification if a security, permission, SQL or gate change appears

## Intake

Original check stopped after 131 PASS lines with `AssertionError: embedded browser shortcuts issue no map requests`
(`src/api/checks/map_fullscreen_browser_check.py:82`). A diagnostic rerun saw one `/api/map` read on shortcut
presses. Cause (app event handling versus check wait logic) was not asserted in advance.

Update after investigation: disposition executed; Planning Readiness Ready.

## Sources read

Issue #1828, `.github/copilot-instructions.md`, case study original and addendum, `docs/reference/README.md`,
`docs/reference/memory.md` (context only), the read-only #440 `10-map.log` and its 2026-11-16 IoT map checkpoint
section (`cutover-evidence-pack.md` lines 8620-8660; not modified). Skills `web-design-guidelines` (source fetched
2026-11-16; only the first 3000 characters were retrieved, rest truncated) and `redesign-existing-projects` loaded.
No web source or style is edited, so no visual change is made.

## Reproduction at base (own venv with editable installs of this worktree; heavy lock free, taken with `flock -n`)

* Unmodified full check (`/tmp/1828/repro1.log`): PASS, 272 PASS lines, exit 0. The failure is timing dependent.
* Instrumented probe (`/tmp/1828/probe.py`, not committed) ran `check_expanded_filters` then `check_browser_shortcuts`
  with hooks on `window.fetch` (stack), `keydown` (capture), `resize` and `setTimeout(...,200)`. Six runs: 3 FAIL,
  3 PASS. Failing run `/tmp/1828/probe-1.log`:
  * window `resize` event (1280x900) at t=5926 ms, after "Exit expanded map";
  * map `fetch` at t=6126 ms, exactly 200 ms later, stack `draw <- moveend handler (app.js:2744) <- Leaflet fire`
    with no `invalidateSize` or key frame, so it is a timer callback;
  * first shortcut keydown at t=6135 ms, after the fetch.
* Vendored Leaflet `_onResize` calls `invalidateSize({debounceMoveend: true})`, which fires `moveend` from a 200 ms
  `setTimeout` when the container size changed.

## Diagnosis

Keys do not trigger the read: the `#leaflet` keydown handler returns early for ctrl, meta and alt, and the fetch
preceded every key event in the failing run. The read is the legitimate viewport refetch (new bbox) after the dialog
closes. The cause is the check wait logic: `aria-busy` is not set before the draw starts, and
`wait_for_load_state("networkidle")` returns immediately once that state already fired for the document, so neither
covers a pending 200 ms Leaflet timer. Host load shifts whether the timer lands before or after the observer is
attached, matching the repeat failures on the #440 host. App behaviour is correct and kept (Fluent 2, WCAG,
keyboard, assistive-technology and reduced-motion behaviour unchanged).

## Options

1. Settle in the check with a quiet window longer than the 200 ms debounce, assertion untouched. Chosen.
2. Suppress the resize refetch in the app: changes ordinary behaviour. Rejected.
3. Loosen or skip the assertion: forbidden.

## Deterministic regression

Change the viewport width (real `resize`, container width changes, Leaflet starts its 200 ms debounce) and run
`check_browser_shortcuts` immediately: fails every time with the old wait, passes with the settle, and still fails if a
key press itself issued a read.

## Boundaries

Do not touch `style.css` or `case_journey_browser_check.py` (#1297). Heavy lock was free at investigation time.
