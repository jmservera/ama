<!-- markdownlint-disable-file -->
# Employee chat local checks: research (2026-11-02)

Task: `employee-chat-local-checks-530`. Branch `feat/employee-chat-skills-530`, base `origin/main` 071e132a. Refs #530.
Research disposition: reused (existing evidence adequate). Planning Readiness: Ready.

## Evidence

* Criteria 1 to 7 of #530 were delivered by PR #541 and later fixes (#743, #752); the 2026-10-31 closure audit left only criterion 8 open.
* Criterion 8 gap named by the audit: local unit, browser and SQL checks were not run locally together; hosted mssql is not local SQL execution.
* Local prerequisites present: Docker, `mcr.microsoft.com/mssql/server:2022-latest` image, Playwright Chromium 1248.
* `test_mssqlstore.MssqlChatThreads` runs the shared `chat_thread` behaviour suite against SQL Server.
* `checks/employee_chat_browser_check.py` is the employee chat browser and pinned axe 4.10.3 check (SHA-256 880970c0...a68bb).
* `checks/chat_widget_browser_check.py` is not wired into `tools/rpi-checks.py` or any workflow.

## Decision

Slice: run the local unit, browser and disposable SQL checks on the current main head and record the result. No product code change.

## Follow-ups

* `chat_widget_browser_check` fails locally at 1280x720 (see changes record); needs its own triage.
