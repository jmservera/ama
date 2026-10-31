---
title: Sensor standard-deviation inclusive boundary research
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Research Brief

Research the second PR #587 correction, Refs #188: exact inclusive
standard-deviation comparison in `sensor_consistency.py`. Audience: implementer
and independent reviewer. Output mode: convergence preparing planning.
Scope: comparator, existing external-package sensor consistency tests and
directly related documentation. Non-goals: live acceptance, Azure, secrets,
remote writes, unrelated numerical changes or whole-issue completion.
Criteria: exact boundary accepted; just-above rejected; existing semantics and
report shape retained; requested local unit, lint, format and type checks.

## Research Parameters

Focused posture, selected from the caller's bounded source target and concrete
failure. Evidence root: `.copilot-tracking/`. Initial internal candidates:
comparator, existing external-package tests, component instructions,
prior correction evidence. External scope: none. Research source edits: none.
User explicitly requests the full ordered loop and local commit without push.
No clarification is needed; execution is non-interactive.

## Extension Registry and Provenance

| Extension | Disposition and authority |
| --- | --- |
| `.github/copilot-instructions.md` | Selected: pip, local component checks, branch/privacy/trailer and publication boundaries |
| RPI research/plan/implement/review skills | Selected: ordered evidence and one-pass critique/review |
| Research specialist | Skipped: one tightly coupled numerical trace, handled inline |
| Web/design skills | Skipped: backend-only change |

## Direction Controls

* Preserve inclusive tolerance and report schema, no epsilon or rounded acceptance.
* Reuse clean `feat/sensor-ingestion-consistency-188`, confirmed open PR #587.
* Commit locally only; Refs #188, no issue completion assertion.

## Research Questions

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | What exact comparison preserves the standard-deviation limit? | depth | Answered C1/C4 |
| Q2 | Which fixtures prove the boundary and detect widening? | straightforward | Answered C4/C5 |
| Q3 | What validation and acceptance boundaries apply? | straightforward | Answered C3/C6 |

## Prior Knowledge Gate

Caller example and prior mean correction were verified against the current
comparator and `git show cd8fc725`. Existing mean correction research/critique
and state were inspected; original evidence remains untouched. Branch HEAD at
intake: `2f5685ce`; worktree clean. The previous correction is completed with
publication/live follow-ups still unproven.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

The comparator currently subtracts `pstdev(Decimal)` values for acceptance.
Point and mean checks use Decimal; diagnostics expose floats. External-package
SQL integration tests are in `src/api/tests`; statistical tests are in
`src/core/tests/test_sensor_handover.py`, outside the package. Reflection:
preserve diagnostics, investigate an
exact variance predicate rather than altering thresholds or public metrics.

#### Wave 2: Deeper

For nonnegative exact variances a, b and limit t,
`abs(sqrt(a)-sqrt(b)) <= t` iff `a+b-t*t <= 0` or
`(a+b-t*t)**2 <= 4*a*b`. The guard preserves sign before squaring.
`pvariance` over Fraction-converted Decimal readings yields exact rational
population variance, independent of recurring division and square-root rounding.
Reference spread 1.45 with four extremes in nine readings yields variance
841/900; outward spread 1.60 yields 256/225. Their exact stddev difference is
1/10 but the current subtraction is
`0.1000000000000000000000000003`, incorrectly rejecting the inclusive boundary.
Reflection: isolate exact acceptance from existing rounded diagnostic metrics.

#### Wave 3: Contrarian

Inline arithmetic probe accepted spread changes 0.14/0.15 and rejected 0.16.
The same 0.15 fixture with limit `0.09999999999999999` rejected; limit zero
rejected and limit two accepted. Algebra is symmetric in variance order.
At t=0 it accepts iff a=b; with a zero variance it reduces to the other variance
being <=t*t. Negative residual must short-circuit before squaring.
Finite-precision Decimal variance/sqrt or epsilon acceptance remain vulnerable
to context/boundary errors or intentional widening. Reflection: choose exact
Fraction variance, retain rounded reporting; test both directions, channels and
handover sides, plus an immediately smaller representable float tolerance.

#### Parent Synthesis and Re-entry

Accepted exact rational variance and guarded squared comparison (C4), existing
statistical fixture ownership (C5), and focused validation (C3/C6). Rejected
epsilon and larger Decimal precision as non-exact alternatives. No delegated
research ran: this is one coupled trace. No further cycle required: all scoped
questions are answered and contrarian challenges leave no material gap.

## Evidence Log

| ID | Finding | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Acceptance subtracts rounded square roots; all limits documented inclusive | `src/core/src/zava_forward/core/synthetic/sensor_consistency.py:64`, `:125`, `:135` | High |
| C2 | Exact mean-step numerator already avoids rounded means | `src/core/src/zava_forward/core/synthetic/sensor_consistency.py:127` | High |
| C3 | Dev tools declared as ruff/mypy and Python >=3.12 | `src/core/pyproject.toml:9`, `:18` | High |
| C4 | Exact comparison follows guarded squaring; supplied boundary reproduced | `src/core/src/zava_forward/core/synthetic/sensor_consistency.py:125`, `:135`; inline Python arithmetic probe 2026-10-31 | High |
| C5 | Existing statistical and mean-boundary regressions belong outside package | `src/core/tests/test_sensor_handover.py:57`, `:221` | High |
| C6 | Local synthetic checks are not live/whole-issue acceptance; full gate before publication | `src/core/README.md:259`, `src/README.md:61`, `.github/copilot-instructions.md:62` | High |

External evidence: none required or fetched.

## Alternatives and Decision State

Select a small private exact-variance predicate called for each side and channel.
Keep `pstdev` and its subtraction only for report diagnostics. Fraction conversion
from Decimal preserves reading values; Fraction from `str(tolerance.stddev)`
preserves existing decimal-intent tolerance semantics. No dependencies change.

Remaining uncertainty: exact-rational arithmetic costs more than rounded
arithmetic, bounded by existing admitted windows; no live capacity claim is made.
No arbitrary Decimal-context contract is added for unrelated point/mean checks.
Publication receipt and live criteria are deferred, not satisfied by this fix.

## Planning Readiness

Ready. Research disposition: executed, complete wider/deeper/contrarian cycle.
Self-check: scoped questions answered; evidence/alternatives/constraints recorded;
source unchanged; actual test owner resolved; original evidence preserved.
Baseline test failed with missing `zava_forward`; isolated pip installation of
`src/core[dev]` succeeded after that failure. Planning can proceed with existing
test owner and exact algebra. No publication or remote action is authorized.
