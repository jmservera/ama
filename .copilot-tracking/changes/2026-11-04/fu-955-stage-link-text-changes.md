# Changes: issue 955

* Modified `src/api/src/zava_forward/api/web/role-screens.js`: stage links carry the stage name.
* Modified `src/api/tests/test_programme_screen.py`: link-text uniqueness test and helper.
* Modified `docs/reference/log.md`: appended entry.

## Validation (focused tier)

* Run: `tests.test_programme_screen` (16 OK); `node --check role-screens.js`; `ruff check` and `ruff format --check` on the test; `mypy --cache-dir=/tmp/mypy-952 src tests/test_programme_screen.py` in `src/api` (clean). New test fails on the previous JS.
* Not run: browser or screen-reader check, axe, web-design-guidelines review, full suites, gate, benchmarks. No pyproject.toml edited.

## Divergences

None.
