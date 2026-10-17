<!-- markdownlint-disable-file -->

# Task Research: historical-progress-controls-102

| Field | Value |
| --- | --- |
| Date | 2026-10-17 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-17/historical-progress-controls-102-research.md |

## Research Brief

Research issue #102 historical event progression, deterministic forecasts and
role-scoped export evidence for a cohort and explicit as-of timestamp.
Audience: implementation and coordinator review. Output mode: convergence.
Acceptance: timestamp-derived durations/handoffs/pauses/returns/reopenings;
labelled assumptions, uncertainty and data limits; exports with definitions,
sources, denominators and unresolved exceptions.

## Research Parameters

Focused posture selected from the caller's bounded internal scope. Initial
areas: src/core, src/api, src/agents report/event/forecast paths and tests,
PRD FR-022/023/024 and BRD BG-011. External research: none required initially.
Evidence root: .copilot-tracking/. Research writes only evidence and state.
No private data, other worktrees, retired mvp edits, live infrastructure,
provider calls, UI redesign or invented historical observations.

## Extension Registry and Provenance

Repository instructions selected for source/package and knowledge routing;
rpi-research selected for ordered three-wave evidence. Domain web skills
deferred unless actual web changes are necessary. Specialist delegation
skipped initially: the existing report-to-event trace is tightly coupled.

## User Participation and Research Decisions

The user explicitly requested all ordered phases, critique, one Review, up to
two concrete correction cycles, commit/push and a main-targeted PR. This is
direct authorization for this bounded full loop, not authority for live actions.
No intake clarification needed.

## Direction Controls

Preserve independent lifecycle states and immutable audit semantics. Never
infer missing timestamps from current records or narrative. Unknown or malformed
history must remain visibly unresolved. Reuse source-authorized cohort filters.
Research overlap with #91/#92 before editing; coordinator owns integration.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | Which existing events, lifecycle definitions and report interfaces are authoritative? | Answered C1-C4 |
| Q2 | How are cohort role filters and report exports protected? | Answered C5-C6 |
| Q3 | Which existing deterministic forecasts and tests can be reused? | Answered C7 |
| Q4 | Which implementation surfaces overlap parallel work? | Answered C8 |

## Prior Knowledge Gate

Original case study, addendum exercise register, KB index and memory read.
Current-state charts explicitly do not establish historical acceptance.
Branch is the caller-specified clean topic at the supplied base; no existing PR.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Inspected core insights/projection/Store, API GET report/export routes, PRD
and BRD and existing handoff tests. No deterministic delivery forecast exists
in the executable report paths. `projection.py` is a field-rights module,
not a forecast. Stats are current-state counts; CSV is a current case list.
Reflection: preserve both legacy responses; add an explicit historical report
mode to these existing paths, not a new assistant or screen.

#### Wave 2: Deeper

Traced `_filtered`, sync-on-lock SQL reads, returns/reopen dispositions,
handoff history and change-provenance structured old/new events.
`history` is narrative; audit `detail` is often prose and audit timestamps are
legacy naive local time. None can establish a UTC stage clock.
Reflection: use explicit structured histories only, timezone-aware timestamps,
exact stage/state kinds and source paths. Missing event coverage remains unknown.
The first observed `from_stage` does not establish its entry timestamp.

#### Wave 3: Contrarian

Challenge targets: mixed timezone/date-only events, invalid versions, broken
stage chains, simultaneous contradictory transitions, current-filter membership
mistaken for an as-of cohort, unrecorded accepted handover, raw source/actor free
text leaking through exports, zero-event success and untouched audit integrity.
Inline investigation continues on exact source shapes and SQL test harness.

Reflection after exact-source inspection: administrative edit history does not
authorize lifecycle stage changes. Returns/reopens carry explicit `from_stage`,
`to_stage`, UTC `at`, version and actor, but missing source is allowed. Handoffs
have exact state snapshots, not a transferable ownership inference from receipt.
Thus stage intervals can be derived between consistent return/reopen events,
but incomplete ordinary forward progression must be reported unknown. No new
event writer or guessed taxonomy is justified. Existing paused stage labels
can classify observed intervals, not a separate resident/safety lifecycle.

Parent synthesis: accept a read-only report mode on existing stats/CSV paths,
with a shared report object, strict timezone/as-of validation, allow-listed
event metadata, explicit partial coverage, independent handoff timeline and
conservative unknowns. Deterministic forecast uses declared synthetic scenario
assumptions only; it cannot assert actual committed capacity or historical fit.
No further cycle needed: contracts and material limitations are established.

## Evidence Log

