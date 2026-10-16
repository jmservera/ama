---
title: Issue 200 source cut-over review
ms.date: 2026-10-16
---
<!-- markdownlint-disable-file -->

## Scope and Evidence

Task #200 / `repoint-ci-to-src-200`; review date 2026-10-16. One post-implementation
Review for the complete local source cut-over task, not approval of remaining
Azure/private-data/owner acceptance.

* Research: .copilot-tracking/research/2026-10-16/repoint-ci-to-src-200-research.md
* Plan: .copilot-tracking/plans/2026-10-16/repoint-ci-to-src-200-plan.md
* Details: .copilot-tracking/details/2026-10-16/repoint-ci-to-src-200-phase-details.md
* Critique: .copilot-tracking/reviews/2026-10-16/repoint-ci-to-src-200-plan-critique.md
* Changes: .copilot-tracking/changes/2026-10-16/repoint-ci-to-src-200-changes.md
* Runtime evidence: .copilot-tracking/changes/2026-10-16/repoint-ci-to-src-200-validate.py
* Acceptance: issue #200 body/comments, caller constraints, ADR 0006 updated
  context and cut-over notes, merged src READMEs.

## Opening Review State

Goal: compare actual src path changes and measured local evidence against the
plan and issue criteria, preserving honest unmet gates. Source implementation,
details, plan markers, critique dispositions and changes evidence are reconciled.
P02-T03 intentionally awaits this Review and subsequent publication.
Initial comparison: API entry point/CI probes, isolated images/Bicep identity
preservation, data/tooling paths, documentation and evidence limits.
Read-only boundary: only this review record is changed by Review.
Initial blockers: none for comparison; cloud/owner gates remain outside scope.

## Execution Status

Complete: one direct review of the entire supplied boundary. No review worker or
second Review ran. Source diff, new resolver/evidence harness, current artifacts,
test results and protection of historical records were compared.

## Plan-to-Change Reconciliation and Completed Work Assessment

| Marker | Observed changes and evidence | Assessment |
| --- | --- | --- |
| P01-T01 | API __main__ delegates server.main; Docker CMD uses ADR entry point; both src-ci version sites explicitly print, unchanged names/job IDs asserted against HEAD; loopback module run healthy | Reconciled |
| P01-T02 | API no longer copies/packages orchestrator; jobs use orchestratorImage; commands and identities/grants unchanged; compiled Bicep regression and all four image checks pass | Reconciled |
| P01-T03 | Shared core data_paths resolver handles default/folder/custom JSON, factory and generator agree; synthetic tools reuse it; branding policy/web/logo target src; no mvp output assertion | Reconciled |
| P02-T01 | Full five suites, static tools, focused final generator rerun, Bicep/infra, branding, namespace, four-image/local API and added-link/syntax/guards recorded | Reconciled; live-platform and skipped checks explicitly limited |
| P02-T02 | Source/API/orchestrator/infra/branding guides, root README, instructions and knowledge-base index/log aligned; dated historical recipe preserved | Reconciled |
| P02-T03 | This single Review is executed; commit/push/main PR remains the parent publication action | Not an implementation gap; publication after Review |

## Implementation-Time Update and Critique Assessment

The data resolver was extracted from synthetic into core rather than imported
from synthetic by runtime, preserving ADR dependency boundaries and existing
folder/file semantics. The isolated stock-fabric fixture now copies this required
module; the initially failing full suite was rerun successfully. Generator
custom-filename parity was tightened and a focused 14-test rerun passed after
the full suite. These are directly related corrections, reconciled in details
and changes, not unapproved feature scope or SQL/authorization changes.

PC-001 was rejected because its claimed workspace-only restriction is not a
parent constraint and contradicts the caller-approved /tmp/zf164 tool path.
PC-002 was applied with explicit print probes at both sites. Exactly one critique
ran; no significant or divergent decision needed new human authority.
Four focused methods were added, under the ten-method lock, with no removals.
No general lint cleanup, new ignore configuration or dependency upgrades.

## Validation Evidence

