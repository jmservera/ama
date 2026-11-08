---
title: Issue 79 plan, continuation r5
ms.date: 2026-11-05
---

* [x] Phase 1: verify each generated path exactly (type, symlink, tracked, git-ignored, owner, creation time, expected member names), write a finite manifest and hash archive outside the checkout.
* [x] Phase 2: remove only manifest files individually after readback and per-file hash match, then `rmdir` the now-empty directories one by one.
* [x] Phase 3: report the typing coverage; no code change unless a tightly coupled defect is shown.
* [x] Phase 4: record evidence, commit once, freeze.

Details: [details](../../details/2026-11-05/issue-79-r5-details.md). Research: [research](../../research/2026-11-05/issue-79-r5-research.md).

Critique (single pass, self-run, final candidate): no `rm -rf`, wildcard, age rule or name-only deletion; a directory is removed only with `rmdir` after every member file was individually eligible; any refusal aborts the whole run before removal. Private datasets are untouched: the one `support/` directory held only bytecode with sibling sources present. The `egg-info` removal does not affect the editable installs (they point to the main checkout). Findings applied directly; none conflicts with a confirmed decision and none is significant or divergent. Tier: focused (no infrastructure, SQL, deployment or security change); the FULL requirement from the r4 plan is unchanged and still pending.
