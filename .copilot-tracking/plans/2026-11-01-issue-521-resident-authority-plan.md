# Plan: issue 521 resident authority end

1. Replace the browser-check fixture constant with `rs.AUTHORITY_END` (single source).
2. Update `test_resident_demo_check.py` to prove 2027-02-01 applies and 2026-11-01 does not.
3. Add coordinator SQL/redeploy steps to `infra/README.md`.
4. Validate with focused tests, ruff, mypy. No Azure/SQL apply.

Critique (one pass): compatible; keep AI tariff expiry unchanged per "existing owner approvals unchanged". No divergence.
