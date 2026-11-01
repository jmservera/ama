# Changes: employee chat skills re-verification (#530)

* Plan: [plan](../../plans/2026-11-01/employee-chat-skills-530-reverify-plan.md)
* Base: `origin/main` efebfc6d. No source, test or workflow change.

## Added

* Dated RPI artifacts and session state; a log entry in `docs/reference/log.md`.

## Evidence (local, 2026-11-01, pip venv)

| Check | Result |
| --- | --- |
| Core `test_chat*.py` (from `src/core`) | 99 OK |
| Agents `test_chat_model.py` (PYTHONPATH core tests) | 7 OK |
| API `test_chat_panel` (from `src/api`) | 41 OK, 1 skipped |
| API `test_chat_widget_focus` with `ZF_BROWSER_TESTS=1` | 6 OK |
| ruff check, ruff format --check (core, agents, api) | pass |
| mypy src (core 91, agents 10, api 21 files) | no issues |
| `checks.employee_chat_browser_check`, axe 4.10.3 (SHA matches pin) | PASS |

Not run: SQL contract tests, full API discover, live employee site, screen reader, voice control. Counts are indicative; no durable raw output kept.
