---
title: Sensor mean-step boundary correction phase details
description: Bounded execution details for PR 587, Refs #188
ms.date: 2026-10-30
---

## Metadata

* Task ID: 188-pr587-mean-step-boundary
* Slug: sensor-mean-step-boundary-188
* Plan: `.copilot-tracking/plans/2026-10-30/sensor-mean-step-boundary-188-plan.md`
* Research: `.copilot-tracking/research/2026-10-30/sensor-mean-step-boundary-188-research.md`

## Phase Index

| Phase | Intent | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Correct and validate exact boundary | Complete | P01-T01, P01-T02 |
| P02 | Review and commit local candidate | Complete in local evidence commit | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Correct and validate inclusive comparison

Context: C1-C4 demonstrate recurring means reject exact 0.10; admitted inputs
are small, fixed-point decimal values. Preserve all report keys and unaffected
statistics. No API or SQL schema changes.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Add failing regression and exact comparison

Use `rows()` from the existing handover test module, select one home and a
contiguous six-slot window. Handover at the fourth slot produces exactly three
prefix and three suffix samples. Use baseline 10.00 with suffix first value
9.99; derive observations using Decimal arithmetic and two-decimal strings.
Parametrize both channels, signed shifts and `0.09/0.10/0.11`. A second
prefix-count variant with two prefix samples and the same three suffix values
proves count scaling. Apply a common 0.02 offset for that variant to exercise
prefix-reference subtraction; the required three-prefix variant has no offset.
Keep point and stddev tolerances at 1.0 and mean_step at 0.1 on the target
channel; keep the other channel unchanged with default zero tolerance.
Inspect check/result and reported error. Capture original failure before
editing production.

Production target:
`src/core/src/zava_forward/core/synthetic/sensor_consistency.py`.
Retain existing means/stddev for reports. Compute reference-adjusted sums,
cross-multiply by opposite side counts, compare before division, and divide
that numerator for the report metric. Update `src/core/README.md` to describe
comparison before dividing rather than imply all Decimal means are exact.

Test owner: `src/core/tests/test_sensor_handover.py`; one new method maximum,
no removals, no packaged tests, no generated targets.
Completion: observed red-to-green regression and surgical diff.
Unresolved items: none.

Completion evidence: new method originally failed in four exact-positive
boundary subcases and passed after the correction. Formula uses explicitly
seeded Decimal sums for strict type inference.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validate requested core surface

Dependency: P01-T01. Missing installed core was demonstrated in Research.
Create the venv under external session files, install editable core with pip
and pinned dev extra. Run from `src/core`; use absolute environment binaries.
Acquire `flock -w 600 /tmp/ama-rpi-heavy.lock` for install and test/type/lint
commands, retaining output externally. Use unittest discovery suite construction
to combine `test_sensor_*.py` with `test_resident_sensors.py` in one runner.
Full-core `ruff check .`, `ruff format --check .`, and `mypy` follow.
Completion: exit codes, exact commands and test count recorded in changes.
No uv, Azure calls, private fixture reads, silent skips or fabricated receipt.

<!-- rpi:phase id=P02 -->
## P02: Review and persist local candidate

<!-- rpi:task id=P02-T01 -->
### P02-T01: Independent Review and local commit

Dependency: P01 validation and markers/details/changes reconciliation.
Activate the canonical review skill once. Independent reviewer receives
research/plan/details/critique/changes pointers plus exact source diff,
acceptance criteria, authority boundaries and validation logs. Preserve its
original outcome and route residual work; do not repeat Review.
Commit explicit paths only using the authenticated GitHub user's constructed
noreply email for author and committer, Conventional Commit message containing
Refs #188 and the requested trailer. Verify the commit and clean worktree.
Do not push, rewrite/rebase, change PR or assert full publication acceptance.
Full receipt/live/hosted/human evidence is outside focused local proof.

## Current Completion State

P01-T01 and P01-T02 complete. Final sensor run: 142 tests, one existing
dedicated-local-SQL opt-in skip; ruff check passed, format check passed
(115 files), mypy passed (168 files). Original failed mypy result retained
in changes; final check log is external. P02-T01 completed one original
independent Review, Complete / Conformant with no correction defects.
Its local persistence is the commit containing these final artifacts;
publication is not performed. No source changes followed the Review.
RV-001/RV-002 remain distinct coordinator-owned follow-ups.
