# Changes: issue 531 briefing loading and provenance

* `src/api/src/zava_forward/api/web/app.js`: section `aria-busy`, new loading/refresh status text, provenance `dl`, per-statement basis line.
* `src/api/src/zava_forward/api/web/style.css`: `.briefing-status` min-height, `.briefing-provenance` layout.
* `src/api/tests/test_briefing_loading_provenance.py`: four focused source-level tests.
* Validation: mypy, `ruff check .`, `ruff format --check .` pass. 50 listed unittests pass except `test_connected_home_check` discovery test, which fails identically on the base because the shell `PYTHONPATH` needed for imports leaks `core/tests`. Browser render not run.
