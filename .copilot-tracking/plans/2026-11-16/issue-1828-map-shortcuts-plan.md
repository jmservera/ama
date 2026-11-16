# Plan: issue #1828 settle pending map debounce before shortcut observation

* Details: [issue-1828-map-shortcuts-details.md](../../details/2026-11-16/issue-1828-map-shortcuts-details.md)
* Research: [issue-1828-map-shortcuts-research.md](../../research/2026-11-16/issue-1828-map-shortcuts-research.md)
* Tier: FOCUSED. Reclassify FULL if any security, permission, SQL, deployment or gate change appears.

## Phases

* [ ] Phase 1: failing-first regression `check_shortcuts_after_pending_resize` in `src/api/checks/map_fullscreen_browser_check.py`; run it against the unchanged wait and record the failure.
* [ ] Phase 2: add `settle_map_reads` and use it in `check_browser_shortcuts` in place of the networkidle wait; assertion unchanged.
* [ ] Phase 3: validate: regression passes repeatedly, full map check with axe passes, targeted API tests, ordinary request checks intact; record counts.
* [ ] Phase 4: changes record, review, commit.

## Constraints

* App JS unchanged; no edits to `style.css` or `case_journey_browser_check.py`.
* Existing assertion text and semantics preserved.
* Heavy browser runs only under a free `/tmp/ama-rpi-heavy.lock` taken with `flock -n`.
