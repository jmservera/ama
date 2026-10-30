<!-- markdownlint-disable-file -->

# Task Research: progress-dashboard-533-correction4

| Field | Value |
| --- | --- |
| Date | 2026-10-29 |
| Researcher / agent | RPI Agent / rpi-research |
| Status | Complete |
| Artifact path | .copilot-tracking/research/2026-10-29/progress-dashboard-533-correction4-research.md |

## Research Brief

* What to research: preserve lifecycle event identity, enumerate all five-event transitions and verify JSON/SQLite regression surfaces.
* Why it matters: ambiguous replay currently invents reopenings and suppresses missing closures in demonstration backlog and episode counts.
* Audience or intended use: correction round for PR #540, Refs #533.
* Scope: API progress replay, its tests, component documentation and relevant browser check.
* Non-goals: web redesign, data regeneration, schema changes, deployment, Azure and remote publication.
* Criteria: complete transition table, genuine duplicate preservation, unknown contradictory/incomplete evidence, strict typing and two storage backends.
* Requested outputs: evidence-backed recommendation and RPI handoff.
* Output mode: convergence.

## Research Parameters

| Field | Value |
| --- | --- |
| Research questions | Which transitions and repeated evidence are valid, and which fixtures/checks cover them? |
| Codebase scope | src/api, lifecycle producers in src/core, existing correction evidence |
| External scope | None |
| Initial internal candidate areas | progress.py, test_progress_dashboard.py, core workflow producers, progress_browser_check.py |
| Initial external candidate areas | None |
| Research posture | focused |
| Posture provenance | Default for named internal correction |
| Explicit limits / deadline | No push, az or force-push; local commits; nonblocking shared lock for heavy checks |
| Completion basis | Full transition semantics and observable regression coverage |
| Edits allowed during research? | No source edits |
| Resolved evidence root | .copilot-tracking/ |
| Known constraints / excluded sources | No private dataset, live models or cloud calls |

## Extension Registry and Provenance

| Kind | Candidate | Match and provenance | Scoped authority | Disposition |
| --- | --- | --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Repository-wide | Branch, src layout, evidence and checks | Selected |
| Skill | rpi-research | RPI phase | Three-wave evidence | Selected |
| Specialist | hve-core-all:rpi-researcher | Registered research worker | Bounded independent research | Skipped: one tightly coupled code trace |
| Skill | Web design skills | Backend-only correction | Web edits only | Skipped: no web edits |

## User Participation and Research Decisions

User explicitly requests the full RPI correction loop and local-only closeout.
This is authorization for these four phases, not an indefinite automatic child
session. No routine prompts or follow-up child work are needed.

## Scope and Success Criteria

Every initial and pairwise lifecycle transition must have an explicit legal,
duplicate or unknown disposition. JSON and SQLite must expose matching known/
unknown coverage, historical counters and archive date behavior.

## Task Research Requests

Preserve event kinds during replay; do not treat identification as reopening or
reopening as repeated identification. Deduplicate genuinely repeated evidence.

## Direction Controls

| Control | Source | Effect |
| --- | --- | --- |
| Reuse feat/progress-dashboard-533 and PR #540 | User | Clean worktree checked; requested git pull --rebase completed, already up to date |
| Commit locally, no push, no az, no closing keywords | User | Applies through closeout |

## Research Questions

| ID | Question | Type | Priority | Status |
| --- | --- | --- | --- | --- |
| Q1 | What event kinds and chronology do the producers actually emit? | depth | High | Answered |
| Q2 | What complete transition and duplicate rules preserve known evidence? | depth | High | Answered |
| Q3 | Which backend and browser checks establish the observable contract? | straightforward | High | Answered |

## Prior Knowledge Gate

Supplied finding is a hypothesis verified against the current boolean replay.
Prior correction artifacts are starting context, not proof this sibling issue
is resolved. Current branch starts at 788937e4.

## Research Cycle Log

### Cycle 1

* Wider, inline: C1-C3 identify five semantic event kinds and the shared inherited
  backend tests. Reflection: boolean replay cannot enforce event preconditions.
* Deeper, inline: C4-C6 verify return requires open, reopen requires closed,
  human closure requires open, and synthetic accepted handover closes. Reflection:
  a returned case is still in the same open episode, not a new episode.
* Contrarian, inline: distinguish exact repeated evidence from different-time
  same-kind actions. A second distinct reopen requires intervening closure;
  another identification cannot start a second episode. Same-instant
  accepted/closure evidence can corroborate one closure, but distinct closure
  instants without reopen are incomplete. Preserve chronological sorting and
  source order for timestamp ties (including legal zero-day episodes).
  Reflection: broad same-state dedup is rejected; exact UTC instant/kind
  dedup and same-instant closure corroboration preserve genuine repetition
  without silently repairing missing events.
