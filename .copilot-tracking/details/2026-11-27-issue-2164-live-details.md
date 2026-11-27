# Issue 2164 phase details (2026-11-27)

Phase 1: in `src/api/tests/test_assistants.py`, after `test_unbound_and_view_only_entra_principals`, add `test_bound_view_only_entra_principal_is_denied`, using `bound_entra(case_ids=["ZF-1"])` and `dict(user, view_only=True)`; assert PermissionError for a case-scoped and a case-less call, while the same row still authorizes the non-view-only principal.
Phase 2: `python3 -m unittest tests.test_assistants -k entra -k view_only` from `src/api`; mypy is unaffected by a test-only edit unless tests are typed (check `python3 -m mypy` config).
