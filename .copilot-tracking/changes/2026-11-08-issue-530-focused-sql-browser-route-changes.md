---
title: Issue 530 focused actual SQL and chat browser route changes
ms.date: 2026-11-08
---

* Records only. No source, tool, test, workflow or production edit. Base Main 0f05e9aa (re-fetched, unchanged). Plan and critique commit 442e2773e preceded the LIGHT checks.

## Source identity

* Tree ids of `src`, `tools`, `infra` and `.github` at HEAD equal those at 209e585cf (98b3178c, 2dd2ca78, c1c120a8, 7eb0d1da), so the C1 92-test and AST/dispatch results are source-equivalent. Production source outside tests differs from Main only in `src/api/checks/employee_chat_browser_check.py` (the C1 behaviour-preserving format fix).
* Module origins: `zava_forward.core`, `agents` and `api` resolve under this worktree `src/*/src` from the external venv. The unit module is `tools/test_rpi_checks.py` run from `tools/` in this worktree.

## LIGHT commands (venv /tmp/rpi-530-sqlbrowser-venv; caches and bytecode under /tmp/rpi-530-c3-cache)

* `python -B -m unittest test_rpi_checks` (tools): 92 tests OK, exit 0, no skips. The suite includes a synthetic loopback server `/healthz` call, authorised in the details; no external call.
* ruff check and format check: tools files pass; all four browser checkers pass (check 0, format 0) from `src/api`. `mypy --strict` on the two tools files: pass. `git diff --check`: pass.
* `git status --short --ignored` was empty before and after. No generated input needed relocation; prior journal `/tmp/rpi-530-c1-meta` and the C1 caches and venv are untouched.
* A pure `changed_groups` lookup (no runner execution, no probes) predicted `preflight, project-api, namespace, static, browser, mssql, tooling`.

## Prepared and UNEXECUTED

* Actual SQL: group `mssql` runs `python -m unittest -v <SQL_SELECTORS>` in `src/api`, in a runner-owned disposable SQL Server container, with `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, `ZF_SQL_DATABASE=rpi_disposable`, password auth and trust cert. All 21 methods must report `ok` exactly once: `MssqlChatPrivacy` 13, `MssqlChatRoleProjection` 4, `MssqlChatDemoMeter` 4 (exact headers in `SQL_CHAT_REQUIRED_TESTS`).
* Dedicated browser: `python -c BROWSER_ENTRY checks.employee_chat_browser_check --axe <out>/axe-4.10.3.min.js --out <out>/employee-chat` in `src/api`, timeout 900, `PYTHONPATH=<out>/safety:` plus api test paths. Required: pinned axe SHA-256 880970c0...a68bb, three states, zero violations, non-empty passes, `PASS employee chat: ` line, `employee-chat-results.json`, non-base requests aborted, failure controls from the runner regressions.
* Admission command shape (NOT ADMITTED): `python3 tools/rpi-checks.py --changed --jobs 1 --lock-timeout 0 --base <fresh-main> --out <new short external path> < /dev/null`; the lock is runner-acquired unless admission names `--heavy-lock-fd`. Resources: 2 CPU and 4 GiB per worker plus 1 GiB headroom on the shared 4 CPU host, SQL container `--memory=3g`, Chromium and axe downloads, canonical lock held throughout, no parallel database or browser use. The currently held lock (actual SQL lane) was not touched or polled.
