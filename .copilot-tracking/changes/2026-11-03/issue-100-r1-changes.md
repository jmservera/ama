# Changes: issue 100 r1 AI usage and alerts panel

Files changed: role-screens.js, test_asset_board_screen.py, atlas-screen-trace.md, log.md and these artifacts.

Validation run (venv in /tmp with pip install of src/core, agents, api):

* `unittest tests.test_asset_board_screen tests.test_role_screens tests.test_role_screens_conformance tests.test_design_system tests.test_content_standard tests.test_accessibility_baseline`: 55 pass.
* `ruff check`, `ruff format --check` and `mypy --cache-dir=/tmp/mypy-100` on the changed test: pass.

Not run: rpi-checks gate (coordinator runs gates), browser/axe check, full suites, benchmarks, live Azure evidence.

Divergences: none. Pip build directories were removed so ignored files are empty.
