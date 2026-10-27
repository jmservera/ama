---
title: Resident S16 dependency correction plan
description: Bounded correction for PR 454 review thread 4390263899
ms.date: 2026-10-27
---

Task: `jmservera/ama#454:discussion_r4390263899`
Slug: `resident-s16-dependency-454`

## Executive Summary

Make RB-18 follow RB-17 in the active backlog graph and slice description,
matching PR442-S16 -> S15. Clarify that ordering in the grouped proposal table.
The canonical PRD already states it correctly and remains unchanged. Preserve
independent urgent help, separate task-release authority and routine OFF.
Independent critique passed with no findings; documentary implementation and
validation are complete. Independent Review: Complete / Conformant, no findings.
Only the authorized publication sequence remains.
No runtime work is planned or claimed.

## User Decisions and Requirements

* Continue on the specified worktree/branch and PR 454; pull with rebase first.
* Split the combined graph row; make RB-18 depend on RB-17.
* Keep urgent help independent and OD-53 unnecessary for both items.
* Check the PRD and other backlog tables for consistency.
* Docs-only: Markdown/link review and git diff; no uv or secrets.
* Push without force, reply to and resolve the thread; do not merge.
* Use the requested Copilot co-author trailer.

## Sources

Research: `.copilot-tracking/research/2026-10-27/resident-s16-dependency-454-research.md`,
C1-C4 and W1. Details:
`.copilot-tracking/details/2026-10-27/resident-s16-dependency-454-phase-details.md`.

## Goals

Remove the graph's premature RB-18 completion path without changing authority.

## Scope and Non-Goals

Edit two active tracking planning views and create dated RPI evidence.
No application, PRD requirement/version, historical assessment, KB synthesis,
real service, activation or requirements-acceptance change.

## Functional Requirements

RB-17 retains RB-15, conditional RB-01 comparison freeze and external task
registration/evaluation/release prerequisites. RB-18 retains those and adds
RB-17. Both tables must agree. Independent urgent help is not conditional on
the model, RB-17 or task release. The proposal states S16 follows S13/S15
while retaining the R3/human route independently.

## Non-Functional Requirements

Plain Markdown, existing table structure and ASCII additions. Preserve
history, requirements IDs, current OFF policy and all live acceptance gates.
No tooling/dependency changes. Respect the owner's bounded validation request;
do not run a full runtime/SQL/image gate or claim a receipt.

## Acceptance Criteria

* Separate RB-17 and RB-18 dependency rows; only RB-18 adds RB-17.
* RB-18 slice wording explicitly repeats the edge and independent urgent help.
* Both RB items explicitly need no OD-53; comparison freeze remains conditional.
* PRD S16/S15 and grouped proposal reconciliation agree.
* No broken introduced relative links, malformed changed table rows or diff
  whitespace errors; independent Review retained without approval inflation.
* Commit, normal push, evidence reply and resolution only for the named thread.

## Validation Contract

Test ownership: author performs documentary assertions, Markdown/link review and
`git diff --check`; fresh independent reviewer checks meaning and changed files.
Exact removals: none. Maximum new runtime tests/tooling: zero.
Canonical targets: active backlog and proposal; generated targets: none.
Semantic coverage: ordering and release/help/OD-53 boundaries.
Regression coverage: RB-19/RB-20, protocol freeze and unsigned status unchanged.
No full local gate/receipt: explicit docs-only caller limit. Hosted CI and human
approvals remain separate, not passed by these checks.

## Phase Checklist

<!-- P01 -->
### P01: Correct and validate the documentary dependency

* [x] P01-T01: Split graph row and synchronize RB-18 slice narrative.
* [x] P01-T02: Clarify proposal ordering; verify PRD and preserve historical inputs.
* [x] P01-T03: Validate Markdown, links, exact dependency assertions and diff.

<!-- P02 -->
### P02: Independent Review and publication

* [x] P02-T01: Obtain one independent post-implementation Review and retain outcome.
* [ ] P02-T02: Commit evidence/correction, push normally, reply/resolve named thread.

## Critique Disposition

One independent final-candidate critique executed: Pass, no findings.
Evidence: `.copilot-tracking/reviews/plans/2026-10-27/resident-s16-dependency-454-critique.md`.
No revisions or user decisions required; critique will not be repeated.

## Follow-Up Items

Inherited requirements-quality FAIL, unsigned owner acceptance, architecture
registration and live gates remain outside this correction; none is closed here.

## Handoff

P01 and P02-T01 complete with no blockers or source divergence. Independent
Review retained at `.copilot-tracking/reviews/logs/2026-10-27/resident-s16-dependency-454-review.md`;
no findings or second Review. P02-T02 publication remains pending. Changes evidence:
`.copilot-tracking/changes/2026-10-27/resident-s16-dependency-454-changes.md`.
