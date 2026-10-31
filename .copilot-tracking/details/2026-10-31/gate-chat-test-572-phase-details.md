<!-- markdownlint-disable-file -->
# RPI Phase Details: gate-chat-test-572

## Metadata

* Task ID: 572
* Date: 2026-10-31
* Related plan: .copilot-tracking/plans/2026-10-31/gate-chat-test-572-plan.md
* Evidence: .copilot-tracking/research/2026-10-31/gate-chat-test-572-research.md, C1-C8.
* Starting state: current source already wires the selector. No implementation edits yet.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Exact execution evidence | Complete | P01-T01, P01-T02 |
| P02 | Validation and Review | Actual execution blocked; original Review Complete / Residual work | P02-T01, P02-T02 |
| P03 | Publication gate | Attempted; blocked by shared lock | P03-T01 |

<!-- rpi:phase id=P01 -->
## P01: Exact execution evidence

Boundary: gate/parser/regression owners and src guide only. Preserve inherited
dispatch/inventory/workflows and all existing tests. No generated code targets.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Shared parser and execution/verification parity

C3/C4 establish aggregate-only verification. Extend check_skips with optional
expected-test ID, default None. When set, parse verbose test-result lines and
require exactly the expected "... ok", total=1, executed=1, no skips. Determine
the expected ID only for CHAT_PANEL_BROWSER_SELECTOR in argv at both call sites.
Existing generic suite/SQL behavior is unchanged. Errors are explicit GateError.
Completion: both call sites use the same parser and focused regressions pass.
Completed: optional expected_test shared by both call sites; tooling regressions
pass (39 tests). Existing discovery and generic suite contracts remain unchanged.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Owned regression coverage and guide

GateTests owns all new tests (maximum two methods). Remove none. Extend existing
chat receipt mutation coverage for wrong success name, missing success line,
duplicate lines and count mismatch with freshly recomputed hashes. Update
scoped_receipt and full-receipt fixture generators only for the named command.
A live Runner.command regression must reject unrelated positive aggregate output.
Document exact verbose success enforcement in src/README.md. Existing opted-in
chat_panel test remains the semantic Playwright owner.
Completed: two new test methods, five new receipt mutation cases, both passing
fixtures corrected and guide updated. No test removed; no workflow changed.

<!-- rpi:phase id=P02 -->
## P02: Validation and independent Review

Depends on P01. Only synthetic local exercises; never inherit private datasets or
credential files. Shared heavy lock admission must be respected.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Requested commands and browser

From src/api:

```bash
PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q
ruff check .
ruff format --check .
ZF_BROWSER_TESTS=1 PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest -v test_chat_panel.PanelTests.test_browser_warning_failure_keyboard_refusal_and_live_log
```

From root: tools unittest as requested, targeted Ruff and strict mypy. The exact
browser test proves warning/failure/keyboard/refusal/live-log behavior locally,
not human accessibility or model/live-service acceptance. Retain external logs.
Current evidence: 39 tooling tests and tooling static checks passed after main
integration; pinned API Ruff passed. Initial API suite failed only for missing
dependencies, restored with pip. Both restored API/Chromium attempts timed out
on the foreign shared lock before execution. Actual browser remains Not run.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Original one-pass Review

Independent reader assesses frozen implementation, plan/critique and supplied
validation once. Review execution is distinct from outcome and final gate.
Blocked P02-T01 execution remains unchecked and is assessed explicitly; this
permits credible source review, not acceptance or publication without execution.
Write .copilot-tracking/reviews/logs/2026-10-31/gate-chat-test-572-review.md.
Blocking current-task source/acceptance findings stop publication and remain
preserved. Missing final committed gate evidence may proceed to P03 as planned.
Nonblocking residuals must be explicitly disposed without relaxing requirements.
Original Review completed once on integrated head b9a0db45. No blocking source
defects found; overall outcome Residual work. RV-001 requires actual restored
API/Chromium and RV-002 requires fresh full committed gate/verification and
eligible exact-head assessment. Both remain acceptance obligations, not closure.

<!-- rpi:phase id=P03 -->
## P03: Publication gate

Depends on original Review and clean candidate commit.

<!-- rpi:task id=P03-T01 -->
### P03-T01: Final receipt and publication

Commit implementation/original evidence before running the full gate. Use
python3 tools/rpi-checks.py --all --jobs 3 --lock-timeout 600 --base current-main
--out new-external-directory, without an outer lock (runner already locks).
Require all selected groups, actual browser and MSSQL, passing fresh receipt and
--verify-receipt against fetched current origin/main immediately before push.
Independent exact-head assessment remains separate from original Review and
cannot substitute for human/hosted approval. If any prerequisite fails, preserve
adverse evidence and block publication, rather than omit a group or fake success.
Publication also requires no unresolved blocking original Review findings and an
eligible independent exact-head assessment. No second original Review is allowed.
Current-main drift may be reconciled by an intermediate implementation checkpoint
and clean non-rewriting topic merge before original Review. This is not the final
candidate: original Review/evidence commit still precedes the complete gate.
Actual attempt: after original evidence commit 1a481c4f, incorporated upstream
agent-only #599 through non-rewriting merge dd89a42f (no task source changes).
Ran --all --jobs 3 --lock-timeout 600 against base 1330869e and new external
gate-572-final-dd89a42f directory. Exit 1: Global heavy-resource lock timeout.
No required group, including browser or MSSQL, executed; no receipt was sealed.
Verification, eligible independent publication assessment, push and PR were not
performed. Keep P03-T01 unchecked. Later retry requires the new committed head
and freshly fetched base, not reuse of this adverse attempt.
