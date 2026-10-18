---
title: Issue 108 evaluation run accounting plan
description: Minimal per-recommendation evidence repair
ms.date: 2026-10-18
---

## Task Metadata

* Task ID: 108
* Task slug: issue-108-evaluation-runs
* Planning status: Complete; source candidate reviewed and PR #405 published
* Base: 69091f4149f2fd217fc33a8c965ebcb6d5064956
* Details: .copilot-tracking/details/2026-10-18/issue-108-evaluation-runs-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-18/issue-108-evaluation-runs-plan-critique.md

## Executive Summary

Keep every repeated priority recommendation's actual returned identity and
latencies. Derive run counts and model/prompt sets from that ordered evidence,
not the final scenario result. Correct `ai_runs` from AI-final scenarios to
AI-sourced recommendation runs and expose separate scenario/run denominators.
Preserve existing quality statistics, checks, review counts and not-evaluated
limitations. This is partial engineering delivery for #108, not issue acceptance.

### What You May Not Know

A template fallback can carry a model/deployment label from a rejected scripted
answer; that is not a successful AI output or an attested serving model version.
Fourteen priority recommendations currently report four AI runs, not eight.
Quality means are final-recommendation-per-scenario statistics; critical/citation
checks already cover all repetitions. The extra comparator is not a repeated
priority run. Reviewer actions are scripted and occur only on the final draft.

The original critique returned Revise (one Medium environmental-recipe finding).
Project-local TMPDIR isolation is adopted without changing source behavior.
No unresolved design decision blocks this bounded repair. Actual evaluation and
release prerequisites remain unmet outside scope.

## User Decisions and Requirements

* Full ordered Research, Plan with one independent critique, Implement and one
  original independent Review; preserve all original adverse evidence unchanged.
* Work only in this isolated branch/worktree at the supplied base; at most two
  corrective source cycles, no second original Review or unilateral integration.
* Keep returned source/model/prompt and latency per repetition; reconcile actual
  AI/template recommendation counts separately from scenarios, never provider calls.
* Preserve failure gates and quality scope unless tightly coupled correctness
  demands a change; do not multiply reviewer actions by repetition.
* Constructed offline scripted providers only, empty inherited endpoint/credential
  configuration, task-local stores. No private inputs, support, env files, service
  SQL, Azure, inference, deployment, IAM, spend or new MVP code.
* Normal publication to main with Refs #108, no whole-issue closure, checkbox or
  board writes; stop for coordinator independent exact-head review.

## Goals

Restore evidence-faithful run identity and count reconciliation without changing
model behavior, task eligibility, ranking or evaluation policy.

## Scope and Non-Goals

In scope: ai_eval.py, its focused existing tests, narrow agents README contract,
one direct API pass-through assertion if needed, and required RPI evidence.
Non-goals: new frameworks/datasets/tasks, chat/regulatory grading, provider-call/
token budget accounting, actual held-out/human/model evaluation or model selection.
No KB material changes are needed; upstream KB and src controls remain intact.

## Functional Requirements

* Scenario `run_results` retains ordered `run` (one-based ordinal),
  `recommendation_id`, `source`, `model`, `prompt_version`, `latency_ms`
  (harness wall time) and `model_latency_ms` (returned recommendation measurement).
  Copy values exactly, including null model identity.
* Preserve legacy `source`, `model`, `prompt_version`, overlap, Spearman and recall
  as final-result views, and legacy latency arrays/variation. Disclose quality
  scope in JSON and README.
* Summary `recommendation_runs` equals all priority repetition records;
  `ai_runs` and `template_runs` count actual returned sources. `priority_scenarios`
  counts measured priority scenarios, while `ai_scenarios`/`template_scenarios`
  count scenarios containing those sources (non-exclusive for mixed scenarios).
  Model/prompt sets use every run, filtering unknown null identities only from
  the aggregate sets. No fabricated serving version.
* Review stays once per scenario with actual scripted owner and recommendation
  binding. Legacy summary counts/reasons remain compatible.
* Console exposes explicit run/scenario counts; API remains a pass-through.

## Non-Functional Requirements

No network or private dataset use in validation. No dependency additions or
framework/schema layer. Keep existing migration Ruff/mypy exemptions visible;
do not represent their pass as strict checking of exempt harness code.
All task artifacts delivered with source; original critique/Review hashes retained.
All subsequent isolated application/test commands explicitly set TMPDIR to
the pre-created worktree-local `.copilot-tracking/.issue-108-tmp`, and verify
`tempfile.gettempdir()` there. Scratch is removed before delivery.

## Acceptance Criteria

