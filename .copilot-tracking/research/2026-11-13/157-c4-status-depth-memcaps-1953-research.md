# Research: 157 C4 status depth and memory caps (1953)

Disposition: executed (reused prior proof 157-c4-post1547-proof-1921). Planning Readiness: Ready.

Findings:
* `chat_panel.role_limits` and `server.py` `/api/chat/status` (line ~1054) hold the limits literals; widget note in `web/chat.js` line 53 omits `calls_per_request`.
* Memory caps live in `chat_privacy.MEMORY_LIMIT` (50) and `MEMORY_MAX` (1000); chat `_ask` does not build memory into prompts.
* Tests: `src/api/tests/test_chat_panel.py` (`test_status_reports_role_limits_and_bounds`, `test_receipt_reports_usage_and_thread_limit_falls_back`).
Scope: report-only fields plus tests; no behaviour change.
