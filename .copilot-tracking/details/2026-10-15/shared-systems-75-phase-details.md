---
title: Building shared systems phase details
ms.date: 2026-10-15
---

Task: 75 / shared-systems-75. Research C1 to C8 and W1 govern this plan.

## P01

### P01-T01

Add core buildings module with an explicit schema, positive version, stable
IDs, required provenance, explicit per-record applicability and exact money
representation. Keep per-home records untouched when reading building data.
Applicability consists of case_ids and package_ids on holds, dependencies and
works. null means unknown; [] means explicitly none; otherwise exact IDs only.
Case references must exist and belong to the building; package references must
exist in procurement. No free-text scope matching. All-scope home readiness
considers every applicable unresolved blocker; a package instruction considers
only that package, with unknown package scope conservatively blocking affected
cases. Changing a work-order's free-text description cannot change applicability.
Reissue checks the same explicit package ID. Test same-home different-package
instructions and reissue. No inferred connection between building works/packages.
Seed `buildings` through SqlStore.DOCS so JSON, SQLite and inherited MSSQL use
the same body without new DDL. Unknown linked building or scope fails closed.
Use building blocker checks in detail, advance, issue/reissue instruction.
Do not add release or approval endpoints; do not stop hazard response.
Legacy live JSON/populated SQL stores are not reseeded: missing building context
for an explicitly linked home is unknown, never a clear gate. Unlinked legacy
homes retain existing behavior.

### P01-T02

Add GET building endpoint under existing role authorization and a read-only
building screen with links from/to cases. Display all categories including
unknown/empty states. Do not expose sibling resident fields, home evidence,
approval objects or individual home allocations in building view.
Shared building costs and home cost_allocation are visible only to existing
Finance-view roles. Retain existing AI as proposal-only.
Non-Finance serialized responses omit costs/amounts and UI says restricted.

## P02

### P02-T01

Two-home synthetic fixture in the same building, separate consent, technical,
funding, quality and closure state, plus a shared work with explicit affected
cases. Prove no copied approvals, unknown scope blocks, unaffected sibling
stays independent, home allocation is not included in shared cost totals,
read isolation and restart persistence. Both JSON and SQLite fresh/reopen
checks are mandatory, including pre-existing populated stores without buildings.
Assert resident, funding and technical gates separately when building is clear;
quality, closure and evidence remain distinct and unchanged by building reads.
Blocked advance/issue/reissue leaves both homes and work-order versions intact;
contact/hazard intake remains available while building work is held.
API endpoint tests cover staff/Finance/contractor/unknown and missing records.
Run local application with this synthetic fixture. Validate source suites and
the normal project tooling; pip only if dependencies are missing.

### P02-T02

Update core/API READMEs, reference index and append-only log. Record all command
results in changes and prepare the one Review handoff. After Review, perform
administrative publication: commit with authenticated privacy-safe identity and
required coauthor trailer, push only the topic and create main PR using Refs.
Acceptance checkboxes require evidence; unsupported live/human criteria stay
unticked. No merge or deployment is authorized.

P01/P02 completion: typed core model, scoped blockers, both local persistence
backends, staff API/UI and Finance projection are implemented. Final evidence:
core 270, api 462 (92 skipped), agents 70, orchestrator 17 and importer 39;
all project lint/format/mypy passed. Migration 25 passed; browser home/building/
sibling navigation and cost separation passed after synthetic fixture repair.
Docker denied. Changes record contains commands, corrections and limitations.
