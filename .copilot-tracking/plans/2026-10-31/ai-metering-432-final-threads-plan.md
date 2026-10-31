---
title: AI metering final threads correction plan
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->
Task: issue-432-pr-602-final-threads.

## Executive Summary

Preserve bounded serving-model mismatch evidence through worker serialization
to quarantine and release suspension. Separate invalid report inputs from
backend financial holds. Deliver persistent manual fallbacks when post-call
financial links are held, without redispatch or weaker ledger bounds.

## User Decisions and Requirements

* Correct exactly the three unresolved PR #602 review threads, Refs #432.
* Pull topic first, merge main, preserve both log entries and main rubric.
* Full automatic RPI loop with original dated artifacts and independent gates.
* CI is publication gate; do not wait for complete local gate.
* Focused tests outside packages; ruff, format check, mypy and relevant tests
  from src/api with the requested PYTHONPATH; pip only, no secrets.
* Privacy-safe author/committer, supplied co-author trailer, ordinary push,
  thread replies and resolution; no force push or merge of PR.

## Goals

Prevent retry of model-mismatched tasks and prevent financial holds from
discarding usable manual routes or evaluation reports.

## Scope and Non-Goals

Provider, assistant completion, consumption publication helper, API report,
legacy text/document drafts, priority and chat delivery, external tests and
directly related guides/knowledge index/log. No schema or admission-limit change,
paid call, deployment, historical evidence edits or issue closure.

## Functional Requirements

* FR1: Closed model-mismatch outcome, bounded returned model, settled financial
  usage, no provider output, quarantined/non-retryable task, suspended release.
* FR2: Valid held reports return 200 with evaluation/live/registry and Unknown
  unavailable consumption; invalid parameters remain 400.
* FR3: Catch only DispatchHeld at financial publication; saved and returned
  fallback fields agree and attribution is explicitly unresolved/Unknown.
* FR4: Subsequent dispatch remains held; missing joins stay incomplete when
  read capacity recovers; unexpected output/persistence errors propagate.

## Non-Functional Requirements

Retain bounded privacy-safe evidence, immutable joins, authorization, citations,
continuity guards and existing package/test ownership.

## Acceptance Criteria

* AC1: Real loopback different/oversized/non-string model tests survive worker
  result serialization, settle usage, quarantine and suspend, never redispatch.
* AC2: HTTP capacity/evidence holds retain report sections and safe reason;
  invalid inputs still fail before reading unavailable ledger.
* AC3: Real 9,999-event admission reaches 10,001 and returns usable persisted
  fallback for legacy SQL/JSON, priority SQL/JSON and chat SQL/JSON. No duplicate
  calls, saves of AI shown as manual, or eligible financial links.
* AC4: Focused and related regression suites plus requested static checks pass.
* AC5: Independent critique and one Review preserved; implementation and dated
  original evidence committed/pushed and the three threads resolved.

## Test Ownership and Locked Candidate

Canonical tests: src/api/tests/test_ai_consumption_api.py. Removals: none.
Maximum additions: four test methods plus fixture controls/helpers in that
same external test file. Canonical source only, no generated runtime targets.
Semantic assertions cover bounded mismatch, HTTP output shape, exact event
threshold, persistent fallback consistency and subsequent dispatch refusal;
regression coverage retains provider failures, attribution repairs and review.

## Phase Checklist

<!-- P01 -->
### P01: Corrections

* [x] P01-T01: Bounded mismatch envelope and quarantine check.
* [x] P01-T02: Separate backend report holds from parameter validation.
* [x] P01-T03: Publication-only financial hold helper and consistent fallbacks.

<!-- P02 -->
### P02: Evidence and Publication

* [x] P02-T01: External focused tests and related guide/index/log updates.
* [x] P02-T02: Requested static checks/unit tests and one independent Review.
* [ ] P02-T03: Privacy-safe commit, non-force push, replies and resolutions.

## Critique Disposition

Single critique executed; original verdict Revise is preserved.

* PC-001 accepted: SQL chat finalization uses actual sequence and the message
  transaction's connection; JSON saves first then replaces only the actual
  just-saved message on hold. No predicted immutable joins.
* PC-002 accepted: model field is bounded consistently to 512 through shaping;
  oversized/non-string values become None, closed mismatch still quarantines.
* PC-003 accepted: ordinary push precedes exact-head required CI verification;
  thread resolution waits for successful applicable CI.
* PC-004 accepted insofar as current criteria must not be falsely closed:
  preserve original Review; no unresolved scoped finding may be claimed fixed
  or its thread resolved. No repeated Review or relabelled outcome.

Planning readiness: Ready after direct dispositions; no repeated critique.

## Follow-Up Items

Existing #432 live price/billing/approval gaps remain outside source closure.

## Handoff

Research: .copilot-tracking/research/2026-10-31/ai-metering-432-final-threads-research.md
Details: .copilot-tracking/details/2026-10-31/ai-metering-432-final-threads-phase-details.md
Changes: .copilot-tracking/changes/2026-10-31/ai-metering-432-final-threads-changes.md
Planning readiness: Ready; implementation P01 and P02-T01 complete.
P02-T02 complete: independent Review execution Complete, source Conformant,
no material findings. Original Review retained.
P02-T03 remains publication work after Review.
