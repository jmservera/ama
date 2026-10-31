---
title: Sensor mean-step inclusive boundary correction research
description: Focused research for PR 587, Refs #188
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

* Target: verify rounded Decimal mean subtraction and exact cross-multiplied comparison.
* Purpose and audience: evidence for a bounded correction to PR #587, Refs #188.
* Scope: `src/core` consistency evaluator, external tests, relevant component guides.
* Non-goals: live sensors, Azure, secrets, unrelated changes, publication or push.
* Criteria: reproduce the nonconstant-reference inclusive-boundary failure, retain
  rejection above the limit, preserve report shape and existing checks.
* Output mode: convergence; prepares implementation planning.
* Requested outputs: dated full RPI evidence and a local correction commit.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Why does exact 0.10 fail, and how should the comparison preserve inclusivity? |
| Codebase scope | `src/core`, dated tracking artifacts |
| External scope | None |
| Initial internal candidate areas | `sensor_consistency.py`, `tests/test_sensor_handover.py`, component README and pyproject |
| Initial external candidate areas | None |
| Research posture | Focused |
| Provenance | Bounded caller-supplied target and reproducer |
| Explicit limits | pip only, src only, heavy runs under `/tmp/ama-rpi-heavy.lock`; no Azure/secrets/push |
| Completion basis | Material arithmetic and coverage questions resolved |
| Research edits | Evidence and workflow state only |
| Resolved evidence root | `.copilot-tracking/research/2026-10-30/` |

## Extension Registry and Provenance

| Kind | Candidate | Provenance and contract | Selection |
| --- | --- | --- | --- |
| Instruction | `.github/copilot-instructions.md` | Repository-wide code, evidence, local gate and branch rules | Selected |
| Skill | `rpi-research` | Three-wave evidence protocol | Selected |
| Specialist | RPI Researcher | Registered independent research lanes | Skipped: one tightly coupled arithmetic trace |
| Domain | Web and regulatory skills | No web or legal changes | Not applicable |

## User Participation and Research Decisions

The explicit full-loop request authorizes ordered phase execution without routine
phase prompts. Noninteractive execution needs no scope clarification. Use the
existing clean `feat/sensor-ingestion-consistency-188` branch, associated with open
PR #587, based on `18602ae7`. Do not push.

## Scope and Success Criteria

Research must establish the exact formula, current input precision/validation,
test conventions and required commands. Assertions about live acceptance and
whole #188 completion remain excluded.

## Task Research Requests and Direction Controls

The caller supplies prefix `10.00` three times, reference suffix `9.99, 10.00,
10.00`, observed suffix shifted by `0.10`, inclusive `mean_step=0.1`. Compare
cross-multiplied sums before division. Test code belongs outside the package.

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What arithmetic causes the false rejection? | Straightforward | High | Answered |
| Q2 | Which exact comparison and regression preserve the contract? | Depth | High | Answered |
| Q3 | What validation and publication boundaries apply? | Straightforward | High | Answered |

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory. The index identifies
existing synthetic-only handover evidence and explicitly excludes live acceptance.
The clean branch and open PR were verified, not assumed from the request.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

The evaluator uses Decimal observations and `statistics.mean` per side, then
subtracts means. Existing guides and tests are the next evidence sources.
Inline execution is appropriate for this bounded continuous trace.

Reflection: the reported defect matches the comparison shape; verify fixture,
numeric input bounds and negative/unequal-side counterexamples before planning.

#### Wave 2: Deeper

Verified the caller's arithmetic with Python 3.12.3: rounded error is
`0.100000000000000000000000003` and the old comparison is false. The
cross-multiplied numerator is `0.90`, equal to scaled limit `0.9`. With before
count B and after count A, compare
`abs((sum_after - ref_sum_after) * B - (sum_before - ref_sum_before) * A)`
to `Decimal(str(limit)) * B * A`, dividing only for the reported error.

The observation contract permits at most two fractional digits and absolute
values <=999.99 (C3). Existing tests cover constant-reference inclusive limits,
but not a nonconstant reference with recurring means (C4). The public report
shape and means/stddev calculations need not change.

Reflection: non-dividing arithmetic resolves the real failure without epsilon.
Challenge both step signs and unequal side counts; keep independent point and
stddev checks from masking the mean-step assertion.

