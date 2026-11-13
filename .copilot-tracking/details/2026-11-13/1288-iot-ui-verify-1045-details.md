# Details: 1288-iot-ui-verify-1045

## Phase 1

* `git -C ../demo-sensor-ui-readiness-0620 show dc1404abb:<path>` into the same relative paths; compare sha256 of source blob output and the copies.

## Phase 2

* `python3 -m venv /tmp/venv-1288-1045`; `pip install --no-deps -e src/core -e src/agents -e src/api`. If unittest needs third-party deps (not installable under --no-deps), record as a blocker rather than adding network-less workarounds; permit only dependencies declared in the pyproject if import fails, and record that deviation.
* Import check prints `__file__` for zava_forward.core, .agents, .api.

## Phase 3

* Core: from src/core, `python -m unittest -v tests.test_device_identity tests.test_live_readings tests.test_sensor_consumer_live` (or discover with pattern); API: from src/api with `PYTHONPATH=../core/tests:../agents/tests`, six modules. Capture status via redirect to a file and `$?`.
* Count tests, skips (grep "skipped"), report them separately.

## Phase 4

* Write changes file with outputs, then `rm -rf /tmp/venv-1288-1045`.
