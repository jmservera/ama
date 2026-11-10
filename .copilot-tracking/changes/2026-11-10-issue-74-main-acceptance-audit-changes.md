# Issue 74 current-main acceptance audit: changes

Plan: [plan](../plans/2026-11-10-issue-74-main-acceptance-audit-plan.md). Status: implemented 2026-11-10 (prospective list written before implement-start; actuals below).

## Planned changes (documentation and evidence only)

* Add this changes record and the acceptance matrix [matrix](2026-11-10-issue-74-main-acceptance-matrix.md) under `.copilot-tracking/changes/`.
* Add the single post-implementation review under `.copilot-tracking/reviews/`.
* Update the state JSON under `.copilot-tracking/rpi-sessions/2026-11-10/`.
* Raw command output and the witness log stay outside the repository in the Root evidence folder `phase74-main-acceptance-audit-evidence-1110`.

## Explicitly no changes

No change to `src/`, `docs/`, tests, the browser check, fixtures, dependency manifests, workflows, issue #74 criteria, shared pack, index, log or README. No push, PR, issue or board write.

## Actual changes

* Added the acceptance matrix, this record, research, plan, details, critique, review and state JSON, all under `.copilot-tracking/`.
* Raw logs 01-05 and the witness log are in the Root evidence folder `phase74-main-acceptance-audit-evidence-1110`.
* Removed the ignored `build/`, `*.egg-info` and `tests/__pycache__` directories that the venv install and a fixture import created in the worktree; no tracked file changed.

## Amendments and divergences

* The chromium revision cached (1248) was accepted by Playwright 1.64.0; no browser download was needed.
* The pinned axe 4.10.3 file already existed at `/tmp/axe-4.10.3.min.js`; its hash equals the check's pinned constant, so axe ran rather than being skipped.
* No other divergence. No source, test, fixture, criterion or issue edit.
