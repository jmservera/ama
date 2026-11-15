---
title: Profile Journey Contract and Connected Same-Home Journey Acceptance
description: Five-element profile journey contract across the eleven PRD perspectives, connected same-home walkthrough invariants across the six staff profiles, contractor view and resident portal, code-testable assertions and unmet human acceptance boundaries (issue #134)
ms.date: 2026-11-15
ms.topic: reference
---

## Scope and evidence boundary

Delivery record and reference contract for [#134](https://github.com/jmservera/ama/issues/134) under
[#149](https://github.com/jmservera/ama/issues/149), connecting the profile-by-profile UX review in
[zava-forward-prototype-profile-review.md](./zava-forward-prototype-profile-review.md), the eight-stage
same-home screen map in [atlas-screen-trace.md](./atlas-screen-trace.md), the plain-language rules in
[content-standard.md](./content-standard.md), the accessibility baseline in
[wcag-conformance-baseline.md](./wcag-conformance-baseline.md) and the journey traceability matrix in
[design-system.md](./design-system.md#journey-to-requirement-to-design-to-test-traceability).

Executable contract modules and tests on synthetic data:

* Core contract and same-home validators: `src/core/src/zava_forward/core/profile_journey_contract.py`
* Perspective walkthrough evidence gate: `src/core/src/zava_forward/core/perspective_walkthroughs.py`
* Journey acceptance criteria gate: `src/core/src/zava_forward/core/journey_acceptance.py`
* Specialist role-screen continuity host: `src/api/src/zava_forward/api/web/role-screens.js`
* Core unit and Store transition suite: `src/core/tests/test_profile_journey_contract.py`
* Full-stack HTTP, live resident portal and Node specialist screen suite: `src/api/tests/test_same_home_profile_journey_acceptance.py`
* Connected-home and same-home stage map suites: `src/api/tests/test_connected_home_check.py`, `src/api/tests/test_role_screens_same_home_identity.py`, `src/api/tests/test_role_screens_connected_journey.py` and `src/api/tests/test_role_screens_stage_map_focus.py`

Automated code checks prove repository shape, server-side projection, handover preconditions and
plain-language continuity on constructed synthetic data only. They never mark a perspective journey or
acceptance criterion (`AC-034` to `AC-043`) as accepted: `validate()` and `validate_same_home_walk()`
always return `accepted = False` (`status = "complete_in_shape"` when zero blockers remain). Live
role-representative walkthroughs ([#155](https://github.com/jmservera/ama/issues/155)), screen-reader
and keyboard assistive-technology runs ([#151](https://github.com/jmservera/ama/issues/151)) and named
human and resident sign-offs remain `not-established`.

## Five-element profile journey contract across eleven perspectives

Every perspective in `perspective_walkthroughs.PERSPECTIVES` (`SA-001` to `SA-008`, `AC-034` to
`AC-043`, `NFR-001`) requires five explicit contract elements (`ELEMENTS` in
`profile_journey_contract.py`):

| Element | Required contract behaviour | Blocking failure when absent or placeholder |
| --- | --- | --- |
| `entry` | Role-appropriate entry point into the case, queue or read-only portal without cross-role leakage | Missing text or placeholder (`unknown`, `tbd`, `todo`, `n/a`, `none`) |
| `evidence` | Current facts, provenance, unknowns and plain-language owner and next action needed for the role's step | Missing evidence statement or unlabelled stale/unknown record |
| `safe_endpoint` | Bounded stop or completion state that preserves human authority, resident consent and safety holds | Implied approval from AI output, unconfirmed receipt or silent override |
| `recovery` | Explicit return, correction, pause or withdrawal path naming who acts next | Dead end without reason, named owner or verb-led next action |
| `handoff` | Named sender, proposed or confirmed receiver, chase owner and resident-update responsibility | Silent ownership transfer before receiver acceptance |

Perspective scope covered by `gaps(root)` and `perspective_walkthroughs.check(root)`:

* Asset and investment lead (`AC-040`, `AC-041`, `SA-001`, `SA-002`, [customer-journeys/asset.md](./customer-journeys/asset.md))
* Retrofit Programme Manager (`AC-034`, `AC-036`, `AC-043`, `SA-001`, `SA-002`, [customer-journeys/programme.md](./customer-journeys/programme.md))
* Retrofit Coordinator (`AC-042`, `FR-011`, `FR-012`, `SA-003`, [customer-journeys/reviewer.md](./customer-journeys/reviewer.md))
* Resident Liaison Officer (`AC-035`, `AC-037`, `FR-003`, `FR-004`, `SA-008`, [customer-journeys/residents.md](./customer-journeys/residents.md))
* Neighbourhood Housing Officer (`AC-035`, `AC-037`, `SA-002`, [customer-journeys/frontline.md](./customer-journeys/frontline.md))
* Building Safety Liaison (`AC-038`, `FR-014`, `FR-015`, `SA-007`, [customer-journeys/safety.md](./customer-journeys/safety.md))
* Quality Inspector (`AC-042`, `FR-034`, `FR-035`, `SA-003`, [customer-journeys/reviewer.md](./customer-journeys/reviewer.md))
* Procurement and contractor manager (`AC-039`, `FR-016`, `FR-017`, `NFR-009`, [customer-journeys/suppliers.md](./customer-journeys/suppliers.md))
* Assigned contractor operative (`AC-039`, `NFR-009`, `NFR-018`, [customer-journeys/suppliers.md](./customer-journeys/suppliers.md))
* Grants and Evidence Officer (`AC-041`, `AC-042`, `FR-045`, `FR-048`, `FR-049`, [customer-journeys/finance.md](./customer-journeys/finance.md))
* Resident and authorised representative (`AC-035`, `AC-037`, `SA-006`, `SA-008`, [customer-journeys/residents.md](./customer-journeys/residents.md))

## Connected same-home invariants

`validate_same_home_walk()` composes four deterministic invariant checks across one selected home (for
example `ZF-1`) while holding a sibling home (`ZF-2`) in the same dataset to detect cross-home leakage:

| Invariant group | Validator in `profile_journey_contract.py` | Enforced rules across the six staff profiles, contractor view and resident portal | Automated verification |
| --- | --- | --- | --- |
| Shared home facts and sibling isolation | `check_shared_facts` | All six core staff profiles (`Retrofit Programme Manager`, `Retrofit Coordinator`, `Resident Liaison Officer`, `Building Safety Liaison`, `Quality Inspector`, `Grants and Evidence Officer`), `Programme Support Officer`, assigned `Contractor`, work orders, staff-mediated job pack and `resident_preview` agree on home identity (`id`, `home.address`, `home.postcode`), stage, normalized measures and stage-derived resident progress text; zero sibling `ZF-2` IDs or notes leak into any surface | `test_profile_journey_contract.py`, `test_same_home_profile_journey_acceptance.py`, `test_role_screens_same_home_identity.py` |
| Role-appropriate vulnerability redaction | `check_vulnerability_redaction` | Roles with a recorded need (`OD-14`, `OD-19`: `Resident Liaison Officer`, `Building Safety Liaison`, `Retrofit Programme Manager`) see `resident.adjustment`; other staff (`Retrofit Coordinator`, `Quality Inspector`, `Grants and Evidence Officer`, `Programme Support Officer`) see `Extra support noted` and `Held for roles with a recorded need` on staff-written free text; `Contractor` payloads (`contractor_summary`, `contractor_detail`, `work_orders`, `job_pack`) and `contractor-job-pack` show only `needs_notice = True` (`Needs notice`) and `named_contact`, omitting `resident`, `adjustment`, `priority_support`, `hazards`, `notes`, `work`, `audit` and `Extra support noted`; unassigned contractors receive HTTP `404` on `/api/cases/<id>` and `[]` on `/api/workorders`, and assigned contractors receive HTTP `403` on staff-only `/api/workorders/<id>/job-pack` | `test_profile_journey_contract.py`, `test_same_home_profile_journey_acceptance.py` |
| Handover and authority dependencies | `check_handover_dependencies` | Unreleased safety or safeguarding hazards block advancement (`FR-014`, `FR-015`); unresolved stock/EPC queries remain surfaced; contractor `resident_readiness` cannot report `Proceed` and quality handover cannot complete without `Accepted` resident measure decisions; the read-only resident preview (`GET /resident/view`) keeps `Consent and decisions` unavailable; offered handoffs do not transfer `owner` or `confirmed_receiver` before `accept_handoff`; `job_pack.worker_receipt` (`Submitted` status, never quality acceptance) and `acknowledge_receipt` (`Receipt recorded`, awaiting quality inspection) keep `accepted = False`; completed work orders cannot close the home without independent `Quality Inspector` acceptance (`accepted_by != submitted_by`) | `test_profile_journey_contract.py`, `test_same_home_profile_journey_acceptance.py`, `test_connected_home_check.py` |
| Plain-language owner and next-action continuity | `check_next_action_continuity` | Every staff projection carries non-empty `work.owner` and verb-led plain-language `work.next_action` (with `Held for roles with a recorded need` when a pending handoff carries free-text `next_action`), free of internal jargon (`gate`, `hold`, `provenance`, `trace`, `envelope`, `snapshot`); selected-home staff specialist screens in `role-screens.js` render `Same home: case <id>`, `Current owner: <owner>. Next action: <next_action>` (`data-same-home-next-action`) and `Journey stages for <id>` while contractor views omit internal `work` continuity | `test_profile_journey_contract.py`, `test_same_home_profile_journey_acceptance.py`, `test_content_standard.py`, `test_role_screens_connected_journey.py` |

## Explicit human, resident and accessibility boundaries

Code-level contract checks remain strictly separate from human governance and lived-experience sign-off:

| Boundary key in `BOUNDARIES` | Status | Required owner and open gate |
| --- | --- | --- |
| `human_approval` | `not-established` | Named housing, technical, building safety, quality and finance role holders retain all statutory, consent, contract and payment decisions (`SA-004`, `FR-014`, `FR-034`, `FR-048`) |
| `resident_consent` | `not-established` | Resident choice, refusal, pause and withdrawal stay with the resident or verified representative through staff-supported channels; the resident portal is read-only preview (`SA-006`, `SA-008`, `AC-035`, `AC-037`) |
| `live_accessibility_walkthrough` | `not-established` | Screen-reader, keyboard-only, zoom and reduced-motion walkthroughs with named testers remain open under [#151](https://github.com/jmservera/ama/issues/151) and [#155](https://github.com/jmservera/ama/issues/155) (`NFR-001`) |
| `perspective_walkthrough_signoff` | `not-established` | `perspective_walkthroughs.check(root)` (`0` of `55` elements met) and `journey_acceptance.check(root)` (`passed = []` across `AC-034` to `AC-043`) stay open until real perspective sessions are recorded |
