---
title: Initializer ACR CLI plan
description: Bounded renewed publication and conditional image-only pin
ms.date: 2026-10-17
---

Task ID: 360. Task slug: initializer-acr-cli-360. Base: bab4bf3.

## Executive Summary

Actual local retained-base build failed manifest403. Actual hosted quick-build
uploaded/downloaded source and queued ordinary cpu2 run dbc, then failed registry
login403 before build. No image or pin. Actual installed-source localhost200/401
smoke passes but is not image proof. Deliver honest evidence PR; full private
job settings unchanged. Independent Review Complete/Residual work and open
PR385 complete the bounded lifecycle, with image delivery explicitly blocked.

## User Decisions and Requirements

* Full ordered RPI, one independent critique and one independent Review.
* Preserve private services, base/security upgrades, seven-file proof context
  and existing #375/#379 behavior/grants; no new features.
* Existing publication authorization only; no new pools/infrastructure/network,
  IAM, tenant/SQL/data/Graph operations, job execution, API restart or retirement.
* Pin only job-cutover-test-init, conditional on complete validation and
  before/after configuration-preservation proof.
* Commit all dated phase artifacts, update existing KB/runbook honestly, push
  normal topic branch and open main PR Refs #360. No merge/closing reference.
* Pip only, worktree-local dependencies, tiny fictional data.

## Sources

.copilot-tracking/research/2026-10-17/initializer-acr-cli-360-research.md
(C1-C5, W1-W4), merged #375/#379/#381 and issue #360.

## Goals

Establish current empirical CLI publication capability and safely deliver an
immutable initializer image only if validation succeeds.

## Scope and Non-Goals

Existing registry crcutovertestrzsrg, proof Dockerfile with infra context,
retained API digest and existing initializer only. Source features, public
network access, new spend infrastructure, human acceptance and retirement
are excluded. Ordinary bounded existing-service build attempt is authorized.

## Functional Requirements

Record exact command outcomes and failure stage (upload versus agent build).
Use unique source-SHA/time tag. Verify hosted output digest if produced.
No credential-bearing URLs/raw context archives/environment values in evidence.

## Non-Functional Requirements

Bound local attempt with timeout 180 seconds and hosted service timeout 600
seconds plus client watchdog 720 seconds. No unbounded retry.
Local smoke uses entrypoint override, network none for imports/help and
loopback-only ephemeral port for tiny fictional JSON health/API checks.
No arbitrary cached-base substitution or source-image equivalence inference.
Preserve immutable base and inherited nonroot/security requirements.

## Acceptance Criteria

1. Actual local retained-base build attempted before hosted attempt; actual
   image smoke or exact blocker recorded without source-only substitution.
2. Actual hosted quick-build command attempted with existing registry and
   exact seven-file context, finite bounds and sanitized result.
3. If successful, join run ID, source commit, exact seven-file upload path/hash
   manifest and retained base to the output repository/digest. Pull that hosted
   digest, verify local RepoDigest/image identity, compare all six copied payload
   hashes against the submitted manifest and run UID/import/help/localhost smoke
   on that same digest-addressed image. Only that digest may be pinned. Separate
   local build smoke, mutable tag or missing/mismatched evidence cannot open the
   gate. Otherwise unchanged job proven.
4. Documentation distinguishes historical dbb success/current attempt/runtime
   evidence; #360 d/e remain UNMET; all ordered artifacts included in PR.

## Test Ownership and Locked Candidate

Existing infra tests own context/container/proof/staff behavior. Exact removals:
none. Maximum new test methods: zero unless a concrete root defect is discovered
and requires an explicitly recorded plan amendment. No source feature changes
planned. Canonical targets: infra/README.md, docs/architecture/cutover-evidence-pack.md,
docs/reference/README.md and append-only docs/reference/log.md; generated targets:
dated RPI evidence and sanitized receipt. Semantic proof is actual Docker/ACR
commands; regression tests do not substitute for live image acceptance.
Run existing four focused modules (83 historical tests), escalating only for a
concrete source change; existing scoped lint if code changes.

## Phase Checklist

<!-- P01 -->
### P01: Local and hosted validation

* [x] P01-T01: Local retained-base attempt failed on registry firewall403;
  actual image smoke unavailable, not substituted with source checks.
* [x] P01-T02: Corrected actual az acr build queued dbc; upload/download passed,
  hosted agent registry login403, Failed, no output image.
* [x] P01-T03: No pin; full read-visible job fingerprints and old image equal.

<!-- P02 -->
### P02: Evidence and publication

* [x] P02-T01: 83 focused tests, source localhost smoke, factual KB/runbook/
  receipt, seven links/anchors, append-prefix and exact source preservation pass.
  Native preflight archive/localhost fixture scratch removed.
* [x] P02-T02: Independent Review Complete, outcome Residual work; no defects,
  PC-001 resolved. RV-001 image delivery, RV-002 live acceptance, RV-003 retirement
  routed later. No correction cycle or second Review.
* [x] P02-T03: Fresh privacy-safe identity, evidence commit5504f87, ordinary push
  and open main PR385 verified at matching head; terminal lifecycle commit follows.
  Final remote/PR head is verified externally, not self-embedded in its own commit.

## Critique Disposition

One independent final-candidate critique executed, verdict Revise. PC-001 High
resolved directly: criterion 3 and P01-T02/T03 require the exact hosted digest
for local pull/hash/smoke and pin, joined to submitted manifest and base. No
tests added or source change. No new owner decision or second critique.
Planning execution Complete; implementation readiness Ready.

## Follow-Up Items

RV-001: later authorized existing-service publisher diagnoses hosted-agent
registry403 and supplies exact digest/image smoke before any pin.
RV-002: genuine operator tenant/browser/role/SQL/AI acceptance.
RV-003: separately authorized retirement only after criterion d.
These remain later work, not active implementation completion.

## Handoff

Details: .copilot-tracking/details/2026-10-17/initializer-acr-cli-360-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-17/initializer-acr-cli-360-changes.md.
All bounded plan markers complete as evidence delivery, not image success.
Independent Review Complete/Residual work; PR385 open, automatic session stopped
at explicit owner boundary. Actual image delivery remains Blocked and human
acceptance remains UNMET. No merge/rebase/force-push/closing reference.
