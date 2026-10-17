<!-- markdownlint-disable-file -->
# Authorized issue88 integration onto merged quality PR387

## Authorization and Immutable Evidence

Coordinator authorized own-branch rebase of PR392 onto freshly fetched main
3f544fb9cda2c51b219db2cc8368c7525bbe0c86, with force-with-lease limited to
expected remote a9a5f554151336f6e617fbcee35033234813c6e5. Clean own worktree
and expected remote were verified before rebase. No other worktree/private data,
Azure writes, merge, issue closure or independent Pass is authorized.

All seven original resident-update-remedy-controls-88 RPI artifacts remain
byte-identical to the expected remote, including original state/Review/critique.
No new full Review or critique. Original Review remains Complete / Residual work,
RV-001 Low broader governance routing, not an unresolved exact remedy criterion.
Original Review SHA256:
204aab7fa36e86feae5b5f76a2107e8e7a2655a6b11a6d2113a3c231ea008e99.
Original critique SHA256:
70fad5b641605fd83c7bc490fcac4c926c9cfcc1d06ba4eaeb63b297c631e01d.

## Rebase and Source Parity

Executed git fetch origin main, verified full main ID above, then git rebase
origin/main. Sole textual conflict: append insertion in docs/reference/log.md.
Resolution retains complete latest-main log followed by all original issue88
entries. Latest upstream exact byte-prefix SHA256:
c1e858f50b2d3e55565c1aa6cc78c1b2b43c82086ccfea17b2d4d9b31ab75d52.
All existing index routes and both component guide sections survive.

Rebased implementation 583ab213 and bookkeeping 89ce541f. Compared
git diff --unified=0 added/removed lines for all fourteen changed src paths
against old base/expected remote and main/rebased head: exact source/test/guide
patch-line parity, ignoring relocated context only. Original seven RPI artifacts
are byte-identical. Resident app.js/panels.js bytes unchanged from old head;
quality.py/assistants.py/ops.js bytes exactly latest main. No runtime resolution
or correction was made. Auto-merged server retains resident-specific committed
409 and outer QualityOutcomeError committed 503 handlers. Auto-merged resident
tests retain quality's stricter replacement refusal and all resident assertions.

## Integration Execution State

Combined validation complete. No application source fault established; zero
application correction cycles used. Combined run: 499 tests, 445 pass and 54
existing opt-in/JSON-only skips; actual resident browser: one pass.
Actual MSSQL final replay: 38 run, 37 pass and one explicitly SQLite-only skip.
Full configured core/API Ruff/format/mypy and integrated image controls pass.
This evidence is recorded before the authorized expected-lease push.

## Validation Plan and Evidence

Run installed-src resident/update/remedy, quality/replacement/current-evidence
assistant, hazard, finance/grants, stale actor/approval and recovery tests together,
plus configured core/API Ruff/format/mypy. Replay actual task-owned loopback
MSSQL negative writer, rollback and post-COMMIT/no-replay tests using small
fictional fixtures and isolated databases. No existing shared server touched.

Changed web bytes: none relative to previously exercised resident head; merged
quality ops bytes unchanged from main. Original fresh-guideline/browser evidence
remains historical, not represented as an integration rerun or WCAG acceptance.
Run actual integration browser journey as additional HTTP/runtime compatibility
evidence if the existing runner is available.

First actual MSSQL replay ran 38 selected tests; 36 methods passed, two errored.
The harness for SQLite-only classes had passed the mutable process environment
instead of a per-store database snapshot, so hazard assistant_connection opened
master and eight registry-change subtests could not find staff. Fixed the
external test transport to pass explicit immutable per-store env; no application
code changed. The other method requires SQLite set_trace_callback/in_transaction;
it passed in the combined SQLite suite but is explicitly skipped on MSSQL.
Resident eleven, quality seven, finance ten, grant five and the other hazard
methods already passed actual SQL on this attempt. Do not label this attempt
successful or confuse harness correction with an application source fault.
Initial container setup also corrected unsupported Path.open(opener=...) to
built-in open before creating the private credential; no secret was output.

## Exact Issue Criteria Mapping

