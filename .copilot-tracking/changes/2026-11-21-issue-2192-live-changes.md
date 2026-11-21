---
title: Issue 2192 changes
date: 2026-11-21
---

Tier FULL (src change). Targeted checks only; the coordinator runs the gate.

## Files

* `src/core/src/zava_forward/core/sensor_consumer.py`: `set_home_consent`, `consent_audit`, table `sensor_consent_audit`.
* `src/api/src/zava_forward/api/resident_demo/sensor_consent.py` (new), `app.py`, `__main__.py`, `web/demo.js`: port, route `POST /demo/sensor-consent`, native checkbox.
* Tests: `src/core/tests/test_telemetry_consent.py`, `src/api/tests/test_resident_sensor_consent.py`, fixture and view-key updates.
* Evidence: `docs/reference/research/issue-2192-live-2026-11-21.md` plus folder, index and log entries.

## Validation run

* core `test_telemetry_consent`, `test_sensor_consumer`: pass. API `test_resident_sensor_consent`, `test_resident_demo_api`, `test_accessibility_baseline`, `test_content_standard`: pass. ruff check and format pass; mypy shows only the pre-existing missing opentelemetry stubs in core and none in changed files.
* Web guidelines (fetched 2026-11-21) review of `demo.js` changes: label wraps native checkbox, `role="status"` live region, no outline changes, ellipsis character used, no motion added.
* Playwright desktop proof recorded in the research note.

## Criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Plain-language consent text per content standard | Proven | `test_content_standard` passes; text reuses the issue 151 notice |
| Native checkbox semantics, keyboard, WCAG baseline | Proven for engineering checks and Playwright keyboard toggle; no person-run AT test (not needed for demo) | `test_accessibility_baseline`, note |
| Withdrawal takes effect and employee view shows withheld state | Proven locally (SQLite, real consumer and `sensor_view`); not proven on live Azure | employee JSON files |
| Audit entry | Proven locally | `sensor_consent_audit` rows, core test |
| Tests | Proven | new core and API tests |
| Live ca-resident-demo / ca-cutover-test-demo-api walkthrough | Unproven: needs image build, new SQL principal and config change on the live app | research note limits |
