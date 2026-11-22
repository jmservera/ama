---
title: Issue 2192 live details (round 2)
date: 2026-11-21
---

* `sensor_consent.py`: add `homes(row)` returning the unique ordered tuple of `sensor_home_id` and `case_id`; add `apply(port, primary, extra, granted)`: set primary (errors propagate), then set each extra, ignoring `ValueError` (UNKNOWN_HOME), propagating other errors.
* `app.py` POST route: call `sc.apply(app.sensor_consent, row.sensor_home_id, row.case_id, granted)`.
* Test: extend `test_resident_sensor_consent.py` with a fake port that raises `ValueError` for unknown homes; assert calls for `ZF-1` and the case id `C-1`, and that a port without the case home still returns 200.