| Exact criterion | Source behavior | Executed test proof and boundary |
| --- | --- | --- |
| Commitment has purpose, owner, due date and basis | src/core/src/zava_forward/core/resident_decisions.py:_res_update_record requires purpose/basis, current eligible named registered owner, aware due_at, expected version and Outstanding/Proposed; history retains old captured snapshot; validate_sql replays validation inside writer transaction | test_resident_decisions: test_complete_update_and_explicit_reassignment_preserve_history and test_incomplete_commitments_dates_and_identity_fail_without_mutation across JSON/SQLite and actual MSSQL; test_followup_writer_rechecks_current_actor_assignee_and_legacy_identity proves registry changes without case-sequence bump refuse. Actual browser creates/reassigns and retains invalid draft. No message-sent/received claim |
| Closing response/package never closes open remedy, defect or charge query | _res_service_close changes only response and response event; _res_remedy_update changes only the separately versioned remedy; workflows/work-order and upstream quality operations retain their separate records, not service-request cascades | test_response_and_remedy_close_and_reopen_are_independent and test_mixed_closure_clocks_survive_unrelated_transitions_and_restart across JSON/SQLite/actual MSSQL. Mixed test closes Complaint response with remedy Open, retains separate Defect/Charge query requests through real order completion, quality handover/returned defect, finance note, case return/reopen and store restart; remedy resolution on Charge query leaves response Open and other requests unchanged. Actual browser closes response, observes Open remedy, resolves/closes/reopens remedy, then reopens response independently |
| Each status keeps its own owner and date | _res_service_open/_response_event record response status_owner/status_at and captured service/redress identities; remedy has owner/at/original opened_at/history. _res_remedy_update preserves original open time, changes own owner/status date/history. Existing order completed_by/completed_at, quality defect owner/raised_at and handover.by/at remain separate. finance._fin_payment_status records own note owner/date/history only | Mixed-clocks test asserts all service records/commitment unchanged after each unrelated transition/restart, checks order completion, quality handover/defect and finance clocks explicitly; independent close/reopen tests retain remedy original/history clocks. test_legacy_confirmation_preserves_unknown_history_and_closed_response and test_actionable_owner_roles_projection_and_captured_identity prove absent original provenance stays null/Unknown, confirmation has only current responsibility and captured identity is not rebound. These run JSON/SQLite/actual MSSQL |

Each of the three criteria has direct local source/test proof, independently of
plan follow-up completion. This is not an independent coordinator acceptance or
full PRD AC-063/BRD AC-089 acceptance.

## Actual Commands and Final Results

Executed from this worktree with existing pip-installed editable src packages.
Application imports are installed packages; PYTHONPATH supplies test helpers only.
No install, uv, mvp path, private data or cloud configuration was needed.

```bash
PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests .venv/bin/python -m unittest \
  test_resident_decisions.JsonResidentDecisions test_resident_decisions.SqlResidentDecisions \
  test_handoff_lifecycle test_handoff_api test_workflows \
  test_finance_match_controls.JsonFinanceChecks test_finance_match_controls.SqlFinanceChecks \
  test_finance_signoffs test_finance_match_api \
  test_grant_lifecycle_controls.JsonGrantChecks test_grant_lifecycle_controls.SqlGrantChecks \
  test_grant_lifecycle_api test_hazard_referral.JsonHazardReferral \
  test_hazard_referral.SqlHazardReferral test_hazard_api \
  test_stock_reconciliation test_stock_reconciliation_api test_quality_procurement \
  test_procurement_api test_role_matrix test_sqlstore test_recovery \
  test_change_provenance test_resident_api test_assistants -q

ZF_RESIDENT_BROWSER=1 PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests \
  .venv/bin/python -m unittest \
  test_resident_api.ResidentApi.test_browser_commitment_reassignment_response_closure_and_remedy_reopen -q

(cd src/core && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy)
(cd src/api && ../../.venv/bin/ruff check . && ../../.venv/bin/ruff format --check . && ../../.venv/bin/mypy)
docker build -q -f src/api/Dockerfile -t zf-issue88-integration:local src
.venv/bin/python src/check-container.py api zf-issue88-integration:local
git diff --check
```

