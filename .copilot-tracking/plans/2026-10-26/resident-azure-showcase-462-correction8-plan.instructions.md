# Plan: correction 8 (#462), 2026-10-26
1. Invert the public predicate: refuse any G/W grant to public except documented defaults (class 0 CONNECT and two VIEW ANY COLUMN ... KEY DEFINITION; class 1 in sys/INFORMATION_SCHEMA). Extend real-SQL tests (IMPERSONATE, ALTER ANY USER, CONTROL on schema, VIEW DEFINITION on user, EXECUTE), throwaway container under the heavy lock, removed afterwards.
2. app.py: reuse a valid CSRF cookie token instead of rotating; two-tab regression test.
3. Run tests, mypy strict, ruff; one commit; reply on threads. Critique is self-recorded in the review file (no independent critique; disclosed).
