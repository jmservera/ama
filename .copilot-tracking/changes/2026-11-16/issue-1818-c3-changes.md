# Issue 1818 c3 changes

* `src/api/checks/design_system_browser_check.py`: marker status-name check uses an anchored regex `^Pat Test, <label>(\. .+)?$` so the status name stays required and the sensor suffix added in c5e5eefb1 is allowed.
* `src/api/checks/map_fullscreen_browser_check.py`: `check_browser_shortcuts` waits for the map to stop loading and the network to go idle before observing requests; a redraw left by earlier steps was counted as a shortcut request (found locally, deterministic).

Validation (PYTHONPATH set to worktree sources, since the installed package resolves to the main checkout): design-system check fails before and passes after; map_fullscreen check passes with `--axe /tmp/axe1818/package/axe.min.js`; unittest 21 OK; mypy clean; `ruff check checks tests/test_map_sensors.py` clean; CI isolated ruff and format on design_system check clean. Pre-existing isolated-ruff findings in map_fullscreen check are outside CI's listed scope and untouched.
