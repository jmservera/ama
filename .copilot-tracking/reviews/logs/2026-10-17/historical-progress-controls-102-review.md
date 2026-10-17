<!-- markdownlint-disable-file -->
# Review: historical-progress-controls-102

## Scope and Evidence

Task 102. Review date 2026-10-17. Full implemented task boundary: event-derived
progress/history, declared forecast, source-authorized cohorts and CSV exports.
P03 publication remains after Review, not represented as already complete.

* Plan: .copilot-tracking/plans/2026-10-17/historical-progress-controls-102-plan.md
* Details: .copilot-tracking/details/2026-10-17/historical-progress-controls-102-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-17/historical-progress-controls-102-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-17/historical-progress-controls-102-changes.md
* Research: .copilot-tracking/research/2026-10-17/historical-progress-controls-102-research.md

## Opening Review State

Interpreted goal: compare exact issue criteria, source limitations and plan
against executable report contracts and actual evidence once. P01/P02 are
reconciled and available; PC-102-001/002/003 resolved. Initial comparison:
typed normalization, malformed input behavior, timestamp boundaries, cohort
rights, forecast simulation and semantic export parity. Read-only source
boundary; only this Review record may change in this phase. No initial blocker.
No independent coordinator verdict is implied.

## Execution Status

Execution: Complete. One original Review performed in this session by the
parent, directly over the complete supplied boundary. No second full Review
or independent coordinator assessment occurred.

## Plan-to-Change Reconciliation

| Scope | Evidence | Assessment |
| --- | --- | --- |
| P01-T01 | progress.py exact returns/handoff mappings, unknowns, independent clocks, declared simulation and CSV | Implemented; malformed boundary defects RV-001/RV-002 below |
| P01-T02 | Store.progress_report direct staff/default deny, existing `_filtered`, lock refresh; stats/CSV progress mode | Implemented; blank query parsing violates strict report input contract |
| P02-T01 | Two owned fictional test files, no shared fixture/test removals | Valid semantic tests and regressions; blank query and UTC representable-range gaps |
| P02-T02 | 24 focused passes, 6 actual MSSQL passes, core/API static passes, actual non-root image smoke | Executed; image predates final source guards, final rebuild remains required |
| P02-T03 | Core/API READMEs, programme synthesis, KB index/log | Scope/limitations explicit; upstream append-prefix verified |
| P03 | Review/publication and bounded corrections | This Review executes now; publication not yet claimed complete |

## Completed Work Assessment

Exact event kinds and source locators are normalized without narrative parsing,
snapshot clock reconstruction, domain writes or event mutation. Sequential
version and chain/participant checks null invalid durations. Separate lifecycle
states are not collapsed; missing forward capture and accepted-handover actuals
remain explicit unknowns. Stage interval end and censored offer wait definitions
are distinct. Raw actor/source/free text is withheld for all report audiences;
the minimum shared staff report does not grant another role's sensitive fields.
Contractors and unknown roles are denied before cohort access.

The independent-pool forecast reproduces all EXA-009 numerical sensitivities;
declared ready count is hypothetical, not sourced readiness or commitment.
Assumptions, uncertainty, missing inputs, approval status and limits are
visible. No paid provider or new AI service is added. CSV reconstructs the
same versioned semantic object and preserves as-of/cohort/denominators,
definitions/sources/exceptions. Default stats/CSV remain unchanged.

## Implementation-Time Plan and Detail Update Assessment

Retaining UUID local databases and stopped named containers instead of deleting
resources preserves the caller's explicit prohibition. The manual image
positive hardening/app check is a justified validation substitution, not an
executed generic negative-probe suite. Typed test overrides are bounded to
existing migrated untyped boundaries, not new source error suppression.
No scope-changing domain choice, unapproved implementation divergence or
premature resumption after a human blocker found.

## Critique and Material Revision Assessment

PC-102-001 direct default-deny and HTTP boundary applied and tested.
PC-102-002 exact source mappings/unknowns applied, with Completed source-defined
reopen origin and participant consistency. PC-102-003 canonical schema/order/
CSV representation and byte/semantic parity applied. No repeated critique.

## Findings

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: Blank report parameters silently change the requested result

* Scope: P01-T02/P02-T01.
* Evidence: server.do_GET uses default `parse_qs(url.query)`, which drops blank
  values before the progress branch validates input. Actual session probe
  `?report=&as_of=2026-10-10T12:00:00Z` returned 200 legacy stats with no report
  schema. `?report=progress&as_of=2026-10-10T12:00:00Z&ready=` returned 200
  progress/v1 with Forecast Unavailable, rather than refusing the explicitly
  supplied malformed scenario. Repeated blank parameters evade duplicate checks.
