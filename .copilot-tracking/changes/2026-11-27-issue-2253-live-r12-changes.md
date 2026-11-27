---
title: Issue 2253 r12 changes
---

# Changes

Tier FULL (src change); the coordinator runs the complete gate. No `rpi-checks.py --all` was run.

* `src/api/src/zava_forward/api/resident_demo/web/demo.js`: the "Latest stored" label moves to the bottom of the plot when readings or forecast squares sit near the top in its x span (previously fixed at y=26, overlapped markers at humidity 95 percent).
* `src/api/tests/test_resident_sensor_chart_browser.py`: new test for high-value readings on both metrics (3 history sizes); asserts no text overlap and no circle or square over a label. Without the fix it fails 6 sub-cases; with it, passes.
* `docs/reference/research/issue-2253-live-r12-2026-11-27/`: probe plus `probe-before.txt` (10 collisions) and `probe-after.txt` (none).

Validation run: browser test, test_accessibility_baseline, test_content_standard, test_epic149_child_ux_contracts (all OK), `python3 -m mypy` in src/api (no issues), ruff check and format on the test file.

Incident: `git stash pop` on the shared repository stash returned another worktree's stash (not mine). I reverted those files here and saved the content as `foreign-stash-popped.patch` in the evidence directory so the coordinator can restore it.

## Per-criterion table

| Criterion (issue 2253 expected result) | Status | Evidence |
| --- | --- | --- |
| Axis and marker labels sized like body text | Proven in a real Chromium harness running the shipped demo.js and demo.css (ratio 0.75-1.25); not re-proven on the live app for this change | existing test, r1-r11 live notes |
| No overlap of "Latest stored" with ticks or markers | Proven locally including the new high-value case (fails before, passes after); live revision does not yet contain this change, so live is unproven | new test, probe-before/after |
| Circle markers on stored readings as legend states | Proven locally (circleCount, radius >= 2.5); earlier live proofs in r8-r11 notes | existing test |
| Live demo (ca-resident-demo) shows the fix | Unproven for this change: no deploy performed (no production changes authorised for this task) | n/a |
