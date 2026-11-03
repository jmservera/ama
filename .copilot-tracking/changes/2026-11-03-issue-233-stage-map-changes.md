# Changes: issue 233 stage map slice

* `src/api/src/zava_forward/api/web/role-screens.js`: stage map helper and its call in `programme-queue` render.
* `src/api/tests/test_programme_screen.py`: new stage map test.
* `docs/reference/research/ux/atlas-screen-trace.md`: stage map paragraph and limit.
* `docs/reference/log.md`: appended entry.
* Validation run: 58 unit tests (programme screen, conformance, role screens, design system, content standard, accessibility baseline), atlas checker, `node --check`, ruff check and format, mypy. Not run: complete or focused gate (`rpi-checks`), browser or assistive-technology checks, full suites.
* Divergences: none. Packages were not pip-installed; `PYTHONPATH` pointed at `src/*/src` to avoid ignored build files.
