# Issue 82 capacity-at-booking correction plan supplement

Date: 2026-11-06 (UTC). Refs #82. Follows the correction research supplement.

## Phases

1. Tests first (shared `Flows`, inherited by Json, Sql, MssqlProcurement): capture RED against 8cae.
2. Source: convert the single-order failure to `CapacityGateError(same text, None)`; make the sole-failure decision structural.
3. Light checks, Changes, dedicated Review, local commit.

## Tests

* No order at all: `advance` raises `CapacityGateError`, `result.outcome == UNKNOWN`, message unchanged, no case, procurement or audit change after reopen.
* Order issued but not booked (not APPOINTED): same assertions.
* Existing capacity, authority, resident and consultation tests remain the controls. The existing mixed-failure behavior is unchanged.

## Source

* `procurement.require_booked_capacity`: raise `gates.CapacityGateError(text, None)` instead of `ValueError` at the single-order check; same text, same position.
* `appointments._appointment_assessment`: return the capacity error only when `len(missing) == 1` after the capacity handler (structural), else `None`. `require_appointment_commitment` rethrows structured only when a capacity error is returned; no `str()` comparison.

## Validation (light, real exits)

Targeted shared cases, then `test_gates test_quality_procurement test_consultation_controls`, `ruff check`, `ruff format --check`, mypy from `src/core`. Bytecode off, external caches, import path asserted. FULL later and separate; SQL skips are not SQL Server evidence.

## Critique

Risk: converting the single-order error could change the exception seen by `advance` callers. Mitigated: `CapacityGateError` is a `ValueError` with identical text; existing `assertRaises(ValueError)` tests still pass. No other families touched.
