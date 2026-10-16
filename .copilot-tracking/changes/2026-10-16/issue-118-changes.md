---
title: Issue 118 implementation changes
description: Execution evidence and remaining acceptance boundaries
ms.date: 2026-10-16
---

Task ID: 118. Slug: issue-118. Full plan in scope.

## PR 347 owner-directed continuation

Independent review returned CHANGES. Owner directs removal of shipped guard,
external runtime enforcement, fixable-only Trivy gate and separate unfixed report.
This is an explicit change to the original guard/scan decision, not an inferred
approval. No repeated critique or Review of the original task is required.
C01 completed: inspected PR body/diff and issue criteria, fetched and merged
origin/main; only conflict was docs/reference/log.md. Kept both sides intact.
Merge 8ac9367 pushed to existing branch; no new PR.
C02 is first implementation boundary. Local validation and honest per-criterion
evidence precede publication. Another loop owns edge changes; Bicep scope is
only two guard-bearing job commands. Docker available via sudo; no Azure needed.

### C02 external controls and compatible startup

Removed src/container-entrypoint.py and all Dockerfile COPY/ENTRYPOINT wiring;
retained UID/GID 10001, digest pins and apt upgrade. Reverted only guard additions
in the two maintenance job commands and their compiled assertion.
Harness now uses the kernel probe as an external contract under explicit Docker
flags. Five intentionally incomplete-control probes must fail that contract;
the image itself is no longer required to refuse normal ACA-compatible startup.
Both hardened and plain non-root default CLI/API health/static startup are
exercised. Seven focused infra regressions, isolated Ruff and strict mypy pass.

### C03 scan policy and measured remediation

Docker Hub latest same-tag index equals existing pinned 34386ef... digest.
All four --pull --no-cache builds reran apt update/upgrade: zero upgrades.
Before and after full scans, same fresh DB and verified Trivy 0.76.0 binary:
61 HIGH/two CRITICAL package findings each, 16 unique CVEs, zero with a fix.
No reduction claimed. All four fixable gates pass with zero findings.
Both existing image workflows now gate with scanner ignore-unfixed true and
run non-gating full/unfixed-inclusive reports with exit-code 0 and false.
Both JSON files upload even after gate failure. Scanner errors remain visible.
No ignore list, baseline, CVE suppression or metadata removal added.
CI Trivy version matches local 0.76.0. Runtime scans survive smoke failures.

### C04 local validation and tightly coupled CI correction

All project suites and Ruff check/format/mypy passed: core 504 (one skip),
API 549 (110 skips), agents 70, orchestrator 22, importer 39.
Absolute per-project fixture PYTHONPATH, editable installs in session venv.
Infra discovery passed 130 tests; all Bicep templates built/linted with 0.48.1.
Seven container regressions, isolated Ruff/format and strict mypy passed.
actionlint 1.7.12 verified archive, changed workflows pass without shellcheck.
All four actual Docker runtime probes/default startups pass in hardened and
plain non-root modes. API HTTP health and exact PNG pass in both modes.
Docker omits Entrypoint metadata when unset; harness handles that legitimate
optional field and verifies exact CMD instead of assuming a null JSON key.
PR CI logs revealed /src/core/tests fixture paths: matrix interpolation resolved
github.workspace too early. Moved scoped path expressions to the unit-test step
environment; regression prevents the old matrix form. This is directly coupled
CI correctness, not unrelated cleanup. No source application logic changed.

### C05 publication and concurrent-main integration

Published corrections as ab1c5c0 and updated existing PR 347 (still draft).
All 11 checks passed after one failed source API browser navigation timeout:
full browser harness passed locally unchanged, followed by successful rerun
of run 38934285993. No test bypass or speculative UI change. MVP CI
38934285490 and MVP validation 38934285398 passed. Downloaded and verified
all four source reports plus the existing API image report: every full report
retains 61 HIGH/two CRITICAL, every fixable gate has zero findings.

While CI ran, main advanced with c1deba4 (#348), making the PR log conflict.
Merged again as 8142553; both prior log histories preserved verbatim.
New agents tests need core fixtures: preserved the upstream dependency in
the absolute-path step expression instead of retaining an unused matrix field.
No infrastructure source conflict; containerapps.bicep now has no diff from main.
Repeated full local checks after integration: core 517 (one skip), API 553
(110 skips), agents 77, orchestrator 22, importer 39; all Ruff/format/mypy pass.
Infra 130 tests and helper checks pass. All four integrated builds and real
hardened/plain startup contracts pass; same-DB scans remain 61 HIGH/two
CRITICAL unfixed per image, zero fixable.

Integrated candidate 8142553 passes all 11 PR checks on the first attempt:
Source projects CI 38936437239, MVP CI 38936437236, MVP validation 38936437380.
No skipped/failed checks are counted as green. The final closeout changes only
documentation/RPI evidence, with identical source/infra/workflow trees.
Existing PR body is reconciled to current counts and explicit Partial criteria.
PR ready remains gated on the latest evidence-only head checks; no new PR,
merge, issue checkbox edits, Azure action or operational approval.
Task implementation complete; manual session stopped. Original Review remains
executed/Not accepted for full hosted hardening, with owner-directed dispositions
recorded rather than a repeated Review. Remaining acceptance gaps are explicit
follow-ups, not hidden implementation claims.

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
