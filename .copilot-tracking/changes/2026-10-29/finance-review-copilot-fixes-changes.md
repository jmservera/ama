<!-- markdownlint-disable-file -->
# RPI Changes: Finance review Copilot fixes

## Metadata

* Task ID: finance-review-copilot-fixes-510
* Date: 2026-10-29
* Plan: .copilot-tracking/plans/2026-10-29/finance-review-copilot-fixes-plan.md
* Details: .copilot-tracking/details/2026-10-29/finance-review-copilot-fixes-phase-details.md

## Execution Status

* Scope: full plan.
* Status: Implementation and independent Review complete.
* Completed: P01/P02 and P03-T01; requested and adjacent validation.
* Remaining: P03-T02 local commit and gate attempt.
* Write boundary: approved core module, external tests, component READMEs and
  dated artifacts. No push, Azure or rubric-score editing.

## Execution Summary

Baseline focused discovery passed 26 tests in the installed session venv.
Implement regressions first, preserve their failing output, then apply fixes.

## Completed Work

### Failing regression evidence

* P01-T01/P02-T01: three new test methods in src/core/tests/test_form_review.py.
* Before production edits, targeted unittest ran 3 tests, exit 1, with 8 blank
  missing-diagnostic subtest failures and 8 source-unavailable subtest errors.
* Both JSON and SQLite reproduced the defects. Zero/false control test passed.
* Missing bytes and deleted metadata raised DocumentUnavailable; subsequent
  quarantine subtests encountered StopIteration because the failing assertions
  prevented fixture restoration. This is original adverse evidence, not proof
  of an additional product defect. Re-run all scenarios after the fix.

## Implementation-Time Plan and Detail Updates

None; the approved plan remains Ready.

### Required-input confirmation and isolated unavailable reports

* P01-T01/P02-T01: _valid remains type-only; blank strings are omitted from
  confirmed without discarding corrections or emitting incorrect type failures.
* view builds each report inside a DocumentUnavailable-only handler, returning
  exactly draft_id, Unavailable status and a fixed notice; actor/case checks and
  all write paths remain outside that handler.
* Updated existing read-denial tests to exact opaque entries, retaining action
  exceptions, source-recovery, nonmutation, outage and cache tests.
* Completion evidence: focused discovery now passes all 29 tests (8.762 s).
  Two-draft missing-byte, metadata-deletion, pending and infected scenarios pass
  on both JSON and SQLite, with unaffected sibling equality and full recovery.

### Authenticated endpoint and contract documentation

* P02-T02: one new two-draft HTTP test verifies GET 200 with an exact opaque
  first entry and unchanged readable sibling. The existing quarantine test now
  asserts the per-entry response and explicitly checks POST still returns 403.
* Core/API README sections describe required blank semantics and GET/POST
  unavailability distinctions. No web assets, new routes or financial authority.
* Exactly four new test methods total (three core, one API), no tests removed.
* Validation: all 7 API staging/review tests pass, as do targeted Ruff/format/mypy.

### Gate eligibility and preserved workspace inputs

* Ordinary local judgment: no source/acceptance change. Unknown/pre-existing
  ignored caches, bytecode and editable egg-info metadata exist in this
  checkout. The gate's clean_identity explicitly refuses ignored inputs.
* A blanket cleanup is outside retention/ownership authority. Preserve those
  inputs and attempt the gate after commit, recording refusal without claiming
  an exact-head receipt. No foreign heavy-lock holder was listed by lslocks.
* This does not block the requested focused checks or the local-only commit.

### Single independent Review

* P03-T01: independent general-purpose reviewer activated rpi-review and wrote
  .copilot-tracking/reviews/logs/2026-10-29/finance-review-copilot-fixes-review.md.
* Execution Complete, outcome Residual work. No implementation defects.
  RV-001 Low routes clean-candidate/gate readiness to separate owner follow-up.
* Reviewer inspected full task delta and evidence, verified diff hygiene/test
  budget, and did not rerun supplied tests. No second Review or source changes.
* Reconciled plan/details/state; original critique and Review retained unchanged.
* git-commit skill's referenced commit-message instruction file was absent and
  get_changed_files is unavailable in this host. Use repository Conventional
  Commit, explicit scoped staging and required coauthor trailer instead.

## Validation Record

| Check | Result | Evidence |
| --- | --- | --- |
| Initial four requested commands | Unavailable, exit 127 | python, ruff, mypy absent on PATH |
| Install existing core[dev], agents, api | Passed, exit 0 | Session-owned external venv; pip editable installs |
| Baseline form-review discovery | Passed, exit 0 | 26 tests, 7.453 seconds |
| New regression-only run before fixes | Failed, exit 1 | 3 methods; 8 failures / 8 errors, recorded above |
| Required discovery after fixes | Passed, exit 0 | 29 tests, 10.381 seconds |
| Adjacent form staging | Passed, exit 0 | 17 tests, 4.373 seconds |
| Core ruff check . | Passed, exit 0 | All checks passed |
| Core ruff format --check . | Passed, exit 0 | 112 files already formatted |
| Core mypy | Passed, exit 0 | 165 source files, no issues |
| API test_form_staging_api | Passed, exit 0 | 7 tests, 7.233 seconds |
| API changed-test Ruff/format/mypy | Passed, exit 0 | 1 file formatted/typed, no issues |
| git diff --check | Passed, exit 0 | No whitespace errors |

Commands from src/core (all four requested commands, unchanged):

```bash
PYTHONPATH=src:tests:../agents/src:../agents/tests python -m unittest discover -s tests -p 'test_form_review*'
ruff check .
ruff format --check .
mypy
PYTHONPATH=src:tests:../agents/src:../agents/tests python -m unittest test_form_staging -q
```

Commands from src/api:

```bash
PYTHONPATH=tests:../core/tests:../agents/tests python -m unittest test_form_staging_api -q
ruff check tests/test_form_staging_api.py
ruff format --check tests/test_form_staging_api.py
mypy tests/test_form_staging_api.py
```

External environment:
/home/azureuser/.copilot/session-state/f0ad9e37-f38b-4230-b815-593da420a420/files/finance-review-venv.
Use PYTHONDONTWRITEBYTECODE=1 and external caches for further validation.

## Pre-Review Reconciliation

* Plan P01/P02 and details completion current; P03 Review/commit/gate remain.
* Required and adjacent checks passed; failing-before evidence retained.
* No unresolved implementation divergence or follow-up source change.
* Single independent task-delta Review complete; original Residual work outcome
  and RV-001 preserved. No code change or re-review follows this record.
* Full-gate eligibility blocked by ignored workspace inputs, separately from
  the successful requested checks. Human/hosted approvals not performed.

## Blockers

None for implementation. Full-gate clean-input policy blocks this checkout;
preserve unknown scratch and obtain an authorized clean candidate before any
publication. No push is authorized in this task.

## Remaining Work

P03-T02 local commit/gate attempt.

## Follow-Up Items

RV-001 Low: clean-candidate/gate readiness before future publication, rank 1;
owner-authorized follow-up outside this local-only fix.

## Return-to-Caller State

Implementation and Review complete; parent owns local commit/gate bookkeeping
under the explicit bounded loop request. Required focused checks passed;
full gate is not claimed. Preserve original Complete / Residual work Review.
