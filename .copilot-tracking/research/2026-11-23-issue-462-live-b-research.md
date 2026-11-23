# Research: issue 462 criterion 2, hosted evidence (2026-11-23, second pass)

Disposition: executed. Planning Readiness: Ready.

Basis: the earlier same-day pass (`2026-11-23-issue-462-live-*`) left criterion 2 unproven because it assumed hosted run history needed a push. Read-only `gh` queries show that history is available.

Findings:
* PR #455 merged 2026-10-25T21:25:42Z, head `2523a70b16`. #444 is closed.
* Rubric workflow failed once on head `b82a7c4c93` (Capstone Rubric Scorer run 40207492780, with Source projects CI run 40207492737).
* Every `chore(rubric): record score` commit on the PR (`b82a7c4c93` 72/100, `2523a70b16` 73/100) has author and committer `github-actions[bot]` and touches only `.github/rubric/scores/{latest.json,badge.svg}`.
* After the failure the head SHA changed twice with new content (`b7966f5dfa` threat-model research and plan, `a3ce598429` threat model); the runs on `a3ce598429` and `2523a70b16` succeeded. No run was repeated on an unchanged SHA, so no unchanged-rerun fishing.
* Failure step detail is not retrievable (logs expired); the cause is not asserted.
* Existing local previews: not re-tested; not needed for this criterion.
* HSTS absence on the resident app remains an unrequired follow-up; a source change would need the full tier and redeploy, so none is made.
