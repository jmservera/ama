# Changes: issue 229 data steward and operator screen (2026-11-01)

* Added: `data-operator` screen in `src/api/src/zava_forward/api/web/role-screens.js` (read-only, MANAGER roles, reuses issue 226 helpers).
* Added: `src/api/tests/test_data_operator_screen.py`.
* Divergence: none. No server, role or endpoint change; integration run state shown as Unknown because no source exists.
* Validation: unittest (data operator, asset board, role screens, accessibility baseline, design system, workspace scripts) pass; ruff check and format pass; mypy reports no errors in touched files (remaining errors are pre-existing missing optional stubs/playwright). `test_static_assets` needs a different test path and was not run.
