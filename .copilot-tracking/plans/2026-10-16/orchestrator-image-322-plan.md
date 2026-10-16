---
title: Orchestrator image resolution plan
description: Owner-directed offline deployment safety for issue 322
ms.date: 2026-10-16
---

## Task Metadata

Task #322; slug orchestrator-image-322. Parent orchestration: rpi-quick.
Branch feat/orchestrator-image-resolution-322 is clean and has no existing PR.

## Executive Summary

Keep Bicep bootstrap semantics simple and resolve deployment images outside
ARM. No deployment script currently exists in infra/ or tools/, so add one
canonical Python CLI under infra/scripts, alongside existing infra helpers.
Application packages and image build contexts remain unchanged in src/.

## Sources

* Issue #322 owner comment dated 2026-10-16, retrieved with comments first.
* infra/main.bicep and infra/modules/containerapps.bicep.
* infra/README.md, infra/tests/test_bicep_policy.py and ADR 0006.

Research disposition: reused. Planning Readiness: Ready. Direct repository
inspection and the explicit owner decision supply sufficient evidence; no
external investigation or Azure access is needed.

## User Decisions and Requirements

* Empty orchestratorImage means placeholder in Bicep.
* Before deployment select current job image, else newest registry tag, else
  placeholder, and print the selection. Preserve real images on redeploy.
* Add offline tests using fake az and compiled Bicep, including mutation checks.
* Update infra/README.md and append docs/reference/log.md.
* Publish a PR with Refs #322 only; no merge or Azure deployment.
* Do not read private data or modify prohibited paths; pip venv, no uv/Docker.

## Goals

Prevent accidental replacement of real job images by bootstrap defaults.

## Scope and Non-Goals

Infra entrypoint, deploy helper, external tests and related documentation only.
No pipeline #138, application changes, Azure writes or data access.

## Functional Requirements

Resolve across the three orchestrator-image jobs for the explicit workload and
environment. Ignore placeholder images when a real current image exists.
Reject conflicting real job images rather than silently overwrite one.
Use registry loginServer and newest repository tag ordered by update time.
Distinguish absent resources/repository from failed queries; errors stop deploy.
Print image and source before what-if/create; warn explicitly on placeholder.
Support explicit image selection, including intentionally selecting placeholder.
Pass workload/environment and resolved image last, preventing parameter-file
defaults from disagreeing with discovery. Reject conflicting inline overrides.

## Non-Functional Requirements

Standard-library helper; no secrets or raw CLI response logging. No credentials
or Azure required by resolver tests. Existing CI discovers infra/tests.

## Acceptance Criteria

Compiled Bicep proves empty default/fallback and exact explicit tag/digest
forwarding into all three jobs. Fake az tests exercise precedence, empty
infrastructure/repository, explicit selection, conflicts, lookup failures and
deployment argument forwarding. Mutations of the default, fallback and resolver
must fail the intended assertions.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implementation

<!-- rpi:task id=P01-T01 -->
* [x] P01-T01: Change Bicep and add guarded deployment CLI.
<!-- rpi:task id=P01-T02 -->
* [x] P01-T02: Add offline resolver and compiled-template regressions.

<!-- rpi:phase id=P02 -->
### [x] P02: Evidence and delivery

<!-- rpi:task id=P02-T01 -->
* [x] P02-T01: Run tests, mutations, Ruff and mypy; document contract and limits.
<!-- rpi:task id=P02-T02 -->
* [x] P02-T02: One post-implementation Review; commit/push/open PR.

## Test Ownership

Canonical resolver tests: infra/tests/test_deploy.py (one new test file).
Compiled assertions: existing infra/tests/test_bicep_policy.py.
No removals; maximum two production files added/modified plus these tests,
related docs and existing CI lint selectors. Generated templates stay temporary.
Semantic precedence tests plus exact Bicep/CLI wiring regressions required.

## Critique Disposition

One final-candidate critique executed: Pass, no findings.
Evidence: .copilot-tracking/reviews/plans/2026-10-16/orchestrator-image-322-plan-critique.md.
Implementation ready; explicit user implementation/publication request applies.

## Follow-Up Items

* Pipeline #138 should reuse the resolver later, outside this task.

## Handoff

Details: .copilot-tracking/details/2026-10-16/orchestrator-image-322-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-16/orchestrator-image-322-changes.md.
Implementation and local evidence complete. One Review executed: Complete,
Conformant, no findings. Normal push and PR #337 completed after Review.
Hosted checks queued at handoff; merge remains the owner's decision.
