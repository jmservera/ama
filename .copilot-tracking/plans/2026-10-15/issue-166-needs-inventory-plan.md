---
title: Issue 166 needs inventory implementation plan
description: Bounded scenario integration and iteration review
ms.date: 2026-10-15
---

## Task Metadata

* Task ID: issue-166
* Task slug: issue-166-needs-inventory
* Planning status: Executed; one critique completed and directly resolved
* Plan date: 2026-10-15
* Phase details: .copilot-tracking/details/2026-10-15/issue-166-needs-inventory-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-15/issue-166-needs-inventory-plan-critique.md

## Executive Summary

Connect the existing thirteen-row inventory to a versioned, explicitly partial
constructed-scenario manifest. Record this iteration's engineering review,
correct stale coverage with migrated source evidence, and extend existing core
regression tooling. Do not build a runtime gate or claim full #103 delivery.
Owner ratification, volume/scope approvals and the absent historical matrix
remain unmet. The PR will reference, not close, #166.

## Sources

* .copilot-tracking/research/2026-10-15/issue-166-needs-inventory-research.md:
  executed research, Ready; C1-C8 and W1-W3.
* Issue #166, #103 owner comments; ADR 0006; parity matrix; PRs #296-#302.

## User Decisions and Requirements

* Complete Research, Plan, Implement and Review and commit evidence in the PR.
* Work only in the specified worktree and `feat/src-needs-inventory-166`;
  all new code/tests in src, no mvp code, reuse merged implementation.
* Preserve human approval, resident choice, no private data, Azure deployment
  boundary, portable SQL and workload dependency restrictions.
* Run local src suites, ruff, mypy and a synthetic local app check first;
  record commands/results, including missing dependencies and Docker limits.
* Use pip, not uv; do not touch .env, .vscode or tracking/github-issues.
* Update knowledge index/log, commit with the requested identity/trailer,
  push topic branch and open PR to main with Refs #166.
* Leave criteria requiring unavailable owner decisions/evidence unchecked.

## Goals

* Make inventory/scenario version linkage and iteration review inspectable.
* Preserve truthful coverage and open approval boundaries.

## Scope and Non-Goals

Inventory/provenance metadata, one scenario integration manifest, pack README,
knowledge index/log, core README, existing inventory tests and RPI artifacts.
No new generator, approval service, deployment, real inference, private data,
full #103 scripts/endpoints or application acceptance claim.

## Functional Requirements

* Reciprocal relative links bind manifest to the exact inventory version.
* Manifest declares active documentation/tooling slice, applicable inventory
  checks, deferred full #103 checks and unapproved owner review.
* Stable SN rows retain source, consumer, volume, proposed owner and coverage.
* Gate remains a pre-build issue/PR row citation plus owner scope/volume
  decision for partial/missing rows; tests do not pretend to prove chronology.

## Non-Functional Requirements

* No added runtime dependencies, SQL or workload imports.
* Existing core test file owns inventory integrity; additions are typed and
  explicitly linted/checked even though migrated code has broad exemptions.
* No private values, generated data or credentials enter git.

## Acceptance Criteria

* [x] Thirteen complete unique needs, evidence corrections and register links.
* [x] Build-start citation rule and owner decision requirement remain explicit.
* [x] Versioned manifest links inventory and records iteration engineering
  review; tests reject stale version/date, missing or duplicate reviewed rows,
  broken reciprocal paths and claimed owner approval.
* [x] Existing src suites (two private-reader exclusions), ruff, mypy and
  local synthetic app smoke recorded; Docker unavailable locally.
* [x] RPI artifacts, knowledge index/log and PR evidence committed in
  029f15f and published as PR #308 to main.
* [ ] Owner ratification of inventory/row owners and historical matrix
  reconciliation (unavailable; deliberately not part of local completion).

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reconcile inventory and scenario integration

Dependencies: completed research and one final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Update canonical metadata and documented gate

Update inventory to v1.2.0 and public provenance metadata only where migrated
sources demonstrate an existing fixture. Add at most one manifest JSON under
the pack; mark full profile/workflow evidence deferred to #103. Update pack
README, core README, reference index and append-only log.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Extend core regression tooling

Extend only `src/core/tests/test_needs_inventory.py`, with at most eight new
tests; exact removals: none. Validate reviewed SN set, reciprocal paths,
version/date, synthetic label and pending owner review. Include mutation
regressions for stale/missing metadata. No source module or new test file.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate, review and publish

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run local verification and record limits

Use worktree-local `.validation-166/` for the environment, logs and scratch;
set TMPDIR/TMP/TEMP and preflight `tempfile.gettempdir()`. Exclude the two
private-reader core cases named in details before execution; report them as
Not run rather than an unqualified full-suite pass.
Install editable src packages/dev tools with pip only after observed missing
module failures. Run all five src suites, per-project ruff/format/mypy,
explicit checks for changed tests, synthetic local HTTP app smoke and Docker
availability. No billable calls or deployment; actual AI/SQL/Azure application
acceptance stays Not run, not replaced by synthetic smoke.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Review once and publish

Run one post-implementation RPI Review, route residuals rather than loop.
Resolve `gh api user` again immediately before committing and derive the
privacy email from returned id/login; block publication if it conflicts with
the caller's requested identity. Commit complete artifacts with that email
for author and committer and the requested trailer,
push the assigned branch and open main PR with command results and Refs #166.
Leave merge to owner and checks to CI.

## Dependencies

* #290 and moves #296-#302 merged; no migration prerequisite remains.
* #103 full script/endpoint manifest evidence remains a separate follow-up.
* Owner review/volume decisions and 2026-10-14 matrix are unavailable.

## Critique Disposition

One independent critique executed, verdict Revise; compatible changes applied
directly without another critique.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Resolved in plan | P02-T01 and details name pre-execution exclusion of two private readers and qualified suite reporting |
| PC-002 | Resolved in plan | P02-T01 and details bind scratch, environment and smoke paths under the worktree |
| PC-003 | Resolved in plan | P02-T02 resolves current GitHub identity, derives email and verifies both commit identities |

## Follow-Up Items

* Owner: ratify inventory/owners, proposed volume/scope and gap mapping;
  reconcile the unavailable 2026-10-14 handoff.
* #103: replace explicit deferred profile/workflow script checks with actual
  version-linked fixtures, defaults, expected endpoints and execution evidence.

## Handoff

Implementation creates .copilot-tracking/changes/2026-10-15/issue-166-needs-inventory-changes.md.
All engineering plan tasks complete. One Review executed Complete, outcome
Residual work; first commit 029f15f published in PR #308 to main with Refs #166.
CI started; image/SQL Server outcomes not yet claimed. Automatic task is
completed in Follow-up, session remains running awaiting an owner-selected
follow-up. Human ratification and full #103 evidence remain open.
