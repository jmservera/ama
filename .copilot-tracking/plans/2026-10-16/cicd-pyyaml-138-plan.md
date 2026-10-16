---
title: CI infra test dependency correction plan
description: Bounded repair for PR 357
ms.date: 2026-10-16
---

Task: 138-ci-pyyaml. Slug: cicd-pyyaml-138.

## Executive Summary

Install the existing pinned PyYAML only in the failing infra test step.
Preserve production packaging and structural workflow controls. Reproduce
the baseline failure, then verify with the explicit test-only prerequisite.

## User Decisions and Requirements

* Reuse PR 357 and its branch, merge origin/main if needed; never force push.
* Refs #138 only. Preserve both append-only log histories.
* Pinned test-only PyYAML is explicitly allowed; no production dependency.
* Produce RPI evidence, update README/log, commit with required identity/trailer.
* No live Azure/OIDC acceptance or invented human approval.

## Goals

Make validate discover and execute every infra test, including control mutations.

## Scope and Non-Goals

One CI test step, infra tests, directly related docs and RPI artifacts.
No application logic, deployment, retired-layout changes or issue checkbox edits.

## Functional Requirements

Both CI consumers install `PyYAML==6.0.3` before infra discovery. A missing
installation must fail the regression assertion, not skip workflow checks.

## Non-Functional Requirements

No production dependency additions; existing job/check names retained.
Use existing PyYAML parsing rather than a bespoke YAML subset.

## Acceptance Criteria

* Baseline clean venv reproduces the import failure with source packages only.
* Same venv, after the pinned test prerequisite, passes complete infra discovery.
* Removing the dependency-install command from either consumer is detected.
* Existing unsafe pipeline-control mutations continue to fail their assertions.
* Local Ruff/format, helper mypy and existing real local API probe pass.
* Commit pushed to existing PR without force, all live criteria still unchecked.

## Phase Checklist

<!-- P01 -->
### P01: Integrate and repair

* [x] P01-T01: Merge origin/main, retaining both log histories.
* [x] P01-T02: Add pinned install and dependency-removal regression.
* [x] P01-T03: Update complete infra recipe, index and append-only log.

<!-- P02 -->
### P02: Validate and publish

* [x] P02-T01: Run clean-venv infra suite, mutations, Ruff/format and mypy.
* [x] P02-T02: Record one post-implementation review and acceptance audit.
* [ ] P02-T03: Commit and push; reuse existing PR 357.

## Test Ownership and Change Budget

Canonical tests: `infra/tests/test_pipeline.py`. Removals: none.
Maximum additions: two test methods and one small shared assertion helper.
Semantic coverage: pin installed before execution; regression coverage:
delete install in each consumer and reject the resulting document.
Generated targets: none. Validation: exact clean-venv reproduction, full
infra suite (including actual local HTTP/API probes), isolated Ruff and mypy.

## Critique Disposition

One independent critique executed, verdict Revise. PC-001 recommends moving
the isolated venv because of a worker-local restriction on `/tmp`. Rejected:
no such restriction applies to this parent execution; the path is a unique,
explicitly created task-owned venv, not shared state. Retain the already
reproduced baseline and same-interpreter comparison. The useful clarification
is adopted: install lint/type tools only after the dependency comparison.
No unresolved decision; implementation-ready. No second critique.

## Follow-Up Items

Existing PR acceptance audit remains authoritative: actual OIDC/RBAC,
protected-environment approval, what-if, registry release/deployment,
private runtime checks and live log audit remain unmet.

## Handoff

Research: `.copilot-tracking/research/2026-10-16/cicd-pyyaml-138-research.md`.
Changes: `.copilot-tracking/changes/2026-10-16/cicd-pyyaml-138-changes.md`.
Implementation readiness: Ready.
