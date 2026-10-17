<!-- markdownlint-disable-file -->
# RPI Plan: progress-event-capture-102

## Task Metadata

Task ID 102. Date 2026-10-17. Planning: Ready after direct critique corrections.
Details: .copilot-tracking/details/2026-10-17/progress-event-capture-102-phase-details.md
Critique: .copilot-tracking/reviews/plans/2026-10-17/progress-event-capture-102-plan-critique.md

## Executive Summary

Capture prospective controlled progression in existing versioned histories,
and consume independent quality acceptance/handover events without inventing
missing history. Retain #390 forecasts and export contracts.

### What You May Not Know

There is only one actual forward-stage writer, final checks to install booked.
Pause/resume and full-home completion have no general forward API. A precise
recorded return into pause is measurable only when an actual exit is recorded.
Quality handover is per measure, not financial or whole-home completion.
JSON atomically replaces case/event state but cannot atomically commit its
separate audit file across process crashes. SQL does commit both together.
quality.py overlap with parallel #88 requires coordinator integration.

## User Decisions and Requirements

* Full ordered Research, Plan/one critique, Implement and one original Review.
* Fresh supplied branch/base, distinct follow-up to merged #390; criterion one.
* Preserve UTC/as-of/role/filter/export semantics, legacy precision and unknowns.
* Current registered fictional staff and legitimate domain methods, no bypasses.
* Atomic successful writes and exactly-once events/audit after rollback/retry
  and committed-refresh failure; never claim failed writes succeeded.
* Actual JSON/SQLite/task-owned loopback MSSQL and core/API guard checks.
* Maximum two concrete post-Review corrections; retain original findings.
* Own-branch commit/push/main PR Refs #102, no close, merge or history rewrite.
* Owner recovery exception: commit retained work, then one own-branch rebase
  onto main74617981 before normal initial push; preserve source/test patches.

## Goals

Trustworthy prospective events and bounded durations using existing contracts.

## Scope and Non-Goals

Scope: core store/workflows/change_provenance/quality/progress, owned test file,
direct docs and KB. No web/API handler, finance, infra, telemetry service,
history backfill, authority creation, Azure/private data or live AI.

## Functional Requirements

* All three stage writers append explicit advance/return/reopen dictionaries
  to existing returns stream; old dictionaries remain byte-for-byte unchanged.
* Existing handoff lifecycle carries registered actor, owner, source/version,
  precise server time and append version, preserving metadata-required offer/
  accept and sender accountability.
* Quality submission/state/supersession histories receive prospective version,
  event kind, precise server time, actor/owner and evidence/checklist source.
* Report consumes these exact dictionaries, with valid known intervals only.
  Existing legacy records never become measured through current snapshots.
* Shared controlled scope quarantines failed SQL pending audit and distinguishes
  committed-refresh error from rejection. Existing quality/hazard truth retained.

## Non-Functional Requirements

No new service/storage table; no broad catches that disguise errors. Preserve
current registered actors and writer-transaction revalidation. Role redaction
withholds raw actor, owner, source text, reasons and commercial/resident detail.
New clocks use microsecond UTC. Versions/append order authoritative, legacy
minute uncertainty bounded. No cross-stream ordering claim.

## Acceptance Criteria

* Actual domain forward/return/reopen/pause and offer/receive/accept across
  JSON, SQLite and MSSQL append once with correct types/version/provenance.
* Actual independent quality submit/accept/handover produces per-measure
  event evidence and known duration; stale replacement remains independent.
* Inject prewrite/audit failures: state/event rollback, no success audit,
  prior audit retained; retry records exactly once.
* SQL second-writer post-COMMIT sync failure: explicit committed error, exact
  event/audit count on second connection/restart and rejected retry.
* Mixed minute precision, malformed/contradictory events, missing periods and
  unrecorded legacy transitions remain unknown. Existing API CSV parity stays.

## Sources

.copilot-tracking/research/2026-10-17/progress-event-capture-102-research.md C1-C7.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Capture and consume existing events
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Controlled writers and truthful commit boundary
<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Exact consumer dictionary and unknown preservation

