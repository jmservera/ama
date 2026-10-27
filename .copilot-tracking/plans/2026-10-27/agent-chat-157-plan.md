<!-- markdownlint-disable-file -->
# RPI Plan: Per-user agent chat and memory

## Task Metadata

* Task ID: 157
* Task slug: agent-chat-157
* Plan date: 2026-10-27
* Planning status: Ready for independent engineering; human activation blocked
* Phase details: .copilot-tracking/details/2026-10-27/agent-chat-157-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/agent-chat-157-plan-critique.md

## Executive Summary

Harden existing staff chat without enabling it for real data or model spend.
Use one cited turn path, preserve provider usage per invocation, bound prompt
input without silently breaking JSON, recheck permissions after a model call,
and display the canonical privacy warning.

### What You May Not Know

Most original engineering already exists. The remaining whole-issue criteria
include decisions no agent can supply. The development golden report has a
known critical claim-grounding failure; preserve it and keep enablement denied.
The existing release gate does not register/authorize a conversational task.

### Unresolved Decisions or Blockers

OD-45/46/48/49, competent human/held-out/serving-model evidence, named
screen-reader testing, finite owner-approved role budgets and stabilization
#440 remain open. No issue will be closed on this PR.

## User Decisions and Requirements

* Complete the ordered RPI loop with dated artifacts, one PR to main on the provided branch.
* Cover #162, #159, #164 and #163 under parent #157, without rebuilding existing abstractions.
* No Azure, paid inference, private data, secrets, uv or full gate.
* Preserve human approval/resident consent. Do independent work and report human blockers.
* Local tests; at most one locked changed gate for large work, timeout zero if busy.

## Goals

Close independently evidenced dispatch, prompt, telemetry and warning gaps.
Keep local engineering outcomes distinct from whole-issue or live acceptance.

## Scope and Non-Goals

Existing chat core, agents adapter/evaluator and staff panel/API only.
No new agents/store, real processing, retention policy, break-glass authorization,
semantic grounding guarantee, independently labelled dataset or accessibility
conformance claim.

## Functional Requirements

* Both public general-chat turn routes use the cited, proposal-only panel.
* Actual model adapter refuses dispatch without admission. API consumes the
  existing release/registry boundary; unregistered conversational task is denied.
* Usage/outcome metadata never contains prompts, messages, memory or provider errors.
* Canonical warning is server sourced and associated with the question field.
* Model completion cannot release a reply after current role/case/source changes.

## Non-Functional Requirements

* One provider call per turn, zero retries, at most 600 output tokens in the
  default adapter; no new spend authorization.
* Hard engineering ceiling: system plus prompt <=16,000 characters, user
  history <=12 messages and <=4,000 characters. Oversize returns workflow-only;
  no malformed/truncated source JSON. These are implementation caps, not
  owner-approved token/role/budget limits.
* Reuse existing provider envelope and metadata ledger; tests use synthetic stores.
* Retain native Fluent styling/semantics and current plain-language standard.

## Acceptance Criteria

* Regression tests prove no dispatch on denied admission or oversized context,
  usage validation and explicit Unknown tokens/cost, and post-call revocation.
* Legacy HTTP turn route cannot bypass cited/refusal/admission policy.
* Report records calls, outcomes, tokens or Unknown per turn/scenario and per
  runtime accepted answer; that denominator is not human acceptance.
* Warning is visible, accessible by description, and retrieval failure blocks
  entry with an explicit manual route.
* Existing chat/isolation/privacy suites pass; known semantic eval failure remains
  visible with enablement fail/disabled.

## Sources

Research C1-C7, W1-W3 in
.copilot-tracking/research/2026-10-27/agent-chat-157-research.md;
ADR 0004/0006, linked BRD/PRD sections and named issues read at intake.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Bound and unify chat turns
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Admission, invocation receipts and prompt/completion guards

Core panel + agents adapter; preserve old injected string providers for
scripted tests but mark token usage unknown. No shared mutable last-usage state.
Route `/messages` through panel with compatible `withheld` field.

<!-- rpi:phase id=P02 -->
### [x] P02: Warning and evidence reporting
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Server warning, UI status and offline consumption report

Reuse canonical warning in a permitted `/api/chat/status` response; fail closed
on loading errors; display refusals accurately. Extend shared chat evaluator,
not a new harness; no real calls.

<!-- rpi:phase id=P03 -->
### [x] P03: Validation and evidence
<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Local regression, documents and Review preparation

Update DPIA draft/index/log and component README contracts. Preserve all human
checkboxes unchecked and report stabilization/AI/accessibility residuals.
Review preparation is complete; the one independent Review is the subsequent
lifecycle phase, not a second implementation pass. Final targeted API/browser
suite: 80 passed; agents discovery: 109 passed. Broader core/API discoveries
are supplemental and still running, not claimed passed.

## Test Ownership and Locked Candidate

Core: existing test_chat_panel.py and chat lifecycle/isolation tests.
Agents: existing test_chat_model.py, test_chat_eval.py.
API: existing test_chat_panel.py, role endpoint inventory/isolation tests.
Exact removals: none. Maximum additions: 20 test methods across existing files,
one browser-focused test file only if existing harness cannot cover new controls.
Canonical outputs: source/tests/docs and RPI artifacts. Generated evaluation
report: dated changes subdirectory, not replacement of historical golden evidence.
Semantic coverage remains explicitly unmeasured; scripted tests are regressions.
Validate targeted suites, Ruff/mypy and API discovery; browser if available.
This bounded change uses targeted local checks, not the optional heavy gate.

## Dependencies

P02 depends on P01 receipt shape; P03 depends on both. Privacy/access/release
approval is a blocker for activation, not for offline independent engineering.

## Critique Disposition

One critique executed, original verdict Revise (1 High, 3 Medium), preserved.

| Finding | Disposition | Resolution |
| --- | --- | --- |
| PC-001 | Applied | Adapter admission is checked before and after the provider; changed/denied admission discards text but retains usage. Actual release remains unavailable. |
| PC-002 | Applied | One per-turn metadata event survives post-call rejection; evaluator reads ledger events on exception rather than only replies. Zero-call denial is separately recorded. |
| PC-003 | Rejected: unsupported premise | No active instruction prohibits /tmp. User explicitly requires /tmp heavy lock and external output; current isolated pip venv is valid. Do not invent an environment restriction. |
| PC-004 | Partially applied | Preserve original Review verdict and do not claim independent acceptance of later heads. New material defects block publication; route as later work without a repeated Review under the one-pass caller contract. Human residuals alone permit a Refs-only draft PR. |

No second critique. Executive summary and details reconciled.

## Follow-Up Items

* Human owner/DPO/Legal decisions and named accessibility exercise remain
  outside independently implementable scope.
* Known semantic grounding failure and #440 prevent whole-parent acceptance.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-27/agent-chat-157-changes.md.
P01-P03 complete for independent engineering. Proceed once to Review using the
changes acceptance disposition and generated evaluation failure. Core/API broad
discovery results remain pending and must not be inferred from targeted passes.
