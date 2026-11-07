---
title: Issue 1231 plan r5 (unsupported hard link and committed-cleanup error boundaries)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written about 13:58Z after the r5 research and before any rebase, test run or edit. Details are in the matching details file. One independent plan critique will run on this plan and be recorded in `issue-1231-r5-error-boundaries-critique.md`; it will not be repeated.

## Phases

* [ ] Phase 1: commit research, plan, details, critique and state (this stage, before anything else).
* [ ] Phase 2: local integration. Create backup ref `refs/heads/backup/issue-1231-b7f6186-pre-r65-rebase` at `b7f6186` (refuse if it exists), verify parent, source, main and clean status, then rebase the child onto `43080ab42a96fada36b9d0bc523dfa16fe0c3cd5` with fresh repository-local noreply identity. Stop with exact paths on irreconcilable conflict.
* [ ] Phase 3: tests first. Add regressions, run them RED on the rebased unchanged source, keep raw outputs under `/mnt/ama-gates/e1231-r5-r65-1106/`.
* [ ] Phase 4: correction. Helper (`stage_retained`, `ArchiveStorageError`), runner (warning and field), Store (translate, audit, log), server (503 mapping), README sentence.
* [ ] Phase 5: GREEN focused core and API tests, Ruff check and format, mypy on edited source; import proof from this worktree.
* [ ] Phase 6: Changes record, separate later author Review, state; commit and freeze.

## Scope and non-goals

* Two own-child Medium findings only. No change to helper schema validation, non-directory residual, ranking algorithm, parent runner behaviour, auth handling or the hard-link contract.
* No FULL, SQL, browser, container, image, scanner, install, lock queue, cloud, deployment, cleanup or publication.

## Acceptance (light)

* EPERM and ENOTSUP at `os.link` through Store and the manager route yield 503 with a non-auth, path-free, actionable message, no final record and no audit entry; role 403 checks unchanged.
* With real `os.link` succeeding and only the stage unlink failing, the helper returns committed metadata with `stage_retained`; the runner reports `published`, `written` true and a warning; Store audits the publication and logs a warning. The stage stays; no foreign file touched.
* All existing helper, runner, concurrent-writer, collision, retention and policy tests unchanged and passing.
