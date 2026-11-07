---
title: Issue 1231 r12 research (merge corrected parent 181a1c1bb and align the child)
ms.date: 2026-11-06
---

## Chronology statement (prospective)

Written just after the clock read 23:59:17Z on 2026-11-06 (last evidence command); this file is committed before any merge commit or source edit. An exploratory `git merge --no-commit` was run and aborted (`git merge --abort`) to read the conflicts; it left no commit, ref or file. Original R1 to R10 records, the r4, r7, r9 and r11 receipts and the r10 findings are preserved unchanged. The r11 FULL receipt is for head `ae23c0d72` and is historical, not current, for any new head.

## Trigger

Independent review of `ae23c0d72` (`files/review-1231-ae23/functional-findings.json` in the coordinator session, verdict pass-with-notes, partial): M1 no fsync before `os.link` (a crash can leave an empty record at the final name), M2 a corrupt or foreign record at the final name gives `JSONDecodeError` or `KeyError` and so a misleading 400/404 or a runner traceback, L5 brittle source-text test and stale `os.replace` patch, L6 gaps (corrupt-record test, multiprocess test, `ArchiveStorageError` to 503). The parent #79 head `181a1c1bb5e83c2ce08a7663d0a2b9145e6fc85e` (first-writer-wins, `mkstemp` unique temp, `fsync` file and directory, `_existing(path, snap)` validation raising `PublicationError`, `policy_signed` in audit and response, a structured status listing error) fixes the same findings in the parent helper.

## Evidence (read-only)

* Child HEAD `ae23c0d7274d1314ff632de268ad77e103d09ca6`, branch `fix/ranking-archive-concurrent-writer-metadata`, ignored-inclusive clean. Preserved prealignment ref `backup/issue-1231-ae23-pre-r12-align` at that head.
* Parent head `181a1c1bb` descends from the earlier parent `d654634fc` (merge-base). Two parent-only commits. Parent delta touches `ranking_publication.py`, `store.py`, `README.md`, `test_ranking_publication.py` and `test_ranking_publication_wiring.py`.
* `git merge-tree` reports content conflicts in `ranking_publication.py`, `store.py` and `test_ranking_publication.py`; `test_ranking_publication_wiring.py` and `README.md` auto-merge.
* Helper conflict: the child `_existing(path)` reads `published_on` unvalidated and stages with an own `O_EXCL` name and `_remove` with a `stage_retained` warning; the parent `_existing(path, snap)` validates and `_fsync_dir` exists. The child needs both: the parent validation and syncs, and the child unique staging with truthful retained-stage reporting.
* Store conflict: the child translates `OSError` to `ArchiveStorageError` and adds a `warning` for a retained stage; the parent adds `policy_signed`. Both are compatible.
* Test conflict: the parent adds a source-text test requiring exactly one `unlink` and the literal `os.unlink(tmp)`, which contradicts the child `_remove` helper (finding L5 names such tests as brittle). The parent also adds fsync, race, multiprocess and corrupt-record tests.
* The runner already catches `PublicationError` and `OSError` around `publish` (`ranking_publication_runner.py` line about 348); the parent leaves the runner unchanged, so the runner needs no edit.

## Design (within the existing contract)

* Keep the child unique exclusive stage and `_remove`/`stage_retained`; add the parent file `fsync` before `os.link` and the directory `fsync` after a successful link; adopt the parent `_existing(path, snap)` and `os.path.lexists` for the pre-check and for the lost-race branch.
* Store: keep the `OSError` to `ArchiveStorageError` translation and the retained-stage warning, add `policy_signed`, the audit detail wording and the status listing handling from the parent.
* Tests: keep every child test; replace the parent source-text `unlink` test with a behavioural assertion that no staging file remains and that the module has no clock; keep the parent behavioural tests; adapt the parent fsync test to the child stage name; leave no `os.replace` patch.

## Residual issue to record, not widen

A directory `fsync` failure after a successful link raises `OSError`, and the Store message says "Nothing was published", although the record is linked. A retry reports it already published. This is recorded as a Review finding for the owner; no new return state is invented here.

## Limits

Merge aligns ancestry only. It is not FULL validation, independent review, human approval or publication. No FULL, SQL, browser, image or scanner. Targets stay 1231 to 79 to 73; the parent remote is absent.

## Planning readiness

Ready. Disposition: executed (read-only evidence).
