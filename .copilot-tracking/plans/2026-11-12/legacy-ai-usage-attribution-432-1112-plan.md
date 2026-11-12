<!-- markdownlint-disable-file -->
# RPI Plan: Legacy AI usage attribution (Refs #432, first criterion, initial slice)

## Task Metadata

* Task ID: legacy-ai-usage-attribution-432-1112
* Task slug: legacy-ai-usage-attribution-432-1112
* Planning status: ready
* Plan date: 2026-11-12
* Phase details: .copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan-critique.md

## Executive Summary

Research found that the legacy text-draft path already returns validated provider usage, a meter id and root, and joins its output and human review to the Consumption ledger. The "legacy paths discard usage" statement in the issue and the tokenomics resource is stale. So this plan adds no capture. It fixes one ordering defect in `Ai._request` (usage is placed in the result before the ledger settles it, so a failed settlement can leave a record envelope claiming tokens the ledger does not hold), proves the legacy text-draft join with synthetic provider spies (success, missing usage, malformed usage, provider failure, settlement failure, unchanged workflow-only no dispatch), and corrects the stale documentation sentence. It claims no cost, price, billing, authority renewal or criterion tick.

### User Decisions and Requirements Highlights

* One initial bounded offline slice, reuse existing wrappers, Store and ledger; no new dispatch, price or budget assumption.
* Missing or invalid usage is Unknown, never estimated.
* Existing criterion 1 stays unticked; this is not a fresh five or extra correction.

### What You May Not Know

* The installed editable distributions point at another checkout; validation must put this worktree's src directories first on PYTHONPATH.
* The resident chat host's direct `_chat` call is a different path and stays excluded.

### Unresolved Decisions or Blockers

* None for this slice. OD-51, price source, authority renewal, billing reconciliation and held-out batch remain owner gates.

## User Decisions and Requirements

* Run the full RPI sequence with genuine dated artifacts; local-only clean frozen candidate; no push, PR or issue edits, cloud or provider calls or spend.
* Base 139176fa0382add781b1830b1ac9db785ed086fe, target main, Refs #432 only.
* Not a resident-host window renewal, paid measurement, OD-51 approval, release, correction allowance or production cost acceptance.
* Verify an unimplemented path first; if already implemented, report precise proof and do not duplicate.
* Cover a successful legacy join, missing and malformed usage, failures and retries, and unchanged no-dispatch refusal and manual behavior; synthetic provider spies only; no raw text or case content in receipts.
* Do not edit the #116 provider-spy tests or duplicate its payload-equality matrix; do not touch assistants.js; #184 stays design-only.
* Targeted tests plus lint and types only; no full gates, SQL or browser runs; no new dependency installs unless a real missing-dependency failure.

## Goals

* Make the legacy text-draft result carry usage only when the ledger settled it, and prove the legacy join and Unknown handling.
* Remove the stale "discards usage" claim from the knowledge base with a dated log entry.

## Scope and Non-Goals

### In Scope

* `Ai._request` receipt ordering in src/core/src/zava_forward/core/ai.py.
* New tests in the existing src/api/tests/test_ai_consumption_api.py for the `briefing` text-draft path.
* Correction of docs/reference/resources/ai-tokenomics.md legacy sentence, docs/reference/log.md entry.

### Non-Goals

* Resident chat host, assistants, `look_at` and priority proof, prices, budgets, billing, reports, authority, models, any live call, any criterion tick, issue edits.

## Functional Requirements

* A successful legacy draft returns usage equal to the ledger completion tokens and joins output and review.
  * Observable acceptance criteria: test asserts envelope usage equals the completed ledger record tokens and `meter_id`/`meter_root` match the reservation; output record exists.
* Missing or malformed provider usage yields envelope usage None, ledger tokens None, an Unknown liability alert, report token cost Unknown and the manual route with no AI source.
  * Observable acceptance criteria: tests for omitted usage and total-mismatch usage.
