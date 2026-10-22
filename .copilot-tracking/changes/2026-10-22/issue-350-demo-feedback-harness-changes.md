<!-- markdownlint-disable-file -->
# RPI Changes: Offline demo-feedback acceptance harness (Refs #350)

## Metadata

* Task ID: issue-350-demo-feedback-harness
* Related plan: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-harness-plan.md
* Phase details: .copilot-tracking/details/2026-10-22/issue-350-demo-feedback-harness-phase-details.md
* Implementation date: 2026-10-22

## Execution Status

* Status: Partial (P03 validation, gate and publication remain)
* Declared invocation scope: full plan
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01
* All remaining active-plan markers: P03, P03-T01
* Status basis: checker and tests written and passing; Review, gate and publication outstanding.

## Execution Summary

Implementation opened after the single plan critique (Revise, PC-001..PC-007 applied directly). Isolated venv at /tmp/fh350-venv with pip-installed src/core, src/agents and src/api (editable) and Ruff 0.17.1; `zava-forward-agents` is a local distribution, so all three are installed together.

## Completed Work

### Offline checker

* Related phase or task: P01-T01, P01-T02
* Files: tools/check-demo-feedback.py
* What changed and why: new standalone checker; bounded evidence loader, four-state per-check report, exit codes 1/2/3 (0 reserved, unreachable), checks for image identity, /api/me, case write/reload, bounded AI, baseline distinction, plus permanent not-run gaps for spend bound and administrator account. Runtime builders are imported lazily only when evidence is supplied.
* Completion evidence: CLI with no evidence prints all not-run and exits 3.
* Validation: unit tests and Ruff passed (see Validation Record).

### Focused tests

* Related phase or task: P02-T01
* Files: tools/test_check_demo_feedback.py
* What changed and why: 45 tests using fixtures built from `me_payload`, `navigation`, `taskqueues.contract`, ledger entries and `Store.REC_LABEL`; cover pass/fail/blocked/not-run, redirects and 401/403 never succeeding, template-vs-AI, 980 vs 60,000, input safety, AST check for broad handlers/network imports, CLI exit codes.
* Completion evidence: 45 tests OK.
* Validation: Passed.

## Implementation-Time Plan and Detail Updates

### Image identity pass needs an independent expected digest

* Affected plan area or markers: P01-T02 image_identity
* What changed: a valid digest reference alone is `blocked`; `pass` requires a matching `--expect-image-digest`.
* Why: the reference is self-declared evidence, and the plan says self-declared fields cannot raise a verdict above blocked on their own (PC-003). Consistent with approved intent, no user decision needed.
* Triggering evidence: implementation of PC-003 against the image slot.
* User answer or decision: none required
* Reconciliation performed: plan functional requirement text already allows expected-digest comparison; no marker change.
* Planning and critique state: not needed; critique not repeated.

### Ruff configuration observation

* Affected plan area or markers: P03-T01 quality gates
* What changed: Ruff 0.17.1 default-config run reports 47 C408 (`dict()` call) findings from the environment's settings; existing tools/rpi-checks.py shows the same class of findings, and the gate lints only project directories. Ran `ruff check --isolated --select E,F,W,B,BLE,I --ignore E501` (clean) and `ruff format`.
* Why: avoid unrelated style churn; existing tools are not held to C408.
* Triggering evidence: ruff output on tools/rpi-checks.py.
* User answer or decision: none required

## Validation Record

| Check | Scope | Status | Evidence or reason |
|-------|-------|--------|--------------------|
| Runtime packages import | venv | Passed | `zava_forward.api.workbench` and `core.projection` import |
| Focused unittest | tools/test_check_demo_feedback.py | Passed | `/tmp/fh350-venv/bin/python -m unittest tools.test_check_demo_feedback -q`: 45 tests OK |
| Ruff 0.17.1 targeted | two new files | Passed | `ruff check --isolated --select E,F,W,B,BLE,I --ignore E501`; `ruff format` applied |
| CLI smoke | no evidence | Passed | all not-run, exit 3 |

## Pre-Review Reconciliation

* Plan markers and phase details: current (P01, P02 checked; P03 open)
* Completed-work evidence and handoff prose: current
* Validation, blockers, remaining work, and follow-up items: current; full gate pending after Review
* Review readiness: ready

## Blockers

* none

## Remaining Work

* P03, P03-T01: Review, commit, full gate, receipt verify, push, draft PR.

## Follow-Up Items

* Canonical plan list: .copilot-tracking/plans/2026-10-22/issue-350-demo-feedback-harness-plan.md
* none yet

## Return-to-Caller State

* Implementation execution status: Partial (P03 publication remains)
* Declared scope and markers: full plan; P01, P02 complete
* Validation coverage: focused tests and Ruff passed; gate pending
* Blockers: none
* Current plan and detail updates: none
* Planning and critique state: ready; critique PC-001..PC-007 resolved
* Follow-up items: none
* Review readiness or no-handoff reason: ready_for_review
* Continuation owner: confirmed automatic RPI Agent
