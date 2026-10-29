<!-- markdownlint-disable-file -->
# RPI Phase Details: Progress lifecycle event-kind correction

## Metadata

* Task ID: 533-correction4
* Task slug: progress-dashboard-533-correction4
* Plan: .copilot-tracking/plans/2026-10-29/progress-dashboard-533-correction4-plan.md
* Evidence: matching dated research, C1-C8; no unresolved research gap.

## Phase Index

| Phase | Name | Status | Tasks |
| --- | --- | --- | --- |
| P01 | Replay and regression matrix | Complete | P01-T01, P01-T02 |
| P02 | Validation and local review | Execution complete; original Review Not accepted; full/browser blocked | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Event-aware replay and exhaustive regressions

Context: boolean reduction destroys required event preconditions. Initial
identified, accepted handover, closure, reopened and returned require distinct
classification. Both HTTP read models use lifecycle(), so the correction
must preserve unknown coverage and archive visibility/filtering together.
Boundary: no producer, schema, dataset or UI edits. Source ownership and
maximum additions are locked in the plan.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Persist the transition matrix

Build an independent literal expected table, five rows plus initial prefix,
using valid prefixes for reopened and returned states. Assign successive
dates so illegal same-kind cells cannot be mistaken for exact duplicates.
For unknown sequences set final closed state consistently with their apparent
last action; state consistency alone must not repair history. For each cell
save and reopen the actual store, then check lifecycle(), both endpoints,
known siblings, exact counts/durations and both one-sided archive date filters.
Use explicit case synthetic admission so malformed history cannot disappear.
Test both supplied counterexamples and all closure/reopen representations.
Positive controls prove exact UTC instant/kind dedup, timestamp ties,
multi-episode replay and ignored controlled advance evidence.
PC-002: JSON uses Store.save() and a new Store; SQLite injects only the
constructed case body with UPDATE cases under lock as in the existing malformed
fixture matrix, then opens a new SqlStore. Close each owned reader in finally.
Assert reopened history/home_case_closures/returns/closed fields exactly equal
the constructed fixture before any replay/aggregate assertions.
PC-001: positive controls include I before t followed by A,R,A,R at t and
closing aliases separated by R at t, with exact episode counts/durations.

Completion: retained pre-fix failure and focused green from both inherited
backend classes. No existing assertions removed.
Observed: initial helper replacement broke JSON object aliasing; fixed locally
to mutate the existing case dictionary. The corrected red independently
reproduces both review sequences in both reopened stores (four failures).
Final progress suite contains 41 tests; all pass within the 77-test fallback.
Exactly four inherited methods and two helpers added; none removed.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validate semantic kinds before projection

Preserve extraction guards and observed() UTC normalization. Classify history
Identified, Accepted handover, Withdrawn/Excluded and aftercare reopen; human
home closure and controlled reopen/return are distinct. Legacy recognized
flags remain supported; controlled advance does not become a return.
Require identification before any other meaningful lifecycle evidence.
Exact repeated evidence does not create transitions only while it repeats
the current lifecycle-changing event; never use global instant/kind membership.
Same-instant A,R,A,R retains every alternating transition.
A return requires open,
but does not alter the episode-start kind. Closing corroboration is bounded
to the same observed instant; distinct-time repeated closing/opening evidence
is unknown. Keep final closed-state check and output shape.
Document these conservative semantics in the existing API README section.

Completion: unchanged ordinary fixture totals, new full matrix green and strict
static checks. No pinned file is anticipated to change.

<!-- rpi:phase id=P02 -->
## P02: Validation, original Review and local closeout

Context: previous correction recorded busy heavy-lock validation. That adverse
record remains immutable; this round gets one new admission attempt and its
own exact results, not borrowed success.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Scoped and admitted checks

Use /tmp/mv mypy/Ruff from src/api and src/core with this worktree's src and
test directories explicitly on PYTHONPATH (core tests first for core mypy).
Nonblocking flock -n /tmp/ama-rpi-heavy.lock encloses pip editable setup and
full unit/browser suites for the entire execution, not just an initial probe.
If busy, no shared venv mutation, waiting or polling; existing runtime runs
targeted progress/workbench/role/workspace/taskqueue/manifest selectors.
Existing axe asset: /tmp/ama-533-correction2-20261029/axe-4.10.3.min.js; hash
verified by the canonical browser checker. New output lives externally under
/tmp/ama-533-correction4-20261029.
Record actual commands, exit codes, test counts/skips, source/tool identities
and limitations. Browser is engineering evidence, not human acceptance.
Observed: one nonblocking admission returned 75 before any enclosed command.
An independent lock listing after the failure showed no holder, so its
transient holder identity is unavailable. Do not infer free admission or retry.
Shared editable setup was not executed. /tmp/mv tools were already available;
explicit import paths resolve the current worktree. Required static checks and
77 targeted tests pass; full API/core and browser remain blocked.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Candidate and independent Review

Reconcile plan/detail markers and validation evidence before committing.
Use local privacy-safe identity and both author/committer noreply email.
Conventional Commit with required Copilot trailer, Refs #533 (not closing).
One independent reviewer assesses source candidate and the full supplied
requirements/plan/critique/change boundary; writes only the dated original
review file. Retain adverse findings without current-task fix/re-review.
Commit closeout artifacts and stop session as explicitly requested, leaving
all commits local and publication/human/hosted gates separate.
Completed original Review: Complete / Not accepted at 60004dde. RV-001 high
mixed-source ties and RV-003 medium masked return cells route to separate bounded
implementation progress-dashboard-533-tie-remediation; RV-002 medium full/browser
validation remains blocked. No repeated critique/Review or rewritten outcome.