| ID | Evidence |
| --- | --- |
| C1 | `src/core/src/zava_forward/core/workflows.py:100` return/reopen disposition schema; source can be absent, history is retained |
| C2 | `src/core/src/zava_forward/core/workflows.py:215` exact handoff history snapshots and independent receipt/acceptance |
| C3 | `src/core/src/zava_forward/core/store.py:502` ordinary advance writes prose audit, not a structured UTC transition |
| C4 | `src/core/src/zava_forward/core/ledger.py:29` audit timestamps are legacy naive local times; hashes must stay unchanged |
| C5 | `src/core/src/zava_forward/core/store.py:245` existing `_filtered` current-state cohort rights, mine/all/manager closed views |
| C6 | `src/core/src/zava_forward/core/projection.py:38` staff GET and denied contractor report/export surfaces; raw free text unsafe |
| C7 | `docs/case_study_48_addendum.md:137` EXA-009 and numerical targets: independent installation/QA pools, one/two-week duration, capacity one/two/three; constructed assumptions not supplier commitments |
| C8 | Read-only GitHub PR file lists #387/#389: shared Store/API/component READMEs/KB routes anticipated by caller; actual PRs touch API server, core/API READMEs and KB index/log. No other worktree read |
| C9 | `src/core/src/zava_forward/core/sqlstore.py:92` lock sync refreshes current cases, inherited stats/export use in-memory read model |
| C10 | `src/api/src/zava_forward/api/server.py:320` existing CSV and stats interfaces and source filters |
| C11 | PRD FR-022/023/024 and AC-025/026/027 govern this work. Current BRD FR-022/023/024 instead concern procurement/grants: stale numbering is a source contradiction, not authority to change those domains |

## Alternatives and Decision State

Selected: deterministic, read-only normalized history and scenario report;
reuse `_filtered` under Store lock and existing report/export authorization.
Reject snapshot-to-history reconstruction, prose parsing, new AI, domain
writers and UI changes. Reject changing SQL schema or other issue domain logic.
Shared-file delta limited to additive Store method and report routing; new
issue-specific tests avoid shared fixtures. Coordinator sequences integration.

## Open Questions, Risks and Residual Uncertainty

Historical coverage is partial by design until source records exist. No exact
accepted-handover mapping can be authorized from a stage or closure flag.
Forecast dependencies/capacity are declared scenario assumptions, not validated
resources. Report mode is API/export only; existing screens remain unchanged.
SQL consumer behavior will be tested on a unique local Docker SQL Server.
No operational, human, WCAG, Azure or paid AI acceptance is claimed.

## Planning Readiness

Ready for bounded safe engineering. Research disposition: executed.
Self-check: three ordered inline waves, stable C IDs, alternatives, overlap,
contradiction, limitations and readiness recorded. No workers implied.

## Correction TWO targeted source investigation (2026-10-17)

Coordinator exact-28227fa8 independent Revise / Medium is an additional concrete
finding, not a second full RPI Review in this session. Actual source contracts:

* `change_provenance.operation` compares caller handoff_version with the current
  history length, refuses stale writes, captures precise aware UTC `at` before
  yield and appends version `len(history)+1`. Offer/accept use this existing
  operation and preserve its source/version/actor/change and audit semantics.
* `WorkflowMixin._handoff_event` appends snapshot/version `len(events)+1`;
  receipt/escalation/decline/withdraw/complete used `_now()` with
  `isoformat(timespec="minutes")`. Their state timestamps used the same
  minute-format helper. Neither source promises chronological sorting can
  replace the authoritative append sequence. Completion is not acceptance.
* A minute-format timestamp or a seconds-expanded zero corroborated by the
  corresponding exact legacy state minute field supports a minute interval.
  Zero seconds alone, fractional precision or arbitrary backward times do not.
  Compare full possible minute intervals with the greatest predecessor lower
  bound; a backward date outside that range is still contradictory.
* The existing `_now` helper can take an optional timespec with its default
  unchanged. Handoff-only calls use microseconds; offer/accept snapshot times
  reuse their already-authoritative operation event time. `controls.now` is
  naive/minute-resolution and is unsuitable; it is not changed or reused.
* Fetched main 3f544fb9 contains quality #387. Read upstream quality,
  assistants and API diffs: active_records excludes only Superseded; capture/
  discrepancy/contributor review use current evidence and evidence_version
  stales replacement proposals. Quality committed-refresh errors map to 503
  with outcome committed. These and existing SQL/hazard/financial/stock hooks
  are retained unchanged, not merely declared parity after logic changes.

Observed failing-first execution used real Store offer/receive/accept writers
with frozen fictional old timestamps. It reproduced `[2,1,3]` report ordering
for a valid `[1,2,3]` source sequence. Dedicated fixtures cover exact precise
backward times, all known minute writer states, export and as-of/start unknowns.
Forward stage and accepted-handover event coverage remains incomplete.
Prospective complete capture is buildable distinct follow-up, not a human
blocker or full-history acceptance. No persisted event rewriting is justified.
