# Details: issue 1288 live pass (2026-11-21)

* Phase 1 commands: from src/api with the guide PYTHONPATH, python3 -m unittest on tests.test_quality_sensor_grounding, tests.test_quality_sensors_correlation, tests.test_quality_sensors_c7, tests.test_quality_sensors_e1, tests.test_quality_sensors_e2, tests.test_quality_sensors.
* Phase 2: az containerapp job and revision list (read-only); Playwright script .copilot-tracking/evidence/2026-11-21/issue-1288-live6/live_probe.py reads credentials at run time and scrubs email addresses; no POST to the assistants.
* Phase 3: research note in docs/reference/research, README index line, log entry.
* Out of scope: recording a release, starting or changing simulator runs, source edits.