#### Wave 3: Contrarian

Challenged sign handling, cancellation and unequal counts using before/after
counts `(3,3)`, `(2,3)`, `(3,4)`, both signs, and `0.09/0.10/0.11` deltas.
All 18 cross-multiplied comparisons agreed with a `Fraction` oracle, including
a shared `0.02` offset on both sides. This guards against accidentally assuming
equal counts or dropping the prefix-reference correction.

Reflection: increasing Decimal precision cannot generally terminate recurring
means; epsilon would loosen the contract. Fixed-point input sums and integer
cross-products avoid the identified recurring-division error before comparison.
No new dependency or API change is needed.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Cross-multiplied sums | C1, C3, arithmetic/oracle experiments | Accepted | Exact boundary comparisons for the admitted fixed-point inputs |
| External nonconstant-reference regression | C4 | Accepted | Existing constant references miss this failure |
| Increased context precision or epsilon | C1, oracle experiment | Rejected | Does not address recurring division or weakens inclusive limit |
| Actual Hub/Azure SQL evidence | C6, caller exclusion | Deferred | Not authorized or established by local arithmetic checks |

#### Cycle Re-entry Evaluation

No further cycle required: focused arithmetic questions and surrounding contract
are covered, and counterexamples confirm the formula. Broader discovery would
not change this correction.

## Evidence Log

| ID | Claim | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Mean-step check subtracts already divided Decimal means | `src/core/src/zava_forward/core/synthetic/sensor_consistency.py:117` | Read | High |
| C2 | Strict type checking and lint/format tooling are configured | `src/core/pyproject.toml:23` | Read | High |
| C3 | Input values have <=2 decimal places and magnitude <=999.99 | `src/core/src/zava_forward/core/sensor_consumer.py:20`, `:395` | Read | High |
| C4 | Constant-reference boundaries are tested; recurring-reference example is absent | `src/core/tests/test_sensor_handover.py:110` | Read | High |
| C5 | Local full gate is required before publication; its runner owns the heavy lock | `src/README.md:62`, `:113` | Read | High |
| C6 | Local handover contract declares inclusive limits and synthetic-only scope | `src/core/README.md:271` | Read | High |

## Findings Mapped to Questions and Evidence

| Question | Finding | Evidence | Confidence |
| --- | --- | --- | --- |
| Q1 | Recurring means round before cancellation | C1, reproduced caller example | High |
| Q2 | Cross-multiply both reference-adjusted side sums; divide only for reporting | C1, C3, C4, 18-case oracle | High |
| Q3 | Run sensor tests and full-core ruff/format/mypy under heavy lock; do not publish | C2, C5, caller request | High |

## Alternatives and Decision State

Select the caller-directed cross-multiplied comparison. Preserve means/stddev
metrics and schema; derive reported mean-step error from the same numerator.
Reject precision changes, epsilon and arbitrary quantization as unnecessary.
Implementation affects evaluator, external handover tests and its README.

## Open Questions, Risks, and Residual Uncertainty

The admitted numbers are small fixed-point decimals; no recurring division is
needed for the decision. Ambient Decimal context mutation is not a new supported
contract. Full publication gate is separate from requested focused checks and
no push is authorized. Package import failed in the default Python environment;
install core with pip into an isolated external environment before testing.

## Current Decisions

Keep changes within the named arithmetic path, tests, directly related component
documentation and dated RPI artifacts.

## Potential Next Research

Only re-enter if numeric bounds or input behavior contradict exact comparison.

## Planning Readiness

Ready (C1-C6). Research disposition: executed, complete. Wider, Deeper and
Contrarian waves completed inline, no workers needed. All research questions
answered; no implementation blocker. No source was changed during Research.

## Closeout Record and Advisory Next Step

The automatic RPI parent continues to Plan after persisting transition intent.
Explicit ordered-loop consent comes from the current user request. This research
artifact is the canonical evidence pointer; full-gate and live-evidence limits
must remain explicit. No unresolved decision needs user input.

## Artifact Self-Check

Brief, parameters, extensions, participation, direction controls, ordered waves,
reflections, disposition, evidence IDs, alternatives, readiness and source record
are complete. No external sources, delegated lanes, secrets or source edits.

## Sources

No external sources used.
