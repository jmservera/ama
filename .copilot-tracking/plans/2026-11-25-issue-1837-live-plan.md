# Issue 1837 plan, 2026-11-25

* Phase 1: add `test_correction_and_challenge_writes_refuse_unsafe_requests_and_write_nothing` to `src/api/tests/test_nomination_api_routes.py` (unauthenticated 401, contractor 403, array body 400, native urlencoded 400, trusted-proxy without CSRF header 403, stale version rejected; stored case unchanged).
* Phase 2: run the file and neighbouring API tests, ruff and mypy.
* Tier: focused (test-only). The changes record carries the per-criterion table.
