---
title: Resident decisions research for issue 86
description: Focused evidence and readiness for resident-owned decisions in src
ms.date: 2026-10-15
---

## Research Brief

Implement issue #86 in the existing migrated core and API, not in mvp.
Audience: implementers and PR reviewers. Output mode: convergence, preparing
planning. Posture: focused, selected for a bounded issue with named sources.
No new legal interpretation, deployment, private data or inferred consent.

## Research Parameters and Direction Controls

Task identity: issue-86 / resident-decisions-86. Branch:
feat/src-resident-decisions-86. Evidence root: .copilot-tracking/research/.
The user explicitly requests the full automatic RPI loop, commit, push and PR.
No interaction is available; owner-dependent criteria remain open.

## Extension Registry and Participation

Repository instructions and ADR 0006 apply. RPI phase skills are selected.
Company-role research and external regulatory research are skipped: this task
implements an existing exercise contract, not new company or legal policy.
Research is inline because this is one tightly coupled workflow trace.

## Questions and Candidate Areas

* Q1: What is already delivered, and where does it belong after the pivot?
* Q2: How are representative authority, dependent readiness and disclosure enforced?
* Q3: Which independent review/complaint and live evidence criteria remain unproven?

Starting areas: resident_decisions, store, sqlstore, workflows, API routes and
role tests; issue #86, PRD and BRD requirements. External sources: GitHub issue
and merged move metadata only.

## Research Cycle Log

Cycle 1 opening: wider inventory establishes existing controls and source
placement; deeper traces all read/write/release paths; contrarian tests legacy
consent, expired authority, sibling scope and agent proposal bypasses.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/86 retrieved 2026-10-15.
  Four acceptance criteria; representative task/source/scope/review evidence
  missing. GitHub returns no comments, including no post-pivot comment updates.
* W2: https://github.com/jmservera/ama/pull/296 through
  https://github.com/jmservera/ama/pull/302 retrieved 2026-10-15, all merged.
  M1-M6 and R1 have already moved/rebuilt the code; reuse it.
* C1: docs/adrs/0006-src-layout-and-cutover.md:12, Accepted; :198
  maps resident_decisions/workflows/stores to core and server to api.
* C2: docs/architecture/mvp-to-src-parity-matrix.md:199 maps
  resident_decisions to core; :297 keeps server-driven workflow tests in api.
* C3: src/core/src/zava_forward/core/resident_decisions.py:25-60:
  per-measure versioned status defaults to Not recorded; representative_ref
  alone currently suffices; scope/design and authority validation are absent.

## Findings, Alternatives and Decision State

Wider wave completed: merged placement and all four issue criteria verified.
Deeper wave completed: legacy case-wide acceptance gates installation while
per-measure answers do not; draft() addresses a representative without checking
authority. Procurement release paths also need the same resident guard.
Contrarian wave completed: contact history must not create consent, legacy
acceptance cannot attest an exact scope/design, interpreter-only permission is
not consent authority, and a complaint cannot remove or create a works hold.
Several representatives and changed safe-contact references must invalidate only
their own authority. Existing AI source allow-lists omit representative fields.

* C4: src/core/src/zava_forward/core/store.py:141-152, :351-361, :382-386:
  legacy aggregate decision/release and unvalidated representative addressing.
* C5: src/core/src/zava_forward/core/procurement.py:137-232: issue/reissue,
  booking, completion and correction paths require safety but not resident checks.
* C6: src/core/src/zava_forward/core/projection.py:110-120: role projection
  currently does not withhold representative authority records.
* C7: src/core/src/zava_forward/core/signoffs.py:72-95: design versions are
  existing technical context; changed designs must not inherit resident consent.
* C8: docs/prds/zava-forward-retrofit-programme-demonstrator.md:880-881,
  :1501-1502, :1510: exact scope/design/source and representative boundaries.
* C9: src/core/src/zava_forward/core/sqlstore.py:334: existing transactional
  dependent-case guard can revalidate resident release without new SQL dialects.

Select explicit per-measure scope registration and supplied human decisions,
versioned representative authorities, a guarded disclosure-check action that
sends nothing, and a named independent-review service route. Reuse JSON case
bodies and the transactional dependency guard. Reject inferred scope/design,
backfilling legacy consent, parallel schema, automatic reapproval, AI consent
tools and fictional formal complaints contacts.

Legacy case-wide answers remain historical only; booking must require current
per-measure acceptance. Existing tests that need install readiness will acquire
explicit constructed decision fixtures, not production backfill.

Open evidence: approved representative retention/role policy, real resident
accessibility/independence/without-detriment validation, formal complaint service
integration, permitted real inference and Azure SQL execution. These do not block
the bounded synthetic implementation; they block full issue/product acceptance.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready for the bounded
synthetic implementation with the above acceptance limits retained.
No additional cycle: focused questions answered; remaining gaps need owner or
live-service evidence, not more source discovery. Parent may continue to Plan.
Self-check: all three waves recorded, C/W evidence mapped, constraints preserved.