* Provider failure yields usage None, template text and no output join.
* A settlement failure leaves the result without usage.
* Workflow-only mode dispatches nothing and reserves nothing.

## Non-Functional Requirements

* No raw prompt, case text or provider text in ledger receipts.
  * Objective threshold or evaluation condition: serialized ledger records contain none of the synthetic input or output marker strings.
* Backward compatibility of result shape.
  * Objective threshold or evaluation condition: the existing 32 tests in test_ai_consumption_api and related legacy API tests still pass.

## Acceptance Criteria

* New tests fail before the source change where they exercise the defect and pass after.
* Existing targeted suites pass; lint and type checks on changed files pass.
* No network or model use; only the loopback spy.

## Implementation Context Record

| Context item | Current artifact or record |
| --- | --- |
| Plan | .copilot-tracking/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan.md |
| Phase details | .copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md |
| Latest critique | .copilot-tracking/reviews/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan-critique.md |
| Relevant research | .copilot-tracking/research/2026-11-12/legacy-ai-usage-attribution-432-1112-research.md |
| Changes-record role | .copilot-tracking/changes/2026-11-12/legacy-ai-usage-attribution-432-1112-changes.md is created by implementation |
| Planning execution and readiness | Planned; ready after critique disposition |
| Continuation context | Automatic parent continues to Implement |

## Sources

* .copilot-tracking/research/2026-11-12/legacy-ai-usage-attribution-432-1112-research.md: evidence C1-C7, W1 and the selected recommendation.
* src/api/tests/test_ai_consumption_api.py: fixture and loopback provider spy to extend.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Prove and fix the legacy usage join

* Intent: failing-first tests, then the one-statement-order fix.
* Dependencies: none

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add legacy join tests

* Requirement and evidence: C1, C5
* Expected result: tests for success, missing, malformed, failure, settlement failure, workflow-only.
* Detail section: P01-T01 in .copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reorder receipt usage after settlement

* Requirement and evidence: C1
* Expected result: settlement-failure test passes; no other behavior change.
* Detail section: P01-T02 in .copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md

<!-- rpi:phase id=P02 -->
### [x] P02: Correct documentation and validate

* Intent: remove the stale claim; run targeted validation.
* Dependencies: P01

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Correct the tokenomics sentence, index check and log

* Requirement and evidence: Contradictions section of the research
* Expected result: sentence corrected with source links; log entry appended.
* Detail section: P02-T01 in .copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Targeted validation

* Requirement and evidence: acceptance criteria
* Expected result: targeted unittest, ruff and mypy results recorded.
* Detail section: P02-T02 in .copilot-tracking/details/2026-11-12/legacy-ai-usage-attribution-432-1112-phase-details.md

## Dependencies

* Worktree src directories first on PYTHONPATH: installed distributions point elsewhere.

## Follow-Up Items

* Envelope-usage proof for `look_at` and priority; resident chat host join (owner-gated).

## Critique Disposition

One critique, verdict Revise, 0 Critical, 0 High, 3 Medium, 2 Low, all planner-owned and applied directly with no user decision. No second critique.

| Finding | Disposition |
| --- | --- |
| PC-001 `_request` is shared with `evidence()` | Applied: P02-T02 now names the other `_request` consumer suites |
| PC-002 case map missing | Applied: case table with coverage citations in P01-T01; all six cases kept because none is proven at legacy level |
| PC-003 settlement-failure mechanism | Applied: one-shot fault on `consumption.complete`, expected assertions and failing-first evidence specified |
| PC-004 docs bounded | Applied: one ASCII sentence, source-observed wording, one 2026-11-12 log entry, no tick |
| PC-005 ownership lock | Applied: all edits in the existing test module, at most six additions, removals none |

Critique artifact: .copilot-tracking/reviews/plans/2026-11-12/legacy-ai-usage-attribution-432-1112-plan-critique.md. Accepted residual risk: none.
