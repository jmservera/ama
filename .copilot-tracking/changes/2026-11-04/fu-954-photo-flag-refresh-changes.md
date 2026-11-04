# Changes: issue 954

* Modified `src/api/src/zava_forward/api/web/app.js`: photo availability re-check and 503/403 handling.
* Added `src/api/tests/test_photo_availability.py`.
* Modified `docs/reference/log.md`: appended entry.

## Validation (focused tier)

* Run: `tests.test_photo_availability`, `tests.test_workspace_scripts`, `tests.test_content_standard` (20 tests OK); `node --check app.js`; `ruff check`/`ruff format --check` on the new test; `mypy --cache-dir=/tmp/mypy-952 src` in `src/api` (clean). New test confirmed failing against the old `app.js`.
* Not run: real-browser check, axe, full suites, gate, benchmarks. No pyproject.toml edited.
* Not performed: fetch of web-design-guidelines source and full guideline review.

## Divergences

None.
