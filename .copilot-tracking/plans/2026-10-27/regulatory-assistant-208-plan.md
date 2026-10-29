<!-- markdownlint-disable-file -->
# RPI Plan: Regulatory assistant completion

## Task Metadata

* Task ID: 208
* Task slug: regulatory-assistant-208
* Planning status: Ready; original critique Revise retained, six direct corrections applied
* Plan date: 2026-10-27
* Phase details: .copilot-tracking/details/2026-10-27/regulatory-assistant-208-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/regulatory-assistant-208-plan-critique.md

## Executive Summary

Complete the independent synthetic slice: automatically refer supported source
conflicts with their original evidence, report content-free zero-model
consumption by outcome and current role/day, and expose explicit Unknown costs
and cards-only shipping in evaluation and UI. Reuse existing retrieval,
thread isolation, rule checks, audit and native Fluent-token UI.

### What You May Not Know

Most original functionality already exists. The missing human evidence cannot
be supplied by code: DPO review/retention periods, real Entra assignments,
owner-agreed thresholds, continuing-stock validation and staff comprehension
remain unmet. No model is introduced and no spend authority is inferred.

### Unresolved Decisions or Blockers

Operational reliance and issue closure remain blocked. Caller excludes the
full gate mandated by repository publication policy; record the conflict and
do not bypass it. #440 remains an epic-closure dependency.

## User Decisions and Requirements

* Run research, plan, implement and one independent Review in order.
* Cover #208 and listed children #214, #216, #215, #217 on the supplied branch.
* New code stays in src namespace packages; tests outside packages.
* Preserve human interpretation, approval, resident consent and safety routes.
* Use local synthetic tests only, pip, no secrets/private datasets/Azure/paid AI.
* Do not invent owner, Legal, DPO or Compliance decisions; retain blockers.
* At most one scoped changed gate with a fresh external output and nonblocking
  heavy lock is authorized; no full gate.
* Conventional commit with required trailer and privacy-safe local email.
* Use Refs, not Closes, for criteria still missing evidence.

## Goals

* Make conflicting-source escalation real and durable, not merely suggested.
* Make offline calls, outcomes, cost unknowns and non-authorization visible.
* Preserve and document the boundary between local engineering and acceptance.

## Scope and Non-Goals

Included: regulatory chat/usage/privacy, deterministic check/alert metadata,
evaluation comparator, existing alert/chat UI and focused browser checks.
Excluded: new AI task/provider, live activation, real participant studies,
legal decisions, actual Entra provisioning, retention disposal, unrelated fixes.

## Functional Requirements

* Store conflict question, both cited versions and isolated owner receipt
  atomically using the existing chat transaction. Reuse one referral writer
  for automatic and manual doubt routes; one inbox per stored thread/turn.
  Repeated asks, even equal text, intentionally create distinct turns.
* Missing/ambiguous/unauthorized owner refuses before storing an unroutable
  conflict; ordinary supported answers/refusals retain their existing path.
* Audit consumption as identifiers/counts/versions/outcome only, with no raw
  question, home facts or retrieved text. Aggregate only the authenticated
  user's current role and UTC day, without reading message content.
  Read at most the latest 1,000 audit positions; SQL projects foreign detail
  as NULL. JSON additionally tails at most 256 KiB, dropping a partial line.
  Expose bounded_partial when truncated and recorded_audit_only otherwise;
  never claim exact turn totals because JSON post-commit audit gaps and
  historical unmetered records cannot be reconstructed.
* State zero model calls per offline question/check/alert and a hard zero
  model-call allowance for every role/day; this is disabled inference, not an
  owner-approved paid budget. Report token counts zero and monetary cost
  Unknown, naming price/billing/allocation and review-effort gaps.
* Show automatic routing receipt, zero-call consumption and Unknown cost in the
  existing UI with text status and native keyboard controls.
* Comparator reports cost per accepted check as Unknown with missing inputs,
  finite zero-call execution, absent paid authority, and cards_only shipment.

## Non-Functional Requirements

* No model, source or user text can alter clocks, alerts, permissions or rules.
* SQL stores commit messages, inbox, receipt and audit together; JSON rollback
  preserves its preimage, retaining the existing separate file-ledger boundary.
  Post-save JSON audit failure preserves committed chat and exposes an error
  instructing history reload, never a false rollback. Audit-only counts cannot
  prove all turns were metered.
* Recheck sender provisioning/role, thread role and both case projections plus
  named-owner identity/role inside the locked transaction before mutation.
  Preserve trusted-proxy role authority. Expose no other user's metering.
* No new schema, dependencies, framework or workflow/check rename.
* WCAG checks remain scoped engineering evidence, not a conformance claim.

## Acceptance Criteria

* Both conflict sources and the selected turn reach exactly one named owner's
  inbox per stored thread/turn. SQL failure before COMMIT takes effect rolls
  back all rows/audit; JSON pre-save failure leaves no partial chat. Actual
  SQL COMMIT injection is distinct from its no-op repo.commit hook, and from
  an acknowledgement lost after a successful commit.
