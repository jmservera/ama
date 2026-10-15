---
title: Issue 83 return, reopen and role-owned handoffs research
ms.date: 2026-10-15
---
<!-- markdownlint-disable-file -->

## Research Brief

Implement the evidence-supported remainder of issue #83, preparing a plan for
return/reopen provenance and distinct accountable handoff states. Audience:
maintainers and issue owner. Output mode: convergence. Research posture: focused,
selected from the explicit issue, ADR and source targets.

## Research Parameters and Direction Controls

* Work only on `feat/src-handoffs-83` in the assigned worktree.
* All new implementation and tests live in `src/`; reuse migrated modules.
* Do not touch `.env`, `.vscode`, or `.copilot-tracking/github-issues`.
* No live deployment, private data, billable inference or invented approval.
* Record local checks and missing CI/live evidence rather than infer acceptance.
* Resolved research root: `.copilot-tracking/research/2026-10-15/`.

## Extension Registry and Participation

Repository instructions and accepted ADR 0006 selected as layout/dependency
constraints. RPI phase skills selected as lifecycle contracts. Python guidance
applies to implementation, not a separate research lane. Role agents and external
research skipped: this is a bounded source-contract investigation, not company
discovery. Inline investigation avoids fragmenting a continuous workflow trace.
No interaction required: user explicitly requested the complete loop and directed
that owner-dependent criteria remain unticked.

## Questions and Candidate Areas

1. What do FR-009/010/011 and BG-010 actually require?
2. Which migrated workflow, store, API and UI paths already implement them?
3. Which omissions can be implemented without inventing owner decisions?

Candidate areas: `core/workflows.py`, store implementations, API endpoints,
workflow tests, approved exercise assumptions and source requirements.

## Research Cycle Log

Cycle 1 completed inline:

1. Wider: issue, migration PRs #296 to #302, ADR, matrix, PRD and approved
   exercise assumptions establish the layout and acceptance boundary.
2. Deeper: traced WorkflowMixin through Store/SqlStore persistence, API dispatch,
   projection, UI and existing workflow/role tests. Existing offers transfer
   ownership only on acceptance but omit receipt/escalation/completion.
3. Contrarian: the legacy `hand_over` bypass transfers ownership immediately;
   a new state path alone would not fix the invariant. Pending queues expose
   notes without role redaction and only show recipient work. Legacy returns
   have no source/authority/next-step fields. Fix coupled bypass and projection.

Reflection: reuse the mixin and case JSON persistence; no new SQL schema or
dependency is needed. Existing AI remains enabled/configurable and proposal-only.
No new model call belongs in deterministic ownership transitions.

## Evidence Log

* W1: https://github.com/jmservera/ama/issues/83, retrieved 2026-10-15.
  Three unticked criteria; owner comment changes paths only, not acceptance.
* C1: `docs/adrs/0006-src-layout-and-cutover.md:166`: core imports no workload;
  API may import agents temporarily until #144.
* C2: `docs/case_study_48_addendum.md:124`: EXA-008 preserves sender chase
  responsibility and labels 24/48/72h thresholds artificial exercise targets.
* C3: `docs/prds/zava-forward-retrofit-programme-demonstrator.md:844`:
  FR-009/010/011 define return provenance and distinct ownership/receipt states.
* C4: `src/core/src/zava_forward/core/workflows.py:38`: returns record reason
  and stages only; offers retain sender ownership, but lack three states.
* C5: `src/core/src/zava_forward/core/store.py:341`: immediate hand_over bypass.
* C6: `src/core/src/zava_forward/core/sqlstore.py:350`: touched case bodies and
  audit entries persist together; MSSQL inherits the workflow implementation.
* C7: `src/core/src/zava_forward/core/projection.py:99`: existing note holding
  must apply to new source/next-action free text and pending queues.
* C8: `src/api/tests/test_workflows.py:80`: regression contract retains legacy
  Offered/Declined labels; additive canonical status avoids breaking persisted data.
* C9: `docs/brds/agentic-retrofit-programme-brd.md:599`: BG-010 approved
  operational timings remain unknown (OD-09); synthetic hours are not approval.

## Findings, Alternatives and Decision State

Select additive provenance and handoff state/history fields in existing core
mixin; API/UI expose the same fields. Retain Offered (sent) and Declined
(rejected) storage labels with explicit canonical status. Reject renaming old
data or adding a parallel workflow service. Route legacy immediate handover
through offer/accept rather than allowing a second authority path.

Return metadata is required for new API/UI confirmations; legacy direct calls
remain compatible with explicit unknown source/next action. Source is a human
reference, not proof of verified evidence. Receiving owner defaults to the
existing named case owner unless explicitly selected.

Unaccepted queues include sender/chase/receiver and manager visibility; manual
escalation has a named manager and reason. Optional human-selected due date is
visible. Do not invent approved operational timers or claim automatic escalation
within BG-010 approved periods. Preserve resident decisions and safety guards.

## Open Questions and Residual Uncertainty

Approved operational timing/authority and witnessed live SQL/Azure/model evidence
are unavailable. Leave criterion 3 unticked and identify these as follow-ups.
Broader selective approval invalidation (FR-043) is not silently claimed here.

## Planning Readiness

Ready for bounded implementation; owner/live criteria excluded explicitly.
Research disposition: executed. No additional cycle needed: remaining gaps need
owner or CI/live evidence, not another source search. Parent continues to Plan.

## Implementation Reconciliation

The initial direct-call compatibility option above was strengthened during
implementation: every new core/API disposition requires source and next action.
Only previously persisted records retain unknown provenance. The receiving
owner selection option was simplified after PC-001: dispositions always record
the current case owner and never reassign. Current plan/details/changes and the
single Review record own the delivered contract; this section preserves the
research-to-implementation decision trail without claiming legacy data was
verified. Published as PR #311 using Refs #83.
