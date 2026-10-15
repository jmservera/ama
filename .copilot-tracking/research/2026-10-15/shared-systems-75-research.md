---
title: Building shared systems research for issue 75
ms.date: 2026-10-15
---

## Research Brief

Task identity: `75`, slug `shared-systems-75`. Focused convergence research
for implementation of the three issue acceptance criteria. Audience: implementer
and PR reviewer. Trusted evidence root: `.copilot-tracking/research/2026-10-15/`.

## Direction Controls and Extensions

The owner explicitly requests the complete RPI loop and publication to a topic
PR. Work only in the specified worktree and branch. ADR 0006 and repository
instructions apply. No new code in mvp, private data, environment-file access,
deployment, new approval authority or financial allocation policy. Existing AI
remains enabled through its human-gated proposal paths; no new model authority.
Research is inline because these uncertainties form one coupled source trace.
Domain specialists and external research are unnecessary for a bounded model
change, not a legal interpretation. Interaction is unavailable and scope is clear.

## Questions and Candidate Areas

1. Where do the building model and its views belong?
2. Which persistence, authorization and approval patterns can be reused?
3. Can shared identity accidentally imply shared approval or duplicate costs?

## Research Cycle Log

Cycle 1, Wider: verified issue body and owner pivot comment, merged moves
296 through 302, accepted ADR, parity matrix, source README and knowledge index.
The BRD FR-002 is hazard continuity, not the building requirement: retain this
source-reference discrepancy rather than silently reinterpret it. PRD FR-002
and issue criteria are the implementation boundary.

Cycle 1, Deeper: traced Store detail/advance, role projection, procurement
instructions and checked SQL documents. Building records can be seeded and
persisted using the existing checked-document interface, avoiding a new dialect
or workload dependency. Read-only building context needs a staff-only endpoint
and linked home navigation. Costs must be explicit GBP amounts, not inferred
allocation, and restricted to the existing Finance-view roles.

Cycle 1, Contrarian: shared IDs cannot establish work applicability. Each shared
work, dependency and hold must name affected case IDs explicitly; unknown scope
blocks linked-home progression rather than claiming every home is applicable.
No building approval/release mutation is introduced. Imported shared records
cannot contain resident evidence or home decisions. Empty data is labelled
unknown, not "no holds". Home costs are not summed into building costs.

## Evidence Log

* C1: `docs/adrs/0006-src-layout-and-cutover.md:64`: all new code in src;
  shared domain belongs to core and HTTP/web to api.
* C2: `src/README.md:26`: namespace projects and dependency constraints.
* C3: `src/core/src/zava_forward/core/store.py:43`: existing Store mixins,
  per-home cases and gates.
* C4: `src/core/src/zava_forward/core/sqlstore.py:116`: SqlStore inherits Store,
  SQL-backed meta and case synchronization.
* W1: https://github.com/jmservera/ama/issues/75 retrieved 2026-10-15:
  building shared systems/dependencies/holds/works/costs; home evidence and
  allocation stay home; test no inherited approval.
* C5: `src/core/src/zava_forward/core/sqlstore.py:423`: DOCS checked documents
  seed, synchronize and persist atomically, inherited by MssqlStore.
* C6: `src/core/src/zava_forward/core/projection.py:30`: staff and Finance
  allow-lists; contractors must not see shared context or sibling records.
* C7: `src/core/src/zava_forward/core/store.py:352`: advance enforces home
  gates; procurement work-order issue also needs applicable shared holds.
* C8: `docs/prds/zava-forward-retrofit-programme-demonstrator.md:251`:
  FR-002 separates shared context and per-home approvals; AC-001/002/003
  require navigation and explicit scope independence (located by named IDs).

## Alternatives and Decision State

Selected: typed core building validation/views and scoped blockers, imported
read-only records, existing checked-document persistence, staff-only API and
read-only web view. Rejected: shared approval objects, automatic allocation,
building-wide implicit work applicability and a new management workflow.
No new AI task is justified: retain existing gated AI on the home, and do not
feed shared free text or financial evidence into model prompts.

Remaining evidence limits: no real building register, live SQL Server, real
inference, Azure deployment or human UX acceptance can be claimed from local
tests. Preserve them as separate release evidence, not fictional approvals.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready for this bounded
model/view slice. One complete focused cycle answered all three questions;
further regulatory research would not change this non-operational model.
Parent: explicit full-loop RPI orchestration; continue to Plan.
