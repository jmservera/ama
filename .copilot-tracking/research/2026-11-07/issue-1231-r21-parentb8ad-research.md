---
title: Issue 1231 r21 research, local alignment to parent79 b8ad4a0e
description: Prospective research for one normal merge of local parent79 b8ad4a0e carrying score-only main 23b26a7f
ms.date: 2026-11-07
---

Disposition: executed (read-only), committed before the merge. r15 deviation and r16 to r20 records are preserved unchanged.

* Child start 8d2350a5eda4f1ff41e418cabb51c01f81c7d883 / tree 9bcda840, ignored-clean, branch fix/ranking-archive-concurrent-writer-metadata. PR1242 OPEN, base feat/ranking-publication-runner-79.
* Local parent79 b8ad4a0e607fca85cef198f6428cd41c758b04b0 / tree 8c9b7aa994446f91ab330b3bc1c9042a1f0b0c47, ignored-clean. Merge-base is prior parent 0a8ecd50. Stale remote parent not used.
* Main 23b26a7f3a4693cd20dcf0447303d97491096cb3 (score-only, admitted by the coordinator) equals origin/main, is an ancestor of the parent, and is NOT yet in the child. The gate requires it as an ancestor of every stack member, so this merge supplies it.
* Incoming 0a8ecd50..b8ad4a0e: commits b6f61c059, a24cae019, b8ad4a0e6 plus main 23b26a7f. Outside .copilot-tracking: .github/rubric/scores/latest.json and docs/reference/log.md (append-only). No executable, test, tool or config change.
* Dry run clean (tree 449f725b before planning files).
* Because every executable/test/tool/config blob is unchanged, the r20 test results stay historical and are not rerun; blob identity is the proof. A static proof of unchanged src, tools and tests blobs replaces new runs.
* Qualification of r20 RV-002: its claim that the wider tools/ Ruff diagnostics (111 errors, 16 files) were "baseline from main" was not verified by rerunning them on main. tools/ is identical to main 23b26a7f, which makes it plausible but the exact counts were not reproduced on main. The original review is preserved unedited; this record and the r21 review append the qualification.
