---
title: Research for issue 110 live IoT Hub to SQL rerun (demo)
ms.date: 2026-11-18
---

Refs #110. Task `110-live2-20261118T1349Z`, slug `issue-110-live2`. Demo scope, desktop, owner-authorised live Azure (rg `ama`, cap USD 700).

## Disposition

Research disposition: `reused` plus a bounded new probe.

* Issue state: one unticked criterion (C1, distinct Hub identity with schema version and stable reading ID); C2 to C5 are ticked.
* Prior worktree `issue-110-20261117T2307` and `issue-110-live-20261118T1349Z` history: PR #1941 merged `docs/reference/research/issue-110-live-iot-identity-evidence-2026-11-18.md` (3 distinct SAS identities, Event Hub read-back, raw job output kept outside the repo).
* Gap named by that note: Event Hub read-back does not show SQL ingestion; the SQL leg is in the #1818 round 7 note (stored=9) with an unmerged receiver image.
* Prior state file `issue-110-live-state.json` is tracked and must not be overwritten; this task uses `issue-110-live2-state.json`.
* Hub `iot-cutover-test-rzsrg` (B1): public access Disabled, local auth disabled flag true (read-only `az iot hub list`).

## Plan input

Run one bounded synthetic job (3 homes x 2 slots, 6 messages, cap 200 cumulative) that registers `SYN-` devices, sends, reads Event Hub and writes to SQL; retain raw output outside the repo; clean up the job, roles and devices; record a per-criterion table.

## Planning Readiness

Ready, subject to the deployed image containing `zava_forward.api.live_demo` (to be probed).
