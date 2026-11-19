# Issue 111 live research (2026-11-19)

Opening note. Question: is the only unticked criterion ("Research phases R1 to R3 are complete before a derived measure is used beyond an exercise rule") provable or buildable for the demo?

## Findings

* Only criterion 3 is unticked; criteria 1 and 2 are already ticked.
* Code gate exists: `AnalysisPolicy.validate` in `src/core/src/zava_forward/core/sensor_analysis.py` rejects a `SOURCED:` threshold without a `ResearchGate` (`RESEARCH_GATE_REQUIRED`), and the default policy has no approval, so no SENSOR_REVIEW_DUE candidate is produced. Test: `src/core/tests/test_sensor_analysis.py:251`.
* Run 2026-11-19: `PYTHONPATH=src:tests python3 -m unittest tests.test_sensor_analysis -q` in `src/core`: 18 tests OK (1 expected failure).
* Completion of R1 to R3 needs a competent building-physics reviewer and Asset sign-off on the R2 method and agreed R3 false-alert and miss limits (`docs/reference/research/iot-sensor-analytics-research-plan.md`, Phases table). That is a human act; the plan records R1 to R3 open. A code attestation would only record a sign-off that does not exist.
* Planning Readiness: Ready for a no-source-change disposition. Live Azure not touched.
