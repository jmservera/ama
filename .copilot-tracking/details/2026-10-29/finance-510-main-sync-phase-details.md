<!-- markdownlint-disable-file -->
---
title: Finance PR 510 main synchronization phase details
description: Resolution and validation expectations for the local finance integration
ms.date: 2026-10-29
---

## Metadata

Task ID / slug: `finance-510-main-sync`; date: 2026-10-29.
Plan: .copilot-tracking/plans/2026-10-29/finance-510-main-sync-plan.md.
Research: .copilot-tracking/research/2026-10-29/finance-510-main-sync-research.md C1-C6.
Initial direction: additive replay, no feature changes. Local blockers: none.

## Phase Index

| Phase | State | Tasks |
| --- | --- | --- |
| P01 Rebase | Complete | P01-T01 |
| P02 Validate/deliver | Validation complete; Review/local commit pending | P02-T01, P02-T02 |

<!-- rpi:phase id=P01 -->
## P01: Rebase and preserve intent

Context: main `8ee1b77f8983ddf39216da07ae60c63ef66431d6` adds #512;
finance `bafcb2415991a15eb3a16b781649a2ce7c749fcf` has eight unique commits.
Only expected overlapping targets are reference README/log and rubric score.
No existing user changes were present; new untracked current-task artifacts
are owned by this invocation and have unique names.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Replay and resolve

Before `git rebase origin/main`, assert `git rev-parse origin/main` equals
`8ee1b77f8983ddf39216da07ae60c63ef66431d6`. Capture original start and
merge-base ranges for `range-diff`. Assert the base ref is unchanged after
replay and use that immutable SHA for ancestry/protected-copy comparisons.
If main changed, reconcile its affected diff and evidence before replay rather
than silently using an unassessed target. Later coordinator publication still
requires fresh-main verification. Inspect every actual conflict. For the index,
preserve main's single current date and monitoring entry plus the finance
entry. For the append-only log, preserve main as a byte-prefix and append the
finance entry with proper heading spacing. Keep main's rubric tree and exact
manifest. Skip an empty score-only replay if main already supplies its
authoritative replacement; no finance/source commit may be skipped.

Validate ancestry, `range-diff` and original source/evidence bytes against the
start SHA. No branch deletion, reset, forced remote action or stash is needed.
Completion evidence: no unmerged entries/rebase state, main ancestor, both
contributions preserved, protected paths equal main.

Actual result: replay completed at `5d232eca31b1b44f67a9f9b741b5596a7038b473`;
only index/log additive conflicts and the authoritative score conflict.
Score-only replay became empty after taking main. All seven substantive
commits retained, with unchanged source and pre-existing tracking bytes.

<!-- rpi:phase id=P02 -->
## P02: Validation and local handoff

Context: C3-C6 define existing commands and local-versus-hosted limits.
No source or test ownership migration, new tests, removals or generated hashes.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Validate

From `src/core`, set
`PYTHONPATH=src:tests:../api/src:../api/tests:../agents/src:../agents/tests`;
from `src/api`, set
`PYTHONPATH=src:tests:../core/src:../core/tests:../agents/src:../agents/tests`.
Use `/tmp/mv/bin/python`, `/tmp/mv/bin/ruff`, `/tmp/mv/bin/mypy`.
Set `TMPDIR="$PWD"` from each stated project directory before Python starts,
so existing self-cleaning synthetic fixtures stay local to that worktree.
Set `PYTHONDONTWRITEBYTECODE=1`, use Ruff `--no-cache` and mypy
`--cache-dir=/dev/null`; remove only specifically identified outputs owned by
this invocation, if existing test cleanup leaves any.
Assert core/API/agents imports live under this worktree, not the shared
editable source. Disable cache/bytecode where practical.

Run each project's `ruff check .`, `ruff format --check .`, `mypy`.
Run core `test_form_review test_form_staging test_finance_match_controls
test_finance_signoffs test_grant_lifecycle_controls test_change_provenance
test_document_rescan test_scenario_manifest test_dependency_rule`.
Run API `test_form_staging_api test_finance_match_api
test_role_endpoint_inventory test_dependency_rule`.
Also run the existing adjacent `test_form_review_pack` module, separately
after the selected core group to cover saved diagnostic packs explicitly.
Full API discovery is not selected. No SQL/private-data/browser/cloud
acceptance claim. Record unexpected errors; resolve coupled local integration
errors before Review without altering historical evidence.

Completion evidence: actual exits/totals/skips, `git diff --check`, no new
legacy code/package-internal tests and protected-path preservation.

Actual result: core Ruff/format/mypy pass (112 formatted, 165 typed);
218 selected tests, 54 existing optional SQL Server skips. Existing pack module:
8 passed. API Ruff/format/mypy pass (59 formatted, 112 typed); 28 focused tests
passed, no skips. Imports use this worktree. Preservation assertions pass.

<!-- rpi:task id=P02-T02 -->
### P02-T02: Review and commit

Reconcile P01/P02-T01 markers, details and changes before one independent
integration Review. The reviewer may write only its named Review artifact.
Keep original research/critique/Review bytes and later corrective outcomes.
Route findings as separate follow-up work; do not loop back to implementation.

Before commit run `gh api user`, construct `{id}+{login}@users.noreply.github.com`,
set repository-local `user.email` and use for both author and committer.
Stage exact task/resolution files. Commit with a Conventional Commit and
`Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>`.
Use `Refs #96` / `Refs #510` only. No push.
Postcommit confirm clean status, ancestry/protected copies and committed
trailer/evidence. Metadata closeout commits are allowed without source change;
they are not a second Review or exact-head publication receipt.
