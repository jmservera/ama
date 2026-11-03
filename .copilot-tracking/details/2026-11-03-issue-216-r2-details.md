---
title: Issue 216 round 2 details
ms.date: 2026-11-03
---

* Input record: `alert_id`, `reviewer`, timezone-aware `published_at`, `classification` (`true_positive`, `false_positive` or null), optional `acknowledged_at` not before publication.
* Thresholds: `owner`, `agreed_on`, `min_alerts`, `min_precision`, `max_median_ack_seconds`; any gap reports `unset_pending_owner_agreement`.
* Output: two checks, counts of unclassified and unacknowledged, invalid records excluded and named, `overall_pass` null.
