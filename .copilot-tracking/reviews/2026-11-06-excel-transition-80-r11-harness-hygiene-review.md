---
title: Issue 80 r11 Review (final, author-only)
description: Author review of the harness hygiene correction and preservation proof
ms.date: 2026-11-06
---

* Boundary: commits 004c0a005 (research, plan, details) and b9b47b3a0 (harness, test, README, changes, state) over 1fa33543. Changes: [changes](../changes/2026-11-06-excel-transition-80-r11-harness-hygiene-changes.md).
* Review execution: executed once by the author, not independent. Outcome: conformant for the bounded light scope; end-to-end effect unproven.
* Web guidelines: no web file (JS, CSS, HTML) was changed or read for review; the changes are Python harness, a unit test and README text, so the web-design-guidelines fetch was not repeated. Not claimed as a web review.

## Findings

* src/api/checks/design_system_browser_check.py scratch_parent: the in-checkout refusal uses `resolve().is_relative_to(ROOT)`; a symlink outside pointing inside is refused, a path inside via symlink out is allowed. Acceptable.
* src/api/checks/design_system_browser_check.py child_env: passes only bytecode controls beyond the old three keys. No credential or endpoint inheritance added.
* Residual: the parent process of a later run must also run with bytecode disabled; the harness cannot control that. The fix is verified only by unit tests; the real run must show zero new ignored paths.
* Residual: the preservation script is an external, unreviewed helper (`/mnt/ama-gates/e80-r11-r64-1106/preserve.py`), used because `tools/tracking_retention.py` is bound to the PR 438 manifest. Its first restore attempt failed on modes and is preserved.
* Residual: the archive snapshot was taken before the r11 changes, state and this Review existed; those are new files, not modified ones (`protected-compare.json` shows no modified tracking file at snapshot-plus-proof time).

## Completed versus deferred

* Completed: RED then GREEN of 4 new tests; 124 tests in ten modules, Ruff, format, mypy (188 files); production byte identity for four src trees; archive, full readback, mode-correct restore and protected comparison.
* Deferred, not run: browser rerun, FULL with pip-installed distributions, SQL, independent exact-head review, hosted CI, any deletion. The worktree is NOT clean: three ignored `__pycache__` directories and an empty `.venv` remain by design pending root authorisation. Publication blocked. No ticks or closures.
