---
title: Issue 1231 r16 changes, alignment to parent79 87c027a30
description: Implementation record for the local merge of parent79 87c027a30 into the child
ms.date: 2026-11-07
---

## Changes

* Backup refs created: `backup/issue-1231-a4ada-pre-r16-align` (a4ada1e9, source baseline) and `backup/issue-1231-1321b-pre-r16-merge` (1321be55, planning head).
* Authorised format-only amendment: commit 1caf7b47 added YAML frontmatter (title, description, ms.date) to the four r16 prospective files and removed their redundant H1. Substantive content and critique outcomes are unchanged. The original commit 1321be55 is preserved and not rewritten.
* Dry-run `git merge-tree --write-tree --merge-base=357e842d HEAD 87c027a30` was clean (tree e43612fb, which includes the four planning files; the researched a00c8d19 predated them).
* Normal `git merge --no-ff` of 87c027a30 into 1caf7b47 with no conflict. Merge commit 2677cfd6e016a9c39126878afb8f919864f2d256, tree cde6917fa4c36971a30f4ea2a81b3dc591acf108, parents 1caf7b47 and 87c027a3.
* No source or test edit was made by this iteration. Source diff against a4ada1e9 is the parent's runner, runner test, core README and log.md hunks plus parent r18 records.

## Static proof

* ranking_publication.py, store.py, test_ranking_publication.py and the API wiring test blobs are identical to a4ada1e9.
* The only stage open is `os.open(..., O_EXCL, 0o600)`; no 0o666.
* The merged runner contains `_policy_problem`, `_future`, `stage_retained` and the blocked exit.

## Checks (PYTHONDONTWRITEBYTECODE=1, /tmp/zf79venv, PYTHONPATH to this worktree)

* Import origin of ranking_publication_runner is this worktree.
* Core `tests.test_ranking_publication tests.test_ranking_publication_runner`: 70 OK, 0 skipped.
* API `tests.test_ranking_publication_wiring`: 18 OK.
* Ruff 0.17.1 check passed; format check: 331 files already formatted.
* mypy src/core: 268 files clean (external cache).
* `git diff --check` clean. Ignored-inclusive status empty. No failures occurred.
* No interaction gap was demonstrated, so no regression was added and no assertion was changed.

## Not done

* FULL, SQL, browser, images, scanners, push, PR, ticks, parent or main mutation. No cross-UID observation. Earlier receipts (r14, g79) do not cover this head.
