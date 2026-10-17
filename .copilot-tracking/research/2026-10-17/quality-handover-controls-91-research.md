---
title: Quality handover controls issue91 research
description: Ordered acceptance-control investigation
ms.date: 2026-10-17
---

## Research Brief

Audit issue91's exact three criteria across per-measure quality, defects,
handover, trusted API actors and transactional persistence. Existing stepwise
states and separation are hypotheses to verify, not gaps to assume.
Audience: implementation and independent review. Output mode: audit.
Scope: current src core/API, requirements, ADR0002, quality journeys and tests.
Non-goals: new risk policy, professional authority, payment execution, finance
feature expansion, private datasets, Azure or changes in other worktrees.

## Research Parameters and Extensions

Focused posture, selected for caller's bounded internal acceptance audit.
Research is read-only except canonical evidence/state. Evidence root:
`.copilot-tracking/`. No external legal research required.
Repository instructions and rpi-research selected; phase skills activate only
at their own transitions. Web skills deferred unless web changes become needed.
Inline investigation selected because this is one continuous authority and
transaction trace. Independent critique and review will use separate agents.
User participation unnecessary: exact criteria and automatic progression
explicitly supplied. Parent #89 is hierarchy, not a dependency; #90 is merged.

## Direction Controls

* Preserve stock #84, finance #94 and provider/scheduling #90 safeguards.
* Do not edit finance.py; shared dataset/API/UI/manifest overlap is declared,
  not assumed independent. No fixture change unless necessary.
* No real human/professional/SQL Azure acceptance may be inferred from seeds.
* Execute all phases even if existing criteria already hold.

## Questions and Prior Knowledge Gate

| ID | Question | Type | Status |
| --- | --- | --- | --- |
| Q1 | Do current trusted actors prevent contractor acceptance/closure/payment? | depth | Answered: HTTP denies, direct stale staff bypass |
| Q2 | Does defect closure require remediation and independent verification? | depth | Answered: blank remediation accepted |
| Q3 | Does evidence replacement invalidate dependent handover atomically? | depth | Answered: old handover remains active |

Clean caller-designated topic branch at b5d4c840 after #90/PR #384. No open PR
for this branch. Fresh issue91 retains all criteria unchecked. Original case,
addendum opening, KB index and owner memory read; further relevant slices follow.

## Research Cycle Log

### Cycle 1

#### Wider

Opening investigation: map requirements, quality journeys, component entry
points, current trusted actors and SQL transaction helpers.
Reflection: stepwise transitions already exist; contractor HTTP writes are
default-denied, including evidence submission. Staff record provider evidence.
Do not invent a provider portal or professional authority.

#### Deeper

Traced quality.py, server QUALITY_ACTIONS, projection, Store, SQL save and
existing stock/procurement/finance scopes. Executed temporary probes on tiny
fictional JSON and SQLite. Both stores allowed blank remediation, acceptance
using revoked inspector data, and replacement left states `Handed over`,
`Submitted` with the old handover intact. Existing 50 quality/procurement tests
pass, demonstrating missing assertions rather than a broken baseline.
Reflection: reuse the current registered-actor resolver and stock decision
scope/SQL validation instead of another transaction hook. Add quality-scoped
JSON preimage recovery and preserve legitimate SQL pending audit on failure.

#### Contrarian

Challenged the gap hypothesis against current helpers, actual HTTP deny policy,
finance's record-only implementation and current requirements. No payment
execution exists; no quality change should mutate finance. A contractor cannot
submit directly today; staff-assisted submission is the existing manual route.
Independent acceptance currently compares names/codes, not retained email/OID;
aliases or changing the latest fixer can defeat original-participant exclusion.
Reinspection "pass" delegates to acceptance without requiring FIXED. Record
indices accept negative values. Accepted records cannot currently be replaced
until handed over, then replacement fails to invalidate that handover.
Reflection: these are tightly coupled control gaps, not grounds for broader
quality risk policy or finance expansion. Always require independent
reverification for the existing returned/fixed path, without inventing risk
categories. Preserve original evidence/history and invalidate only same-measure
acceptance/handover. Make superseded records non-actionable.

