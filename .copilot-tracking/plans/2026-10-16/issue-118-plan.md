---
title: Issue 118 implementation plan
description: Container hardening and bounded infrastructure evidence
ms.date: 2026-10-16
---

Task ID: 118. Slug: issue-118. Scope: full plan.
Delivery status: implemented and published as draft PR 347. Full hardened hosted
acceptance remains blocked by RV-001/RV-002; no rollout or merge approval.

## Executive Summary

Enforce image startup invariants and test all four images in existing CI.
Remove vulnerability suppression, retain private gated Bicep and code explicit
governance decisions. Audit, do not claim, unsupported hosted enforcement.

## User Decisions and Requirements

* Refs #118; implement and publish a PR, never edit issue acceptance checkboxes.
* Work only in src/infra and related CI/docs; no legacy trees, private data,
  environment files, identifiers, deployment CI or Azure changes.
* Preserve human approvals. ADR 0005 is synthetic-development-only.
* Unsuppressed scans; local-first tests, Ruff, mypy and an actual app run.

## Goals

Fail unsafe image startup; produce reproducible runtime/CI/IaC evidence.

## Scope and Non-Goals

Four source Dockerfiles, shared build/runtime helpers, infra/tests, existing
workflows and directly related documentation. No public rollout, live policy
changes, worker implementation, tenant setup or operational/legal approval.

## Functional Requirements

Check UID/GID, read-only root, all Linux capability sets and NoNewPrivs before
exec. Preserve image commands/signals. Validate unsafe launch refusal and actual
API health on a constructed fixture. Keep job arguments through entrypoint.

## Non-Functional Requirements

No third-party runtime dependencies, bypass switch, scan baseline or ignore list.
Existing CI names and project isolation remain unchanged.

## Acceptance Criteria

Four images must pass runtime controls and negative launches; CI tests and
HIGH/CRITICAL scan include unfixed findings. Compiled Bicep must prove all
workload images, API probes/replicas, gated Premium/WAF/Private Link and
explicit policy/Defender decisions. Hosted controls and scans without successful
execution remain unmet and are reported honestly.

## Phase Checklist

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
* All four image scans fail on unfixed base packages. Technical/project owner
  must research a compatible maintained base/remediation path; no ignore lists.
* One Review completed: full hardened hosted acceptance Not accepted while
  RV-001/RV-002 remain open. Publication does not approve rollout.
