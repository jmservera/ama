<!-- markdownlint-disable-file -->
# Issue88 authorized correction ONE: recover departed response owners

## Approved Scope and Opening State

Coordinator external review of final3938fb7f returned Revise / Medium:
_response_event requires the original assigned service/redress owner still be
current eligible staff, but no explicit response-owner reassignment exists.
A departed owner strands response progression, including manager attempts.
The user authorizes correction ONE, not a second full Review or new RPI cycle.
Original single RPI Review/critique remain unchanged. Base74617981 and clean
local/remote3938fb7f9ad6ec413768037f53ea7c9b9b96e608 verified; current
main inspected but no rebase authorized or performed.

Bounded P01-T01/T02 correction: explicit manager-only, versioned reassignment
of service or redress responsibility on an existing service request. Validate
current new owner/actor in writer transaction, retain captured departed-owner
provenance, actor/reason/time and old/new responsibility; never silently make
the acting manager the owner. Ordinary update/close/reopen retain their existing
role and independent-review contract. Remedy, defect/query, delivery, quality,
finance and grants remain separate. No Legal/safety authority is created.

## Execution Checklist

* [x] Failing-first JSON/SQLite departure and recovery/refusal tests.
* [x] Minimal domain action and existing-panel recovery control.
* [x] Writer authority/concurrency and audit/recovery/committed outcome tests.
* [x] Actual owned loopback MSSQL plus HTTP/browser and configured checks.
* [x] Documentation/evidence and source fingerprints.
* [x] Normal same-PR publication; external coordinator acceptance remains pending.

## Planned Evidence

Use existing installed-src fixture/test files, no private data or other dirty
worktrees. Small fictional staff registry only. Exact stale/malformed versions,
unknown/wrong-role assignees, nonmanager/departed manager and writer-time rebinds
must refuse without successful audit or mutation; unrelated clocks unchanged.
Fresh web guidelines retrieved in this correction before editing, and must be
refetched for final changed-web review. Actual browser must exercise recovery/
retained input/focus/live status, keyboard and reduced motion. No WCAG claim.
Prior63pass/two-skip integration and actual SQL receipts remain historical.
No second full Review/self Pass, Azure/paid AI/communications or new role.

## Current State

Implementation, local validation and normal source publication complete for the
authorized correction ONE. The external Revise/Medium disposition remains the
coordinator's to close, not an implementation self-Pass. No new full Review.
Original Review/critique retained, no rebase or scope expansion.

## P01-T01: Actual Failure, Implementation and Writer Evidence

Before domain edits, the new
`test_departed_response_owners_explicit_recovery_keeps_other_clocks` ran against
both JsonResidentDecisions and SqlResidentDecisions. Both reproduced the
ordinary-action refusal after service-owner departure, then failed at the
required recovery action with `ValueError: Unknown step.` Two errors, not a
passing baseline. New `service_reassign` is now in existing action dispatch/
followup transaction validation. It requires current manager, integer current
request version, explicit service/redress responsibility, current eligible
named owner and reason. No acting-manager proxy assignment.

Captured old identity is historical, not reauthorized; history retains old/new
identity, old email/name/status owner/date, event version, acting identity, reason
and UTC time. Legacy absent identity/date remains null. Only selected
responsibility changes; its current status owner/date changes only when it owned
that status. Other responsibility, remedy, original open date and history remain.
Complaint/review alias independence and contested-recorder exclusion remain.
Ordinary service update/close input version semantics were not expanded.

Four new core methods cover JSON/SQLite plus inherited actual MSSQL:

* `test_departed_response_owners_explicit_recovery_keeps_other_clocks`: actual
  service and redress departures, manager recovery, new-owner update, independent
  resolved close/reopen and retained remedy/history.
* `test_response_reassignment_requires_current_manager_version_and_independence`:
  nonmanager/wrong-role/unknown/blank owner, stale/malformed version, missing
  reason/invalid responsibility, departed manager, independent-review restrictions
  and legacy absent identity/date without reconstruction.
* `test_response_reassignment_rechecks_writer_actor_assignee_and_version`: second
  SQL connection rebinds actor/assignee role or OID without case sequence change;
  refusal retains original error/state/audit. Competing stores allow only one
  versioned reassignment and successful event.
