---
title: Issue 1231 r28 plan critique (author, one pass)
description: Author critique of the root propagation plan before mutation
ms.date: 2026-11-07
---

Execution: complete, author-only, not independent. Verdict: proceed with the changes below applied.

* Risk: copying the root tests unchanged would not trigger their fault, because of the `.publishing-` prefix. Disposition: adapt to the child's stage name.
* Risk: taking the root `publish` body would drop `_confirmed` re-sync and the unique stage. Disposition: keep the child helper.
* Risk: a rebase would rewrite PR #1242 history. Disposition: normal merge, disclosed.
* Risk: duplicate README wording. Disposition: state `stage_retained` once.
* No conflict with confirmed decisions; no owner decision needed.
