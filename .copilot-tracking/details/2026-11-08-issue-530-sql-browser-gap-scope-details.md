---
title: Issue 530 actual SQL and employee browser gap scope details
ms.date: 2026-11-08
---

## Phase 2: employee chat browser wiring

* Constants in `tools/rpi-checks.py`: `EMPLOYEE_CHAT_BROWSER_MODULE = "checks.employee_chat_browser_check"`, `EMPLOYEE_CHAT_STATES = ("actual-model-unavailable", "synthetic-cited-answer", "demo-disclaimer-model-answer")`, `EMPLOYEE_CHAT_PASS = "PASS employee chat: "`.
* Plan (`required_checks` browser group) and `Runner.browser()`: add `employee_chat_browser_check` to the lint tuple; after the case-journey command and its results copy, run `python -c BROWSER_ENTRY checks.employee_chat_browser_check --axe <output>/axe-4.10.3.min.js --out <output>/employee-chat` in `src/api` with `PYTHONPATH=<output>/safety:` plus `test_paths("api", True)`, timeout 900, not a suite. At execution, copy `employee-chat/axe-results.json` to `employee-chat-results.json` and validate it before continuing. Existing browser commands, order and the other 16 groups are untouched.
* Verifier: `verify_commands` requires the chat command row (identity from the plan) and `EMPLOYEE_CHAT_PASS` in its log and no `skipped` in the log; `required_files` for `browser` adds `employee-chat-results.json`; `verify_results` calls one shared `check_employee_chat_results(path)`: JSON list, exactly the three states in order, each `violations == []`, integer `passes > 0`, no `skipped` text. The same helper validates at execution time. Fails closed on any missing, extra or reordered state.
* Regressions in `tools/test_rpi_checks.py`: the browser contract contains exactly one chat command after case-journey with exact argv/cwd/env/timeout; `Runner.browser()` dispatches the same sequence (fixture runner, patched `command`, patched download and copy); receipt mutations (missing row, wrong module, wrong paths, missing file, wrong or reordered states, violations, zero passes, missing PASS line, `skipped` text) are rejected; the scoped receipt fixture gains the chat file and PASS log.

## Phase 3: actual MSSQL chat coverage

New classes in `src/api/tests/test_mssqlstore.py`, all gated by `unittest.skipUnless(ON, "needs a SQL Server (ZF_TEST_MSSQL=1)")` (an existing allowed skip reason), no method docstrings (verbose output names must stay `method (module.Class.method)`), using existing `wipe()`/`factory()`:

* `MssqlChatPrivacy(chatprivacy.ChatPrivacyBehaviour, TestCase)`: reuses the #160 privacy mixin (DPO/legal/notice refs refusal, redaction, special-category memory rejection, rights through the repository, retention purge) on `MssqlStore`.
* `MssqlChatRoleProjection(TestCase)`: store seeded from `role_matrix_fixture.build()` (staff of every role, seeded `REASON`/`PHONE`). Tests: each staff role's prompt for `ZF-1` excludes `PHONE`, includes `REASON` exactly for `projection.DEFAULT_REASON_ROLES`; stale-roster revocation (role to Contractor/Unknown, disabled, inactive, deleted) written by an independent autocommit connection denies before dispatch with zero model calls and an `access-rejected` audit receipt without the question text; permitted demotion during inference withholds the answer; another user cannot resume a thread (`ChatNotFound`) and lists none. Roster writes use an overridable `write_staff` through a separate `_Conn`, not `sqlite3`.
* `MssqlChatDemoMeter(assistants.MssqlFixture, continuity.ChatDemoMeterOnSqlStore)`: the four existing chat financial-meter behaviours (admits exactly one call; second call in the same request held; refused without the demo switch; synthetic price still holds a live call) on actual SQL Server `assistant_events`. Overrides only the order-dependent seed test with an order-independent equivalent (sorted kinds, synthetic flags, authority `max_calls == 1`, calls budget `CHAT_DEMO_METER.CALLS`). SQLite originals stay unchanged.
* Selection: unchanged `SQL_SELECTORS` (whole `test_mssqlstore` module). Runner scope: `SQL_CHAT_REQUIRED_TESTS` lists every new method header; the SQL suite command is verified at execution and in `verify_commands` to show each as `... ok`, and a regression asserts every required test's module/class is covered by a `SQL_SELECTORS` entry and exists as a method in the tracked file.
* LIGHT proofs available now: import and skip behaviour without `ZF_TEST_MSSQL`, `ruff`, `mypy` on tools, runner unit suite, and a scratch SQLite stand-in for privacy and roster classes labelled a proxy only.

## Admission of the future gate (NOT ADMITTED)

Fresh Main re-pin, all 17 groups, `--all --jobs 1 --lock-timeout 0`, canonical lock actually free, attached bounded run, new external output, receipt verified on current Main, independent exact-head review, hosted CI. Actual MSSQL methods and the employee chat browser step must be `ok` in that receipt. Live, human and approval exclusions stay unmet.
