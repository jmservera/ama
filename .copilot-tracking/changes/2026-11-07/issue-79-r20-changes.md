---
title: Issue 79 changes, r20 merge of main 39506027
ms.date: 2026-11-07
---

Task `issue-79-r20-merge-main-1253`. Planning commit `482904dbd` preceded the merge; refs `preserve/issue-79-pre-main1253-merge` (start `cf5f57a0`) and `preserve/issue-79-r20-planning`.

## Chronology

* Start verified ignored-clean, PR 1239 open to main. Scorer run 42379486600 completed success; `origin/main` `39506027` is `95f7600d4` plus a score-only commit (only `.github/rubric/scores/latest.json`, valid JSON). Dry-run merge clean.
* Planning committed, main re-fetched unchanged, then `git merge --no-ff` produced `a9a7e1e42` (tree `60aef8522`), parents `482904dbd` and `39506027`. No conflict, rebase or rewrite.

## Proofs

* All 24 paths changed by main since `8af3aea6` have main's blob and mode in the merge, including `src/api/tests/test_assistant_release.py` (`48be02b95`, +46 -1, the received test). The 22 added 107 records and the score file are main's.
* Every topic path other than the score file keeps its pre-merge blob and mode; the score file differs from the start only because main's newer score takes over. No mode changes. Log additions only (this entry added afterwards).
* Runner SHA-256 `5987f45d...c878a08` and helper `500e31e4...df0c9` unchanged; import origin is this worktree.

## Checks (scratch `/mnt/ama-gates/g79-main1253-preparation-1107/`, `PYTHONDONTWRITEBYTECODE=1`, exits read directly)

* Core ranking publication and runner: exit 0, 53 tests OK, 0 skipped.
* API ranking wiring: exit 0, 15 OK, 0 skipped. Received `test_assistant_release.py`: exit 0, 46 OK, 0 skipped.
* Ruff 0.17.1 check and format check (five ranking files) exit 0; mypy 2.4.0 exit 0, 268 files. External caches; no ignored files created.
* Not run: FULL, SQL, browser, scanners, images. Environments are my earlier `/tmp` ones, origin proven.
