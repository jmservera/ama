---
title: Issue 2256 live re-verification on API revision 0000054 (2026-11-22)
description: Live Playwright probe of the Handoff waiting times screen against the case card, with the limits of the evidence
ms.date: 2026-11-22
ms.topic: reference
---

Scope: synthetic demo, desktop only, resource group `ama`, app `ca-cutover-test-demo-api`, revision `ca-cutover-test-demo-api--0000054` (created 2026-11-22 23:14 UTC, active, Healthy, 100% traffic; `az containerapp revision list`). Sign-in values were read at run time and never printed. No Azure change.

The issue has no checkbox list, so its Expected paragraph is split into criteria below.

## Result (probe 2026-11-22 23:34 UTC)

| Call or screen | Result |
| --- | --- |
| `GET /api/handoffs` | 200, 4 rows (ZF-2025-0029 to 0032, state Offered) |
| `GET /api/handoffs/unaccepted` | 200, 4 rows, status Sent, proposed receiver Miguel Garcia, chase owners Daisy Phillips (0029) and Aadi Kapoor (0030 to 0032); `due_at` null; `limit_note` "Approved escalation time not set (OD-09)" |
| `#/handoff-waiting` | lists all four rows with chase owner and proposed receiver; waiting reads "Unknown. The offered time has no recorded timezone."; due reads Unknown |
| `#/case/ZF-2025-0030` | still says "Offered to Miguel Garcia, not yet confirmed", next action "Ask the proposed receiver to accept or decline", chase owner Aadi Kapoor |

## Per-criterion outcome

| Criterion | Outcome |
| --- | --- |
| A. The offered handoff appears in the waiting list | Proven live: ZF-2025-0030 is row 2 of 4 on the screen and in the API |
| B1. Chase owner shown | Proven live: Aadi Kapoor, and it matches the case card owner |
| B2. Due time shown | Not provable for the demo data: the seeded offers have `due_at` null, so the screen honestly shows Unknown; the code never invents one |
| C. Case card and waiting list agree | Proven: both describe the same open, unconfirmed offer to Miguel Garcia |

The raw `offered_at` is `2026-10-13T09:00` with no timezone, so the elapsed wait cannot be computed and the screen says so instead of guessing. Showing a real due time and wait needs seed data with timezone-aware `offered_at` and `due_at`; that is a data change outside this evidence-only task and the demo production-change limit.

## Limits

* The image digest was not mapped to a commit; the fix is inferred from behaviour that only the fixed code produces (non-empty list, the timezone wording).
* The screen labels the state "Sent" where the card says "Offered"; a wording difference, not a visibility defect.
* The probe used the Retrofit Programme Manager-visible sign-in; other roles were not probed.

Evidence: [result JSON](issue-2256-liveverify-r54-2026-11-22/probe-handoff-result.json), [waiting screenshot](issue-2256-liveverify-r54-2026-11-22/screens/handoff-waiting.png), [case screenshot](issue-2256-liveverify-r54-2026-11-22/screens/case-ZF-2025-0030.png), [script](issue-2256-liveverify-r54-2026-11-22/probe_handoff.py). Earlier probe on revision 0000053: [note](issue-2256-liveverify-2026-11-22.md).
