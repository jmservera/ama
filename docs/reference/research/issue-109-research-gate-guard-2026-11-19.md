---
title: Issue 109 first unmet criterion, R1 to R3 research gate guard
description: Per-criterion proven or unproven table for epic 109 and the code guard added for the #111 R1 to R3 criterion
ms.date: 2026-11-19
ms.topic: reference
---

Refs #109, #111. Synthetic demo, desktop only. No live Azure write was needed or made; the criterion is a code guard proven by local tests.

## Result

| Criterion | Result | Evidence or reason |
| --- | --- | --- |
| #109 #440 stabilization checkpoint | Unproven | #440 is open with two unticked criteria (finding triage, review artifacts); it is an owner and coordinator process outcome that code cannot satisfy. |
| #109 all child features closed or deferred | Unproven | #111 stays open (R1 to R3), #184 and #1818 open on 2026-11-18; no deferral decision is recorded. |
| #109 no sensor signal diagnoses a hazard... | Already ticked | Existing non-authority tests re-run and pass (see below). |
| #111 R1 to R3 complete before a derived measure is used beyond an exercise rule | Partly proven | Code guard: a `SOURCED:` threshold label without a `ResearchGate` (R1 source review, R2 reviewer sign-off, R3 synthetic validation references) now fails with `RESEARCH_GATE_REQUIRED`. R1 to R3 themselves stay open (R2 sign-off and agreed R3 limits are human outcomes), so the criterion is not ticked. |

## Change

`src/core/src/zava_forward/core/sensor_analysis.py`: `ResearchGate`, `AnalysisPolicy.research_gate`, guard in `validate`, gate included in `policy_digest` only when set (existing digests unchanged). Test: `test_sourced_threshold_requires_research_gate` in `src/core/tests/test_sensor_analysis.py`.

## Validation (focused)

* `PYTHONPATH=src:tests python3 -m unittest test_sensor_analysis test_sensor_analysis_reproducibility test_sensor_analysis_store test_sensor_non_authority test_sensor_reproducibility_111 -q` in `src/core`: 49 tests OK (1 expected failure, pre-existing).
* `python3 -m mypy` in `src/core`: 22 errors in 3 files, all pre-existing missing optional stubs (for example `opentelemetry`), none in `sensor_analysis`.
* `ruff format --isolated --line-length 100` applied to the two changed files. `rpi-checks.py --all` not run (coordinator brief).
