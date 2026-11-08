---
title: Issue 1231 r20 plan critique
description: Prospective one-pass author-only critique of the r20 merge plan
ms.date: 2026-11-07
---

Author-run, NOT independent, before mutation. Verdict: proceed.

| ID | Severity | Concern | Disposition |
| --- | --- | --- | --- |
| C-01 | High | Clean merge may hide drift. | Full raw/mode/blob delta proof. |
| C-02 | High | Child privacy, stage_retained, winner metadata and parent guards must survive. | Child ranking blobs equal start; tests unchanged. |
| C-03 | Medium | log.md is append-only. | Zero deleted lines. |
| C-04 | Medium | Incoming src test file means src is not wholly unchanged. | Claim only the exact paths. |
| C-05 | Medium | Known formatter diagnostic on incoming tests. | Preserve; no reformat. |
| C-06 | Low | Unmasked exits and own-source origin. | Per-command exit files; print origins. |
| C-07 | Low | Parent Mediums unconfirmed; cross-UID, unsupported mount, directory-sync, future-date gaps remain. | Not claimed closed. |