| Check | Actual result |
| --- | --- |
| Combined unittest command | 499 run, 445 pass, 54 existing opt-in/JSON-only skips, 130.018 seconds. Includes upstream test_quality_replacement_uses_only_current_evidence_and_version and test_quality_current_discrepancies_do_not_rely_on_retired_acceptance; no paid assistant call |
| Actual integrated Chromium | One pass, 4.017 seconds; native Enter create/reassign, invalid draft/live feedback, independent close/reopen, reduced motion, widths320/390/1280, off-origin blocked. Unavailable law-store fixture logs Unknown checks, not legal clearance |
| Full configured checks | Core/API Ruff checks pass; 60/22 files formatted; mypy113/54 source files pass |
| Integrated API image/non-root local startup | sha256:8c5bfb4499569008404e018efa229d4a4b83348aacc2659216631981b81b3471; existing hardening/negative probes and compatible startup pass |
| Source/record integrity | Exact original seven artifact byte parity, latest upstream log prefix and all own entries; both route sets preserved; own fourteen src patch additions/removals equal old patch; git diff --check passes |

### Actual MSSQL Command, Transport and Selection

Unique container issue88-integration-3a36c179,
ID10d4aadf59047ac499bf0909a11c9cf54844a2863a750f49da3fe25d8ddccd83,
bound only127.0.0.1:32812. Actual SELECT1 confirmed responsive. Generated password
was in mode0600 external session file, never printed/committed. Existing installed
mssql-python transport uses the same store save hooks as production.

```bash
PYTHONPATH=src/core/tests:src/api:src/api/tests:src/agents/tests \
  .venv/bin/python \
  /home/azureuser/.copilot/session-state/3a36c179-e1e3-4332-9c33-fa947262fd79/files/issue88-integration-mssql.py
```

External harness SHA256:
ce47f2c79637859043af38dbc6002215080a540944c97cf5b087e32ef08d092a.
Resident/finance/grant use existing Mssql* subclasses with UUID databases.
For existing quality/hazard SQLite test classes, harness replaces only their
SqlStore constructor with a MssqlStore subclass mapping each logical SQLite path
to a UUID zf_issue88_integration database and explicit per-store env snapshot;
original seed, actions, fault injection and assertions remain. Multiple opens
share only the same test logical database; separate logical paths stay isolated.
All connections close, databases drop, then master environment restores.
The single SQLite trace-only method is explicitly skipped, not weakened.

Final result: 38 run, 37 pass, one skip, 219.671 seconds.
Selected method names below have test_ prefix in existing test modules:

* resident_decisions.MssqlResidentControls (11): complete_update_and_explicit_reassignment_preserve_history;
  incomplete_commitments_dates_and_identity_fail_without_mutation;
  response_and_remedy_close_and_reopen_are_independent;
  legacy_confirmation_preserves_unknown_history_and_closed_response;
  actionable_owner_roles_projection_and_captured_identity;
  mixed_closure_clocks_survive_unrelated_transitions_and_restart;
  handoff_cannot_create_partial_commitment_or_clear_existing_one;
  followup_writer_rechecks_current_actor_assignee_and_legacy_identity;
  concurrent_followup_writers_one_version_one_success_event;
  followup_audit_insert_and_recovery_faults_never_replay_success;
  followup_postcommit_sync_fault_is_truthful_and_not_replayed.
* quality_procurement.SqlFlows (7): quality_sql_postcommit_refresh;
  quality_sql_actor_and_stale; quality_sql_failures;
  quality_legacy_repeated_recorders; quality_replacement_dependencies;
  quality_remediation_and_reinspection; quality_identity_history.
* hazard_referral.SqlHazardReferral (4 pass/1 skip):
  authority_changes_rechecked_at_transaction_for_caller_and_destination;
  failed_writes_preserve_prior_pending_audit_and_original_error;
  recovery_read_failure_quarantines_hazard_and_keeps_prior_audit;
  interleaved_emergency_hold_blocks_every_guarded_commit;
  transaction_reload_and_writer_lock_cover_validation_to_commit (SQLite
  set_trace_callback/in_transaction assertion, executed on SQLite, skipped here).
