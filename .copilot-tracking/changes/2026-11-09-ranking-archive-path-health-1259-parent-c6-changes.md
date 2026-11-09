---
title: Issue 1259 frozen parent C6 integration changes
description: Executed merge, hand resolution and local checks for exact parent 99814198
ms.date: 2026-11-09
---

## Summary

Integration only. No product source file was edited by hand; the only hand edit is the mechanical resolution of one test-file conflict. No review-correction cycle spent (C1 and C2 spent, three remain by default; none granted).

## Order of events

* Prospective research, plan, details and critique committed as `fee97f971` before the merge.
* `git merge --no-ff` of exact `99814198079c7c8fcd641497826986c706627b0f` gave one conflict in `src/core/tests/test_ranking_archive_blob.py`: the child's C2-typed conditional-create test sat above the method the parent annotated `-> None`. Resolution kept both (child test, then the parent's annotated method); no marker remained. Merge commit `b3e58e2d7`, second parent `99814198`, tree `e47d24dea`.

## Proofs

* Own range over the parent (`git diff 99814198 HEAD -- src tools infra`): 5 paths, +291/-3, identical to the earlier own range.
* Blob equality with the Azurite-qualified `7fc680d0e` at the merged HEAD: `ranking_archive_blob.py` `346784573abf`, `documents.py` `ca026b8c1b64`, `ranking_publication.py` `ed2879856e4d`, `ranking_publication_runner.py` `0ea15181038a` all equal. `ranking.py` differs by the parent's annotation-only change (imports and a typed `snapshot` signature).
* Checks (owned scratch `g1259-parent-c6-1109`, Python 3.12.3, ruff 0.17.1, mypy 2.4.0, CI-style editable install of the worktree, `azure-storage-blob` 12.31.0 in the API venv): ruff check, ruff format check and mypy exit 0 for core (226 formatted, 279 mypy files) and API (127, 203), child and the parent export identical.
* Tests: core `test_ranking_archive_blob test_ranking_publication test_ranking_publication_runner test_documents` 146 OK; API `test_ranking_publication_wiring` 36 OK; no skips. A first core run with two wrongly named modules (wiring is an API test; `test_ranking` does not exist) errored on import only and was replaced.
* Log manifest `SHA256SUMS` (32 files) in `$S/logs`; not committed.

## Not run

Azurite (not re-run; evidence reuse is limited to the adapter inputs above, never a claim on the merged tree), SQL, browser, full gate, hosted CI, real Azure, WORM, deployment, model calls.
