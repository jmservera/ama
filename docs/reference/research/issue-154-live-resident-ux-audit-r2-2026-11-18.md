---
title: Resident and Representative UX Audit on the Live Demo, Round 2 (Issue 154)
description: Desktop audit of the deployed synthetic resident showcase and the workbench resident screens against the UX research standards, with retained raw output and a per-criterion table for #154
author: AMA programme
ms.date: 2026-11-18
ms.topic: reference
---

## Scope and authority

Owner decisions of 2026-11-18: synthetic demo, desktop only; live Azure authorised (resource group `ama`, cap USD 700, no drills, no Key Vault rotation, no production change). Billing reconciliation, DPO and Legal approval and person-run assistive-technology testing are not needed for the demo. This round extends [round 1](issue-154-live-resident-ux-evidence-2026-11-18.md), which is unchanged. No Azure resource was created or changed, so nothing needed deleting, and no source code changed.

Sign-ins were read from the owner's files at run time and never printed or stored. Retained JSON and the resident screenshots mask emails, home ids and addresses; workbench screenshots are not retained. Results are observations on one date from automated DOM checks at 1366 px. They are not a WCAG conformance claim, a comprehension result or a usability result.

## Evidence

All under `.copilot-tracking/evidence/2026-11-18/issue-154-live-r2/`.

| File | Content |
| --- | --- |
| [local-tests-raw.txt](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r2/local-tests-raw.txt) | Verbose run of `tests.test_representative_expiry_api` and `tests.test_resident_demo_api`: 53 tests, OK, exit 0 |
| [outbound-search-raw.txt](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r2/outbound-search-raw.txt) | Search of `src` and `infra` for smtplib, SendGrid, Twilio, Azure Communication Services, GOV.UK Notify: only `src/core/tests/test_funding_automation_boundary.py` |
| [ux_audit.py](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r2/ux_audit.py), [ux-audit-raw.json](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r2/ux-audit-raw.json) | Audit script and raw output |
| [screen_excerpts.py](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r2/screen_excerpts.py), [screen-excerpts-raw.json](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r2/screen-excerpts-raw.json) | Matching text lines from three workbench role screens |
| `r2-01`, `r2-02`, `r2-03` PNGs | Resident showcase signed in, with panels expanded, and at 683 px width (200% equivalent) |

The workbench screens (Resident choice, Resident service issues, Package queue, case list and case detail) were audited, but their screenshots are not retained because they show the signed-in user's name and resident names. Their DOM text is kept only as redacted excerpts in the JSON files.

## Audit against `docs/reference/research/ux`

Checks follow the [WCAG baseline](../research/ux/wcag-conformance-baseline.md) dimensions (keyboard, focus, names, contrast, reflow, target size), the [content standard](../research/ux/content-standard.md) glossary and the [design system](../research/ux/design-system.md) desktop tier (1280 px and wider).

| Check | Resident showcase (signed in) | Workbench role screens and case views |
| --- | --- | --- |
| Language, single h1, landmarks | `en-GB`, one h1, header, main, nav, footer | `en-GB`, one h1 per screen, skip link present |
| Text contrast (4.5:1, 3:1 large) | 0 failures in 278 elements | 0 failures in 164 to 601 elements per screen |
| Keyboard focus indicator | 8 stops, all with an indicator | 25 stops per screen; one input (`hz-aware`) on case detail without a detected indicator |
| Control names | Sign out flagged by the detector; its text is "Sign out" (detector artefact) | Two shell buttons flagged on each screen ("Use another account", "Sign out"), same artefact; case list row links carry id text only |
| Targets under 24 px | none | "Back to my work" 144 by 18 px and some list links 18 px high; the WCAG 2.5.8 spacing exemption was not assessed |
| Reflow at 200% equivalent | no horizontal scroll | not run |
| Reduced motion | rule present, context emulated reduced motion | same |
| Internal terms banned by the glossary | none of gate, hold, provenance, trace, envelope, snapshot | none on the five screens checked |

## Per-criterion table

| Criterion (issue state) | Result | Live evidence |
| --- | --- | --- |
| 1. Journeys cover choice per measure, pause or withdrawal, appointments, update commitments, handover, complaint or remedy (ticked) | Partly proven live | The workbench Resident choice screen lists each home's measure choices, "Paused or withdrawn" and "Update commitment" columns and states that a paused or withdrawn measure is listed separately from contact and access ([screen excerpts](../../../.copilot-tracking/evidence/2026-11-18/issue-154-live-r2/screen-excerpts-raw.json)). Appointments, handover and complaint or remedy status were not seen live in any resident-facing view |
| 2. Non-digital alternative, language, literacy and adjustment support without inferring incapacity (ticked) | Partly proven live | Round 1 recorded the non-digital routes on the resident page. The Resident choice screen carries contact-needs wording; the resident showcase has no language or adjustment content (no match for language, adjustment, easy read or large print). Not inferring incapacity was not assessable from the screens |
| 3. Representative views task-limited and expiring (ticked) | Unproven live | No demo case has a representative, so the view returns 404 (round 1). Expiry and revocation are covered by the retained 53-test local run |
| 4. Offers distinct from confirmed commitments (ticked) | Partly proven live | The Resident choice screen states that "Not recorded", "None recorded" and "No commitment recorded" mean nothing is recorded and do not show consent or readiness. No offer is displayed on the resident showcase, so the offer-versus-commitment distinction was not seen there |
| 5a. No live resident contact (unticked) | Proven for the demo | Showcase banner and read-only statements and zero contact links (round 1), retained outbound-library search, retained test run. Limit: no network trace |
| 5b. Validated through the usability programme before any use (unticked) | Unproven; cannot be for the demo | Needs moderated sessions and staff agreement (SA-010), which the owner has not asked for; the criterion stays unticked |

## Residual items

* A synthetic case with a representative and an offered slot would allow live proof of criteria 3 and 4; it means changing demo data, which this round did not do.
* The focus-indicator and 18 px target observations are candidates for a keyboard and target-size review of the workbench; they were not fixed here.
* Resident-facing appointment, handover and complaint views are not exposed on the showcase.
