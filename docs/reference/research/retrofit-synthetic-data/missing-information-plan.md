---
title: Missing Information Plan for Synthetic Retrofit Evidence
description: What the Zava Forward year-one synthetic pack now represents, what it deliberately leaves out, and the next iterations
ms.date: 2026-09-30
ms.topic: reference
---

> [!WARNING]
> SYNTHETIC DATA. This plan describes a fictional evidence model for design
> practice. It does not describe Zava North Homes' systems or records.

## Purpose

The first version of this pack held ten homes with one status each. It could
illustrate record types but could not show where time goes. Version 2.0.0
models fifteen months of operating records for 980 candidate homes. The
records come from the sources a real team would hold, with the gaps and
imperfections those sources typically have.

The central assumption is unchanged. The programme does not fail because the
team has no data. It struggles because data sits in separate systems, current
values overwrite history, handoffs are not acknowledged, and ownership of
waiting time is not visible.

## What the Pack Now Represents

| Domain | Where it is | Deliberate limitation |
| --- | --- | --- |
| Property identity | `property-register.csv` | Merger duplicates, legacy references and missing UPRNs |
| Candidate selection | `candidate-lifecycle.csv`, `RESEQUENCED` events | Rule change in January 2026 |
| Lifecycle history | `lifecycle-events.csv` | First-pass assembly; some events missing, duplicated or mis-dated |
| Current status and ownership | `candidate-lifecycle.csv` | Overwritten cells, month-end bulk updates, stale next actions |
| Resident journey | `resident-journey.csv`, `resident-contacts.csv` | Access constraints and adjustments under-recorded |
| Appointments | `appointments.csv` | Supplier outcome codes as recorded, not as verified |
| Safety holds | `safety-holds.csv` | Repairs and tracker dates held separately; some rows lack candidate ID |
| Design versions and returns | `lifecycle-events.csv` | Coordinator review throughput not tracked |
| Supplier capacity | `contractor-capacity.csv` | Supplier returns only; no subcontractor detail |
| Quality and evidence | `quality-evidence.csv` | Evidence rejection reasons as free categories |
| Finance and grant | `grant-and-finance.csv` | Formatting variants; no cost variations |
| Management reporting | `programme-board-snapshots.csv` | Reports practical completion as completion |
| Returns and escalations | `edge-case-returns.csv` | Only issues someone chose to log |

## Still Missing by Design

These gaps are realistic for a team one year in, and they are useful tests
of whether an analysis states its limits:

* Coordinator review throughput and queue, because internal roles have a
  leave planner only
* Leaseholder consultation completion dates
* Referral acceptance and first-action dates for most handoffs
* Staff and supplier effort per task
* Contract variations and change orders
* Post-retrofit EPC lodgement, energy use, comfort and affordability
* Complaints and satisfaction
* Subcontractor allocation

The [evidence gap register](./evidence-gap-register.csv) records the status
of each domain.

## Critical Control Points

The pack keeps these controls visible as separate events:

* Candidate selection and resequencing
* Resident contact, access and measure-specific works decision
* Safety hold placed, repair completed and hold released
* Design submission, return and competent-role approval
* Funding confirmation and budget holds
* Work order release
* Installation, physical acceptance, documentary acceptance, resident
  handover and accepted handover
* Aftercare reopening

## Recommended Next Iterations

1. Run a blind discovery analysis over the pack, following the
   [discovery brief](../../../brds/retrofit-flow-discovery-brief.md), and
   record the ranked constraint register before consulting the answer key.
2. Ask the role agents to validate event boundaries and delay attribution
   for their own domains, keeping disputed causes visible.
3. Compare the team's delay-code view with the time attribution rebuilt from
   events.
4. Use the gaps above to specify the minimum instrumentation for a Phase 0
   baseline.
5. Only then use the pack to test workflow, deterministic rules and bounded
   agent concepts, including in shadow mode.
