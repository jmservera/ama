---
title: Hazard referral phase details
description: Marker-addressed implementation and validation contract for issue 85
ms.date: 2026-10-15
---

Task 85, src-hazard-referral-85. Uses research C1-C7 and W1-W2.
Execution state: P01-T01, P02-T01, P03-T01 and P03-T02 complete, with command/results
in the canonical changes record. Single Review Complete / Not accepted: RV-001
High concurrency defect routed to a distinct later implementation. Draft PR
https://github.com/jmservera/ama/pull/314 targets main, Refs #85, not merge-ready.
No full issue, operational policy or real-platform acceptance is asserted.

<!-- P01 -->
## P01 Core accountability

<!-- P01-T01 -->
### P01-T01 Workflow, projection and semantic tests

Extend WorkflowMixin, not a parallel store. Require source/aware_at for new
reports; derive actor and whole-home hold authority from authenticated staff.
Maintain legacy category/priority as reported observations only. Preserve
legacy stored hazards and mark missing provenance unknown in projection.
Refer requires external case/job plus sent evidence; does not transfer case
owner or imply receipt. Only the selected safety receiver may receive/accept.
Acceptance requires receipt and separate evidence. Sender retains follow-up
before acceptance. Managers may record a manual escalation, not invent policy.
Externally supplied timing observations carry source evidence; unknowns stay
null. A repair is an observation from the service, never a close command.
Release requires an independent safety actor, external evidence and reason,
and releases only the linked-home retrofit hold.

Validate before mutation, reject negative/bool/fractional indexes, immutable
event snapshots and ledger for each transition. Existing JSON body persistence
provides SQL portability. Add no SQL. Redact new source/evidence narratives from
no-need roles; never add them to model prompts or contractor projections.
Tests own lifecycle, authority/replays, restart, legacy unknowns, invalid inputs,
AI/retrofit-pause independence and preserved resident decision/building gates.
Closed records allow new raise/referral without changing closed/stage/consent/
case ownership. Active legacy records may be prospectively bound through
referral with new sent evidence; preserve an immutable legacy snapshot and do
not backfill receipt or acceptance. Legacy repaired records require fresh repair
evidence after acceptance; already released records stay released.
Update gate_reasons/status_line and newly emitted emergency audit guidance to
refer only to the retrofit hold, never service resolution or an invented
same-day policy. Do not rewrite past ledger entries.

<!-- P02 -->
## P02 Staff surfaces

<!-- P02-T01 -->
### P02-T01 HTTP and UI

Extend `/api/cases/{id}/hazard-*`; server supplies actors and cannot accept
client authority. Wire received, accepted and externally observed times to the
same workflow. Update existing safety panel labels to separate report from
service classification and hold release from hazard closure. Display source,
awareness, destination, evidence, follow-up owner, scope and timing unknowns.
Local HTTP tests use fictional staff/home data and a loopback server, including
auth/role failures, forged actor fields, persistence and the static safety UI.
Do not add mandatory AI calls to manual safety intake.
The safety panel must expose intake even on a closed retrofit record.

<!-- P03 -->
## P03 Evidence and delivery

<!-- P03-T01 -->
### P03-T01 Docs and validation

Document contracts and honest limitations in existing core/API READMEs.
Update reference index and append log. Preserve original case study and memory.
Run all five src suites, their ruff and mypy checks, synthetic loopback app,
migration regressions if relevant, and attempt Docker readiness/build. Missing
dependencies may be restored with pip in an isolated local venv.
Record commands, exits/counts, missing-service and Docker limits; do not claim
real inference, SQL Server, deployment or legal/service acceptance from mocks.

<!-- P03-T02 -->
### P03-T02 Review and PR

Reconcile plan/details/changes before one independent RPI Review. Route any
open finding to distinct follow-up; do not repeat Review. Verify authenticated
GitHub noreply identity, use Conventional Commit and requested coauthor.
Commit all RPI artifacts; push only the supplied topic and open main PR using
Refs #85. Preserve unmet issue criteria as unchecked. CI is the image gate;
leave merge to owner.
