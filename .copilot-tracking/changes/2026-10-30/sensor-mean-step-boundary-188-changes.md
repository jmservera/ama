---
title: Sensor mean-step boundary correction changes
description: Original implementation evidence for PR 587, Refs #188
ms.date: 2026-10-30
---

## Metadata

* Task ID: 188-pr587-mean-step-boundary
* Slug: sensor-mean-step-boundary-188
* Plan: `.copilot-tracking/plans/2026-10-30/sensor-mean-step-boundary-188-plan.md`
* Details: `.copilot-tracking/details/2026-10-30/sensor-mean-step-boundary-188-phase-details.md`
* Date: 2026-10-30

## Execution Status

Complete in the local commit containing this final evidence, full plan scope:
P01, P01-T01, P01-T02, P02 and P02-T01. No remaining active source work.

## Execution Summary

The passing one-time plan critique authorizes the bounded evaluator/test/README
correction. The external regression demonstrated the original failure before
the production correction. Exact comparison and all requested checks passed.
One original independent Review assessed Complete / Conformant with no
correction defects. Commit source/test/docs and original dated evidence locally;
no push. Local commit identity is established by Git history, avoiding a
self-referential commit hash in its own contents.

## Approved Implementation Boundary

Evaluator, existing external handover test module, directly related core README
and this dated RPI artifact set. One added unittest method, no removals, generated
targets, dependency edits, Azure, private data, push or unrelated source changes.

## Completed Work

### P01-T01: Nonconstant-reference red-to-green correction

* Files: `src/core/src/zava_forward/core/synthetic/sensor_consistency.py`,
  `src/core/tests/test_sensor_handover.py`, `src/core/README.md`.
* Replace rounded mean subtraction with absolute cross-multiplied
  reference-adjusted sum numerator; compare inclusively to count-scaled limit
  before dividing solely for reported `mean_step_error`.
* Preserve means/stddev, point/stddev checks, report keys/version and validation.
* One new external unittest method covers 24 subcases: both channels, both
  signs, prefix counts 3/2, suffix count 3, and 0.09/0.10/0.11 shifts.
  Unequal-count cases include common 0.02 offset; required three-prefix example
  has no prefix offset. Generous point/stddev limits isolate the mean-step check.
* Original implementation: one method failed in four exact-positive-boundary
  subcases (both channels and both prefix counts), exit 1.
* Corrected implementation: same method passed all subcases, exit 0.
* External logs under session
  `451e3ac2-96a7-4da9-a4ad-5f807e8aad8a/files/`:
  `mean-step-red.log`, `mean-step-green.log`.

### P02-T01: Original Review and local evidence persistence

One independent assessor wrote
`.copilot-tracking/reviews/logs/2026-10-30/sensor-mean-step-boundary-188-review.md`.
Execution Complete; original outcome Conformant for bounded correction.
No correction defects; exact formula additionally matched its 24-case Fraction
oracle. Original RV-001 [Low] publication and RV-002 [Low] live-evidence work
are distinct coordinator follow-ups, not new active implementation.
No source/test edits or repeated Review after that assessment.

The final local commit includes the source/test/README correction and all seven
dated artifacts. Authenticated account `jmservera`, id `8036360`, was resolved
with `gh api user`; repository-local noreply author/committer email is
constructed from these returned fields. Commit message uses Refs #188 and
the requested Copilot Co-authored-by trailer. No push, PR mutation, rebase,
deployment, secrets or live datasets.

## Implementation-Time Plan and Detail Updates

### P01-T02: Typed Decimal sums

First full-core run completed 142 sensor tests with one existing opt-in local
SQL privacy test skipped, passed ruff and format checks, but mypy reported
two errors: unseeded `sum` inferred an `object` numerator. Add explicit
`Decimal(0)` sum starts to preserve the Decimal type without casts or ignores.
This is a local implementation correction, not a material plan divergence;
original critique remains Pass and is not repeated.

## Validation Record

Default Python package import failed during Research. Installed editable
`src/core[dev]` with pip into external session `files/core-venv`, exit 0;
`core-install.log` retained. Python 3.12.3, configured ruff 0.17.1/mypy 2.4.0.
Install and red/green commands ran under
`flock -w 600 /tmp/ama-rpi-heavy.lock`.
First full run: 142 tests, 17.213s, one existing opt-in SQL skip; ruff passed,
115 files formatted; mypy failed with two type errors. Original
`core-validation.log` retained. Final rerun follows the typed-sum correction.
Skipped test: `src/core/tests/test_sensor_privacy.py:376`, requires
`ZF_SENSOR112_MSSQL=1` and dedicated local SQL. No opt-in SQL activation or
full/live SQL proof is claimed.

### Final requested local validation

From `src/core`, all commands held
`flock -w 600 /tmp/ama-rpi-heavy.lock`:

| Check | Scope | Result |
| --- | --- | --- |
| unittest combined discovery | `test_sensor_*.py` and `test_resident_sensors.py` | 142 tests, 17.474s, 141 passed, one existing opt-in local SQL skip |
| `ruff check .` | Complete core | Passed |
| `ruff format --check .` | Complete configured core | Passed, 115 files already formatted |
| `mypy` | Complete configured core | Passed, 168 files |

Exit 0. External `files/core-validation-final.log` retained along with the
original failed run and red/green logs. No cloud/paid inference/private data.
No complete publication gate receipt was produced; source/base/commit changes
invalidate historical receipts and publication remains unauthorized.

## Pre-Review Reconciliation

At Review entry, P01 markers and details matched completed source/test/docs
and final validation. P02-T01 remains explicitly pending independent original
Review and local persistence; it is not misrepresented as implemented source work.
Blockers, remaining work, handoff and follow-up lists agree.

After the original Review, parent reconciled the final completed plan/details,
changes and state for local persistence. The Review artifact is preserved;
P02 completion is established by the commit containing these artifacts.
Historical Review statements about pending parent commit remain its original
assessed temporal boundary, not unperformed source work.

## Blockers

No implementation blocker. Complete publication receipt and actual live
sensor/Hub/Azure SQL evidence are not proven or authorized by this correction.

## Remaining Work

No remaining active correction work. Complete-gate receipt, hosted/human approval
and live evidence remain unproven follow-up boundaries.

## Follow-Up Items

Coordinator-owned full publication gate, hosted/human approval and separately
authorized live evidence remain outside correction acceptance.

Rank 1: RV-001, coordinator-owned full exact-candidate publication gate and
hosted/human prerequisites; focused checks cannot establish publication readiness.
Rank 2: RV-002, separately authorized live Hub/Azure SQL handover evidence after
prerequisites; this cannot be inferred from synthetic/local tests.

## Return-to-Caller State

Full bounded correction complete and locally persisted. Original critique
Pass; original Review Complete / Conformant. Validation proves the nonconstant
inclusive-boundary regression, signed/unequal-window comparisons and requested
configured core checks. One pre-existing dedicated-local-SQL opt-in skip
disclosed. Automatic session remains running at Follow-up, with no child
selection or unauthorized continuation. Do not push.
