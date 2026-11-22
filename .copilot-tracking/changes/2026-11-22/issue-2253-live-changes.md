---
title: Issue 2253 changes
ms.date: 2026-11-22
---

Changes (tier FULL because src changed; the coordinator runs gates):

* `demo.css`: chart text 12 user units (was 1.25rem), SVG max-width 42rem, narrow-width text rule, stored line 1.5.
* `demo.js`: circles r=2.5 spaced at least 9 units apart, latest always marked, legend note when thinned.
* `test_epic149_child_ux_contracts.py`: wiring test for text units, max-width and marker thinning.
* Evidence: `docs/reference/research/issue-2253-resident-chart-2026-11-22.md` and its folder.

Validation run locally: `test_accessibility_baseline`, `test_content_standard`, `test_epic149_child_ux_contracts` (63 tests OK, PYTHONPATH pointing at the worktree because the editable install resolves to the main checkout); mypy clean in `src/api`; ruff check and format clean on the test; `checks/resident_sensors_browser_check.py` all PASS against worktree sources. Hosted CI not observed (no push).

| Criterion (issue 2253 expected behaviour) | Status | Evidence |
| --- | --- | --- |
| Axis and marker labels sized like body text | Proven locally; unproven live | 16.8 px vs 16 px body (after-local.json); live before 27.9 px |
| No label overlap | Proven locally; unproven live | text_overlaps 0 (after-local.json); live before 1 |
| Circle markers on stored readings as the legend states | Proven locally; unproven live | 25 distinct circles, 0 touching; legend notes thinning |
| Fix visible on deployed ca-resident-demo | Unproven | not redeployed; no production change authorised |
