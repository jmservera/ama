---
title: Issue 530 C1 chat checker lint and ignored-input hygiene changes
ms.date: 2026-11-08
---

* Base: Main 0f05e9aa, HEAD before C1 1c771189, plan and critique commit c26a1b3f3. Refs #530 only. Earlier records are unchanged.

## Changes

* `src/api/checks/employee_chat_browser_check.py`: ruff format, import sorting in the gate cwd (`src/api`), three over-long string splits by implicit concatenation, one `# noqa: E501` on the embedded JavaScript string so its bytes stay identical, and `denied_reply(route, *, denied=denied)` for B023 (keyword-only per critique F1). Proof: the AST equals the original after normalising import order and the one keyword-only default. Playwright `wrap_handler` calls the callback with only the positional route (`arg_count` ignores keyword-only parameters), shown with a scratch call that returned `('R', 401)` and `('R', 403)`.
* `tools/rpi-checks.py`: `employee_chat_browser_check` added to both browser lint tuples (planned and `Runner.browser`).
* `tools/test_rpi_checks.py`: `test_employee_chat_checker_is_linted_in_planned_and_executed_browser_contracts`. It fails when either tuple alone omits the checker (omit planned: `[] != [check, format]`; omit executed: lint calls lack the checker).
* No workflow, native CI, production, schema or SQL test change. Hosted CI parity for the chat check stays a residual gap.

## LIGHT evidence (external venv /tmp/rpi-530-sqlbrowser-venv, caches under /tmp/rpi-530-c1-cache)

* `python -m unittest test_rpi_checks` (tools): 92 tests OK, exit 0. Earlier runs in this phase were exit 1 because of a wrong slice and a missing fixture in my new test, both fixed in the test only.
* ruff (E,F,I,B,UP, line 100) and format check: tools files pass; the checker passes from `src/api`; the other three browser checkers still pass. `mypy --strict` on both tools files: pass. `git diff --check`: pass.
* Module origins: `zava_forward.core`, `agents` and `api` resolve under this worktree `src/*/src`.
* No SQLite or MSSQL suite rerun (unmodified). No runner, probe, lock, SQL, Docker, browser or live call.

## Ignored-input normalization

* Twelve ignored generated paths (135 files) were created after plan commit 285280edb by this RPI's pip installs, ruff, mypy and unittest runs. They were untracked, not source, receipt or resume inputs, and the editable installs use path `.pth` files. Each was copied to `/tmp/rpi-530-c1-meta/moved/`, byte hashes were verified equal, then only that exact path was removed. Journal: `/tmp/rpi-530-c1-meta/journal.json` (SHA-256 per file). Future caches use `PYTHONPYCACHEPREFIX`, `RUFF_CACHE_DIR` and `MYPY_CACHE_DIR` outside the worktree. After the move `git status --short --ignored` showed only the three intended modified files.
