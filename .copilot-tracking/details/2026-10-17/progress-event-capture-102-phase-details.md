<!-- markdownlint-disable-file -->
# RPI Phase Details: progress-event-capture-102

Task ID 102. Date 2026-10-17.
Plan: .copilot-tracking/plans/2026-10-17/progress-event-capture-102-plan.md
Research: .copilot-tracking/research/2026-10-17/progress-event-capture-102-research.md

<!-- rpi:phase id=P01 -->
## P01: Capture and consume

Existing append/version dictionaries and SQL save are canonical. No new
transition capability, blanket human approval or reconstructed event.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Controlled writers and truthful commit boundary

Targets: change_provenance.py reusable controlled scope using stock current
actor/transaction guard and quality snapshot-based committed-error pattern;
store.advance; workflows return/reopen and non-metadata handoff writes.
Keep offer/accept metadata and expected-version contracts while applying
truthful failure handling. Keep existing public method signatures.
Quality targets only append dictionaries in submit/_qmove/supersession;
preserve _quality_operation, active_records, independence and staleness.
Append source references are internal exact evidence record/version pointers,
not claims of external verification. Completion: actual writers append one
new record and failed transactions append none, with auditable real actor.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Consumer dictionary and unknowns

progress.py recognizes exact new advance kind and legacy return/reopen.
Use bounded legacy minute precision on stage histories too, preserve version/
append order and reject ambiguous elapsed intervals. Last exit remains unknown.
Consume nested quality histories using explicit evidence_version, record index,
history append version and checklist source; map acceptance/handover independently
of stage or case closure. No inferred whole-home accepted count. Preserve
forecast algorithm, schema and semantic CSV parity, raw identity redaction.
Completion: exact times only where both actual boundaries support them.

PC-001: project quality events into history.events after independent returns/
handoff streams; add history.accepted_handovers with source/end_source,
evidence_version, accepted_at, handed_over_at, elapsed_seconds and historical
status. Pair only same quality record/evidence version, valid append sequence.
Retain historical observed pairs after supersession; report superseded_at only
when its event is within as-of. Future replacement cannot rewrite earlier
answers. Legacy prefixes and malformed/contradictory boundaries yield null
clocks, never cross-version pairing. Whole-home actual denominator stays null.
PC-002: include accepted_handovers in audit False/None suppression and CSV
assertions; no trusted numeric interval may survive the existing trust gate.

<!-- rpi:phase id=P02 -->
## P02: Proof and docs

<!-- rpi:task id=P02-T01 -->
### P02-T01: Actual domain/backend tests

Owned test_progress_event_capture.py with small DATA copy and registered
fictional staff. Set original starting state as explicit nonhistorical fixture;
never insert past events to prove new capture. Create genuine existing
package/delegation/commitment fixture and issue/book order before advance.
Use return_case to enter/leave supported earlier stages and reopen on an
explicit initial closed case. Quality actual independent recorders and existing
resident fixture. Test refused actors/guards and source privacy.
Inject failures in save and audit append, preserving original errors and prior
audit. On SQL force second writer before save and a post-COMMIT _sync fault;
check separate connection, retry/restart and exact count. MSSQL unique task-owned
container and databases, loopback only, no shared container/credential reuse.
Run progress/history, workflow/quality/resident, finance/grant/stock/procurement
and API report guard suites; core/API Ruff/format/mypy.

PC-003: parameterized SQLite/MSSQL matrix for both metadata-backed and shared
scope callers: queue legitimate prior audit, fail save/audit insertion and
recovery readback, assert quarantine before outer exit, original error retained,
prior audit once, failed event/success absent on second connection/restart.
Clean retry must append exactly once. Keep post-COMMIT failure distinct.

Implementation-time local refinement: retain QualityOutcomeError as the public
alias of the shared committed-outcome error, so the existing HTTP 503
outcome=committed handler needs no parallel server.py edit. Add one tightly
coupled HTTP test to existing issue102 test_progress_report_api.py to prove
actual post-COMMIT offer failure reaches that existing contract on SQLite and
MSSQL. This amends test ownership; no removed tests or new production surface.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Docs and image

Update core README and existing programme journey synthesis, KB route and
append-only log; preserve exact upstream log prefix. API guide only if required
to correct event boundary wording. Build src/API image and run non-root loopback
health plus installed-source event/report smoke. No browser because no web edit.

<!-- rpi:phase id=P03 -->
## P03: Review/publication

<!-- rpi:task id=P03-T01 -->
### P03-T01: One Review

Fresh one complete post-implementation review with supplied context; retain
all findings and original verdict, maximum two concrete correction cycles.
No repeated full Review or claimed coordinator Pass. Persist exact evidence.
Original Review now Complete/Defects found; correction ONE resolves RV-001
handoff lifecycle fail-closed waits and RV-002 exact post-COMMIT event count/
version checks on second connection/restart/retry, including return/pause exit/
reopen. Same owned method matrix, no expanded authority or new transition API.

<!-- rpi:task id=P03-T02 -->
### P03-T02: Publication

Resolve fresh gh api user; local privacy-safe noreply author and committer.
Own files only, required coauthor trailer. Push supplied topic and open main
PR with Refs #102, exact remaining criterion, evidence/limitations and quality
overlap. Owner recovery explicitly authorizes one own-branch rebase after
committing retained work onto main74617981; preserve source/test patch parity
and exact upstream KB prefix. Normal initial push if remote branch absent.
Never merge, close issue or force-push. Record exact head/PR.

Current owner exception 2026-10-17 22:28: rebase own topic onto fresh
main943febc23e99e397724cb81d2580f781b91e13f7 after merged sensor #393.
Allow only own-topic force-with-lease exact remote
92c3bae39c09d68dd72f2fe82c5ed40f0fdcfb2a. Preserve both Store imports and all
sensor export/pre-dispatch/current-generator checks, both README sections and
exact upstream KB prefixes. Prove unchanged deltas and execute combined event/
sensor status/document/chat/map regressions. No new full Review or correction
cycle. Existing SQL25 receipt remains historical for unchanged persistence.
