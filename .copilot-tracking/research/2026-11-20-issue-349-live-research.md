# Issue 349 research, 2026-11-20 (task issue-349-live)

Research disposition: reused. Planning Readiness: Ready.

Evidence: docs/reference/research/issue-349-tenant-prerequisites-live-r4-2026-11-19.md (live, 2026-11-19).
Criteria 1-3 need tenant-owner Graph rights (denied); 4 needs an owner roster (not demo); 6 proven r4.
Buildable gap in criterion 5: `/app` for a validly shaped Entra principal with no mapped role or a wrong
tenant returns the 403 "Account not authorised" page (server.py ~909); existing tests cover only an
"invalid" principal there. Wrong-role denial at HTML level is untested.
Decision: add a unit test in src/api/tests/test_auth.py; no live Azure action needed.
