---
title: Issue 531 retry-check drift details
ms.date: 2026-11-03
---

## Phase 1: browser check

* `companion_failure_check`: expected requests for a blocked required script 3 to 4.
* `helper_bootstrap_check`: terminal when `failures == 4`; terminal request count 4 (still 2 for missing global, unready helper and unready method, which stop without retry).
* `run_browser`: helper bootstrap sweep covers failures 1 to 4.

## Phase 2: README

* `src/api/README.md` "Workspace script recovery (#524)": retries after 250, 500 and 1500 ms; three-retry budget.

## Phase 3: validation

* Focused unittest modules, `checks.loading_briefing_browser_check` with pinned axe 4.10.3, `checks.employee_briefing_browser_check`, ruff, mypy with `--cache-dir=/tmp/mypy-531`.
