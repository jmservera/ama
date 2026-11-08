# Changes: issue 1231 R13 alignment onto rewritten parent 11fb73f45

Date: 2026-11-07. Governing records: the R13 research and plan (commit 87023b2b4).

## Actions

* Preserved ref backup/issue-1231-f874-pre-r13-align at f87416add.
* Rebase onto 11fb73f45 attempted and aborted on a source conflict in ranking_publication.py and test_ranking_publication.py (first child source commit df0f2ede7). HEAD was unchanged afterwards.
* Merge commit 1eeb8d6c9 (parents 87023b2b4 and 11fb73f45), tree ada6a84b6, from `git merge-tree --write-tree --merge-base=181a1c1bb`: clean, no conflicts, no manual source edit.

## Proofs

* f87416add, 11fb73f45, 181a1c1bb, main 56eec736 and add72cc90 are all ancestors of HEAD.
* `git diff f87416add HEAD -- src tools infra .github` is exactly the 16 main-drift files (535 insertions, 21 deletions) identical to the parent's drift; no ranking file changed.
* Diff against 11fb73f45 in src is the 8 child-only files (ranking_publication.py, runner, store.py, server.py, three test files, core README).

## Checks (source-bound; /tmp/zf79venv, worktree src on PYTHONPATH, import origin in the worktree, PYTHONDONTWRITEBYTECODE=1)

* core ranking publication and runner tests: 63 run, OK, 0 skipped.
* api ranking wiring tests: 17 run, OK, 0 skipped.
* Ruff 0.17.1 check on src/api and the changed core files: pass; format check 118 files: pass.
* mypy from src/core: no issues in 268 files. git diff --check: clean. Ignored-inclusive status empty.

## Not done

No FULL gate, SQL, browser or installed-package run. Receipts g1231 r4, r7 (failed, preserved), r9, r11, r13 and g79 r17 do not cover this head.
