# Issue 2310 changes, live run 3 (2026-11-23)

Tier: FULL class for the src change; per gate economy only targeted tests ran locally; rpi-checks not run (coordinator gates). Planned files: src/api/src/zava_forward/api/server.py, src/api/tests/test_auth.py, docs/reference/research/issue-2310-anon-401-live-2026-11-23.md, docs/reference/log.md. (Record written before source edit.)

## Files

* src/api/src/zava_forward/api/server.py (`_unsupported_method`, `do_PUT`, `do_PATCH`, `do_DELETE`)
* src/api/tests/test_auth.py (`test_anonymous_api_put_patch_delete_return_401_not_501`)
* docs/reference/research/issue-2310-anon-401-live-2026-11-23.md, docs/reference/log.md

## Validation

* `tests.test_auth tests.test_auth_branch_floor tests.test_entra_authoritative` (src/api, documented PYTHONPATH): 93 OK.
* Failing-first: new test fails with server.py stashed, passes after.
* `ruff check` clean; bare `mypy` in src/api: no issues. Not run: rpi-checks, hosted CI (nothing pushed), live probe.

## Per-criterion table

| Criterion | Status | Basis |
| --- | --- | --- |
| Anonymous protected API GET with browser UA and Accept application/json returns 401, not a redirect | Proven in code and tests (now also PUT, PATCH, DELETE); unproven live | Live Easy Auth edge returns 302 before the app; edge change is infrastructure outside demo authority |
| Anonymous protected page request still redirects to Entra | Proven in tests; live proven in earlier run | /sign-in 302 to /.auth/login/aad; /app 302 to /sign-in; not re-probed |
| Existing auth tests pass; no weakening of any route protection | Proven | 93 tests OK; change only adds 401 for previously 501 anonymous verbs; signed-in behaviour pinned at 501 |
