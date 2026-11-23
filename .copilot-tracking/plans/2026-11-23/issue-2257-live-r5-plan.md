# Issue 2257 r5 plan

1. Add `driver_sqlstate` to `src/core/src/zava_forward/core/mssqlstore.py`.
2. Append `sqlstate=<code>` to the overlay warning in `assistants.py`.
3. Add a regression test in `src/api/tests/test_map_sensors.py`.
4. Run targeted tests, mypy and ruff; add the research note, README index entry and log entry.
