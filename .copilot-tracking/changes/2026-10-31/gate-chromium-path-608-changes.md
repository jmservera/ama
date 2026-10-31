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

## PR #610 Fixture Correction Intake (2026-10-31)

* User-authorized bounded correction: merge origin/main, retain main's rubric
  score and both knowledge-base log entries, correct tools/test_rpi_checks.py
  fixtures, validate, commit, non-force push, reply to and resolve the thread.
* Review input: PRRT_kwDOUU8JX86yStiP identifies ambient gate-owned TMPDIR
  inflation of real pathname fixtures and mock-only Runner selections.
* Approved writes: merge resolutions, tooling tests and current RPI artifacts.
* Validation: focused unittest, including gate-owned TMPDIR at ordinary,
  admitted 58-byte and browser-free long outer outputs. Heavy lock/full gate
  excluded by explicit user direction; CI remains the gate, Refs #608 only.
* Existing critique and original Review remain historical; this invocation
  implements the later hosted finding without repeating either assessment.
* Execution status: in progress; first boundary is the authorized main merge.

### P03-T01: Main integration and owned fixture repair

* Merged origin/main 9c67a399c62eb42f99ac46e1861b55526552c112 in
  9ac5b484. No conflicts occurred, so no `--theirs` resolution was necessary.
  The rubric score and docs/reference/log.md exactly match main; both existing
  knowledge histories are preserved.
* Real socket/Unicode/CLI byte-bound and admitted-resume tests now create
  length-controlled owned `/tmp` roots with registered cleanup, independent
  of ambient TMPDIR. The helper verifies its encoded prefix fits the boundary.
* Individual-method/mock-only Runner fixtures explicitly select no browser
  groups. Cancellation selects preflight only; its child/container cleanup
  assertions remain unchanged. Resource and scheduler fixtures use the same
  browser-free helper; no production guard or dispatch changed.
* Added one regression running ten affected fixture methods beneath actual
  Runner-owned TMPDIR at 18/58/100-byte outer outputs, resetting tempfile's
  cached root and verifying the effective directory.
* Local implementation judgment only; original critique and Review preserved.

### P03-T02: Focused correction validation

| Check | Status | Evidence |
| --- | --- | --- |
| python3 -m unittest tools.test_rpi_checks -q | Passed | 55 tests, 20.484s, exit 0 |
| Full focused suite with gate-owned TMPDIR, 18-byte outer output | Passed after formatting | 55 tests, 21.446s, exit 0 |
| Full focused suite with gate-owned TMPDIR, 58-byte outer output | Passed after formatting | 55 tests, 20.082s, exit 0 |
| Full focused suite with gate-owned TMPDIR, 100-byte outer output | Passed after formatting | 55 tests, 20.609s, exit 0 |
| Existing isolated Ruff E,F,I,B,UP / py312 / 100-column check | Passed | tools/test_rpi_checks.py, exit 0 |
| Existing isolated Ruff format check / 100 columns | Passed after format | Initial one-helper wrapping mismatch recorded; final exit 0 |
| git diff --check | Passed | Exit 0 |
| Heavy lock/full browser/SQL gate | Not run | Explicit user-selected focused tier; CI remains the gate |

Full focused TMPDIR logs are external session artifacts
`files/608-correction-tmpdir-{18,58,100}.log`, not gate receipts.
The entire suite was launched in fresh child processes with
`TMPDIR=<owned-output>/tmp` and `PYTHONDONTWRITEBYTECODE=1`.

### Correction reconciliation and publication handoff

* P03-T01 complete; P03-T02 validation complete, commit/push/thread actions pending.
* Plan and details describe the current bounded correction. Original P01-P02
  evidence and adverse/limited outcomes remain unchanged.
* Direct bounded diff assessment confirms real 107/108-byte sockets and 58/59-byte
  admission assertions remain active, as do no-write/no-probe and cleanup checks.
* No additional independent critique or Review was executed or claimed.
* Refs #608 only; actual full browser/SQL, CI and owner approval remain unmet.

### P03 publication and hosted resolution

* Correction committed as de0aa9aa with the requested Co-authored-by trailer
  and privacy-safe authenticated author/committer email.
* Initial push rejected because origin had e33f98cf. Executed exactly
  `git pull --no-rebase origin fix/gate-chromium-path-608`; only the rubric
  score conflicted. Kept `--ours` because this later pull's ours was fetched
  main's score, whereas theirs was the stale remote topic score. Verified the
  resolved score matches origin/main. The initial main merge needed no conflict
  resolution, and docs/reference/log.md remains unchanged from main.
* Remote integration committed as 7fb024e2 with requested trailer. Non-force
  `git push origin HEAD` succeeded; ls-remote and PR GraphQL headRefOid both
  verified 7fb024e263245f0566629061894db77609a28693.
* Posted reply PRRC_kwDOUU8JX88AAAABCDNZ5g to PRRT_kwDOUU8JX86yStiP, then
  resolved it via GraphQL. Both mutation and fresh query returned isResolved=true.
* P03, P03-T01 and P03-T02 complete. Current correction has no blockers or
  remaining source work; final evidence-only commit/push follows on this branch.
* Automatic state returns to Follow-up, task completed/session running.
  Original independent Review execution/outcome and RV-001 remain preserved.
