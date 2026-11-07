---
title: Issue 80 r14 details, browser lint docstring correction
description: Exact edit and check commands for the child_env docstring correction
ms.date: 2026-11-06
---

* Plan: [r14 plan](../plans/2026-11-06-excel-transition-80-r14-docstring-lint-plan.md).

## Phase 1 edit

* File `src/api/checks/design_system_browser_check.py`, function `child_env()`. Replace the single 108-column docstring line with:

```python
    """Server environment inherited from the caller.

    No credentials or endpoints are passed; bytecode controls are kept.
    """
```

* Keep the `keys` tuple and the dict comprehension unchanged.

## Phase 2 checks (from `src/api`, worktree files, pinned `/mnt/ama-gates/e80-full-r68/venvs/api/bin/ruff`)

* `ruff --version` (expect 0.17.1).
* `ruff check --isolated --no-cache --select E,F,I,B,UP --target-version py312 --line-length 100` over `checks/design_system_browser_check.py`, `checks/regulatory_ux_check.py`, `checks/case_journey_browser_check.py`.
* `ruff format --isolated --no-cache --line-length 100 --check` over the same files.
* `git diff --stat` and a diff of the check file; byte-compare other source with `git diff --quiet` against HEAD outside that file.
* Success: both ruff commands exit 0 and only the docstring differs. The browser journeys are not executed.