<!-- rpi:phase id=P02 -->
### [x] P02: Prove and document
Dependency: P01.
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Actual-domain backend, failure and regression checks
<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Component/KB documentation and image smoke

<!-- rpi:phase id=P03 -->
### [x] P03: One Review and publication
Dependency: P02.
<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: One original Review, bounded concrete corrections
<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Privacy-safe commit, push and main PR

## Test Ownership and Locked Candidate

Canonical additions: src/core/tests/test_progress_event_capture.py plus one
actual post-COMMIT HTTP test in existing src/api/tests/test_progress_report_api.py;
maximum 24 distinct semantic/regression test methods, backend subclasses reuse
the same contract. Existing tests may receive tightly coupled expectation
updates only when explicit behavior changes require them. Removals: none.
No generated targets. Semantic tests exercise actual public domain methods;
regressions cover legacy unknowns, UTC precision, report/export roles and
failure boundaries. Existing fixtures remain unchanged.

## Dependencies

Parent #100 hierarchy only, no explicit dependency. #390 merged at supplied
base. #88 and #391 parallel exclusions; actual quality overlap declared.

## Critique Disposition

One critique executed, verdict Revise. All findings directly incorporated:

| Finding | Disposition | Resolving plan |
| --- | --- | --- |
| PC-001 | Resolved | P01-T02 explicit quality events/accepted_handovers shape, same-version pairs, supersession/as-of and legacy unknown rules |
| PC-002 | Resolved | P01-T02 and P02-T01 apply audit gate to accepted_handovers including CSV |
| PC-003 | Resolved | P02-T01 combined save/audit and recovery-read failures, preserved prefix/original error, exact-once retry/restart |

## Follow-Up Items

* Operational approval, complete historical capture and JSON cross-file crash
  atomicity remain separate evidence/architecture work, not claimed here.

## Handoff

Implementation creates .copilot-tracking/changes/2026-10-17/progress-event-capture-102-changes.md.
P03-T02 sensor integration complete onto main943febc2; published main PR #394
continues on own branch with Refs #102. Combined301 run/274 pass/27 skips and
core/API/agents statics pass; exact unchanged deltas/upstream prefixes verified.
No blocker or human approval inferred. No second critique or Review.

Resumed state: original Review Complete/Defects found; P03-T01 correction ONE
resolved RV-001 lifecycle fail-closed handoff waits and RV-002 exact event
counts/version proof for committed refresh/retry/restart. Original Review
retained. Actual correction evidence complete; privacy-safe publication done.
Owner-authorized one-time integration onto main74617981 preserved complete
source/test patch and upstream KB prefixes. Next independent coordinator
final-head judgment, not another RPI Review or automatic merge/issue closure.
2026-10-17 22:28 owner authorization permits own-topic force-with-lease only
against exact remote92c3bae39c09d68dd72f2fe82c5ed40f0fdcfb2a. Preserve sensor
closed export/current-generator admission and event capture/recovery; combined
runtime/static checks follow the additive Store import conflict resolution.
Original Review and correction ONE remain unchanged. SQL evidence historical
unless persistence behavior changes; no such change required by import union.

22:42 independent final-gate Revise: one Medium document operational-failure
audit regression. Correction TWO LAST authorized cycle resumes P03-T01/T02
only for truthful post-rollback failure/rejection, original-error retention and
exact pending-audit/committed diagnostics. Original Review/critique/correction
ONE immutable. No new full Review. Actual MSSQL and full core checks required
for this shared failure-path change; maintain all sensor/legacy boundaries.

Current final state: correction TWO complete and integrated onto merged
resident mainbcb4871b under owner's moved-main authorization. Both SQL recovery
guards retained; exact own deltas and upstream KB prefixes proved.
Full core942/847 pass/95 skips, combined349/294 pass/55 skips, actual MSSQL35
pass, final non-root image94/92 pass/two skips and configured statics pass.
P03 evidence complete; publish existing PR #394 with exact7fda223a remote lease
for own rebase only. Independent coordinator final gate outstanding.
No third defect cycle, new Review, merge or issue closure.
