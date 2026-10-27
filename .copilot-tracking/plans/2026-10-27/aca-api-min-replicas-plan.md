<!-- markdownlint-disable-file -->
---
title: API minimum replicas implementation plan
description: Demo-safe minimum with explicit production override
ms.date: 2026-10-27
---

# RPI Plan: API minimum replicas

## Task Metadata

* Task ID: aca-api-min-replicas-2026-10-27
* Task slug: aca-api-min-replicas
* Planning status: Ready; single critique complete and disposition recorded
* Plan date: 2026-10-27
* Phase details: .copilot-tracking/details/2026-10-27/aca-api-min-replicas-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/aca-api-min-replicas-plan-critique.md

## Executive Summary

Expose `apiMinReplicas` in the Container Apps module and main entry point,
defaulting to 0 with bounds 0..4. Keep every committed parameter example at 0
and document the explicit production override to 2. Preserve max replicas,
HTTP rules, authentication, agents and jobs. Run existing offline infra tests
and Bicep compilation/lint, with one independent post-implementation Review.

### What You May Not Know

The production security profile does not mean always-on API replicas.
Scale-to-zero can add cold-start latency. The standalone resident demo has a
separate fixed 0..1 scale and is unchanged. Publication is blocked because
the mandatory complete infrastructure gate conflicts with the caller's no-full-
gate limit; commit locally without push/PR.

## User Decisions and Requirements

* Parameterize the hardcoded API minimum, default 0 for demo and permit 2 for production.
* Thread it through parent and parameter files; update infra README and related tests.
* Preserve everything else; no Azure deployment, secrets, full gate or uv.
* Execute research, plan, implement and review in order; commit dated evidence.
* Use fix/aca-api-min-replicas in the supplied worktree.
* Request is to push and open a PR to main using Refs only; publication is separately blocked.
* Use Conventional Commits and the supplied Copilot co-author trailer.

## Goals

Make future demo templates cost-safe by default without losing production
configurability or silently changing any other workload.

## Scope and Non-Goals

In scope: module/main parameter, three parameter examples, directly related
infra README passages, two existing test files and dated RPI evidence.
Non-goals: new scale rules, changing the maximum, runtime/web changes, live
what-if/deployment or reworking standalone resident-demo resources.

## Functional Requirements

* `apiMinReplicas` is integer default 0 in main and module and feeds API minReplicas.
* Parent forwards the exact input; accepted values include 0 and 2.
* Bound accepted inputs to 0..4, compatible with the unchanged maxReplicas 4.
* All committed examples explicitly select 0, including production-security examples.
* Document `param apiMinReplicas = 2` in an owner-managed production parameter copy.

## Non-Functional Requirements

* No changes to API max 4, concurrency 50, probes, agents min 0/max 5 or jobs.
* No secrets/private data reads, authenticated Azure action or deployment.
* Tests use compiled ARM and existing helpers; no new dependencies or tooling.

## Acceptance Criteria

* Compiled module and main parameters have default 0 and bounds 0..4.
* Compiled parent forwarding and API scale expressions resolve to both 0 and 2.
* Compiled dev/test/pilot parameter examples contain 0.
* Existing policy and resident-demo contracts pass with the intentional API default updated.
* Complete offline infra discovery and az bicep build/lint succeed without unexpected skips.
* Research, plan, details, critique, changes and Review remain dated, honest and committed.
* Publication remains explicitly blocked if complete-gate evidence is absent.

## Implementation Context Record

| Context item | Current artifact |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-27/aca-api-min-replicas-research.md |
| Plan | .copilot-tracking/plans/2026-10-27/aca-api-min-replicas-plan.md |
| Phase details | .copilot-tracking/details/2026-10-27/aca-api-min-replicas-phase-details.md |
| Critique | .copilot-tracking/reviews/plans/2026-10-27/aca-api-min-replicas-plan-critique.md (original Revise; PC-001 disposition below) |
| Changes record | .copilot-tracking/changes/2026-10-27/aca-api-min-replicas-changes.md (implementation-owned) |
| Readiness | Ready; single critique finding dispositioned, no functional blocker |
| Continuation | Automatic parent; local implementation eligible, publication blocked |

## Sources

* .copilot-tracking/research/2026-10-27/aca-api-min-replicas-research.md: C1-C9.
* Owner task, 2026-10-27: scope, branch, validation and publication intent.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Parameterize and document

Intent: wire the minimum without altering other resources. Dependencies: ready critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Add and forward bounded minimum

Update containerapps.bicep, main.bicep and all three existing parameter examples.
Expected: default 0, clear cost/production description, unchanged other scale.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reconcile documentation and regression contracts

Update README frontmatter, environment table, minimum guidance and stale resident
separation prose. Extend existing policy test and replace stale resident assertion.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and reconcile

Intent: provide scoped offline evidence. Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run infra checks and record changes

Use README infra unittest discovery with REQUIRE_AZ_BICEP=1 and Bicep build/lint.
If dependency imports fail, use pip in a disposable external venv; do not install
otherwise. Run the existing changed-file Ruff selector where available.
Reconcile plan/details/changes before handing to one independent Review.

## Locked Test Ownership and Evidence

* Owner: infra/tests/test_bicep_policy.py owns compiled main/module scale contracts.
* Owner: infra/tests/test_resident_demo_deploy.py owns standalone separation.
* Exact removals: replace the old `minReplicas == 2` assertion and source-text
  `minReplicas: 2` assertion only; remove no test methods or other checks.
* Maximum additions: two test methods, both in existing policy test file.
* Canonical targets: Bicep and bicepparam sources above; generated ARM goes to
  stdout or external temporary storage, never committed.
* Semantic evidence: compiled input schema, parent forwarding, evaluate helper
  exercised for default and production 2, compiled parameter files.
* Regression evidence: unchanged HTTP rule/max/probes, agent min/max, separate
  resident scale, full offline infra discovery including fake what-if wrappers.
* Validation commands: README infra unittest discovery; az bicep build/lint;
  az bicep build-params for existing examples; targeted Ruff if available.
* tools/rpi-checks.py --changed is not run: it selects extra gates and requires
  clean exact-HEAD/tool prerequisites; direct component checks satisfy requested
  testing, not mandatory complete-gate publication evidence.

## Dependencies

Local Azure CLI/Bicep already available (0.48.1); Python 3.12.3.
No live Azure access needed. Full-gate evidence is a publication-only dependency.

## Critique Disposition

| Finding | Owner | Disposition | Evidence / rationale |
| --- | --- | --- | --- |
| PC-001, original Revise | Planning parent | Rejected as inapplicable worker-local constraint | The critique assumes a prohibition on external/system temporary storage not present in the parent's execution environment or caller scope. Existing tempfile tests and disposable external venvs are permitted. Preserve original critique unchanged; use a task-owned session files directory for temporary output/venv if needed, with TMPDIR set for test processes. No source/test changes or second critique are warranted. |

Original critique execution Complete, verdict Revise. Parent readiness Ready
after rejecting the unsupported constraint; this does not rewrite that verdict.

## Follow-Up Items

* Complete required publication gate under a later authorized scope, then exact-head
  assessment and push/PR. Do not treat scoped checks as equivalent.

## Handoff

Implementation artifact: .copilot-tracking/changes/2026-10-27/aca-api-min-replicas-changes.md.
P01/P02 complete with offline evidence in the changes record. Ready for the
single independent Review; publication-only blocker remains.
