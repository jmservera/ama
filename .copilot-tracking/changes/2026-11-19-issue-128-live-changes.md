# Issue 128 live changes, 2026-11-19

No source or documentation change outside `.copilot-tracking/`. Tier FOCUSED; rpi-checks.py not run.

| Criterion | Status | Evidence |
| --- | --- | --- |
| Accessibility testing includes keyboard and screen reader | Deferred (ticked, #1907, owner decision 2026-11-18) | Person-run assistive-technology testing not needed for the demo |
| Missing data and incomplete appointments get human review | Proven earlier (ticked) | Prior runs, unchanged |
| Direct user research protocol agreed | Unproven | Equity test plan agreement record has no named person or date; needs a human |
| Usability measures aggregate only | Proven at source level | `cd src/core && PYTHONPATH=src:tests python3 -m unittest test_usability_programme test_journey_register`: 27 tests OK, 2026-11-19 |

The single remaining criterion needs a named human agreement, so nothing can be built or proven for the demo. Unticked criteria: 1 (protocol agreed).
