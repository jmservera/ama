# Changes: issue 230 design-system class check

Files: design-system.md, test_design_system.py, log.md, and these artifacts.

Run (venv in /tmp, pip): unittest test_design_system, test_programme_screen, test_role_screens_conformance, test_content_standard (43 tests, pass); ruff check on the changed test; mypy --cache-dir=/tmp/mypy-230 on the changed test.

Not run: rpi-checks gate (coordinator runs it), browser/axe, full suites, benchmarks. `ruff format --check` reports pre-existing drift elsewhere in test_design_system.py; left untouched, new lines are formatted.

Divergences: none. Build directories from pip install were removed.
