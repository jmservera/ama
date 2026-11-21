---
title: Issue 2191 live changes (2026-11-21)
ms.date: 2026-11-21
---

Tier: FULL (src changes); `rpi-checks.py --all` not run, coordinator owns gates. Hosted CI not observed.

## Changed files

* `src/api/src/zava_forward/api/live_control.py`, `iot_stream.py`, `live_receiver.py` (docstring): cohort and receiver binding ceiling 100 to 500.
* `src/api/src/zava_forward/api/live_simulator.py`: seeded `failure_rate`, `Summary.skipped`, `--failure-rate`, `ZF_SIM_FAILURE_RATE`.
* `src/api/src/zava_forward/api/web/simulator-control.js`: help text "1 to 500 homes" (copy only; accessibility baseline and content standard tests pass; web-design-guidelines fetched and no rule touched by the one-word change).
* `tools/demo_consent_mix.py`: `select_cohort`, `select` mode, alternating consent split.
* Tests: `test_live_control.py`, `test_live_simulator.py`, `test_simulator_admin.py`, `tools/test_demo_consent_mix.py`; `src/api/README.md`; research note, index and log.

## Validation

229 api tests OK (2 skipped) across the touched modules plus accessibility and content tests; 5 tool tests OK; ruff clean on changed files; mypy only the 7 existing opentelemetry import errors. The full api discover run was stopped after more than 17 minutes; targeted tests ran instead.

## Criterion table

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least 50% of homes | Code proven, live unproven | `select_cohort` test; live Azure not touched, device identities and job secrets for the extra homes do not exist |
| Configurable intermittent-failure rate | Proven locally | `IntermittentFailureTests`; live job env not set |
| Consent mix preserved | Proven locally | `plan` alternation test |
| Unit tests | Proven | counts above |
| Refs #184 #165 | Referenced only | no closing keyword |
