<!-- markdownlint-disable-file -->
# Issue88 authorized correction TWO: responsibility-owned status clock

## Authorized Scope and Opening State

Coordinator independent review f786737f returned Revise Medium at exact PR392
head36b5dcfaba9b502887e1f727db86b5b83976dc53. Original departed-owner
finding is closed by coordinator evidence; correction ONE introduced email-
collision ambiguity when one person holds both service/redress responsibility.
This is the second and last authorized correction, not a new full Review.
Original RPI Review/critique and correction ONE historical evidence stay unchanged.

Clean own worktree/topic and exact local/remote36b5dcfa verified before writes.
Remote main remains74617981b71bc3f10bd21d0b78691bc3cf36c473.
No rebase/force push, other worktree/private input, new authority or UI changes.

## Active Plan Scope and Checklist

Reopen P01-T01 and P02-T01/T02 only for this bounded backend correction.
P01-T02 web remains completed and outside new edits. Current status responsibility
is redress for Closed/Independent review, otherwise service. Reassignment changes
status_owner/status_at only if the selected responsibility matches that rule,
never because identities collide. Preserve absent legacy owner/date for the
non-owning responsibility; preserve null historical snapshots when explicitly
assigning current responsibility. Remedy and original history remain independent.

* [x] Failing-first JSON/SQLite shared-person status/responsibility/legacy matrix.
* [x] Minimal responsibility-based source fix and existing control expectation.
* [x] Fresh core/API selectors, current-actor/concurrency/recovery and actual MSSQL.
* [x] Configured statics and docs/evidence/state.
* [x] Normal same-PR source publication; external disposition belongs to coordinator.

No blocker; implementation, local evidence and normal source publication complete.
External correction TWO disposition remains Revise Medium until coordinator
acceptance. No third correction/full Review or self-declared independent Pass.

## P01-T01: Actual Failing-First Boundary and Source Fix

Added one grouped method in existing test_resident_decisions.py:
`test_response_reassignment_status_clock_follows_responsibility_not_shared_person`.
It executes actual service_open/update/close/reassign methods, not fabricated
status transitions. Matrix: three routes (Service request, Complaint, Independent
review), two statuses (Open, Closed), two responsibility keys (service, redress),
two provenance states (captured, legacy absent status owner/date):24 subcases
per backend. Ordinary Service request intentionally assigns Rae to both roles;
Complaint/review use distinct Sam/Rae. Legacy fields are explicitly removed and
saved, never inferred from today's roster.

Before production edits, this command ran:

```bash
PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest \
  test_resident_decisions.JsonResidentDecisions.test_response_reassignment_status_clock_follows_responsibility_not_shared_person \
  test_resident_decisions.SqlResidentDecisions.test_response_reassignment_status_clock_follows_responsibility_not_shared_person -q
```

Two methods ran1.130s, eight failing subcases total. On each backend, same-person
Open/redress and Closed/service reassignment changed the wrong status clock.
Independent review Open/service wrongly changed it, Open/redress failed to update
it because the original intake had captured service owner. These are actual
source failures, not retrospective test claims.

Minimal production fix removes status_owner email lookup and collision-based
owns_status; existing route/state status_key remains, assignment uses
`if key == status_key`. No authority, date, version, identity, transaction, audit,
remedy or response update/close/reopen checks removed or weakened.
Existing independent-review recovery assertion now expects explicitly reassigned
redress manager as status owner, not the previously captured service owner.

Each matrix subcase asserts:

* Owning responsibility reassignment explicitly records Rex/new event date.
* Non-owning responsibility preserves status owner/date exactly, including absent
  legacy fields, even when both responsibilities have the same email.
* Other responsibility owner/email/captured identity remain unchanged.
* Remedy, original opened_at, response status and prior history remain unchanged.
* Version advances once; history retains old status owner/date exactly, null when
  unknown, and new event time matches its explicit current assignment.
* Reopened store and audit chain remain valid.

Current manager/nonmanager, complaint independence, contested reviewer, stale/
malformed version, unknown/wrong-role owner and writer role/OID rebind/concurrency
assertions remain and run unchanged, except the corrected independent-review
status-owner expectation. The new test is inherited by existing MSSQL transport.

## P02-T01: Fresh Executed Selectors and Actual SQL

```bash
.venv/bin/ruff format src/core/tests/test_resident_decisions.py
PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest test_resident_decisions.JsonResidentDecisions \
  test_resident_decisions.SqlResidentDecisions test_resident_api -q
```

74 run18.642s:72 pass/two existing skips (JSON-only rollback in SQLite,
opt-in actual browser). Includes complete commitments, independent mixed closure/
restart, legacy unknowns, new matrix, original recovery, second SQL writer
actor/assignee role/OID changes, competing reassignment, rollback and committed
truthful exactly-once/no-replay plus authenticated HTTP contracts. Fixture's
absent law-store diagnostics are explicit and expected, not legal approval.

Configured checks ran sequentially and passed:

```bash
cd src/core
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
cd ../api
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
```

Core62 formatted/115 typed files; API23 formatted/55 typed. No new exclusions,
dependency installs, weak casts or skipped assertions. No new JS/browser/image
run: no web/server bytes changed; previous correction ONE receipts remain
historical, as authorized. Prior134pass11skip/eight SQL are not fresh counts.