* Missing owner, stale role, hostile content and ordinary refusals cannot
  bypass isolation or suppress deterministic alerts.
* Usage survives SQL restart, separates answer/refused/conflict outcomes,
  excludes foreign-role/user/day records and contains no content canaries.
* Deterministic check/alert metadata declares zero calls without changing
  check identity, clocks, visibility or idempotency.
* Independent evaluation mutations fail for forged consumption metadata;
  numeric checks remain separate and cards_only recommendation remains.
* Browser covers keyboard, plain-language mode, source conflict, routing,
  consumption, responsive widths and axe when available.
* Every issue criterion is mapped to evidence or an explicit unmet boundary.
  These are slice criteria, not replacements for the issues' full acceptance.

## Sources

Research artifact .copilot-tracking/research/2026-10-27/regulatory-assistant-208-research.md;
ADR 0005/0006; BRD FR-051/AC-099/OD-50 and PRD FR-060/AC-104-106/OQ-026;
actual gh issue views 208/214/216/215/217/440; existing project READMEs.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Durable conflicts and content-free consumption

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Atomic automatic and manual doubt writer

Targets core regulatory_chat, existing core/API tests. Reuse current role/case
admission and owner validation; store one receipt within the turn transaction.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Offline usage and privacy boundaries

Add a small pure usage contract and existing audit/status integration; include
deterministic checks and alerts. No provider or new financial authority.

<!-- rpi:phase id=P02 -->
### [x] P02: Evaluation and role-shaped presentation

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Explicit cost and no-spend comparator

Extend independently authored consumption expectations, negative controls and
generated report; preserve per-check evidence and all unknown human measures.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Existing alert/chat presentation

Add plain text receipt/usage states with native semantics. Extend existing
regulatory browser harness, not a redesign.

<!-- rpi:phase id=P03 -->
### [x] P03: Validation, documentation and evidence

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Local regression and acceptance reconciliation

Run relevant suites, lint/types, frozen evaluation, browser and migration guard.
Update project guides and existing knowledge synthesis/index/log. Preserve
original adverse results. Hand off to exactly one independent post-implementation
Review; Review execution is recorded separately from these implementation
markers. Findings become follow-up work, not a second Review.

## Test Ownership and Change Budget

Canonical tests: core regulatory_chat/privacy/rule_engine; agents
regulatory_answers/gates; API regulatory_chat_api/rule_alerts and
checks/regulatory_ux_check.py. New pure usage tests belong to core/tests.
Exact removals: none. Maximum additions: 20 test methods plus extensions of
existing assertions/browser states. Generated target:
src/agents/evals/regulatory_gates_results.json, regenerated with the existing
runner only after canonical fixture/grader changes. The older 13-case
regulatory_chat_results.json stays unchanged unless its output contract changes.
Behavioral tests cover actual persistence/HTTP/browser; closed-template grader
mutations cover regression consistency, not semantic/legal validation.
External logs and browser assets stay in the session files directory.

## Dependencies

Existing law store/cards/engine and isolated thread repository. Real DPO,
threshold and staff decisions are not prerequisites for this independent slice,
but block operational acceptance. Mandatory publication gate remains unmet.

## Critique Disposition

One independent critique executed, original verdict Revise (2 High, 4 Medium).
All are compatible planner-owned corrections; no second critique.

| Finding | Owner and disposition | Resolving plan evidence |
| --- | --- | --- |
| PC-001 | Planner, applied | Bounded SQL position window and JSON byte/position tail; honest audit-only/partial coverage in FR and P01-T02 details |
| PC-002 | Planner, applied | Explicit pre-save/SQL rollback versus JSON committed-audit-failure contract in NFR and P01 details |
| PC-003 | Planner, applied | Transaction-time sender/owner/case rechecks; preserve authenticated trusted role |
| PC-004 | Planner, applied | Dedupe unit is source thread/assistant turn; repeated ask is new work |
| PC-005 | Planner, applied | Inject actual SQL COMMIT-before-effect failure; distinguish acknowledgement loss |
| PC-006 | Planner, applied | Complete criterion allocation below, unchanged issue checkboxes |

## Issue Criterion Allocation

Historical implementation is not fresh validation. P03's changes record now
maps all 35 rows below to actual execution evidence and unmet boundaries.
No issue can be closed from this slice alone.

