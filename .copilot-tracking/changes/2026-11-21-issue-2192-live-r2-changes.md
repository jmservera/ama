---
title: Issue 2192 changes (round 2)
date: 2026-11-21
---

Tier FULL (src change); targeted checks only, the coordinator runs the gate. Classification basis: `src/api` behaviour change touching a consent control.

## Files

* `src/api/src/zava_forward/api/resident_demo/sensor_consent.py`: `apply` sets the sensor home then the case-id home.
* `src/api/src/zava_forward/api/resident_demo/app.py`: route uses `sc.apply`.
* `src/api/tests/test_resident_sensor_consent.py`: new test, fake port raises `ValueError` for unknown homes.
* Evidence: `docs/reference/research/issue-2192-live-r2-2026-11-21.md` and folder, index and log entries, round 2 RPI artifacts.

## Validation

* `tests.test_resident_sensor_consent tests.test_resident_demo_api tests.test_accessibility_baseline tests.test_content_standard`: 103 tests OK. ruff check and format pass; `python3 -m mypy` in `src/api` clean.
* Hosted CI not observed; no push. Live Azure was read, and the test resident consent toggled and restored; no resource changed.

## Criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Plain-language consent text | Proven | `test_content_standard`; live page text |
| Native checkbox, keyboard, WCAG baseline | Proven (engineering checks and live desktop Playwright); person-run AT not needed | `test_accessibility_baseline`, `live_probe.json` |
| Withdrawal takes effect, employee view shows withheld | Proven locally; live employee effect unproven (defect found and fixed locally, not deployed; registry is network-locked) | research note |
| Audit entry | Proven locally; Azure SQL rows not read | core test |
| Tests | Proven | validation above |
