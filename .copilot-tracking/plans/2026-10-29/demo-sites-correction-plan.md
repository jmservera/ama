---
title: Demo sites correction plan
description: Bounded local evidence, validation and blocked live execution handoff
ms.date: 2026-10-29
---

Task ID: eb7ee1f8-42fd-48a8-9c24-a1cbebb99513.
Task slug: demo-sites-correction.
Source baseline: 77c87e0d76b827544fde9b2f2ce7dfbd9d879232.

## Executive Summary

Complete the ordered local RPI loop and commit its original evidence, without
claiming a deployment. Live actions are blocked by the explicit no-az rule.
Preserve the owner's earlier approvals in a precise coordinator handoff.
Do not silently integrate unmerged #521 or consume another revision.

## User Decisions and Requirements

* Owner reports explicit live approvals at 2026-10-29 09:36Z for the SQL view,
  one additional resident forward revision, employee redeployment and #521
  authority/credential/SQL renewal after both sites are healthy.
* Final correction-round instructions prohibit az, gh, push and force-push.
  Pull with rebase first, commit on this branch with Conventional Commit
  messages and the exact Copilot trailer; no closing keywords.
* Preserve env entries/secretrefs, identity, registry, ingress, min replicas 0,
  eight Manual jobs, rollback revision and live ACR digests. No secret values,
  `.env`, private data, networking/RBAC/server changes or image deletions.
* Run core/API mypy, Ruff lint/format, unit and relevant browser checks with
  this worktree's src packages. Use nonblocking heavy admission; if busy,
  run targeted tests and explicitly record the blocked suites.

## Goals

Deliver an honest local correction record and enough exact prerequisites for
the coordinator to avoid repeating the failed image-only resident rollout.

## Scope and Non-Goals

Only new dated tracking evidence is edited. No production/source, authority
branch, pinned synthetic data, runbook, live app, SQL or cloud changes.
Live smoke tests are limited to anonymous public status codes/body hashes.
Local synthetic browser harnesses may use their invented fixture credentials;
no live sign-in or model call is permitted.

## Functional Requirements

Record before/after revisions and digests as unknown for this round unless
freshly observed. Label the historical evidence explicitly. Preserve a strict
SQL-before-resident-before-employee-before-authority sequence for later live
execution. Capture each executed command's exit/result in the changes record.

## Non-Functional Requirements

Use `/tmp/mv` only under shared heavy admission when changing editables.
No waiting, polling, killing foreign processes or bypassing a busy lock.
Use explicit worktree PYTHONPATH with all relevant src and fixture roots.
Keep raw validation outputs external; commit only non-secret summaries/hashes.
A missing SQL/browser/scanner prerequisite blocks its check, not a cloud
fallback or invented pass. Complete publication gate remains unavailable
because it invokes az, even for offline Bicep.

## Acceptance Criteria

1. Research, plan, critique, details, changes, Review and state exist dated
   2026-10-29, with one stable identity and preserved original findings.
2. No az/gh/cloud mutation, secret read, push, unrelated source edit or closing
   keyword; implementation is explicitly partial/blocked for live delivery.
3. Requested checks have actual results or a precise admission/prerequisite
   blocker, never historical results relabelled as fresh.
4. Local evidence commit uses the existing verified privacy-safe repo identity
   and required trailer. No fresh GitHub-account lookup can use prohibited gh;
   prior authenticated identity evidence is reused and disclosed.
5. Both-sites latest-main and January live authority remain UNMET until the
   coordinator performs fresh backup, exact-preservation and health evidence.

## Locked Test Ownership

Existing suites remain with core/API/infra; removals none, maximum additions
zero, no generated or canonical output changes. Semantic coverage is supplied
by existing resident SQL/startup and employee chat browser tests, not new mocks.
This evidence-only candidate does not change scenario-manifest pins.
Do not mutate/revalidate #521's separate worktree as part of this task.

## Phase Checklist

<!-- P01 -->
### P01: Preserve execution boundaries and coordinator sequence

* [x] P01-T01: Record live blockers, historical revision/digest evidence and
  the exact pending sequence without executing it.
* [x] P01-T02: Park authority apply with exact credential, SQL, source/image
  and revision-budget prerequisites.

<!-- P02 -->
### P02: Validate the current local baseline

* [x] P02-T01: Attempt nonblocking shared lock; install this worktree's
  core/agents/API editables, run core/API Ruff/mypy and unit suites, then
  relevant existing browser checks when prerequisites are available.
* [x] P02-T02: Record anonymous live health observations if reachable,
  distinguish public health from new-revision readiness, and reconcile
  artifacts/command results before the single original Review.

<!-- P03 -->
### P03: Independent Review and local persistence

* [ ] P03-T01: Execute one independent Review and route remaining work;
  no post-Review implementation/review loop.
* [ ] P03-T02: Commit original evidence locally, verify identity/trailer
  and clean worktree; leave publication and live acceptance gated.

## Critique Disposition

One independent critique executed Complete / Revise, preserved at
.copilot-tracking/reviews/plans/2026-10-29/demo-sites-correction-plan-critique.md.
No second critique.

| Finding | Disposition | Evidence |
| --- | --- | --- |
| PC-001 High | Rejected as conflicting with explicit caller direction. | The claimed blanket prohibition on temporary-directory operations is absent from the parent instructions. The user expressly requires `/tmp/mv` and `flock -n /tmp/ama-rpi-heavy.lock`; repository policy names the same lock. Do not invent a replacement lock or weaken that direction. |
| PC-002 Medium | Applied directly. | P02-T01 now isolates HOME/data/state and specifies exact focused fallback selectors before imports, not merely clearing ZF_ variables. |

Planning readiness: Ready for local-only execution. Live execution remains
Blocked. Critique verdict remains Revise as originally written; dispositions,
not a repeated critique, establish the bounded local handoff.

## Follow-Up Items

1. Coordinator live execution in an allowed context: highest delivery impact.
2. #521 source integration, exact-version credential operation and individually
   approved SQL-row renewal: dependent on healthy sites and reconciled revision
   budget, not silently included in a latest-main image.
3. Complete local publication gate and exact-head assessment: separate from
   these requested checks; no pass or push authority inferred.

## Handoff

Research: .copilot-tracking/research/2026-10-29/demo-sites-correction-research.md.
Details: .copilot-tracking/details/2026-10-29/demo-sites-correction-phase-details.md.
Changes destination: .copilot-tracking/changes/2026-10-29/demo-sites-correction-changes.md.
Ready for one original independent Review of the bounded local candidate;
live plan Blocked. Original critique already executed and disposed above.

Pre-Review reconciliation: P01/P02 local deliverables complete, P03 pending.
Requested checks have final passing local results after the two documented
harness corrections. Fresh cloud/January authority acceptance remains UNMET.
