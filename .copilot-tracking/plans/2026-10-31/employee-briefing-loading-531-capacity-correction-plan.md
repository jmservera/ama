---
title: Employee briefing validation capacity correction plan
description: Current-main integration, executed assurance and gated PR publication
ms.date: 2026-10-31
---

## Task Metadata

Task 531 / employee-briefing-loading-531-capacity-correction; automatic child of
employee-briefing-loading-531. Research and details share this dated slug.

## Executive Summary

Main integration is committed without rewriting history. Execute the existing
API and local Playwright/axe assurance rather than recycle historical passes.
Keep the original blocked Review intact and add one correction Review. Publish
only after a clean committed full gate and current-base exact-head assessment.
Whole issue acceptance remains unmet for live AC7 and the specialist note.

## User Decisions and Requirements

* Continue in feat/employee-briefing-loading-531; merge latest main first.
* Main's rubric wins; preserve both log entries; hashes change only with workflows.
* Heavy execution waits 1800 seconds on the shared lock, retry once on timeout.
* Run API unit discovery, Ruff check, Ruff format check and changed-UI Playwright.
* Commit requested Copilot trailer, push -u origin HEAD without force, PR to main.
* Use Refs #531 unless every criterion has reviewed proof; pip only, no Azure/secrets.

## Sources

Research: .copilot-tracking/research/2026-10-31/employee-briefing-loading-531-capacity-correction-research.md.
Original changes and Review use employee-briefing-loading-531 dated 2026-10-31.
Base 1330869ea675ff019958846330108b4f45e163ce; merge 18c1531f.

## Goals

Resolve missing execution and ancestry with fresh, retained evidence; publish a
reviewable correction without overstating live or human acceptance.

## Scope and Non-Goals

Existing browser scenario and directly related guide/evidence only. No test
removals; no workflow, runtime UI, authority, schema or dependency changes planned.
No live verification or new UX discovery. No other worktree/process interference.

## Functional Requirements

Preserve and execute every existing loading/briefing scenario and three actual
accept/edit/reject round trips with export persistence and refusal checks.

## Non-Functional Requirements

No unlocked heavy fallback, hidden failures or success-shaped skip. External
logs/caches/receipt; bytecode disabled. Full gate already self-locks: use its
--lock-timeout 1800, not nested flock. Retry once only for capacity timeout, not
for assertion failures. Required prerequisites remain fail-closed.

## Acceptance Criteria

* Main ancestry, main rubric/hash identities and both log histories verified.
* Fresh API/Ruff results and complete pinned-axe browser results retained.
* All three same-ID review outcomes pass and retain unchanged case projections.
* Original correction critique/Review and truthful changes record committed.
* Full receipt passes at exact clean HEAD/current main, verified before push;
  independent exact-head assessment; PR references issue and unmet criteria.

## Test Ownership and Change Budget

Parent owns commands and evidence; existing runner owns all UI semantics.
Exact removals none. Maximum new scenario functions zero unless a demonstrated
failure requires a coupled correction; preserve original three-outcome function.
Canonical targets: existing loading_briefing_browser_check.py and API guide.
Generated targets: fresh external logs/JSON/screenshots, not Git source.
Semantic evidence is real UI/API/export execution; lint is only regression hygiene.
Full gate is additional publication evidence, not a substitute for the focused runner.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01: Execute and reconcile assurance

* [x] P01-T01: Merge latest main with required preservation.
* [ ] P01-T02: Execute requested API/Ruff and serialized pinned-axe browser.
* [ ] P01-T03: Reconcile changes/details and obtain original correction Review.

<!-- rpi:phase id=P02 -->
### P02: Publish exact committed candidate

* [ ] P02-T01: Commit implementation/evidence with privacy-safe identity/trailer.
* [ ] P02-T02: Full gate, current-base receipt verification, independent exact-head assessment.
* [ ] P02-T03: Push -u origin HEAD and open PR to main using Refs #531.

## Critique Disposition

Exactly one critique executed Complete / Revise. PC-001 (Medium) is applied
directly: mandatory external TemporaryDirectory override and narrowly matched
owned-server -B subprocess invocation, followed by ignored-input inventory.
Original verdict preserved; no divergent decision and no repeat critique.
Final planning readiness Ready.

## Follow-Up Items

* Prior RV-002: discovery-backed UX specialist note remains absent.
* Prior RV-003 / AC7: separately authorized live employee-site verification.
* Staff, screen-reader/voice-control and full Fluent acceptance remain separate.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-31/employee-briefing-loading-531-capacity-correction-changes.md.
Ready candidate for critique; no implementation redesign. Full gate tool identity
and no ignored inputs are publication requirements after all evidence commits.
