# Plan: issue 228 supplier, contractor and procurement screens (2026-11-01)

1. Append `procurementPackagesScreen` and `contractorJobPackScreen` registrations to `role-screens.js` (manager roles; `Contractor`).
2. Add node-vm tests `src/api/tests/test_procurement_screens.py`: package fields, offered versus committed, call-off ref, work-order ref, readiness draft with unmet prerequisites and next reviewer, contractor view has no reason or manager fields, submission separate from review, no button, form, input, select or textarea, role lists, Unknown handling.
3. Validate: unittest for new, role_screens, asset_board, design_system, accessibility_baseline tests; ruff check, ruff format --check, mypy for `src/api`.
4. Commit, push, PR (Refs #228 unless every criterion proven).

Critique (single pass, self): keep read-only; never state readiness as ready (draft only); evidence checklist items default to "Not supplied" because nothing records them; do not add submit buttons without a server authority; reviewer must differ from contractor and is named from package or work-order issuer else "Unassigned". Accepted. Rejected: adding POST endpoints (deferred in PRD, needs OD-47).