Started only task-owned issue88-correction2-3a36c179, exact container ID
1156685d8dccf687ede66d6ba94dd140ec0b8525be8a27724be228af2ff23a26,
SQL Server2022 with127.0.0.1:32772 binding. Generated mode0600 credential outside
repo, never printed. External nonsecret existing replay harness adapted only
container identity/credential path and added the new matrix selector.
Actual SELECT1 proved responsiveness before tests. UUID databases per fixture.

```bash
PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests \
  .venv/bin/python /home/azureuser/.copilot/session-state/3a36c179-e1e3-4332-9c33-fa947262fd79/files/issue88-integration-mssql.py
docker stop --timeout 20 issue88-correction2-3a36c179
```

Nine actual MSSQL tests passed/no skips48.740s:

* Five resident methods: new24-subcase matrix, original departed-owner recovery,
  manager/version/independent-review/legacy refusals, second-writer role/OID/
  competing-version refusal and audit-insert/recovery-read/precommit rollback/
  postcommit synchronization/exactly-once history and audit.
* Quality postcommit refresh truthful outcome, hazard recovery-read quarantine,
  finance current permission inside save, grant transaction designation/expiry.

Same fixtures/assertions as repository tests; quality/hazard adapter changes only
transport from SQLite to owned actual MSSQL. Expected injected diagnostics remain
visible in session log. Own container stopped immediately after tests, then exact
stopped ID verified before removal with its generated credential. No other
container, process, dirty worktree, private input or cloud write touched.

## P02-T02: Documentation, Fingerprints and Exact Criteria

Existing core/API guides clarify route/state responsibility and unknown history.
Resident synthesis adds this finding/evidence without altering previous receipts;
index retains all routes and links this correction. KB log appends after exact
previous-head/upstream prefixes. No memory/original-case changes.

Only corrected runtime file: resident_decisions.py. Only corrected test file:
test_resident_decisions.py. Original Review/critique and correction ONE evidence
are byte-identical to36b5dcfa; web/server/Store/workflows/progress/quality/hazard/
finance/grants and all SQL commit/discard hooks remain unchanged.

* Original Review SHA256204aab7fa36e86feae5b5f76a2107e8e7a2655a6b11a6d2113a3c231ea008e99.
* Original critique SHA25670fad5b641605fd83c7bc490fcac4c926c9cfcc1d06ba4eaeb63b297c631e01d.
* Correction ONE receipt SHA256c97b6b22c98b2825047682d4924fd5a1e2af8386bed7fbbd5f9dd9f09f398a23.
* Corrected resident source SHA256937a81417a6d073c8ce8f85d976f834af84ab09f0ce1a60c418a158b81587883.
* Corrected core tests SHA2565e19249110e758aa0490cc9f90d6d6f76342040c2fb883bce875be41233d23a7.

| Exact issue criterion | Source and fresh executable proof |
| --- | --- |
| Commitment purpose/current named owner/due/basis | Unchanged update_record/validate_sql and existing complete/reassign/invalid/date/identity methods pass in fresh JSON/SQLite resident suite |
| Response/package never closes open remedy/defect/charge query | Response close/reopen and remedy actions remain separate; mixed_closure_clocks/response_and_remedy tests pass fresh JSON/SQLite; new matrix and recovered close/reopen actual MSSQL preserve entire remedy snapshot |
| Each status retains its owner/date | Corrected service_reassign selects route/state responsibility, not email; 24-subcase actual domain matrix passes JSON/SQLite/MSSQL, checking shared/distinct identities, Open/Closed/Independent review and legacy unknowns; writer rebind/version/recovery tests prove persisted truthful outcomes |

Broader governance RV-001 remains separately owned by planning parent/repository
owner for next #81 backlog triage to Legal/Housing/Complaints; no invented approval
or thresholds. It does not substitute for exact criteria proof. Coordinator owns
final independent correction TWO disposition. No new full Review, self-Pass,
third correction, merge or issue closure.

## Publication Boundary

Final read-only remote check found main advanced to
943febc23e99e397724cb81d2580f781b91e13f7 (sensor PR393). Fetched and
read actual graph: this is a child of pinned validated base74617981. Own topic
remains based on74617981; no authorization to rebase and no new main source
imported. Coordinator owns sequencing with that newer main.
Remote topic remains exact36b5dcfa before source publication.
Fresh account identity resolved via gh api user for repository-local noreply
author/committer; normal same-topic push with required Copilot trailer only.
Exact final published head belongs in PR body/final handoff, not self-referencing
this commit. CI and independent disposition remain pending; do not idle-watch.

Source/tests/docs/evidence published normally as
75a12e9541e2996d77fcb416f27d8174f0b047bb to same PR392. PR/local head
verified, worktree clean after source push. Fresh noreply author/committer and
Copilot trailer present; no force/lease/rebase or main write. Final metadata-only
receipt/state commit follows normally; source bytes remain exactly validated.
Stop for coordinator independent final-head correction TWO disposition. Original
Review/critique/correction ONE receipt unchanged. Resume ID
3a36c179-e1e3-4332-9c33-fa947262fd79. No merge/issue closure or third correction.
