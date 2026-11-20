# Changes: issue 349 (2026-11-20)

Added `test_valid_entra_principal_without_staff_role_or_in_wrong_tenant_is_denied` to
`src/api/tests/test_auth.py`: a validly shaped Entra principal with no role, an unmapped role or a wrong tenant
gets `/api/me` 401 and `/app` 403 with the sign-out link. No src change. The witness `implement-start` was
refused once (changes path missing from state), then accepted after the state was fixed; the test edit
predated the accepted call (witness qualification recorded).

Validation (FOCUSED): `unittest test_auth` 42 tests OK. `mypy` in src/api: 7 pre-existing errors, all in
src/core/tests/telemetry_support.py (opentelemetry stub missing in this environment), none in the changed file.
ruff format is not applicable (infra Python only). No live Azure action; r4 live evidence (2026-11-19) reused.

| # | Criterion | Status |
| --- | --- | --- |
| 1 | Tenant app, roles, credential | Unproven: needs tenant-owner Graph rights (denied) |
| 2 | Credential via private vault | Proven for demo (r4: vault reference, public access disabled) |
| 3 | Audience and callback, priors preserved | Partly proven; prior callbacks unreadable |
| 4 | Private staff roster reconciled | Unproven, not applicable to demo (no roster) |
| 5 | Real-user sign-in, logout, wrong-role denial | Proven for test account (r4); wrong-role/unassigned denial now proven by unit test; real second-role account unavailable |
| 6 | Anonymous 401, forged-header denial, positive request | Proven (r4) |
