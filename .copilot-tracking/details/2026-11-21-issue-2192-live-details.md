---
title: Issue 2192 plan
date: 2026-11-21
---

Tier: FULL applies because src code changes; the coordinator runs gates, and this task runs only targeted tests, mypy, ruff and the web baseline tests.

## Phases

1. Core: `SensorConsumer.set_home_consent(home_id, consent, actor)` with audit table `sensor_consent_audit`, and `consent_audit(home_id)`; tests in `src/core/tests/test_telemetry_consent.py`.
2. API: `resident_demo/sensor_consent.py` port, `ResidentDemo.sensor_consent`, view field `sensor_consent`, `POST /demo/sensor-consent`; `__main__` opt-in wiring; tests.
3. Web: checkbox in `renderSensors` with live status; CSS if needed; run accessibility and content tests; Playwright proof.
4. Evidence note under docs/reference/research, index and log entry, changes record with criteria table.

## Critique (once, final candidate)

* Direct T-SQL writes by the resident principal rejected: the guard trigger would drop the marker and consent would fail closed. Accepted: use the consumer seam.
* Resident SELECT-only principal must not be widened. Accepted: separate opt-in connector.
* Withdrawal must not touch repairs or safety duties: reuse `PRESERVED_DUTIES` wording. Accepted.
* Verdict: accepted with no conflicting user decision.
