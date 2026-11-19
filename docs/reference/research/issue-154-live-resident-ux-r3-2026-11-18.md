---
title: Resident and Representative UX on the Live Demo, Round 3 (Issue 154)
description: Network trace, Azure messaging-resource check and per-criterion status for the one unticked criterion of #154 on the synthetic demo
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only; live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. This round follows [round 1](issue-154-live-resident-ux-evidence-2026-11-18.md) and [round 2](issue-154-live-resident-ux-audit-r2-2026-11-18.md), which are unchanged. The only unticked criterion in the issue is "No live resident contact; designs are validated through the usability programme before any use", split here as 5a and 5b.

The resident sign-in was read from the owner's file at run time and never printed or stored. The trace script stores method, host and path only, no request bodies. No resource was created, so nothing needed deleting. Results are observations on one date, not an accessibility acceptance or a usability result.

## Evidence

All under `.copilot-tracking/evidence/2026-11-18/issue-154-live-r3/`.

| File | Content |
| --- | --- |
| [network_trace.py](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r3/network_trace.py), [network-trace-raw.json](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r3/network-trace-raw.json) | Playwright trace of the signed-in resident showcase with every panel expanded |
| [azure-messaging-check-raw.txt](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r3/azure-messaging-check-raw.txt) | Read-only `az resource list` for resource group `ama`, a type filter for messaging resources, and the resident app's environment variable names |
| [local-tests-raw.txt](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r3/local-tests-raw.txt) | Verbose run of `tests.test_representative_expiry_api` and `tests.test_resident_demo_api`: 53 tests, OK |
| [outbound-search-raw.txt](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r3/outbound-search-raw.txt) | Search of `src` and `infra` for smtplib, SendGrid, Twilio, Azure Communication Services and GOV.UK Notify: one file, `src/core/tests/test_funding_automation_boundary.py` |

## Results for 5a

* The trace recorded 9 requests to one host (`ca-resident-demo`). Eight were GET requests for the page, its CSS and scripts and the session and view data; the only other request was `POST /demo/login`.
* The signed-in page has no `mailto:`, `tel:` or `sms:` link and its only form action is `/demo/login`.
* The resource group holds no Azure Communication Services, email, SendGrid, Logic Apps or Notification Hubs resource, and the resident app has no environment variable naming a messaging service.
* The 53-test local run passed, and the outbound-library search matched only the boundary test that forbids those libraries.
* Correction to round 1: the signed-in page has one textarea, the assistant question box from `chat-widget.js`. Round 1 said there was no free-text control. It was not used here, because that would call a real AI service.
* Limits: one page load, one account, one date. The trace shows no outbound contact from the browser or from the app configuration; it cannot show server-side behaviour that the code and resource checks do not cover.

## Per-criterion table

| Criterion (issue state) | Result | Basis |
| --- | --- | --- |
| 1 Journeys cover choice, pause or withdrawal, appointments, commitments, handover, complaint (ticked) | Partly proven live; not re-run | Round 2 |
| 2 Non-digital alternative, language, literacy and adjustments without inferring incapacity (ticked) | Partly proven live; not re-run | Round 2 |
| 3 Representative views task-limited and expiring (ticked) | Unproven live | No demo case has a representative (round 1); expiry covered by the retained 53-test run |
| 4 Offers distinct from confirmed commitments (ticked) | Partly proven live; not re-run | Round 2 |
| 5a No live resident contact (unticked) | Proven for the demo | Network trace, Azure resource check, DOM check and tests above |
| 5b Validated through the usability programme before any use (unticked) | Unproven; cannot be for the demo | Needs moderated sessions and staff agreement (SA-010), which the owner has not asked for; the criterion stays unticked |

## Residual items

* A synthetic case with a representative and an offered slot would allow live proof of criteria 3 and 4; it means changing demo data.
* Whether the assistant question box can reach staff was not exercised.
