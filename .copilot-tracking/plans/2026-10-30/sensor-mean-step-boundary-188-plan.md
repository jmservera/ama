---
title: Sensor mean-step boundary correction plan
description: Implementation-ready candidate for PR 587, Refs #188
ms.date: 2026-10-30
---

## Task Metadata

* Task ID: 188-pr587-mean-step-boundary
* Task slug: sensor-mean-step-boundary-188
* Date: 2026-10-30
* Planning status: Complete; one independent critique Pass and one original Review Conformant
* Details: `.copilot-tracking/details/2026-10-30/sensor-mean-step-boundary-188-phase-details.md`
* Critique: `.copilot-tracking/reviews/plans/2026-10-30/sensor-mean-step-boundary-188-plan-critique.md`

## Executive Summary

Remove recurring-mean rounding from the inclusive mean-step decision by
cross-multiplying reference-adjusted side sums before comparing the limit.
Keep the same JSON report, means and standard deviations. Add one external
regression method covering nonconstant references, both channels and signs,
equal and unequal windows, and below/equal/above-limit results.

### What You May Not Know

Current constant-reference boundary tests cannot reproduce this bug. The
reported mean-step error should be divided from the same numerator used by the
check, not reconstructed from independently rounded means. Focused local
checks prove this correction, not actual sensor accuracy, live transport,
whole #188 acceptance or publication readiness.

### Unresolved Decisions or Blockers

None for the correction. Default Python cannot import core; an isolated pip
environment is required. Full publication validation remains a later boundary.

## User Decisions and Requirements

* Run Research, Plan, Implement and Review in order with dated tracking artifacts.
* Correct PR #587 on existing `feat/sensor-ingestion-consistency-188`, based on
  `18602ae7`, using cross-multiplied sums before division.
* Cover prefix `10.00,10.00,10.00`, reference suffix `9.99,10.00,10.00`,
  observed suffix shifted by `0.10`, inclusive `mean_step=0.1`.
* Keep tests outside the package; use pip, src only, no Azure or secrets.
* Run sensor tests and ruff check/format check/mypy from `src/core`; heavy
  commands hold `/tmp/ama-rpi-heavy.lock` with a 600-second wait.
* Commit locally with the required Copilot trailer. Do not push. Refs #188 only.

## Goals

* Eliminate false rejection at the exact inclusive mean-step threshold.
* Preserve explicit rejection above the limit and independent channel checks.
* Produce inspectable local validation and one independent original Review.

## Scope and Non-Goals

In scope: evaluator arithmetic, existing external handover test module,
directly related core README and dated RPI evidence. No test removals, new
production module, dependency change, generated output or unrelated cleanup.
No remote mutation, live datasets, Azure access, deployment or issue closure.

## Functional Requirements

* Compute numerator
  `abs((actual_after_sum-reference_after_sum)*before_count -
  (actual_before_sum-reference_before_sum)*after_count)`.
* Compare numerator inclusively with
  `Decimal(str(tolerance.mean_step))*before_count*after_count`.
* Divide numerator by the count product only for reported `mean_step_error`.
* Preserve report version/keys and point/stddev semantics.

## Non-Functional Requirements

* Keep existing Decimal fixed-point representation, no epsilon, arbitrary
  quantization, global precision modification or new dependency.
* Preserve strict typing and component formatting conventions.
* Test ownership: `src/core/tests/test_sensor_handover.py`, outside package
  `src/core/src`. Maximum additions: one parametrized unittest method. Exact
  removals: none. Canonical targets are evaluator, test module and core README;
  generated targets: none.

## Acceptance Criteria

* New regression fails on the original implementation at the exact boundary.
* New code passes nonconstant-reference 0.09 and 0.10 steps and rejects 0.11
  at `mean_step=0.1`, with both signs/channels and unequal counts.
* Test assertions inspect mean-step checks, aggregate pass and error magnitude;
  point/stddev limits are generous enough to isolate mean-step behavior.
* Sensor tests, full-core ruff check, format check and mypy pass under heavy lock.
* One independent Review records its assessed boundary and any residual work.
* Local commit contains source/test/docs and original dated RPI artifacts,
  privacy-safe author/committer identity and requested trailer; no push.

## Sources

* `.copilot-tracking/research/2026-10-30/sensor-mean-step-boundary-188-research.md`:
  C1-C6, reproduced rounded error and signed/unequal-window exact oracle.
* `.github/copilot-instructions.md` and `src/README.md`: branch, pip, gate,
  evidence and local-check contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and validate inclusive comparison

Dependencies: completed Research and one finalized critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add failing regression and exact comparison

Add the nonconstant-reference method first, capture its original failure,
then change only the mean-step calculation and document it in core README.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Validate the complete core surface requested

After missing-package failure, create an external Python 3.12 environment and
use `pip install -e 'src/core[dev]'`. From `src/core` run under
`flock -w 600 /tmp/ama-rpi-heavy.lock`:

```bash
python -m unittest discover -s tests -p 'test_sensor_*.py' -q
ruff check .
ruff format --check .
mypy
```

Also include `test_resident_sensors.py` in the same sensor run, without
duplicating suites. Keep command output in external session files and record
counts/status in changes evidence.

<!-- rpi:phase id=P02 -->
### [x] P02: Review and persist local candidate

Dependencies: P01 reconciled and checks completed.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run one independent original Review and local commit

Activate `rpi-review` once, delegate the required independent bounded assessment,
retain original outcome and route open work separately. Then commit with
privacy-safe GitHub identity and Copilot trailer. No push. Do not claim a
fresh complete publication receipt from focused checks.

## Dependencies

* Existing Python 3.12 and pip; external environment install authorized by actual
  missing-package failure.
* Heavy-lock acquisition; unavailable lock or tooling must be reported honestly.
* Independent critique and Review, no repeated gate loops.

## Critique Disposition

Exactly one independent final-candidate critique executed. Original verdict:
Pass, no actionable PC findings. No revision or repeated critique is required.
Artifact:
`.copilot-tracking/reviews/plans/2026-10-30/sensor-mean-step-boundary-188-plan-critique.md`.

## Follow-Up Items

* Coordinator-owned exact-candidate publication gate, hosted checks and human
  approval remain separate; no push is authorized here.
* Actual Hub/Azure SQL handover evidence remains outside this local correction.

## Implementation Context Record

Research and plan are Ready. Details and passing original critique paths are above.
Implementation owns
`.copilot-tracking/changes/2026-10-30/sensor-mean-step-boundary-188-changes.md`.
The automatic parent advances after the one critique is disposed.

## Handoff

P01 complete: 142 sensor tests, one pre-existing opt-in local SQL skip,
full-core ruff/format/mypy passed after typed Decimal sum starts.
P02-T01 complete in the local commit containing this final plan and original
dated evidence. One original independent Review: Complete / Conformant for
the bounded correction, no implementation defects. RV-001 publication and
RV-002 live evidence remain coordinator-owned follow-ups. No source work
remains; no unresolved ordinary decision. No push or issue acceptance follows.
