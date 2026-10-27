---
title: Resident assistant 469 implementation plan
description: Own-case advisory prototype plan
ms.date: 2026-10-27
---

Task: #469; parent #466. Automatic native RPI session. Research executed/Ready:
`.copilot-tracking/research/2026-10-27/resident-assistant-469-research.md`.

## Executive Summary

Ship a separate native advisory panel with three explicit question topics.
Default rules provider spends nothing. Optional Azure adapter cannot receive
resident facts/free text and cannot render generated content. Real activation
is a distinct owner decision. Unit, typing/lint and focused local Chromium
checks replace the long gate at the owner's explicit direction.

## User Decisions and Requirements

* Full research, plan, implement, review loop with dated genuine artifacts.
* Stack on feat/resident-interactive; Refs #469 only; no merge/force push.
* No Azure, real model calls, private data, secrets, .env or verifier file.
* USD 5 additional ceiling through 2026-10-31; owner decides on the design.
* Separate panel to avoid #467/#468; preserve MAX_MAPPINGS.
* Advisory only; own case, accessible native controls, human/manual routes.

## Goals

Answer current status, what documents can be established and basic form help
without inventing evidence or delegating actions.

## Scope and Non-Goals

Core typed response/provider boundary; API adapter and authenticated endpoint;
independent panel script; design note and tests. No generated prose, free-text
history, document upload/inventory changes, sibling panels, live activation,
new Azure resources or deployment.

## Functional Requirements

* Accept exactly one topic enum: status, documents or forms. Reject extra keys.
* Every request reuses fresh session-bound view authorization.
* Render only locally owned status/next-step text and fixed advice/source labels.
* Missing requested-document facts explicitly mean unknown, not none required.
* Provider protocol, deterministic fake, disabled Azure adapter with token and
  durable budget-reservation callbacks, fixed timeout/no retries/expiry.
* Unknown topic, malformed provider output and provider failure surface errors.

## Non-Functional Requirements

No PII/questions in model payload or logs. Model output must equal requested
topic enum, otherwise fail closed. No client case selector. No persistence of
questions. Fluent token styling, visible focus, live status, keyboard native
form and clear advisory/manual-help notice. No animation or framework changes.

## Acceptance Criteria

* Design note published before source implementation, marked owner decision.
* Two residents receive only their own status; attempted selectors fail.
* Revoked/expired/signed-out session cannot get advice; CSRF/origin enforced.
* Injection topic/response and synthetic secret sentinels never escape into
  model prompts/logs/responses. Disabled real adapter makes zero calls.
* Budget reservation failure/expiry fail before token/transport; failures
  explicit and no fallback disguised as model success.
* Core/API unit suites, changed-file ruff/mypy and local Playwright pass.

## Phase Checklist

<!-- P01 -->
### P01 - Design and contracts
* [x] P01-T01 Publish owner-decision design, typed topic/provider and rules advice.
<!-- P02 -->
### P02 - API and separate panel
* [x] P02-T01 Add disabled Azure adapter and authenticated own-view endpoint.
* [x] P02-T02 Add panel script/styles, loading/failure/recovery states.
<!-- P03 -->
### P03 - Verification and publication
* [x] P03-T01 Add core/API semantic and regression tests plus focused browser check.
* [x] P03-T02 Run targeted evidence and prepare independent Review/publication handoff.

## Locked Test Ownership and Targets

No removals. At most four new test/check files: core test_resident_assistant.py,
API test_resident_assistant_api.py, API test_resident_assistant_provider.py,
API checks/resident_assistant_browser_check.py. Existing showcase fixtures
reused. Canonical code under core/resident_assistant.py and
api/resident_demo/assistant.py; web/assistant.js is separate from demo.js
except one integration call. No generated checked-in bundles.
Semantic coverage: case binding, truthfulness, prompt/output constraints,
enablement/expiry/budget. Regression coverage: both affected full unit suites.

## Critique Disposition

Single independent critique executed; original verdict Revise preserved in
resident-assistant-469-critique.md.

* PC-001 rejected: conflicts with the owner's explicit current instruction to
  run targeted checks instead of the two-hour gate and open the stacked PR.
  The earlier standing gate is not claimed complete; this issue-specific
  publication direction is recorded as such, not as passing gate evidence.
* PC-002 accepted/applied: fixed enum-only ASCII prompt <=512 bytes, output
  max_tokens=16, budget reservation for that exact envelope before token/HTTP.
  Failed/ambiguous attempts retain reservation, no refund or retry. Verified
  tariff/model compatibility and durable USD4 shared accounting remain required
  for future host activation.

Readiness: Ready for local implementation. No unresolved critique decision.

## Follow-Up Items

Owner must select model/region/tariff and credential composition; durable global
USD budget control plus privacy/evaluation evidence required before activation.
Screen-reader/user acceptance remains distinct from Chromium checks.

## Handoff

Details: `.copilot-tracking/details/2026-10-27/resident-assistant-469-phase-details.md`.
Changes: `.copilot-tracking/changes/2026-10-27/resident-assistant-469-changes.md`.
Implementation and local checks complete. Parent now owns one independent
Review, followed by commit/push/stacked PR under the explicit owner direction.
Publication and hosted checks are not claimed complete by implementation.
