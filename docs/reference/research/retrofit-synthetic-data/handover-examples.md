---
title: Example Operational Handovers
description: Handovers between delivery roles, reconstructed from five synthetic records in the Proper Warm year-one evidence pack
ms.date: 2026-09-30
ms.topic: reference
---

> [!WARNING]
> SYNTHETIC DATA. These are fictional cases from the synthetic evidence pack.
> They show how handovers appear in the records. They are not findings.

Each example follows one home across the tables it touches, so readers can
see what a handover looks like in the evidence and which record holds each
step. The examples describe the records without interpreting them; drawing
conclusions is part of the discovery analysis.

## 1. Assessor to Design Consultancy to Retrofit Coordination

Case `CAND-2025-0012`, a Wave 1 shared-ownership home.

| Date | Record | What was handed over |
| --- | --- | --- |
| 2025-07-14 to 2025-09-26 | `lifecycle-events.csv` | Lease review with Legal before contact |
| 2025-10-27 | `ASSESSMENT_COMPLETED` | Assessment report issued to the shared design mailbox |
| 2025-10-28 | `HANDOFF_ACCEPTED` | Design consultancy acknowledged receipt |
| 2025-11-10 | `DESIGN_SUBMITTED` `D-v1` | Design sent to the coordinators |
| 2025-11-26 | `DESIGN_RETURNED` | Occupancy assessment out of date |
| 2025-12-05 | `DESIGN_SUBMITTED` `D-v2` | Revised design |
| 2026-02-09 | `DESIGN_RETURNED` | U-value calculation inconsistent |
| 2026-02-18 | `DESIGN_SUBMITTED` `D-v3` | Revised design |
| 2026-05-06 | `DESIGN_APPROVED` `D-v3` | Coordinator sign-off |
| 2026-09-24 | `ACCEPTED_HANDOVER` | Closed after installation, QA, evidence and resident handover |

Throughout the design period the tracker showed a single status. Record
questions for the analysis: how long did each version wait before review, and
who held the work in each gap?

## 2. Building Safety to Programme

Case `CAND-2025-0024`, a heat pump home. The hold register row
`HLD-0004` carries no candidate ID and is matched through the legacy
reference `HB/11691`.

| Date | Record | What was handed over |
| --- | --- | --- |
| 2025-08-12 | `safety-holds.csv` | Damp and mould observed at survey and referred the same day |
| 2025-08-14 | `SAFETY_HOLD_PLACED` | Retrofit hold placed in the tracker |
| 2025-09-03 | `safety-holds.csv` | Repairs service investigation |
| 2025-10-03 | `safety-holds.csv` | Repair completed in the repairs system |
| 2025-10-22 | `SAFETY_HOLD_RELEASED` | Hold released in the tracker, citing job `RJ-700025` |
| 2025-10-22 | `WORK_ORDER_ISSUED` | Work released to the heat pump installer |

Record questions: what evidence did the release rely on, and how did the
programme learn that the repair was complete?

## 3. Supplier to Grants and Evidence

Case `CAND-2025-0052`, an external wall insulation home whose loft measure
was removed pending roof renewal.

| Date | Record | What was handed over |
| --- | --- | --- |
| 2026-05-06 | `INSTALL_COMPLETE` | Supplier claims practical completion |
| 2026-05-07 | `QA_PASSED` | Physical inspection passed |
| 2026-06-02 | `quality-evidence.csv` | Evidence pack `EP-v1` submitted |
| 2026-06-03 | Evidence review | Rejected: ventilation commissioning sheet missing |
| 2026-07-02 | Evidence submission | `EP-v2` submitted |
| 2026-07-15 | Evidence review | Rejected: missing pre-installation photographs |
| 2026-08-03 | Evidence submission | `EP-v3` submitted |
| 2026-08-04 | `EVIDENCE_ACCEPTED` | Documentary acceptance |
| 2026-08-27 | `ACCEPTED_HANDOVER` | Case closed |

The resident handover event is missing from the event log extract for this
case. Record questions: what happened between physical acceptance and
documentary acceptance, and when could the grant be claimed?

## 4. Supplier to Resident Liaison

Case `CAND-2025-0090`. The household record shows the constraint "Not
available weekdays 08:00-17:00" and a preference for letters.

| Date | Record | What was handed over |
| --- | --- | --- |
| 2026-01-14 | `WORK_ORDER_ISSUED` | Heating works released to SUP-HT |
| 2026-01-23 | `appointments.csv` | PM visit, outcome `NA`, "Nobody home at 13:30" |
| 2026-03-13 | `appointments.csv` | PM visit, outcome `REF`, "Nobody home at 13:30" |
| 2026-03-13 | `CASE_EXITED` | Withdrawn: resident refused access, job returned by contractor |

Record questions: does the appointment note support the outcome code, and
what did the resident liaison officer know about access before the
visits?

## 5. Programme to Block Delivery

Case `CAND-2025-0218`, a flat in block `SYN-BLDG-00131`.

| Date | Record | What was handed over |
| --- | --- | --- |
| 2025-09-17 | `CONTACT_PAUSED` | No contact after six attempts |
| 2025-12-08 | `ASSESSMENT_COMPLETED` | Assessment completed after contact resumed |
| 2026-01-14 | `DESIGN_SUBMITTED` | Design sent to the coordinators |
| 2026-02-20 | `BLOCK_PROCEEDED_WITHOUT` | Block released to the external wall insulation supplier without this flat |

The tracker now shows `On hold` with the note "Waiting rest of block".
Record questions: what was this flat waiting for when the block was released,
and what route does it now have to installation?

## Using These Examples

Use the examples to agree event boundaries and handoff ownership with the
role owners before analysing the full population. The discovery brief
requires a sending team, a receiving team, a sent date, an acceptance date
where one exists, and an owner for the next action at each handoff. Check
which of these the records hold and which must be inferred or remain unknown.