* `test_response_reassignment_faults_preserve_history_and_exactly_once_outcome`:
  actual audit insert then first/persistent recovery-read failure preserves prior
  audit and original error, rollback removes reassignment; committed sync failure
  reports ResidentCommittedError, persists exactly once, never replays audit.

HTTP `test_manager_response_owner_recovery_and_truthful_http_outcome` proves
400 departed-owner update, 403 nonmanager, 409 stale version, committed 409 after
successful reassignment/detail failure and healthy new-owner update/redress close.

## P01-T02: Existing Panel and Actual Browser

Only panels.js web bytes changed: native manager-only labelled select/reason
form sends service_reassign to existing resident endpoint with current version.
Visible history names old/new owners and acting manager, reason and date. Existing
scoped form retains draft/error focus/live status and committed-outcome behavior.
No CSS, animation, global form-system, endpoint or permissions redesign.

Actual Chromium journey extends the original test: service owner departs,
Pam submits incomplete recovery, receives focused live error with owner selection
retained; Enter submits explicit new owner Rex. Rex cannot see manager recovery
controls, updates response; Rae closes independently with remedy still Open.
320/390/1280 widths and reduced motion; no page errors. Fixture intentionally has
no law store and emits explicit rule-unavailable diagnostics, not legal approval.
Initial browser selector matched both summary and submit button; corrected
selector uses first summary, no application fallback or weakened assertion.

Fresh source retrieved again during final changed-web review:
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md.
Read all panels.js and evaluated all rules, with owner Fluent/plain-language/
ASCII conventions prevailing over generic capitalization/typography suggestions.
No new-control defect identified in that bounded check. Existing unrelated
findings, not repaired in this correction:

* src/api/src/zava_forward/api/web/panels.js:11 - shared finance/grant numeric
  inputs default to text rather than numeric type/inputmode.
* src/api/src/zava_forward/api/web/panels.js:15 - unrelated actForm is details/
  button rather than native form, so Enter submission is not provided.
* src/api/src/zava_forward/api/web/panels.js:71 - stock assertions use h4 after
  h2 without an intervening h3.

These are not new recovery controls and do not establish full-file conformance.
No screen-reader/human/WCAG acceptance or second full RPI Review claimed.

## P02-T01: Sequential Validation and Honest Interruption

The initial broad combined run and broad SQL replay were interrupted during VM
resource/session failure. No final result exists: neither is a pass. Earlier
72-test resident run passed with two skips; browser then passed separately after
the selector repair. Initial Ruff reported B023 test closures, and subsequent
mypy rejected inferred defaulted lambdas. Fixed with bound class state/typed
default arguments and functools.partial, retaining every assertion.

After owner-authorized resume and exact local/remote/main checks, final commands:

```bash
ZF_RESIDENT_BROWSER=1 PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest test_resident_decisions.JsonResidentDecisions \
  test_resident_decisions.SqlResidentDecisions test_resident_api \
  test_handoff_lifecycle test_handoff_api test_progress_reports test_progress_report_api -q
```

145 run, 134 pass, 11 skips, 51.230s. Actual browser included, not skipped.
Skips: ten opt-in MssqlProgressApi methods and JSON-only rollback in SQLite.
Report source/export/role, full UTC precision/prospective handoff and retained
response/remedy mixed-clock tests pass; historical event capture remains #102.

```bash
PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest test_workflows \
  test_quality_procurement.SqlFlows.test_quality_sql_postcommit_refresh \
  test_quality_procurement.SqlFlows.test_quality_sql_actor_and_stale \
  test_quality_procurement.SqlFlows.test_quality_sql_failures \
  test_hazard_referral.SqlHazardReferral.test_authority_changes_rechecked_at_transaction_for_caller_and_destination \
  test_hazard_referral.SqlHazardReferral.test_recovery_read_failure_quarantines_hazard_and_keeps_prior_audit -q
```

24 pass, no skips, 8.093s. Injected quality refresh/recovery diagnostics are
expected, not swallowed failures.

Actual owned MSSQL: the verified container ID
e021b59b115515280ab3dde5ee28459bb42f700739a39265a08318e1a8ff4ba2,
name issue88-correction1-3a36c179, loopback127.0.0.1:32818 only.
External nonsecret harness selects four new resident tests above, quality
postcommit refresh, hazard recovery quarantine, finance current permission inside
save and grant transaction designation/expiry. Same original fixtures/assertions,
only transport adapted for quality/hazard. Each test owns UUID databases.
SELECT1 verified responsiveness. Eight tests passed/no skips in41.944s before
VM upgrade; after /tmp logs disappeared on upgrade, reran with persistent session
receipt: eight passed/no skips in39.181s. Stopped immediately after each run.
Removed exact stopped owned container and generated credential only after tests.
No other container/process/worktree or private dataset accessed.

