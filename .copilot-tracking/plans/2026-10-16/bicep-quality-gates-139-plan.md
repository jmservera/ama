---
title: Bicep quality gates 139 plan
description: Offline compiled-template controls and mutation coverage
ms.date: 2026-10-16
---

Task: #139 / `bicep-quality-gates-139`.

## Executive Summary

Extend existing error-level lint and compiled-template tests, not a new policy
engine. Prove named controls fail when removed. Wire source CI inside its
existing namespace job, keep legacy checks intact, and document static versus
live assurance. Small safe Bicep corrections: positive audit-retention bound
and tenant-scoped built-in policy IDs exposed by the all-entry-point build.

## User Decisions and Requirements

* Offline only; #138 and all deployment activity are excluded.
* Preserve workflow, job and check names per #321 and ADR 0006.
* Check endpoints, no keys/listKeys, Entra-only SQL, purge protection,
  immutability and production/public rejection; unsupported inputs need names.
* Run local az build/lint, Python unittest and ruff using pip only.
* Never read properwarm.json or touch .env, .vscode or the issues tracking area.
* Update infra README and append knowledge log; push PR with Refs #139 only,
  verified privacy email and specified Copilot trailer.

## Goals

Turn README claims into deterministic, regression-sensitive offline gates.

## Scope and Non-Goals

Existing infra tests/config/guard, small safe Bicep bounds, CI and documentation.
No Azure calls, deployment pipeline, irreversible locking or private data.

## Functional Requirements

Assert each service's endpoint connection/DNS, local-auth controls, SQL,
purge wiring, actual audit container targets and positive retention. Exhaust
production/public/purge input combinations with named guard rejection.
Use the same assertions for clean compiled JSON and mutated copies. Require
presence of every public-access property and forwarding argument, Container
Apps internal mode and development-only SQL firewall condition (PC-001).

## Non-Functional Requirements

No new runtime dependency or committed compiled snapshot. Fail if required
compiler is missing; deterministic local compilation with no login required.
Preserve all existing test semantics and CI identities.

## Acceptance Criteria

Main/governance and modules build/lint. Infra suite and scoped ruff pass.
Mutation cases demonstrate failures for every requested control category,
including endpoint deletion, public bypass, key auth, SQL, purge and retention.
CI triggers on infra changes and runs offline checks within existing jobs.
README and PR explicitly preserve unlocked-policy and live-network limitations.

## Ownership and Validation Contract

Canonical tests: `infra/tests/test_bicep_policy.py`; no test removals.
Maximum additions: one test file only if extraction is needed (prefer none).
Generated targets: temporary JSON only, not committed. Semantic coverage:
compiled controls and profile matrix. Regression coverage: same test assertions
run on deep-copied mutated templates, no Bicep source mutation in worktree.
Run existing full infra suite after pip-installing missing editable source
distributions in an isolated venv; use isolated ruff on changed Python.

## Phase Checklist

<!-- P01 -->
### P01: Implement offline gates

* [x] P01-T01: Strengthen exact controls, profile matrix and mutation coverage.
* [x] P01-T02: Add retention bound and CI wiring without renamed checks.

<!-- P02 -->
### P02: Validate and deliver

* [x] P02-T01: Execute local build/lint, infra suite, ruff and diff review.
* [x] P02-T02: Update docs/evidence for one Review and publication.

## Critique Disposition

One independent critique executed; verdict Revise. PC-001 accepted and resolved
directly in functional requirements and phase details: presence-sensitive
public-access/forwarding assertions and compiled internal/firewall mutations.
No divergent decision or additional critique required. Plan ready.

## Follow-Up Items

Live private-network/Front Door acceptance and owner locking/legal retention
remain outside this offline slice. Pipeline #138 remains separate.

## Handoff

Details: `.copilot-tracking/details/2026-10-16/bicep-quality-gates-139-phase-details.md`.
Changes destination: `.copilot-tracking/changes/2026-10-16/bicep-quality-gates-139-changes.md`.
Implementation and local validation complete. One Review precedes the
caller-authorized commit/push/PR; publication is delivery, not additional
implementation. No required human acceptance is inferred.
