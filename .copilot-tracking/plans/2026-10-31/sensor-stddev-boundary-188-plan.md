---
title: Sensor standard-deviation inclusive boundary plan
ms.date: 2026-10-31
---

## Task Metadata

* Task ID: 188-pr-587-second-correction
* Task slug: sensor-stddev-boundary-188
* Planning status: Ready; one independent critique Complete / Pass
* Details: .copilot-tracking/details/2026-10-31/sensor-stddev-boundary-188-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-31/sensor-stddev-boundary-188-plan-critique.md

## Executive Summary

Replace rounded standard-deviation subtraction in acceptance with exact
rational population variances and a guarded squared comparison. Keep rounded
metrics as diagnostics and preserve inclusive limits. Add regressions to the
existing core statistical test file, then perform requested local checks,
one independent Review and a local-only commit. Implementation validation passed;
the one original Review is Complete / Conformant, with no implementation defects.
The local completion snapshot is sealed by the commit containing this artifact.

### What You May Not Know

The supplied nine-sample suffix has stddev 29/30; moving its extremes outward
by 0.15 yields 16/15, an exact 0.1 step currently reported slightly larger.
Increasing Decimal precision cannot establish exact acceptance generally.
This correction does not satisfy live #188 or publication gates.

No unresolved implementation decisions. Original evidence stays immutable.

## User Decisions and Requirements

* Full ordered research, plan, implement, review with dated tracking evidence.
* Correct the real PR #587 second finding using exact arithmetic.
* Preserve inclusive limits; add exact-limit and just-above regressions outside package.
* Run core sensor consistency tests, ruff check, ruff format --check and changed-file mypy.
* Pip only, no Azure, secrets, private data or push; local commit with requested trailer.
* Refs #188 only; state bounded proof, not whole-issue acceptance.

## Goals

* Make standard-deviation acceptance exact for admitted fixed-point readings
  and decimal-intent tolerances, without widening limits.

## Scope and Non-Goals

Canonical targets: `src/core/src/zava_forward/core/synthetic/sensor_consistency.py`,
`src/core/tests/test_sensor_handover.py`, `src/core/README.md` and current dated
RPI evidence. Generated targets: none. No removals. No dependency changes,
unrelated numerical fixes, live exercise, publication or remote writes.

## Functional Requirements

* Per-side stddev checks accept iff `abs(sqrt(a)-sqrt(b)) <= t`.
* For exact nonnegative variances a, b and t, let r=a+b-t*t:
  accept iff r<=0 or r*r<=4*a*b. Preserve the sign guard.
* Use Fraction-converted Decimal readings with `pvariance` and
  `Fraction(str(tolerance.stddev))`; no rounded roots in the acceptance predicate.
* Retain means, `pstdev`, error metrics, schema, zero tolerance and other checks.

## Non-Functional Requirements

* Standard library only, proper types, existing lint/format conventions.
* No epsilon, precision guess, relaxed config or packaged tests.
* Keep exact arithmetic private and narrowly scoped.

## Acceptance Criteria

* Supplied 18.55/21.45/20.00 nine-sample reference plus unchanged prefix:
  outward 0.15 accepted at limit 0.1; outward 0.16 rejected.
* Both channels, inward/outward direction and before/after sides tested.
* The 0.15 step rejected with immediately smaller float tolerance
  `math.nextafter(0.1, 0.0)`; point/mean checks remain true.
* Existing sensor tests preserved; requested unit/lint/format/types succeed.
* One original critique and one post-implementation independent Review retained;
  local privacy-safe commit includes dated evidence and Copilot trailer, no push.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-31/sensor-stddev-boundary-188-research.md,
C1-C6, complete/Ready. Changes record to create:
.copilot-tracking/changes/2026-10-31/sensor-stddev-boundary-188-changes.md.
Automatic parent continues only after critique disposition.

## Sources

* Current comparator, core handover tests and core README.
* Core pyproject declares Python >=3.12, ruff 0.17.1, mypy 2.4.0.
* Repository instructions and caller define local-only evidence boundary.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and validate exact acceptance

Dependencies: completed Research and critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add boundary regressions and capture original failure

Owner: existing `src/core/tests/test_sensor_handover.py`. Maximum additions:
one parameterized unittest method; no removals. Semantic and regression coverage
are combined in this method. Details own the fixture matrix.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Implement exact comparison, document and validate

Depends on P01-T01. Private predicate, exact variances and inclusive comparison;
update core README. Record requested checks and failure-to-success evidence.

<!-- rpi:phase id=P02 -->
### [x] P02: Independent Review and local persistence

Depends on P01 completion, reconciled markers/details/changes and validation.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Perform one independent Review and commit locally

Preserve original Review outcome, route any findings to later work; do not
repeat Review. Commit only explicit task paths with privacy-safe identity and
requested trailer. No push, issue update or publication receipt claim.

## Dependencies

Missing-package baseline failure occurred; isolated pip core[dev] installation
succeeded. Requested checks passed, including full-core ruff check/format and
changed-file mypy. No SQL/browser needed for this focused
numerical correction; full publication gating remains deferred before any push.

## Critique Disposition

One independent final-candidate critique executed, original verdict Pass,
zero PC findings. Accepted with no candidate revisions or user decision.
Original artifact: .copilot-tracking/reviews/plans/2026-10-31/sensor-stddev-boundary-188-plan-critique.md.

## Follow-Up Items

* Coordinator: current exact-candidate complete publication receipt and
  hosted/human prerequisites before any separately authorized push.
* Separately authorized live handover evidence: outside this local correction.

## Handoff

P01 complete: original four failing boundary subcases now
pass; all 32 regression subcases pass; core sensor suite 134 tests, 133 passed
and one existing opt-in SQL skip. Full-core ruff check/format (115 files) and
changed-file mypy passed. P02 original independent Review Complete / Conformant;
RV-003 local persistence is satisfied by the local commit containing this final
snapshot (verify commit existence and clean status before claiming completion).
No unresolved local user decision. RV-004 publication and RV-005 live evidence
remain distinct deferred follow-ups; no push or child work authorized.
