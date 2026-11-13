# Review: 891 chat grounding core (independent code-review agent, once)

Execution: executed. Outcome: one Medium finding, fixed in this task; no other high-confidence bugs.

* Medium: `unblock` intent placed first and too broad (hijacked funding, owner, status questions). Fixed: placed after `funding`, narrowed to explicit unblock, fix-the-blocker, fix-safety and "should we schedule/book/arrange" phrasing; test added for owner and status questions.
* Confirmed correct: receipt meter fields, fallback scope (abstain or UNGROUNDED only, case_id set, skill-scoped), attribution reset on settlement downgrade, no banned words.

Post-fix validation: unittest chat_case_answers 8, chat_panel 53, ai_consumption 34, chat_memory 21, chat_privacy 29 OK; ruff check, ruff format --check, mypy src clean; git diff --check 0.
Follow-up: wire the agents model caller to populate ModelUnavailable meter_root (outside this write surface).
