---
title: Finite exposure observation guard (issue 99) plan
description: One bounded reproduce-and-fix plan
ms.date: 2026-11-12
---

## Objective

Make `assess` treat a nonfinite numeric observation (positive infinity, negative infinity, NaN) as Unknown, which already pauses for a human decision, so no nonfinite value can yield Within limits / No pause signal.

## Phases

* [x] Phase 0 research and runtime reproduction (see research artifact), reproduced.
* [x] Phase 1 failing-first test `test_nonfinite_observation_is_unknown_not_within` in `src/core/tests/test_exposure_limits.py` (exit 1 before fix).
* [x] Phase 2 guard in `src/core/src/zava_forward/core/exposure_limits.py`: replace the NaN-only check with helper `_finite_observation` (exact int, or exact finite float) for the committed value and each tolerance observation; amended after critique CR-01 to avoid `isfinite` overflow on huge ints. Reuses existing Unknown semantics.
* [x] Phase 3 focused validation: targeted core test module, ruff check and format check, mypy on the two files.

## Out of scope

Board/Finance inputs, tolerance thresholds, new HTTP observations, UI, approval changes, investment decisions, automatic resume or acceleration, whole-issue acceptance, negative finite observations, blanket gates, heavy services.

## Validation tier

Focused (owner demo instruction), classification basis: small core logic fix, no workflow, dependency, deployment, SQL, infrastructure or security-control change. The full local gate and external receipt were not run and are not claimed. Independent exact-head review, human approval and hosted CI remain required before any merge.

## Plan note

The reproduction and the edits were performed before this artifact was written; the artifact records them as done and states that order openly. Details: [details](../../details/2026-11-12/finite-exposure-99-1112-details.md). Critique: [critique](finite-exposure-99-1112-critique.md).
