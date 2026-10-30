<!-- markdownlint-disable-file -->
---
title: Case journey round seven mutation outcome research
description: Prevent repeated mutations after committed or uncertain responses
ms.date: 2026-10-29
---

## Research Brief

Investigate PR #529's unresolved quality-save thread and sibling mutation paths
in ops.js, assistants.js, app.js and case-workspace.js. Audience: implementer,
independent reviewer and publication coordinator. Output mode: convergence.
Success requires preserved API outcomes, blocked resubmission until authoritative
reload, focused unit/browser regression and no weakening of retryable refusals.
No redesign, Azure, secrets, private data, push or thread mutation is in scope.

## Research Parameters

Focused posture, selected for the supplied failure and named modules. Evidence
root: .copilot-tracking/. Internal candidates: four web modules, API mutation
contracts, test_case_journey, test_workspace_scripts, journey/assistants checks.
External candidates: named Copilot thread and current web interface guidelines.
Heavy checks use nonblocking /tmp/ama-rpi-heavy.lock, retry at most 40 minutes.

## Extension Registry and Provenance

Repository instructions and RPI phase skills selected for workflow/evidence.
web-design-guidelines selected for behavioral web changes, not visual redesign.
Design/redesign skills skipped because existing presentation is unchanged.
Research specialists skipped: this is one coupled outcome-propagation trace.

## User Participation and Research Decisions

Explicit full-loop request supplies automatic execution and scope. No intake
question is needed or possible in this non-interactive execution.

## Direction Controls

Retain branch and Refs #526. Commit dated original artifacts with Conventional
Commits and required trailer. Do not push. Use shared .venv and Ruff 100 columns.
Check remote first: clean topic matches open PR; fetched remote has no new commit.

## Research Questions

* Q1: Where are committed/uncertain outcomes lost?
* Q2: Which sibling mutations can be resent before authoritative reload?
* Q3: Which regression checks prove no duplicate POST and safe reload recovery?

## Prior Knowledge Gate

Supplied thread retrieved through GraphQL, unresolved:
https://github.com/jmservera/ama/pull/529#discussion_r4407516838
(retrieved 2026-10-29). Prior round artifacts are starting context, not evidence
of current correctness. Required case study, addendum, reference index and owner
memory read. No private dataset or environment file accessed.

## Research Cycle Log

### Cycle 1

### Wider

Inline trace found shared case refresh, proposal review, draft review, priority
review, document upload and procurement handlers. case-workspace.js has no
mutation or network handler. Reflection: outcome classification is shared
infrastructure, not a Save evidence-only fix.

### Deeper

api() preserves status/reasons but discards outcome (C1). Shared refresh uses
absence of status as its only uncertainty signal (C2). Proposal and AI draft
reviews repeat that assumption (C3/C4). Upload dispatches before refresh (C5).
Raw resident/challenge forms preserve committed but not uncertain (C6).
Reflection: status alone cannot establish that a mutation was refused.

### Contrarian

Explicit 409 refusal must remain correctable. Network errors without status
already need history checking. Committed need not mean a valid approval; do not
invent a successful review or discard unconfirmed draft values. Authoritative
case/list reload, not tab changes, measure changes or failed GETs, may reset
uncertainty. A field-key-only guard can be bypassed by changing selected measure
or using no submitted controls: retain a session history barrier too.

### Parent Synthesis and Disposition

Accept one shared error classifier with outcome precedence and use it in sibling
guards. Keep existing readable errors and draft recovery. Add status/outcome
matrices including 409/503 committed, uncertain, ordinary refusal and transport
loss. Reject blocking every HTTP error: proven pre-commit refusals are retryable.
Reject adding backend idempotency as unnecessary to the requested UI correction.
No new cycle required: named paths and material alternatives are covered.

## Evidence Log

* W1: Unresolved thread above identifies HTTP 503 / outcome committed being
  reduced to a retryable refusal by ops.js.
* C1: src/api/src/zava_forward/api/web/app.js:29 API error construction drops outcome.
* C2: src/api/src/zava_forward/api/web/app.js:612 shared refresh treats HTTP status as refusal.
* C3: src/api/src/zava_forward/api/web/assistants.js:66 proposal review resets on any status.
* C4: src/api/src/zava_forward/api/web/app.js:358 draft review reenables on any status;
  app.js:429 priority review repaints actionable stale data after any failure.
* C5: src/api/src/zava_forward/api/web/app.js:1247 upload POST precedes protected refresh.
* C6: src/api/src/zava_forward/api/web/panels.js:174 and :368 raw forms omit uncertain.
* C7: src/api/src/zava_forward/api/web/ops.js:195 procurement reenables after all errors.
* C8: src/api/src/zava_forward/api/server.py:1040 quality uses 503 committed;
  :915 procurement and :1004 resident use 409 committed.
* C9: src/api/tests/test_case_journey.py:200 and :679 and browser helper matrices
  exercise actual shipped handlers but omit structured committed/uncertain errors.
* W2: https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
  fetched completely 2026-10-29; preserve status semantics, native actions and drafts.

## Findings, Alternatives and Decision State

Selected approach above grounded in C1-C9. Assistant invocation also needs a
same-case request barrier because repeated requests can record duplicate proposals.
Other generation/manual paths use shared refresh or are advisory GET/import/
authentication flows, not a safe-refusal oracle. No authority boundaries change.

## Planning Readiness

Ready. Research disposition: executed, Complete. Questions Q1-Q3 answered.
Self-check: evidence IDs, ordered waves, alternatives, constraints and handoff
present. No claim of live acceptance or absence of all future findings.
