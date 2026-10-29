<!-- markdownlint-disable-file -->
# RPI Phase Details: Bounded mixed-source lifecycle remediation

Task ID: 533-tie-remediation. Parent: 533-correction4.
Plan: .copilot-tracking/plans/2026-10-29/progress-dashboard-533-tie-remediation-plan.md.
Evidence: original correction4 Review RV-001/RV-003. No unresolved decision.

<!-- rpi:phase id=P01 -->
## P01: Resolve ambiguity and coverage confounding

<!-- rpi:task id=P01-T01 -->
### P01-T01: Persistent regressions

Use the existing lifecycle fixture and persisted assertion helpers. Repeated
closes in history/human closures and controlled reopens in returns share one
instant. Exact duplicate appearance does not establish cross-stream adjacency.
Require Unknown for open snapshots and when followed by a later closure, so
archive dates also stay unknown. Keep positive same-stream episodes, plain
duplicates and unambiguous cross-source close/reopen known.
For A->T/C->T keep closed=True to isolate return preconditions from final-state
validation. No additional helpers, methods, schema or generated files.
Completed: mixed-source repeated close/reopen and corroborating-alias cases
remain unknown in both persisted stores, with both current-open and later-closed
snapshots. Distinct version observations at one instant also remain unknown.
Safe single-close/control-reopen and genuine duplicate controls remain known.
The isolated return-guard mutant now fails exactly A->T/C->T per backend.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Source-aware ties

Carry history/home-case-closure/return collection provenance through extraction.
Before replay, examine each equal-instant group. Repeated closing or opening
evidence alongside opposing reopened/closing evidence from multiple sources
cannot prove duplicate adjacency; return unknown. Do not global-deduplicate,
fabricate event IDs or invent cross-stream ordering.
Preserve ordered same-stream history, closing corroboration without reopening,
and isolated cross-stream close/reopen without repeated evidence.
Completed: provenance-bearing events are grouped by normalized UTC instant
before replay. Multi-source groups with opposing closes/reopens and repeated
evidence are unknown. Within replay, observations of each current-transition
kind must agree on every field other than timestamp spelling, so distinct
versions cannot be erased. Observation identities reset at each boundary.
This directly tightens genuine-duplicate detection within the existing scope;
no new user decision, producer, schema, abstraction or dependency.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Validation and local-only closeout

Record a red against original candidate, then final targeted units and strict
API/core mypy/Ruff. The round's sole heavy admission already returned busy:
do not retry/poll or mutate /tmp/mv; use worktree-local imports and existing
runtime. Original Review remains Complete / Not accepted at 60004dde.
Subsequent implementation is not independently re-reviewed or accepted.
Retain original evidence and commit source/remediation/closeout locally.
Validation complete: final 77 targeted tests, API/core strict mypy and both Ruff
commands pass. No heavy retry, browser run or shared editable install.
Completed: source/original Review/remediation evidence commit
72cdda2774c64510aea88c1ac4fddc570fcaa346. Final stopped-session closeout contains
only dated evidence/state changes; no remaining active implementation task.
