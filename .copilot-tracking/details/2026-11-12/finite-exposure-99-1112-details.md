---
title: Finite exposure observation guard (issue 99) details
description: Phase details for the bounded candidate
ms.date: 2026-11-12
---

## Phase 1: failing-first test

* File: `src/core/tests/test_exposure_limits.py`, class `ExposureLimits`.
* Cases: for each of -inf, +inf, NaN: bad committed with valid tolerances; bad values for both tolerances with valid committed; all bad. Assert status Unknown, signal `Pause for human decision`, and no finding carries a nonfinite `observed`.
* Synthetic values only.

## Phase 2: guard

* File: `src/core/src/zava_forward/core/exposure_limits.py`, function `assess`, committed and tolerance checks.
* First attempt kept `type(x) not in (int, float)` and added `math.isfinite(x)`; mypy 2.4.0 failed with two `arg-type` errors (`Any | None` to `isfinite`). Reworked to `isinstance` plus `isfinite`, which the critique (CR-01) showed overflows for huge integers. Final: helper `_finite_observation` (exact `int`, or exact `float` that is finite), keeping the original exact-type behaviour so bool stays Unknown. Added test `test_huge_integer_observation_still_breaches`.

## Phase 3: commands (run from `src/core`, venv `/tmp/f99/venv`)

* `python -m unittest tests.test_exposure_limits -v`
* `ruff check` and `ruff format --check` on the two files (pinned ruff 0.17.1)
* `mypy` on the two files (pinned mypy 2.4.0)

Raw outputs: `.copilot-tracking/evidence/2026-11-12/finite-exposure-99-1112/`.
