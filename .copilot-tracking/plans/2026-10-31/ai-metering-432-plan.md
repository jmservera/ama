<!-- markdownlint-disable-file -->
# RPI Plan: AI consumption economics

## Task Metadata

* Task ID: 432
* Task slug: ai-metering-432
* Plan date: 2026-10-31
* Planning status: Ready after direct critique dispositions
* Details: .copilot-tracking/details/2026-10-31/ai-metering-432-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-31/ai-metering-432-plan-critique.md

## Executive Summary

Extend the existing append-only assistant ledger with attributable consumption,
owner-referenced financial admission and billing-led economics. Source-only
controls fail closed to the ordinary workflow when price or liability is unknown.
No deployment or paid exercise is authorised by this implementation.

### What You May Not Know

Later merged resident work already reserves currency conservatively. It still
does not establish accepted-proposal economics. OD-51, actual billing and a
held-out paid batch remain operational gaps, not engineering assumptions.

## User Decisions and Requirements

* Run Research, Plan, Implement, Review in order and commit dated evidence.
* Extend src ledger, never mvp, deployment, Azure, credentials or other worktrees.
* Use pip only; run the exact requested API unittest command and both Ruff checks.
* Exercise changed behaviour locally; Playwright is required for changed UI.
* Commit and gated publication on feat/ai-metering-432; Refs #432, not closure.

## Goals

* Bound dispatch and retain every financial uncertainty explicitly.
* Report billing cost per human-accepted proposal with quality, not token price alone.

## Scope and Non-Goals

Source ledger/model adapters/output-review links, API JSON economics and related
guides/pitch gap statements. No UI changes or new deployment settings are applied.
No live bill, price applicability, owner appointment, acceptance or spend is invented.

## Functional Requirements

* Versioned immutable price and spend records, metadata-only model call records.
* Atomic call/depth/token/currency/expiry admission; unknown price or liability denies
  further dispatch and records an alert owner/reference plus workflow-only route.
* Preserve provider input/output/cached tokens, failures, retries, configuration and
  prompt identifiers. Output and human review links are separate immutable events.
* Imported billing records are financial authority for an exact period/currency,
  with owner tolerance variance; projections are never labelled financial cost.
* Separate token billing from TCA components, accepted denominator, quality floors,
  overrides/reopened cases and capacity versus Finance-booked cash.
* Missing evidence returns Unknown and explicit coverage/operational gaps.

## Non-Functional Requirements

* Reuse Assistants.transaction and assistant_events; no parallel database.
* Do not emit case text, prompt text, output text, resident details or exception text.
* Conservative bounded input liability; image liability is unknown, never inferred
  from base64 length. Retain charged failures and reject uncertain usage.
* Existing release, role, continuity, hazard and consent checks remain authoritative.

## Acceptance Criteria

* Synthetic fan-out/loop stops at exact calls/depth limits with durable owned alert.
* Unknown cached usage/price, exhausted token/money budget and expiry deny dispatch.
* Exact decimal pricing and billing reconciliation, quality regression failure,
  zero accepted denominator Unknown and capacity-not-cash are tested.
* Real financial/batch criteria remain explicitly unmet until owner evidence exists.
* Existing API tests/Ruff and affected core tests/type checks pass, or blockers are
  preserved without false publication claims.

## Sources

Research .copilot-tracking/research/2026-10-31/ai-metering-432-research.md C4-C8,
issue #432 and merged #433/#480/#593.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Financial ledger and source wiring

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Extend immutable assistant events

Add typed core consumption module with bounded ledger reads, atomic admission,
price/spend/billing records, output/review links and quality-aware report.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Wire model calls and reports

Wire core Ai transport and assistant/legacy output links to ledger, retain cached
usage through shaping/chat, deny unmetered real Ai dispatch and expose manager
JSON report. Preserve independent resident SQL accounting and report its unjoined
coverage as explicitly unmet rather than claim a deployed financial migration.

<!-- rpi:phase id=P02 -->
### [x] P02: Evidence and validation

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Tests, guides and pitch

Core owns new ledger semantic tests, API owns composed fake-network/report tests.
Exact removals: none. Maximum additions: two test modules, 35 test methods.
Canonical targets: core ledger, Ai/assistant/ai_tasks/chat usage, API report.
Generated targets: none in source; external validation output only.
Preserve existing regression tests, test measurable limits and money shapes.
Run requested API discovery and Ruff, affected core lint/types/tests. Prepare
the full gate for the clean committed candidate after independent Review;
publication remains blocked until that separate gate passes and is verified.
No changed UI, so Playwright requirement is not applicable to new UI; browser gate
still executes existing real Chromium checks.

## Dependencies

P01-T02 depends on P01-T01; P02 depends on completed wiring.
Operational acceptance needs owner OD-51, actual prices/billing and paid batch.
Publication requires independent Review, clean committed candidate and full receipt.

## Critique Disposition

One critique executed, original verdict Revise retained. PC-001 through PC-008
are directly applicable and resolved by the contract addendum in phase details.
No second critique, live approval or scope expansion is inferred.

## Follow-Up Items

* Owner/Finance must supply OD-51, applicable prices, billing, quality floor and held-out spend authority.
* Resident procedure-to-ledger financial composition is separate source/deployment work; do not claim complete call coverage.

## Handoff

Changes: .copilot-tracking/changes/2026-10-31/ai-metering-432-changes.md.
Ready subject to one critique and explicit operational gaps.
