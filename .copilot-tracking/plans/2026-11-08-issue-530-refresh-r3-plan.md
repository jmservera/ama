---
title: Issue 530 focused-gate refresh r3 plan
ms.date: 2026-11-08
---

* Research: [.copilot-tracking/research/2026-11-08-issue-530-refresh-r3-research.md](../research/2026-11-08-issue-530-refresh-r3-research.md)
* Details: [.copilot-tracking/details/2026-11-08-issue-530-refresh-r3-details.md](../details/2026-11-08-issue-530-refresh-r3-details.md)
* All earlier plans, reviews, the r1 receipt and adverse evidence stay unchanged. Tier FOCUSED, tracking-only, contingent on the post-merge proof.

## Phases

* [x] Phase 1: independent critique of this plan, then commit research, plan, details and critique alone.
* [ ] Phase 2: one normal merge of fetched `2e0c676a` into this branch; prove ancestry, `src`/`tools`/`infra`/`.github` trees equal Main, post-merge `<main>...HEAD` set inert-only, chat blob attribution.
* [ ] Phase 3: write changes, review and state records; commit; freeze ignored-clean.
* [ ] Phase 4: one attached `--changed` gate and partial verification against freshly fetched Main.

## Stop rules

Stop without guessing on: Main differing from `2e0c676a`, a merge conflict, any non-inert path in the post-merge set, tree inequality with Main, a held lock, any selected group other than `preflight,namespace,static`, any late commit, or a failed, interrupted or receipt-less gate, a failed verification or a failed proof; preserve all adverse evidence. No rebase, force, push, resume, waiver or source edit.
