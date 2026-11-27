# Issue 2164 changes (2026-11-27)

Tier: focused (test-only; no src behaviour change; no workflow/dependency edits).

Changes
* `src/api/tests/test_assistants.py`: added `test_bound_view_only_entra_principal_is_denied`.
* `docs/reference/research/issue-2164-bound-entra-scope-2026-11-27.md`, README index entry, log entry.

Validation: 20 targeted tests OK; mutation check (view_only guard disabled) fails the new test, source restored; mypy (src/api) and ruff check pass. Hosted CI not observed (no push).

| Criterion | Status |
| --- | --- |
| Decide bound Entra staff inherit roster case_ids/areas | Proven (implemented in #2274, tests pass) |
| Test view_only with eligible role | Proven (new bound test; mutation-checked) |
| Test scope bypass | Proven (existing forged-pointer and scope tests pass) |
| Live Azure proof | Unprovable and unneeded: pure authorization rule |
