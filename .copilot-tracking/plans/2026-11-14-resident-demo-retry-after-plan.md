# Plan: resident demo bulkhead retry guidance (#1054)

1. app.py: RETRY_AFTER_SECONDS=2, payload `retry_after_seconds`, plain-language BUSY text.
2. demo.js: banner reads `retry_after_seconds` (fallback header, then 2) and states the wait.
3. Test: assert key and text in test_shed_signed_in_view_carries_retry_guidance.
4. Validate from src/api: bare mypy, ruff check/format, resident_demo + accessibility baseline tests (PYTHONPATH pointing at worktree src, as the editable install resolves to another checkout).
Critique: single pass, no conflicts. Tier: focused (small, non-security change).
