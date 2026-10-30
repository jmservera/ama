---
title: Data Dictionary - Retrofit Synthetic Evidence Pack
description: Field definitions, keys, allowed values and record-keeping notes for the Zava Forward year-one synthetic evidence pack
ms.date: 2026-10-27
ms.topic: reference
---

> [!WARNING]
> SYNTHETIC DATA. Fictional records for design and analysis practice. Not
> Zava North Homes data. Public operating records use `is_synthetic=true`;
> generated families use the explicit label contracts below. Actual user chat
> and tenant bindings are private and are not certified synthetic.

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
| `stock_link` | Seed-only report with one resolution per case, linked/unlinked totals, unlinked IDs/reasons and shared source-anchor counts; legacy home-count keys do not count verified dwellings |
| `case.stock_link` | `case_id`, nullable `stock_home_id`, `status` (`linked` or `unlinked`), nullable `reason`, `shared_anchor`, `scope`, `is_synthetic`; exact source-reference match, not verified unit identity |
| `case.stock_fabric` | Unique matched source row's seeded build year/age band, dwelling type, construction, heating, v1 draw version and both synthetic labels; not survey/EPC/company evidence |
| `case.history` | Retained shifted simulation states, labelled source export, not workbench approvals |
| `case.appointments[].fixture` | `forward-visit` or `historical-visit` for added labelled scenarios; source appointments remain |
| `procurement.packages`, `procurement.work_orders` | Source-issued simulation orders and synthetic capacity allocation; not live contract authority |
| `case.finance`, `case.grants`, `case.quality` | Pending/received/unverified operational fixtures; no approval, acceptance or payment implied |
| `case.handoff`, `case.service_requests` | Offered transfers and open service/redress scenarios, with resolvable staff references |

The private coverage sidecar counts booked visits and their current-week
intersection. `/api/visits` returns booked appointments by owner/all; it does
not implement a date-range filter. Historical outcomes stay in case detail.

