<!-- markdownlint-disable-file -->
# Review: progress-event-capture-102

Task 102. Date 2026-10-17. Execution: Complete. Outcome: Defects found.
One original Review of this distinct implementation follow-up to merged #390.
No re-adjudication or mutation of #390's Review.

## Opening Review State

Complete supplied boundary: prospective existing stage, handoff and quality
writers, timestamp/version/source/owner mapping, atomicity, failure truth,
legacy precision, unknowns, as-of/period, report privacy and preserved forecast/
export behavior. P01/P02 reconciled in plan/details/changes; P03 publication
is pending, not falsely checked complete. One critique Complete/Revise with
PC-001/002/003 direct dispositions. No initial blocker or human approval claim.
Review is source-read-only; only this canonical review record may be written.

## Artifact Set

* .copilot-tracking/research/2026-10-17/progress-event-capture-102-research.md
* .copilot-tracking/plans/2026-10-17/progress-event-capture-102-plan.md
* .copilot-tracking/details/2026-10-17/progress-event-capture-102-phase-details.md
* .copilot-tracking/reviews/plans/2026-10-17/progress-event-capture-102-plan-critique.md
* .copilot-tracking/changes/2026-10-17/progress-event-capture-102-changes.md

## Evidence Available

Final local targeted 358 run/320 pass/38 explicit skips; actual task-owned
MSSQL24 pass; existing API guards67 run/66 pass/one skip; core/API configured
Ruff/format/mypy pass. Final non-root API image controls/negative probes/startup
and 35 installed-source domain/HTTP tests passed, six core source hashes match.
Full upstream KB index/log prefixes preserved. No external/live acceptance.

## Interrupted Execution and Continuation

SIGKILL interrupted the original Review after this artifact was created, before
any completed findings were recorded. Owner resumed this same session at
22:07 UTC after VM upgrade. The parent checked retained status/head/remote and
the canonical recovery brief, then continued the remaining original comparison
directly. No second Review, new critique or coordinator judgment was run.
Pre-pause results above are historical executed receipts, not freshly rerun
results. Ephemeral /tmp logs did not survive the VM restart; the changes record
and retained conversation contain their actual commands/results.

## Plan-to-Change and Critique Assessment

P01 instruments the three actual stage writers, metadata-backed offer/accept
and other handoff states without creating a generic transition API. Quality
history adds append/evidence/checklist versions and source/owner/actor snapshots
while retaining active-record, resident, safety and contributor-independence
guards. P02 tests actual methods with fictional registered staff and supplied
prerequisites, not fabricated history alone. No finance, server/web or setup
source edits. P03 publication remains pending.

PC-001 quality projection/as-of/supersession and PC-002 audit suppression are
implemented and exercised. PC-003 failed recovery with pending prior audit is
exercised on both metadata/shared paths. A remaining exact event-count gap in
the post-COMMIT proof is RV-002 below. The shared committed-error public alias
and tightly coupled HTTP test preserve the existing handler contract; changing
the existing recovery test's logger expectation is justified, not weakening
its assertions. No removed test or unsupported user-owned decision found.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: A later contradictory handoff state leaves an earlier measured wait

Source: src/core/src/zava_forward/core/progress.py, history handoff loop and
return. The loop marks handoff_valid false on an invalid lifecycle transition
but does not invalidate wait dictionaries already emitted earlier in the loop.

Actual resumed Review probe: use the actual SQLite offer/receive/accept domain
test, copy its resulting history, then append a contradictory version4 Received
at 10:04 after version3 Accepted at 10:03. At 10:10, history reports
contradictory_handoff_chain yet still returns Accepted elapsed_seconds=180.
This contradicts the requested explicit unknown for contradictory events and
the new quality collection's fail-closed consistency policy.

Smallest correction: after validating the whole as-of lifecycle, null affected
handoff waits when its chain is invalid. Keep an earlier as-of before the bad
event measured, preserve all source append versions and raw history, and test
JSON/CSV and audit-gate semantics. No repair/reordering/backfill.
Destination: rpi-implement, parent-owned concrete correction ONE.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Post-COMMIT proof asserts audit counts but not exact event counts

Source: src/core/tests/test_progress_event_capture.py,
test_sql_postcommit_sync_failure_is_committed_once_second_connection_and_retry.
The seven actual operations verify audit count=1, cleared pending/touched,
restarted ledger and refused retry, but never assert the new history's exact
event count/version on the original and restarted stores before/after retry.
Return/reopen are covered by rollback tests, not this committed-refresh case.

The implementation looks structurally sound, but the exact caller requirement
is event AND audit once, not audit as a proxy. A duplicate appended dictionary
could pass this test. This is a bounded acceptance-evidence defect, not a
claim that an observed duplicate already exists.

Smallest correction: parameterize the existing method with expected stream,
prior/after length, next append version and event kind for each operation;
assert exact new event once on independent/restarted connection and unchanged
after retry. Include controlled return/reopen (and supported pause path) in the
same method. Run SQLite and actual task-owned MSSQL, retaining all assertions.
Destination: rpi-implement, same concrete correction ONE.

## Completed-Work and Residual Assessment

Forecast implementation is unchanged, CSV serializes the same semantic report,
current authorized cohort and roles are retained. No past event, prior audit
or source precision is rewritten. First entry, last exit, absent general
forward/closure/resume capability and whole-home accepted-handover actuals stay
unknown; quality pairs mean historical per-measure work acceptance and
resident-told handover, not resident consent or financial completion.

JSON cross-file process-crash atomicity remains explicitly unavailable; SQL
commits event/case/audit together. Operational authority, forecast calibration,
complete historical data, human/WCAG/Azure/live-AI acceptance and independent
coordinator final-head judgment remain distinct follow-ups, not active defects
or approvals. quality.py overlap with parallel #88 is declared for integration.

## Outcome and Routing

Execution Complete. Outcome Defects found. Two Medium findings route once to
implementation; no decision/research blocker. Preserve this original verdict
and both findings unchanged after corrections. At most two concrete correction
cycles remain authorized, no second full Review. Publication follows concrete
fixes and their actual validation. Owner's 22:07 recovery direction separately
authorizes committing then integrating this own branch onto fresh main74617981;
that integration was not represented as already performed in this Review.
