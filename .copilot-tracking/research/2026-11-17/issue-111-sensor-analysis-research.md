---
title: Issue 111 sensor analysis research (measure)
ms.date: 2026-11-17
---

## Status

Disposition: executed (measure). Planning Readiness: Ready. Base eb51af5c9, branch docs/sensor-analysis-111, tier FOCUSED.

## Measured state

* `sensor_analysis.py` and `sensor_analysis_store.py` exist on the base; PR 1780 (parent-topic merge) is not an ancestor of this base, so its claims are not measured here.
* From `src/core` with `PYTHONPATH=$PWD/src:$PWD/tests` (the editable installs point at the main checkout, so the path is required to test the worktree): `python3 -m unittest tests.test_sensor_analysis tests.test_sensor_analysis_store tests.test_epic165_deterministic_reproducibility tests.test_sensor_handover tests.test_sensor_review_draft` ran 101 tests, OK, 22 skipped (SQL Server opt-in tests). Without `tests` on the path, `test_sensor_analysis_store` fails to import `sensor_consumer_fixture`; that is a harness path need, not a defect.
* Reproducible: identical rows give equal signals; digest is order independent and changes with data. Missing, stale, declined and unknown consent give INSUFFICIENT/STALE/DECLINED with priority_effect NONE. No candidate without an approved rule. Duplicate rows reject the series to INSUFFICIENT (fail safe).
* Staleness boundary: exactly 48 h is SUFFICIENT, 48 h plus 1 s is STALE.

## Reproduced gap (not fixed)

Policy identity does not bind the threshold. `AnalysisPolicy(humidity_threshold_pct=40.0)` keeps `version == "sensor-analysis-exercise-v1"`; the `Signal` records `policy_version` and `threshold_label` but no threshold or staleness limit. Measured on the `normal` scenario: default policy gives NO_EXERCISE_SIGNAL, 40.0 gives REVIEW_CANDIDATE, both with the same `policy_version` and digest. A `RuleApproval` for that version therefore approves any threshold, and a retained signal cannot be reproduced from its recorded version. Repair needs a change in `sensor_analysis.py` (bind thresholds to the version or record them), which is beyond the docs/test scope. Stop-and-report applies.

## Criteria

* C1 reproducible: supported for the exercise slice by the measurements above; the version/threshold gap qualifies it.
* C2 labelled exercise values: holds (label required by `validate`).
* C3 R1 to R3: unproven; needs the named human approver. No change.
