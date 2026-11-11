# Details: #134 extension E3

* Owned paths when admitted: src/api/checks/connected_home_browser_check.py, src/api/tests/test_connected_home_check.py, new dated ext3 tracking. No product, role, auth, helper API or README change.
* Selectors: tests.test_connected_home_check (existing ten plus the new negatives); python -m checks.connected_home_browser_check once.
* Capture: a fresh directory /tmp/z134/e3-<UTC timestamp>; each command writes name.out, name.err, name.exit by direct redirection with noclobber; refuse to start if the directory or any file exists; never reuse a basename; record the exit of the command itself. Failed attempts keep their own new names; no renaming or overwriting.
* Browser identity from browser.version as in E2. Axe not run.
* Preconditions, no execution now: private venv /tmp/z134/venv, cached Chromium, lock /tmp/ama-rpi-heavy.lock non-queued (flock -n -E99), timeout 900. Missing dependency: pip into the owned venv only.
* Remaining: R1 unresolved; classification rests on the source anchors in the research; Evidence boundary and Journey stages are id-only and not scanned.
