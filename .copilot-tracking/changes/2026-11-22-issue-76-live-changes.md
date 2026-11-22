---
title: Issue 76 live changes (2026-11-22)
ms.date: 2026-11-22
---

Refs #76. Tier FULL (src change); `rpi-checks.py --all` not run by instruction. No push, no Azure change, nothing to delete.

## Changes

* `src/core/src/zava_forward/core/taskqueues.py`: `clock_fields()` merges the target clock and named or escalation owner into every queue and case-card hazard and safeguarding clock; safeguarding label redacted without reason visibility.
* `src/api/src/zava_forward/api/web/app.js`: new `clockStatusText()` and a reworded safety-panel clock: hours remaining, overdue by N hours, completed, or time unknown with a next action. No negative hours.
* `src/api/tests/test_workbench_hazard_clock_owner.py`: three new tests.
* `docs/reference/research/issue-76-live-r7-2026-11-22.md` (+ proof script, output, screenshot), `docs/reference/README.md`, `docs/reference/log.md`.

No divergence from plan. A second wording site (safety panel) was found during the browser proof and fixed.

## Validation

* API: `test_workbench_hazard_clock_owner`, `test_accessibility_baseline`, `test_content_standard`, `test_safety_panel_ux`, `test_safety_screens`, `test_safety_screen_wcag_keyboard`, `test_role_screens`, `test_design_system`, `test_workbench`, `test_hazard_api`, `test_task_queue_api` and others: pass.
* Core: `test_taskqueues`, `test_hazard_referral`, both clock-owner modules, `test_rule_engine`: 113 pass, 1 skipped.
* ruff check and format clean; api mypy clean; core mypy 3 pre-existing errors, identical at baseline.
* Local Playwright on synthetic data: pass.

## Per-criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Default view single list, one status, one next action | Ticked in issue; not re-run | n/a |
| No perspective picker | Ticked; not re-run | n/a |
| Queue with visible definitions | Ticked; not re-run | n/a |
| Blocked steps reason, owner, action | Ticked; not re-run | n/a |
| Hazard and safeguarding show clock and named owner | Proven locally on synthetic data; unproven live (needs a deploy; live hazard lacks an awareness time and reads "time remaining unknown") | [r7 note](../../docs/reference/research/issue-76-live-r7-2026-11-22.md) |
| Ownership agreement (FR-034) | Ticked; not re-run | n/a |
| Single reset (FR-032) | Ticked; not re-run | n/a |
