---
title: Issue 79 research, r19 merge of main 8af3aea6
ms.date: 2026-11-07
---

Task `issue-79-r19-merge-main-8af3`, parent `issue-79-r18-357-assessment-corrections`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Start: branch `feat/ranking-publication-runner-79`, head `87c027a30ba5a1dd5e4f16b01052e7c32a09138c`, tree `f391682d93bac1ce9ec256c6d02dfebf9bda4dc4`, ignored-clean. PR 1239 targets `main`. Child 1231 local `5f904c29` is not touched.
* Freshly fetched `origin/main` is `8af3aea6b042f5dfb3305e18334439717f7c5649`; merge base with the topic is `0f420dc9514db22081cb48fa733267d9d33a0d24`. Incoming commits: `a7f166c74` docs 1247, `7551e50e9` browser readiness 1249, `8af3aea6b` score-only bot commit.
* Incoming delta: 27 paths, 813 insertions, 12 deletions: tracking records, `docs/reference/README.md`, `docs/reference/resources/ai-tokenomics.md`, `src/api/checks/case_journey_browser_check.py`, `.github/rubric/scores/latest.json`, `docs/reference/log.md`.
* Overlap with topic changes: only `docs/reference/log.md` (both append at the end). `git merge-tree --write-tree HEAD origin/main` completes with no conflict (tree `46a98241dc8a`). No overlap with ranking, publication, runner or tests.
* Preserve ref created before integration: `preserve/issue-79-pre-8af3-merge` at the start head.
* The three original Medium findings of the 357e842d assessment were corrected by r18 and checked only by the author's tests and Review; no independent confirmation exists. They are not relabelled resolved by an independent party.

## Conclusions

* One normal merge of the exact main commit is the least disruptive path: no rewrite of the 20 existing topic commits, ancestry of earlier evidence and child stack preserved. A rebase would rewrite hashes already cited and stacked on.
* Expected result: log.md auto-merges with append-only entries kept.

## Limits and unknowns

* The merge changes the browser check source in `src/api`; no browser run is admitted, so that file is verified only by blob identity to main.
* FULL is not admitted (#107 owns the sole FULL); earlier receipts do not cover this head.
