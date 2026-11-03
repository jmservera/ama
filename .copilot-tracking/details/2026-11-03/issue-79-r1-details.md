---
title: Issue 79 phase details
ms.date: 2026-11-03
---

* Archive name `ranking-{version}-{as_of}-{hash12}.json`; record is `published_on` plus the snapshot. Identical snapshot is not rewritten; first publication date is kept.
* `verify` reports edited content, wrong file name, unknown policy version or hash, unreadable files, as plain sentences.
* `SCHEDULE.owner` is "to be named" and `retention` is "not set".
* Manual path: managers still read `/api/ranking/snapshot`. No AI involved.
