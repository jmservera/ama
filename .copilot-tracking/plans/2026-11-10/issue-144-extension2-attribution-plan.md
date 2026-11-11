---
title: Issue 144 extension 2 result-attribution plan
description: Plan to bind permitted result attribution to the stored reservation root
ms.date: 2026-11-10
task_id: issue-144-extension2-attribution
---

## Objective

In `Assistants.complete_result`, for a permitted attempt, bind `meter_id` and `meter_root` to the server-stored reservation, reject conflicting caller values, and pass the bound envelope to `complete`.

## Phases

* [ ] Phase 1: source change in `assistants.py` (`complete_result` and a small root lookup helper).
* [ ] Phase 2: regressions in `src/api/tests/test_ai_consumption_api.py`.
* [ ] Phase 3: validation (targeted tests, lint, type, optional SQL), changes record, review, commit.

## Phase 1 detail

* Read the reservation record for `marker["meter_id"]` through the existing consumption reader; use its `root`.
* Reject with `result-rejected` (`reason` `conflicting-attribution`) when `envelope.meter_root` is present and differs; reject with `reason` `permitted-reservation-missing` when the record is absent.
* Copy the envelope, set both fields, call `_settle_meter` and `complete` with the copy. No catch-all, no fallback.

## Phase 2 detail

* Valid output with root omitted: state ready, one output record on the reserved root, task envelope has the root; a later accept review records financial review on it.
* Conflicting root and conflicting `meter_id`: `False`, `result-rejected`, no completed record, no output record, task still leased and unsettled.
* Failed and no-output result with omitted root: settles the meter, no output attribution published (unchanged semantics).
* Existing marker settlement test unchanged.

## Phase 3 detail

* Selectors: api `test_ai_consumption_api`, `test_assistants`, `test_assistants_dispatch`, `test_ai_tasks`, `test_ai_boundary`, `test_assistant_release`, `test_ai_call_site_inventory`, `test_ai_transport_deadline`, `test_quality_sensors_e2`, `test_quality_simulation_lane`; core `test_ai_consumption*`, `test_ai_dispatch_marker`, `test_ai_input_bounds`; agents `test_dispatch`; real sensor fixture tests `test_quality_sensors_e1`, `test_quality_sensors_e2`, `test_quality_sensors_c7` if they run on owned local fixtures.
* ruff check and format check per project config; mypy core strict and the api test file.
* Real SQL lock-crossing selectors only if existing prerequisites are already available and the heavy lock is free non-queued; otherwise recorded blocked.
* Causal RED: new tests fail on the frozen source (log) and pass fixed.

## Constraints

No B scope, no new feature or ticket, no network, provider or credentials, no full gate, no push or GitHub write.
