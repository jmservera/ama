---
title: Issue 79 research, r20 merge of main 39506027
ms.date: 2026-11-07
---

Task `issue-79-r20-merge-main-1253`, parent `issue-79-r19-merge-main-8af3`. Research disposition: executed. Planning readiness: Ready.

## Evidence

* Start: `feat/ranking-publication-runner-79`, head `cf5f57a0084bb3ade9b53c7d2884e0db8367c20c`, tree `dd20fdc71e7385c024c90e970fcc7d92fc1dd49b`, ignored-clean; PR 1239 open, base `main`. Child 1231 is not touched.
* `origin/main` is `3950602754437c21d20e91c49ddc1589426e7d1b`: PR 1253 merge commit `95f7600d4` plus one score-only bot commit. Scorer run 42379486600 on `95f7600d4` is `completed`/`success`. The descendant changes only `.github/rubric/scores/latest.json` (parses as JSON; parent is `95f7600d4`).
* Delta against previous main `8af3aea6`: 22 added 107 RPI record files, `.github/rubric/scores/latest.json`, and the modified test `src/api/tests/test_assistant_release.py`. No production, schema or workflow path.
* Overlap with topic-changed paths: only the rubric score file, which `git merge-tree` merges without conflict. No ranking, publication, runner or log overlap.
* Preserve ref `preserve/issue-79-pre-main1253-merge` at the start head.
* The three 357e842d Medium findings stay author-corrected only, not independently confirmed.

## Conclusions

* One normal merge of exactly `39506027` is safe and keeps all history. Whole 107 remains open on its own gaps; nothing here changes that.

## Limits

* No FULL, SQL, browser or heavy lock. The incoming test is verified by blob identity, and run only if it is directly relevant and light.
