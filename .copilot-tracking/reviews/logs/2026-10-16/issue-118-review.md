---
title: Issue 118 implementation review
description: One post-implementation review and honest acceptance routing
ms.date: 2026-10-16
---

Task ID: 118. Slug: issue-118.

## Opening Review State

Review goal: compare the requested container, CI and Bicep scope against
implementation evidence and each original issue criterion.
Scope: full implementation, publication pending P03-T02.
Read-only boundary: all source, plans and evidence; write only this record.
Evidence readiness: all implementation items through P03-T01 have completion
evidence; scan failures and unsupported hosted controls are explicitly recorded.
First comparison: P01 image guard/runtime harness, then P02 compiled controls,
P03 acceptance audit and publication. No Azure execution or private data.
Acceptance basis: user request, original issue body/comments, plan requirements
and the four directly dispositioned critique findings.
Initial blockers: hosted kernel controls unavailable in the selected ACA schema;
all image scans report unfixed HIGH/CRITICAL packages.

## Compared Artifact Set

* .copilot-tracking/research/2026-10-16/issue-118-research.md
* .copilot-tracking/plans/2026-10-16/issue-118-plan.md
* .copilot-tracking/details/2026-10-16/issue-118-phase-details.md
* .copilot-tracking/reviews/2026-10-16/issue-118-plan-critique.md
* .copilot-tracking/changes/2026-10-16/issue-118-changes.md
* docs/architecture/cutover-evidence-pack.md, Deployment Hardening Audit 118
* Source diff and new container helpers/tests; source/infra README changes;
  changed workflows and published local command results.

## Execution and Outcome

Execution: Complete. Outcome: Not accepted for full hardened hosted deployment.
The bounded code delivery and offline evidence are reviewable; material
acceptance gates remain open. No source corrections or repeated Review are
performed by this review.

## Comparison and Reconciliation

P01: each Dockerfile retains the pinned base, hashed dependencies, own packages
and original CMD. Explicit UID/GID and common ENTRYPOINT make default startup
fail closed. The guard uses explicit checks rather than optimizable assertions;
errors include diagnostics, exec preserves process signals. Unit tests cover
each field, denial diagnostics, missing command and exact command forwarding.
Actual Docker tests independently prove mount flags, EROFS, state writes,
five capability sets, NoNewPrivs and five negative launches per image.
The API runs a real server on an empty constructed fixture. Non-API commands
are truthfully version-only, not worker transport evidence.

CI keeps existing job/check names and uses src build context. Scan runs after
successful build even if runtime smoke fails, with per-image JSON retained.
Explicit scan config includes unfixed OS/library HIGH/CRITICAL findings and
uses no ignore list or baseline. The old workflow name remains but it builds
only the source API. No deployment steps were added.

P02: compiled tests check six image consumers, API probes and 2-4 replicas,
default-off gated Premium edge, WAF association, HTTPS and Private Link.
Existing production/private guards remain. Explicit maintenance commands invoke
the guard; no unsupported Bicep security properties were invented.
Disabled Defender creates no pricing resource, avoiding an existing-plan
downgrade, while selected opt-in plans request Standard. Policy remains
DoNotEnforce for new assignments only, not a bypass of existing enforcement.
Cost acceptance and active protection are explicitly absent.

P03: durable audit accounts for every original criterion, tests, image IDs,
failed scans, hosted limitation and human approval boundaries. Reference log
change is append-only. No legacy tree, memory, private dataset or environment
file changed. Publishing remains parent-owned P03-T02 after this review.

Implementation updates preserve user intent: API context exception is necessary
to copy the guard; connection-reset retry is bounded startup handling, not a
success fallback. PC-001 explicit command replaces the initially proposed
args-only change; PC-002 scan failures remain failures; PC-003 uses subTest;
PC-004 confirms the new harness path. All critique dispositions are recorded.
There was one critique and this is the single post-implementation Review.

## Findings and Routing

### RV-001 | High | Hosted runtime enforcement is unmet

Evidence: current ACA schema lacks required mount/capability security settings;
the code intentionally refuses startup without them. Local Docker control
proof does not establish hosted settings. The changed maintenance commands
also require a guard-bearing orchestrator image, not an old preserved image.
Impact: do not deploy new images or apply these job-command changes to the
current running app until hosting supports the contract.
Destination: later rpi-plan, owned by the technical/project owner, to select a
supported configuration/host and private rollout proof. Do not weaken checks.
This is a known acceptance blocker, not a request to deploy in this task.

### RV-002 | High | Unsuppressed image scans fail on unfixed packages

Evidence: Trivy 0.76.0 scans all four final image IDs; each exits 1 with
61 HIGH and two CRITICAL findings, 16 unique CVEs, no FixedVersion. Counts and
critical identifiers are recorded in the durable audit; local JSON is retained
in session files. No application exploitability conclusion is inferred.
Impact: new CI scan gates are expected to be red with the same database/base.
Destination: later rpi-research, owned by the technical/project owner, to
identify a maintained compatible base/remediation path, followed by a distinct
implementation. Never suppress findings, erase package metadata or invent fixes.

## Residual Follow-Ups

Worker transport remains issue 144, not new active implementation work.
Live edge origin approval/health remains issue 143 and must precede public use.
Policy compliance and paid Defender appraisal/activation remain issue 147 under
Juan Manuel Servera's approval boundary. None of these definitions proves
operational readiness or real legal approval under synthetic-only ADR 0005.
The parent publishes the requested PR and leaves issue checkboxes unchanged.

## Validation Evidence

* Passed: four source Docker builds, runtime positive/negative contracts,
  agents dependency isolation, API health/static PNG and writable-state check.
* Passed: core 504 tests (one skip), API 549 (110 skips), agents 70,
  orchestrator 22, importer 39; all five Ruff/format/mypy checks.
* Passed: 126 infrastructure tests; all Bicep build/lint; new helpers'
  isolated Ruff/format and strict mypy; actionlint for changed workflows
  with shellcheck integration disabled; git diff whitespace check.
* Failed: all four unsuppressed image scans, correctly exit 1.
* Not run: Azure deployment/what-if, live runtime/edge/policy changes,
  SQL integration requiring opt-in credentials, tenant setup, human approval.
  These are outside the authorized local-first scope and are not passed.
* Pending at review time: branch CI after publication. It is not represented
  as a successful branch run by this review.

## Final Routing

Full hosted acceptance is Not accepted while RV-001/RV-002 remain open.
Publication of the bounded implementation with explicit findings is permitted
by the user request. Parent owns publication and no automatic merge. No second
Review or return to Implement is initiated inside this completed task review.
