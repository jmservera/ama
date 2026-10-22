<!-- markdownlint-disable-file -->
# RPI Changes: Correction 2 (Refs #350)

* Task ID: issue-350-demo-feedback-correction2
* Related plan: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-correction2-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-correction2-phase-details.md

## Execution Status

* Status: Partial (P03 outstanding)
* Completed scope markers: P01, P01-T01, P02, P02-T01

## Completed Work

### Note comparison
* Files: tools/check-demo-feedback.py
* What changed and why: submitted note compared with write-response and reloaded contacts using the runtime 500-character truncation; held note blocked.

### Regression tests
* Files: tools/test_check_demo_feedback.py
* What changed and why: 51 tests, adding note mismatch, truncation and held-note cases.

### Correction-1 claim fixed
* Files: .copilot-tracking/changes/2026-10-22/issue-350-demo-feedback-correction1-changes.md
* What changed and why: states that request comparison covered outcome and channel only.

## Validation Record

| Check | Status | Evidence |
|---|---|---|
| unittest tools.test_check_demo_feedback (venv) | Passed | 51 tests OK |
| ruff check --isolated --select E,F,W,B,BLE,I --ignore E501; format | Passed | clean |
| Full gate and receipt | Pending | after commit |

## Blockers
* none

## Remaining Work
* P03-T01
