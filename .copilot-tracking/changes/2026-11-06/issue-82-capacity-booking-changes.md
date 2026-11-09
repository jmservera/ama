# Issue 82 capacity-at-booking changes

Date: 2026-11-06 (UTC). Branch `feat/remaining-gate-family-readiness-82`, base `d688866b2`, target parent `feat/controlled-lifecycle-integration-81` at `d4d33c7ec`. Main `bb3a3b03c` is separate. Refs #82.

## Prospective order

1. Research, plan and details supplements written first (`*-capacity-booking-*-supplement.md`). The d688 originals are byte-identical (sha256 e9f169a4, 00283261, 46d237f7 verified after the edits).
2. Three shared `Flows` tests added; RED captured: 6 errors on JsonFlows and SqlFlows, exit 1 (`/tmp/ama82-cap-red.log`).
3. Source implemented; GREEN.

## Source changes (src/ only)

* `gates.py`: `CAPACITY_RULE` (PRD FR-008/FR-016, date 2026-11-06, version 1, reviewer "Unreviewed exercise rule"), `capacity_gate(state, reason)` giving Pass, Fail or Unknown, and `CapacityGateError(ValueError)` carrying `.state` and `.result`.
* `procurement.py`: `_evidenced_capacity` raises `CapacityGateError` with the unchanged text. Unknown (None): missing or legacy evidence, unreadable details, hash, scope, contract or home mismatch, invalid accepting manager, authority changed. Fail (False): work date outside the period, deficit against existing orders. `require_booked_capacity` now returns the Pass `GateResult` after the unchanged check order (commitment, capacity, resident clearance).
* `appointments.py`: `appointment_status` body moved to `_appointment_assessment`, which also returns the capacity error. The public `appointment_status` shape is unchanged. `require_appointment_commitment` re-raises as `CapacityGateError` only when the sole missing item is the capacity error; the text and `ValueError` type are identical. Mixed or other failures remain plain `ValueError`.

Discriminators are typed (`isinstance`, `.state`); there is no message matching and no blanket catch. A narrow try surrounds only `_capacity_details`.

## Tests

`test_quality_procurement.py` (shared Flows, inherited by Json, Sql and MssqlProcurement): pass with unreviewed provenance, known violation gives Fail, unreadable evidence gives Unknown. Each refusal asserts no case, procurement or audit change after reopening.

## Deviations and disclosures

* The "single evidenced work order" ValueError stays a plain `ValueError`, not Unknown as the plan supplement listed. Left unchanged to avoid altering an existing contract.
* The Pass result is returned to the caller only. It is not persisted: no event, schema or API change.
* A direct authority-revocation test was not added (SQL staff mutation is complex). Existing authority tests ran in the selection and passed.
* Ruff E501 and format findings in the first attempt were fixed in the new code.

## Light evidence (real exits)

* Targeted: `unittest -k booking_capacity JsonFlows SqlFlows` exit 0, 6 tests OK.
* `test_gates test_quality_procurement test_consultation_controls`: exit 0, 193 tests, OK (skipped=16). Skips are not SQL Server evidence.
* `ruff check --no-cache .` 0; `ruff format --no-cache --check .` 0; `mypy` 266 files, 0.
* Import path asserted with `PYTHONPATH=<worktree>/src/core/src`, bytecode off, external caches.

## Not done

FULL gate (SQL Server MssqlProcurement execution) HELD BY #185. No push or publication.
