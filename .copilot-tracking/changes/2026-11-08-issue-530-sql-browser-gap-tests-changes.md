---
title: Issue 530 actual SQL and employee browser gap tests changes
ms.date: 2026-11-08
---

* Base: Main 0f05e9aa, plan and critique commit 285280edb. Refs #530 only.

## Changes

* `tools/rpi-checks.py`: the browser group now runs `employee_chat_browser_check` with pinned axe and an owned fresh output inside the existing `try/finally`. It copies `employee-chat/axe-results.json` to `employee-chat-results.json`. The receipt verifier requires the exact command, the `PASS employee chat: ` line, the file, three exact states, zero violations and non-empty passes. The SQL group requires 21 named new MSSQL test methods to report `ok` exactly once, parsed from verbose headers. Fail-closed behaviour and all 17 groups are unchanged.
* `src/api/tests/test_mssqlstore.py`: new `MssqlChatPrivacy` (13 inherited), `MssqlChatRoleProjection` (4) and `MssqlChatDemoMeter` (4, with `kinds()` and the seed test overridden for the non-iterable cursor). They are skipped unless `ZF_TEST_MSSQL=1`, and they reuse existing synthetic fixtures. The module is already in `SQL_SELECTORS`.
* `tools/test_rpi_checks.py`: fixtures plus five new regressions and a tamper case.
* No production, schema, workflow, dependency or README change.

## LIGHT evidence (venv /tmp/rpi-530-sqlbrowser-venv, module paths under this worktree src/*/src)

* `python -m unittest test_rpi_checks` (tools): 91 tests OK, exit 0. Printed workflow drift and tool-missing text is expected fixture output.
* ruff (E,F,I,B,UP) and format check: pass. `mypy --strict` on both tools files: pass. `git diff --check`: pass.
* `test_mssqlstore` without ZF_TEST_MSSQL: 226 tests, skipped 217 (baseline 205 and 196), so 21 new skips. This is an unverified skip, not SQL acceptance.
* SQLite logic proxy (scratch under /tmp/rpi-530-sqlbrowser-out/proxy, `wipe` and `factory` patched to SqlStore): 21 tests OK, exit 0. It is a logic proxy only, not an MSSQL result.
* No runner, dry run, probe, lock, SQL, Docker, browser or live call.

## Gaps

* No actual MSSQL or Chromium/axe execution. Risks on real SQL Server remain until the future gate.
* `checks/employee_chat_browser_check.py` has 17 ruff errors and fails the format check under the browser lint profile, so it is not added to lint. This needs a separate fix scope.
* Native CI does not run the chat browser check (workflows out of scope).
