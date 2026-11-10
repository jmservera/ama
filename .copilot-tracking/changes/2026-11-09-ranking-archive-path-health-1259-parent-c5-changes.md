---
title: Issue 1259 frozen parent c5 integration changes
description: Changes record for the exact parent 52f9b61bb merge and Blob path-health adaptation
ms.date: 2026-11-09
---

## Ordered execution

Research, plan, details and one critique were committed (`bb93a4fd4`) before the merge and any source edit. Then: merge, failing-first probes, one source edit, targeted tests.

## Identities

* Merge commit: ordinary `--no-ff` merge of exact `52f9b61bb22c5ceaaed0f9bf6a55dab7a7a59cb8` (tree `20901b61eddb68d3740f6976187d17ff5fc0cea2`) into `bb93a4fd44eecc9cebf577ccd8c3d5a9127c3582`, commit `d16b25c7bbb7c5a5f9d4952a9e10c5a1816b0fd5` (parents bb93a4fd4 and 52f9b61bb). No rebase, reset, force, amend, push, PR, issue or board change. Fetched `origin/main` `daf45a46ca85b93cfac510ef6f8b2d685dec5136` recorded only; main was not merged and #1292 was not imported. Declared PR target stays the parent topic.
* The merge produced the predicted two conflicts. `ranking_publication.py`: both import sets kept (`contextlib`, `errno`, `stat`); `verify` takes the parent `Archive` signature and one docstring stating the Blob listing rule and the local-folder fixture rule. `test_ranking_publication_runner.py`: both classes kept. Only those two files were hand edited; `git diff 52f9b61bb d16b25c7b -- src` is limited to the child path-health hunks and tests.

## Failing-first probes (before the source edit)

* Core: new `BlobArchivePathHealthTests` plus `ConditionalCreateTests`: exit 1, 12 tests, 8 failures. Seven failures were the runner problem text for each unreadable Blob listing shape (403, 404, 500, transport failure, malformed body, later page fails, endless pagination): the child's generic fallback replaced the parent's fixed path-free Blob messages with `reason not available` (critique PC-2 confirmed). Unknown window, `archive_unreadable` refusal, zero PUT and secret-free output already held. One failure was a wrong probe assertion (`verify` status for a valid empty archive is not `ok` while overdue); the test was corrected, not the source.
* API Blob wiring probe (conditional create route does not list; status stays unreadable-shaped): exit 0, 12 tests OK without a source change; kept as regression coverage.
* Direct conditional create with an unreadable listing: passed without a source change; regression coverage (no invented listing dependency).

## Source change (one, minimal)

`ranking_publication_runner._verify`: for `BlobArchiveError` the fixed adapter message is shown (`str(e)`), otherwise the existing `e.strerror` or the child's generic fallback applies, so no arbitrary `OSError` text is restored. No change to `ranking_archive_blob.py` or the local-folder code.

## Tests added

* `BlobArchivePathHealthTests` (runner, mocked Blob transport): seven unreadable listing shapes are unknown for schedule, verify (overdue unknown) and publish (`archive_unreadable`, zero PUT, no blobs), with the expected fixed text and no account host, container or SAS in output; valid empty listing is a first run and publish proceeds.
* `ConditionalCreateTests`: conditional create with an unreadable listing succeeds with no list request.
* API `BlobPublicationWiring`: publish route is a conditional create with no list request while status reports the unreadable listing path-free.

## Results (DEMO targeted tier; PYTHONPATH to this worktree on a non-editable scratch venv; synthetic ZF_DATA)

* Baseline merged, before the new tests: core 143 OK exit 0; API wiring 35 OK exit 0.
* Final: core `test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents`: 146 OK, exit 0, no skips shown. API `test_ranking_policy test_ranking_publication_wiring test_ranking_scale`: 67 OK, exit 0, no skips shown.
* `ruff check` and `ruff format --check` (ruff 0.17.1) on the four changed files: clean after one format and one docstring-length fix. `mypy` 2.4.0 from `src/core` on `ranking_publication.py`, `ranking_publication_runner.py`, `ranking_archive_blob.py`: no issues, exit 0.
* Not run by tier or because unaffected: agents `test_cohort_ranking_eval` (no ranking module outside the runner changed), orchestrator, full core, SQL, browser, emulator, cloud, scanners, `rpi-checks`. Mocked REST contract tests are not Azure acceptance.
* Logs under `/home/azureuser/.local/share/ama/gates/g1259-parent-c5-int-1109/` (not committed).

## Routed, not fixed (PC-1)

The frozen parent listing parser reads only the first `NextMarker`: scratch probe `<NextMarker/><NextMarker>more</NextMarker>` returns the names with no error (`pc1-scratch-probe.log`). Real Azure does not emit duplicate markers. Fixing it needs a change to the parent-owned adapter, whose budget is five of five spent. Policy choice for the owner: authorize the child to patch the parent adapter (diverging from the independently approved head) or give the parent a new cycle. Only that scope stops; nothing was committed for it.

## Cycle count

Historical productive review-correction cycles: 0. This task: 1 consumed. Final: 1 of 5, four remaining. No reset or extra grant.
