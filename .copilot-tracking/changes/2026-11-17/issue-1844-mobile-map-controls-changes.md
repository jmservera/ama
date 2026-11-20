---
title: Issue 1844 changes
ms.date: 2026-11-17
---

## Files

* `src/api/src/zava_forward/api/web/style.css`: narrow-width static home summary.
* `src/api/checks/map_fullscreen_browser_check.py`: regression.

## Order divergence (recorded honestly)

The plan, details and changes files and the `implement-start` witness were written after the source edits, because the code was explored and edited in one pass. The witness boundaries therefore follow the edits.

## Evidence (directory /home/azureuser/.local/share/ama/phase-witness/1844)

* Failing first, unchanged CSS: `AssertionError: tiles unavailable 320x568: no marker or zoom control is covered ({'controls': 5, 'covered': 5})` in `failing-first.txt`. An earlier failure run is the same assertion.
* Served-byte identity: `PASS served app.js bytes match the checked-out source` and the same for `style.css` (sha256 of served body equals the file on disk), printed in `rerun2.txt`. The check reads from the served loopback app only; it does not prove the checkout equals the retained candidate 167eb9c6.
* With the fix, `rerun2.txt`: rc 0, 380 PASS lines, no skips. All 8 states (320x568, 320x900, 390x568, 390x900; tiles unavailable and synthetic tiles): 5 of 5 controls uncovered at 9 of 9 sampled points, summary does not overlap the map, no horizontal overflow, attribution link reachable and uncovered after scrolling, Escape and Close return focus to the marker, opening another home replaces the summary and focuses its heading.
* Existing axe scans in the same run reported zero violations; incomplete axe items and assistive-technology testing remain open. No conformance claim.
* Base flake: `filter label and focus fit at 390x568` (existing `check_expanded_filters`) failed in 1 of 4 runs on unchanged code (`base4.txt`) and 1 of 3 on fixed code (`after-fix.txt`, `rerun1.txt`); the next run passed. Not caused by this change; left unfixed.
* `map_tile_status_browser_check`: pass. `python3 -m unittest test_map_fullscreen test_map_viewport_premise test_map_status_locators test_design_system test_accessibility_baseline`: OK. `node --check app.js`: ok. `mypy src` (src/api): no issues. `ruff format --isolated --line-length 100 --check` on the changed file: clean (48 unrelated files already would reformat on the base).
* Core `test_scenario_manifest test_needs_inventory`: 19 tests OK. The workbench recipe was not changed, so no manifest SHA update was needed.

## Not covered

Expand, collapse and reopen at narrow widths is covered by existing 320/390 expanded-dialog assertions, not by the new test. Desktop unchanged by construction (rule is max-width 600px) and by the existing desktop checks passing.

## Correction cycle 1 (2026-11-17)

Started; results are appended below as they are produced. The earlier "Not covered" statement above (expand/collapse/reopen only covered by existing assertions) is retained as the adverse record that the review found insufficient.

### Changes

* `src/api/checks/map_fullscreen_browser_check.py`: added `check_narrow_keyboard_order` (Shift+Tab from the open summary heading reaches all 3 markers and 2 zoom controls, reverse order follows DOM order, none covered at the moment it holds focus, Tab returns forward) and `check_narrow_expand_reopen` (at 320/390: open a home, Expand map, same summary shown with heading focused, summary intercepts no control, Exit returns focus to Expand map, reopen reselects the same home, Escape closes the summary and returns focus to the marker). Removed the unused `base` parameter of `check_served_source_identity`.
* CSS unchanged in this cycle.

### Validation (run from `src/api`, axe 4.10.3 sha256 880970c0...a68bb)

* `PYTHONPATH=tests:../core/tests:../agents/tests python3 -m checks.map_fullscreen_browser_check --axe <axe> --out <new dir>`: with fix, 2 runs, both rc=0, 436 PASS each; no flake observed in these two runs (the known intermittent `filter label and focus fit at 390x568` was not seen; it is not fixed).
* Failing-first, CSS reverted to the base: the hard-fail run stops at the first assertion (`tiles unavailable 320x568: no marker or zoom control is covered ({'controls': 5, 'covered': 5})`). A soft-fail harness (`check` replaced by a recorder, temporary, outside the repo) with the CSS reverted gave 24 failures: per viewport (8) the pre-existing "no control covered", "summary does not overlap the map" and the NEW "no control is covered at the moment it holds keyboard focus". The new expand/reopen assertions pass without the CSS because the expanded dialog has its own layout; they guard criterion 3 (focus and selection preservation), not the CSS. CSS restored afterwards (`git diff` shows no CSS change).
* `ruff format --isolated --line-length 100 --check` on the changed file: clean. `mypy src` (src/api): no issues.
* Finding while writing the test: in the expanded dialog a Leaflet attribution link can overlap a marker at 320x568 (pre-existing Leaflet geometry, not the summary); the dialog assertion therefore tests that the summary intercepts no control, not that nothing does. Recorded, not fixed.

### Limitation

The rule is `max-width:600px`; widths 321-600px (e.g. 480, 600) get the same layout by construction but are not exercised by the check (viewports are 320 and 390). Above 600px the original overlay is unchanged.

### Branch note

`git branch -a | grep mobile-map-assessment` and `git ls-remote` found no `test/mobile-map-assessment-1818-restart` branch locally or on origin (see final reply).
