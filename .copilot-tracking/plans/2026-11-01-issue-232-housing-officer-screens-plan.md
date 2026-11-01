# Plan: issue 232 housing officer and resident engagement screens (2026-11-01)

1. Append `resident-choice` screen registration to `role-screens.js` (render only, reads case fields already in the view).
2. Add node-vm tests `src/api/tests/test_resident_choice_screen.py`: roles, measure/version specific choice, linked commitment with purpose/owner/safe route, pause or withdrawn distinct from access, no controls, unknowns.
3. Validate: unittest new test plus existing asset_board, role_screens, design_system, accessibility_baseline tests; ruff check, ruff format --check, mypy src/api.
4. Commit (Conventional Commit, trailer), push, PR to main (Refs #232 unless all criteria proven).

Critique (single pass, self): keep read-only and role-limited; show Not recorded rather than inferring a choice; never derive consent from contact or access; show safe route reference as supplied reference only. Accepted. Rejected: adding recording forms (duplicates case workspace; conflicts with no-contact criterion).
