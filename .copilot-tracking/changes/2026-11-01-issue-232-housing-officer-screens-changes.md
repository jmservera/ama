# Changes: issue 232 housing officer and resident engagement screens (2026-11-01)

* Added: `resident-choice` read-only role screen appended to `src/api/src/zava_forward/api/web/role-screens.js` for resident-view roles.
* Added: `src/api/tests/test_resident_choice_screen.py` (3 node-vm tests).
* Validation: new, asset_board, role_screens, design_system, accessibility_baseline tests pass (role_screens need the core/agents PYTHONPATH per the api guide); ruff check, ruff format --check and mypy on touched files clean.
* Divergence: none. Browser and axe keyboard checks not run locally; CI is the evidence.