* Impact: success-shaped fallback to a different report contract or silently
  dropped assumptions contradicts strict input/denominator/export behavior.
* Destination: rpi-implement, user-authorized concrete correction cycle.
* Smallest action: preserve blank values only for progress detection/validation,
  reject empty/repeated fields, and test both existing report paths. Preserve
  legacy default parsing when no report parameter was supplied.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: UTC conversion overflow escapes malformed-event handling

* Scope: P01-T01/P02-T01.
* Evidence: progress.timestamp catches ValueError only around fromisoformat,
  then calls astimezone(UTC) outside the guard. Actual session probes
  `0001-01-01T00:00:00+01:00` and `9999-12-31T23:59:59-01:00` both raised
  OverflowError. `_events` catches ValueError, not this overflow.
* Impact: a malformed/unrepresentable event time crashes history instead of
  explicit unknowns; an unrepresentable request boundary can escape 400 handling.
* Destination: rpi-implement, same user-authorized concrete correction cycle.
* Smallest action: include UTC normalization inside the guarded conversion and
  map ValueError/OverflowError to the existing explicit validation error.
  Test direct timestamp, event normalization and authenticated API inputs.

## Defects and Routed Findings

RV-001 and RV-002 are directly implementable within accepted scope. No human
domain decision is required for these fixes. They are not grounds to rewrite
events, broaden scope or rerun a full Review.

## Plan Follow-Up Assessment and Residual Work

Complete source-authorized forward-event capture is outside this read-only
report task: current Store.advance prose/legacy naive audit cannot establish
missing UTC clocks. Programme/Data owners must approve/capture the missing
event dictionary and periods prospectively, never backfill invented history.
Operational forecast resource/dependency/source-age evidence and calibration
require Programme/Finance/QA owners. These are distinct evidence follow-ups,
not defects in a labelled declared scenario.
Coordinator owns integration of overlapping Store/API/docs with #91/#92 and
independent final-head acceptance; no dependency ordering is invented.
PRD/BRD numbering mismatch is disclosed, not a guessed procurement/grant change.

## Validation Evidence

| Scope | Actual evidence | Status |
| --- | --- | --- |
| New pure + fictional JSON/SQLite HTTP | 24 tests | Passed |
| Actual unique loopback MSSQL report HTTP/consumer | 6 tests, retained UUID databases | Passed |
| Existing targeted regressions | 90 passed plus initial handoff import failure; documented-cwd rerun 6 passed | Passed after harness correction |
| Core/API configured ruff, format, mypy | 115 / 55 source files typed | Passed |
| Source image build/non-root app | Hardened UID/GID 10001, health and authenticated report/export parity | Passed on earlier implementation snapshot; final rebuild pending |
| Original Review blank-input probes | Two unintended 200 responses | Failed contract, RV-001 |
| Original Review UTC-range probes | Two OverflowError results | Failed contract, RV-002 |
| Web/browser/WCAG, Azure, real AI and human outcome | No web assets changed; external/live checks not authorized | Not run; no acceptance claimed |

## Outcome

Outcome: Defects found.
The original implementation is not accepted as fully satisfying malformed-input
requirements until RV-001/RV-002 are corrected. This original adverse outcome
must remain intact even after targeted correction evidence. Full operational
or complete historical capture acceptance remains unestablished independently.

## Blockers and Remaining Work

Concrete defects are unblocked safe engineering. Remaining P03 work: at most
two correction cycles, final image rebuild/smoke, own-only commit/push/main PR.
Source-authorized missing history/verified capacity and independent coordinator
closure remain explicit human/evidence prerequisites, not automated approval.

## Closeout Routing Record

| Finding class | Destination | Owner / next action |
| --- | --- | --- |
| Implementation defects RV-001/RV-002 | rpi-implement | Parent, same-session user-authorized correction ONE |
| Significant decision gap | None for concrete fixes | Do not guess domain authority |
| Material source evidence gaps | Distinct Programme/Data and Programme/Finance/QA follow-ups | Prospective event capture and verified resources/calibration |
| Integration/final-head acceptance | Coordinator | Review exact pushed head and overlapping integration |

Execution Complete. Outcome Defects found. No second full Review scheduled.