The [stock fabric CLI](../../../../src/core/README.md#stock-fabric-and-case-references-168)
records `missing_stock_anchor`, `invalid_stock_anchor`, `stock_anchor_not_found`
or `ambiguous_stock_anchor`; invalid/duplicate case IDs fail the run. Stock IDs
are exact opaque strings without outer whitespace. Shared references remain
source matches, never merged households. Fabric refresh removes the previous
derived `stock_epc` block; the retained builder regenerates it, the standalone
CLI does not. Operational `home.built`/`home.type`, consent and history are not
reconciled or overwritten. Existing populated stores are not automatically
reseeded; top-level link reports remain seed metadata while case fields persist.

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
register of the known dataset families, their public/private visibility,
generators, dictionary entries and external sources. Generation status is
separate from visibility: tested generators do not prove a full-stock run.
The executable `zava_forward.core.synthetic.privacy` checker and core/agents
regressions enforce the bounded contracts, without reading private working data.

| Dataset | Visibility | Dictionary entry |
| --- | --- | --- |
| Year-one operating CSV pack and manifest | Public | This file, table sections above |
| Operational JSON seed | Private (`ZF_DATA`, outside the repository) | [Private MVP JSON extension](#separate-private-mvp-json-extension) |
| 60,000-home stock register and map overlay | Private (`support/`) | [Private stock geography register](#private-stock-geography-register) |
| Stock-scale homes, households/tenancies and events | Private generated snapshots (`ZF_DATA/scale-fixture`) | [Stock-scale fixture](#stock-scale-household-and-tenancy-fixture-2026-10-15) |
| Derived fabric, link reports and linked cases | Private generated snapshots (`ZF_DATA/stock-fabric`) | [Derived fabric and links](#derived-stock-fabric-and-link-reports) |
| Stock EPC, surveys and conflict manifest/summary | Private source-anchor working area (`support/`) | [EPC/survey fixture](#stock-epc-surveys-and-conflicts) |
| AI/chat/regulatory evaluation scenarios and reports | Public constructed scenarios/reports | [Chat and assistant data](#chat-and-assistant-data) |
| Assistant attempts/events and actual chat/memory | Private serving database; potentially personal user content | [Chat and assistant data](#chat-and-assistant-data) |
| Document controls, form-schema and seeded-defect fixtures; eval registry | Public | [Document and form data](#document-and-form-data) |
| Sensor register, readings, estimate and optional fabric | Private generated snapshots (`ZF_DATA/sensor-backfill`); generators and small fixtures delivered | [Sensor data](#sensor-data) |

External sources are inventoried, not all verified. The local source README
records OpenStreetMap ODbL 1.0, retrieval 2026-09-30 and contributor attribution.
Census 2021 TS054, IMD 2025 and ONS boundaries still lack historic retrieval
dates and verified licence/attribution terms. Null dates and provisional wording
remain explicit; a Git commit date is not a retrieval date. The strict source
audit returns nonzero for these three entries. No official-source recheck was
performed in this offline task. Exercise Legal, Compliance and DPO owner
Juan Manuel Servera retains interpretation/approval; real owners and sources
remain a gap before operational reliance.

### Private stock geography register

`private-north-east-stock-register.csv` holds one row per synthetic home
(`SYN-NE-nnnnnn`). `map_address`, `postcode`, `latitude`, `longitude`,
`osm_object_type` and `osm_object_id` are a real OpenStreetMap anchor
(`location_is_real_map_anchor` is `true`). Tenure, portfolio category, EPC
need, occupancy and condition are invented (`is_synthetic` is `true`,
`actual_owner_or_tenure_verified` is `false`). No resident or person field exists.

### Stock-scale household and tenancy fixture (2026-10-15)

`src/core/src/zava_forward/core/synthetic/scale_fixture.py` (version 1.2.0, seed 174) writes
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

The same snapshot includes `homes.jsonl`: `id`, area, stage, fixed fictional
resident name, support/safety flags, numbered Test Road address, fictional
`TE[0-8] 1ST` postcode and invented grid coordinates. `events.jsonl` has `case`,
`seq`, `kind` (contact, appointment, stage_change, hazard_check, decision) and
`day` in the declared calendar year 2026. These two historical payloads inherit
the `source_type=SYNTHETIC` manifest label, bound to exact `file_sha256` values;
they do not have per-row Boolean labels. Manifest version, seed, as-of, source
revision, counts and hashes identify the snapshot; they are not approval.

### Derived stock fabric and link reports

`stock-fabric.csv` has `synthetic_home_id`, `build_year`, `age_band`,
`dwelling_type`, `construction`, `heating`, `fabric_is_synthetic`,
`fabric_version` and `is_synthetic`. `summary.json` records assumptions, seed,
revision, counts and hashes; optional `linked-cases.json` retains the supplied
case dataset with the link/fabric fields documented above. The outputs are
private: an arbitrary input case snapshot may contain personal data. The
standalone generator refuses repository output paths. No private dataset is
opened by the public provenance tests.

### Stock EPC, surveys and conflicts

The retained `zf_stock_epc.py` generator adds EPC band/SAP, lodgement/expiry
dates, status and recorded age/dwelling/construction/heating; about 35% of
constructed homes have survey type/date, surveyed SAP/band and fabric values.
`private-stock-epc-conflict-manifest.csv` records home reference, conflict type,
EPC value and surveyed value. `private-stock-epc-summary.json` holds counts
and assumptions; the full EPC CSV remains private generated working data.
The operational seed's `case.stock_epc` and `stock_epc_seed` carry derived
values, not verified certificates. This is schema-level coverage from the
[existing recipe](./README.md#stock-epc-survey-and-conflict-fixtures-2026-10-15),
not a new private-output inspection or reproduction. Stock and case EPC
denominators are not reconciled; the owner has not confirmed the conflict mix.

### Document and form data

`src/importer/evals/document_form_fixtures.json` holds 120 constructed document families,
form schemas and seeded defects with gold labels. All content is synthetic and
holds no personal data. The real funding form schema (OQ-015) and human
adjudication of the gold labels are open items, not inferred here.
The registered `DS-FICT-FORM-REVIEW-PACK` is a separate, fictional review pack,
`src/core/evals/fictional_form_review_pack.json`, with a versioned template
`FICT-FUND-FORM`, per-field type, unit, authority, evidence, freshness and
lineage, proposed preparer/reviewer separation and stale-propagation data, and
fourteen unresolved Finance decision fields. It is not an approved template;
see the [review guide](./form-review-pack-97.md).
`src/core/evals/document_control_fixtures.json` separately holds labelled
`cases` with constructed home references, uploads/scan classes, retention
triggers and legal-hold fixtures. These are not actual documents, retention
policy or legal approval. Form `families` and control `cases` require labels;
nested metadata inherits its labelled record, and existing nested Boolean
declarations must remain true. `src/agents/evals/registry.json` supplies dataset
version, owner, purpose, consumers and `contains_real_data=false`; the provenance
register adds visibility, label contract and external sources, without replacing
that evaluation-specific registry.

### Chat and assistant data

Generated fixture turns are scripted; actual chat does store user free text.
The assistant surfaces create
`assistant_tasks`, `assistant_attempts` and `assistant_events` rows from the
synthetic seed; these hold prompts built from synthetic case fields, bounded
model output labelled as an AI suggestion, and append-only audit events. They
stay in the private serving database. Inputs and model outputs are not
automatically personal-data-free. `chat_thread`, `chat_message`, `chat_memory`
and `chat_memory_control` hold owner/case/task context, messages, memory and
switches; the retained ledger holds audit metadata. Runtime access, deletion,
retention and human privacy approvals are independent of fixture validation.

`src/agents/evals/ai_priority_golden.json` and `chat_golden.json` hold constructed
scenarios, scripted outputs, citations and expectations, inheriting their root
constructed/synthetic note. `regulatory_gates_cases.json` holds question,
scenario and expected answer/refusal fields; `regulatory_chat_results.json` and
`regulatory_gates_results.json` hold observed offline outcomes, denominators,
comparators and fixture fingerprints. These inherit the root synthetic label.
They are not live conversations, real-model benefit or human legal grading.
All inherited/exempt content is still pattern-scanned.

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
| `isolation_cases.jsonl` | Same-role and cross-role reads, spoofed user key, role revoked mid-thread, administrator access with and without reason (AC-094, AC-102); explicit contractor actor read/list/search denial expectations against an active eligible staff-owned thread |
| `deletion_cases.jsonl` | Expected absence of content and metadata-only ledger after deletion or expiry (AC-095, AC-097) |

#### Resource-specific isolation coverage (2026-10-18, #172)

All 22 personas still represent eleven perspectives, with existing role/task
mappings unchanged. Thread-owner coverage is derived from `eligible_tasks`,
not from an unconditional eleven-perspective target. The current registry
permits 14 fixture users across seven perspectives to own the 42 seeded threads.
The other four perspectives retain their existing memory/probe representation;
this does not grant them assistant eligibility.

Both contractor personas have empty eligible-task lists and own no threads.
Six explicit `contractor_access_denied` probes cover each contractor as actor
for read, list and search against a real active eligible staff-owned thread.
Missing such a target is an explicit generation error, never a fabricated
owner or silently omitted coverage. Regression tests remove each actor/action
probe and corrupt targets to verify that coverage checks reject the changes.

These remain declarative expected fixtures, not executed runtime authorization.
The earlier eleven-perspective assertion counted memory and was not a failing
thread-ownership test. All nine payload labels/pattern canaries, deletion/expiry
null content, opt-in/withdrawal and metadata-only ledger checks remain separate.
Fresh `write()` manifests hash the generated bytes; no stored chat snapshots or
unrelated frozen source hashes are refreshed. SN-08 remains partial: actual
scope/volume approval is unverified, and OD-45 to OD-49 remain open. ADR 0004
was accepted as written on 2026-10-15 through #158/PR #279; acceptance does not
approve live personal data, retention policy or operational use.

The 90-day retention is an illustrative parameter, not a policy. Expected outcomes
are fixture targets for #160 to #164, not evidence that a runtime enforces them.

### Sensor data

`src/core/src/zava_forward/core/synthetic/sensor_backfill.py` delivers
`sensor-backfill-v2` and register-backed `sensor-backfill-stock-v1`. Small
generated snapshots are tested; a canonical full-stock materialization is
not verified. Neither generation mode reads real device/resident telemetry.

| File / table | Fields and meaning |
| --- | --- |
| `sensors.csv` / `sensor_register` | `sensor_id`, `home_id`, dwelling type/age band, modelled retrofit Boolean, heating/fault profile and `source_type=SYNTHETIC` |
| `readings-NNNN.csv` / `sensor_reading` | `sensor_id`, `reading_id`, `home_id`, UTC `observed_at`, `temperature_c`, `humidity_pct`, `source_type=SYNTHETIC`, `scenario=BACKFILL_2Y`, seed, `schema_version=reading-v1`, `injected_fault` (empty, OUTLIER or STUCK); dropout means absent readings |
| `estimate.json` | Homes/days/cadence, nominal readings, measured sample/estimated rows and storage; estimates, not completed full-run counts |
| `manifest.json` | Version/schema, seed/as-of, source revision, half-open UTC start/end, climate source/model parameters, coverage, actual rows/shards and exact payload hashes |
| Optional `stock-fabric.csv` | Fabric fields above plus synthetic `monitoring_consent` (`granted`, `declined`, `unknown`); only granted fixtures emit readings |

Default history is 730 days from 2024-10-01, hourly, unless explicitly overridden.
Scale mode links fictional `ZF-` homes to `SENS-SYN-` sensors; register mode
retains supplied opaque synthetic IDs and hashes them for sensor IDs. Synthetic
permission fixtures are not resident consent. Default climate is the labelled
`synthetic-uk-seasonal-model-v1`; Met Office/Environment Agency data are not
silently used. The approved opt-in composition now also supports the pinned
paired ERA5 packet, explicit dated synthetic measures and household variation,
as described below. CO2, energy, measured calibration and live publishing
are not delivered by this generator.
Injected faults deliberately include out-of-range measurements; ingestion
validation and privacy/label validation are separate checks.

#### Composed backfill and shared live-stage contract

The [core guide](../../../../src/core/README.md#approved-paired-climate-composition-2026-10-27-refs-177)
defines run/estimate commands, seeds, register consent filtering, measures,
compression, budgets and source-fingerprint behavior. Schema depends on mode,
not the transport:

| Mode / payload | Fields and meaning |
| --- | --- |
| Legacy `reading-v1` | Eleven fields in the table above, including inline historical fault label; not the modern consumer contract |
| Opt-in/composed `sensor-fault-input-v1` | Exactly `sensor_id`, `reading_id`, `home_id`, UTC `observed_at`, `temperature_c`, `humidity_pct`, `source_type`, `scenario`, `seed`, `schema_version`, `temperature_unit`, `humidity_unit`, `calibrated`; no truth labels |
| Observation units/types | CSV strings; temperature finite degC, humidity percent; `calibrated` is lowercase `"true"`/`"false"` in the constructed shared contract, not evidence of physical calibration |
| Identity | Paired reading key `(sensor_id, reading_id)`; canonical stock IDs use hashed `stock-sensor-v2` sensor IDs and timestamp-derived reading IDs; no real device identity implied |
| Fault input | Units must be inspected even though column remains `temperature_c`; wrong-unit exercises declare degF; gaps omit rows; duplicates preserve IDs |
| `analysis/` | Fault-mode inputs, sensor register without fault profile, optional sanitized stock/fabric, estimate and manifest |
| `truth/` | Evaluator-only fault packet label, clean counterfactual, emitted row positions, seed/rates/parameters; separate manifest binds analysis hash |
| Composed manifest | Paired climate/metadata hashes, explicit measure-history hash, model versions/parameters, source revision, seed/window/cadence, selected/excluded IDs, rows/shards and payload hashes |
| Dated measure input | `measure_id`, `home_id`, supported `kind`, whole-second UTC `completed_at`, Boolean `is_synthetic=true`; no inferred dates or actual works |

Stage 2 uses this shared 13-field schema (#186) and proposed IoT Hub identities,
not a second storage schema. The finite offline #110 consumer validates and
appends accepted records to `sensor_reading`; rejected/duplicate/order/unit/
mapping/time/calibration exceptions stay separate from derived analysis.
The [two-stage guide](../../../../src/core/README.md#two-stage-simulator-operation-and-limits-194)
states the live runner is unavailable: provisioning, credential ownership,
rate/replay/failure/cost controls and actual cloud operation remain #184 work.
Three paired observations/home/day implies `3N` records/day, not a measured
billable-message count. Hourly validation is a separate offline cadence.

Climate provenance: the
[retained ERA5 packet](../climate-paired-source-178/open-meteo-era5-durham-2023-2024-metadata.json)
is Open-Meteo/C3S outdoor reanalysis, Durham returned cell 54.75/-1.5,
hourly 0.25-degree source resolution, 17,544 paired hours covering 2023-2024,
retrieved 2026-10-27. Raw SHA-256:
`af76a90414d9ad8f19dacc95a38f06d4c4321a91bdf030ba231558c42506051e`.
Weather data by [Open-Meteo.com](https://open-meteo.com/),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); underlying ERA5 is
Copernicus Climate Change Service (C3S) material. Raw bytes retained unchanged;
bounds summarised and exact timestamps subsampled for synthetic indoor projections.
Hersbach et al. (2023), DOI
[10.24381/cds.adbb2d47](https://doi.org/10.24381/cds.adbb2d47);
Open-Meteo software: Zippenfenig (2023),
[10.5281/ZENODO.7970649](https://doi.org/10.5281/ZENODO.7970649).
The metadata's actual 2026-10-22 terms snapshot records CC BY 4.0/API
non-commercial conditions; underlying C3S reuse remains legally unverified.
Owner approval `owner-approvals-2026-10-27-b` is synthetic-demo-only, not
production/Legal approval or a fresh terms check. Exact provider revision and
server build are not exposed; retained bytes, not a repeat URL request, pin
the data. Sample extrema are not safety/healthy-home or regional design limits.

#### Separate scenario validation pack

`synthetic.sensor_scenarios`, version `sensor-scenarios-exercise-v1`, uses
clean backfill identities/schema with explicit exercise overlays. It does not
write to general history or use the ERA5 bytes. See the
[runnable scenario guide and full parameters](../../../../src/core/README.md#synthetic-scenario-validation-pack-190-192-193-194).
All windows, profile values, sizes and comparator thresholds are exercise
assumptions, not sourced physical findings.

| Payload / field | Type, units and meaning |
| --- | --- |
| `analysis/C01.csv`..`C11.csv` | Shared 13-field strings above; neutral case IDs, common `scenario=SCENARIO_PACK`, actual pack seed and `source_type=SYNTHETIC`; no labels/expected outcomes/RNG keys |
| `analysis/windows.json` | Version/source strings, `start`/`end_exclusive` UTC strings, integer `cadence_minutes=60`; list of neutral `case_id`, relative `file` and nullable UTC `measure_at` |
| `truth/cases.json` | One evaluator record per case: `case_id`, `family` (`damp`/`retrofit`), `label`, integer `seed`, string `rng_key`, `expected_outcome`, numeric `temperature_delta_c`/`humidity_delta_points`, integer `delay_days` |
| Damp truth labels | normal, condensation_prone, sustained_high_humidity, repeated_overnight_peaks, sensor_fault, missing_data, seasonal_shift |
| Retrofit truth labels | improvement, no_change, delayed_effect, adverse_effect; labelled exercise direction/size, not actual works or causation |
| `truth/manifest.json` | Schema/method versions, synthetic label, Python version, generator source fingerprint, seed, UTC window/cadence, nominal slots, constructed-weather identity, all exercise parameters, case/row counts, relative `file_sha256` map |
| `truth/report.json` | Method/version/source, evaluated rules and analysis-only `input_sha256`; per-check list, confusion counters, sensitivity and explicit limits; no overall pass |
| `checks[]` | Neutral `case_id`, evaluator label, check name (`damp_outcome` or separate `retrofit_early`/`retrofit_late`), fixed expectation, observed analysis/comparison, `status=PASS`/`FAIL` |
| Analysis result | `status=NO_EXERCISE_SIGNAL`/`REVIEW_CANDIDATE`/`INSUFFICIENT`; expected/present/valid counts, coverage fraction, reasons, longest high/flatline hours, high-night count; nullable mean temperature C/RH percent |
| Retrofit comparison | Whole and baseline/early/late window analysis, `status=SUFFICIENT`/`INSUFFICIENT`, nullable early/late delta objects (`temperature_c`, `humidity_points`); descriptive-only interpretation |
| Confusion | Case-level total, eligible, binary_classified, abstained, expected_insufficient, correct/incorrect_insufficient and tp/tn/fp/fn; false-alert/miss rates use classified negative/positive denominators, null when zero |
| Sensitivity | Same fixed damp truth at RH thresholds 70/75/85; separate confusion objects, four retrofit cases excluded |

Fixed UTC window: [2024-01-01,2024-01-29), 672 hourly slots/case;
default seed 190, supported integer range 0..2^63-1. Eleven cases yield 6,888
emitted rows (one 75%-missing case), all synthetic. Weather is constructed
constant outdoor 2 C/70% RH. Completion is day 14; delayed activation day 21.
The comparator does not read truth or use seed/identity as labels. It checks
uniqueness/order/grid, fields/units/labels/calibration and finite domains;
>=90% valid coverage per whole/day/overnight and no >=24-hour paired flatline
are required. Gaps break high-RH runs. Threshold 75%, >=12 consecutive hours
or >=3 nights with >=3 high-RH samples are versioned exercise criteria only.
Baseline/early/late seven-day windows have independent sufficiency; null
deltas never become a reassuring negative. Truth separation is not OS access
control, and a negative exercise result does not establish a safe home.

These are simulated readings, not evidence of an installed device or any real
home condition. #111/#133 actual downstream tests, live publishing, competent
R2 review, agreed R3 limits, human approval and real resident consent remain
separate gates. No sensor result overrides a resident report or changes a
clock, hold, service, priority or investment decision.

### Real-person guarantee

The guarantee is bounded to constructed inputs and the executable pattern/label
contract, not a proof that arbitrary text cannot identify a person. The checker
rejects email, UK telephone, NI and UK-postcode patterns (case-insensitive where
applicable), missing/false required labels, malformed payloads, unknown snapshot
files and hash mismatches. It never prints matched values. It does not recognize
all names, addresses, international identifiers or contextual reidentification.
Real map anchors remain private and require human review before any disclosure.

Public operating CSV rows require `is_synthetic=true`, except the named
`evidence-gap-register.csv` metadata table. Public manifests require the root
Boolean label; labelled eval collections and declared inherited labels use the
contracts above. Generated sensor rows use `source_type=SYNTHETIC`; generated
chat rows require Boolean labels on all nine JSONL payloads. Scale homes/events
inherit only a valid hash-bound manifest. Only the scale home's exact fictional
postcode field has a narrow pattern exception, not other fields or datasets.
No generator payload/schema was changed to satisfy this check.

Run the [core commands](../../../../src/core/README.md#offline-provenance-and-privacy-audit-175)
and [chat regression](../../../../src/agents/README.md#generated-chat-provenance-175).
Public checks open no private stock, runtime database or tenant roster. Tests
check registry visibility, ignored working-data/answer-key paths and fresh
snapshots; this is not an attestation of existing private data or runtime chat.

### Issue 175 acceptance audit (2026-10-16)

| Criterion | Status | Evidence and limit |
| --- | --- | --- |
| Dictionary covers every dataset including sensor/chat | Met for known dataset families | Register covers public CSV/manifests/evals, private seed/geography, scale/fabric, sensor and generated/runtime chat. Core coverage test checks IDs/anchors and every public JSON/CSV payload |
| Every external source has licence, retrieval date and attribution | Unmet | Three historic source entries lack verified dates/terms; strict `--sources` audit rejects them. Offline work cannot invent or refresh that evidence |
| Automated check rejects real-person patterns or unlabelled records | Met for specified bounded contract | Production checker/CLI mutation tests cover four patterns, required labels, inherited/exempt content and independently rehashed fixtures; not universal PII certification |
| Private/public separation is tested | Met locally | Public-only inventory/scan, ignored-path checks and fresh scale/sensor/chat fixtures; no private corpus read or publish approval |

Issue remains open. Coordinator decides checkboxes at merge; no operational
legal interpretation, rule activation, safety, consent or financial approval
is inferred. ADR 0005 acceptance is synthetic-development-only.
