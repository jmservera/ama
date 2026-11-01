# Changes: employee chat skills local verification (#530)

* Plan: [employee-chat-skills-530-verification-plan.md](../../plans/2026-11-01/employee-chat-skills-530-verification-plan.md)
* Base: `origin/main` cb57c1b7. No source, test or workflow change.

## Added

* Dated RPI artifacts (research, plan, changes, review) and session state under `.copilot-tracking/`.
* Entry in `docs/reference/log.md` recording the local run.

## Evidence (local, 2026-11-01, Python 3.12.3, pip venv)

| Check | Result |
| --- | --- |
| API `unittest discover` (CI invocation) | 1485 tests OK, 323 skipped (SQL/browser env gated) |
| Agents `unittest discover` | 123 OK |
| Core `test_chat*` | 99 OK |
| ruff check, ruff format --check (core, agents, api) | pass |
| mypy (core 170, agents 25, api 127 files) | no issues |
| `checks.employee_chat_browser_check` with pinned axe 4.10.3 | PASS |
| `test_chat_panel...live_log` with `ZF_BROWSER_TESTS=1` | OK |
| `checks.employee_acceptance_check` | 3 tests OK |
| SQL: test_mssqlstore, lawstore, assistants Mssql*, resident_aoai_sql, local SQL Server 2022 container | 271 OK, 1 skipped |

## Environment notes

* Installed `msodbcsql18` and `unixodbc` (system packages) for the SQL run.
* Test path order matters: `test_chat_panel` exists in core and api tests.
* The throwaway SQL container was removed; the password was never written to disk.

## Not established

* Live employee-site verification (#612 attestation denied, zero employee sign-ins).
* Screen-reader and voice-control acceptance; owner confirmation of agent names.
* Hosted CI result for this branch.