* Parent synthesis: accept event-specific preconditions and persisted
  endpoint matrix. Reject repairing missing events or changing producer/schema
  contracts. No independent lane warranted for this single code trace.
* Re-entry: not needed; all scoped questions answered by producers and tests.

## Evidence Log

| ID | Finding | Location | Tool | Confidence |
| --- | --- | --- | --- | --- |
| C1 | Replay maps all starts to True and all finishes to False before deduplication | src/api/src/zava_forward/api/progress.py:76 | view | High |
| C2 | Dashboard episode/backlog and archive date share lifecycle(); unknown is already surfaced | src/api/src/zava_forward/api/progress.py:190 | view | High |
| C3 | JSON tests inherited by SQLite; existing persistence matrix reopens both stores | src/api/tests/test_progress_dashboard.py:297 | view | High |
| C4 | Return requires open; manager reopen requires closed | src/core/src/zava_forward/core/workflows.py:112 | view | High |
| C5 | Human closure requires explicitly active case | src/core/src/zava_forward/core/appointments.py:59 | view | High |
| C6 | Simulation accepted handover closes; aftercare reopens then recloses | support/synthetic-data/retrofit-flow/zava-forward-year-one/generator/zf_flow_b.py:353 | view | High |
| C7 | Relevant real-server browser check compares six chart/table series with API and archive behavior | src/api/checks/progress_browser_check.py:28 | view | High |
| C8 | Existing dev configuration requires strict mypy and Ruff; pinned tools and axe are available | src/api/pyproject.toml:61 | view and tool version probes | High |

## Findings Mapped to Questions and Evidence

Q1: C4-C6 establish semantic preconditions, not just target booleans.
Q2: C1 and C4-C6 support the table below. Q3: C2-C3/C7-C8
establish persistent-backend endpoint assertions and existing browser coverage.

## Alternatives and Decision State

Selected: retain typed event kinds until validation, then emit the existing
date/bool API-internal transitions. Only identical normalized UTC instant/kind
evidence is an unconditional duplicate. Equivalent closing kinds at the same
instant corroborate one close. Returns require an already-open episode and
never open or close one. Non-transition history and controlled advances remain
ignored. Distinct repeat lifecycle actions without their required intervening
event are unknown. This is intentionally more conservative than treating all
same-state events as duplicates.

Rejected: boolean-only dedup (C1 counterexamples); infer missing closure or
reopen from current state (fabricates historical measures); add schema/producer
changes (not necessary for read-model correction).

## Full Transition Table

I = identified, A = accepted handover, C = closure (human, withdrawn, excluded),
R = reopened (simulation or controlled), T = returned.
This table applies to distinct evidence after exact instant/kind deduplication.
An initial event must be I. A and C at the same instant corroborate one closure;
otherwise a second closing event without reopening is unknown.
T does not replace the last lifecycle-changing event.

| Prior semantic event | I | A | C | R | T |
| --- | --- | --- | --- | --- | --- |
| None | Open | Unknown | Unknown | Unknown | Unknown |
| I | Unknown | Close | Close | Unknown | Stay open |
| A | Unknown | Unknown | Unknown | Reopen | Unknown |
| C | Unknown | Unknown | Unknown | Reopen | Unknown |
| R | Unknown | Close | Close | Unknown | Stay open |
| T | Unknown | Close | Close | Unknown | Stay open |

For T->I, I is unknown unless it is an exact duplicate of the original
identification, already removed. T->R is unknown because no closure occurred.
Repeated T remains valid open-stage movement. I following any reopening is
unknown even after T. Every table cell will have persisted JSON/SQLite coverage,
with separate exact duplicate, closing corroboration, timestamp tie, ordering,
final-state and multi-episode controls.

## Sources

No external sources used. No private data read. Producer code only, not
generated or working datasets, was inspected.

## Risks and Residual Uncertainty

Timestamp-only evidence has no stable event ID. Distinct-time repeated lifecycle
actions cannot safely be assumed to be the same observation; conservative
unknown counts are preferable to invented episodes. Human accessibility,
hosted approvals and any future publication gate remain outside local acceptance.

## Research Disposition and Self-check

Executed. All three waves complete; evidence IDs resolve; no unresolved
implementation decision, external dependency or remaining research gap.

## Planning Readiness

Ready (C1-C8). Explicit full-loop user direction permits parent-owned Plan.
