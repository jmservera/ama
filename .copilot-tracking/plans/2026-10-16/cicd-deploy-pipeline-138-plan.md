---
title: Deployment pipeline implementation plan
description: Issue 138 implementation and evidence boundary
ms.date: 2026-10-16
---

Task: 138 / cicd-deploy-pipeline-138

## Executive Summary

Add pinned, least-privilege workflows with offline tests and private-runner,
environment-gated OIDC what-if/release. Preserve existing source CI names and
legacy files. Local evidence cannot satisfy live Azure acceptance.

## User Decisions and Requirements

* No Azure execution, real identifiers, stored secrets or retired-layout edits.
* Use merged environment examples and source-image hardening/Trivy policy.
* Only ama, incremental deployment, SQL always private.
* Open a PR with Refs #138 and an honest criterion-by-criterion audit.

## Goals

Provide a reviewable, fail-closed deployment path for four source images.

## Scope and Non-Goals

Workflows, infra helpers/tests and directly related documentation. No tenant
provisioning, role assignment changes, private data or live acceptance.

## Functional Requirements

Generate ARM parameters from committed examples with environment-variable
overrides. Attach a sanitized what-if summary. Release versioned images after
runtime/Trivy gates; deploy digests using the same main template/parameter set.
Run exact HTTP denial probes and verify SQL public access after deployment.

## Non-Functional Requirements

Only job-local id-token write; checkout without credentials; pinned actions;
no raw Azure output or exception text in logs/artifacts. Private ephemeral
runners and protected environment approval are setup prerequisites.

## Acceptance Criteria

Offline workflow structure and behavior tests pass; errors fail closed;
documentation records all external approval/federation/runtime gaps.

## Phase Checklist

* [x] P01-T01: Add workflow and infra helper with unit tests.
* [x] P02-T01: Update READMEs, reference index and append-only log.
* [ ] P03-T01: Run local lint/types/tests, one review, commit and open PR.

## Test Ownership

Canonical tests: infra/tests/test_pipeline.py. No removals. At most two new
test files and three new helper files. Behavioral tests use fake processes and
local HTTP, not Azure; structure tests parse YAML. Run actionlint if available.
No generated deployment output is committed.

## Critique Disposition

One critique executed, verdict Revise. Compatible findings applied directly:

* PC-001/008: trusted default-branch workflow_run consumes successful source CI
  for same-repository PRs only. Candidate infra is data; only trusted helpers run.
  Exact candidate SHA appears in the sanitized artifact. Forks excluded.
* PC-002/006: hosted build/test jobs have no OIDC. Separate private publish,
  plan and deploy identities; scope/RBAC and runner policy are external gates.
* PC-003/004: main-only dispatch, immutable run-specific image digests, typed
  environment overrides, fixed template/profile, fresh pre-apply what-if.
* PC-005/012: explicit typed authentication-mode choice preserves browser UX
  unless service-test mode is deliberately selected; exact output-bound HTTPS
  endpoint, no redirects; strict health/anonymous/malformed/forged-header probes
  plus browser sign-in 302 when selected.
* PC-007/013: group-only incremental operations, structured what-if fails on
  Delete/unknown/Ignore/out-of-group; existing SQL precheck and postcheck must
  find at least one server with every server Disabled.
* PC-009/010: drop registry cache reuse. Every release rebuilds all four images
  from one immutable main SHA, scans and publishes unique run/attempt tags.
  Per-project PR path filtering belongs to the existing source CI build steps.
* PC-011: do not disable quarantine. Deployment uses a separate pull-only
  registry login to pull every exact digest before apply; quarantined artifacts
  fail closed until an independently approved release process makes them
  available (documented live gap).
* PC-014/015: serialize all ama releases; no cancellation or automated rollback;
  persist checks in offline CI; exact commands and negative fixtures recorded.
* PC-016: report all six issue criteria as live-unverified/partial and preserve
  the inherited hosted-kernel-hardening limitation.

No significant divergence from user direction requires a new decision.

## Follow-Up Items

Live environment reviewer/branch rules, federated credentials, scoped RBAC,
private runners, pilot ownership/region and actual deployment evidence.
