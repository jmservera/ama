---
title: Issue 462 live r5 research
ms.date: 2026-11-19
---

Session `rpi-462-live`, task `issue-462-live-r5`. Refs #462. Owner decisions 2026-11-18: synthetic demo, desktop only, live Azure authorised.

Research disposition: executed. Planning Readiness: Ready.

## Findings

* Unticked criteria: 1, 2, 6, 7. Criteria 1, 6 and 7 are proven for the demo in the r3 note (`docs/reference/research/resident-showcase-live-r3-2026-11-18.md`); the r4 fix for review thread `discussion_r4372517587` is already on main as `0d90c2bee` (#2112, `_usable_id` guard at `resident_preview.py` line 513).
* Criterion 2: PR #455 is MERGED (2026-10-25T21:25:42Z), #444 is CLOSED, but the review thread 4372517587 is still unresolved on GitHub. Resolving it, confirming no manual score edits and observing a hosted rubric rerun are maintainer/hosted actions; no push is allowed.
* Live refresh: `ca-resident-demo` is Running on image digest `sha256:65481780...bbbd19`; unauthenticated `GET /` returns 200 (first probe timed out on cold start), `/login`, `/api/case` and `/staff` return 404.

## Decision

No buildable or locally provable criterion remains; every remaining item needs a human or hosted action. Record evidence only, no source change.
