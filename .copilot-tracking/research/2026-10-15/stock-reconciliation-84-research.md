---
title: Stock reconciliation and technical sign-off research
description: Issue 84 evidence and implementation readiness
ms.date: 2026-10-15
---

## Brief and controls

Task: #84, stock-reconciliation-84. Audience: maintainers reviewing the
src-only feature. Output: convergence for implementation, not legal or
professional acceptance. Posture: focused, selected from the owner's bounded
scope. Trusted evidence root: `.copilot-tracking/research/2026-10-15/`.
All code and tests belong in src; no new mvp code, private data, deployment,
owner-decision invention, or changes to protected paths.

## Extensions and participation

Repository instructions, ADR 0006 and the parity matrix govern placement.
RPI research is selected for missing reconciliation evidence and sign-off
edge cases. Research is inline: one tightly coupled workflow trace does not
justify independent research workers. No external legal research is needed:
this change records human decisions, not statutory rules. Owner supplied
explicit full-loop and PR authorization; interaction is unavailable.

## Questions

* Q1: What acceptance criteria and exclusions are currently authoritative?
* Q2: Where do reconciliation, ranking and sign-off changes belong?
* Q3: How can conflict evidence remain visible without automatic authority,
  privacy leakage or collateral reapproval?

## Cycle 1

### Wider (opening)

* W1: https://github.com/jmservera/ama/issues/84, retrieved 2026-10-15:
  four criteria cover compared stock values/query owner, separate versioned
  sign-offs, affected-only reapproval and non-vulnerability-only ranking.
  The only current owner comment moves nomination/challenge to #130 and
  tenure/lease routing to #131. No later pivot comment was returned.
* C1: `docs/adrs/0006-src-layout-and-cutover.md:60`: all new code in src.
* C2: `src/README.md:27`: core has no workload imports; API may use agents
  until #144; no agent SQL/blob dependencies.
* C3: `src/core/src/zava_forward/core/signoffs.py:18`: existing separate
  sign-offs and affected-only design change logic are the reuse point.

### Deeper

* C4: `src/core/src/zava_forward/core/store.py:324`: detail copies the case,
  then applies contractor allowlists and staff note redaction. Reconciliation
  must be projected explicitly and limited to non-resident stock fields.
* C5: `src/core/src/zava_forward/core/sqlstore.py:113`: SQL stores inherit
  Store; existing optimistic persistence and JSON case bodies need no new SQL.
* C6: `src/api/src/zava_forward/api/server.py:625`: technical endpoint already
  dispatches human actions. Add reconciliation alongside it, not a new service.
* C7: `src/core/src/zava_forward/core/ranking.py:67`: ranking indexes missing
  support flags directly; waiting days, stage and safety are already separate
  ranking factors. Preserve policy order and record unknown coverage explicitly.
* C8: `src/core/tests/test_finance_signoffs.py:202`: JSON/SQL sign-off tests
  already prove affected-only invalidation, distinct roles and no self-approval.
* C9: `docs/prds/zava-forward-retrofit-programme-demonstrator.md:1`
  (FR-012/013, AC-015/016/040): source conflict must retain identifiers,
  dates, versions, validation, owner and unknown authority/eligibility.
* W2: merged PRs #296-#302, retrieved through `gh pr view` on 2026-10-15:
  move-not-copy completed, tests follow owning workloads, no new mvp code.

### Contrarian

* C10: `src/core/src/zava_forward/core/signoffs.py:108`: optional note is
  validated after setdefault. A malformed note must not create a sign-off.
* C11: `src/core/src/zava_forward/core/signoffs.py:76`: explicit empty affects
  currently defaults to all; validate a nonempty unique list and reject malformed
  types before any mutation. History needs authenticated identity/version,
  not client-supplied names or inferred agent approval.
* C12: `src/core/src/zava_forward/core/buildings.py:119` and
  `src/core/src/zava_forward/core/store.py:359`: existing building blockers and
  hazard holds must also gate technical approval. Do not copy their logic.
* C13: `src/core/src/zava_forward/core/projection.py:60` and
  `src/core/src/zava_forward/core/insights.py:54`: missing adjustment values
  can be mistaken for support or raise errors. Share tri-state support helpers
  across ranking, views, filtering and SQL-derived support.
* Alternative rejected: automatically selecting newest stock source or letting
  AI resolve a conflict. Neither has approved source authority; AC-040 requires
  the uncertainty to remain visible. Store owned unresolved comparisons only.
* Alternative rejected: duplicate sign-off engine or change ranking weights.
  Existing engine/policy already provide the essential controls.

## Findings and selected direction

Q1 is answered by W1/C9; Q2 by C1-C6/W2; Q3 by C7-C13.
Implement bounded, staff-recorded non-resident stock comparisons; both assertions
and named owner remain visible, authority/resolution/eligibility stay Unknown.
Unresolved conflicts hold technical progression without deleting or reprioritising
the home. No source-resolution or eligibility-rule decision is invented.
Retain named human sign-off roles, strengthen input atomicity and authenticated
history, reuse building/hazard checks. Record missing support flags as Unknown
without inferring vulnerability, preserve known-data policy ordering.
Existing AI remains available through governed proposal-only paths; real model
access, operational competence/delegation, Azure/SQL Server and direct human
acceptance are evidence gaps, not reasons to remove the feature's human gate.

## Decisions and readiness

Research disposition: executed, complete.
Planning Readiness: Ready for the bounded engineering slice above.
One wider/deeper/contrarian cycle covers the material questions; another cycle
would repeat the same contracts. No independent worker was used.
No operational delegation, live model evidence or professional approval is
claimed. Owner-dependent acceptance remains explicitly unticked.
