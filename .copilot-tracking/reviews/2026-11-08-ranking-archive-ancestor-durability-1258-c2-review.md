---
title: Ranking archive ancestor durability 1258 correction 2 review
description: Authored review of correction 2, executed once after implementation
ms.date: 2026-11-08
---

Authored review, one execution, of correction 2 at the commit that adds this file. Outcome: Residual work. It is the author's own review, not independent. Earlier Reviews, critiques, the cbb1cc5b receipt and the e40 Residual outcome are unchanged and not regraded.

## Checked

| Item | Result |
| --- | --- |
| PC-001 bind mount (archive and archive-inside-mount) | Fixed in the mount-table logic; tested with a mocked mount table only. |
| PC-004 Btrfs subvolume false boundary | Fixed in logic: a non-mounted subvolume root no longer ends the chain; tested with mocked `ismount` and mount table, not a real Btrfs. |
| Unknown mount data | Explicit `DurabilityUnconfirmedError` through the existing path; core and API tested (record kept, 409, audit, sound retry). |
| Hidden mounts (critique PC-001) | Ignored by a later-mount rule; tested. |
| First-run behavior, private staging, retry, original date, symlink realpath, path-free messages | Code unchanged; Core 95 and API 24 pass. |
| Red before fix | Preserved (core 10 of 18, API 1 of 24). |
| Order of work | Research, plan and critique were committed before any code or test edit. |

## Residual work (unproved or open)

* R1 real power-loss and live-filesystem durability; R4 extra steady-state syncs, now plus one `/proc/self/mountinfo` read per confirmation. Unmeasured.
* Mount topology is assumed stable during a confirmation (critique PC-002); no descriptor-based detection. Deployment assurance is a human item.
* The later-line-hides-earlier rule relies on mountinfo ordering; chroot, container-relative mountinfo and overlayfs durability are not validated.
* Linux only. Where `/proc/self/mountinfo` is missing the result is `committed_unconfirmed` on every publication. Whether to support other platforms is a human decision, not assumed.
* No real mount, bind mount or Btrfs volume was created; those cases are mocked and named so.
* Pre-existing operator symlinks, PC-003 execute-only ancestors and deployment-permission acceptance remain unproved; no owner acceptance is claimed.
* Race-loser path has no ancestor-specific test (shared `_confirmed`).

## Not performed

Fresh FULL gate and receipt on the new head, external verification, independent exact-head assessment, hosted checks, qualified-human approval and any criterion tick or closure. The cbb1cc5b receipt and any e40 evidence no longer apply to this source. The independent critique's blocking items PC-001 is applied and PC-002 is open as a human ledger item.
