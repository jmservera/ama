---
title: Issue 530 focused actual SQL and chat browser route research
ms.date: 2026-11-08
---

* Disposition: executed (read-only). HEAD 209e585cf (tree 6dc15119), Main 0f05e9aa unchanged on fetch. Refs #530 only. Preparation only: nothing heavy runs.
* Owner direction at 08:15 supersedes the earlier Full17 and Main-only full plans: avoid blanket local full validation; run relevant unit, static and type checks plus affected actual SQL and Playwright, then rely on fresh exact-head CI for the broad merge gate with actual selection and skips checked.

## Findings

* Hosted CI selects `test_mssqlstore` as a whole module, so the three new classes are selected there, but a CI pass proves the 21 methods ran only if its verbose log shows each `ok`. Hosted CI does not run `employee_chat_browser_check`.
* Maintained actual-SQL route: runner group `mssql` runs `python -m unittest -v <SQL_SELECTORS>` in `src/api` (`tools/rpi-checks.py` about line 1241), against a runner-owned disposable SQL Server container (`mcr.microsoft.com/mssql/server:2022-latest`, `MSSQL_MEMORY_LIMIT_MB=2048`, `ZF_TEST_MSSQL=1`, `ZF_SQL_SERVER=127.0.0.1`, `ZF_SQL_DATABASE=rpi_disposable`, password auth, trust cert). `SQL_SELECTORS` starts with whole-module `test_mssqlstore`, and `SQL_CHAT_REQUIRED_TESTS` (21 exact verbose headers) makes each new method required to report `ok` exactly once. `--extra-test` accepts only `PROJECT:test_module[.Class.method]` project selectors, not the mssql group, so it is not a narrower SQL route.
* Narrowest maintained actual route without tool edits is therefore `--changed` (or `--all`) with the mssql group. A pure lookup of `changed_groups` (no runner execution, no probes) for the actual diff against Main returns `preflight, project-api, namespace, static, browser, mssql, tooling`: seven groups, no images, scans, SBOM or other project groups. That selection also runs the browser group (which includes the chat check) and the tooling suite. It is a static prediction, not a gate run, and the actual runner selection must be re-read at admission.
* Dedicated browser route: the browser group runs `[python, -c, BROWSER_ENTRY, checks.employee_chat_browser_check, --axe, <out>/axe-4.10.3.min.js, --out, <out>/employee-chat]` in `src/api`, timeout 900, `PYTHONPATH=<out>/safety:` plus api test paths, pinned axe SHA-256 `880970c081707360e64f34cea25ff91892f5bc95675b0776925b9709dd8a68bb`. Required evidence: `PASS employee chat: ` line, `employee-chat-results.json` with exactly three states, zero violations, non-empty passes. Network egress is limited by the check's route abort of non-base URLs.
* Resources: the maintained worker guard needs 2 CPUs and 4 GiB per worker plus 1 GiB headroom on a shared 4 CPU host; SQL container memory 2 GiB; one canonical lock `/tmp/ama-rpi-heavy.lock` must be held throughout, no parallel DB or browser assumption. The lock is currently held by the actual SQL lane (PID 1500305, parent 1499773): not touched, not polled.
* Limits: SQLite proxies, skip-only imports and static checks are not actual SQL or browser results. Prior 92-test and AST/dispatch proof is historical exact-code evidence only if source, tool and module origins are re-proved now.

## Planning readiness

* Ready for a prospective plan plus LIGHT re-proof. No source, tool, test or workflow edit.
