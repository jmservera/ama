---
title: Issue 118 implementation changes
description: Execution evidence and remaining acceptance boundaries
ms.date: 2026-10-16
---

Task ID: 118. Slug: issue-118. Full plan in scope.

## Initial State

Existing clean topic branch feat/hardened-deployment-ci-118, no open PR.
First boundary P01-T01. Readiness evidence in research and phase details.
Planned validation: four image builds/runtime contracts, unsuppressed scans,
infra tests/build/lint, project suites/Ruff/mypy and synthetic app health.
Hosted runtime enforcement is a known acceptance gap, not a deployment action.

## P01 Container and CI Evidence

Four Dockerfiles copy a stdlib-only guard and set UID/GID explicitly. Guard
refuses unsafe startup with exit 78 and diagnostic; exec preserves signals.
src/check-container.py proves kernel state and actual write denial, plus five
negative launches per image, agents dependency isolation, actual API health/PNG
and non-API default CLI. All four local builds/runtime harnesses passed.
The API allow-list initially excluded the new guard; build failed explicitly,
then its Dockerfile.dockerignore was corrected and all builds passed.
An early HTTP connection reset exposed a startup race in the harness; narrowly
retry startup connection failures with running-state check, then all passed.
ACR recipe no longer overrides entrypoint. It was not run in Azure.

src-ci uses the harness, absolute test-fixture paths, Trivy config and scan
artifacts. Existing API workflow scan uses identical no-ignore/unfixed policy.
No new deploying CI. Four local Trivy 0.76.0 scans exit 1: 61 HIGH, 2 CRITICAL
package findings, 16 unique CVEs, all unfixed. Reports retained in session files;
acceptance audit includes counts and image IDs. This is a real unmet gate.

## P02 Infrastructure Evidence

Explicit maintenance job commands invoke guard before Python application,
avoiding args-only behavior ambiguity (PC-001). Compiled six-consumer image
wiring, API probes/replicas and Premium/WAF/private-origin checks passed.
Disabled Defender condition submits no pricing resource; existing plans are
preserved instead of downgraded to Free. Policy remains DoNotEnforce for these
new assignments, no existing policy bypass. Rationale documented.
126 infrastructure tests passed; all templates built/linted with Bicep 0.48.1.
Nine new test methods, consolidated using subTest, below the 25-method limit.

## Critique Dispositions and Current-State Updates

One critique executed, verdict Revise, all four findings directly dispositioned.
PC-001 explicit guard invocation; PC-002 no fallback on unfixed CVEs, retain failed
scan evidence; PC-003 subTest consolidation; PC-004 confirmed new harness path.
No new user decision, repeated critique or unsupported hosted property.
Hosted runtime remains unmet; rollout blocked and documented. No Azure runs.

## P03 Validation and Handoff

Complete project suites passed: core 504 (one skipped), API 549 (110 skipped),
agents 70, orchestrator 22, importer 39. Ruff check/format and mypy passed in
all five projects; shared test PYTHONPATH was absolute and scoped per project.
Strict mypy and isolated Ruff/format passed for container helpers. actionlint
1.7.12 passed both changed workflows with shellcheck integration disabled.
Final infrastructure discovery passed 126 tests. No private dataset was read.
Scan failures and unsupported hosted enforcement are acceptance findings, not
hidden exceptions. All five original criteria audited in durable evidence.
Index/log and directly related source/infra READMEs updated.

One post-implementation Review executed, Complete; outcome Not accepted for
full hardened hosted deployment. RV-001 routes supported hosting to later Plan;
RV-002 routes unfixed base remediation to later Research. No repeated Review.
Code delivery is ready for the explicitly requested PR with these gates open.

## P03 Publication

Committed implementation as 9a33120 on feat/hardened-deployment-ci-118, pushed
without rewriting history, and opened draft PR 347 targeting main:
https://github.com/jmservera/ama/pull/347 .
Authenticated account id/login matched the required repo-local noreply email;
both commits carry the required Copilot coauthor trailer. Issue body unchanged.
PR is OPEN and draft, with original criteria individually audited. No merge.
Immediately after creation GitHub reported no checks yet, not successful CI.
Final publication metadata is committed separately; no production source changes
were made after the single Review.
