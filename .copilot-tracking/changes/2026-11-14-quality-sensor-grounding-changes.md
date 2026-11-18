# Changes: retained sensor values and Quality AI flag grounding (Refs #1288)

Date: 2026-11-14.

* `core/sensor_view.py`: `NOT_RETAINED`, `reading_text`, `grounding`; view adds `grounding`.
* `core/assistants.py`: `review_flag` readings add `citation`, `observed_at`, `temperature_c`, `humidity_pct`, `text`; adds `origin`, `origin_text`, `not_retained`.
* `core/chat_case_answers.py`: `sensor` intent, `sensor_facts`, `_sensor` answer citing `[sensor:...]`.
* `core/chat_isolation.py`: optional `sensors` provider merged into `case_facts`; `api/server.py` wires `Assistants.sensors`.
* `web/ops.js`, `web/assistants.js`: grounding line, flag values and origin line.
* `api/tests/test_quality_sensor_grounding.py`: 4 behaviour tests plus a web-source check.

Validation (PYTHONPATH to worktree sources because the editable install points at the main checkout): new tests, `test_connected_home_check`, `test_role_screens_conformance`, `test_accessibility_baseline`, chat, quality-sensor and sensor suites ran 653 tests, all pass except one that failed only from the ad hoc PYTHONPATH order and passes (14 OK) when run with tests first. `ruff check .`, `ruff format --check .` and `mypy` pass in `src/api`. Not run: full suites, browser harness, hosted CI, full gate (focused tier).
