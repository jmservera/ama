# Research: issue 2310 anonymous API 401 tests (2026-11-25)

Disposition: executed. Planning Readiness: Ready.

Canonical findings: [docs/reference/research/2026-11-25-issue-2310-anonymous-api-401-proof.md](../../docs/reference/research/2026-11-25-issue-2310-anonymous-api-401-proof.md).

* The tests the issue asks for already exist in src/api/tests/test_auth.py (commit d29535aca0).
* test_auth: 45 tests pass locally.
* Live demo app redirects anonymous API requests to Entra at the platform layer (RedirectToLoginPage); unchanged by policy.
* Decision: no source or test change; document evidence only.
