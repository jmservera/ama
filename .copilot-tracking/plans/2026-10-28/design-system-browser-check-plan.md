---
title: Design-system browser check fix plan
ms.date: 2026-10-28
---

## Task Metadata

Task: design-system-browser-check. Automatic full loop requested.

## Executive Summary

Correct the harness's obsolete loading-copy assumption introduced by #516.
Keep app wording and all lifecycle coverage; strengthen synthetic payload
rendering assertions. Local exact reproduction already matches both CI failures.

## Sources

Research: .copilot-tracking/research/2026-10-28/design-system-browser-check-research.md,
C1-C5. Baseline: origin/main 197e5e3c6d4f7cfb135c9a985af3f13e0f688ac4.

## User Decisions and Requirements

* Full RPI loop with brief artifacts; reproduce the actual synthetic server check.
* Minimal fix, no weakened check; focused regression and API/core existing suites.
* Pip/Chromium only, no uv, .env, private data or Docker builds; minimize heavy lock.
* Commit with requested Copilot trailer; push fix/design-system-browser-check;
  open a Refs-only PR, not closing referenced issues.

## Goals

Make current-main browser CI deterministic and preserve its briefing contract.

## Scope and Non-Goals

Only workbench browser harness, directly related API README, dependent public
scenario recipe hash with required knowledge-base index/log maintenance, and RPI evidence.
No app, store, workflow, timeout or dependency changes.

## Functional Requirements

Wait for visible current loading state inside the Today's briefing section.
Retain held-request counts, cancellation, stale-result rejection, cache reuse
and explicit workflow-mode failure/retry. Use complete scope/count fixtures.

## Non-Functional Requirements

No sleeps/retries/skips to conceal failure. No shared lock needed for direct
synthetic browser and unit checks. Apply the documented small-issue focused
validation tier; the owner explicitly excludes Docker builds, so do not claim
a full-matrix receipt or operational/human acceptance.

## Acceptance Criteria

Exact full design-system entry point passes twice; workbench regression checks
current loading disappearance and visible scope/counts. API/core discovery,
affected lint/format/types pass with all skips disclosed.
Independent one-pass critique and post-implementation Review are preserved.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct and validate harness

<!-- rpi:task id=P01-T01 -->
* [x] P01-T01: Update loading locator, fixtures and focused lifecycle assertions.
<!-- rpi:task id=P01-T02 -->
* [x] P01-T02: Document root cause; repeat browser entry point and run API/core suites.

<!-- rpi:phase id=P02 -->
### [ ] P02: Review and publish

<!-- rpi:task id=P02-T01 -->
* [ ] P02-T01: Independent Review; commit dated evidence, focused final-head checks.
<!-- rpi:task id=P02-T02 -->
* [ ] P02-T02: Push requested branch and open Refs-only PR; leave merge to owner.

## Test Ownership and Change Budget

Canonical test: src/api/checks/workbench_browser_check.py, executed by the
existing src-api CI entry point. Removals: none. Maximum additions: one
focused rendering assertion and one shared fixture mapping, no new test file.
Semantic coverage: full response shape and real visible loading.
Regression coverage: existing cancellation/cache/retry paths. Generated targets:
none. Validation evidence remains external logs plus dated changes/Review.

Implementation amendment: full core discovery demonstrated two stale-recipe-hash
errors after the harness changed. Refresh its existing scenario-manifest source
binding and required index/log only; no fixture/inventory/version/coverage change.
This tightly coupled integrity maintenance preserves the plan intent and needs
no new user decision or repeated critique.

## Critique Disposition

One final-candidate independent critique: Complete / Pass, no findings.
Evidence: .copilot-tracking/reviews/plans/2026-10-28/design-system-browser-check-plan-critique.md.
No significant/divergent decision or second critique is required.

## Follow-Up Items

* Optional later harness lint cleanup: isolated strict lint reproduces baseline
  I001 import order and B023 queue-callback diagnostics. Existing configured lint
  passes. Outside the briefing-copy regression; owner may select later cleanup.

## Handoff

Details: .copilot-tracking/details/2026-10-28/design-system-browser-check-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-28/design-system-browser-check-changes.md.
