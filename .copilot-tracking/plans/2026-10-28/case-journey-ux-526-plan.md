---
title: Case journey UX 526 implementation plan
description: Native journey, summary, retained tab panels and AI review consistency
ms.date: 2026-10-28
---

Task ID: 526. Slug: case-journey-ux-526. Mode: automatic.

## Executive Summary

Replace the employee case's long page with an evidence-based six-step journey,
six-value summary and nine retained tab panels. Keep safety visible above all
tabs, native/manual actions and existing human review authority. No API journey
or confidence extension is required. The single independent critique returned Revise. All five compatible findings
are directly resolved in the phase details below; the original verdict is
preserved. Planning is Ready for implementation without a second critique.

## User Decisions and Requirements

* Use issue #526 and the supplied design; include that uncommitted file in the
  first commit and add the knowledge-base index and append-only log entry.
* Use feat/case-journey-ux-526 in the current worktree; src/api web assets only,
  no framework swap, Azure, secrets, .env or private datasets.
* Keep slide order; Funding/Resident agreement require their recorded evidence.
* Preserve Fluent 2, WCAG baseline, plain language, non-colour signals,
  reduced motion and suggestion-not-instruction/human approval boundaries.
* Run unit, existing browser/axe, new stepper/tab/keyboard/200% checks and a
  real local case with constructed synthetic data.
* Use the shared heavy lock nonblocking, 60-second retries up to 40 minutes.
* Commit dated RPI evidence with Conventional Commit/trailer/privacy-safe
  identity; full local gate/receipt, non-force push and PR with Refs #526.
* Live verification and screen-reader acceptance remain pending the owner.

## Sources

Research: .copilot-tracking/research/2026-10-28/case-journey-ux-526-research.md
Specification: docs/reference/research/ux/employee-case-workspace-redesign.md

## Goals

Make current work, accountable owner, blockers and optional AI help findable
without losing forms, hiding safety or implying a new approval.

## Scope and Non-Goals

Employee case UI and tightly coupled tests/docs. Contractor projection and
server decision rights remain unchanged. No new framework, confidence score,
server journey, production activation or operational acceptance.

## Functional Requirements

* One stage mapping covers all 25 stages. Six real links, ordered states,
  explicit current/blocked/upcoming/done and evidence exceptions.
* Summary uses existing case/work fields and asynchronously updated assistant
  state/counts; no fabricated owner, funding mismatch or confidence.
* Nine ARIA manual-activation tabs retain DOM and drafts, use ?tab= in hash,
  preserve other query parameters, refresh/back and valid/unknown deep links.
* Every existing panel/action remains once; open safety is a single shared
  live panel above the journey with an in-tab pointer.
* Draft/proposal cards share warning, sources, missing-confidence wording,
  explicit review reason and linked errors; accept stays blocked for
  unverified/stale output and assistant verification remains person-specific.
* Chat has no recorded-review API. Present matching advisory card metadata
  and explicit existing request-proposal route; flag this gap, do not fake audit.

## Non-Functional Requirements

Existing tokens/native controls, visible keyboard focus, non-colour states,
no tab/stepper animation, 320px and 200% zoom reflow. Existing server
authorization/revision enforcement remains authoritative.

## Acceptance Criteria

Design criteria 1-8 are checked with new tests and actual browser checks;
record any unmet criterion or unavailable state explicitly. Automated results
do not establish human/screen-reader/live approval.

## Test Ownership and Change Budget

Parent owns journey derivation, summary/tabs integration, unit assertions and
existing browser selector adaptations. At most one new web module, one new
unit file and one new focused browser check; no removals. Existing test
behavioural guarantees stay; tab navigation and the intentionally changed AI
accessible names/disabled accept assertions may be adapted explicitly.
Canonical targets are src/api web sources and checks, not generated bundles.
Semantic coverage: all stages and blocker/evidence rules, ARIA/manual keys,
draft retention and exact human review boundaries. Regression coverage:
existing API unit, design-system/workbench/employee, assistant, challenge and
regulatory axe checks. Validation: full external exact-head gate after Review
and candidate commit, with original outcomes preserved.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Workspace structure and state
<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Derive journey and render summary/stepper
<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Retain and route tab panels and drafts

<!-- rpi:phase id=P02 -->
### [x] P02: AI presentation and review
<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Harmonize cards and accessible review controls

<!-- rpi:phase id=P03 -->
### [ ] P03: Evidence and validation
<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Add semantic/browser checks and update documentation
<!-- rpi:task id=P03-T02 -->
#### [ ] P03-T02: Run local checks, independent Review and publication gate

## Critique Disposition

Critique executed once: Complete / Revise, 1 High and 4 Medium. Original:
.copilot-tracking/reviews/plans/2026-10-28/case-journey-ux-526-plan-critique.md.

| Finding | Disposition | Resolving implementation contract |
| --- | --- | --- |
| PC-001 | Applied directly | Retain complete resident draft node/review closures; dirty-field identities and action-local clearing; discard on case/identity departure |
| PC-002 | Applied directly | Paginate case proposals; one count model and callback for summary/tab; explicit state table in details |
| PC-003 | Applied directly | Permit AI label selectors and disabled stale accept assertion changes; keep source verification and domain invariance assertions |
| PC-004 | Applied directly | Atomic optional module enhancement; headed stacked sections remain if module missing |
| PC-005 | Applied directly | Explicit geometry/state/axe/key/zoom matrix in details |

No finding needs a new owner decision. No critique rerun.

## Follow-Up Items

* Owner live deployment verification, screen-reader and staff usability.
* Chat turn recorded review is not supported by the existing API; evaluate
  a separate bounded extension rather than invent client-only acceptance.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-28/case-journey-ux-526-changes.md.
No implementation before critique disposition.

Current handoff: Implement blocked at P03-T02 by G-LOCK after 40 one-minute
nonblocking admission retries. Full API/browser/axe/actual-zoom validation,
the one independent Review and publication remain pending. Checked P01/P02
markers mean implemented, not accepted or fully browser-verified. No phase
advancement or publication gate has been bypassed.
