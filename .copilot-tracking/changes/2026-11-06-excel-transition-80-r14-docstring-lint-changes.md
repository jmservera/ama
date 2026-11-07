---
title: Issue 80 r14 changes, browser lint docstring correction
description: Actual change and checks for the child_env docstring wrap
ms.date: 2026-11-06
---

* Plan: [r14 plan](../plans/2026-11-06-excel-transition-80-r14-docstring-lint-plan.md). Planning records committed as c3e4db182 before the edit; source commit 261e9b96582496a2342349027bad4df5fe19fc9f.

## Change

* `src/api/checks/design_system_browser_check.py`, `child_env()`: the 108-column one-line docstring became a three-line wrapped docstring ("Server environment inherited from the caller." and "No credentials or endpoints are passed; bytecode controls are kept."). 4 insertions, 1 deletion; the `keys` tuple, code, assertions and browser behaviour are unchanged. No test added.

## Checks (from `src/api`, pinned `/mnt/ama-gates/e80-full-r68/venvs/api/bin/ruff`, version 0.17.1, `--no-cache`)

* `ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100` over the three browser-group files: exit 0, "All checks passed!".
* `ruff format --isolated --line-length 100 --check` over the same files: exit 0, "3 files already formatted".
* Ignored-inclusive status after the checks showed only the intended modification.

## Limits

* The browser journeys, FULL, SQL, Docker, scanners and installs were not run. The failed receipt `/mnt/ama-gates/e80-full-r68` (SHA-256 34e8c122d6a1f0e12263a2d1f7fbba9d2d4e274f7fbaae34988d06d76419a609) is retained unchanged and does not cover this head. The schema_download check file is not in the gate's browser lint list and was not linted here. A new FULL on the final head is pending coordinator admission.
