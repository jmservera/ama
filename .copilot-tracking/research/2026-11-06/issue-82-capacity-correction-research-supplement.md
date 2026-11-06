# Issue 82 capacity-at-booking correction research supplement

Date: 2026-11-06 (UTC), before any corrective test or source edit. Base `8cae59ec8`, parent81 `d4d33c7ec`, main `bb3a3b03c`. Refs #82. Originals (r1 research, plan, details, changes, review) stay unchanged.

## Findings reproduced by reading source at 8cae

* RV-001: `require_booked_capacity` (procurement.py) raises a plain `ValueError("A single evidenced work order with a confirmed appointment is required...")` when no single active APPOINTED order exists. The r1 plan listed this as Unknown, so it exposes no `GateResult`. Missing or unbooked order evidence is absent evidence, so Unknown and still refusing.
* Message matching: `require_appointment_commitment` (appointments.py) decides whether to rethrow `CapacityGateError` with `result["missing"] == [str(capacity_error)]`. This compares exception text, against the explicit no-message-matching requirement. `_appointment_assessment` already knows structurally how many missing items exist when the capacity handler appends, so the typed error can be returned only when it is the sole missing item. Equality is currently redundant; no runtime defect is asserted, this is a discriminator correction.

## Boundaries

* Keep the exact ValueError text and class (`CapacityGateError` subclasses `ValueError`), check order, authority, resident, context and rollback behavior, and the `appointment_status` public shape.
* Out of scope: eligibility, finance, other authority families, API or persistence of the Pass (RV-002), real MSSQL execution (RV-003, pending FULL), named rule review. `CAPACITY_RULE` stays an unreviewed exercise rule.

## Tier

Implementation tier FULL (server authority and capacity over SQL persistence), held; this cycle is source plus light checks only. #188 owns heavy admission.
