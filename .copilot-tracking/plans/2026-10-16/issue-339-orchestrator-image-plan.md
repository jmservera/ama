---
title: Issue 339 implementation plan
description: Normalize explicit orchestrator images and prove offline CLI behavior
ms.date: 2026-10-16
---

## Task Metadata

* Task ID: issue-339
* Task slug: issue-339-orchestrator-image
* Plan date: 2026-10-16
* Planning status: Complete; implemented, reviewed and published
* Phase details: .copilot-tracking/details/2026-10-16/issue-339-orchestrator-image-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-16/issue-339-orchestrator-image-plan-critique.md

## Executive Summary

Strip the explicit image before selecting it so blank values use the established
discovery path instead of reaching Bicep. Expand existing offline subprocess
tests and update the deployment README and append-only reference log.

### What You May Not Know

The same CLI constructs both what-if and apply commands; both must be tested
without invoking real Azure. Placeholder fallback remains visibly warned.
No live deployment acceptance is claimed.

## User Decisions and Requirements

* Deliver #339 in this worktree and open a PR using `Refs #339`.
* Work offline; do not edit `infra/scripts/setup-entra.py`, legacy trees,
  private datasets, environment/editor configuration or GitHub issue tracking.
* Add tests, update directly related README, append reference log, provide
  research/plan/changes/review artifacts and honest criterion evidence.
* Do not tick the issue body; coordinator owns merge-time updates.
* Use the authenticated account's repository-local noreply email and required
  Copilot coauthor trailer; push normally, without merging or force-pushing.

## Goals

* Prevent whitespace-only explicit images from bypassing resolution.

## Scope and Non-Goals

* In scope: deploy CLI, its existing tests, infra README, reference log and RPI artifacts.
* Non-goals: new image validation policy, Bicep changes, live deployment, web work,
  authentication changes, operational approvals or unrelated cleanup.

## Functional Requirements

* Strip explicit input before the truthiness check; blank input resolves.
* Preserve valid explicit images after trimming, bypassing image discovery.
* Retain placeholder warning, authentication guard and exit-code propagation.

## Non-Functional Requirements

* Offline tests use the existing fake-az subprocess harness only.
* Scoped Ruff/format and mypy must pass; install missing tools with pip in an
  isolated temporary venv. No application-package changes are needed.

## Acceptance Criteria

* AC1: Empty and whitespace-only values use discovery, never a blank image.
* AC2: A discovered real image is preserved; absent images use warned placeholder.
* AC3: Padded explicit tag, digest and placeholder are trimmed and skip discovery.
* AC4: What-if and apply forward the resolved image; existing behavior stays covered.
* AC5: README, log and artifacts document evidence and offline/live boundaries;
  branch is committed, pushed and a PR opened with `Refs #339`.

## Sources

* .copilot-tracking/research/2026-10-16/issue-339-orchestrator-image-research.md
* infra/scripts/deploy.py
* infra/tests/test_deploy.py
* infra/README.md
* GitHub issue #339 and user task instructions

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Normalize and verify the deployment CLI

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add regression coverage and normalize input

* Add blank-resolution matrix and expand explicit-image coverage; demonstrate
  failure before the fix, then normalize once at CLI parse boundary.
* Test ownership: infra/tests/test_deploy.py; removals: none; maximum additions:
  one test method, with existing methods expanded. No new harness or generated targets.
* Semantic coverage: exact image/source/warning and command forwarding.
  Regression coverage: existing deploy suite, including authentication/errors.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Document, validate and publish

* Update infra README and append reference log; run focused unit tests, scoped
  Ruff/format/mypy and local CLI help. No service app changed, so no unrelated
  HTTP server or live Azure is required.
* Record changes, one post-implementation review and criterion audit.
* Commit/push/open PR; leave merge and issue ticks to coordinator.

## Dependencies

* P01-T02 depends on P01-T01 for recorded validation evidence.
* Independent critique must finish before implementation.

## Critique Disposition

* One critique executed; verdict Revise, PC-001 (validation provisioning).
  Disposition: rejected unsupported constraint. The critique claims system
  temporary paths are prohibited; no applicable caller instruction says this.
  User explicitly permits pip after missing-tool failures and requires GitHub
  publication. Offline here prohibits live Azure, not approved GitHub/pip use.
  Ruff/mypy were absent; tools restored in /tmp/ama-339-validation with pip.
  Existing temporary-directory harness remains unchanged. No new acceptance
  criterion or human decision is needed; no second critique will run.

## Follow-Up Items

* None.

## Handoff

* Changes: .copilot-tracking/changes/2026-10-16/issue-339-orchestrator-image-changes.md
* All plan tasks complete. CLI/test/doc Review executed once: Complete,
  Conformant. Publication completed afterward by parent, not a second Review.
* PR: https://github.com/jmservera/ama/pull/366 (Refs #339), main base.
* Implementation commit: 56d2d7c; pushed without force.
* Merge and issue ticks remain coordinator/owner decisions, not task blockers.
* Blockers: none; critique finding disposition recorded.
