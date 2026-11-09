---
title: Infrastructure integration 136 metadata correction C2 research
description: Research for correcting two current-use metadata defects in the post-merge records of issue 136
ms.date: 2026-11-09
---

## Provenance

Written and committed before any correction edit. Research disposition: executed (read-only git, gh and log inspection on 2026-11-09). Parent task: `infrastructure-integration-136-pm`. This is correction cycle C2 of the default five scoped cycles for issue 136 (C1 closure is retained).

## Identities

* Branch `fix/demo-recovery-136-1109`, frozen clean start `fc6adc5c5d2dba6f2b2acdac25048e14fe3e2508`, tree `6df8ec47e465525d7d521fb4b01ed74921817dc9`.
* Freshly fetched `origin/main` `1f28d09130c8e058a0436d468e6a22f3c4c24f47` (github-actions bot rubric score commit). Its parent is `d4d6827fe60be651cd922ab9656688c18c978e1d` (PR 1222), the main imported by the merge commit `f2554acbd`.
* PR 1272: OPEN, base `main`, head `f16a398d400538b918eb965baf461cb2997a0c27` (unchanged, an ancestor of the candidate), `mergeStateStatus` CLEAN at retrieval, empty `statusCheckRollup`. No hosted check evidence was observed for head `f16a398d4` at that retrieval (2026-11-09); the claim is bounded to that head and time.

## Findings

* R1 Defect 1 (Medium, from the independent post-merge readiness review): `next_action` in `.copilot-tracking/rpi-sessions/2026-11-09/infrastructure-integration-136-pm-state.json` orders hosted checks on the new head before authorized publication. Hosted checks run only on a pushed head, so that order is impossible for a local candidate, and the old remote head `f16a398d4` cannot validate it. The correct order is independent exact-head and current-base assessment, then separately authorized forward PR-head publication or update, then actual new-head hosted checks, then gated merge. The same sentence pattern is in the PM review (Execution) and PM details (Phase 4) and the PM changes record line about hosted evidence reads as an outstanding coordinator action; only the state JSON `next_action` orders actions, so it is the corrected field. Other records are read as describing outstanding actions without an order and are superseded only by the dated correction note.
* R2 Defect 2 (Low): the PM plan Critique result names `claude-sonnet-5.5 harness default` for the independent critique. The preserved native stdout (`rpi-136-postmerge-refresh.log` line 76 in the coordinator session files) displays `Rubber-duck (model: gpt-6.1-terra) Critique post-merge plan` with verdict `proceed with changes`. Confirmed by direct read of that stdout before editing. The author of the plan and the native rpi-agent is Claude Sonnet 5.5, a different role from the independent critique agent. The verdict, findings PC-001 to PC-004 and the file's original history stay as recorded in the commits `008a8dea2` and `b1cf9b525`.
* R3 Overlap classification. `git diff d4d6827fe origin/main` is exactly one path, `.github/rubric/scores/latest.json` (bot score commit 78/100 with a new `commit`, `scored_at`, `run_url` and `solution-code` fingerprint). The candidate's non-tracking tree equals `d4d6827fe`'s (`git ls-tree -r` filtered by `.copilot-tracking/`, hash `61ce05d5...`) and is not equal to `1f28d0913`'s (`abf52b6c...`); the only non-tracking difference to current main is that one bot-generated file. PR 1272 as published (`f16a398d4`) changes only `.copilot-tracking/` paths (16 files, none non-tracking), so it does not overlap main's bot file; a trial `git merge-tree --write-tree HEAD origin/main` is clean.
* R4 The earlier "non-tracking equality" is equality with imported main `d4d6827fe`, not with the newer base `1f28d0913`. No claim of newer-base equality is made.
* R5 No source, test, infra, dependency, `docs/reference/log.md` or other non-tracking path needs an edit. Main's bot-only change does not alter intent, so no merge is performed (no blind merge); it is for the coordinator to re-evaluate at publication time against the then-current base.

## Planning readiness

Ready. Scope is two metadata corrections plus dated C2 records. No issue 136 acceptance criterion is proven; use `Refs #136`.
