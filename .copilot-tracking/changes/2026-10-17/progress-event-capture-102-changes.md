<!-- markdownlint-disable-file -->
# Changes: progress-event-capture-102

Task 102. Date 2026-10-17. Full approved plan scope. Implementation active.
Plan/details same dated slug; research Ready; one critique Complete/Revise,
PC-001/002/003 directly resolved before implementation. Original #390 Review
unchanged. P01 starts controlled writers then consumer; P02 proof/docs follows.

## Opening State

Clean supplied branch/base verified before artifacts. Source unchanged until
this phase. No blockers. No UI, finance, infra or other worktree reads.
Baseline 50 tests passed after missing-distribution installation via pip.

## P01: Capture and consumer

P01-T01/T02 complete. Existing returns stream now captures actual advance and
precise return/reopen boundaries, with actual work-order versions. All handoff
states use registered actor, source/owner, exact state timestamp and append
version. The shared controlled scope preserves pending audit prefixes and
quarantines failed writes before recovery. Quality histories add explicit
per-evidence-version event dictionaries; active records, staleness, contributor
independence and quality's existing rollback/committed-outcome scope remain.

Report recognizes exact dictionary kinds, legacy minute bounds and
per-record quality acceptance/handover pairs; all invalid/missing boundaries
remain null, with no cross-version pairing. Later supersession cannot rewrite
an earlier as-of answer. Every measured collection shares the audit trust gate.
Whole-home actuals remain unknown. Forecast algorithm/export semantics retained.

### Immediately relevant plan refinements

Shared CommittedOutcomeError is also the public QualityOutcomeError alias,
retaining the existing HTTP 503 outcome=committed handler without server edits.
Added one existing issue102 HTTP test to prove this with an actual committed
offer, not a mocked exception. Test ownership amended in plan/details. Existing
quality/procurement recovery test changes only the advance logger expectation
to its new shared-scope module. No test removed, bypass or exception suppression.
One critique only, no user decision needed.

## P02: Validation and documentation

Actual combined history/domain guards: 356 run, 319 pass, 37 opt-in/backend
skips. Latest source-specific checks: 67 run, 66 pass, one JSON-only skip.
Actual task-owned loopback MSSQL writer and HTTP consumer: 24 pass, including
second writer, failed recovery, SQL rollback and post-COMMIT exact-once events/
audit across retry and separate connection/restart. Existing API workflow/
resident/role/finance/stock guards: 67 run, 66 pass, one existing skip.
Core/API configured Ruff/format/mypy pass (116/55 files typed).
Initial API image built and 35 installed-source domain/HTTP tests passed as
UID/GID10001 with read-only root and dropped capabilities. Final source
definitions/validation refinements require final rerun/rebuild before Review.
Task-owned SQL container progress102-8f7a5abbc2 loopback32815, UUID databases
retained. Startup receipt initially failed import while executing the external
session helper; actual connection/test runs subsequently proved responsiveness.
No shared SQL container used. Docs/KB routes updated; both full upstream
index/log byte prefixes verified unchanged.

## P03: Review and publication

Pending one original Review, maximum two concrete correction cycles.

## Final P02 Evidence and Pre-Review Reconciliation

P02-T01/T02 complete. Final targeted local selection ran 358 tests:
320 passed, 38 existing opt-in/backend-specific or JSON COMMIT-boundary skips.
Actual isolated loopback MSSQL capture plus HTTP report tests: 24 passed.
Existing API workflow/resident/role/finance/stock checks: 67 run, 66 passed,
one existing skip. Configured core/API Ruff, format and mypy pass, 116/55
source files typed. No test deletion, new live provider call or private input.

Final image sha256:46cb809b0753565be782015c9840930324a3dbab4bf244075b492ac0c961c136.
Existing src/check-container.py passed Docker controls, all negative probes
and compatible API entry-point startup. The same image passed 35 installed-
source actual-domain and loopback HTTP tests under read-only root, dropped
capabilities and UID/GID10001. All six changed core module source hashes match
the final installed image. An initial hash check raced its rebuild and failed;
the required post-build comparison passed. Final changes after these runtime
checks are test annotation/documentation only, not production behavior.

Both full upstream KB index/log byte prefixes remain exact, diff whitespace and
state JSON validate. Plan/details/changes match P01/P02 completion and the
HTTP-test ownership refinement. Remaining P03 is Review/publication only.
Follow-ups remain operational/full-history evidence, JSON cross-file crash
atomicity and coordinator integration of quality overlap; none invented as
completed approval. Ready for one original Review of this distinct follow-up.

## Resumed Original Review and Concrete Correction ONE

Owner resumed retained task/session after VM upgrade 22:07 UTC. Verified own
dirty work, original head2267027, no remote topic/PR and stopped own SQL
container. Recovery brief authorizes a one-time rebase of committed own work
onto main74617981 and normal initial push. No other worktree read or changed.

Original Review genuinely continued after its interrupted opening. Execution
Complete, Outcome Defects found: RV-001 later contradictory handoff state left
an earlier numeric wait; actual SQLite-domain probe reproduced 180 seconds
alongside contradictory_handoff_chain. RV-002 post-COMMIT test asserted audit
once but not exact history counts on independent/restarted stores.
This correction ONE targets those two findings only. Original Review and
critique remain unchanged; no second full Review or coordinator Pass.
Planned validation: failing-first RV-001, JSON/SQLite corrected scope, static
checks, own SQL started only for fresh selector and immediately stopped, then
sequential final-source image smoke as production report code changes.

Correction ONE complete: both findings addressed with actual fresh evidence in
.copilot-tracking/changes/2026-10-17/progress-event-capture-102-correction-one.md.
RV-001 failed first with 180 seconds surviving a contradiction, now unknown
only when that contradiction is within as-of. RV-002 now checks exact stream
length/prefix, append version/type and event equality across second connection,
restart and refused retry for ten actual operations including pause entry/exit.
Fresh local 457 run/394 pass/63 explicit skips; actual own MSSQL25 pass; static
checks pass; corrected non-root image48 run/47 pass/one JSON-boundary skip,
controls/negative probes/startup and all six installed source hashes pass.
Only P03-T02 privacy-safe publication/integration remains. Original Review
Complete/Defects found and all original findings are retained, not overwritten.
