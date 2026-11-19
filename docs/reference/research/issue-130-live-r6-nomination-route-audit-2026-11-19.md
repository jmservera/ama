---
title: Sixth audit of the nomination, self-referral, acknowledgement and challenge route (issue 130)
description: Recorded 2026-11-19 read-only re-check of the synthetic demo apps and offline tests, with a per-criterion proven or unproven table
author: AMA RPI agent
ms.date: 2026-11-19
ms.topic: reference
keywords:
  - issue 130
  - nomination route
  - representative authority
  - live demo
estimated_reading_time: 3
---

Refs #130. Scope is the synthetic desktop demo under the owner decisions of 2026-11-18 (live Azure in resource group `ama`, cap USD 700; billing reconciliation, DPO and Legal approval and person-run assistive-technology testing not needed). This run follows the [fifth audit](./issue-130-live-r5-nomination-route-audit-2026-11-18.md). Nothing was deployed or changed.

## Method and results

* Azure CLI, read-only: `ca-cutover-test-demo-api` is on revision `--0000033` (Running) with the unchanged image digest `sha256:5368f4e4...e5fb`; `ca-resident-demo` is on `--0000014` (Running). Both revisions are newer than in run 5 (`--0000032`, `--0000013`).
* Offline, `src/core`: `test_nomination_route`, `test_nomination_bootstrap`, `test_hazard_referral`: 66 tests, OK, 1 skipped (about 129 s).
* Not repeated: the live write probes. The same image digest means the run 4 and 5 finding of a 403 identity refusal on staff-recorded writes still applies as the last observed result; this run did not re-observe it.
* Evidence: `.copilot-tracking/evidence/2026-11-19/issue-130-live-r6/` (`az-revisions.txt`, `offline-core.txt`). No credentials were read or printed.

## Per-criterion result

| Criterion in #130 | Issue state | Demo result | Evidence and limit |
| --- | --- | --- | --- |
| Representative participation and comprehension need authorized human evidence | Unticked | Unproven; cannot be proven for the demo | Needs real representatives and residents; the owner excluded person-run testing, and constructed UI checks alone cannot pass this gate. No code change can supply it. |
| Original account, source and channel kept | Ticked | Offline proven; live write not re-observed | 66 core tests |
| Acknowledged route and named owner before review | Ticked | Offline proven | Same tests |
| Challenge or correction with evidence, reviewer and outcome | Ticked | Offline proven | Same tests |
| Correction re-reviews only dependents | Ticked | Offline proven | Same tests |
| Hazard concerns route to #85 | Ticked | Offline proven | `test_hazard_referral` |
| Non-response and support needs never lower priority | Ticked | Offline proven | Same tests |
| Wrong identity, limited authority, manual route tested | Ticked | Offline proven | Same tests |

No unmet criterion is buildable as code, so no source change was made.