Final configured checks, sequential:

```bash
cd src/core
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
cd ../api
../../.venv/bin/ruff check .
../../.venv/bin/ruff format --check .
../../.venv/bin/mypy
node --check src/zava_forward/api/web/panels.js
```

All pass: core62 formatted/115 typed, API23 formatted/55 typed.
No dependency install or PYTHONPATH=mvp. No new image build: original integrated
image/nonroot receipts remain historical, not represented as fresh correction
evidence. Actual changed app journey ran on loopback. No full-core suite claimed.

## P02-T02: Exact Criterion Mapping and Source Preservation

| Exact issue88 criterion | Direct source and executable proof |
| --- | --- |
| Purpose, owner, due date and basis | Unchanged `_res_update_record`/validate_sql, `test_complete_update_and_explicit_reassignment_preserve_history` and invalid/date/current-identity tests in fresh JSON/SQLite suite; actual browser commitment create/reassign/refusal retained |
| Response/package never closes outstanding remedy/defect/charge query | `_res_service_close` response only, `_res_remedy_update` separate remedy, new reassignment only selected responsibility; `test_response_and_remedy_close_and_reopen_are_independent` and `test_mixed_closure_clocks_survive_unrelated_transitions_and_restart` fresh JSON/SQLite; recovered-owner close/reopen also actual MSSQL/browser |
| Each status retains own owner/date | Response status_owner/status_at, remedy owner/at/opened_at/history and existing delivery/quality/finance provenance; new departed-owner/legacy recovery tests preserve old captured owner/date and explicitly record new assignment/time, writer races and refusal/recovery/no-replay prove persistence behavior on SQLite and actual MSSQL |

Only production code changed in correction: resident_decisions.py and panels.js;
tests only test_resident_decisions.py and test_resident_api.py. Component guides,
existing resident synthesis/index/log and current RPI state updated. No actual
correction overlap in shared Store/server/workflows/quality/progress/finance/grants/
hazard runtime; those remain byte-identical to3938fb7f. No #102/#112 dirty source.
KB log retains exact upstream74617981 and previous3938fb7f byte prefixes; index
all routes retained. Original Review/critique exact previous-head bytes:

* Review SHA256204aab7fa36e86feae5b5f76a2107e8e7a2655a6b11a6d2113a3c231ea008e99.
* Critique SHA25670fad5b641605fd83c7bc490fcac4c926c9cfcc1d06ba4eaeb63b297c631e01d.
* Corrected resident source SHA25628f22ba71e9ab80f9e67f4552c26e66d95f1acf2015dd061774d2e3cc864be9e.
* Corrected panels SHA256c9a09479c796d080ca6166a7be69f7ed48550392b25554ab46feb241b027a789.
* Core tests SHA2564de5c9d071bce0e60e6b7148eccedb1f4002852ee003c92f2a3e764b4ceb54e3.
* API tests SHA2564f0694c186defc09e01d9764563ec603161d118d73d0f87f258e7a025e50cc5f.

Excluded governance residual RV-001 remains owned by planning parent/repository
owner: next #81 backlog triage routes lease/scope/age bands to separately owned
Legal/Housing/Complaints review. That is not a replacement for exact remedy proof
and does not block ordinary independently evidenced issue88 behavior.
External final correction disposition remains pending coordinator review8d5e66bd.

## Publication and Stop

Fresh gh api user resolved account identity; repository-local noreply email used
for both author and committer with required Copilot coauthor trailer. Normal
source/evidence commit5cfa8e53ef28fbfe2a9aae681902c4c6829d53e3 pushed
from verified remote3938fb7f to the same topic/PR392, no lease/force/rebase.
Local and PR head matched5cfa8e53 with clean worktree after source publication.
This final publication receipt/state reconciliation is metadata only and will
be normally committed/pushed on that topic; exact final head is recorded in PR
body and final handoff rather than self-referencing this commit.
PR remains open/base main74617981. No merge/issue closure or independent Pass.
No CI watch; unreported/incomplete checks remain pending. Resume ID
3a36c179-e1e3-4332-9c33-fa947262fd79.
