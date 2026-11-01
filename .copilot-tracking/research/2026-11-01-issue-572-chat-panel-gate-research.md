---
title: Issue 572 chat-panel Chromium gate research
ms.date: 2026-11-01
---

Research disposition: executed (read-only, against `origin/main` 51657d30).

## Findings

* `tools/rpi-checks.py` already defines `CHAT_PANEL_BROWSER_SELECTOR` and `CHAT_PANEL_DISCOVERY_SKIP`, and runs the exact case in the browser stage with `ZF_BROWSER_TESTS=1` as a required suite (plan and runtime paths).
* The `opt-in local Chromium` skip is accepted only for the exact (test, reason) pair in the `project-api` group; any other pairing, or any integration-stage skip, raises `Unexpected required integration/dependency skip`.
* Delivered by merged PRs #575, #595, #600, #627 (all `Refs #572`).
* `tools/test_rpi_checks.py` has regression coverage: command is required and dispatched with the opt-in, discovery skip is exact and fails closed, receipt rejects missing flag/selector/execution, exact-success parser preserves other suite contracts, runtime requires exact success evidence.
* Focused run: `python3 -m unittest tools.test_rpi_checks` gives 55 tests OK.
* Acceptance criteria 1 to 3 are met on main. Criterion 4 (fresh complete exact-head gate including browser and MSSQL) needs the heavy local gate and Docker/Chromium prerequisites; the owner scoped this task to the focused tier, so it is unproven here.

Planning Readiness: Ready (no source change required).
