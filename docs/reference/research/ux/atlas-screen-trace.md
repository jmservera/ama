---
title: Atlas findings and role journeys traced to screens
description: Cross-role trace of the eleven profile perspectives, five atlas design themes, two tensions and one same-home walkthrough to role screens or recorded deferrals (issue #233)
ms.date: 2026-11-03
ms.topic: reference
---

## Scope and evidence label

Partial delivery for [#233](https://github.com/jmservera/ama/issues/233) under
[#149](https://github.com/jmservera/ama/issues/149). All atlas findings, themes
and walkthrough content below are **hypotheses** from the desk-based
[customer journey atlas](./customer-journeys/customer-journey-atlas.md), not
observed behaviour, until validated in [#155](https://github.com/jmservera/ama/issues/155).
Screen identifiers are `registerRoleScreen` ids in
`src/api/src/zava_forward/api/web/role-screens.js`. At the 2026-11-01 snapshot
all twelve screens are registered on main (marked "main" with the
delivering pull request); `programme-queue`, `technical-queue` and
`quality-queue` merged after the first snapshot. The checker compares these labels with the registered
ids. This trace does not assess their rendered behaviour, accessibility or design-system conformance.

Run `python3 -m zava_forward.core.atlas_screen_trace` from `src/core` (after
`pip install -e .`) to check that every perspective, theme, tension and
walkthrough stage is present. The checker reports completeness only and records
no human, accessibility or content acceptance.

## Perspectives to screens

Perspective names match the
[PRD profile contract](../../../prds/zava-forward-retrofit-programme-demonstrator.md#profile-journey-contract-for-the-next-prototype).
Profile selection is a view filter, never authorisation, and no screen contains a
role simulator.

| Perspective | Screen and status | Confirms | Changes | Remains hypothesis |
| --- | --- | --- | --- | --- |
| Asset and investment | `asset-board` (main, #226) | Conflict, source age and unknown investment inputs shown with a resolution owner | Portfolio scope shown separately from stock total | Which inputs asset staff need; no asset role exists in fixtures; AI report Loaded or Unavailable with a without-AI manual path; a second panel lists metered calls, held-call alerts with owners and other cost components, with Unknown (never zero) for any missing figure (unit-tested only, Refs #100) |
| Programme coordinator | `programme-queue` (main, PR 662) | Returned work, sender, current owner and receiver shown | Chase and update responsibility kept apart from return reason | Whether visible reset suffices as recovery |
| Retrofit case team | `programme-queue` connected home view (main, PR 662) | Independent technical, resident, delivery, quality and finance states per home | One linked fixture home first, separate homes never merged | Whether a read-only lifecycle is enough for case teams |
| Retrofit Assessor, designer and Coordinator | `technical-queue` (main, PR 656) | Missing design reference blocks readiness | Return routed to a named competent reviewer, not a generic approval | Separate sign-off wording |
| Housing and Resident Engagement | `resident-choice` (main, #652) | Measure-specific choice, pause and withdrawal distinct from contact and access | Update commitment shows purpose, owner and safe-route reference | Resident-facing wording; no resident contact |
| Housing and Resident Engagement | `resident-service-issues` (#232 slice, 2026-11-02) | Service issue with route, named service and redress owners, contact needs and next update | Same linked update commitment with safe-route reference | Resident-facing wording; no resident contact; screen conformance not assessed |
| Repairs and Building Safety | `safety-lead` and `hazard-triage` (main, #653) | Sent, received and accepted states with a scoped hold | Pending receipt has an owned follow-up | Referral timing expectations; no hazard classification by the UI |
| Procurement and contract manager | `procurement-packages` (main, #655) | Offered and committed capacity separated | Unmet prerequisites and next reviewer shown | Period and call-off conventions |
| Provider / contractor contact | `contractor-job-pack` (main, #655; Contractor role, "Your job pack") | Contractor-facing job pack, not the staff-mediated constructed intake in the PRD contract; no provider identity claim | Submission kept separate from independent acceptance | Staff-facing constructed intake is deferred until a supporting screen design exists; whether a provider portal is wanted at all |
| Quality and assurance | `quality-queue` (main, PR 656) | Incomplete evidence blocks handover | Positive per-measure evidence, defect owner and reinspection shown | Reinspection thresholds |
| Finance and Grants | `finance-invoices` and `finance-funding` (main, #657) | Invoice, award, claim and cash kept as separate states | Exceptions explained before any export or readiness block (per-exception plain-language table, #785; AI economics section with every input Unknown on both screens, 2026-11-03) | Funding route and schema; no payment or submission control |
| Digital operator and auditor | `data-operator` (main, #654) | Both source values and provenance shown, original preserved | Illustrative event metadata labelled as not an operational audit trail | Operator recovery context |

## Atlas design themes to screens

Source: [five design themes](./customer-journeys/customer-journey-atlas.md#five-design-themes-and-tensions).

| Theme | Screen or recorded deferral | What the design shows |
| --- | --- | --- |
| Continuity rather than repeated intake | `programme-queue` and `resident-choice` | Home context and owner carried across screens; only purpose-scoped fields shown |
| Resident-controlled coordination | `resident-choice` and `procurement-packages` | Choice and withdrawal shown before offered capacity; urgent safety route independent |
| Evidence that carries its context | `technical-queue` and `data-operator` | Provenance, unknowns and independent review shown; reuse never transfers approval |
| Prevention through rehearsal | Deferred: dispatch rehearsal and grant challenge need a deterministic comparator and a later exploratory build (atlas O10, O18 to O20 stay outside the next accepted exercise) | Nothing built; `finance-funding` shows only readiness blocks |
| Accountable recovery and learning | `quality-queue` and `hazard-triage` | Human remedy, return reasons and owners shown; aftercare concern pack deferred to the handover bundle |

## Tensions

| Tension | Where resolved | Resolution | Status |
| --- | --- | --- | --- |
| Continuity versus disclosure | `programme-queue` and `resident-choice` | Each screen shows the minimum fields its role needs; withheld items are listed as text under a "Not shown for this role" panel (on the per-home view of both screens, on the `programme-queue` overview and on the `resident-choice` page summary) rather than silently omitted; contact and access appear as a route reference, not sensitive history | Proposed rule; rendered behaviour and conformance not assessed |
| Utilisation versus choice | `resident-choice` and `procurement-packages` | Resident options and withdrawal render first; capacity is labelled offered or committed and never ordered by utilisation; an offered slot is never worded as a promise | Proposed rule; rendered behaviour and conformance not assessed |

## Same-home walkthrough

One constructed fixture home, EX-HOME-901, is walked through the eight atlas
stages in [one connected service journey](./customer-journeys/customer-journey-atlas.md#one-connected-service-journey).
It is new for this walkthrough and is not one of the eight existing separate
examples, which are not relabelled as stages. It is a design-level walk: no
fixture or screen for EX-HOME-901 exists in code yet, and consent, readiness,
release, acceptance, handover and financial closure stay separate states.

| Stage | Role screen | What the screen shows for EX-HOME-901 | Boundary |
| --- | --- | --- | --- |
| 1. Report or nominate | Deferred: no screen in #652 (merged) shows a source account or recipient-scoped link; proposed addition to `resident-choice` | Source account and recipient-scoped link, design not yet supported | Urgent safety intake runs independently |
| 2. Understand home and household | `technical-queue` | Condition records and missing reference | Unknown stays unknown; hazard route parallel in `hazard-triage` |
| 3. Decide scope and feasibility | `resident-choice` | Measure-specific choice beside design version | Generic consent is not accepted |
| 4. Coordinate ready work | `procurement-packages` | Offered versus committed capacity | Offer is not a booking |
| 5. Deliver and capture | `contractor-job-pack` | Evidence checklist and submission state | Submission is not acceptance |
| 6. Inspect and remedy | `quality-queue` | Per-measure evidence, return reason, defect owner | Independent acceptance separate |
| 7. Handover and live with measures | `resident-choice` | Aftercare update with owner and safe route | Open remedies not closed by handover |
| 8. Reconcile and learn | `finance-invoices` | Invoice, claim and cash as separate states | No award inferred from an invoice |

## Static guardrail evidence (2026-11-02)

`src/api/tests/test_role_screens_conformance.py` reads `role-screens.js` and
`style.css` as text. It shows that every registered screen is named in this
trace, no screen contains role-simulator wording, every CSS class used is defined
in the design system stylesheet, controls are native elements, scrollable table
regions are labelled and focusable, tables have captions and column scope, state
is stated in text rather than inline colour, the screen styles add no motion, and
each selected-home view states that no message, approval or record change is made.
It also guards that the "Not shown for this role" panel is present on
`programme-queue` and `resident-choice` and that the rule stays labelled proposed. These are source-level
checks only; they do not render a page, use assistive technology or involve users.

## Boundaries and unmet criteria

* Accessibility to the WCAG 2.2 baseline ([#151](https://github.com/jmservera/ama/issues/151)) is only partly evidenced by the static checks above; rendered keyboard and assistive-technology checks in CI and human review remain open.
* Use of design system components ([#150](https://github.com/jmservera/ama/issues/150)) is supported only by the static class check above; component-level verification remains open.
* Validation with users remains in [#155](https://github.com/jmservera/ama/issues/155); owner decisions on the deferral above are open.
* The journey source names one "Programme Manager / planner" persona ([programme journey](./customer-journeys/programme.md)). The codebase has no separate planner role: `programme-queue` is available to Retrofit Programme Manager, Programme Support Officer and Retrofit Coordinator. Whether a distinct planner role is needed is an owner decision and stays open; no role is invented here.
