# Details: issue #350 slice 1 (2026-11-04)

Plan: ../plans/2026-11-04-issue-350-anon-api-401-plan.md

## Phase 1: browser-style anonymous test

* File: `src/api/tests/test_auth.py`, class with the trusted-proxy HTTP server (next to `test_no_principal_is_401_and_password_login_is_gone`).
* Asserts 401 for `/api/me`, `/api/cases`, `/api/account/photo` with a Chrome User-Agent, `Accept: application/json`, `Sec-Fetch-Mode: cors`, `X-Requested-With: fetch`.
* Asserts 401 with a malformed `X-MS-CLIENT-PRINCIPAL` and for a CSRF-marked POST to `/api/logout`.
* Asserts `/app` with a browser HTML request still returns 302 to `/sign-in`.
* Success: test passes; ruff and mypy clean.
