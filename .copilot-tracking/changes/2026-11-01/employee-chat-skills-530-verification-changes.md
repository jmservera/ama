# Changes: employee chat skills local verification (#530)

* Plan: [employee-chat-skills-530-verification-plan.md](../../plans/2026-11-01/employee-chat-skills-530-verification-plan.md)
* Base: `origin/main` cb57c1b7. No source, test or workflow change.

## Added

* Dated RPI artifacts (research, plan, changes, review) and session state under `.copilot-tracking/`.
* Entry in `docs/reference/log.md` recording the local run.

## Evidence (local, 2026-11-01, Python 3.12.3, pip venv)

| Check | Result |
| --- | --- |
| API `unittest discover` (CI invocation) | 1485 tests OK, 323 skipped (mix of backend-inapplicable and env-gated; see notes) |
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

## Evidence limits (review correction)

* Tested tree: branch `feat/employee-agent-chat-skills` on base `origin/main` cb57c1b7, working directory `src/api` for the API discover (CI invocation of `mvp-ci.yml`), `src/agents` and `src/core` for the others. Core chat tests ran from `src/core` and the API `test_chat_panel` from `src/api`, so the two same-named modules were run separately in their own directories.
* Totals are as printed by `unittest`; per-run exit statuses, a separate skipped-versus-passed breakdown and durable sanitized output were not captured. Treat the counts as indicative, not independently reproducible, until the follow-up gate below re-runs them with captured output.
* Skips are of two kinds: backend-inapplicable (for example `JsonProgressApi` skips a SQL-specific test and `MssqlHazardReferral` skips the JSON-only audit-ordering test) and environment-gated (browser and SQL prerequisites, `ZF_BROWSER_TESTS`, `ZF_TEST_MSSQL`). The 323 API skips were not split between the two.

## Follow-up (publication gate)

* Run `python3 tools/rpi-checks.py --all --base <reviewed-main-sha> --out <new-external-directory>` on the committed candidate and verify with `--verify-receipt` against current `origin/main` before merge. Not yet done; recorded in the review as an open gate.

## Not established

* Live employee-site verification (#612 attestation denied, zero employee sign-ins).
* Screen-reader and voice-control acceptance; owner confirmation of agent names.
* Hosted CI result for this branch.