* finance_match_controls.MssqlFinanceChecks (10):
  audit_insert_then_early_discard_read_failure_never_flushes_success;
  persistent_discard_read_failure_never_flushes_success;
  failed_operation_preserves_prior_legitimate_pending_audit;
  failed_lock_exit_keeps_original_error_and_prior_audit_for_retry;
  save_refusal_keeps_original_error_when_internal_discard_read_fails;
  fresh_permission_without_case_sequence_change_and_inside_save;
  competing_store_write_refuses_stale_approval_without_success_audit;
  two_concurrent_acceptances_cannot_spend_the_same_budget;
  oid_revocation_without_case_sequence_change_refuses_write;
  sql_audit_failure_rolls_back_state_and_success_event.
* grant_lifecycle_controls.MssqlGrantChecks (5):
  legacy_preparer_is_reloaded_inside_grant_and_finance_transaction;
  transaction_rechecks_designation_change_and_clock_expiry;
  rowversion_conflict_cannot_approve_stale_grant;
  grant_and_application_audit_insert_and_recovery_failure;
  application_authority_evidence_history_and_separation.

Actual sys.databases readback after replay found no user databases left. The
37 passing methods cover negative concurrent writers, current registry without
case bump, stale approvals, hazard-before-COMMIT race, audit insert and
first/persistent recovery failure, prior audit prefixes and exactly-once committed
events after synchronization failures. No exception handling or success-shaped
fallback was added to application code. Other MSSQL tests are not claimed run.

## Cleanup and Authorized Publication

Verified exact integration container ID before removing only that container,
own zf-issue88-integration:local image tag and generated external SQL credential.
No user databases remained before removal. Original session's other resources
and all other worktrees remain untouched. External nonsecret test harness is
retained in this resume session for reproducibility, not an application artifact.

Before publication gh api user freshly resolves id8036360/loginjmservera;
repository-local author/committer email uses the returned ID/login noreply form.
Remote was rechecked as exact authorized expected lease
a9a5f554151336f6e617fbcee35033234813c6e5 after all checks and cleanup.
New evidence/KB changes are a normal Conventional Commit with Copilot trailer.
The sole history rewrite is the expressly authorized rebase and push:

```bash
git push --force-with-lease=refs/heads/fix/resident-update-remedy-controls-88:a9a5f554151336f6e617fbcee35033234813c6e5 \
  origin HEAD:refs/heads/fix/resident-update-remedy-controls-88
```

If the expected lease changes, publication must fail rather than widening the
lease. Final exact head will be the published integration commit, verified
against local HEAD, remote branch and existing open main-targeted PR392.
Original RPI records stay immutable; this separate integration state records the
user-selected stopped endpoint. No merge, issue closure or independent Pass.
Resume ID: 3a36c179-e1e3-4332-9c33-fa947262fd79.

## Publication Receipt and Moving Main Ref

Authorized exact-lease push succeeded at
07f988c78daf1fa8107b541a13f1679cdbb4d83f. Only the two authorized old commits
were rebased, followed by own integration evidence. No application source fix.

A final prepublication integrity script asserted against the mutable
origin/main ref, which had advanced concurrently to
226702779e57e490cb10dc06ab014760c7d8a761 (merged #390/#102) while local
validation ran. That prefix assertion failed; the shell command's separate
publication chain still ran. This was not an application failure or failed
expected-lease push. The immutable authorized base remained
3f544fb9cda2c51b219db2cc8368c7525bbe0c86 throughout this branch's integration.
Fresh explicit pinned-base revalidation then passed: original seven artifact
bytes equal expected old remote, exact authorized-base log prefix retained,
all own entries preserved and authorized base is an ancestor of this head.
Earlier whole source patch parity was likewise proved against the pinned base.
This tooling/ref race is retained as failed evidence, not relabelled a pass.

No additional rebase or new main source was imported after the authorized
integration. #390/#102 progress/store/API compatibility and any newer main
integration remain coordinator-sequenced work; the combined 499/38/browser/image
receipts apply to the pinned PR387 base, not newly arrived #390. A subsequent
normal evidence-only commit records this distinction without another force push,
source correction, full Review or change to original RPI artifacts.

## Residual Governance and Stop Boundary

RV-001 stays separately routed to planning parent/repository owner at next #81
backlog triage to identify an existing separately owned governance item or assign
one for Legal/Housing/Complaints lease/scope/age-band policy. Those specialists
retain approval; thresholds/authority are not invented. No runtime implementation
gap may be hidden by this exclusion. Independent final-head acceptance remains
coordinator-owned; stop at clean published exact head/resume ID, no merge/closure.
