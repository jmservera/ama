---
title: Ranking archive ancestor durability 1258 correction 1 review
description: Authored review of the correction 1 implementation
ms.date: 2026-11-08
---

Authored review, executed once, of correction 1 (source at the commit that adds this file). Outcome: Residual work. Prior Reviews, outcomes and the cbb1cc5b FULL receipt are unchanged history.

## Checked

| Item | Result |
| --- | --- |
| H1 permission cutoff cannot falsely confirm | Fixed. No `os.access` use; a failed ancestor then a chmod retry stays unconfirmed (non-root test, uid 1000) and succeeds only after the sync passes. |
| M1 archive mount point | Fixed for the `os.path.ismount` meaning; tested by mock only. |
| First-run behavior, private staging, record and original date on failure, path-free messages | Unchanged code; Core 89 and API 23 pass. |
| Criterion 4 503 | Two named API tests executed (see Changes), not an aggregate inference. |
| Red before fix | Preserved (3 failures, 1 error in 13). |
| Static checks | ruff and mypy clean on touched paths. |

## Residual work

* R1 real power-loss and live-filesystem durability remain unproven. Tests use mocked fsync order and a temporary directory.
* R4 steady-state extra directory syncs remain; a deeper chain adds more. No measurement.
* PC-001 bind mounts and PC-004 Btrfs subvolumes are not detected by `ismount`; fail-closed but unfixed.
* PC-002 pre-existing operator symlink durability is not asserted.
* PC-003 an ancestor that is not readable makes every publication unconfirmed; deployment permissions and owner acceptance are untested.
* The mount cases are mocked; no real mount was created. The privileged path is mocked; the real chmod case ran as uid 1000 only.
* The race-loser path has no ancestor-specific test (same `_confirmed`; existing loser test covers directory-sync failure).
* A real stage in this change: code was drafted before the critique (disclosed in the critique).

## Not performed

Fresh FULL local gate and receipt on the new head, external verification, independent exact-head assessment, hosted checks, qualified-human and whole #79/#1231 approval, and any issue criterion tick or closure. The cbb1cc5b receipt no longer applies. This review is the author's own and is not independent.
