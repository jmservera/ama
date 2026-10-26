<!-- markdownlint-disable-file -->
# RPI Changes: Correction 3 (Refs #350)

* Task ID: issue-350-demo-feedback-correction3
* Related plan: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-correction3-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction3-phase-details.md

## Execution Status

* Status: Partial (P03 outstanding)
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01

## Completed Work

### Newest-first contact handling
* Files: tools/check-demo-feedback.py
* What changed and why: newest contact is index 0; cap 40; older-contact continuity; fixes false failure on cases with existing contacts.

### Strict JSON and latency
* Files: tools/check-demo-feedback.py
* What changed and why: NaN/Infinity rejected at load; latency finite and non-negative.

### Tests
* Files: tools/test_check_demo_feedback.py
* What changed and why: 58 tests with newest-first fixtures, cap, tamper and non-finite regressions.

## Validation Record

| Check | Status | Evidence |
|---|---|---|
| unittest tools.test_check_demo_feedback (venv, installed packages) | Passed | 58 tests OK |
| ruff check --isolated --select E,F,W,B,BLE,I --ignore E501; format | Passed | clean |
| Direct module tests are outside the gate matrix | Noted | run directly |
| Full gate and receipt | Pending | after commit |

## Blockers
* none

## Remaining Work
* P03-T01

## Critique-driven fix

PC-001: `math.isfinite` only on floats; huge integer regression tests added.
