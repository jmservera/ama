# Plan: issue 953 slice 2

* Phase 1: add `test_client_reset_during_post_body_read_logs_warning_not_error` (raw socket, Content-Length larger than sent body, RST via SO_LINGER 0) in `src/api/tests/test_error_logging.py`.
* Phase 2: run focused tests, ruff, mypy; log entry; PR with `Refs #953`.
* Critique (single pass, self): scope is test-only, no conflicts with confirmed decisions. Verdict: proceed.
