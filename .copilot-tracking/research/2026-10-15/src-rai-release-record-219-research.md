---
title: Research - task-bound RAI release records
description: Issue 219 evidence and scoped readiness
ms.date: 2026-10-15
---
<!-- markdownlint-disable-file -->

## Research Brief

Research issue #219 for a task-bound RAI release gate in the migrated src
registry and dispatch paths. Audience: implementer and PR reviewer. Output mode:
convergence. Non-goals: live authority, deployment, private data, queue transport
(#144), and owner decisions. Acceptance is the five issue checkboxes, with
unsupported evidence left open.

## Research Parameters

Focused posture (bounded caller scope); internal candidates: core ai_registry,
ai_tasks, assistant_release, assistants and stores; API and agents dispatch.
External candidates: issue #219 and merged PRs #296-#302 only. Evidence root:
.copilot-tracking/research/. Research edits restricted to evidence and required
session tracking. No external regulatory claims or billable inference.

## Extension Registry and Provenance

| Kind | Candidate | Disposition |
| --- | --- | --- |
| Instruction | .github/copilot-instructions.md | Selected: src layout, knowledge-base maintenance, privacy-safe commits |
| Skill | rpi-research | Selected: inline wider/deeper/contrarian research |
| Skill | rai-standards | Skipped: no new standards assessment or compliance claim |
| Specialist | hve-core-all:rpi-researcher | Skipped: one tightly coupled registry/dispatch trace |

## User Participation and Research Decisions

No interaction needed: caller explicitly requests the full loop, topic branch,
push and PR. Unavailable OQ-017 authority must be recorded, never invented.

## Scope and Success Criteria

Only the specified worktree and branch; all code/tests under src. Core imports
no workload; no SQL/blob dependencies for agents. Preserve human approvals,
resident consent, synthetic-only exercise and SQL Server portability.

## Direction Controls

ADR 0006 is Accepted. The issue owner comment changes legacy paths, not
criteria. No new code in mvp. Do not touch .env, .vscode, or the issue mirror.

## Research Questions

| ID | Question | Status |
| --- | --- | --- |
| Q1 | Where can one release gate cover registered task activations? | Investigating |
| Q2 | Which merged admission controls can be reused? | Investigating |
| Q3 | What evidence and authority remain unavailable? | Investigating |

## Prior Knowledge Gate

Read case study original/addendum, reference index/memory, repository
instructions, src README, ADR 0006 and parity mapping. Verified #296-#302
merged; ai_registry and assistants are in core by the parity matrix's explicit
dependency-rule exception, not their older proposed agents targets.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Issue #219 requires version binding, denials, approved exercise proposals,
material-change invalidation and named authorities or an explicit gap.
Merged migration mapping identifies existing assistant_release and registry
as reuse candidates. Reflection: inspect the actual activation and provider
paths rather than build a second dispatch system.

#### Wave 2: Deeper

Existing SQL admission already covers invoke, scan/enqueue, claim,
pre-dispatch, completion and human reliance. Reuse it. The record currently
lacks intended/prohibited use, stakeholders, owner, impact and explicit
change triggers. Matching is duplicated in SqlStore; JSON bypasses release
admission. Activations do not retain the selected record identity.

Reflection: extend the merged contract and centralize matching, not a second
release store. Preserve all existing SQL schema and authority configuration.

#### Wave 3: Contrarian

Challenged the assumption that a matching deployment alias identifies a model:
it does not. Add an explicit expected model version, and keep returned model
comparison labelled as a check, not provider attestation. Challenged a
record-only change: a permissive historical record could revive after a
rollback, or another active record's model could authorize completion.
Supersede records per task/endpoint/deployment and bind each activation to
the exact selected record. JSON cannot provide SQL-owned approval, so
configured AI there must deny, with synthetic tests explicitly installing
test-only authorization where they test unrelated output behavior.

Parent synthesis: accept reuse plus contract/matching/identity changes; reject
a parallel governance framework. Defer real evaluation approval, qualified
review and live holders to OQ-017. No further cycle needed: trace and negative
cases cover the bounded engineering decision.

## Evidence Log

| ID | Evidence | Finding |
| --- | --- | --- |
| W1 | https://github.com/jmservera/ama/issues/219 (retrieved 2026-10-15, body and comments via gh) | Five criteria unchanged after src pivot |
| C1 | docs/adrs/0006-src-layout-and-cutover.md:54 | New code under src; core cannot import workloads |
| C2 | docs/architecture/mvp-to-src-parity-matrix.md:170 | Registry/assistants migrated into core; assistant_release reused there |
| C3 | src/core/src/zava_forward/core/assistant_release.py:13 | Existing BOUND, admission, record/change and portable DDL |
| C4 | src/core/src/zava_forward/core/assistants.py:478 | Existing admission used through dispatch/reliance, but no activation record identity |
| C5 | src/core/src/zava_forward/core/sqlstore.py:158 | Duplicated legacy matching; configured provider needs actual evidence |
| C6 | src/core/src/zava_forward/core/store.py:64 | JSON gate checks suspension only |
| C7 | docs/prds/zava-forward-retrofit-programme-demonstrator.md:2018 | OQ-017 authority remains unresolved |

## Alternatives and Decision State

Selected: enrich existing release records and reuse SQL storage/approval routes
with one shared matching implementation. Reject a second store and new service.
Do not approve live use or invent evaluation results. Real-model and Azure
checks cannot be claimed from local nonbillable provider fixtures.

## Open Questions, Risks and Residual Uncertainty

OQ-017 holders and real approved evaluation evidence are not supplied.

## Planning Readiness

Research disposition: executed. Planning Readiness: Ready for scoped engineering.
All Q1-Q3 answered by C3-C7. Unavailable live authority/evaluation evidence is an
explicit acceptance limitation, not a blocker to implementing deny-by-default.
Self-check: three ordered waves complete, local/external evidence separated,
scope and decisions retained, no source implementation during Research.
