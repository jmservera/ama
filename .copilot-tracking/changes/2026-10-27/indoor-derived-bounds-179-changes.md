---
title: Indoor derived bounds implementation evidence
description: Issue 179 changes, checks and acceptance evidence
ms.date: 2026-10-27
---

## Execution and Scope

Task 179 / indoor-derived-bounds-179. Implement P01 and P02 of
.copilot-tracking/plans/2026-10-27/indoor-derived-bounds-179-plan.md.
Research Ready; one critique Complete / Revise, PC-001 directly applied.
Execution: Complete for the full plan. All P01/P02 markers are complete.
Single Review: Complete / Conformant; PR502 published. Earlier checkpoints
and failures below are preserved with their later dispositions.

## Decisions and Boundaries

Shared per-outdoor-record baseline/vapour math, bounded exercise residuals,
physical RH saturation only; version both projection models. No private data,
cloud or whole-stock generation. No heavy gate for this small correction.
Operational/calibration/human approval remains outside this story.

## Validation

Initial uninstalled baseline failed with ModuleNotFoundError. Created an
isolated external session venv and installed core/agents/API editable with pip.
Baseline canonical projection tests: 4 passed.

Combined relevant core check passed: 142 tests, one existing optional SQL skip
(141 executed passes), in 70.926 seconds. This includes ten canonical projection
tests, actual full public history traversal, stock/fault/privacy/provenance,
household/dated effects, historical writer/replay and consumer regressions.
Existing unclosed-file ResourceWarnings were emitted by test_sensor_backfill;
no test failed. API discovery was still running at that checkpoint; final
failure/restoration/retry evidence is recorded below.
Ruff/mypy were absent; installed the project's declared dev extra into the
isolated venv. Initial lint found formatting/import issues in the new code;
the formatting/import corrections are complete. Final changed-file ruff,
format check and strict mypy passed. Final canonical rerun: 10 tests passed
in 5.005 seconds. Dependent resident sensor suite: 9 tests passed.

### Reproduction Commands

Commands use the installed isolated venv's Python (substitute its executable
for `python3`), never a source-package PYTHONPATH:

```bash
cd src/core
PYTHONPATH=tests python3 -m unittest \
  test_indoor_projection test_historical_backfill test_climate_history \
  test_household_conditions test_retrofit_effects test_sensor_backfill \
  test_sensor_stock test_sensor_faults test_sensor_plausibility \
  test_sensor_privacy test_sensor_consumer test_synthetic_provenance -q
python3 -m unittest discover -s tests -p test_resident_sensors.py -q
python3 -m ruff check src/zava_forward/core/synthetic/indoor_projection.py \
  tests/test_indoor_projection.py
python3 -m ruff format --check src/zava_forward/core/synthetic/indoor_projection.py \
  tests/test_indoor_projection.py
python3 -m mypy src/zava_forward/core/synthetic/indoor_projection.py \
  tests/test_indoor_projection.py
cd ../api
PYTHONPATH=../core/tests:../agents/tests python3 -m unittest discover -s tests -q
```

One skipped core test is the existing opt-in own-local-SQL test in
test_sensor_privacy, gated by ZF_SENSOR112_MSSQL=1. It is not a projection
test; no SQL/platform result is inferred. No heavy gate was run: task-specific
authorization allows --changed only for large changes and forbids --all.
Git diff whitespace review and existence checks for all three newly added
relative links passed. Fetched main/base:
0ded682bab690d24eb59b78e704be82d337bf6cd (same as branch starting HEAD).

### Actual Public-Record Measurement

The same nominal replay was independently measured after the test run.
All rows are SYNTHETIC. Values below are sample extrema, not fixed limits;
every row was checked against its own tighter paired-record envelope.

| Dwelling / path | Rows | Actual T C | Derived overall T envelope C | Actual RH % | Derived overall RH envelope % |
| --- | --- | --- | --- | --- | --- |
| apartments / legacy | 17,544 | 15.42..21.40 | 15.2377..21.7150 | 20.83..100 | 17.0588..100 |
| apartments / composed | 17,544 | 14.53..23.01 | 14.2377..23.5159 | 17.55..100 | 13.3382..100 |
| detached / legacy | 17,544 | 14.81..21.40 | 14.4986..21.7150 | 27.54..100 | 23.5380..100 |
| detached / composed | 17,544 | 13.98..23.01 | 13.4986..23.5159 | 19.46..100 | 15.0733..100 |

