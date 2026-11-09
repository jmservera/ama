---
title: Ranking archive ancestor durability 1258 correction 3 review
description: Authored review of correction 3, executed once after implementation
ms.date: 2026-11-08
---

Authored review, one execution, of correction 3 at the commit that adds this file. Outcome: Blocked on a platform-contract decision (residual race PC3-1) with the rest Residual work. It is the author's own review, not independent. Earlier Reviews, critiques, the cbb1cc5b receipt and the c1 and c2 outcomes are unchanged and not regraded.

## Checked

| Item | Result |
| --- | --- |
| Link and sync target the same folder (PC3-2) | Done by `dir_fd` anchoring; path swap before and after the link is unconfirmed; real-file tests. |
| Record identity during confirmation (PC3-3) | Removal or replacement during a sync is unconfirmed; real-file tests. |
| Parent chain and mount ids unchanged across the syncs (c2 PC-002, partly) | A mount id change between walks is unconfirmed; mocked mount ids. |
| Bind-mount and Btrfs-shaped boundaries (c2 PC-001, PC-004) | Mount ids per descriptor replace the mount table and mountinfo ordering; mocked ids only. |
| Unknown mount data or open failure | Existing unconfirmed path; core and API tested (record kept, original date, path-free 409, audit, sound retry). |
| First-run behaviour, private stage, retry, concurrent loser, owner-only mode, symlinked parent | Core 57 and API 24 pass, no skips. |
| Red before fix | Preserved (core 11 of 28, API 1 of 24); intermediate green attempts retained. |
| Order of work | Research, plan and one critique were committed (c577eea9e) before any source or test edit. |

## Blocking

* PC3-1: a folder moved or remounted and restored inside one confirmation is not detected, so a confirmation could still cover an entry created after its parent's sync. It needs the owner platform-contract decision in the critique record (options A to D; author recommendation A with deployment control, optionally B after platform review). Not decided, not accepted, and the result is not declared conformant for that window.

## Residual work

* R1 real power loss and live-filesystem durability; R4 sync cost, now about double the walking and `/proc` reads per confirmation. Unmeasured.
* Real bind mount, Btrfs subvolume, chroot, container and overlayfs behaviour unproved; `mnt_id` in fdinfo needs Linux with `/proc` mounted, otherwise the existing unconfirmed path applies; platforms without descriptor-relative calls are now refused before writing, a change from c2 that is part of the unapproved platform contract.
* Pre-existing operator symlinks, execute-only ancestors and deployment-permission acceptance remain unproved.
* The author's dispositions of the critique were not re-critiqued (one critique only in this cycle).
* FULL for the final candidate, current-base receipt and verification, independent exact-head assessment, hosted checks and named approvals are not performed. The old cbb receipt is historical.
