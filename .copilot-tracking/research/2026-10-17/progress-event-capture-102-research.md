<!-- markdownlint-disable-file -->
# Task Research: progress-event-capture-102

Date: 2026-10-17. Researcher: RPI parent. Status: Complete.

## Research Brief

Investigate all controlled progression writers and existing append-only audit,
version and persistence contracts for the remaining first criterion of #102.
Audience: implementation and independent integration review. Output mode:
convergence. Scope: src core transitions, progress consumer and dependent tests.
Non-goals: forecast/export redesign, UI, parallel #88/#391, retrospective
history reconstruction, real authority, paid AI, Azure or private data.

## Research Parameters

Focused posture, selected for the caller's bounded engineering follow-up.
Evidence root: .copilot-tracking/. Research is source-read-only. No external
research needed. Starting areas: store, workflows, continuity, quality,
progress, SQL/MSSQL persistence and actual domain tests.
Caller limits: one original Review, at most two concrete correction cycles.

## Extension Registry and Provenance

Repository instructions and component guides selected for source/evidence.
rpi-research selected for three ordered evidence waves; rpi-plan,
rpi-implement and rpi-review deferred until their phases. Web skills skipped:
no web scope. Specialist delegation skipped for the continuous writer trace.

## User Participation and Research Decisions

Caller explicitly requests full ordered automatic execution and publication.
No interactive intake required or available. Distinct follow-up to merged
#390 at 226702779e57e490cb10dc06ab014760c7d8a761; original Review immutable.

## Scope and Success Criteria

Prospective events must share successful controlled transactions, preserve
append/version order and source/owner provenance, and be exactly once across
failure/retry/restart. Unknown legacy intervals remain unknown. Verify actual
domain methods on JSON, SQLite and task-owned loopback MSSQL, including rollback
and committed refresh failure. Forecast/export semantics unchanged.

## Task Research Requests

Q1: Which actual writers change progression, pause and handoff/handover state?
Q2: Which existing transaction/history contracts can capture their events?
Q3: Which consumer gaps prevent trustworthy prospective durations?
Q4: Which tests expose missing capture, contradictory history and commit truth?

## Direction Controls

No historical backfill or audit edits. Preserve role/approval guards, quality
active-record staleness and independence, unrelated domain guards. Actual
quality.py overlap with #88 must be declared. Use installed src worktree venv,
pip, never uv. No merging, rebasing, closing or force pushing.

## Prior Knowledge Gate

Read original, addendum opening/exercise boundary, KB index/memory and merged
original #390 Review. Supplied partial-coverage claims require source verification.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inline inventory found only advance, return_case and reopen_case mutate case
stage. Bulk edits explicitly whitelist non-stage fields. Quality lifecycle is
independent; handoff acceptance transfers ownership, not accepted work.
Reflection: instrument actual writers, not a hypothetical generic stage API.

#### Wave 2: Deeper

Traced SQL save, touched snapshots, pending audit, stock actor validation,
quality committed-outcome detection and JSON rollback. Existing returns list
is append/version ordered; forward capture is absent. Return/reopen use minute
precision. Handoff offer/accept have source-version metadata; other handoff
states have precise times but no source or actor snapshot. Quality history has
neither versioned actor/source provenance nor report consumption.
Reflection: extend existing history dictionaries and a shared controlled scope
at the existing change-provenance boundary; do not add storage or service.

#### Wave 3: Contrarian

Challenged current-snapshot reconstruction, sorting legacy timestamps and
last-event-to-as-of assumptions: all are unsafe. No writer exists for arbitrary
forward stages, case closure or pause resume. A pause can be prospectively
entered by legitimate return, but absent resume remains unknown. Accepted
measure handover does not establish whole-home completion. JSON has two files;
atomic case/event replace is available, but cross-file crash atomicity is not.
SQL owns state/event/audit in one transaction. Existing quality post-COMMIT
tests explicitly force a second writer and failed sync; reuse that test shape.
Reflection: retain unknown last exit and whole-home actual denominator; report
actual per-measure acceptance/handover pairs only, never current-state actuals.

### Parent Synthesis and Disposition

Accepted C1-C7. Reject a new telemetry service or generalized stage transition.
Select minimal existing-history extension with explicit new event dictionary,
precise UTC, current registered actor validation and versioned source locators.
Quality overlap: quality.py submission/history/_qmove/handover paths may overlap
parallel #88 resident updates; coordinator integration required, no #88 writes.
Another cycle not needed: actual writers and material alternatives covered.

## Evidence Log

| ID | Finding | Source |
| --- | --- | --- |
| C1 | Only three controlled stage writers; advance lacks structured history | src/core/src/zava_forward/core/store.py:502; src/core/src/zava_forward/core/workflows.py:99 |
| C2 | Offer/accept append with source/version and caller-version check | src/core/src/zava_forward/core/change_provenance.py:57; src/core/src/zava_forward/core/workflows.py:159 |
| C3 | Other handoff states precise but not failure-scoped | src/core/src/zava_forward/core/workflows.py:215 |
| C4 | SQL state/audit transaction, snapshots advance before optional sync | src/core/src/zava_forward/core/sqlstore.py:545 |
| C5 | Registered actor rechecked inside writer; quality committed outcome pattern | src/core/src/zava_forward/core/stock.py:16; src/core/src/zava_forward/core/quality.py:74 |
| C6 | Quality current/superseded evidence and independence retained | src/core/src/zava_forward/core/quality.py:47; src/core/src/zava_forward/core/quality.py:149 |
| C7 | Consumer returns-only stage map and explicit legacy precision | src/core/src/zava_forward/core/progress.py:55; src/core/src/zava_forward/core/progress.py:205 |

Baseline actual checks: 50 progress/handoff/change-provenance tests passed.
Missing source distributions first failed ModuleNotFoundError; installed
core[dev,sql], agents[dev], api[dev] using pip in this worktree's .venv.
No external evidence or private data used. Inline continuous trace; no workers.

## Findings, Alternatives and Decision State

Use existing returns for all three explicit stage event types, retaining old
return/reopen shape. Version nested quality histories and consume actual
acceptance-to-handover pairs. Bound legacy minute events in append order,
never infer new precision from current records. Preserve report privacy and
forecast/export parity. JSON process-crash cross-file audit atomicity remains
a disclosed limitation, not an acceptance claim.

## Planning Readiness

Ready (C1-C7). Research disposition: executed. Source evidence self-check passed.
Automatic parent may advance to Plan/one critique; no human approval invented.
