# Changes: issue 231 technical queue and quality screens (2026-11-01)

* Added: `technical-queue` and `quality-queue` read-only role screens in `src/api/src/zava_forward/api/web/role-screens.js`, reusing the #226 helpers.
* Added: `src/api/tests/test_technical_quality_screens.py` (9 node-vm tests).
* Validation: new, role_screens, asset_board, workspace_scripts, design_system, accessibility_baseline tests pass (36); ruff check, ruff format --check, mypy src clean for `src/api`. Run in a throwaway venv with pip.
* Divergence: none from plan. Browser and axe keyboard checks not run locally; CI is the evidence.
