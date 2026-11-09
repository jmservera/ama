# Changes: issue 1294 validation policy correction C3

Task: issue-1294-validation-policy-correction-c3 (Refs #1294). Mode: automatic correction loop. Tier: focused (guide and knowledge-base log wording only; no workflow, tool, source, SQL, infrastructure, deployment or security-control change). Base fa7ae0c9770e890f82482456bfcb8e97f1e05429; starting HEAD bd63b22c0b5405ae00f7cbe4d511db30446ab556, tree e2e237d18922d13addd15df735bdff69b22713da.

Plan: .copilot-tracking/plans/2026-11-08/issue-1294-validation-policy-correction-c3-plan.md. Details: .copilot-tracking/details/2026-11-08/issue-1294-validation-policy-correction-c3-phase-details.md. Critique: .copilot-tracking/plans/critiques/2026-11-08/issue-1294-validation-policy-correction-c3-plan-critique.md (Revise; PC-001..PC-003 applied directly).

## Changes

* src/README.md (+7/-1): the direct-check bullet was split. The `python -m checks.employee_acceptance_check` bullet now gives `PYTHONPATH=.:src:tests:../core/src:../agents/src:../core/tests:../agents/tests` from `src/api` (the runner's and hosted job's path) and states three named Chromium regressions, accepted only on exit 0 with exactly three tests and no skip (FR1 / review F3).
* docs/reference/log.md (additions only, 2 entries): a correction that the C2 entry's "final wording" claim was inaccurate (tested HEAD 7260826 plus pre-grade edits, Revise, four post-grade edits not re-simulated), and a C3 outcome entry (FR2 / review F2; outcome of the behavior run). The C2 entry is unchanged.
* Behavior evidence: sandbox 4 (.copilot-tracking/sandbox/2026-11-08-issue-1294-policy-4/: run-state, pre-run-status, target patch, checks/, test-design, test-log, test-review) and report 4 (.copilot-tracking/hve-builder/2026-11-08/issue-1294-validation-policy-behavior-report-4.md) (FR3 / review F1).

## Process note (honest record)

The `src/README.md` acceptance-command edit was made immediately before the `rpi-implement` skill was invoked rather than after; it was within the planned P01-T01 scope and nothing else was edited early.

## Validation (all run from the worktree with PYTHONDONTWRITEBYTECODE=1; outputs under the sandbox checks/)

| Check | Result |
| --- | --- |
| Discovery probe from src/api (checks/discovery-probe.txt) | exit 0: `test_employee_acceptance_check` not findable with PYTHONPATH unset; found with `tests:../core/tests:../agents/tests` and with the runner path; with the runner path three named tests load (count 3) |
| `git diff --check` | exit 0 |
| Non-ASCII in added lines | 0 |
| Removed lines in docs/reference/log.md | 0 (append-only) |
| README link scan (checks/links.txt) | clean |
| Stale-phrase grep (`any mixed`, `genuine risk`, `within the 58-byte`) in the three guides | no matches |
| Behavior run 4 (full, independent design/execution/grading, proxy, retain-sandbox) | Pass, 0 confirmed contract defects, no edit after grading |

Not run: the browser harness or the employee acceptance command (wording only; no browser run claimed), hosted CI (unobserved), a full gate (not required for focused tier).

## Behavior verdict and limits

Pass on the final guide wording, as a proxy simulation (profile unresolved; model not observable; no intended-profile or native claim). The only edits after grading are the appended C3 outcome log entry and tracking records, which are not guide wording. Reports 1-3 and sandboxes 2 and 3 are preserved. Attempt A2 was not needed.

## Status

Pre-run `git status --short --ignored` (sandbox 4 pre-run-status.txt): clean except ignored tools/__pycache__/. Post-run: modified src/README.md and docs/reference/log.md, untracked C3 artifacts, ignored tools/__pycache__/ preserved. Open items: Review (P03), commit. Hosted CI unobserved; nothing pushed.
