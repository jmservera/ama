<!-- markdownlint-disable-file -->
# RPI Plan: infra-policy-release

## Task Metadata

* Task ID: 147-138
* Task slug: infra-policy-release
* Plan date: 2026-10-27
* Planning status: Ready; original critique Revise, all three findings directly resolved
* Phase details: .copilot-tracking/details/2026-10-27/infra-policy-release-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-27/infra-policy-release-plan-critique.md

## Executive Summary

Strengthen existing governance/deployment authoring rather than recreate merged
work. Require pilot locks in the existing Bicep guard; require successful full
source CI for the exact main release SHA; retain an SBOM for each rebuilt release
image. Clarify the historical SQL exception without granting new authority.
Existing workflow/check names and OIDC/approval/digest/private-network controls stay.

### What You May Not Know

The current release scans images but does not depend on complete source CI.
Source CI runs on PRs or manually, not main pushes: an operator will need a
successful manual main run before release. Offline tests cannot satisfy either
issue's outstanding live/owner criteria.

### Unresolved Decisions or Blockers

Defender costs/coverage/activation await subscription owner @jmservera.
Protected environments, per-environment OIDC/RBAC, private runners and real
pipeline acceptance await owner setup. No owner decision is guessed here.

## User Decisions and Requirements

* Run research, plan, implement, review in order; commit dated artifacts.
* Author Bicep/workflows only for #147/#138, validate locally, no deployment.
* Use existing src layout/workflow names; no branch-protection changes.
* No full gate; at most one optional scoped heavy gate, only for large changes.
* Commit, push topic branch and open one evidence-based PR with Refs for
  criteria not fully proven. Stop at owner decisions.

## Goals

* Turn existing pilot-lock intent into an enforced template invariant.
* Connect releases to complete source validation and exact-image inventory.
* Preserve truthful authoring versus live-acceptance boundaries.

## Scope and Non-Goals

In scope: main/guard Bicep, src-deploy YAML, related existing infra tests,
infra README and historical exception metadata.
Non-goals: runtime Python/package changes, new AI behavior, live Azure,
Defender activation/pricing decision, environment setup, source-CI reshaping,
check renames, branch protection, issue closure or ticking unmet criteria.

## Functional Requirements

* Pilot without locks fails the existing named guard; dev/test behavior stays.
* Main release build depends on a read-only, no-Azure CI prerequisite that
  requires successful manual Source projects CI for its exact main SHA.
* Missing, failed, wrong-SHA or inaccessible CI evidence stops the release.
* Each release image gets SPDX JSON before its existing docker-save handoff.
* Historical EX-001 explicitly does not authorize current public SQL.

## Non-Functional Requirements

* Existing privileged jobs retain approval-before-login, OIDC, scoped roles,
  immutable digests and no stored pipeline secrets.
* New job has contents/actions read only, no id-token; no expression injection
  into shell. No change to workflow or pre-existing job/check names.
* Existing infra tests run with required Bicep, no intentional skips.

## Acceptance Criteria

* Compiled guard matrix proves pilot lock rejection and dev/test compatibility.
* Offline workflow contracts and executable fake-gh script cases prove the
  exact-SHA CI prerequisite fails closed before any image build/publish.
* Contracts prove SPDX for all four release matrix images and artifact wiring.
* All Bicep builds and infra discovery pass; actionlint accepts changed YAML.
* PR maps every issue criterion to authored evidence or explicit Not run /
  owner blocker; no unsupported Closes statement.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-27/infra-policy-release-research.md
Changes: .copilot-tracking/changes/2026-10-27/infra-policy-release-changes.md
Review: .copilot-tracking/reviews/logs/2026-10-27/infra-policy-release-review.md
Ready for independent authoring; no cloud setup/approval inferred.

## Sources

* Research C1-C11, issue bodies and owner comments.
* ADR 0002 decision 6; ADR 0006 package/image rules.
* BRD CON-007/AC-086 and PRD CON-009/AC-057 preserve application acceptance.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Governance and release authoring

Intent: wire independent missing guards; dependencies: completed research/critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Require pilot locks and clarify historical exception

Use main/guard and existing compiled guard tests; no new policy or pricing effect.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Gate release on exact source CI and retain release SBOMs

Use existing YAML; bounded read-only gh REST query, main workflow_dispatch
success and exact-SHA match; gate build before all downstream jobs.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and reconcile evidence

Dependencies: P01. Local validation only.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run targeted/full infra tests, compiler and actionlint

Run all template builds, REQUIRE_AZ_BICEP=1 infra discovery and native actionlint.
Use existing toolchain; install dependencies only on missing-tool/package failure.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update runbook and criterion-level evidence

Record owner decisions as unresolved and live checks Not run; reconcile plan,
details and changes before one independent Review and publication.

## Dependencies

Issue #137 parameter sets already exist; actual region/quota checks remain
external. Full source CI on the exact main SHA is a future release prerequisite.
No heavy gate planned: bounded Bicep/workflow-only slice.

## Test Ownership and Change Budget

Canonical tests: infra/tests/test_bicep_policy.py (compiled guard semantics),
infra/tests/test_pipeline.py (workflow structure plus fake-gh execution),
infra/tests/test_governance.py (exception/opt-in existing contracts).
Removals: none. Maximum additions: four test methods; extend existing guard
matrix rather than duplicate it. No generated/committed ARM JSON or new test files.
Semantic checks: compiled expressions and real Bash with fake gh.
Regression checks: existing full infra discovery; actionlint; all Bicep builds.

## Critique Disposition

One final-candidate critique executed; preserve original Revise verdict.

| Finding | Disposition | Resolving plan detail |
| --- | --- | --- |
| PC-001 High | Direct correction applied | Explicit GET/workflow endpoint, bounded filters and complete response predicate; actual Bash fake-gh negative cases |
| PC-002 Medium | Direct correction applied | Extend assert_parameter_controls matrix/forced-ok mutations and preserve committed pilot placeholder failures |
| PC-003 Medium | Direct correction applied | Separate two vulnerability scans from SPDX invocation; assert artifact, ordering and fail-closed export |

No finding needs a new owner decision; no second critique.

## Follow-Up Items

* Owner decision: Defender coverage, accepted cost and activation, #147.
* Owner setup and observed OIDC/what-if/approved deployment/image/health, #138.

## Handoff

P01/P02 complete; 452 infra tests passed with required Bicep, all 25 templates
built/linted and five workflow files passed actionlint. Modified test Ruff checks
passed. Run one independent Review against the complete authoring diff; findings
route later, not a review loop. Human/live acceptance remains separate.
