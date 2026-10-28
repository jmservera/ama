<!-- markdownlint-disable-file -->
---
title: Resident chat 520 proposal expiry follow-up changes
ms.date: 2026-10-28
---

# RPI Changes: resident-chat-520-expiry-followup

## Metadata

Task ID: 520-expiry-followup. Implementation date: 2026-10-28.
Plan: .copilot-tracking/plans/2026-10-28/resident-chat-520-expiry-followup-plan.md.
Details: .copilot-tracking/details/2026-10-28/resident-chat-520-expiry-followup-phase-details.md.

## Execution Status

Partial, full-plan invocation. P01/P01-T01/P01-T02 complete; P02 Review/publication remains.
Original critique Complete / Pass, no findings.

## Execution Summary

Implemented the approved agenda.py query/final-check correction, one owning test method
and README clarification. The regression failed before changing production code.
Tool restoration followed actual missing ruff/mypy errors, not a manifest change.

## Validation Record

Scoped checks passed on the final source bytes. Every heavy command held the shared
nonblocking lock after 60-second retries within 40 minutes. No browser-facing edits.

### Heavy admission and upstream observation

The dependency-restoration command initially waited on the existing shared lock, using the
requested nonblocking retries every 60 seconds with a 40-minute ceiling. Read-only
lslocks confirmed a Python holder (PID 202197); no foreign output or private data was
inspected and the holder was not interrupted. No heavy work has run without admission.
Admission succeeded at 2026-10-28T20:36:04Z, inside the 40-minute ceiling. Pinned
ruff 0.17.1 and mypy 2.4.0 restored to the task-owned external virtual environment.
API import resolved to this exact worktree.

git fetch origin completed; topic and local HEAD both remain
72a7810189db0994111b0a2d9b3341bd002f2f17, with no newer remote bot commit.
Authenticated GitHub account resolved to id 8036360, login jmservera. Refresh upstream
again at publication; this observation does not preclaim no later advancement.

### P01-T01 deterministic red and implementation

External evidence root:
/home/azureuser/.copilot/session-state/0632f8cf-cc46-45e2-acb7-aafa7811e9dd/files/520-expiry-validation.
setup.log records dependency restoration. regression-red.log preserves the first failure:
exact expiry booked incorrectly and contaminated the next failing subtest. Ordinary
test implementation refinement gives each boundary its own disposable agenda; no new
test method or scope expansion. Details updated accordingly, critique unchanged.
regression-red-isolated.log records both exact-expiry and one-microsecond-after cases
independently failing with AgendaConflict not raised (exit 1). Just-before expiry passed.
Both reproduction runs held the shared lock. No sleep in the regression.

agenda.py now selects o.expires and compares expiry and start to one freshly sampled
post-authorization instant within the existing transaction. Either conflict rolls back.
The prior-booking/idempotency and authorization branches are unchanged.
The README states the two-deadline commit boundary.

### P01-T02 initial validation and directly coupled lint correction

The next heavy admission succeeded at 2026-10-28T21:02:23Z. The regression passed,
and all six planned resident-demo selectors passed: 92 tests in 42.984s, no skips.
API-wide Ruff then reported four B023 loop-closure findings in the new test; format
applied first. Formatting/Ruff/mypy later in that command did not run after lint failed.
Original logs retained: regression-green.log, resident-suites.log and ruff-check.log.

Bind the authorization callback's per-subtest clock/deadline as defaults and use an
existing-library Mock callable clock. Assert the authorization-updated time and exactly
two clock samples. This is a lint-driven correction inside the same approved test
method, no dependency, method-count, semantic or production change.
Final locked validation is queued with the same bounded admission policy. It includes
an in-process original-book-method negative control on the exact final test, then
regression/suites, full API Ruff100/format100 and mypy. No original adverse log is replaced.

### P01-T02 final validation

Final admission acquired at 2026-10-28T21:21:55Z; all checks completed at 21:22:44Z.
External logs, all under the evidence root above:

| Check | Result | Log |
| --- | --- | --- |
| Exact final regression against original 72a78101 book method, patched in process only | Expected two failures: exact/after expiry both lack AgendaConflict; no errors | final-negative-control.log |
| Exact final regression against fixed code | 1 test passed; three boundary subtests | final-regression-green.log |
| Six planned resident-demo unit/API selectors | 92 tests passed in 43.557s; zero skips | final-resident-suites.log |
| Full API ruff check --line-length 100 . | Passed | final-ruff-check.log |
| Full API ruff format --check --line-length 100 . | Passed, 50 files already formatted | final-ruff-format.log |
| Full API mypy | Passed, 94 source files | final-mypy.log |
| Browser harness | Not run, no browser-facing code changed | Not applicable |
| Complete local gate | Blocked/unattempted, requires barred az | No receipt claimed |

Expected RuntimeError diagnostic lines in the suite belong to existing explicit
failure-path tests; the suite completed OK without skips.
final-source-sha256.txt binds:
agenda.py 1006b6b04b05ad0593e176695b42905ce4cd72cf1bd6da26cc66eb7b72c6d096;
test_resident_chat_agenda.py 4cae256edaf50b5e2add6a12020a167f617b86521aa9e3b08327fd2d47a2105e;
README.md 7d0c31071fb8f3daa6cd50b2fcaa22be9b0ad89e705abb463ebc909c999b4553.

## Pre-Review Reconciliation

Plan markers/details show P01 complete and P02 ready. Source/test/doc hashes, all actual
outcomes and original failures are retained. Exactly one critique Complete / Pass.
No significant divergence or unresolved implementation finding. Review readiness:
Ready for scoped independent Review; full gate and inherited acceptance remain blocked.

## Blockers

Full gate requires barred az: unavailable and will not be attempted. This is separate
from the authorized narrow fix's focused checks and publication. Human/AT and hosted
approval remain unclaimed.

## Remaining Work

P02 authorized publication/thread resolution; original independent Review is complete.

## Original Review and Publication Handoff

Exactly one original independent Review executed Complete; outcome Residual work,
P01 Conformant, zero implementation defects. RV-001 Medium routes unavailable full
gate to later authorized validation. RV-002 Low routes inherited human/AT/hosted
acceptance to their distinct owners. No finding returns this task to implementation,
and no second Review is planned. The original reviewer record is unchanged.

Publication fetch after Review: remote topic still equals the initial 72a78101 head,
no newer bot commit, so no rebase is necessary. Current origin/main observed:
f41ecbc37bf12670d53ad7b03364b0c3b530d521. Scoped tested source bytes are unchanged.
Commit implementation and dated original evidence now; push normally and verify the
remote fix before posting any thread response. P02 stays pending until live verification.

Commit skill was loaded; its referenced commit-message instruction file and deferred
get_changed_files tool are unavailable in this host. Repository Conventional Commit,
privacy-safe identity, explicit task-only staging and final coauthor trailer rules
govern the commit. No git operation prohibition from a generic skill overrides the
owner's explicit fetch/normal-push publication request.

## Follow-Up Items

Full gate under future authorized prerequisites; inherited human/AT/hosted acceptance.
Canonical list is the plan's Follow-Up Items section. No broader work activated.

## Return-to-Caller State

Automatic parent, RPI through Review complete, phase Follow-up. Original outcome
Residual work with conformant scoped implementation. P02 publication still pending.
