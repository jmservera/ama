---
title: Data Dictionary - Retrofit Synthetic Evidence Pack
description: Field definitions, keys, allowed values and record-keeping notes for the Zava Forward year-one synthetic evidence pack
ms.date: 2026-10-13
ms.topic: reference
---

> [!WARNING]
> SYNTHETIC DATA. Fictional records for design and analysis practice. Not
> Zava North Homes data. Every table has `is_synthetic` set to `true`.

## Separate Private MVP JSON Extension

The [dated coverage recipe](./README.md#mvp-operational-coverage-2026-10-13)
extends the separate private MVP export, not these public CSV schemas.

| Field or structure | Grain and meaning |
| --- | --- |
| `as_of`, `built`, `seed`, `generator_version`, `is_synthetic` | Explicit deterministic exercise date and provenance |
| `stock_register_rows` | Geography-stock denominator, not programme-case count |
| `case.synthetic_stock_anchor_id` | Selected private geography row; multiple flats may share a building anchor |
| `case.history` | Retained shifted simulation states, labelled source export, not workbench approvals |
| `case.appointments[].fixture` | `forward-visit` or `historical-visit` for added labelled scenarios; source appointments remain |
| `procurement.packages`, `procurement.work_orders` | Source-issued simulation orders and synthetic capacity allocation; not live contract authority |
| `case.finance`, `case.grants`, `case.quality` | Pending/received/unverified operational fixtures; no approval, acceptance or payment implied |
| `case.handoff`, `case.service_requests` | Offered transfers and open service/redress scenarios, with resolvable staff references |

The private coverage sidecar counts booked visits and their current-week
intersection. `/api/visits` returns booked appointments by owner/all; it does
not implement a date-range filter. Historical outcomes stay in case detail.

## Identifiers and Relationships

| Identifier | Format | Notes |
| --- | --- | --- |
| `property_id` | `SYN-PROP-000123` | Group property ID. Duplicates from the merger use `SYN-PROP-9xxxxx` |
| `legacy_ref` | `HA-041697` or `HB/10813` | Heritage A and Heritage B references. Used by the repairs system and some suppliers |
| `parent_building_id` | `SYN-BLDG-00045` | One building per house; flats share a block building and `shared_system_id` |
| `candidate_id` | `CAND-2025-0001` | One per candidate home. `CAND-D-nnn` rows are later duplicates |
| `property_ref` | Any of the above | As typed in the source; may be a legacy reference or a typo |
| `resident_ref` | `R-SYN-00001` | Changes when a void home is relet |

`candidate_id` is the main join key. Rows without it must be matched through
`property_ref`, `repairs_property_ref` or the property register.

## Dates

| Table | Format |
| --- | --- |
| `candidate-lifecycle.csv` | `dd/mm/yyyy`, with some free-text values such as `w/c 09/03/2026` |
| `lifecycle-events.csv` | ISO `yyyy-mm-dd`, except `CONTRACTOR_PORTAL` rows in `dd/mm/yyyy` |
| `appointments.csv` | `dd/mm/yyyy` |
| `resident-contacts.csv` | `yyyy-mm-dd hh:mm` |
| Other tables | ISO `yyyy-mm-dd`, with occasional `dd/mm/yyyy` in the property register |

## property-register.csv

| Field | Meaning |
| --- | --- |
| `property_id`, `legacy_ref`, `uprn` | Identifiers. `uprn` is synthetic and sometimes blank |
| `parent_building_id`, `shared_system_id` | Building and shared envelope system |
| `heritage_org` | `Heritage A` or `Heritage B` |
| `locality` | `Locality A - urban core`, `Locality B - former coalfield towns` or `Locality C - rural and coastal` |
| `archetype_id`, `archetype_label` | `ARC-01` pre-1919 solid-wall terrace; `ARC-02` 1945-64 cavity house; `ARC-03` 1965-80 low-rise flat block; `ARC-04` off-gas bungalow; `ARC-05` 1980-99 house; `ARC-06` non-traditional PRC house |
| `property_type`, `construction_type`, `year_built`, `heating_fuel` | Descriptive attributes. `year_built` may be `pre-1919` or blank |
| `tenure` | `Social rent`, `Affordable rent` or `Shared ownership` |
| `current_epc`, `epc_sap`, `epc_lodgement_date` | Latest lodged EPC band, SAP score and date |
| `roof_renewal_due_year`, `windows_renewal_due_year` | Planned maintenance programme year |
| `damp_reports_24m` | Damp or mould repair reports in the last 24 months |
| `occupancy_status` | `Occupied` or `Void` at extract |
| `leaseholders_in_building` | Leaseholders in a flat block; building attribute repeated on each flat |
| `address_legacy` | Fictional address text as held in the legacy register |

## candidate-lifecycle.csv

The team's tracker. It holds the current state only.

| Field | Meaning |
| --- | --- |
| `wave`, `candidate_identified_date` | Cohort and identification date |
| `selection_rule_version`, `priority_score` | `SEL-2025.1` or `SEL-2026.1` (damp-weighted from 2026-01-12) and the score at identification |
| `locality`, `archetype_id`, `measures`, `lead_supplier` | Scope summary |
| `current_status` | v2 list: `01 Identified`, `02 Contacting resident`, `03 Survey booked`, `04 Survey complete`, `05 In design`, `06 Awaiting resident decision`, `07 Ready to order`, `08 Ordered`, `09 On site`, `10 Practical completion`, `11 Handed over`, `12 Closed`, `On hold`, `Reopened`, `Withdrawn`, `Excluded`. Rows untouched since 2026-02-02 carry v1 labels such as `Design`, `Complete`, `Closed` or `Hold` |
| `status_last_updated` | Date the row was last edited, not necessarily when the status changed |
| `owner` | Staff code, occasionally a role name or blank |
| `rag_status` | Manually set RAG |
| `delay_code`, `delay_notes` | One code from the v1 or v2 dictionary, and free text |
| `next_action_due` | Planned next action date |
| `closure_reason` | Reason recorded for `Withdrawn` or `Excluded` |
| `survey_date` to `handover_date` | Milestone dates typed by the team. `handover_date` is the resident handover visit |

## lifecycle-events.csv

A first-pass event log assembled from tracker version history, mailboxes and
system extracts. Contact attempts, appointments, inspections, evidence
reviews and repairs detail are in their own tables.

| Field | Meaning |
| --- | --- |
| `event_date`, `event_type` | When and what |
| `source_system` | `ASSET_EXTRACT`, `TRACKER`, `MAILBOX`, `ASSESSOR_PORTAL`, `CONTRACTOR_PORTAL`, `CRM`, `QA_LOG`, `EVIDENCE_LOG`, `GRANT_TRACKER`, `HOUSING_MGMT`, `PLANNED_MAINTENANCE` or `PROGRAMME` |
| `actor`, `from_team`, `to_team` | Who acted, and the handoff direction where relevant |
| `outcome`, `reason`, `evidence_version`, `notes` | Outcome, reason code or text, version of the design (`D-vn`), assessment (`RA-v1`), works decision (`WD-v1`) or evidence pack (`EP-vn`) |

Event types, in rough lifecycle order:

* Entry and scope: `CANDIDATE_IDENTIFIED`, `RESEQUENCED`, `LEASE_REVIEW_REQUESTED`, `LEASE_REVIEW_COMPLETE`, `CONTACT_PAUSED`
* Assessment: `ASSESSMENT_COMPLETED`, `ASSESSMENT_OUTCOME`, `FUNDING_ROUTE_CHANGED`, `HANDOFF_SENT`, `HANDOFF_ACCEPTED`
* Design: `PM_DEPENDENCY_IDENTIFIED`, `PM_WORKS_AWAITED`, `PM_DEPENDENCY_CLEARED`, `DESIGN_RESCOPED`, `DESIGN_SUBMITTED`, `DESIGN_RETURNED`, `DESIGN_APPROVED`, `LEASEHOLDER_CONSULTATION_STARTED`
* Resident: `RESIDENT_WORKS_DECISION`, `DESIGN_VARIATION_REQUESTED`, `RESIDENT_PAUSE_REQUESTED`, `RESIDENT_PAUSE_ENDED`, `PROPERTY_VOID`, `PROPERTY_RELET`, `WITHDRAWAL_CHALLENGED`
* Release: `FUNDING_HELD`, `FUNDING_CONFIRMED`, `SAFETY_HOLD_PLACED`, `SAFETY_HOLD_RELEASED`, `WORK_ORDER_ISSUED`, `BLOCK_PROCEEDED_WITHOUT`
* Delivery: `INSTALL_STARTED`, `INSTALL_ABORTED`, `INSTALL_COMPLETE` (practical completion claimed by the supplier), `REMEDIATION_COMPLETE`, `QA_PASSED`, `EVIDENCE_ACCEPTED` (documentary acceptance)
* Close: `RESIDENT_HANDOVER`, `ACCEPTED_HANDOVER`, `CASE_EXITED`, `AFTERCARE_REPORTED`, `CASE_REOPENED`, `CASE_RECLOSED`

`HANDOFF_ACCEPTED` exists only where the consultancy acknowledged receipt.
Where the assessment report went to the design mailbox on the same day,
`ASSESSMENT_COMPLETED` carries the handoff teams.

## resident-journey.csv and resident-contacts.csv

| Field | Meaning |
| --- | --- |
| `preferred_channel` | `Phone`, `Text message`, `Letter` or `Email` |
| `accessible_format` | Recorded adjustment: `Large print`, `Interpreter`, `BSL`, `Advocate or representative` or `Communication support` |
| `access_constraints` | Recorded availability constraint |
| `priority_support_flag`, `authorised_representative` | `Y` or `N`. No health detail is held |
| `works_decision_status` | `Not yet requested`, `Pending`, `Accepted` or `Declined` |
| `purpose` | `Survey booking`, `Rebook survey`, `Works decision`, `Rebook installation`, `Handover` or `Aftercare` |
| `outcome` | `Contacted`, `No answer`, `Voicemail left`, `Text sent - no reply`, `Letter sent - no reply`, `Email sent - no reply`, `Resident undecided - call back`, `Handover visit completed` or `Inbound report` |
| `adjustment_recorded`, `adjustment_met` | Adjustment on file and whether the contact used it |

## appointments.csv

| Field | Meaning |
| --- | --- |
| `supplier_id`, `supplier_job_ref` | Assessor or supplier and its own job reference |
| `candidate_id` | Blank where the supplier did not store it |
| `appointment_type` | `Retrofit assessment` or `Installation`. Block external wall insulation has no individual appointment |
| `slot` | `AM`, `PM` or `All day` |
| `outcome_code` | `ATT` attended, `NA` no access, `REF` refused, `BOOKED` future |
| `outcome_note` | Operative's note |

## safety-holds.csv

| Field | Meaning |
| --- | --- |
| `repairs_property_ref` | Legacy reference used by the repairs system |
| `hazard_observed_date`, `referral_sent_date` | Survey observation and referral to the repairs and hazard service |
| `repairs_job_ref`, `hazard_category`, `repairs_priority` | Repairs system job, category and priority |
| `investigation_date`, `repair_completed_date` | From the repairs system |
| `retrofit_hold_placed_date`, `retrofit_hold_released_date`, `hold_status_in_tracker` | From the programme tracker |
| `release_evidence_ref` | Repairs job cited as release evidence, or `see email` |

## quality-evidence.csv

| Field | Meaning |
| --- | --- |
| `record_type` | `QA inspection`, `Evidence submission` or `Evidence review` |
| `attempt_no` | Inspection or evidence version number |
| `result` | `Pass`, `Pass with snags`, `Fail`, `Submitted`, `Accepted` or `Rejected` |
| `defects_found`, `max_defect_severity` | `Minor`, `Major` or `Safety-critical` |
| `reason` | Defect or rejection reason |

## grant-and-finance.csv

| Field | Meaning |
| --- | --- |
| `funding_route`, `eligibility_status` | Route and eligibility as recorded |
| `approved_budget`, `committed_cost`, `invoiced_amount` | GBP; budget formatting varies |
| `invoice_status` | `Not invoiced`, `Part-paid (interim valuation)`, `Invoiced - on hold pending evidence` or `Paid` |
| `grant_eligible_amount` | Synthetic grant value for the home |
| `claim_quarter`, `claim_status`, `claim_received_date` | `Not applicable`, `Not yet claimable`, `Awaiting evidence`, `In preparation`, `Submitted`, `Received` or `Rejected by funder` |
| `hold_reason` | Free text |

## contractor-capacity.csv

Suppliers and the assessor framework report monthly `committed_capacity`,
`work_released`, `jobs_started` and `jobs_completed`. Internal teams
(`TEAM-RC`, `TEAM-QA`, `TEAM-GEO`) appear only as a leave planner with
`available_fte` and notes; the team does not track their throughput. The
design consultancy (`DES-1`) reports designs and revisions submitted.

## programme-board-snapshots.csv

Month-end figures as reported to the programme board: `Status count`,
`Delay code count (open cases)` and `KPI`. `Completions reported` counts
practical completions. Figures were produced from the tracker as it stood at
each month end.

## edge-case-returns.csv

The team's issues and escalations log. It records only the returns and
escalations someone chose to log, so it is not a complete record of returns.

## delay-code-dictionary.csv

The v1 codes, used from 2025-07-01 to 2026-02-01, and the v2 codes, used from
2026-02-02. `maps_to_v2` lists possible v2 codes for each v1 code;
`v1_equivalent` gives the broad v1 code for each v2 code.
