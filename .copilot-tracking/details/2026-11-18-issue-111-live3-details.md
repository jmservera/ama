# Details: issue 111 live3

* Phase 1: `python3 -m unittest tests.test_sensor_analysis tests.test_sensor_non_authority` in src/core; Playwright walk (credentials read at runtime, never printed) hitting /api/me, /api/cases, /api/cases/{id}/sensors and the sensor draft routes.
* Phase 2: note under docs/reference/research/, raw files in issue-111-live3-raw/, README index and log.md entries.
* Phase 3: no src change, so FOCUSED; no rpi-checks --all. No Azure resource was created, so nothing to delete.