#### Parent Synthesis and Disposition

| Material | Evidence | Disposition | Rationale |
| --- | --- | --- | --- |
| Existing stepwise states | C2 | Accepted | Preserve normal submission/return/fix/reinspection sequence |
| Current actor and remediation gaps | C2, C3, C6 | Accepted | Executed fail-before probes agree across JSON/SQLite |
| New direct contractor uploads | C3, C5 | Rejected | Existing boundary denies writes; not needed for exact issue |
| New risk/competence or payment system | C4, C5 | Rejected | Human-owned authority and explicitly out of scope |
| Separate replacement API | C2 | Rejected | Existing submission can version same-measure evidence |

#### Cycle Re-entry Evaluation

No further cycle needed: bounded call paths and counterevidence covered.
Research disposition: executed. Planning Readiness: Ready. No research blocker.

## Evidence Log

| ID | Claim | Location | Confidence |
| --- | --- | --- | --- |
| C1 | Provider work merged at supplied base; clean topic, no open branch PR | Git b5d4c840, fresh gh issue91 and PR-list output | High |
| C2 | Fixed transitions but no remediation requirement; name/code-only independence and surviving prior handover | src/core/src/zava_forward/core/quality.py:44-186 | High |
| C3 | HTTP quality actions use authenticated actor; contractors default-denied all domain writes | src/api/src/zava_forward/api/server.py:132-140,736-739,849-850; src/core/src/zava_forward/core/projection.py:33-68 | High |
| C4 | Separate named quality/finance/resident controls; retained replacement learning | docs/prds/zava-forward-retrofit-programme-demonstrator.md:852,1466,1488; docs/brds/agentic-retrofit-programme-brd.md:1465; docs/adrs/0002-pilot-readiness-architecture.md (retained #24/#27 quality replacement row) | High |
| C5 | Supplier submission is not acceptance; independent remediation and resident handover retain separate owners | docs/reference/research/ux/customer-journeys/programme.md:101-104; docs/reference/research/ux/customer-journeys/suppliers.md:45-69; src/core/src/zava_forward/core/finance.py:1-7 | High |
| C6 | Reusable current actor and transactional decision scope; SQL optimistic versions and quarantine-before-recovery | src/core/src/zava_forward/core/change_provenance.py:15-45; src/core/src/zava_forward/core/stock.py:16-59; src/core/src/zava_forward/core/sqlstore.py:540-658 | High |
| C7 | Existing UI already sends fix/inspection notes and renders unknown state fallback; no replacement version or invalidation text | src/api/src/zava_forward/api/web/ops.js:20-78 | High |

## Fail-before Execution

2026-10-17, worktree-local Python 3.12 venv after missing-package probe;
editable core/API/agents plus declared dev/SQL extras, pip only.
Temporary script output for BOTH Store and SqlStore:
`blank_remediation Fixed, awaiting reinspection`;
`revoked_actor Accepted`;
`replacement_states ['Handed over', 'Submitted'] old_handover True`.
No source edits in Research. Existing baseline:
`PYTHONPATH=src/core/tests .venv/bin/python -m unittest test_quality_procurement -q`
ran 50 tests, all passed.

## Decisions, Risks and Readiness

Research disposition: executed. Planning Readiness: Ready.
Task is not already satisfied. Plan scoped quality fixes, existing helper reuse,
meaningful core/API failure tests, isolated local SQL Server parity and a minimal
quality-panel clarification if supersession changes visible state.
BRD FR-017 now means handoff information, unlike PRD FR-017; preserve the exact
issue wording without pretending their current numbering matches.
No fixture/manifest change needed. Shared edit candidates are sqlstore.py,
server.py only if essential, and isolated ops.js rather than app.js.
All fixture roles demonstrate mechanics, not professional competence or approval.
No external sources used.
