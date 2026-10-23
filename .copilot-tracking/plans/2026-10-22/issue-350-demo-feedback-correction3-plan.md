<!-- markdownlint-disable-file -->
# RPI Plan: Correction 3 (Refs #350)

* Task ID: issue-350-demo-feedback-correction3
* Planning status: ready
* Research: .copilot-tracking/research/2026-10-22/issue-350-demo-feedback-correction3-research.md
* Phase details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction3-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-22/issue-350-demo-feedback-correction3-plan-critique.md

## Requirements

* Select the newest contact as `contacts[0]` in write and reload; enforce the 40-contact cap and older-contact continuity with the before detail.
* Reject NaN, Infinity and -Infinity at JSON load; require finite non-negative numeric `latency_ms`.
* Realistic newest-first fixtures with existing contacts and a capped response; NaN/Infinity regressions; keep SQL durability blocked.

## Phase Checklist

### [x] P01: Checker fixes
#### [x] P01-T01: Newest-first selection, cap, continuity
#### [x] P01-T02: Strict JSON constants and finite latency
### [x] P02: Tests
#### [x] P02-T01: Newest-first, capped, tamper, NaN, Infinity fixtures
### [ ] P03: Validate and publish
#### [ ] P03-T01: One new full gate, official receipt verification, push same draft PR 436

## Critique Disposition

* PC-001 (Medium) huge-integer OverflowError: resolved (isfinite on floats only; regressions added). PC-002 (Low) cap offline limit: accepted residual risk.
* Critique ordering gap: implementation preceded this critique in the session; the critique below is post-implementation evidence and is recorded as such, not as preimplementation.

## Follow-Up Items

* Parent RV-001..RV-004 remain open; the new test module is outside the gate matrix.
