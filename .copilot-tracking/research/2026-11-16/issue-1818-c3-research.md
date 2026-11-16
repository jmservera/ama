# Issue 1818 c3 research

Disposition: executed. Planning Readiness: Ready.

PR #1826 `src-api` fails `Synthetic design-system browser checks` with `AssertionError: normal marker has a status name`. The assertion is in `src/api/checks/design_system_browser_check.py` (not map_fullscreen_browser_check.py).
Cause: since c5e5eefb1 `withSensor` in `src/api/src/zava_forward/api/web/app.js` (line 2692) appends `. <sensor status and readings>` to the marker accessible name when a home has sensor data. The check still looks for the exact name `Pat Test, <label>`, which no longer matches.
Fix: update the check to require the status name as a prefix of the accessible name, still allowing the sensor suffix. The app behaviour (status and sensor status in the name) is correct and stays.
