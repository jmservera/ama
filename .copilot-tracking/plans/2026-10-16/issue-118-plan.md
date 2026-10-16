---
title: Issue 118 implementation plan
description: Container hardening and bounded infrastructure evidence
ms.date: 2026-10-16
---

Task ID: 118. Slug: issue-118. Scope: full plan.
Delivery status: owner-directed PR 347 CHANGES implementation complete on the
existing branch. Integrated source candidate 8142553 passes all 11 PR checks.
Evidence-only publication retains that exact executable tree; latest-head CI
must remain green before ready. Full hosted acceptance remains Partial.

## Executive Summary

Preserve Container Apps startup compatibility and enforce kernel controls in
local/CI Docker contracts, not shipped entrypoints. Gate fixable HIGH/CRITICAL
findings and report unfixed findings without ignore lists or baselines.

## User Decisions and Requirements

* Refs #118; implement and publish a PR, never edit issue acceptance checkboxes.
* Work only in src/infra and related CI/docs; no legacy trees, private data,
  environment files, identifiers, deployment CI or Azure changes.
* Preserve human approvals. ADR 0005 is synthetic-development-only.
* Unsuppressed scans; local-first tests, Ruff, mypy and an actual app run.

## Goals

Produce reproducible runtime/CI/IaC evidence without blocking supported ACA startup.

## Scope and Non-Goals

Four source Dockerfiles, shared build/runtime helpers, infra/tests, existing
workflows and directly related documentation. No public rollout, live policy
changes, worker implementation, tenant setup or operational/legal approval.

## Functional Requirements

Keep Dockerfile UID/GID 10001. Verify read-only root, zero capability sets and
NoNewPrivs in the external Docker harness using launch flags; prove omitted
controls fail the contract, while normal ACA-compatible startup still works.
Remove guard-only maintenance command changes. Refresh the same-tag base digest
if newer, rerun apt upgrade and compare fresh before/after scan counts.

## Non-Functional Requirements

No third-party runtime dependencies, bypass switch, scan baseline or ignore list.
Existing CI names and project isolation remain unchanged.

## Acceptance Criteria

Four images must pass runtime contracts and startup compatibility. CI gates
fixable HIGH/CRITICAL findings and uploads non-gating full/unfixed reports.
Compiled Bicep must prove all
workload images, API probes/replicas, gated Premium/WAF/Private Link and
explicit policy/Defender decisions. Hosted controls remain Partial. Mark PR
ready only after all PR CI is green; leave issue checkboxes to the coordinator.

## Phase Checklist

### Current owner-directed continuation (full scope)

* [x] C01 Merge origin/main, preserve both append-only log sides and push.
* [x] C02 Remove shipped guard; keep non-root images and external runtime contracts;
  revert only two guard-specific Bicep commands and coupled assertions.
* [x] C03 Resolve latest same-tag digest, rebuild with fresh apt upgrade, compare
  before/after scans and split fixable gating from unfixed reporting.
* [x] C04 Run local suites/Ruff/mypy/infra/Bicep and actual Docker/API checks.
* [x] C05 Reconcile README/evidence/log/RPI, push existing PR and confirm CI before ready.

The completed original markers below are historical, not current guard requirements.

<!-- rpi:phase id=P01 -->
### P01 Containers and CI
<!-- rpi:task id=P01-T01 -->
* [x] P01-T01 Add shared startup guard and positive/negative runtime harness.
<!-- rpi:task id=P01-T02 -->
* [x] P01-T02 Wire four Dockerfiles and existing CI; remove scan suppressions.

<!-- rpi:phase id=P02 -->
### P02 Infrastructure
<!-- rpi:task id=P02-T01 -->
* [x] P02-T01 Invoke guard explicitly in maintenance jobs and prove compiled app/edge coverage.
<!-- rpi:task id=P02-T02 -->
* [x] P02-T02 Make disabled Defender opt-in non-mutating and document code rationale.

<!-- rpi:phase id=P03 -->
### P03 Evidence and publication
<!-- rpi:task id=P03-T01 -->
* [x] P03-T01 Run local validation, audit each criterion, update READMEs/index/log.
<!-- rpi:task id=P03-T02 -->
* [x] P03-T02 Perform one review, persist findings, commit, push and open PR.

## Critique Disposition

One critique executed: Revise, directly dispositioned before implementation.
PC-001: use explicit ACA command including the guard rather than rely on args-only
semantics; no hosted runtime claim. PC-002: scan early, retain unsuppressed failure
evidence and report genuinely unfixed CVEs as blockers, never suppress them.
PC-003: subTest consolidates six consumers/edge/settings. PC-004: confirm new
src/check-container.py path. All are planner-owned, no changed user decision.
Test ownership: infra/tests for unit/static/
compiled contracts, src/check-container.py for Docker semantics. No removals.
Maximum 25 added test methods, one runtime harness, four images. No generated
templates committed. Validate guard behavior and actual container kernel state,
not only source-text regression.

## Follow-Up Items

* Hosted runtime enforcement requires a supported hosting/security configuration;
  no public deployment or unsupported Bicep properties in this task.
* Worker transport and operational approval remain 144 and owner gates.
* Unfixed base packages require ongoing remediation tracking even when the
  owner-approved fixable-only gate passes; no ignore lists or baselines.
* One Review completed: full hardened hosted acceptance Not accepted while
  RV-001/RV-002 remain open. Publication does not approve rollout.
