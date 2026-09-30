---
title: Retrofit Synthetic Evidence Pack - Proper Warm Year One
description: Fifteen months of synthetic operating records from a professional retrofit delivery team that knows it has bottlenecks but not where they are
ms.date: 2026-09-30
ms.topic: reference
---

> [!WARNING]
> SYNTHETIC DATA. Every record in this folder is fictional and was generated
> for design, analysis and agent-testing practice. Nothing here is a Proper
> North Homes fact, and no person, address, supplier or organisation is real.
> Every table carries `is_synthetic=true`.

## Purpose

This pack gives the Proper Warm discovery a realistic body of operating
records to analyse. It models a competent, busy retrofit team one year into
delivery. The team knows the programme is behind plan and suspects several
bottlenecks, but its own reports cannot show where the time goes.

The pack supports the
[Retrofit Flow and Constraint Discovery Brief](../../../brds/retrofit-flow-discovery-brief.md):
reconstruct each home's path from candidate to accepted handover, separate
active work from waiting, find unaccepted handoffs and return loops, and test
candidate constraints against evidence. It also provides test data for later
agent and workflow concepts. Redesigning the process is a later step.

The pack was generated so that analysis can be blind. The generator, its
parameters and an answer key are held outside the knowledge base by the
project owner. Record your findings before consulting them.

## Scenario

### The Programme

* Proper Warm mobilised in July 2025 to move homes towards EPC C. It
  identified 980 candidate homes in four waves (July 2025, October 2025,
  January 2026 and April 2026), plus ad hoc additions.
* Candidates identified from 2025-07-01 to 2026-06-30 form the twelve-month
  baseline population. Homes added from July to September 2026 are included
  but fall outside the baseline.
* The year-one plan was 600 completions by September 2026. The extract date
  is 2026-09-30.
* Most homes are funded through a Warm Homes: Social Housing Fund Wave 3
  route, with internal capital where a home is not grant eligible. The award,
  grant rates and claim cycle are synthetic assumptions, not company facts.
* The candidate homes sit in three fictional localities: an urban core with
  1960s and 1970s low-rise blocks, former coalfield towns with terraces and
  semis, and a rural and coastal area with off-gas bungalows.

### The Team

| Code | Role |
| --- | --- |
| `PM-01` | Retrofit Programme Manager |
| `PS-01` | Programme Support Officer, maintains the tracker |
| `RC-01`, `RC-02` | In-house retrofit coordinators (PAS 2035 design review and sign-off) |
| `RC-03` | Framework retrofit coordinator, part time from April 2026 |
| `RLO-01` to `RLO-03` | Resident liaison officers, one per locality; `RLO-03` left in May 2026 |
| `GEO-01` | Grants and Evidence Officer, 0.8 FTE |
| `QA-01` | Quality inspector |
| `BSL-01` | Building safety liaison with the repairs and hazard service |
| `SUP-RA` | Retrofit assessment framework |
| `DES-1` | Retrofit design consultancy |
| `SUP-F1`, `SUP-F2`, `SUP-HP`, `SUP-HT` | Suppliers for fabric measures, external wall insulation, heat pumps and heating |

### How the Team Works

These practices are the team's normal, reasonable ways of working. They are
listed because they shape the records.

* The programme tracker is a SharePoint spreadsheet with one row per home.
  Each row holds the current status, owner, RAG, delay code, notes and
  milestone dates. Changing a status overwrites the previous value.
* The delay-code list was revised on 2 February 2026 from six broad codes to
  fourteen specific codes. Rows not touched since then keep the old code.
* The group formed from the merger of two heritage associations, so many
  homes carry a legacy reference as well as the group property ID. The
  repairs system and some suppliers still use legacy references.
* Assessment reports reach the design consultancy through a shared mailbox.
  Designs go back to the coordinators by email.
* Suppliers report appointments and completions through their own portals.
  Exports use UK `dd/mm/yyyy` dates.
* Damp, mould and other hazards found during retrofit visits are referred to
  the separate repairs and hazard service, and a retrofit hold is placed in
  the tracker.
* Programme Support catches up on tracker updates before the monthly
  programme board, and closed cases are swept at the end of each month.
* Grant claims are prepared quarterly.

### What the Team Sees

