---
title: Issue 79 research, continuation r17 (rebase onto post-891 main)
ms.date: 2026-11-07
---

Task `issue-79-r17-align-post-891`, parent `issue-79-r15-d654-review-corrections`. Research disposition: executed. Planning readiness: Ready, subject to the base gate below.

## Evidence

* Local topic head `11fb73f4543b1ccf12d11eded0b3fdee766ffb90`, tree `a82c7745cb936c8f0f1095a6855031a0f03ada4c`, ignored-clean. Remote `origin/feat/ranking-publication-runner-79` and open PR 1239 (base `main`) are at `181a1c1bb5e83c2ce08a7663d0a2b9145e6fc85e`; the local head is one commit ahead only by the unpublished r15 work (`e87537cc7`, `11fb73f45`).
* Merge base with `origin/main` is `add72cc9013ab84a36a240e635cc4417dae714d3`; the topic has 18 linear commits above it and no merge commits.
* Fresh `origin/main` is `312fa3dcc4866deadf51336f840954852f0ec061` (PR 1245, issue 891, merged 2026-11-07T09:49:16Z), parent `add72cc90`.
* The post-merge Capstone Rubric Scorer run 42361331168 on that commit was `in_progress` when read. Earlier runs on main were followed by a score-only bot commit (`add72cc90 chore(rubric): record score 77/100`), so main may move once more.
* Main since the merge base changed 12 paths (891 chat demo records, `docs/reference/log.md`, `src/api` chat widget, check, test and README). The topic changed 65 paths. The only overlap is `docs/reference/log.md`: the topic appended four dated entries at its end and main appended one 891 entry at its end.
* Preserved exact ref created before any rewrite: `preserve/issue-79-pre-r17-align` at `11fb73f45`.

## Conclusions

* Expected conflicts are confined to `docs/reference/log.md` append-only tail collisions, in the commits that touch it (`92d73ce81`, `d82f7adb2`, `3111f9835`, `5c43eb1c6`). The right resolution keeps main's lines unchanged first and then the topic's entries in original order. No source file conflict is expected.
* A heavy gate on a base that is about to gain a score-only commit would be wasted, so the final base is frozen only after the scorer completes.
* The rewrite diverges local from the remote topic; a later publication needs an owner-approved lease push. Not performed here.

## Limits and unknowns

* The scorer's final outcome and any bot commit are unknown at the time of writing; recorded in Changes.
* No FULL is run in this session; old r14 and r16 receipts and the child receipts are historical and are not counted for the aligned head. Independent exact-head review, hosted CI, named policy-owner signoff and Legal retention remain unproven.
