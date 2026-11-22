---
title: Issue 2256 live verification of the Handoff waiting times fix (2026-11-22)
description: Live Playwright probe showing the waiting list now lists the offered handoffs, with the limits of the evidence
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`, app `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000053` (created 2026-11-22 19:38 UTC, after the fix merge at 17:31 UTC). Sign-in values were read at run time and never printed. No Azure change.

## Result (probe 2026-11-22 23:02 UTC)

| Call | Result |
| --- | --- |
| `GET /api/handoffs` | 200, 4 rows |
| `GET /api/handoffs/unaccepted` | 200, 4 rows: ZF-2025-0029 to ZF-2025-0032, status Sent, proposed receiver Miguel Garcia, chase owners Daisy Phillips and Aadi Kapoor |
| `#/handoff-waiting` | lists all four; waiting shows "Unknown. The offered time has no recorded timezone."; due shows Unknown |

The earlier mismatch (0 rows against 4 pending) is gone. Evidence: [probe-handoff-result.json](issue-2256-liveverify-2026-11-22/probe-handoff-result.json), [screenshot](issue-2256-liveverify-2026-11-22/screens/handoff-waiting.png), [script](issue-2256-liveverify-2026-11-22/probe_handoff.py).

## Limits

* The seeded offers have no due time, so the due column reads Unknown; no due time was invented.
* The container image digest was not mapped to a commit; the fix is inferred from behaviour that only the fixed code produces.
* The screen labels the state "Sent" where the case card says "Offered"; a wording difference, not a visibility defect.

Fix and regression tests: see [the earlier note](issue-2256-handoff-waiting-2026-11-22.md).
