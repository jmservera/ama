# Research: sensor simulation validation (issue 190), 2026-11-01

* Task: issue-190-sensor-validation; Research disposition: reused (executed light re-read).
* Evidence (main at 80673b0d): PRs #505, #588 merged; `src/core/src/zava_forward/core/synthetic/sensor_scenarios.py`, `src/core/tests/test_sensor_scenarios.py`, `test_sensor_plausibility.py`, `test_sensor_stage_validation.py`; docs in `src/core/README.md`.
* GitHub state: #191, #192, #194 closed; #193 open with one unmet criterion ("Scenarios are used by #133 and #111 tests"); #111 and #133 open with no consumer code; #184 open.
* Parent criteria: per-check reporting is met (ticked). "All child stories closed or deferred" is unmet: #193 open and owner deferral absent.
* Gap deliverable now: a consumer-contract test showing the retrofit profiles (improvement, no change, delayed, adverse) can be classified from observations only, with labelled exercise tolerances, so #111/#133 tests can reuse the fixture. This does not implement #111/#133.
* Constraints: tests outside package, no mvp/prototype code, pip only, synthetic only, no secrets.
* Planning Readiness: Ready.
