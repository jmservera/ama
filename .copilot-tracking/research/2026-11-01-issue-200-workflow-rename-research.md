# Issue 200 remaining slice research (2026-11-01)

Task: issue-200-workflow-rename. Research disposition: executed. Planning Readiness: Ready.

## Evidence

* Merged PRs: #304, #302, #298, #321, #342, #357, #499 delivered criteria 1, 4, 5, 6, 7 and the src path/build/test part of criterion 2. Open PR #694 is unrelated.
* Owner decision 2026-10-15: keep old workflow and check names until cut-over, then rename in one PR. Cut-over completed 2026-10-27 (#499).
* `gh api .../branches/main/protection` returns 404 (main not protected), so no required check context is dropped by a rename.
* Live names: `MVP CI` (mvp-ci.yml, jobs test/image/mssql) and `MVP validation` (mvp-validation.yml, job validate). Hash pins in `tools/rpi-checks.py` WORKFLOW_HASHES; text mention in `infra/README.md:1512`.
* Criterion 3 (new tag deployed and verified on Container Apps) needs Azure-live work: not authorised.

## Decision

Deliver only the deliberate display-name rename; keep file names, job IDs and concurrency semantics so history and tooling stay stable. Criterion 3 stays unmet.
