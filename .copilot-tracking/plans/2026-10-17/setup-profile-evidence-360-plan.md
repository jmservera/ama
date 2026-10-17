<!-- markdownlint-disable-file -->
# RPI Plan: setup-profile-evidence-360

## Task Metadata

* Task ID: issue-360-followup
* Task slug: setup-profile-evidence-360
* Plan date: 2026-10-17
* Planning status: Ready; one independent critique executed, Pass
* Phase details: .copilot-tracking/details/2026-10-17/setup-profile-evidence-360-phase-details.md
* Plan critique: .copilot-tracking/reviews/plans/2026-10-17/setup-profile-evidence-360-plan-critique.md

## Executive Summary

Replace the omitted-parameter heuristic with resolution against each exact
resource-bound deployment's exported ARM template. A neutral patch contributes
no profile; a full template's omitted production default still vetoes demo
generation. Explicit development plus dev/test/demo evidence remains mandatory.

### User Decisions and Requirements Highlights

Source-only owner-priority fix, no cloud mutation; full ordered RPI and one
Review, followed by a clean pushed branch and main PR referencing #360.

### What You May Not Know

Deployment list/get metadata does not contain the template declaration. Reading
the exact template requires an additional metadata export; denied, unavailable
or unresolved relevant contracts stop safely, rather than treating them neutral.
Live credentials and initializer publication 403 gates remain unmet.

### Unresolved Decisions or Blockers

None for offline source work. Critique gate passed; live acceptance excluded.

## User Decisions and Requirements

* Preserve all Key Vault, private service, API selection and read-only job refusal behavior from main/#385.
* Reject production, unknown, conflicting, malformed and failed evidence.
* Do not derive safety from names, purpose or ingress; do not spoof tags.
* Reproduce supplied live shape before fixing and prove default-production refusal.
* Install src distributions before setup/staff test suites.
* No Azure/Graph writes, SQL, Docker, private data, temporary cloud jobs or mutating setup.
* Use branch fix/setup-profile-evidence-360 based on fetched latest main; push/open main PR, no merge/rebase/force push.

## Goals

* Correct neutral-patch classification with actual historical contract evidence.
* Preserve fail-closed resource binding and contradictory-evidence vetoes.

## Scope and Non-Goals

* In scope: setup-local resolver, targeted regression extensions, directly related runbook and KB routing/log.
* Non-goals: src migration, generic ARM interpreter, cloud deployment, role creation, roster generation against a tenant, #360 d/e acceptance.

## Functional Requirements

* Inspect only deployments whose outputResources includes exact selected app or bound environment ID.
* Require Succeeded; validate exported template and recognized declarations/values.
* Resolve explicit values first; on omission use literal declared defaults, never local-template guesses.
* A recognized declared required parameter without a usable value/default rejects.
* Relevant ARM expressions, null/malformed structures and unavailable export reject.
* Collect both deploymentProfile and tags-profile, environmentName and tags-environment; preserve every conflict.
* Neutral templates do not supply approval; authoritative development and safe environment evidence still required.
* Verify returned environment ID matches the selected bound ID before using its tags.

## Non-Functional Requirements

* Minimal setup-local change, no new dependency, no raw payloads in errors.
* Metadata-only export scoped to ama/selected subscription using existing Azure wrapper.
* Existing admin@ first-ProgrammeManager mapping and seeded random distinct users unchanged.
* No unrelated reformat or broader classifier/API redesign.

## Acceptance Criteria

* Actual supplied three-deployment shape fails against unchanged source then passes with fix, with no fake mutation calls in classifier-only regression.
* Neutral template alone cannot authorize; genuine explicit/default production still rejects, including alongside development tags.
* Malformed/null/unknown/default-expression/export-failure, incorrect binding and environment conflict cases reject as SetupError/AzureError before roster work.
* Existing setup and staff_azure suites pass completely with source distributions installed.
* Run configured README lint/format scope; touched legacy-style setup files receive focused changed-line checks, not unrelated full reformat.
* One independent critique and one Review are recorded; findings are not relabeled as coordinator Pass.
* Dated artifacts committed, branch pushed, main PR references #360 without closing; live credential/publication gates explicitly unmet.

