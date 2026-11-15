---
title: 1530 c2 rebase plan
ms.date: 2026-11-13
---

## Plan

* [x] P1 Rebase onto 2c71e2c21 (done during research: clean, no conflicts).
* [ ] P2 Verify digests: scenario-manifest recipe is workbench_browser_check.py (unaffected); regenerate cutover inventory and compare.
* [ ] P3 Open `.safety-details` and `.safety-optional` before the populated-safety axe scan in `case_view_ux_browser_check.py`.
* [ ] P4 Run listed tests, browser check with axe, ruff, mypy; recompute digests only if the audit says so.
* [ ] P5 Independent code-review, local commit (no push).

Details: .copilot-tracking/details/2026-11-13/1530-c2-rebase-onto-main-1819-details.md

## Critique amendments (PC-001..003 applied)

* P3 now signs in as `pam@example.test` (Retrofit Programme Manager, in SAFETY_ROLES) and adds an accepted hazard addressed to PM-01 so `.safety-optional` renders; assert both disclosure types are opened before axe.
* P2 verifies all four manifest hashes with sha256sum, not only the recipe.
* P4 commands: unittest test_safety_panel_ux test_hazard_api test_content_standard test_accessibility_baseline test_design_system test_case_journey test_scenario_manifest test_needs_inventory test_cutover_audit; `python -m checks.case_view_ux_browser_check --axe`; ruff check/format --check src/api; mypy in src/api. Pass = all green.
