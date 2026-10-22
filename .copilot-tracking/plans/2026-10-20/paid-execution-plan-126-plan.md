---
title: Paid execution plan 126 plan
description: Documentation-only preparation of a finite costed execution plan for owner approval
ms.date: 2026-10-20
---

Task ID: 126-paid-plan. Slug: paid-execution-plan-126. Branch: docs/paid-execution-plan-126.
Status: planned; no paid execution, allocation, deployment or inference is in scope.

Research: .copilot-tracking/research/2026-10-20/paid-execution-plan-126-research.md.
Details: .copilot-tracking/details/2026-10-20/paid-execution-plan-126-phase-details.md.

## Scope and Write Boundary

Edit only the existing dated Case Study 48 addendum (a new subsection after the 2026-10-13
carry-forward subsection), the knowledge-base index row and the append-only log, plus this
task's RPI artifacts. Not edited: infra/README.md, form schema packs, map documents, cohort
pack, other issues' domain documents. No new standalone page.

<!-- rpi:phase id=P01 -->
### P01: Cost baseline, headroom and options

* [ ] P01-T01: Record E1-E8 evidence (provenance, date, currency, limits, unknowns) without IDs.
* [ ] P01-T02: Derive month-end projection, headroom and idle-burn options S0/S1/S2; state that
  S0 is blocked.

<!-- rpi:phase id=P02 -->
### P02: Bounded tranches and approval fields

* [ ] P02-T01: Define T0 (idle-burn reduction) as an approval prerequisite and T1-T4 with
  per-resource counts/SKU/region/lifetime, finite calls/tokens/model versions, ceilings,
  local-first versus Azure-only need, stop thresholds, expiry, cleanup and recreation.
* [ ] P02-T02: State T1 first-deployment tranche: approval fields, existing commands/scripts,
  preconditions, expected browser/roles/SQL/AI checks, blockers, what the owner may test now.

<!-- rpi:phase id=P03 -->
### P03: Integration and gate

* [ ] P03-T01: Update index row, append log entry, ms.date; run Markdown/link and focused tests.
* [ ] P03-T02: Commit with dated original RPI evidence; run the complete local gate; verify receipt.

## Gates

* Exactly one final-candidate critique (before P01 edits) and one Review (after P02).
* Every claim traceable to E1-E8 or an existing repository section; proposals labelled as such.
* No whole-issue acceptance, closing keyword, approval inference or operational release.
