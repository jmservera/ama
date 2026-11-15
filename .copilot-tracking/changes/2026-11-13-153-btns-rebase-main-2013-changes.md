# Changes: 153-btns-rebase-main-2013

* Rebased `fix/demo-153-app-js-notices-1836` onto `2489d839e9`: `5fd741093`, `c5467845a`, `925fb97fe` (were `4b88545e3`, `91bc7f3e4`, `9fff29a3c`). No conflicts with #1542.
* `git diff 2489d839e9..HEAD -- src/`: `app.js` (+35/-9 lines touched) and `tests/test_app_js_notices_content.py` (+142) only; safetyPanel changes intact.
* Validation (all passed): api 88 tests (notices content, safety panel ux, content standard, accessibility baseline, design system, case journey); core test_cutover_audit and test_scenario_manifest 17 tests; ruff check clean; ruff format 155 files formatted; mypy 239 files clean.
* Venv `/tmp/venv-153rb-2013` removed. Not pushed. Branch needs a force-with-lease push by the owner later.
