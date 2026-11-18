# Issue 1288 sensor grounding, Cycle 2: changes

Branch feat/demo-1288-quality-sensor-grounding-1530 (Refs 1288). Fixes the four findings of the independent Cycle 1 review of c3ab7d4ae. Original artifacts preserved.

* F-1 High: `chat_panel.py` `rules_first` also routes the `sensor` intent, so configured-model case chat answers from `case_facts` with zero model calls.
* F-2 High: `assistants.py` quality-evidence category `sensors` is now `sensor`, matching `sensor.*` fact paths. `_sensor` cites the case stage when no reading is shown, so role-denied replies are cited and `_rules_answer` accepts them.
* F-3 Medium: `chat_case_answers.py` splits `sensor` intent: strong terms (sensor, reading, dew point, mould risk, iot, fault flags) stay first; weak nouns (temperature, humidity, moisture, threshold) sit after `owner`, so owner/blocked/unblock questions keep their intent.
* F-4 Low: `chat_panel.py` `SENSOR_RULE_PATHS` and `chat.js` `RULE_PARTS` classify sensor.watch/thresholds/health/freshness/not_retained as decision-rule; raw readings stay case-record.
* Tests: `test_quality_sensor_grounding.py` adds a `ChatPanel.ask` test with a mock model (general and quality-evidence lenses, role-denied) and an intent-routing test.

Validation: core test_chat_panel and test_chat_case_answers 64 OK, ruff, mypy clean. api quality_sensor_grounding, content_standard, design_system, accessibility_baseline, dependency_rule 66 OK, ruff, mypy clean. Not pushed.

CI fix (PR #1696, `mssql` job): `test_assistants.MssqlContractTests.test_exact_source_role_matrix_and_no_cross_audience_leaks` compared snapshot source keys to registry categories; the `sensors` to `sensor` category rename leaves the stored source key `sensors`. The test now maps `sensor` to `sensors`. Local: ruff check and mypy clean in core, agents, api; test_assistants has 18 pre-existing local failures identical to baseline (the SQL contract test needs the CI SQL Server). Hosted `mssql` re-run not observed. Not pushed.
