---
title: Usability testing programme plan with representative users (issue 155)
description: Moderated usability testing programme specification, contract-derived task scripts, SA-010 aggregate-only measures, severity/backlog findings contract, negative/inconclusive outcome rules, and labelled synthetic walkthrough baseline, with human participant sessions unexecuted
ms.date: 2026-11-17
ms.topic: reference
---

## Purpose and evidence label

Issue [#155](https://github.com/jmservera/ama/issues/155), under #149, covers
PRD SA-009, SA-010, OQ-004, OQ-005 and OQ-011 and BRD NFR-008, NFR-009 and
AC-071. This page defines the complete moderated usability testing programme
specification paired with the deterministic contract and evaluator in
[`usability_programme.py`](../../../../src/core/src/zava_forward/core/usability_programme.py)
and [`test_usability_programme.py`](../../../../src/core/tests/test_usability_programme.py).

At 2026-11-15 no human participant has been recruited, no moderated session has
run, no live human measure exists and no owner, DPO or staff representative
agreement is recorded. Deterministic synthetic checks are reported separately
under the mandatory label `Synthetic walkthrough - not user validation`
(`not_user_validation = True`) and never fill a human participant row, claim
usability acceptance or establish WCAG conformance.

All numeric thresholds remain PRD proposals used as testable hypotheses, not
automated pass marks. Real customer access is not yet available; any proxy
participant or proxy pilot session must carry its explicit non-validation label.

Related pages: [profile journey contract](./profile-journey-contract.md) (#134),
[journey learning-test bundles](./journey-learning-test-bundles.md) (#129),
[equity and user research protocol draft](./equity-journey-test-plan.md) (#128),
[prototype profile review](./zava-forward-prototype-profile-review.md)
(checks UX-01 to UX-08), [Customer Journey Atlas](./customer-journeys/customer-journey-atlas.md),
[resident journeys](./customer-journeys/residents.md) (J1 to J6 and R1 scripts),
[supplier journeys](./customer-journeys/suppliers.md) and
[frontline journeys](./customer-journeys/frontline.md).

## Hypotheses and thresholds (proposals)

| Id | Hypothesis | Source | Cohort applicability | Status |
| --- | --- | --- | --- | --- |
| H1 | At least 80 percent of 5 to 8 users per workbench role find their case and state the next step and accountable owner, unaided, in under 5 minutes | SA-009 | Staff and contractor cohorts (`t0_applicable = True`); `not_applicable` on read-only `resident` and `resident-representative` cohorts where internal case IDs and queues are hidden | Proposal, untested with people |
| H2 | Median SUS of at least 70 per role cohort (with `n >= 5` numeric respondents; otherwise `inconclusive` when participants choose the plain-language read-aloud alternative) | SA-009 | All 13 non-pilot role cohorts | Proposal, untested with people |
| H3 | Every participant completes the manual or staffed non-digital alternative for their task without detriment | NFR-009, AC-071 | All 13 non-pilot role cohorts | Untested with people |
| H4 | Zero task steps imply consent, approval, quality acceptance, a commitment or a submission that has not happened | Bundle stop rules, UX-04, UX-05 | All cohorts and synthetic probes; any nonzero event triggers `not_supported` immediately | Untested with people; synthetic negative probe verified |

With 5 to 8 participants per role cohort, percentages are coarse (4 of 5 is 80
percent). Every report must publish raw counts alongside whole-number
percentages and state that the sample is diagnostic rather than statistically
powered. A participant hesitating, needing an assist or stopping on an unclear
screen is a product finding, never a user error.

## Participants per role cohort (5 to 8 per role plus pilot)

`default_programme_plan()` and `validate_programme_plan()` enforce 5 to 8
participants (`MIN_ROLE_PARTICIPANTS = 5`, `MAX_ROLE_PARTICIPANTS = 8`) across
all 13 representative role cohorts (10 internal staff perspectives, 1 external
contractor perspective, voluntary residents and voluntary authorised
representatives), plus a separate 2 to 3 person `proxy-pilot` cohort for script
calibration that never counts toward role minimums.

| Cohort ID | Group | Role description | Target n | T0 (`<5m`) | Prototype login note and recruitment basis | Status |
| --- | --- | --- | --- | --- | --- | --- |
| `asset-investment` | Staff | Asset management and investment lead | 5 to 8 | Applicable | `PROXY_ONLY` via manager fixture; Zava North Homes sponsor or comparable landlord proxy (SA-009) | Not started |
| `programme-coordinator` | Staff | Retrofit programme manager and coordinator | 5 to 8 | Applicable | Direct role view (`Retrofit Programme Manager`); Excel/workbench users (SA-009) | Not started |
| `retrofit-case-team` | Staff | Retrofit coordinator and case team | 5 to 8 | Applicable | Direct role view (`Retrofit Coordinator`); Excel/workbench users (SA-009) | Not started |
| `assessor-designer` | Staff | Retrofit assessor and designer | 5 to 8 | Applicable | Technical review view; PAS 2035 assessor/designer practitioners (SA-009) | Not started |
| `housing-resident-engagement` | Staff | Housing officer and resident liaison officer | 5 to 8 | Applicable | Direct role view (`Resident Liaison Officer`); frontline housing/RLO staff (SA-009) | Not started |
| `repairs-building-safety` | Staff | Repairs interface and building safety liaison | 5 to 8 | Applicable | Direct role view (`Building Safety Liaison`); safety and hazard staff (SA-009) | Not started |
| `procurement-contracts` | Staff | Procurement and contract manager | 5 to 8 | Applicable | `PROXY_ONLY` via manager fixture; procurement and supplier-management staff (SA-009) | Not started |
| `quality-assurance` | Staff | Quality inspector and clerk of works | 5 to 8 | Applicable | Direct role view (`Quality Inspector`); QA and clerk-of-works reviewers (SA-009) | Not started |
| `finance-grants` | Staff | Finance and grants evidence officer | 5 to 8 | Applicable | Direct role view (`Grants and Evidence Officer`); grant-claim and finance staff (SA-009) | Not started |
| `digital-auditor` | Staff | Digital, data and assurance auditor | 5 to 8 | Applicable | `PROXY_ONLY` via manager fixture; data steward and governance reviewers (SA-009) | Not started |
| `provider-contractor` | Contractor | External installation contractor and field supervisor | 5 to 8 | Applicable | Contractor portal/job-pack view; invited via Procurement and Contracts | Not started |
| `resident` | Resident or representative | Voluntary social housing residents across digital, assisted, phone, paper, language and access needs | 5 to 8 (proposed) | Not applicable | SA-009 sizes staff roles; 5 to 8 proposed to satisfy the `n >= 5` privacy floor, subject to Resident Engagement, owner and DPO confirmation | Not started |
| `resident-representative` | Resident or representative | Authorised family members, carers, advocates or support workers (`R1`) | 5 to 8 (proposed) | Not applicable | Proposed 5 to 8 voluntary representatives testing scoped authority and separate consent, subject to owner and DPO confirmation | Not started |
| `proxy-pilot` | Pilot | Internal proxy dry-run participants for script clarity only | 2 to 3 | Script check only | `counts_toward_role_minimum = False`; labelled `Proxy pilot - script check only, not user validation` | Not started |

Roles with no reachable participants are reported as `not_run` (or
`suppressed_small_cell` when `1 <= n < 5`), never padded with AI role agents or
colleagues role-playing residents. Real workbook shapes, owners and contents
remain open questions (OQ-005); staff sessions begin with brief observation of
the participant's current spreadsheet or manual workaround on synthetic cases.

## Accessibility and support during sessions

`ACCESSIBILITY_SUPPORT_CLAUSES` and `REQUIRED_ASSISTIVE_TECH_ROUTES` require
every session plan to honour eight support commitments and four assistive
routes:

* `channel_choice` - before scheduling, offer in-person, telephone or remote
  browser sessions and allow switching to a staffed non-digital route at any
  moment.
* `own_device_and_assistive_tech` - support the participant's own device,
  screen reader (`screen_reader`: NVDA, JAWS, VoiceOver, TalkBack), keyboard
  navigation (`keyboard_only`), browser zoom up to 400 percent
  (`magnification_400_zoom`), high contrast and reduced motion, alongside the
  staffed phone or paper path (`non_digital_manual_route`). If an assistive
  route cannot be recruited for a cohort, record `assistive technology not
  tested` rather than claiming accessibility.
* `advance_plain_language_briefing` - send plain-language task goals, consent
  sheets and large-print, translated or easy-read packs in advance with no
  cold-reading pressure.
* `interpreter_or_trusted_person` - welcome and fund BSL or community
  interpreters, advocates, carers or a trusted support person without reducing
  task time.
* `extra_time_no_stopwatch_pressure` - offer flexible scheduling, untimed
  familiarisation and breaks; observe the 5-minute `T0` window quietly on staff
  workbenches without announcing or displaying a countdown timer.
* `voluntary_need_recording_only` - record only logistics adjustments
  volunteered by the participant for that session; never ask for or store
  medical diagnoses.
* `pause_or_stop_anytime` - allow skipping any task, pausing or ending the
  session at any point without giving a reason and with zero effect on tenancy,
  works, repairs, contract standing or employment.
* `manual_non_digital_parity` - test the manual or staffed non-digital
  fallback alongside the prototype screen on every script (NFR-009, AC-071).

Screens under test preserve the Fluent 2 design system, the WCAG 2.2 AA
baseline, the plain-language content standard, non-colour status cues and
reduced motion. Automated checks do not substitute for moderated sessions.

## Consent, data handling and the SA-010 audit-use gate

`CONSENT_DATA_CLAUSES` and `validate_audit_use_agreement()` enforce eight
consent and data-handling rules before any measure can be evaluated:

* `voluntary_participation` - participation is voluntary across all staff,
  contractor, resident and representative cohorts.
* `separate_from_tenancy_works_and_employment` - study consent is separate from
  tenancy agreements, retrofit measure consent, repairs, employment appraisals
  and supplier contracts.
* `synthetic_fictional_data_only` - sessions use constructed fictional homes,
  personas and documents only (`synthetic_data_only = True`); real resident
  records, live addresses and live staff caseloads are prohibited.
* `no_recording_without_separate_consent_and_dpo` - audio, video and screen
  recording are off by default (`recording_default_off = True`) and require
  both DPO approval of purpose, storage and deletion and a separate opt-in
  participant consent choice.
* `revocable_before_aggregation` - participants may withdraw their session
  notes at any time prior to role-level aggregation, deleting their notes.
* `pseudonymised_notes_separate_from_signup` - facilitator notes use random
  session codes kept separate from recruitment contact sheets, with zero names,
  emails, staff IDs or combinable verbatim quotes.
* `dpo_retention_gate_required` - lawful basis, minimum recruitment fields and
  retention schedule stay gated on a named DPO decision before recruitment.
* `aggregate_reporting_only_sa010` - repository records, reports and manager
  views store role-level aggregates only (`SA-010`). `evaluate_role_measures()`
  rejects every key in `FORBIDDEN_MEASURE_FIELDS` (`IDENTITY_FIELDS` plus
  participant IDs, quotes, individual scores/times and per-participant row
  lists) and refuses to run unless `agreed_with_staff = True`, `agreed_date` is
  a valid ISO `YYYY-MM-DD` date on or before `measurement_date`, and at least
  one `named_human` staff representative is recorded.

Draft `SA-010` staff audit-use statement (`DEFAULT_AUDIT_USE_STATEMENT`, to be
agreed with staff representatives before recording any staff measure):

> Usability testing measures evaluate the Zava Forward prototype, task scripts,
> and manual fallbacks only. Results are reported solely as role-level
> aggregates (minimum cell size 5) and are never used for individual
> performance management, disciplinary action, capability review, or staff
> surveillance (SA-010).

Governance agreement record (blank):

| Gate item | Named agreeing human(s) | ISO date | Status |
| --- | --- | --- | --- |
| Test plan, cohorts and thresholds as hypotheses (owner) | | | Not agreed |
| Audit-use statement agreed with staff representatives first (SA-010) | | | Not agreed |
| Lawful basis, optional recording and retention schedule (DPO) | | | Not agreed |
| Voluntary resident and representative recruitment and ethics route | | | Not agreed |
| Task-script plain-language wording review (owner and Engagement) | | | Not reviewed |

## Task scripts derived from the profile journey contract and learning-test bundles

`derive_task_scripts()` and `validate_task_scripts()` generate and verify 21
canonical task scripts (`T0`, `T1` to `T8`, `R-J1` to `R-J6`, `R-R1`, and
`B1-story-once` to `B5-funding-evidence`). Every script binds all five
`profile_journey_contract.ELEMENTS` (`entry`, `evidence`, `safe_endpoint`,
`recovery`, `handoff`), live `perspective_walkthroughs.register()` coverage
states (`partial` versus `unmet` and `PROXY_ONLY`), and an explicit manual or
staffed non-digital fallback prompt.

### Core staff and contractor lookup task (`T0`, SA-009)

| Script ID | Target cohorts | Five-element contract summary (`entry` -> `handoff`) | Linked requirements and checks | Manual fallback |
| --- | --- | --- | --- | --- |
| `T0` | All 10 staff cohorts and `provider-contractor` | Open role queue/workbench for a named synthetic home without hints (`entry`); inspect stage, linked evidence and plain-language status (`evidence`); state whether any safety, consent or funding hold applies (`safe_endpoint`); recover from a missed filter/search (`recovery`); name the single accountable human owner for the next step within 5 minutes (`handoff`) | `SA-009`, `SA-010`, `NFR-009`; `UX-01`, `UX-02`, `UX-05`; covers all 6 `SIX_STAFF_PROFILES` | Complete the same lookup and owner check on the current spreadsheet/manual register |

### Staff and contractor profile-contract scripts (`T1` to `T8`)

| Script ID | Derived from | Perspectives and same-home profiles | Five-element contract and register gap focus | Constructed failure case and manual fallback |
| --- | --- | --- | --- | --- |
| `T1` | `UX-01`, `UX-02`; `profile_journey_contract` | `asset-investment` (`PROXY_ONLY`), `programme-coordinator`, `procurement-contracts` (`PROXY_ONLY`), `digital-auditor` (`PROXY_ONLY`); `Retrofit Programme Manager` | Confirm role scope (`entry`), read non-colour portfolio/contract indicators (`evidence`), state role and proxy boundaries (`safe_endpoint`), return from out-of-scope panel (`recovery`), name follow-up owner (`handoff`) | Filter retained across role switch; verify boundaries from the manual governance matrix |
| `T2` | `UX-01`, `UX-03`; `profile_journey_contract` | `programme-coordinator`, `repairs-building-safety`, `digital-auditor` (`PROXY_ONLY`); `Retrofit Programme Manager`, `Building Safety Liaison` (`FR-025`, `NFR-008`, `NFR-009`) | Open exception/safety queue (`entry`), separate hazard clocks, empty states and load failures by text (`evidence`), hold progression while keeping emergency routes open (`safe_endpoint`), recover from empty filter or simulated failure (`recovery`), route highest-risk item (`handoff`) | Failed load misread as zero work; triage via manual hazard and escalation log |
| `T3` | `UX-04`; `profile_journey_contract` | `asset-investment` (`PROXY_ONLY`), `retrofit-case-team`, `assessor-designer` (`recovery` unmet in register), `procurement-contracts` (`PROXY_ONLY`), `finance-grants` (`recovery` unmet in register); `Retrofit Coordinator`, `Grants and Evidence Officer` (`FR-009`, `FR-015`, `NFR-009`) | Open synthetic home awaiting technical/capacity/grant check (`entry`), inspect survey, stock, capacity and funding IDs (`evidence`), refuse advancement on `Unknown` (`safe_endpoint`), record safe held state (`recovery`), assign missing-evidence owner (`handoff`) | Ready-for-review misread as approved; verify against manual PAS 2035 and grant checklist |
| `T4` | `UX-05`; connected same-home contract | All 6 `SIX_STAFF_PROFILES` (`programme-coordinator`, `retrofit-case-team`, `housing-resident-engagement`, `repairs-building-safety`, `quality-assurance`, `finance-grants`; `NFR-008`, `NFR-009`, `AC-071`) | Inspect `Offered` or `Escalated` handoff (`entry`), compare `Current owner`, chase owner and `Next action` across all 6 profiles (`evidence`), retain sender accountability until confirmed (`safe_endpoint`), escalate overdue transfer without orphaning (`recovery`), confirm receiver transfer (`handoff`) | Returned or unconfirmed handoff left ownerless; record and chase on manual transfer register |
| `T5` | `UX-06`; advisory AI boundary | `programme-coordinator`, `retrofit-case-team`, `quality-assurance`, `finance-grants` (`FR-010`, `NFR-009`, `NFR-015`) | Open panel with advisory summary (`entry`), inspect cited records, freshness and uncertainty (`evidence`), reject/edit unsupported draft with zero domain auto-write (`safe_endpoint`), switch off or bypass unavailable assistant (`recovery`), record named human reviewer (`handoff`) | Assistant unavailable or stale; complete review end-to-end manually with AI switched off |
| `T6` | `UX-07`; keyboard and zoom workspace | `retrofit-case-team`, `assessor-designer`, `quality-assurance`; `Retrofit Coordinator`, `Quality Inspector` (`NFR-001`, `NFR-009`, `AC-093`) | Enter single-case workspace by keyboard (`entry`), inspect stage, checklist and evidence at 200% and 400% zoom (`evidence`), verify focus ring and status announcement (`safe_endpoint`), return to exact queue filter and focus anchor (`recovery`), confirm next owner stays visible (`handoff`) | Hover-only or clipped control at zoom; update via printable/manual case pack |
| `T7` | `UX-08`; PR-002 redaction and channels | `housing-resident-engagement`, `retrofit-case-team`, `repairs-building-safety`; `Resident Liaison Officer`, `Retrofit Coordinator`, `Building Safety Liaison` (`FR-029`, `FR-032`, `NFR-009`) | Open synthetic household with language, access and non-digital preferences (`entry`), verify RLO/Safety see adjustment reason while non-reason roles see held notice (`evidence`), prepare synthetic-only communication (`safe_endpoint`), handle withdrawn consent or channel switch (`recovery`), hand over agreed slot to RLO (`handoff`) | Missing contact field shown as invented value; prepare contact sheet via staffed phone/paper workflow |
| `T8` | Contractor contract in [suppliers](./customer-journeys/suppliers.md); `UX-04`, `UX-05` | `provider-contractor` (`handoff` unmet in register), `quality-assurance`; `Quality Inspector` (`FR-015`, `NFR-008`, `NFR-009`) | Open issued contractor work order and job pack (`entry`), verify resident notes, hazards and finance data are absent (`evidence`), submit checklist evidence and confirm receipt reads `Submitted` not `Accepted` (`safe_endpoint`), remediate a returned submission (`recovery`), route to independent named Quality Inspector (`handoff`) | Rejected submission without stated reason or worker receipt read as QA acceptance; submit via staffed field-evidence intake |

### Resident and authorised representative scripts (`R-J1` to `R-J6`, `R-R1`)

Derived live from `journey_register.JOURNEYS` and [resident journeys](./customer-journeys/residents.md)
(`FR-029`, `FR-032`, `NFR-008`, `NFR-009`):

| Script ID | Journey in `journey_register.JOURNEYS` | Primary cohorts | Five-element observation focus | Non-digital manual route |
| --- | --- | --- | --- | --- |
| `R-J1` | `J1`: Choose each proposed measure | `resident`, `resident-representative`, `housing-resident-engagement` | Enter without internal case ID; read plain-language measure scope and read-only portal boundary; confirm declining one measure does not cancel support; hand off questions to named RLO | Staffed telephone or printed measure-choice pack |
| `R-J2` | `J2`: Pause, withdraw or ask for more time | `resident`, `resident-representative`, `housing-resident-engagement` | Request a pause or withdrawal of optional consent without tenancy or repairs detriment; verify plain-language confirmation and named RLO owner | Staffed telephone or written pause notice |
| `R-J3` | `J3`: Compare appointment offers and confirmations | `resident`, `resident-representative`, `housing-resident-engagement` | Distinguish offered, responded and confirmed appointments; recover from a provider cancellation; confirm access adjustments without repeating household notes | Staffed telephone appointment scheduling and posted confirmation |
| `R-J4` | `J4`: Know who will update you and when | `resident`, `resident-representative`, `housing-resident-engagement` | Identify named owner, due date and update channel; handle an overdue update or changed contact number safely without old-route disclosure | Staffed telephone callback log and printed contact card |
| `R-J5` | `J5`: Handover, practise controls and get aftercare | `resident`, `resident-representative`, `housing-resident-engagement` | Use plain-language heating/ventilation handover guidance; report a reopened damp or defect concern; trace escalation to Building Safety Liaison or RLO | In-person demonstration, printed quick-start guide and staffed repairs line |
| `R-J6` | `J6`: Challenge, complain and follow a remedy | `resident`, `resident-representative`, `housing-resident-engagement` | Distinguish a closed response from an open remedy; raise a formal complaint or redress query without detriment or loss of retrofit support | Staffed telephone, paper or assisted complaint intake |
| `R-R1` | `R1`: Task-limited representative briefing and actions | `resident-representative`, `resident`, `housing-resident-engagement` | Verify task-limited and time-bounded representative authority, scoped fields, and separate resident consent before any representative action is recorded | Staffed telephone verification and paper authority check with RLO |

### Two-arm learning-test bundle scripts (`B1` to `B5`)

Derived live from `learning_test_bundles.BUNDLES` and the five learning-test
rows in [Customer Journey Atlas](./customer-journeys/customer-journey-atlas.md).
Out-of-scope opportunities `O10`, `O18`, `O19` and `O20`
(`learning_test_bundles.OUT_OF_SCOPE`) are excluded and rejected by
`validate_task_scripts()`. Shared opportunity `O16` must be declared under a
single bundle (`o16_counted_under`) via `reconcile_o16()` before comparing runs.

| Script ID | Bundle key and Atlas IDs | Non-AI comparator vs workflow arm | Target cohorts and linked requirements | Zero-target stop rule (evaluated before effort) | Constructed Atlas failure cases |
| --- | --- | --- | --- | --- | --- |
| `B1-story-once` | `story-once` (`O01`, `O02`, `O03`, `O15`) | `Manual re-asking and chase log` vs `workflow` | `resident`, `resident-representative`, `housing-resident-engagement` (`FR-045`, `FR-048`, `AC-062`, `AC-064`) | Zero `authority_or_consent_breaches` and zero `promises_without_owner` | Resident declines one measure; withdraws optional sharing; switches to phone/paper channel |
| `B2-pre-visit-pack` | `pre-visit-pack` (`O04`, `O05`, `O06`, `O07`, `O17`) | `Separate notes and manual visit prep` vs `workflow` | `assessor-designer`, `housing-resident-engagement`, `repairs-building-safety`, `provider-contractor` (`FR-009`, `FR-025`, `FR-029`, `NFR-008`) | Zero `missed_safety_or_adjustment_flags` and zero `unauthorised_detail_disclosures` | No-access visit recovery; newly reported damp/mould hazard hold; PR-002 contractor redaction check |
| `B3-change-impact` | `change-impact` (`O08`, `O09`, `O11`, `O16`; `O16` single-count rule) | `Spreadsheet rework across teams` vs `workflow` | `programme-coordinator`, `retrofit-case-team`, `procurement-contracts`, `finance-grants` (`FR-009`, `FR-015`, `AC-034`, `AC-043`) | Zero `silent_scope_or_date_changes` and zero `unowned_rework_handoffs` | Survey scope change invalidates readiness; supplier capacity delay; grant/tenure hold |
| `B4-handover-aftercare` | `handover-aftercare` (`O12`, `O13`, `O14`, `O21`, `O22`) | `Standard pack and reactive repairs chasing` vs `workflow` | `resident`, `quality-assurance`, `housing-resident-engagement`, `repairs-building-safety` (`FR-015`, `FR-032`, `NFR-008`, `NFR-009`) | Zero `premature_closures_or_unaccepted_handovers` and zero `unrouted_defect_escalations` | Post-install defect reopens case; worker receipt shown as Submitted not Accepted; formal complaint route |
| `B5-funding-evidence` | `funding-evidence` (`O16`, `O23`, `O24`; `O16` single-count rule) | `Manual evidence assembly at claim time` vs `workflow` | `finance-grants`, `quality-assurance`, `digital-auditor` (`FR-015`, `AC-042`, `NFR-009`) | Zero `unsupported_or_unreviewed_claim_items` and zero `self_approved_evidence_signoffs` | Missing/stale attachment holds claim; replaced evidence requires fresh independent review; `O16` counted once |

## Demo-first, desktop-only first slice

The first sessions run on the two surfaces that already exist, not on a
production service. This slice narrows where and on what the programme starts;
it removes nothing from the full programme above.

| Surface | Location | Viewport | Data and label |
| --- | --- | --- | --- |
| Employee workbench demo | `src/api/src/zava_forward/api/web/` | Desktop, 1280 CSS px only | Constructed synthetic cases; `Synthetic walkthrough - not user validation` unless a real representative attends |
| Resident showcase demo | `src/api/src/zava_forward/api/resident_demo/web/` | Desktop, 1280 CSS px only | `Synthetic showcase - not a live resident service`; no real resident identity |

Scripts in this slice:

* Employee view: `T0` (find-case task, the SA-009 hypothesis), `T4` (handoff
  owner) and `T5` (advisory AI review with the assistant switched off as the
  manual path).
* Resident view: `R-J1` (choose each proposed measure), `R-J2` (pause,
  withdraw or ask for more time) and `R-J3` (compare appointment offers and
  confirmations), each with its staffed telephone or
  printed fallback.

Rules for the slice:

* Tablet (768), mobile (360), reflow (320), field use and assistive-technology
  device matrices stay in the full programme and are not claimed here. Keyboard
  operation, 200% text resize and 400% zoom are still checked at the 1280 CSS px
  desktop width, because the accessibility clauses above apply to every session.
* No participant data is stored in this repository. Aggregate measures only,
  after the `SA-010` agreement with named staff representatives; the agreement
  is still unrecorded, so no staff session is scheduled by this page.
* Sessions with colleagues or other proxies are `proxy-pilot` runs and carry the
  non-validation label. The resident demo must not be offered to real residents
  as a service, and every resident session stays voluntary with a manual route.
* Every outcome, including negative and inconclusive ones, goes into the results
  record. Nothing in this slice fills a human result row or ticks a #155
  criterion.

## Measures (aggregate only, SA-010)

`evaluate_role_measures()` enforces `MIN_CELL_FLOOR = 5` and prior `SA-010`
staff agreement:

* When `participant_count == 0`, cohort status is `not_run` and all metrics are
  `None`.
* When `1 <= participant_count < 5`, cohort status is `suppressed_small_cell`
  (`suppressed = True`, `suppression_reason = "cell_below_min_floor_5"`), and
  `participant_count` plus all counts, percentages and SUS numbers are masked
  to `None` so small-group identities cannot be inferred. Any `H4` boundary or
  stop-rule breach still sets `h4_stop_rule_breach = True` (`not_supported`)
  without leaking participant counts.
* When `participant_count >= 5`, raw counts and whole-number percentages are
  reported alongside `thresholds_are_hypotheses = True`,
  `user_validation_established = False` and `human_usability_signoff = False`.

| Measure | Per-cohort aggregate (`n >= 5` only) | Sub-5 cell rule (`1 <= n < 5`) | Notes |
| --- | --- | --- | --- |
| `T0` unaided completion under 5 minutes | Raw count of `n` and whole-number percent (`unaided_under_5m_count`, `unaided_under_5m_pct`) | Masked to `None` (`inconclusive`) | `H1` hypothesis on staff and contractor cohorts; `not_applicable` on `resident` and `resident-representative` |
| SUS score | Median, minimum and maximum (`sus_median`, `sus_min`, `sus_max`) when `numeric_sus_count >= 5` | Masked to `None` (`inconclusive`) | `H2` hypothesis; participants may choose the accessible plain-language alternative (`accessible_sus_alternative_count`), returning `inconclusive` if numeric SUS respondents `< 5` |
| Manual or non-digital fallback completion | Raw count of `n` and whole-number percent (`manual_fallback_completed_count`, `manual_fallback_completed_pct`) | Masked to `None` (`inconclusive`) | `H3` parity requirement (`NFR-009`, `AC-071`); using the manual route is never scored as a failure |
| Stop-rule or consent-blur events | Raw count (`stop_rule_or_consent_blur_count`) and boolean `h4_stop_rule_breach` | Count masked to `None`, boolean `h4_stop_rule_breach` preserved | `H4` target zero; any nonzero count forces `h4_zero_boundary_breaches = "not_supported"` |
| Volunteered assistive-technology barriers | Anonymised count by severity in the findings log | Logged without cohort `n` or personal detail | Recorded only where AT support was volunteered |

## Findings log contract

`log_finding()` and `validate_findings_log()` validate every finding without
participant identity or email patterns:

| Field | Validation rule |
| --- | --- |
| `finding_id` | Unique `UF-001` and up (`^UF-\d{3,}$`) |
| `target_id` and `cohort_id` | Canonical script ID (`T0`..`T8`, `R-J1`..`R-R1`, `B1`..`B5`), perspective, journey or bundle key, plus tested cohort or `cross-role` |
| `observation` and `impact` | Non-blank plain-language paraphrased text with zero names, emails or combinable quotes |
| `severity` | `4` (`blocker`: task blocked or consent/safety/authority boundary crossed); `3` (`major`: completed only with moderator assist or heavy workaround); `2` (`minor`: recoverable hesitation); `1` (`note`) |
| `evidence_source` | `moderated_participant`, `proxy_participant`, `proxy_pilot`, or `synthetic_walkthrough` |
| `backlog_issue` | Mandatory GitHub issue reference (`#123` or `https://github.com/<owner>/<repo>/issues/<n>`); unlinked placeholder entries are rejected |
| `status` | `open`, `in_progress`, `retested` (forbidden when `evidence_source` is `synthetic_walkthrough` or `proxy_pilot`), or `accepted_risk` (requires a `named_human` `risk_owner` and non-blank `risk_rationale`) |

Moderated participant findings log (blank):

| Id | Target and cohort | Observation and impact | Severity | Evidence source | Backlog issue | Status |
| --- | --- | --- | --- | --- | --- | --- |
| None recorded | | | | | | |

## Results record

`evaluate_programme_results()` enforces the four-value outcome vocabulary
(`supported`, `not_supported`, `inconclusive`, `not_run`), requires non-empty
`negative_or_failure_notes` on every `not_supported` and `inconclusive` record,
refuses silent omission of expected targets, and keeps
`human_usability_signoff = False`.

### Moderated human participant results (blank)

| Cohort | Evidence source | n | T0 unaided under 5 minutes | SUS median and range | Manual fallback | Stop-rule breaches | Outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| All 13 representative role cohorts and `proxy-pilot` | None (`not_run`) | 0 | Not run | Not run | Not run | Not run | `not_run` |

### Deterministic synthetic walkthrough baseline (`Synthetic walkthrough - not user validation`)

`build_synthetic_walkthrough_report()` executes deterministic contract checks
across `profile_journey_contract.validate()`,
`profile_journey_contract.validate_same_home_walk()`,
`learning_test_bundles.run_report()` and `learning_test_bundles.reconcile_o16()`
on constructed fictional inputs. Every record carries
`evidence_source = "synthetic_walkthrough"`, `not_user_validation = True`,
`validation_label = "Synthetic walkthrough - not user validation"`,
`user_validation_established = False` and `human_usability_signoff = False`.
Negative (`not_supported`) and `inconclusive` outcomes are retained alongside
`supported` shape checks and never populate the human table above:

| Synthetic target group | Evidence label (`not_user_validation = True`) | Synthetic outcome | Retained negative or inconclusive notes |
| --- | --- | --- | --- |
| Direct-role staff perspectives with mapped partial elements (`programme-coordinator`, `retrofit-case-team`, `housing-resident-engagement`, `repairs-building-safety`, `quality-assurance`) | `Synthetic walkthrough - not user validation` | `supported` (5) | Five-element contract shape check passed on constructed inputs; human comprehension and timing remain untested |
| Perspectives with `unmet` register elements or `PROXY_ONLY` login (`asset-investment`, `assessor-designer`, `procurement-contracts`, `provider-contractor`, `finance-grants`, `digital-auditor`) | `Synthetic walkthrough - not user validation` | `inconclusive` (6) | Retains `unmet` `recovery` (`assessor-designer`, `finance-grants`), `unmet` `handoff` (`provider-contractor`), and `PROXY_ONLY` login notes (`asset-investment`, `procurement-contracts`, `digital-auditor`) |
| Connected same-home clean bundle (`same-home-contract`) | `Synthetic walkthrough - not user validation` | `supported` (1) | Constructed 6-staff, contractor, job-pack receipt (`Submitted`) and read-only resident view agree (`complete_in_shape`) |
| Connected same-home negative probe (`same-home-negative-probe`) | `Synthetic walkthrough - not user validation` | `not_supported` (1) | Retains `same_home.handover:worker_receipt_treated_as_acceptance` when a worker receipt is falsely marked accepted |
| Constructed learning bundles (`story-once`, `pre-visit-pack`, `funding-evidence` with `o16_counted_under = "change-impact"`) | `Synthetic walkthrough - not user validation` | `supported` (3) | Zero stop-rule breaches on constructed inputs; saved minutes stay labelled unvalidated capacity |
| Constructed learning-bundle tie (`change-impact`, `o16_counted_under = "change-impact"`) | `Synthetic walkthrough - not user validation` | `inconclusive` (1) | Retains `0.0` minute median difference between workflow and spreadsheet comparator arms |
| Constructed learning-bundle stop-rule probe (`handover-aftercare`) | `Synthetic walkthrough - not user validation` | `not_supported` (1) | Retains `1/workflow/premature_closures_or_unaccepted_handovers` STOP breach before reading effort |

## Acceptance criteria status for issue #155

| Criterion | Engineering and specification status (2026-11-15) | Remaining human gate before ticking or closing #155 |
| --- | --- | --- |
| Test plan names tasks, participants per role, accessibility support, consent and data handling | Specification and `validate_programme_plan()` delivered: 21 tasks, 5 to 8 target per all 13 role cohorts plus 2 to 3 `proxy-pilot`, 8 accessibility clauses, 4 AT routes and 8 consent/data clauses | Named owner review and ratification of plan and voluntary resident/representative sizing; DPO retention and ethics decision |
| Task scripts derive from the profile journey contract and learning-test bundles | `derive_task_scripts()` and `validate_task_scripts()` derive `T0`, `T1`..`T8`, `R-J1`..`R-R1` and `B1`..`B5` live from `profile_journey_contract`, `perspective_walkthroughs`, `journey_register` and `learning_test_bundles` (excluding `O10`, `O18`..`O20`) | Owner and Resident Engagement wording review; execution of `proxy-pilot` and moderated sessions |
| Measures are aggregate only and the audit-use statement is agreed with staff first (SA-010) | `validate_audit_use_agreement()` and `evaluate_role_measures()` block unagreed or backdated runs, reject `FORBIDDEN_MEASURE_FIELDS`, and mask `1 <= n < 5` cells to `None` | Written `SA-010` agreement with named human staff representatives before any staff session runs |
| Findings are logged with severity and linked to backlog issues | `log_finding()` and `validate_findings_log()` enforce `UF-NNN`, `1..4` severity, anonymisation, mandatory GitHub issue links (`#N` or URL), `named_human` risk acceptance and human retest rules | Logging real findings from moderated sessions and retesting fixes with representative participants |
| Results record negative and inconclusive outcomes; synthetic walkthroughs are labelled as not user validation | `evaluate_programme_results()` and `build_synthetic_walkthrough_report()` retain `supported` (10), `not_supported` (2) and `inconclusive` (6) synthetic records stamped `not_user_validation = True` (`Synthetic walkthrough - not user validation`), keeping human rows `not_run` | Moderated participant sessions across staff, contractor, resident and AT cohorts (`#150`, `#151`, `#128`) |

## Next slices (proposed)

* Owner review of this specification and written `SA-010` agreement with named
  staff representatives before scheduling any staff session.
* DPO and ethics decision on lawful basis, optional recording and retention
  schedule (`#128`).
* Dry-run calibration with 2 to 3 `proxy-pilot` participants (labelled non-user
  validation), followed by moderated sessions with 5 to 8 representative users
  per reachable cohort including assistive-technology users (`#151`).

## Historical delivery status record (2026-11-04, #155)

Merged engineering evidence at 2026-11-04 (#1004) was limited to the initial
draft plan: drafted tasks, participants per role, accessibility support, consent
and data handling, aggregate-only measures, findings and results templates, with
no participant, session, staff agreement, finding or result recorded.

## Delivery status update (2026-11-15, Refs #155)

The 2026-11-15 slice upgrades this specification in place and adds deterministic
validation and evaluation in
[`usability_programme.py`](../../../../src/core/src/zava_forward/core/usability_programme.py)
and [`test_usability_programme.py`](../../../../src/core/tests/test_usability_programme.py):
5 to 8 participants across all 13 representative role cohorts (plus a 2 to 3
`proxy-pilot`), live script derivation across the 11 perspectives, 6 same-home
staff profiles, 7 resident/representative journeys and 5 two-arm learning
bundles, `SA-010` prior `named_human` staff agreement and sub-5 `None` cell
masking, mandatory GitHub issue links on severity-tagged findings, and a
labelled `Synthetic walkthrough - not user validation` (`not_user_validation =
True`) baseline preserving `supported`, `not_supported` and `inconclusive`
outcomes while keeping every human session row `not_run`.

No human acceptance criterion on #155 is ticked or closed (`Refs #155` only):
owner ratification, DPO sign-off, written `SA-010` staff agreement, participant
recruitment and moderated human and assistive-technology sessions (`#150`,
`#151`, `#128`) remain open human work.

