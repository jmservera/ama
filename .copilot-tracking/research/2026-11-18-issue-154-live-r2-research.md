---
title: Research for #154 live resident and representative UX proof, round 2
ms.date: 2026-11-18
---

## Scope

Round 2 of the live demo proof for #154 (desktop only, synthetic demo, resident test sign-in). Round 1 is committed as `2026-11-18-issue-154-live-*` and its state file is left untouched. Disposition: executed (new investigation), reusing round 1 evidence where still valid.

## Round 1 gaps to close

* Raw output of the 53-test local run and the outbound-library search was not retained.
* Signed-in workbench screens were never captured; only the signed-out landing page.
* No audit of the live resident page against `docs/reference/research/ux` (content standard, WCAG baseline, design system).
* Criterion 3 (representative view) was probed only by API.

## Planning Readiness

Ready. Sources: issue #154 acceptance criteria, `docs/reference/research/ux/{content-standard,wcag-conformance-baseline,design-system}.md`, round 1 evidence.

## Evidence gathered (retained in `.copilot-tracking/evidence/2026-11-18/issue-154-live-r2/`)

* `local-tests-raw.txt`: verbose run of `tests.test_representative_expiry_api` and `tests.test_resident_demo_api` (53 tests, OK, exit 0).
* `outbound-search-raw.txt`: search of `src` and `infra` for smtplib, SendGrid, Twilio, Azure Communication Services and GOV.UK Notify; only `src/core/tests/test_funding_automation_boundary.py` matches.
* `ux_audit.py` and `ux-audit-raw.json`: desktop 1366 px DOM audit (language, title, h1, landmarks, names, contrast, target size, keyboard focus, 200% equivalent reflow, reduced motion, content-standard banned terms) of the signed-in resident showcase and of the workbench Resident choice, Resident service issue, Package queue, case list and case detail screens. Ids, emails, addresses and names are redacted.
* `screen_excerpts.py` and `screen-excerpts-raw.json`: matching text lines from the three role screens.
* Screenshots `r2-*.png` (resident signed in, expanded, 683 px width as the 200% equivalent). Workbench screenshots (Resident choice, Resident service issues, Package queue, case list, case detail) were not retained because they show names.
* Discovery: the workbench is served at `/app` after `/sign-in`; `/` is the welcome page. Round 1 captured only the welcome page, which explains its empty body-term checks.

## Findings

* Resident showcase: no contrast failure in 278 text elements, no control under 24 px, no horizontal scroll at the 200% equivalent, reduced-motion rule present, 8 keyboard stops all with a visible focus indicator, no internal term from the content standard. The audit flagged `#signout` as unnamed; the element text is "Sign out", so this is a detector artefact.
* Workbench role screens (signed in as Retrofit Programme Manager): Resident choice screen states that a paused or withdrawn measure is listed separately, and that "Not recorded", "None recorded" and "No commitment recorded" do not show consent or readiness. Contrast 0 failures in 601 elements. One 144 by 18 px link ("Back to my work") and list links under 24 px (WCAG 2.5.8 spacing exemption not assessed). Case detail: one control without a visible focus indicator among 25 stops.
* Not visible live: representative, interpreter, easy read or large print strings on the resident showcase; no case has a representative (round 1).

## Open limits

Single date, desktop, synthetic demo; automated DOM checks only, not conformance or usability results.