| Criterion | Allocation and planned evidence | Unmet boundary / owner |
| --- | --- | --- |
| 208.1 Stabilization #440 | P03 requirement/architecture reconciliation | Full #440 checkpoint remains coordinator work |
| 208.2 Decision accepted/amended | ADR 0005 accepted synthetic development, 2026-10-16 | No operational acceptance, owner |
| 208.3 Child phase acceptance order | Existing law/cards/check/chat/monitor code; P03 scoped regressions | Child acceptance/phase ratification not inferred, owner |
| 208.4 No satisfied duty/advice/future active | Existing closed extractive template, rule engine; P01/P02 regressions | No actual legal grading, Legal |
| 208.5 Live blocked pending named approval | Existing synthetic admission and SYNTH privacy refs; P03 API denial tests | Actual appointments/approval absent, Legal/Compliance/DPO |
| 214.1 Every statement cited/status/dates | Existing fixed template/provision/fact metadata; P02 oracle mutations | Exact excerpts only, not generated prose acceptance |
| 214.2 Role/minimum facts | Existing projected allowlist; P01 transaction and cross-role tests | Actual Foundry query unexecuted |
| 214.3 No conclusions/advice/future/terms | Existing refusals; P02 adversarial regression | Held-out/Legal grading absent |
| 214.4 Both conflicts shown/escalated | P01 atomic owner inbox and P02 browser | Synthetic named owner only |
| 214.5 One-action doubt route | Existing selected-turn route, shared P01 writer | No operational appointment |
| 214.6 Retrieved injection inert | Existing quotes only; P02 malicious-source tests | No real-model claim |
| 214.7 Model-negative cannot suppress alerts | No model; existing engine independence, P03 tests | No model evaluation |
| 214.8 Stored turns/sources | Existing isolated history, P01 restart/rollback | JSON file ledger remains separate |
| 214.T1 Calls/question/alert, role/period bounds/outcomes | P01 zero-call records/current-role/day audit and P02 UI | No nonzero owner budget or live usage authority |
| 216.1 Owner-agreed citation/refusal gates/graded set | Existing provisional grader, P02 mutations | Actual agreement/independent graded set absent, owner |
| 216.2 Hazard misses critical | Existing negative controls, P03 rerun | Synthetic baseline only |
| 216.3 Recall baseline before thresholds | Existing stateless 60,000-home runner, P03 rerun | Continuing stock and owner baseline review absent |
| 216.4 Paired value/cards alone | P02 same-source comparator/cards_only | Staff paired measurements absent, owner/staff |
| 216.5 Out-of-cadence labels | Existing freshness API/chat/browser, P03 regressions | Live monitoring/legal currentness absent |
| 216.6 Per-check outcomes | Existing independent check report, P02 rerun | No aggregate acceptance |
| 216.T1 Cost/accepted check and quality/cards_only | P02 explicit Unknown/missing denominator/price/billing | No accepted staff checks/prices, Finance/owner |
| 216.T2 Finite owner-authorized model run | No model; hard zero calls/tokens/budget and no paid expiry | Any paid run requires independent authority, owner |
| 215.1 Per-role know-at-least | Existing role guidance/supplier panel; P02 browser | Actual role needs validation absent |
| 215.2 Notice/source/status/action/owner/clock | Existing alert DL, P02 browser | Fictional clocks not statutory |
| 215.3 WCAG AA/no colour/keyboard/plain mode | P02 existing native controls/axe/keyboard/widths | Full WCAG/manual assistive-tech acceptance absent |
| 215.4 Doubt/no-source states | Existing refusal/route; P01/P02 conflict and browser | Human route remains synthetic |
| 215.5 Staff comprehension | Explicit Not evaluated | Actual repairs/housing/grants participants required |
| 217.1 DPIA with DPO before live | Existing draft and live block, P03 denial tests | Completed actual DPO assessment absent |
| 217.2 Retention aligned/DPO periods | Existing review-only report, P01 usage class | Actual periods/disposal/holds not approved, DPO |
| 217.3 Minimal Foundry/special-category purpose | Existing bounded offline retrieval/no provider; P03 tests | Actual Foundry privacy evidence absent |
| 217.4 Separate Entra author/approver/chat roles | Existing capability map, P03 auth tests | Actual Entra assignment evidence absent, identity owner |
| 217.5 Changes/approvals/checks/alerts/chat audited | Existing append-only stores, P01 atomic SQL audit | JSON ledger separate; real retention unresolved |
| 217.6 Injection/cross-role tests | Existing suites plus P01 transaction-time tests | No deployed security acceptance |
| 217.7 Art 22A-C named human/reasons | Existing deterministic human-review safeguard; P03 tests | Legal applicability/actual appointments not decided |
| 217.T1 Content-free scoped retained audited metering | P01 metadata-only audit/zero calls/role/day and privacy inventory | Actual DPIA/retention periods remain DPO blockers |

## Follow-Up Items

* Owner: agree evaluation tasks/thresholds and measured paired staff trial.
* Legal/Compliance/DPO: actual appointments, DPIA, retention and role separation.
* Coordinator: #440 stabilization and mandatory publication-gate reconciliation.

## Handoff

Changes: .copilot-tracking/changes/2026-10-27/regulatory-assistant-208-changes.md.
P01-P03 implementation and local evidence are reconciled. The one independent
Review is the next lifecycle phase, not yet executed at this handoff. No
material scope divergence or second critique occurred. Publication and human
acceptance blockers remain separate; no issue closure is authorized.
