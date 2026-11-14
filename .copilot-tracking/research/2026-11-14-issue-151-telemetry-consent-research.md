---
title: Issue 151 telemetry consent research
ms.date: 2026-11-14
---

## Scope

Issue #151: resident-facing telemetry notice and withdrawal. Research disposition: executed (local code inspection).

## Findings

* `sensor_consumer.py` (`_quality`) rejects any reading whose control consent is not `granted` with reason `CONSENT`; `configure` applies control changes atomically and waits for an in-flight dispatch.
* `sensor_view.consent` fails closed: any `declined` control wins, and the view returns `consent-withheld` with no values.
* `SensorConsumer.home_consent` is the read-only trusted state.
* Neither module reads or writes cases, repairs or hazards, so consent state cannot block them.
* Gap: no resident-facing plain-language notice and no single withdrawal entry point with a tested guarantee.

## Planning Readiness

Ready. Assumption: notice wording is a proposal needing resident-engagement and legal review; not evidence of approved text.

## Cycle 2: mypy errors in the consent test (PR #1729)

* `python3 -m mypy` in `src/core` reported 5 errors in `tests/test_telemetry_consent.py`: bare `dict` at line 22 (`type-arg`) and `object` attribute access at lines 39, 46 and 52 (`attr-defined`).
* Cause: `process` was annotated `-> object` with a bare `dict` parameter; the real return type is `Receipt` in `zava_forward.core.sensor_consumer`.
* Research disposition: executed (local mypy output and source read). Planning Readiness: Ready.
