<!-- markdownlint-disable-file -->
# Employee chat local checks: changes and evidence (2026-11-02)

Task: `employee-chat-local-checks-530`. Refs #530. Head under test: 071e132a88499c0f3e41917c59f168a9fbf90b9d (origin/main, clean worktree). Plan: [../../plans/2026-11-02/employee-chat-local-checks-530-plan.md](../../plans/2026-11-02/employee-chat-local-checks-530-plan.md).

No product code changed. Only tracking evidence added. Throwaway venv outside the repo; SQL container task-owned, removed after use; data synthetic.

## Results

| Check | Command (from `src/<project>`) | Result |
| --- | --- | --- |
| core chat unit tests | `unittest test_chat_case_answers test_chat_panel test_chat_privacy test_chat_memory test_chatthreads test_chat_dpia_record test_regulatory_chat` | 147 tests OK |
| agents chat unit tests | `unittest test_chat_model test_chat_eval test_regulatory_answers` | 47 tests OK |
| api chat unit tests (role and scope isolation, fixture roles, widget focus, regulatory chat API, AI consumption) | `unittest test_chat_panel test_chat_isolation test_chat_fixture_roles test_chat_widget_focus test_regulatory_chat_api test_ai_consumption_api` | 111 tests OK, 1 skipped |
| SQL chat threads | `ZF_TEST_MSSQL=1 ... unittest test_mssqlstore.MssqlChatThreads` on SQL Server 2022 (image sha256:cf8f0ab2...1718, mssql-python 1.15.0) | 11 tests OK |
| SQL store suite | `unittest test_mssqlstore` same container | 199 tests OK, 1 skipped |
| employee chat browser and axe | `python -m checks.employee_chat_browser_check --axe axe-4.10.3.min.js` (hash matches pin) | PASS: real fallback, six selections, keyboard, focus, live region, reduced motion, reflow, dialog axe, zero violations |
| chat submit browser | `python -m checks.chat_submit_browser_check` | PASS: Enter/Send, 12 combinations |
| chat widget browser | `python -m checks.chat_widget_browser_check` | FAIL (see defect) |

Not run: the other SQL selectors in `tools/rpi-checks.py` (lawstore, assistants, resident AOAI), the complete local gate and live employee-site verification. Screen-reader and voice-control acceptance is not claimed.

## Defect found (not fixed here)

`checks.chat_widget_browser_check` fails deterministically at 1280x720 in the employee panel `reply_scroll` step, mode `sources-older`: after the loading line appears, the focused first "Sources" summary sits 40 px above the top of the log (log 132 px high at default 40vw x 80dvh, scrollTop 5352) and the "About this chat" row is hit at that point, so the focus-obscured assertion fails. The check is not wired into the local gate or any workflow, so main CI does not catch it. Routed to a separate follow-up (small panel log height and focus scroll after the loading line).

## Criterion 8 status

Local unit, browser (employee chat, axe) and SQL (chat threads, store) checks passed. Live verification on the employee site remains separate and unmet (closure audit: no employee sign-ins, attestation denied in #612). Criterion 8 stays unticked, so the PR uses `Refs #530`.