These are apartments/detached with pre-1919 age and construction loss 1.15,
seed 183, no faults, UTC 2023-01-01 through 2025-01-01 exclusive. Composed
mode uses explicit conditions and a synthetic Cavity wall completion at
2024-01-01 with exercise loss factor 0.85. Old 15%/98% clips would not describe
these envelopes. The supported-domain cold/dry/tail tests additionally prove
nominal temperature below 8 C and RH below 15%, without scientific claims.

## Completed Work

### P01: Shared derived nominal envelope

Both validated entry points now share noiseless baseline/vapour math and
bounded Gaussian residuals, keeping the original two-draw order. v2 manifests
include the noise/tail parameters and per-pair temperature/RH envelope equations.
The physical saturation domain is 0..100%; 8/15/98 no longer bound projections.
No generator caller/schema/ingestion policy or historical snapshot was changed.

The canonical suite retains and amends both v1 reference/fixed-bound methods,
retains invalid-input/fingerprint tests and adds six test methods (ten total),
within the approved maximum twelve additions. Independent v2 reference
equations, RNG state/call order, forced tails/saturation, complete supported
fabric endpoints and composed extrema supplement 17,544 paired public hourly
records times two dwellings times two generator paths = 70,176 nominal rows.
Each history is also regenerated and compared exactly. The public raw and
metadata are hash-pinned; no external retrieval or private inputs.

### P02-T01: Related documentation

Core README documents v2 inputs/equations, exercise assumptions, derived
envelopes, fault/rounding and versioned-byte boundaries. Existing IoT synthesis
has a prospective three-criterion audit without rewriting original adverse
outcomes; index and append-only log updated. Existing empirical calibration,
OD-43, parent/live PRD and human approval limits remain explicit.

## Amendments and Divergences

None. PC-001 adds explicit composed numeric and RNG-call/state tests within
the approved test budget; it changes no scope or user decision.

## Completion and Review Handoff

### Initial Pre-Review Checkpoint (Historical)

Model, tests and documentation are complete, with core and static checks
passing. Review-ready engineering boundary: P01 and P02-T01, completed
P02-T02 checks and all #179 criteria. Supplemental API discovery remains
running and P02-T02 stays unchecked until its result is known; publication
P02-T03 stays unchecked. No missing engineering evidence is disguised as a
pass. The single independent Review can inspect the completed source/test/
documentation boundary while the read-only supplemental validation finishes.
No further source edits are planned; no material divergence or user decision.
Historical calibration/OD-43/parent/live PRD work remains outside this story.

### Final Validation and Single Review Disposition

API discovery completed with four failed-test import entries because the
isolated venv lacked the API's declared azure-identity dependency:
1,058 entries, 744 passes, 310 skips, four errors, 830.173 seconds.
Installed the API using pip against its unchanged manifest and reran only
test_resident_aoai, test_resident_aoai_sql, test_resident_assistant_api and
test_resident_demo_api: 67 run, 61 passed, six optional SQL skips, zero errors,
37.650 seconds. The failure is retained, not relabelled as a green full suite.
The reconciled actual API test set totals 805 passes / 316 skips over 1,121
tests after replacing the four failed imports with their 67 real test cases.

Retry command from src/api:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest \
  test_resident_aoai test_resident_aoai_sql \
  test_resident_assistant_api test_resident_demo_api -q
```

Independent Review execution Complete; outcome Conformant at the synthetic
exercise boundary, zero findings, all three #179 criteria supported. Canonical
record: .copilot-tracking/reviews/logs/2026-10-27/indoor-derived-bounds-179-review.md.
No source fix or second Review followed. No significant divergence.
Implementation and local validation are complete (P01/P02-T01/P02-T02).
P02-T03 publication remains; owner merge/hosted checks and future live
calibration/OD-43 are separate. Publication may use Closes #179, Refs #177.

## Publication and Final State

P02-T03 complete. Initial implementation and all original RPI evidence were
committed as 3d24537aab944fad5e1812dd819a87b7d5b27b5b with Conventional Commit
and required Copilot co-author trailer. Local privacy-safe author/committer
email resolved from authenticated gh account, not private/global configuration.
Pushed only feat/indoor-derived-bounds-179, without force; one PR to main:
https://github.com/jmservera/ama/pull/502 (Closes #179, Refs #177).

All P01/P02 tasks complete; manual full requested loop ends at Review,
task completed/session stopped. No additional child work is started. Final
evidence-only bookkeeping records publication; model/test fingerprints in the
Review stay unchanged. No second critique/Review, merge, deployment, full gate,
private-data read or unearned approval. Owner review/merge and hosted checks
are the next action. Future real-use calibration/OD-43 stays a distinct
owner-selected follow-up.
