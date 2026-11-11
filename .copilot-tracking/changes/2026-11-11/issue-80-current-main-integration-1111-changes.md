---
title: Issue 80 current-main integration changes
description: Prospective and actual record
ms.date: 2026-11-11
---

## Prospective (before implement-start)

* The only source-tree change is the already committed ordinary merge `ef16f3e2` of main `0509ddce` with the additive GET inventory resolution. No further source, test, checker or README edit is planned. Checks per the plan; results appended after execution. Only own tracking files are committed afterwards.

## Actual (after implement-start)

Tested tree: the actual committed merge `ef16f3e21454b915a46c930a90cc7d3c010bf055` (tree `4168b3139141318c2cb396d237b22123a37e0901`) in this worktree, cwd `src/api`, venv `/tmp/ama-80-audit-venv-1110` (editable installs of this worktree; import origins asserted for server, staff_intake, resident_decisions), owned temp `ZF_DATA`. Only untracked own tracking files were present. Evidence: `phase80-current-main-integration-evidence-1111/` (`preflight.log` has served hashes: server.py `e14162c0...70ae`, app.js `fb5142bb...6507`, index.html `3270ca3e...e146`, staff-intake.js `8dea09f5...c277`, ops.js `93b32aa2...4972`, checker `59b3e44c...f7a1`; axe asset matches the pin).

Direct exits, all 0:

* Role endpoint inventory (merged); staff intake API; content standard; child CSV 13; handoff API; case journey 31; list export 11; static 60; resident API; Atlas checker test; core resident decisions.
* Real Chromium with built-in locks, no outer flock, 0 skips: child UI 6, handoff guidance 9, staff intake browser 2 (`ZF_STAFF_INTAKE_BROWSER=1`, pinned axe).
* ONE whole `capacity_browser_check --axe` (checker's own lock), exit 0, no skips, both delayed-401 iterations PASS and empty-capacity control PASS. Served `index.html`, `server.py` and `staff-intake.js` differ from the earlier runs, so this is a fresh run; earlier runs are historical.
* Ruff check and format (147 files), mypy 230 files, Node syntax `app.js`, `ops.js`, `staff-intake.js`.

Qualified, preserved:

* The first mypy attempt failed (module absent in the owned venv); `pip install mypy==2.4.0` was run in that owned venv only after the failure (`pip-mypy.log`), rerun `mypy-r2` exit 0.
* Not run, not claimed: staff intake API SQL tests (34 skipped, need task-owned SQL Server; SQL not admitted), Atlas browser 3, resident browser 1, core SQL 149 skipped.
* Review of the merge resolution: only `GET_ENDPOINTS` conflicted; resolution is the union of main's `field-intake` and the child's `unaccepted.csv`; no source file hand-edited.
