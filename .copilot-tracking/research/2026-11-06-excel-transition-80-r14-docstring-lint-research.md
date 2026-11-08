---
title: Issue 80 r14 research, browser lint docstring correction
description: Prospective research for the single Ruff E501 that failed the native FULL browser group
ms.date: 2026-11-06
---

* Task: excel-transition-80-r14-docstring-lint, parent r13. Intake HEAD d633b69e6e12afc65cf204516b85d560e3578b3e, tree 83e73c34f7b494cc6fface1af22449b38c1efa25, parent ead177ef90d24666557708ea344848a1be43bdf8 (ancestor, preserved), origin/main bb3a3b03 as last recorded. Ignored-inclusive status is empty at intake.
* Disposition: executed (read-only). Planning Readiness: Ready.

## Facts from the failed FULL

* Failed native FULL output `/mnt/ama-gates/e80-full-r68`, receipt SHA-256 34e8c122d6a1f0e12263a2d1f7fbba9d2d4e274f7fbaae34988d06d76419a609, status failed. Retained unchanged.
* The browser group's first recorded command (`0074-browser.log`, exit 1) was `<venv>/bin/python -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 checks/design_system_browser_check.py` from `src/api`, with the failed group's own pinned Ruff 0.17.1 (`venvs/api/bin/ruff`).
* The log holds exactly one finding: E501 (108 > 100) at `checks/design_system_browser_check.py:242:101`, the one-line docstring of `child_env()` added in r11: "Server environment inherited from the caller: no credentials or endpoints, bytecode controls kept."
* The runner stops the group at the first failing command, so the group's remaining lint and format commands for `design_system_browser_check`, `regulatory_ux_check` and `case_journey_browser_check` (see `tools/rpi-checks.py`, browser group, `lint()` helper: `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` and `ruff format --isolated --line-length 100 --check`) and the browser journeys never ran. MSSQL was blocked by that prerequisite. Nothing in the receipt proves those other files pass; this correction only proves the lint and format commands, not the journeys.
* Tool state: `venvs/api/bin/ruff` reports 0.17.1, the pinned version. The system `ruff` is 0.17.3 and is not the gate tool.

## Scope

* The only authorised source change is shortening or wrapping that docstring without changing its meaning, code, the `keys` allowlist, assertions, browser behaviour or acceptance scope. No test is added for a docstring.
* r12 and r13 recorded the 124-test pass, Ruff and format checks of that time with the system tooling at the line-length the project configuration uses; the gate's `--isolated --line-length 100` form is stricter and was not run by those rounds. Recorded as a limitation, not rewritten.

## Limits

* LIGHT checks only: pinned Ruff over the three gate-listed browser files, cache disabled. No install, Docker, SQL, browser, scanner or FULL run. No claim of browser, FULL, WCAG, assistive technology, Azure, every-list or owner-threshold acceptance. A new commit invalidates the old-head receipt; a new FULL is a later coordinator admission.
