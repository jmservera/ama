---
title: Issue 1204 exact schedule prompts phase details
description: Phase details for the coordinator schedule prompt persistence change
ms.date: 2026-11-17
---

## Phase 1 edit

In the Recurring schedules section:

* Keep the opening paragraph and existing bullets.
* After the snapshot bullet, add a "Startup and restart" bullet: list live schedules first (`manage_schedule` list); keep a matching active recurrence; create only a missing authorized 10-minute delivery or hourly cleanup; create or find cleanup first and, when instantiating the delivery prompt, substitute only its newly observed live handle for the historical `#2`; read back exactly one of each authorized recurrence (zero after a legitimate stop for pause, expiry or completed scope is correct and is not recreated) and apply the existing replacement and deduplication rules. Ids are runtime handles, never configuration or authority; do not assume ids 5 and 2 survive. Respect owner pause, completed scope, authority and expiry, current blockers and cleanup retention. Do not recreate unauthorized work.
* Honest limit: these are CLI session schedules (`/every [interval] [prompt...]`) that need a running coordinator session, not an OS service or autostart; `/restart` restores supported live sessions but documents no guaranteed schedule recovery. No storage path or API is assumed.
* Add "Approved prompt snapshots (2026-11-17)" with two fenced `text` blocks, delivery (historical id 5, every 10 minutes) and cleanup (historical id 2, hourly), copied verbatim from evidence-1204-refill/approved-live-prompts.json.
* Adjust the Provenance bullet: date-stamped as of 2026-11-05, add that the 2026-11-17 snapshots below are the approved bodies and the live list stays authoritative.

## Phase 2 validation

Extract each fenced block with Python, compare to the strings in /mnt/tmp/ama-run-74bd1fe9-1204-refill-20261117T1140/evidence-1204-refill/approved-live-prompts.json (equality and SHA-256); full `git status --short` (including untracked) shows only the one source file plus `.copilot-tracking` artifacts; frontmatter lines 1-5 unchanged; no non-ASCII added.
