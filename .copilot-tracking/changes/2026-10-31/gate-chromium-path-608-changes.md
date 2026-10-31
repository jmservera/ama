<!-- markdownlint-disable-file -->
# RPI Changes: Chromium pathname admission

## Metadata

* Task ID: 608
* Task slug: gate-chromium-path-608
* Implementation date: 2026-10-31
* Related plan: .copilot-tracking/plans/2026-10-31/gate-chromium-path-608-plan.md
* Phase details: .copilot-tracking/details/2026-10-31/gate-chromium-path-608-phase-details.md

## Execution Status

* Status: Complete
* Declared invocation scope: Full plan P01-P02
* Completed scope markers: P01, P01-T01, P01-T02, P02, P02-T01
* Remaining active-plan markers: None
* First execution boundary: Shared admission helper and CLI/Runner/resume wiring.
* Approved writes: tools/rpi-checks.py, tools/test_rpi_checks.py, src/README.md,
  dated RPI artifacts.
* Validation: Existing focused tooling unittest and ruff; no heavy full run.
* Blockers: None.

## Implementation-Time Plan and Detail Updates

PC-001 was resolved by the planning parent before implementation. Original
critique execution Complete / verdict Revise is retained. Resume uses the
validated selection/source checkpoint before live tool probes. No second critique.

## Validation Record

| Check | Status | Evidence |
| --- | --- | --- |
| python3 -m unittest tools.test_rpi_checks | Passed | 54 tests, 14.160s, exit 0 |
| PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tools.test_rpi_checks | Passed after formatting | 54 tests, 15.291s, exit 0; external session files/608-unittest.log |
| python3 -m ruff check --line-length 100 tools/rpi-checks.py tools/test_rpi_checks.py | Failed, selector mismatch | Global defaults reported 16 pre-existing rule violations; no unrelated source fixes |
| python3 -m ruff format --isolated --line-length 100 tools/rpi-checks.py tools/test_rpi_checks.py | Passed | Formatted changed additions only |
| python3 -m ruff check --isolated --select E,F,I,B,UP --target-version py312 --line-length 100 tools/rpi-checks.py tools/test_rpi_checks.py | Passed | Existing Runner.lint selector; ruff 0.17.3, exit 0 |
| python3 -m ruff format --isolated --line-length 100 --check tools/rpi-checks.py tools/test_rpi_checks.py | Passed | Two files already formatted, exit 0 |
| git diff --check | Passed | Exit 0 |
| Heavy full gate, browser/SQL live execution | Not run | Explicit focused tooling tier; CI is the gate; no receipt produced |

## Completed Work

### Shared pathname admission

P01-T01: tools/rpi-checks.py now derives the 58-byte output bound from Linux
107-byte socket capacity and Chromium's 45-byte suffix using os.fsencode.
CLI checks before output mkdir/tools/lock; Runner checks before folder writes.
Resume passes new_output into validate_receipt after integrity/schema/selection/
source checks and before tool probes, completing PC-001's required wiring.
No receipt schema, environment, ownership, cleanup, workflow or scanner changes.
Focused tests passed.

### Regression and documentation coverage

P01-T02: six methods in tools/test_rpi_checks.py, outside packages, with no
removals. Real Linux AF_UNIX bind succeeds at 107 bytes and rejects 108;
58-byte output admits, 59 rejects; Unicode rejects based on encoded length.
CLI all/changed/resume reject 59/~130-byte outputs before tools, lock, Runner
and verify, leaving no output/receipt; real resume validation is exercised.
Symlink aliases resolve, source/existing-output rejection stays intact; rejected
Runner writes no scratch while browser-free long outputs retain mode 0700,
owned TMPDIR and no receipt. Admitted resume still probes tools and detects
source/integrity tampering. src/README.md documents formula and recovery.

### Focused validation and local judgment

P02-T01 complete. Initial Ruff command accidentally used global configuration;
selected existing Runner.lint isolated rules rather than fixing unrelated
baseline violations. No dependency installation was needed; installed Ruff
0.17.3 ran the existing selectors (gate installs 0.17.1). Tests passed before
and after formatter, and final diff contains no unrelated changes.

## Amendments and Divergences

No scope, authority or architecture divergence. PC-001 was directly planned
before implementation. Validation command refinement is ordinary local judgment.
No workflow was edited and WORKFLOW_HASHES are unchanged.

## Pre-Review Reconciliation

* Plan and details: all declared markers complete with evidence.
* Changes, handoff, validation, blockers and remaining scope: current.
* Follow-up: actual full zero-skip browser/SQL evidence remains outstanding.
* Review readiness: Ready for exactly one independent Review.
* Required human/hosted approval: not performed, not claimed.

## Return-to-Caller State

Implementation Complete for full P01-P02 scope; no active-plan tasks remain.
Automatic RPI parent continues to independent Review. No implementation blocker.

## Follow-Up Items

Actual zero-skip full browser/SQL execution for #608 criterion 3 remains outside
the focused tier and requires CI/full-run evidence. No partial receipt created.
