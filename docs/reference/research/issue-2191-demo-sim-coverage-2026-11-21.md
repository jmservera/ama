---
title: Issue 2191 demo simulator coverage and intermittent readings
description: Code and local-test evidence that the live demo simulator can cover at least half of all homes with a configurable skip rate and the consent mix kept, and what could not be proven without live Azure
author: AMA RPI agent
ms.date: 2026-11-21
ms.topic: reference
keywords:
  - issue 2191
  - simulator
  - sensor coverage
estimated_reading_time: 4
---

Refs #2191, #184, #165. Synthetic desktop demo. The brief forbade touching live Azure, so this note covers repository code and local tests only; no job, device identity or secret was changed.

## What changed

* `tools/demo_consent_mix.py` gains `select`/`select_cohort`: at least half of all homes, sorted, evenly spread and repeatable. `plan` now alternates granted and declined consent, so 341 homes give a 171 home cohort within one home of an even split.
* The cohort ceiling moves from 100 to 500 homes in `live_control.MAX_COHORT`, the receiver binding limit in `iot_stream`, the planner, the admin help text and the README. `check_capacity` still limits a start by the daily quota (1,250 homes at 5 minutes) and the 10 messages per second pace.
* `live_simulator` gains a seeded per home per slot skip decision: `--failure-rate` or `ZF_SIM_FAILURE_RATE`, 0 to 0.9, default 0 (no behaviour change). A skipped device sends nothing; the summary counts `skipped` and code `DEVICE_SKIPPED`, not `failed`. An invalid value refuses with `SIM_CONFIG_INVALID`.

## Test evidence

* `python3 -m unittest tests.test_live_control tests.test_live_simulator tests.test_simulator_admin tests.test_iot_stream tests.test_live_receiver_sql tests.test_accessibility_baseline tests.test_content_standard` from `src/api`: 229 tests, OK (2 skipped).
* `python3 -m unittest tools/test_demo_consent_mix.py`: 5 tests, OK.
* Ruff check and format on changed files clean; `mypy` shows only the 7 existing `opentelemetry` import errors, identical without these changes.

## Acceptance criteria

| Criterion | Status | Evidence |
| --- | --- | --- |
| Cohort covers at least 50% of homes | Code proven; live not proven | `select_cohort` test with 341 homes; the live store, device identities and job secrets were not touched |
| Configurable intermittent-failure rate | Proven locally | `IntermittentFailureTests`; live jobs need `ZF_SIM_FAILURE_RATE` set |
| Consent mix preserved | Proven locally | `plan` test: granted and declined differ by at most one |
| Unit tests | Proven | Counts above |

## Limits

* Live coverage needs one X.509 device identity per added home. The current jobs mount two Container Apps secrets per device, which will not scale to hundreds of homes, so provisioning for the larger cohort needs a different certificate mechanism. This is the main open item.
* The receiver binding and cohort ceilings changed; they need independent review before live use.
* Hosted CI and the full local gate were not run here.
