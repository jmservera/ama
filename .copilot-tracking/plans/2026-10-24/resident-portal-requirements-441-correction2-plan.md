---
title: Resident manifest verification correction plan
description: Second bounded validator correction with no heavy gate or publication
ms.date: 2026-10-24
---

Task jmservera/ama#441 / resident-portal-requirements-441.
Native59f31558-980b-475c-b2e2-3b8d68279ed9. Plan Complete/Ready.

## Executive Summary

Research genuinely reproduced actual-main acceptance of a reversible source
mapping inconsistent with the pinned ADR manifest. Normalize ADR list and PRD
dictionary explicitly, validate inventory records, reject mismatches/unknown
omissions and add focused regressions. Preserve score-only bot by verified
fast-forward, never hand-edit scores. No product/custody bytes change.
One independent pre-implementation critique, then correction, focused checks,
one Review, commit and session handoff. No heavy gate or remote operation.

## User Decisions and Requirements

* Same native worktree/session, ordered prospective RPI, no fabricated phases
  or rewriting adverse evidence; second validator correction retry budget.
* New Medium4365410759 must be reproduced then corrected minimally.
* Preserve actual bot816eea7a direct child off902 via clean fast-forward.
* Current unsigned PRD FAIL/Validate BLOCKED/seven findings, 30Notrun,
  NFR precedence, OD52-55/OQ28-31, routineOFF, id:null/deferred ADR, A5/B6 OPEN
  and twelve FAILED source whitespace diagnostics remain.
* Stop after focused validation, Review and correction commit. No heavy gate,
  push/PR edits/merge/closure/board/acceptance ticks/cloud/paid/scorer action.

## Goals

Every inventoried selected ADR/PRD source is actually checked against its
manifest, and malformed inventories cannot silently evade verification.

## Scope and Non-Goals

Edit only existing validate-refinement.py and test_validate_refinement.py in
the2026-10-23issue441package, plus dated2026-10-24correction2RPI artifacts.
Bot score change is inherited by fast-forward only. No canonical docs,
archived source/manifest, source-to-integrated mapping or generated score edits.
No new package/dependency or broad app suite.

## Functional Requirements

* Normalize nonempty path-keyed dictionaries and lists of path objects.
* Explicit ValueError for unsupported/empty inventory, bad entry/path/hash/
  byte-size shape or duplicate list paths. Never default missing fields.
* Verify selected source SHA and byte size against indexed entry, retaining
  PRD dictionary behavior. Duplicate archive copies are valid selected records.
* Missing selected entries fail except exact self manifests and original
  pre-reconciliation ADR capstone-review-boundary.md, explicitly documented.
  If an exception path is inventoried, compare it normally; never bypass it.
* Keep fixed candidate/manifest pins and reverse/forward mapping checks.

## Non-Functional Requirements

Reuse task-local helpers/tests; explicit contextual errors, no catches/fallbacks.
No immutable source modification. PYTHONDONTWRITEBYTECODE=1 avoids ignored
scratch; logs/reports external, selected focused report may be copied into
existing task package with correction2-specific name, never overwrite history.

## Acceptance Criteria

* AC1: Actual pre-edit main reproduction records source mismatch accepted.
* AC2: Plan/details and one independent critique precede source edits and botFF.
* AC3: Actual-main reproduction rejects afterward at manifest comparison;
  same internally consistent mapping, no unrelated downstream proxy failure.
* AC4: Existing ten tests pass plus bounded new production-helper and
  actual-main regression; positive real-shaped ADR/PRD and malformed/duplicate/
  missing/hash/byte mismatch cases prove boundaries.
* AC5: Both existing focused validators pass actual candidate; Markdown/link/
  hash checks on new artifacts and unchanged product/evidence preservation.
* AC6: One Review records exact scope/outcome/limits; commit with safe identity/
  trailer, clean head/tree/base/actual remote lease handoff. No heavy gate.
* AC7: If still defective after Review, stop/report; no new correction cycle.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### P01 - Correcting manifest enforcement

* [x] P01-T01: Guard unchanged refs/known run-owned tracking and fast-forward
  exact verified score-only bot without moving/discarding other work.
* [x] P01-T02: Normalize and validate actual manifest contracts, enforce records.
* [x] P01-T03: Add bounded regressions, run original reproduction and both
  validators, preserve source/product/history and actual diagnostic boundaries.

<!-- rpi:phase id=P02 -->
### P02 - Reviewing and handing off

* [ ] P02-T01: Reconcile implementation evidence and run one genuine Review.
* [ ] P02-T02: Commit only issue corrections/evidence; clean exact handoff
  external after commit, no later source changes or publication.

## Locked Ownership and Validation

Parent owns implementation, tests and Review. Independent fresh critic writes
only critique. Removals:none; additions at most five new unittest methods in
existing test_validate_refinement.py (subtests for related shape boundaries).
No production app tests added, no broad suite/heavy gate. Semantic regression
must exercise the actual main caller with the research reversible mapping
injection and actual pinned ADR manifest, not only normalization in isolation.
Unit boundary tests call the same production verification helper.
Primary source targets locked above. Reports only external or correction2-named
in existing issue package, no regenerated original report/score.

## Critique Disposition

One fresh independent final-candidate critique executed Complete / Pass,
zero actionable PC findings. Writer changed only critique artifact, confirmed
actual source shapes/caller-test plan and bounded exceptions. No material
revision or user decision needed. Artifact:
.copilot-tracking/reviews/plans/2026-10-24/resident-portal-requirements-441-correction2-plan-critique.md.
Source and bot history remain unmodified at this gate; implementation ready.

## Follow-Up Items

* Coordinator later admits one exact-clean-head/current-base full gate and
  independent publication assessment. Historical67057df2/97filef902 evidence
  does not cover new candidate; no local gate authorized in this correction.
* Requirements owner retains seven quality findings/unsigned approval gates,
  NFR precedence and all30unrun criteria; no quality waiver.
* Supported native registration and live control owners remain separate.
* A5/B6 scorer citations OPEN; coordinator/supported scorer route, not manual
  generated edits or paid rescore.

## Handoff

Details: .copilot-tracking/details/2026-10-24/resident-portal-requirements-441-correction2-phase-details.md
Changes after critique: .copilot-tracking/changes/2026-10-24/resident-portal-requirements-441-correction2-changes.md
Review: .copilot-tracking/reviews/logs/2026-10-24/resident-portal-requirements-441-correction2-review.md
Parent proceeds only under this owner's explicit ordered continuation.

## Implementation Readiness Reconciliation

P01 Complete. Exactly two task-local Python files changed; five added methods,
ten retained. Both validators and15methods pass. Identical actual-main
reproduction now fails specifically at ADR source hash mismatch. Product,
immutable evidence, correction1 and bot bytes unchanged. New-artifact lint
initially flagged long research/critique tables and bare URL; corrected only
formatting/navigation before Review, original critic output retained externally.
Critic Pass/zero findings/prose unchanged. No material plan divergence.
Full-branch whitespace is FAILED52historical diagnostics, including the12
refinement diagnostics, byte-identical to bot-entry check. Correction-only
diff check passes. No waiver or all-branch PASS claim. P02 Review then commit/
handoff remain; commit cannot be preclaimed in its own source record.
