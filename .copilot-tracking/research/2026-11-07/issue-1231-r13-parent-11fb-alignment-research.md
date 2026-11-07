# Research: issue 1231 R13 alignment onto rewritten parent 11fb73f45

Date: 2026-11-07. Research disposition: executed (git ancestry and tree evidence only). Planning readiness: Ready.

## Evidence

* Child HEAD f87416add57a0064494c5ea96e3955f6cc2db11f (tree 9d47bdad). Clean, ignored-inclusive. Preserved ref backup/issue-1231-f874-pre-r13-align.
* Old declared parent 181a1c1bb is an ancestor of HEAD. The coordinator's prepared parent 11fb73f4543b1ccf12d11eded0b3fdee766ffb90 is a rewritten line: it does not contain 181a1c1bb, it contains main add72cc90, and its merge-base with HEAD is main 56eec736.
* `git diff 181a1c1bb 11fb73f45` on the ranking source and tests (ranking_publication*.py, store.py ranking parts, ranking tests) is empty. The parent's ranking behaviour is unchanged. The 535-line source drift is main content only (api checks, form staging, list export, quality, projection).
* Attempted `git rebase --onto 11fb73f45 181a1c1bb`: the first child source commit df0f2ede7 conflicts in ranking_publication.py and test_ranking_publication.py (the old child commits predate the parent's first-writer-wins publish). Rebase aborted (`git rebase --abort`), HEAD unchanged. Resolving 5 intermediate source commits would invent intermediate states that never existed, so a rebase is not used.
* `git merge` of 11fb73f45 uses merge-base 56eec736 and conflicts with add/add in four files. `git merge-tree --write-tree --merge-base=181a1c1bb HEAD 11fb73f45` (old parent as the common content base) is clean and gives tree cc1cdc59 (before this record commit). Its ranking files differ from HEAD by nothing and differ from the parent only by the child-only changes.

## Selected approach

A two-parent merge commit (HEAD, 11fb73f45) whose tree is the clean 3-way result with the old parent as the content base. No source intent is re-decided: parent behaviour and the #1231 concurrent-writer metadata, ArchiveStorageError, stage_retained and tests stay as resolved in R12.

## Limits

No FULL gate (waits for #891 and main to settle). Old receipts r4, r7, r9, r11, r13 (g1231) and g79 r17 are historical, not current. No push, PR update or retarget (PR 1242 still targets feat/ranking-publication-runner-79). Author review is not independent assessment.
