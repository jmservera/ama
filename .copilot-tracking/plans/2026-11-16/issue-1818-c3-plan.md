# Issue 1818 c3 plan

1. In `design_system_browser_check.py`, match the marker accessible name with an anchored regex `^Pat Test, <label>(\. .+)?$` so the status name is required and the sensor suffix is allowed.
2. Run the map browser check, unit tests, mypy and ruff; run the design-system check too. Commit locally; no push.
