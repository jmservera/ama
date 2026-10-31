<!-- markdownlint-disable-file -->
# Changes: gate-chat-test-572-validation-correction

Task ID: 572. Date: 2026-10-31. Scope: full correction plan.
Plan/details/research share the same child slug and date. Parent original
adverse Review and changes are preserved unchanged.

## P01: Execution Entry

Fetched origin/main 1330869ea675ff019958846330108b4f45e163ce.
Requested merge into HEAD 11829dbd4189ed5bb81a21faf0bd0a90d40ece96
reported Already up to date; ancestry independently checked with merge-base.
No conflict, workflow edit, WORKFLOW_HASHES edit or log-entry loss.

Existing external venv has required API/core/agents and declared dependencies.
No pip install or generated repository outputs are needed at entry.
Privacy-safe repository-local identity resolved through gh api user.
Current logs are under
/home/azureuser/.copilot/session-state/8fc27754-5c81-49d8-866e-55a2bc017433/files/.

## Critique Dispositions and Execution Safety

One independent critique Complete / Revise. PC-001's worker-local /tmp
restriction is not present for parent Bash; parent owns real unchanged-lock
execution. PC-002 and PC-003 source-equivalence and blocking-Review publication
safeguards were directly applied to plan/details. No repeated critique.
Full gate uses its internal 1800-second lock wait, not a self-deadlocking outer
flock; focused Chromium uses caller's outer flock. One admission retry only.

## Validation

P01-T02 passed after normal shared-lock admission on the first 1800-second
attempt: exact verbose named case, Ran 1 test in 2.379s, OK, zero skips.
External evidence: correction-chromium-1.log. No retry was needed.

API Ruff check and format passed (65 files). Initial root tooling Ruff invocation
accidentally inherited the root-wide rules and reported 12 findings; corrected
to the existing gate-owned isolated E,F,I,B,UP / py312 / 100-column configuration,
not a source fix or disabled gate. Both tooling files then passed check/format.
All 39 gate unit regressions passed in 14.874s.

Initial reused non-editable API discovery ran 1430 tests in 746.545s, with seven
errors and 320 skips. Five evaluation errors name missing tracked golden
fixtures under the non-editable install; two HTTP endpoints fail for the same
evaluation path. Preserve correction-api.log as adverse evidence.
Restored core/agents/API as editable installs with pip --no-deps from a fresh
external git archive of HEAD's src tree, retaining pins and keeping all build
outputs outside the worktree. API discovery rerun passed: 1430 tests in
668.049s, OK (skipped=320). Explicit opt-in discovery skips are not execution.
External evidence: correction-api-editable.log and editable-restore.log.
This is immediately relevant environment restoration, not a source change.

## Main Drift Before Correction Review

Fetched main advanced to a75bbdffa51ae34b1fcf779250f1f553d566ee93 (#558).
Merged without rewriting into 255d6ad8909c49855d8b0551d6e2ca9bcdcfd4dd.
No conflict. Upstream score/log and workflow/hash changes retained as supplied
by main; no task-authored workflow or WORKFLOW_HASHES edit. The sole merged
gate delta is main's matching src-ci hash. No src source/test changes occurred;
API/browser focused results remain relevant. Correction Review assesses this
integrated source/workflow boundary; full gate uses the new main base.

## Original Correction Review and Candidate Handoff

P01 complete. Integrated tooling rerun: 39 tests in 11.491s, OK.
Single original correction Review Complete / Residual work at integrated head
255d6ad8 / base a75bbdff. No blocking source defects. RV-001 [High] retains
AC4's planned committed full gate, receipt verification and eligible independent
exact-head assessment as publication prerequisites. Review pointer:
.copilot-tracking/reviews/logs/2026-10-31/gate-chat-test-572-validation-correction-review.md.
Original parent and correction adverse outcomes are not rewritten.

P02-T01 complete; P02-T02 candidate commit is next, then P03 full gate/publication.
No issue closure or passing full receipt is claimed by this pre-gate evidence.
No source defect, unrelated cleanup or out-of-scope follow-up is known.
Final status and authoritative receipt stay external and in the PR; do not
make a later evidence commit and reuse this candidate's gate.