## Implementation Context Record

* Research: .copilot-tracking/research/2026-10-17/setup-profile-evidence-360-research.md
* Changes: .copilot-tracking/changes/2026-10-17/setup-profile-evidence-360-changes.md (implementation-owned)
* Continuation: owner explicitly requested full automatic ordered RPI.

## Sources

* Research C1-C6, W1-W4: exact main/module declarations, existing guard/tests and official export/default schema.
* Owner's coordinator-reported live shape: fixture evidence, not fresh live validation.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Reproduce and implement contract-aware evidence

* Dependencies: ready Research and disposed single critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Install distributions and capture failing-first regression

* Extend existing FakeAzure with named deployment/template export contract.
* Test supplied neutral stage plus environment-bound module/main evidence.
* Capture pre-fix failure and existing setup/staff suite counts.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Resolve bound contracts and preserve safety

* Add narrow recognized-parameter resolver and safe container/value guards.
* Validate bound environment identity and independent contradictory tags.
* Preserve all non-classifier behavior.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and document

* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Complete negative matrix and setup/staff validation

* Test ownership: infra/tests/test_setup_entra.py owns classification.
* Exact removals: none. Replace only null-tags bound-success expectation with fail-closed coverage.
* Maximum additions: 18 test methods, using subTest tables for variants.
* Canonical target: setup-entra.py and test_setup_entra.py; no generated target.
* Semantic coverage: literal/default precedence, neutral versus unknown, contradiction and binding.
* Regression coverage: actual reported three-deployment shape; existing admin/random/KV/private/read-only tests.
* Evidence: pre-fix failure, post-fix focused/full setup+staff results, configured lint/format.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Update runbook, index/log and reconcile artifacts

* Correct the runbook's blanket omission-means-production statement.
* Integrate finding into existing setup route; append KB log, preserve memory/original.

<!-- rpi:phase id=P03 -->
### [x] P03: One Review and delivery

* Dependencies: P02, reconciled changes/plan/details.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Execute one Review and route residual work

* Preserve original Review unchanged; no fabricated coordinator acceptance.
* Any residual findings become later work, not a repeated Review.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Commit, push and open main PR

* Fresh gh api user, repo-local noreply author/committer, Conventional Commit plus required Copilot trailer.
* PR includes actual offline results and partial acceptance/live-unmet boundaries.

## Dependencies

* Read-only ARM export permission is a runtime prerequisite; absence rejects safely.
* Pip-installed source distributions and existing hashed test/runtime prerequisites.

## Critique Disposition

| Run | Execution | Verdict | Disposition |
| --- | --- | --- | --- |
| Single final-candidate critique | Complete | Pass, zero findings | Accepted; no second critique |

## Follow-Up Items

* Coordinator authorized own-branch integration onto main 3f544fb9 (#387) and
  exact old-head force-with-lease on 2026-10-17. Rebase completed with only
  append-only log conflict; exact source/test patch and critique/Review parity,
  all upstream src preserved, 200 tests and static checks passed. Publication
  and ordinary check receipt pending; no new full Review.
* Owner/coordinator: live credential and initializer-publication 403 prerequisites, then genuine tenant/browser/SQL/AI acceptance; outside source-only work.

## Handoff

* All plan tasks complete: source commit ac4b28590d8885b314f81be02c2371398270ccd4
  pushed; main PR https://github.com/jmservera/ama/pull/391 opened.
* Evidence: 200 combined setup/staff/auth/secret tests pass; four unsafe
  mutations killed; configured lint/format and changed-line lint pass.
* Review: Complete / Residual work, no source defects found; live gates routed
  to distinct owner/coordinator follow-up, not coordinator acceptance.
* Remaining follow-up: publish authorized integration and obtain actual ordinary
  check status; live acceptance still excluded. See changes integration evidence.
* Automatic session stops per owner's clean-pushed-head instruction. No
  correction cycle, repeated Review or unauthorized history rewrite.
