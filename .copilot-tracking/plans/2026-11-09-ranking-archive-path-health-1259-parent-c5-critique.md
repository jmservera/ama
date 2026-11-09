---
title: Issue 1259 frozen parent c5 integration critique
description: One prospective critique pass of the parent c5 integration plan with dispositions
ms.date: 2026-11-09
---

## Execution and verdict

Critique executed once (rubber-duck, read-only, 2026-11-09) against research, plan and details before any merge or source edit. Verdict: Revise-level (one Significant, two Minor). Not repeated for this task.

## Findings and dispositions

* PC-1 (Significant): the parent `_parse_listing` reads only the first `NextMarker`; a duplicated marker element (an empty one before a non-empty one) ends the listing early without an error, which could report a truncated or empty archive as healthy. Verified against `52f9b61bb:src/core/src/zava_forward/core/ranking_archive_blob.py` lines 55 to 76: `root.findtext("NextMarker")` returns the first match. Disposition: a scratch-only failing-first probe will establish whether it fails. It is a defect in the independently approved, frozen parent adapter (parent budget five of five spent, no further cycle without owner authorization), real Azure does not emit duplicated markers, and a child edit to the adapter would duplicate and diverge from the parent. So it is not fixed here and no failing test is committed (a failing selected test is not waivable). It is reported in the Changes, Review and handoff as a routed parent-owned follow-up, with the exact policy choice (child patches the frozen parent adapter versus parent receives a new authorized cycle). Only that scope stops.
* PC-2 (Minor): the child's runner fallback `e.strerror or "reason not available"` hides the parent's fixed Blob messages. Disposition applied: the plan now states the expected runner text for representative Blob errors. The fixed adapter messages (HTTP status, "storage unreachable", "listing was unreadable") are path-free by construction and tests assert that; if the probe shows they are replaced by "reason not available", restore the fixed text for `BlobArchiveError` only, without restoring arbitrary `OSError` text from local errors.
* PC-3 (Minor): coverage gaps. Disposition applied: add a Store/API-route probe asserting no list request on conditional publish with an unreadable listing, and a probe where the first page succeeds and a later page fails, asserting `archive_unreadable` and no PUT.

## Outcome

Compatible findings applied directly to the plan (phase 4 and the test matrix); PC-1 routed as above. No significant divergence from user direction needs a user decision beyond the reported policy choice.