* Existing five-output scenario yields five AI runs, five latency/identity rows,
  one scripted edit, distinct recommendation IDs and unchanged quality values.
* Valid/fallback outputs in both orders yield one AI and one template result,
  two runs and one scenario/review; no identity lost when last model is null.
* Template-only repetitions reconcile without inventing model identity.
* Existing full golden report reconciles 14 recommendations, eight AI and six
  template, ten measured priority scenarios, eleven total results including
  text-task checks, and ten scripted priority reviewer actions.
* Early critical/citation/invariant failures still fail the scenario/run even
  when a later result is valid; no actual-model/human/benefit claim is promoted.
* Focused tests fail before production repair and pass after; agents discovery,
  configured Ruff/format/mypy, direct API negative controls/pass-through and offline
  JSON harness results recorded with commands, errors, limits and hashes.

## Sources

Research C1-C7 in .copilot-tracking/research/2026-10-18/issue-108-evaluation-runs-research.md.
Issue #108 and PRD RAI/model evaluation/CON-009 contract govern claim boundaries.
No explicit issue dependency; #104 is hierarchy only.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Lock regression evidence

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add focused behavioral regressions and record red baseline

Use existing test_ai_eval.py ownership; compare actual returned metadata with
run records, mixed source orders and unknown model, all-run critical gate and
scripted reviewer binding. Details P01-T01.

<!-- rpi:phase id=P02 -->
### [x] P02: Repair report evidence and direct contract documentation

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add per-run records and reconcile summary counts/sets

Depends on P01. Keep final-only quality fields and failure gates intact.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Document compatibility and direct endpoint contract

Depends on P02-T01. Narrow README paragraph and API assertion only.

<!-- rpi:phase id=P03 -->
### [x] P03: Validate, independently review and publish bounded delivery

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Run local checks and reconcile handoff

Depends on P02. Record command/output evidence and explicit N/A/not-run boundaries.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: One original independent Review and publication

Depends on P03-T01. Preserve immutable original review; separate receipts for
any bounded corrections, maximum two source correction cycles. Publish branch
and PR, then wait for coordinator exact-head review. No second original Review.

## Test Ownership and Budget

Canonical focused owner: src/agents/tests/test_ai_eval.py. Direct consumer:
src/api/tests/test_ai_tasks.py. Removals: none. Maximum additions: seven focused
test methods plus one direct consumer assertion block. No generated test/dataset
targets. Semantic regression coverage: real scripted Store paths with mixed
outputs and mutated returned metadata; failure gate negative controls.
Existing golden JSON remains byte-identical. No tests for unrelated constants.

## Dependencies

P01 -> P02 -> P03 only. Source packages/dev tools installed with pip after actual
ModuleNotFoundError. No actual-model/human prerequisite is imposed on offline
accounting; those remain required for later exercises and issue acceptance.

## Critique Disposition

Exactly one independent critique executed, original verdict Revise, Medium PC-001.
Original SHA-256: b6117e40523ce84c5c163d913263224abda62b8d40530e09fd6de4f5b33f1397.

| Finding | Owner and disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Planner, accepted direct environmental hardening | Non-Functional Requirements and details P03-T01 require explicit project-local TMPDIR and verification before subsequent application runs |

The critique's asserted universal prohibition on external temp directories is
not independently established by the caller/repository instructions. Its useful
task-local isolation recommendation is adopted; earlier baseline evidence is
retained honestly as default-temp execution, not relabelled project-local.
No source correction or second critique is needed.

## Follow-Up Items

* Coordinator independent complete exact-head review and any main integration
  authorization are separate acceptance work, not unilateral source changes.
* RV-001 Low: existing migration-quality owner may separately address inherited
  format/type exclusions; publication retains the limitation, not strict coverage.
* Issue #108 actual-model/held-out/human/Finance/region/quota/serving evidence
  remains unmet; authorized future exercise owner supplies those prerequisites.

## Handoff

Changes target: .copilot-tracking/changes/2026-10-18/issue-108-evaluation-runs-changes.md.
P01-P03 and every task complete. Original independent Review executed once on
source candidate a39ebe9755d07df23730ee81256c0c792fc0ff51: Complete, Conformant
with justified divergence; RV-001 Low inherited coverage residual, no introduced
defects. Original Review is immutable. Normal branch publication and main PR
https://github.com/jmservera/ama/pull/405 authorized and executed.
Delivery evidence commit adds no source changes; its exact hash is pinned in PR
metadata and the final handoff. No source correction cycle or second Review.
Stop for coordinator independent complete exact-head review. No main integration,
merge, issue closure, human approval or actual-model acceptance inferred.
