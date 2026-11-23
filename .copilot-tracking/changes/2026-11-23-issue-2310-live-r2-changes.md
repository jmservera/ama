# Issue 2310 changes, live run 2 (2026-11-23)

Classification: focused tier. Basis: test-only change in `src/api/tests/test_auth.py`; no src, workflow, dependency, infra or UI change. Not run: `rpi-checks.py --all`, `--changed`; hosted CI not observed (nothing pushed). The test was drafted before the implement-start witness call; the witness sequence therefore records the changes record after the edit, a process deviation.

## Files

* src/api/tests/test_auth.py (added `test_anonymous_api_never_redirects_for_any_method_accept_or_unknown_path`)
* docs/reference/research/issue-2310-anon-401-live-2026-11-23.md (second-run addendum)
* docs/reference/log.md (entry)

## Validation

* `python3 -m unittest tests.test_auth` (src/api, documented PYTHONPATH): 42 tests OK, including the new one.
* `tests.test_auth_branch_floor`, `tests.test_entra_authoritative`: 48 tests OK.
* `ruff check tests/test_auth.py`: passed.
* Failing-first: not possible, the server already behaves correctly; no mutation run was performed.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Anonymous protected API GET with browser User-Agent and Accept application/json returns 401, not a redirect | Proven in code and tests; unproven live | Existing #1005 test plus new test (GET, HEAD, POST, three Accept values, cookie). Deployed Easy Auth edge returned 302 in the earlier run; not re-probed, edge change is outside demo authority |
| Anonymous protected page request still redirects to Entra | Proven in tests | New test: /sign-in 302 to /.auth/login/aad; existing test: /app 302 to /sign-in. Live not re-run |
| Existing auth tests pass; no weakening of any route protection | Proven | 42 plus 48 tests OK; test-only diff |
