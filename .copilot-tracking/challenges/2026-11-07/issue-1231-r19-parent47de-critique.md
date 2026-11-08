---
title: Issue 1231 r19 plan critique
description: Prospective one-pass author-only critique of the r19 merge plan
ms.date: 2026-11-07
---

Author-run, NOT independent, before mutation. Verdict: proceed.

| ID | Severity | Concern | Disposition |
| --- | --- | --- | --- |
| C-01 | High | Clean merge may hide drift. | Full raw/mode/blob delta proof. |
| C-02 | High | Child privacy, stage_retained, winner metadata and parent guards must survive. | Child blobs equal start; tests unchanged. |
| C-03 | Medium | log.md is append-only. | Zero deleted lines. |
| C-04 | Medium | Concurrent FULL elsewhere. | No heavy lock, service or main merge; light checks only. |
| C-05 | Medium | Namespace may include another worktree. | Print module origins. |
| C-06 | Low | Parent Mediums are author-corrected only; cross-UID, unsupported mount, directory-sync and future-date gaps remain. | Not claimed closed. |
