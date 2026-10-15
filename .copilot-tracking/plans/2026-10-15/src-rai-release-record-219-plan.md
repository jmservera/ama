---
title: Plan - task-bound RAI release records
description: Issue 219 implementation and evidence boundary
ms.date: 2026-10-15
---

Task ID: 219. Slug: src-rai-release-record-219. Status: loop completed; Review Not accepted.

## Executive Summary

Extend the merged SQL-owned release gate rather than add a parallel registry.
Require an explicit versioned impact/use/evaluation contract, bind activations
to the selected record and reject material changes. Close JSON's configured-AI
bypass. Preserve proposal-only/human/consent boundaries. Live authority,
provider attestation, representative evaluations and Azure execution are not
established by synthetic local evidence.

## User Decisions and Requirements

* Full Research, Plan, Implement, Review loop; commit its artifacts.
* Work only on feat/src-rai-release-record-219 in the supplied worktree.
* Follow #219 criteria, post-pivot decisions, ADR 0006 and merged registry.
* New code/tests in src; core imports no workload, no agents SQL/blob clients.
* SQL Server-portable additions; pip only; local suites, ruff, mypy and app run.
* Leave unsupported criteria unticked; record commands/results and limitations.
* Update reference index/log; privacy-safe Conventional Commit and trailer;
  push topic and open main PR with Refs #219.
* Do not touch .env, .vscode, issue mirrors or add mvp code.

## Sources

.copilot-tracking/research/2026-10-15/src-rai-release-record-219-research.md
(C3-C7, W1); issue #219; ADR 0006 and parity matrix.

## Goals

One shared denial/matching implementation and auditable task-to-record binding.

## Scope and Non-Goals

Core release/registry/client/store contracts, test helpers, owning src tests
and READMEs, reference index/log. No deployment, legal opinion, fabricated
approval, private-data access or #144 queue work. Existing SQLite-specific
schema/setup is not rewritten; new SQL uses portable SELECT/INSERT/UPDATE.

## Functional Requirements

* Require release version, intended/prohibited uses, stakeholders, accountable
  owner, impact, residual-risk decision, approved evidence references and
  change triggers; explicit exercise versus actual evidence.
* Bind use/registry, model, prompt, policy, data, permissions and evaluation
  protocol versions; reject absent/old/malformed/expired records.
* Select the exact matching release, persist its ID/version/digest on
  assistant claims and legacy outputs; recheck it before completion/reliance.
* Supersede prior records for the same task across endpoints/deployments.
  A record approves one deployment; switching a task's fast/strong route requires
  renewed approval. No historical approval revives on routing rollback. Keep history.
* Canonical retained prompt templates own actual system/instruction text and
  citation rules; request construction, release binding and output use their hash.
* Cover cached briefings, ordinary/document reviews and separate priority
  views/reviews. Replacement during a call invalidates that invocation.
* Release-aware activation IDs deduplicate within a release; renewal creates
  fresh work while preserving the old proposal.
* Visible denial carries missing evidence, owner/manual route and is persisted.
* JSON cannot authorize configured inference without a durable release store.

## Non-Functional Requirements

No new dependency or image privileges. New contract logic and tests pass strict
ruff/mypy without broadening migrated-module exemptions. Runtime data remains
outside src. Existing manual, resident consent and safety routes stay intact.

## Acceptance Criteria

* [x] Absent/expired/version-mismatched registered tasks make zero provider calls (synthetic local controls).
* [x] Denial exposes missing evidence, owner/manual route and persists.
* [ ] Matching exercise record consistently enables bounded unreviewed proposals (RV-003 cached denial recovery remains).
* [ ] Material contract/evaluation/permission changes fully invalidate dependent work (RV-001/RV-002 reliance defects).
* [x] OQ-017 holders explicitly stated unavailable, not named as approved.
* [x] Local suites/tools/app evidence recorded; unrun real-service/human gates open.
* [ ] Real approved exercise evaluation and live model/provider evidence.
* [ ] Named OQ-017 holders/delegations, competent review and direct human acceptance.
* [ ] Azure deployment and authoritative serving-version attestation.

## Phase Checklist

<!-- P01 -->
### P01 - Extend and wire the release contract

* [x] P01-T01 - Validate release contract and unify matching/version bindings.
* [x] P01-T02 - Bind SQL activation/completion/reliance and legacy results;
  deny configured JSON inference.

<!-- P02 -->
### P02 - Evidence and documentation

* [x] P02-T01 - Add semantic negative/positive tests; run component suites,
  lint/types, synthetic local HTTP exercise and Docker attempt.
* [x] P02-T02 - Update documentation/index/log; reconcile artifacts for the single Review.

## Test Ownership and Change Budget

Canonical behavior: core assistant_release/ai_registry/Ai/store contracts.
Generated targets: none. Removals: none. Maximum additions: two production
modules (only if a typed contract helper is clearer), three test modules and
one local HTTP-check script, plus the explicitly requested RPI artifacts.
Semantic release-contract tests belong in core/tests; HTTP/assistant integration
in api/tests. Update core/tests/release_support fixtures; unrelated legacy-output
tests may explicitly install nonbillable test-only authorization, never production
bypass. Regression coverage: all five src suites, dependency rules, ruff/mypy.
Do not change golden eval content or pretend scripted inference is real AI.

## Critique Disposition

One independent critique executed, verdict Revise. All findings applied directly;
no owner decision or repeat critique needed:

| Finding | Disposition and resolving work |
| --- | --- |
| PC-001 | Task-wide supersession and rollback denial, P01-T01/T02 |
| PC-002 | Canonical actual prompt templates/citation contract, P01-T01 |
| PC-003 | Explicit cached read, ordinary/document and priority review coverage, P01-T02 |
| PC-004 | Release-aware activation identity and fresh renewal, P01-T02 |
| PC-005 | New unexempt typed rai_release helper and ai_prompts module; project strict mypy includes both; migrated glue remains exempt |

## Follow-Up Items

The one Review executed Complete with outcome Not accepted. Route RV-001
(missing-reference reliance), RV-002 (historical-route reliance) and RV-003
(cached denial recovery) to later rpi-implement, ranked in that order.
No second Review or return to Implement occurs inside this completed loop.

OQ-017 named release/risk/suspend/restart holders and meaningful oversight;
qualified review and real approved evaluation/serving attestation; Azure/SQL
Server CI evidence. These are not fabricated engineering completion.

## Handoff

Details: .copilot-tracking/details/2026-10-15/src-rai-release-record-219-phase-details.md.
Changes target: .copilot-tracking/changes/2026-10-15/src-rai-release-record-219-changes.md.
P01/P02 execution complete; Review Complete / Not accepted. Publish a draft PR
with Refs #219 and the review artifact. Engineering acceptance is blocked by
RV-001 through RV-003. No live approval is inferred; unmet evidence stays in
Follow-Up Items and unchecked acceptance gates.
