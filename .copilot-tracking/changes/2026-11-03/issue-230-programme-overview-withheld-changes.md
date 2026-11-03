# Changes: issue 230 programme overview withheld panel

Files changed: role-screens.js, test_programme_screen.py, test_role_screens_conformance.py, atlas-screen-trace.md, log.md, and these artifacts.

Validation run (venv in /tmp, pip install of src/core, agents, api):

* `unittest tests.test_programme_screen tests.test_role_screens_conformance tests.test_role_screens tests.test_design_system tests.test_content_standard tests.test_accessibility_baseline`: pass.
* `ruff check tests src`, `ruff format --check` on changed tests, `mypy --cache-dir=/tmp/mypy-230` on changed tests: pass.

Not run: rpi-checks gate (coordinator runs gates), browser/axe check (playwright not installed), full suites, benchmarks. test_browser_asset_urls cannot import here (no playwright); unrelated.

Divergences: none. Pip build directories created by the install were removed so ignored files are empty.
