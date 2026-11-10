---
title: Issue 530 actual SQL and employee browser gap scope research
ms.date: 2026-11-08
---

* Task: `issue-530-sql-browser-gap-scope` (child of `issue-530-sql-browser-prep`). Research disposition: executed, read-only on trusted maintained source at clean HEAD `6c7536d230517603d6f7dc2cff7fa564591f4795` (tree `bd64d3bf1f252116b3da45516da2f1068c39cb16`), `origin/main` re-fetched and equal to `0f05e9aae70768def8d1d9c300215f9ee2f11638`. Planning Readiness: Ready.
* Scope: the two gaps named by the owner, as one bounded continuation of the #530 local unit/browser/SQL criterion. No new feature and no production defect is asserted. No runner, probe, lock, Docker, SQL, browser, image, scan or live call is made now.

## Gap 1: employee chat Chromium/axe check outside the maintained gate

* `tools/rpi-checks.py` has two parallel definitions of the browser group: the planned contract in `required_checks` (around line 1073, used by `verify_commands`) and the executed `Runner.browser()` (around line 2195). Both must change together. The verifier derives every command identity (group, argv, cwd, env, timeout, suite, integration) from the plan and walks `receipt["commands"]` in order, rejecting any extra or missing row.
* `checks/employee_chat_browser_check.py` CLI: `--axe <file>` (required, sha256 must equal `AXE_SHA256`) and `--out <dir>` (required). It runs the shared synthetic loopback server through `design_system_browser_check.main(..., synthetic_chat_privacy=True)`, asserts inside `scan()` that axe finds no violation on `#employee-chat`, prints one `PASS employee chat: ...` line on success, and writes `<out>/axe-results.json`, a list of exactly three scans with states `actual-model-unavailable`, `synthetic-cited-answer`, `demo-disclaimer-model-answer`, each `{state, violations, passes}`.
* It reuses the same entry mechanics as the already maintained `case_journey_browser_check`: `BROWSER_ENTRY` wrapper (external scratch via `TMPDIR`), `PYTHONPATH=<output>/safety:` plus `test_paths("api", True)`, pinned axe at `<output>/axe-4.10.3.min.js`, an owned `--out` under the new gate output. It is not unittest, so unittest skip accounting does not apply; skip handling must be a non-unittest rule (no `skipped` text in the log or results, exact three states).
* The existing verifier pins `case-journey-results.json` as a copied top-level file plus `required_files`. The same pattern is the smallest consistent derivation for the chat results.
* The native CI (`.github/workflows/src-ci.yml`) also runs only `employee_acceptance_check`; workflows are out of scope and stay unchanged. Native CI parity for the new browser step is a recorded residual gap.

## Gap 2: actual-MSSQL chat role projection, isolation/privacy, finite cost ledger

Contract ambiguities found before code:

* `api/tests/test_chat_isolation.py` and `test_role_matrix.Matrix` run over the JSON `Store` (`MatrixServer.setUpClass` builds `Store`), not SQLite `SqlStore`. Its assertions mutate `store.data`, `store.staff` and `store.cases` in memory, so it cannot be inherited onto `MssqlStore` without invented behaviour. It is neither an actual-MSSQL nor an SQL proxy; it must stay as is.
* `test_chat_panel` exists in both `src/api/tests` and `src/core/tests`. From `src/api` with `PYTHONPATH=tests:../core/tests:...` only the API module is importable by that name, so core `SqlRosterTests` (SQLite `sqlite3.connect(store.db_path)` writer) cannot be selected or inherited from an API SQL test by module name. The roster-revocation behaviour must be re-expressed in a dialect-neutral way, not by copying a SQLite writer.
* `core/tests/test_chat_privacy.ChatPrivacyBehaviour` is a mixin (`make_store(tmp)`), the same pattern `MssqlChatThreads` uses for `ChatBehaviour`; the SQLite-only `SqlChatPrivacy.test_memory_table_...` is outside the mixin. Reusable on `MssqlStore` through the existing `factory`/`wipe` helpers.
* Finite cost ledger for chat is `chat_demo_meter` plus `ai_consumption.Consumption` over `assistant_events`. The only SQL-store test is `api/tests/test_continuity.ChatDemoMeterOnSqlStore` (SQLite `Base`). `test_assistants.MssqlFixture` provides the established actual-MSSQL store pattern (database `zf_test_assistants`, local server guard, table reset). `assistant_events` has `id` as primary key (random uuid), so an unordered `SELECT body FROM assistant_events` has no defined order on SQL Server; the SQLite test `test_demo_path_seeds_synthetic_records_and_admits_exactly_one_call` asserts event order from such a query. The ledger itself reads with `ORDER BY at,id`. The MSSQL variant must assert kinds order-independently, not copy that order assertion.
* `SQL_SELECTORS` already contains the whole module `test_mssqlstore`, and the native CI selectors (`src-ci.yml`, `mvp-ci.yml`) also run `test_mssqlstore`. New classes inside `test_mssqlstore` are therefore selected by the maintained SQL group and by native CI without a workflow edit and without a duplicate selector run. The gap is not selection but required-execution proof: the verifier only needs zero unexpected skips, so a future admission could pass with the new classes silently absent. Smallest tool scope: a required-test list the SQL group verifier checks (each must report `ok`).
* Existing coverage that is NOT a substitute: `MssqlChatThreads` (thread storage), `MssqlLedgerMigration` chat-memory migration, `MssqlLedgerTests`/release classes (assistant events, not chat roster or privacy), the JSON-store isolation tests, and SQLite proxies.

## Environment facts

* No MSSQL, Docker or Chromium is available or admitted now; heavy lock holder is the 86 lane. LIGHT checks only: new external venv with pip from this worktree's `src/{core,agents,api}`, unit and static checks, with module-origin proof.
* Unit mock outputs for the runner regressions are fixtures and negative cases, not gate executions. MSSQL classes can only be import- and skip-checked now; a scratch SQLite stand-in may exercise class logic and is a proxy, not SQL acceptance.

## Evidence boundary

Synthetic UI and actual-SQL regressions are separate local checks. They are not real sign-in, private-runner authority, model price or budget approval, a real-model grounded answer or serving attestation, named bounded-agent confirmation, screen-reader or voice-control testing, resident, legal or professional approval, and not #530 closure.
