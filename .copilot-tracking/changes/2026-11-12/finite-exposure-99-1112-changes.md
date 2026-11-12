---
title: Finite exposure observation guard (issue 99) changes
description: Changes made for the single bounded candidate
ms.date: 2026-11-12
---

## Files changed

* `src/core/src/zava_forward/core/exposure_limits.py`: new `_finite_observation` helper (exact `int`, or exact finite `float`); `assess` uses it for the committed observation and each tolerance observation, replacing the NaN-only check. Nonfinite (+inf, -inf, NaN) now yields the existing Unknown finding and the existing pause signal. Nothing else changed.
* `src/core/tests/test_exposure_limits.py`: `test_nonfinite_observation_is_unknown_not_within` (9 observations) and `test_huge_integer_observation_still_breaches`; `import math`.

## Amendments and divergences

* Amendment A1: first guard (`isinstance` plus `isfinite`) was replaced by the helper after the critique found an `OverflowError` for huge integers (CR-01).
* Divergence D1: reproduction and first edits preceded writing of the plan artifacts; recorded openly in the plan. Plan, critique and Review were each executed once.
* Behaviour change to note: positive infinity previously reported Breach with an infinite observed value; it now reports Unknown. Both pause for a human decision.

* Post-review correction C1: Review finding RV-01 (the test edit had dropped the `LiveSignal` class header) fixed in a second commit; not re-reviewed.

## Validation

Focused tier only; see [exit codes and outputs](../../evidence/2026-11-12/finite-exposure-99-1112/exit-codes.md). Final: unit module 16 tests OK, ruff check and format check 0, mypy 0 on the two files, neighbouring finance tests 78 OK (19 skipped by the runner, not claimed as passes). Not run: full local gate, other core/api/agents suites, hosted CI.

## Limitations

* Negative finite observations (for example committed = -5) still compare as Within; unchanged and a possible separate follow-up, not claimed fixed.
* No live false-all-clear is claimed; the current finance route typically supplies no tolerance observations.
* No whole-issue 99 acceptance claim; `Refs #99` only. Unknown historical correction balances remain unknown; no correction granted.
* Tools: venv outside the repo, pip only, ruff 0.17.1 and mypy 2.4.0 as pinned by `src/core/pyproject.toml`.