| Scope | Status | Evidence |
| --- | --- | --- |
| Five project unit suites | Passed | 393 core, 517 API (101 skips), 70 agents, 17 orchestrator, 39 importer; 1,036 run total |
| Final generator refinement | Passed | 14 tests after final edit, mocked fictional register, exact output filename and deterministic bytes |
| mypy/ruff/format | Passed | All five projects; core repeated after final edit |
| Bicep build/lint, infra | Passed | Bicep 0.48.1, compiled image/command assertion, 78 infra tests |
| Branding tool | Passed | 25 tests; packaged policy hash, web styles/logo, no mvp recreation, historical identifiers retained |
| Local app and images | Passed | Installed module /healthz 200 outside checkout; four images UID 10001, no data, read-only, no capabilities; exact API PNG and package isolation |
| Workflow/namespace/docs/guards | Passed | Unchanged names/IDs, five installed namespace paths, explicit version stdout, ten added link targets, JS syntax, clean whitespace and no tracked data |
| SQL Server, Azure, actual models, optional browser | Not run / skipped | Explicit SQL/browser opt-ins unset, azure-core missing in local venv, no cloud/inference needed for path-only verification |
| Private relocation/encrypted backup | Not run | Owner-only gate; no private input read |

Initial dependency and isolated-fixture failures are disclosed in changes, with
successful reruns. Existing sensor ResourceWarnings are not new failures.
No assertion here converts a skipped test, source configuration, prototype
historical tag or synthetic observation into operational approval.

## Findings and Routed Residual Work

<!-- rpi:review id=RV-001 -->
### RV-001 [Medium]: New-tag Azure deployment acceptance remains unmet

* Related scope: issue image criterion; P02 acceptance limits.
* Evidence: local image IDs/builds and runtime harness only; infra README clearly
  marks source-image instructions as not deployed.
* Impact: local parity cannot prove healthy existing Container Apps revisions
  or scheduled jobs. Do not close #200 or sign the #201 cut-over from this PR.
* Destination: distinct deployment follow-up under #201/#203.
* Next action: use tested immutable API/orchestrator tags with reviewed what-if
  on existing ama resources; verify health/jobs and retain historical tags.

<!-- rpi:review id=RV-002 -->
### RV-002 [Medium]: Private copy/backup and retirement require owner evidence

* Evidence: ADR 0006 private relocation and cut-over gate; only path/ignore/guard
  code is tested. mvp/README.md is unchanged and retained.
* Impact: changing a default path is not evidence that private state was copied,
  backed up or safely retired.
* Destination: owner-controlled #201/#202 follow-up, not agent implementation.
* Next action: owner confirms readable copy/encrypted backup and sign-off
  without exposing data; no agent migration/deletion is authorized here.

<!-- rpi:review id=RV-003 -->
### RV-003 [Low]: Later workflow/check naming remains a deliberate owner choice

* Evidence: issue #200 2026-10-15 comment retains names through cut-over; caller
  explicitly requires recording the naming question. All names and job IDs equal HEAD.
* Impact: an uncoordinated rename could strand required checks.
* Destination: distinct post-cut-over naming/branch-protection PR.
* Next action: owner chooses later names and updates matching required checks
  in the same controlled change. Current PR intentionally does not rename.

## Defects

No in-scope implementation defect found. Findings above are open issue/cut-over
acceptance gates and distinct future work, not fixes to execute inside this loop.

## Outcome and Closeout Routing

Execution: Complete. Outcome: Residual work. Local implementation satisfies its
planned mechanical scope with justified resolver extraction, but the complete
issue acceptance is not established because RV-001/RV-002 remain open.
No conformant full-issue or operational approval is claimed.

| Class | Destination | Next action |
| --- | --- | --- |
| Implementation defect | None | No source follow-up identified |
| Significant decision gap | None in active scope | Existing caller decisions control |
| Material research gap | None in active scope | Local evidence is sufficient for this path change |
| Residual deployment | #201/#203 | RV-001: reviewed new-tag deployment and hosted health/job evidence |
| Owner data/retirement gate | #201/#202 | RV-002: private backup/copy evidence and owner sign-off |
| Later naming | Separate owner-directed PR | RV-003: coordinate workflow/check names and branch protection |

Parent may now publish the reviewed changes and artifacts with `Refs #200`.
No second Review or implementation return is requested. Required owner checkboxes
remain unchecked; later work requires its own selection/authorization.
