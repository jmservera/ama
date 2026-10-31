---
title: Issue 531 PR 604 correction plan
description: Bounded evidence repairs, validation and authorized non-force publication
ms.date: 2026-10-31
---

Task ID: 531. Slug: employee-briefing-loading-531-pr604-corrections.
Status: P01 complete; one Complete / Conformant Review; P02 publication pending.

## Executive Summary

Main is merged as 6f3f0bf2. Repair 53 link destinations in six evidence
inventories and CLI option typography in phase details and related changes.
Preserve the implementation, original outcomes and both log histories.
Run relevant API tests and configured Ruff/format/mypy, independently review
once, commit/push PR #604 and reply/resolve all seven valid threads.
Hosted CI remains the gate per explicit caller direction; no full local wait.

## Sources

.copilot-tracking/research/2026-10-31/employee-briefing-loading-531-pr604-corrections-research.md,
C1-C6 and W1-W2. Original parent state and adverse evidence remain unchanged.

## User Decisions and Requirements

* Continue the named worktree/branch and existing open PR #604.
* Merge origin/main, take main's rubric score and retain both log entries.
* Read all seven unresolved threads; correct valid findings, with file-relative
  artifact destinations for link-only findings.
* Run relevant src/api tests, Ruff and mypy. Do not wait for the full local
  gate; CI is the gate for this publication.
* Commit with the requested Copilot trailer, use privacy-safe identity, push
  with git push -u origin HEAD, never force, pull --no-rebase first on rejection.
* After pushing, use addPullRequestReviewThreadReply then resolveReviewThread
  for each finding; keep Refs #531 and do not close the issue.

## Goals

Restore usable evidence navigation and executable option syntax without
changing application behavior or historical assurance claims.

## Scope and Non-Goals

Eight existing Markdown files: the seven thread targets and the closely related
publication-harness changes typo. New dated RPI artifacts only.
No runtime/test changes, generated source outputs, workflow/protection changes,
private datasets, live identity/model calls, deployment or issue closure.

## Functional Requirements

All 53 destinations resolve to their existing files from each containing
artifact. Correct --jobs 3 --lock-timeout 1800 syntax. Preserve visible link
labels, descriptions, earlier verdicts and failed gate evidence.

## Non-Functional Requirements

Keep changes surgical and provenance traceable; no secrets or force push.
Test ownership: existing API tests remain canonical, exact removals none,
maximum new tests zero because findings are documentation-only. A temporary
external link checker supplies semantic validation, not a new test framework.
Generated targets: none. Runtime regression coverage: existing employee units
and configured API tooling; link/CLI shape checked separately.

## Acceptance Criteria

* AC1: main ancestry, main rubric score and both log entries preserved.
* AC2: all seven thread findings corrected, including exactly 53 destinations.
* AC3: existing relevant API tests, Ruff/format and mypy execute successfully.
* AC4: one independent critique and one independent post-implementation Review
  retained with dispositions; original adverse evidence unchanged except links.
* AC5: commit with trailer, non-force push, remote head matches, seven replies
  precede seven resolutions, PR remains open with Refs #531.

## Phase Checklist

<!-- P01 -->
### P01: Repair and Validate

* [x] P01-T01: Correct 53 destinations and two CLI typography locations.
* [x] P01-T02: Verify exact shapes/preservation and run API validation.
* [x] P01-T03: Reconcile evidence and execute one independent Review.

<!-- P02 -->
### P02: Publish and Disposition

* [ ] P02-T01: Commit implementation/evidence and non-force push PR #604.
* [ ] P02-T02: Reply and resolve seven threads; record verified remote outcome.

Dependencies: P01-T02 follows T01, T03 follows T02; P02-T01 follows Review,
P02-T02 follows successful push. No complete local gate dependency under the
caller's explicit task-scoped override.

## Critique Disposition

One final-candidate critique executed Complete / Revise. PC-001 applied:
post-pull recovery rechecks correction identity and reruns affected validation;
accounting commits cannot silently change assessed inputs. PC-002 applied:
retain exact seven node IDs, require successful reply identity before resolving,
and verify per-node outcome. No significant/divergent decision and no second
critique. Evidence:
.copilot-tracking/reviews/plans/2026-10-31/employee-briefing-loading-531-pr604-corrections-plan-critique.md.

## Follow-Up Items

1. Live employee-site verification: issue AC7 remains unchecked; synthetic
   checks cannot prove deployed acceptance.
2. Existing specialist/manual accessibility acceptance: retain historical
   residuals, do not infer closure from repaired navigation.
3. Hosted CI and human approval: await actual results after publication;
   local checks are not hosted approval.

## Handoff

P01 complete with exact 53-link/CLI/historical-preservation checks,
145 API tests and configured Ruff/format/mypy passing. P01-T03 executed
one independent Complete / Conformant Review with no substantive findings;
P02 remains pending. Changes evidence:
.copilot-tracking/changes/2026-10-31/employee-briefing-loading-531-pr604-corrections-changes.md.
Review findings route later; do not repeat critique or Review.
