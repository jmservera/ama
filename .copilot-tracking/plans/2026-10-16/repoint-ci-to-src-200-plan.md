---
title: Issue 200 source cut-over plan
ms.date: 2026-10-16
---

Task: #200 / `repoint-ci-to-src-200`

## Executive Summary

Finish the already-merged source migration by aligning runtime entry points,
isolated images, CI inputs, data defaults and branding tools. Preserve existing
job/check names, historical identifiers and the mvp pointer. Verify locally before
publishing the full RPI evidence in one main-targeted PR with `Refs #200`.
Cloud deployment and private-data backup remain explicitly unmet acceptance gates.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review in order with dated artifacts.
* Use branch chore/repoint-ci-to-src-200; commit and push artifacts with code.
* Retain mvp/ and workflow/check names. Record later naming as an owner question;
  issue comments already direct retaining names through cut-over.
* Follow ADR 0006's updated src context, installed packages and named copies.
* No private input, fabricated approval, new mvp feature, SQL dialect or authority change.
* Local-first unit, mypy/ruff, app, rename and infra checks; Bicep if available.
* Use pip only, safe author email and required Copilot trailer; never force-push.

## Sources

Research: `.copilot-tracking/research/2026-10-16/repoint-ci-to-src-200-research.md`
(C1-C9, W1); issue #200 comments; ADR 0006; per-project READMEs.
Previous dated issue-200 artifacts remain historical, not current acceptance.

## Goals

Working installed-src build/run commands and explicit remaining cut-over gates.

## Scope and Non-Goals

Change only live paths/entry points and tightly coupled regression tests/docs.
No source migration duplication, mvp deletion, check renaming, Azure rollout,
private dataset read/relocation, dependency upgrades or general lint cleanup.

## Functional Requirements

* `python -m zava_forward.api` starts the existing server.
* Bicep jobs consume orchestratorImage with existing module commands/identities.
* API image contains API, agents and core only; orchestrator image owns jobs.
* Runtime default data is ~/.zava-forward/data/zavaforward.json; explicit ZF_DATA
  file remains exact, folder resolves its zavaforward.json consistently.
* Branding tooling targets packaged web/policies, never recreates mvp/web.
* CI path filters cover src build inputs without changing names/job IDs.

## Non-Functional Requirements

Preserve hash pins, non-root user, read-only/no-data behavior, dependency rule,
server authorization and historical evidence. Use synthetic fixtures only.

## Acceptance Criteria

* All local suites/checks listed below pass or precise blockers are recorded.
* Docker images built/run locally where tooling permits, with properties checked.
* Generator imports and default paths verified without reading private stock data.
* Index/log, current README commands and artifacts agree on delivered versus unmet.
* New-tag Azure deployment, real SQL/model/human acceptance and private backup
  must not be claimed from local synthetic evidence.

## Phase Checklist

<!-- P01 -->
### P01: Runtime and automation
* [x] P01-T01: Fix API entry point and coordinated CI probes/path filters.
* [x] P01-T02: Isolate API/job images and repoint Bicep image references.
* [x] P01-T03: Align runtime data path and branding tool targets with src.

<!-- P02 -->
### P02: Evidence and delivery
* [x] P02-T01: Run local validation, record exact commands/results.
* [x] P02-T02: Update live docs/index/log and reconcile acceptance status.
* [ ] P02-T03: One Review; commit, push and open main-targeted PR.

## Validation and Test Ownership Lock

API owns entry-point test; core owns factory path tests; infra owns compiled
image/command assertions; rename suite owns current policy/web/logo regression.
Maximum additions: 10 focused test methods; exact removals: none.
Canonical targets are src packages and Bicep; generated ARM stays outside git.
Semantic assertions test image/command bindings and exact data paths; historical
branding tests remain regression evidence.
Run all five unit suites with absolute source/test PYTHONPATH per caller,
project mypy/ruff/format, rename suite, infra suite with Bicep required,
Bicep build/lint, node syntax, loopback app with temporary synthetic data.
Build all four images with src context; run non-root/no-data/read-only checks,
API health and logo response. No Azure needed for this mechanical change.

## Critique Disposition

Exactly one critique executed, verdict Revise. PC-001 rejected: its claimed
workspace-only filesystem restriction is not applicable to this parent and conflicts
with the caller's explicit /tmp/zf164 requirement. Use caller-approved tools and
task-specific temporary synthetic scratch. PC-002 accepted directly: version.py
does not print; both probes must explicitly import and print distribution version.
No significant/divergent user decision remains. Planning readiness: Ready.

## Follow-Up Items

1. #201/#203: deploy immutable new image tags to existing ama resources and verify;
   preserve historical running-revision tags.
2. Owner cut-over: confirm private data copy/encrypted backup and mvp retirement.
3. Owner naming question: rename workflows/checks in one post-cut-over PR.

## Handoff

Implementation changes record:
`.copilot-tracking/changes/2026-10-16/repoint-ci-to-src-200-changes.md`.
P01 and P02-T01/T02 complete; commands and limits are in the changes record.
Source implementation review-ready. P02-T03 is pending one Review and publication,
not unresolved implementation. Cloud/owner follow-ups remain outside local scope.
