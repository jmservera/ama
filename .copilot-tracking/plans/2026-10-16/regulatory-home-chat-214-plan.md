---
title: Home-specific cited chat implementation plan
description: Offline synthetic slice for issue 214
ms.date: 2026-10-16
---

Task: #214 / regulatory-home-chat-214. Full plan.

## Executive Summary

Add a separate, explicitly enabled synthetic regulatory panel over existing
isolated chat storage. The API alone retrieves law/cards and purpose-scoped
facts; agents render a fixed, extractive answer, never legal conclusions.
Retain deterministic alerts and provide a one-action human doubt inbox.

## User Decisions and Requirements

* Implement the bounded offline slice in src only; docs log/READMEs and requested
  RPI evidence are documentation exceptions. Never change legacy trees.
* ADR 0005 accepted for synthetic development only on 2026-10-16.
* Juan Manuel Servera is exercise Legal/Compliance/DPO owner; no other approvals.
* Preserve SQL portability, per-user isolation and existing chat/memory.
* Run deterministic tests, evaluation/card comparator, ruff, mypy, local app;
  push topic branch and open PR with Refs #214. Do not tick issue criteria.

## Goals

Source-grounded question-focused synthesis of one home's permitted facts,
honest refusals and an explicit human handoff.

## Scope and Non-Goals

Only src/core, src/agents, src/api runtime/tests/READMEs. No real inference,
deployment, licensed source fabrication, legal interpretation or live approval.
Source-monitor candidates are not approved retrieval material.

## Functional Requirements

Every factual fragment carries an immutable source/fact ID, status and dates.
Only active approved synthetic cards with eligible cited provisions support
answers. Unsupported/legal questions refuse. Conflicts show both and route.
Selected turns and complete citation envelopes persist in isolated chat.
Explicit doubt copies one turn to the named provisioned exercise owner's inbox.

## Non-Functional Requirements

No database or write capability in agents, no model tools, memory not evidence,
per-turn current role/case checks, bounded context and input, atomic handoff,
no rule-alert suppression, fail-closed synthetic opt-in.

## Acceptance Criteria

Audit all eight issue criteria with concrete tests and limits. Compare the
same questions against deterministic cards with provision links; label measured
offline lookup/context value separately from unmeasured AI/staff benefit.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Contracts and cited answers
* [x] P01-T01: API-owned retrieval/facts, extractive agents answer/refusal and storage.
<!-- rpi:phase id=P02 -->
### P02: Doubt and panel
* [x] P02-T01: Atomic explicit owner inbox handoff and case/home panel controls.
<!-- rpi:phase id=P03 -->
### P03: Evidence and delivery
* [x] P03-T01: Deterministic safety/isolation/evaluation and comparator tests.
* [x] P03-T02: Local validation, acceptance audit and documentation.

Delivery after the single Review: commit and push this independent topic branch,
open the requested PR against main, leave checks/merge and issue ticks to the
coordinator/owner. This is administration, not an unchecked source implementation task.

## Critique Disposition

One final-candidate critique executed; Revise findings PC-001 to PC-008 applied
directly in the details below. No divergent user decision needed. No removals. Test ownership: new core/agents/API
tests beside packages, maximum three new test modules plus one shared synthetic
fixture and one evaluation module/report. Canonical targets are source modules;
no generated runtime targets. Semantic guards, regression/isolation and local
HTTP checks are required, plus project lint/type checks.

## Follow-Up Items

Real-model and held-out evaluation, staff comprehension/net effort, actual
source/owner approval, operational privacy/retention, continuing-stock and Azure
acceptance are outside this expressly offline slice.
