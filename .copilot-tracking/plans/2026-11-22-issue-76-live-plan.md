---
title: Issue 76 live plan and critique (2026-11-22)
ms.date: 2026-11-22
---

Refs #76. Tier FULL (src change); `rpi-checks.py --all` is not run by instruction.

## Critique (executed once, single pass)

* Risk: merging projection fields could leak a safeguarding label to roles without reason visibility. Disposition: accepted; label redacted to "Safety review clock" when `reason_ok` is false, with a test.
* Risk: changing the fail-closed rule for `noticed`-only items. Disposition: rejected; existing test and no-invented-time principle stay. Show the reason and next action instead.
* Risk: JS slice extraction in `test_workbench_hazard_clock_owner.py`. Disposition: accepted; new helper sits between `workSummary` and `workSteps`.
* Verdict: proceed, no user decision needed.

## Plan

1. `taskqueues.py`: add `clock_fields()` returning the projection fields; merge into `hazard_clocks` and `safeguarding_clocks` in `context()`.
2. `app.js`: helper `clockStatusText` giving "N hours remaining until the target", "overdue by N hours", "completed", or "time remaining unknown: awareness time not recorded; next action: record it"; use in hazard and safeguarding clock lines with the named owner.
3. Tests: core test for merged fields and redaction; API test for JS rendering (running, overdue, fail-closed).
4. Run core `test_taskqueues`, hazard clock tests, API targeted tests, `test_accessibility_baseline`, `test_content_standard`, ruff, mypy.
5. Local Playwright proof on synthetic data, screenshots in a research note; per-criterion table in changes.
