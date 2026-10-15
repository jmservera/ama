---
title: Data Dictionary - Retrofit Synthetic Evidence Pack
description: Field definitions, keys, allowed values and record-keeping notes for the Zava Forward year-one synthetic evidence pack
ms.date: 2026-10-14
ms.topic: reference
---

> [!WARNING]
> SYNTHETIC DATA. Fictional records for design and analysis practice. Not
> Zava North Homes data. Every table has `is_synthetic` set to `true`.

## Separate Private MVP JSON Extension

The enriched JSON extension was seeded into the recreated exercise Azure SQL
database on 2026-10-14 after explicit owner reauthorization. Original tenant
staff/oid bindings remain private; synthetic operating records, proposed
budgets, pending grants and unverified quality do not acquire approval merely
because they are persisted in the serving database.

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

## Dataset Coverage and Provenance

[`provenance-register.json`](./provenance-register.json) is the single machine-readable
register of every dataset, its public or private visibility, its generator, its
data dictionary entry and its external sources. The automated check
`src/core/tests/test_synthetic_provenance.py` enforces it.

| Dataset | Visibility | Dictionary entry |
| --- | --- | --- |
| Year-one operating CSV pack and manifest | Public | This file, table sections above |
| MVP operational JSON seed | Private (`mvp/data/`, gitignored) | [Private MVP JSON extension](#separate-private-mvp-json-extension) |
| 60,000-home stock register and map overlay | Private (`support/`) | [Private stock geography register](#private-stock-geography-register) |
| AI evaluation scenarios and assistant runtime tables | Public scenarios, private runtime tables | [Chat and assistant data](#chat-and-assistant-data) |
| Document, form-schema and seeded-defect fixtures | Public | [Document and form data](#document-and-form-data) |
| Sensor readings | Not generated | [Sensor data](#sensor-data) |

External sources record licence, retrieval date and attribution in the register.
OpenStreetMap (ODbL 1.0, retrieved 2026-09-30) is complete. Retrieval dates and
licence wording for Census 2021 TS054, IMD 2025 and the ONS boundaries are open
items for the owner, not inferred here.

### Private stock geography register

`private-north-east-stock-register.csv` holds one row per synthetic home
(`SYN-NE-nnnnnn`). `map_address`, `postcode`, `latitude`, `longitude`,
`osm_object_type` and `osm_object_id` are a real OpenStreetMap anchor
(`location_is_real_map_anchor` is `true`). Tenure, portfolio category, EPC
need, occupancy and condition are invented (`is_synthetic` is `true`,
`actual_owner_or_tenure_verified` is `false`). No resident or person field exists.

### Stock-scale household and tenancy fixture (2026-10-15)

`src/core/src/zava_forward/core/synthetic/scale_fixture.py` (version 1.1.0, seed 174) writes
`households.jsonl` with one row per home in the 60,000-home fixture, rebuilt from
the seed and Git-ignored. Every row has `is_synthetic` set to `true`. Names come
from a fixed fictional list; no email, phone number or real identifier exists.

| Field | Meaning |
| --- | --- |
| `household_ref`, `resident_ref`, `tenancy_ref` | `HH-SYN-nnnnn`, `R-SYN-nnnnn` and `TEN-SYN-nnnnn`; `home_id` links to `homes.jsonl` (`ZF-nnnnn`) |
| `tenancy_type` | `Assured`, `Secure`, `Starter`, `Shared ownership` or `Leasehold`. Invented mix, not Zava tenure data |
| `tenancy_start` | First of a drawn month, 1995 to 2025 |
| `household_size` | 1 to 5 |
| `lead_resident` | Fictional name from the fixed list |
| `preferred_channel`, `adjustment`, `adjustment_recorded` | As in resident-contacts; `adjustment_recorded` is `false` where an adjustment exists but is not on file |
| `priority_support` | Same value as `priority_support` in `homes.jsonl`. No health detail is held |
| `representative_state` | `None recorded`, `Claimed - unverified` or `Authorised - evidence on file`. Never inferred from adjustment or consent, except that the `Advocate or representative` adjustment sets `Authorised - evidence on file` |
| `representative_ref` | `REP-SYN-nnnnn`, empty when `representative_state` is `None recorded` |
| `works_consent_state` | `Not requested`, `Pending`, `Given`, `Declined` or `Withdrawn`. A missing answer is `Not requested` or `Pending`, never `Given` |
| `works_consent_given_by` | `Resident` or `Representative`, empty unless an answer is recorded. `Representative` appears only with `Authorised - evidence on file` |

The distributions are invented for scale testing and are not evidence of Zava
North Homes tenure, consent rates or vulnerability. Consent and representative
rules are demonstrator rules, not legal advice or an approved policy.

### Document and form data

`src/importer/evals/document_form_fixtures.json` holds 120 constructed document families,
form schemas and seeded defects with gold labels. All content is synthetic and
holds no personal data. The real funding form schema (OQ-015) and human
adjudication of the gold labels are open items, not inferred here.

### Chat and assistant data

No free-form chat transcripts are generated. The assistant surfaces create
`assistant_tasks`, `assistant_attempts` and `assistant_events` rows from the
synthetic seed; these hold prompts built from synthetic case fields, bounded
model output labelled as an AI suggestion, and append-only audit events. They
stay in the private serving database. `mvp/evals/ai_priority_golden.json`
holds constructed public scenarios and scripted model outputs.

### Chat and memory test fixtures (2026-10-15)

`src/agents/tests/chat_fixture.py` (version `chat-fixture-v1`, seed 172) writes
JSONL to `chat-fixture/` under the per-user `ZF_DATA` folder, outside the repository, for the per-user chat and memory
backlog (#172, ADR 0004). Every row has `is_synthetic` set to `true`. Text comes
from fixed templates prefixed `[SYNTHETIC`; no real conversation content is used.

| File | Content |
| --- | --- |
| `personas.jsonl` | Two fictional users for each of the eleven PRD perspectives, mapped to an existing Entra app role (fixture mapping, not authorisation) and the assistant tasks that role may use |
| `threads.jsonl`, `turns.jsonl` | Three threads per eligible user, tied to a `ZF-nnnnn` stock case and a registered assistant task; states `active`, `expired` and `deleted_by_owner`, with content removed once expired or deleted |
| `ledger_events.jsonl` | Event metadata only (`content` is null), kept after deletion |
| `memory_state.jsonl`, `memory_items.jsonl` | Opt-in states `not_opted_in`, `opted_in` and `withdrawn`, global and per-task switches, items with source and expiry in `active`, `edited`, `expired` and `deleted` states |
| `exclusion_probes.jsonl` | Seeded health, safeguarding, vulnerability, special-category and consent values that must be rejected |
| `isolation_cases.jsonl` | Same-role and cross-role reads, spoofed user key, role revoked mid-thread, administrator access with and without reason (AC-094, AC-102) |
| `deletion_cases.jsonl` | Expected absence of content and metadata-only ledger after deletion or expiry (AC-095, AC-097) |

The 90-day retention is an illustrative parameter, not a policy. Expected outcomes
are fixture targets for #160 to #164, not evidence that a runtime enforces them.

### Sensor data

No sensor dataset or generator exists. The register records this as an open
item pending an owner decision on scope; no fields are invented here.

### Real-person guarantee

Public datasets must contain no email address, UK phone number, National
Insurance number or real-looking postcode, and every record carries
`is_synthetic=true`. Real map addresses appear only in private datasets. The
check fails when a pattern or an unlabelled record appears, or when a private
path is not ignored or held under `support/`.