The programme board report for September 2026 shows 466 completions against
a plan of 600, with GBP 0.83 million of grant claimed. Delay codes on open
cases point most often at contractors, then residents. Earlier in the year
many homes sat "in design" for months. Staff believe the causes are supplier
capacity, residents not engaging and a slow design consultancy. Nobody has
yet joined the records together to test that belief.

## Files

| File | Source it imitates | Grain | Rows |
| --- | --- | --- | --- |
| [property-register.csv](./property-register.csv) | Asset management system extract | One row per property record, including merger duplicates | 996 |
| [candidate-lifecycle.csv](./candidate-lifecycle.csv) | Programme tracker (current state only) | One row per candidate, including duplicate rows | 992 |
| [lifecycle-events.csv](./lifecycle-events.csv) | First-pass event log assembled from tracker history, mailboxes and system extracts | One row per stage event | 9,859 |
| [resident-journey.csv](./resident-journey.csv) | Housing management and CRM household view | One row per candidate household | 980 |
| [resident-contacts.csv](./resident-contacts.csv) | CRM contact log | One row per contact | 5,905 |
| [appointments.csv](./appointments.csv) | Assessor and supplier portal exports | One row per booked visit | 1,530 |
| [safety-holds.csv](./safety-holds.csv) | Hazard referral register joined to the repairs system | One row per retrofit-channel hazard | 97 |
| [quality-evidence.csv](./quality-evidence.csv) | QA inspection log and evidence tracker | One row per inspection, submission or review | 1,381 |
| [grant-and-finance.csv](./grant-and-finance.csv) | Finance and grant tracker | One row per candidate, plus a duplicate line | 981 |
| [contractor-capacity.csv](./contractor-capacity.csv) | Supplier KPI returns and the internal leave planner | One row per resource per month | 135 |
| [programme-board-snapshots.csv](./programme-board-snapshots.csv) | Monthly programme board report | One row per month, section and item | 480 |
| [edge-case-returns.csv](./edge-case-returns.csv) | Team issues and escalations log | One row per logged issue | 172 |
| [delay-code-dictionary.csv](./delay-code-dictionary.csv) | Delay-code lists v1 and v2 | One row per code | 20 |
| [data-dictionary.md](./data-dictionary.md) | Field definitions, keys and allowed values | | |
| [manifest.json](./manifest.json) | Seed, dates and row counts | | |
| [handover-examples.md](./handover-examples.md) | Example handovers taken from the records | | |
| [missing-information-plan.md](./missing-information-plan.md) | Evidence still missing and next iterations | | |
| [evidence-gap-register.csv](./evidence-gap-register.csv) | Evidence domains and their coverage in this pack | | |

`candidate_id` links the tracker, events, contacts, appointments, quality,
finance and issues tables. Some source rows carry only a property reference,
and that reference may be the group ID, a legacy reference or a mistyped
value. Matching them to candidates is part of the analysis.

## Working With the Records

Expect the imperfections of real operational data from a professional team.
They include mixed date formats, legacy and mistyped references, duplicate
records from the merger, events missing from source extracts, statuses not
yet updated and milestones not entered. They also include free-text dates,
currency formatting and delay codes from two dictionary versions. Report
these issues rather than silently correcting or discarding them. Keep unknown
or disputed causes visible.

Suggested discovery questions:

1. Where did each home spend its calendar time, and how much of it was
   waiting rather than work?
2. Who owned each waiting period, and which handoffs were never acknowledged?
3. Did the constraint stay in one place over the year or move?
4. How do the team's delay codes compare with the time attribution rebuilt
   from events?
5. How far apart are practical completion, documentary acceptance, resident
   handover and accepted handover, and why?
6. Were suppliers short of capacity or short of ready work?
7. Do access failures, refusals and withdrawals fall evenly across
   households?
8. Which delays could have been predicted from data held before the survey?
9. Are any safety holds still open after the underlying repair was completed?

## Limits

* The scenario is one synthetic realisation. Its rates, durations and
  constraints do not describe Proper North Homes or the sector.
* Costs, grant amounts, supplier contracts and staffing are illustrative.
* Energy outcomes, bills, comfort, complaints and resident satisfaction are
  not modelled.
* Regulatory timing appears only as dates for context. Any statutory
  interpretation needs the sources in the
  [Regulatory Source Register](../../regulatory/README.md) and human legal or
  compliance review.
