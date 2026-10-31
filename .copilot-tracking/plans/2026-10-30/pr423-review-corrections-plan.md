---
title: PR 423 review corrections plan
description: Scoped correction and current-main integration plan
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: pr423-review-corrections-2026-10-30
* Task slug: pr423-review-corrections
* Status: Ready; original critique Revise, both findings applied
* Details: .copilot-tracking/details/2026-10-30/pr423-review-corrections-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/pr423-review-corrections-plan-critique.md

## Executive Summary

Bound transport allocation before buffering, measure each complete serialized
page, correct the current runbook and preserve current-main/remote ancestry.
Supply an accurate local PR-description replacement for the coordinator.
Validate offline, preserve original adverse evidence and commit locally only.
Committed handoff is explicitly pre-gate. A final external supplement binds
actual gate evidence to the unchanged committed HEAD/tree/base.

### What You May Not Know

The PR's remote head is a score-only child of this worktree's starting head.
Its hosted score is 77/100 PASS, but the body mislabels an older full-gate
receipt as current. A fresh exact-head gate and hosted assessment remain
separate; local corrections cannot guarantee a score or remote mergeability.
Main later advanced to f168d079 while local validation ran. Read-only
merge-tree is clean, but the exact-head complete gate's current-main-ancestor
requirement is now a publication blocker for the explicitly pinned candidate.
Do not silently expand the owner's reviewed base.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review in order with dated artifacts.
* Address PR #423 review comments as data; integrate main d986c4c4.
* Use src packages, pip, external tests, local API/static/browser checks.
* Hold the shared heavy lock; no Azure, deployment, live sign-in or secrets.
* Commit with the required Copilot trailer; no push or remote mutation.
* Never use issue-completion keywords; report criteria actually proven.

## Goals

* Eliminate the two concrete transport-bound defects with regression evidence.
* Make the local descendant conflict-free against pinned main.
* Correct operational guidance and separate historical/current validation.

## Scope and Non-Goals

Scope: transport helper/tests, active infra runbook, additive KB index/log
entry, local coordinator PR-body handoff, dated RPI artifacts, merging remote
score child and main while preserving all historical evidence.

Non-goals: deployment or live acceptance; changing scoring rules, recorded
grades or unrelated source; broad UI redesign; remote PR edits/publication.
No application web assets are changed by either intended integration or fixes.

## Functional Requirements

* FR1: download request explicitly limits data to MAX_BLOB + 1 from offset 0;
  reject overflow and listing/download length mismatch before JSON decoding.
* FR2: every plaintext page, including first-page head and items wrapper,
  serializes to at most PAGE_BYTES; reject unpageable head/item or >MAX_PAGES
  before any upload, preserving all accepted items and byte totals.
* FR3: active prerequisites/deployment/cleanup describe default-off
  includeResultBlob, separate container writer approval, private route,
  operator Entra list/read and lifecycle-retained ciphertext, not result tags.
* FR4: local replacement PR body marks run9 historical and current gate
  evidence honestly; coordinator owns applying it.

## Non-Functional Requirements

* Keep existing profile/deadline/cleanup/authentication behavior and DN1-DN5.
* Keep tests in infra/tests; no source-layout or dependency workaround.
* Preserve native Fluent/WCAG/plain-language/reduced-motion boundaries.
* No benchmark or score invention; actual command exits/skips are recorded.

## Acceptance Criteria

| ID | Criterion | Evidence expected |
| --- | --- | --- |
| AC1 | Bounded replacement reads and cleanup on refusal | Requested range assertion plus controller cleanup regression |
| AC2 | All serialized page/head/item boundaries enforced | Near-boundary multipage, exact-bound, escaped/UTF-8, max-count and round-trip tests |
| AC3 | Current runbook and handoff accurate | Current-section inspection; dated receipts unchanged; coordinator body ready |
| AC4 | Local descendant preserves remote PR and main d986c4c4 | Ancestry and merge-tree/content evidence |
| AC5 | Requested API unit, Ruff/format/mypy and local Playwright pass | Actual commands and external logs, any skips explicitly qualified |
| AC6 | One critique and one independent Review retained | Dated artifacts, original verdicts and dispositions |
| AC7 | Clean local committed candidate has full gate receipt | Complete local gate and verification, or explicit blocked result |
| AC8 | Rubric is not low | Existing hosted 77 PASS documented; fresh hosted result required for final published candidate |

## Sources

Research: .copilot-tracking/research/2026-10-30/pr423-review-corrections-research.md
(C1-C6, W1-W5). No repeated Research necessary.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Preserve ancestry and correct transport

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Merge remote score child and pinned main

Merge --no-ff, no commit until reviewed conflicts are resolved. Preserve both
KB index/log additions and main's current score. No history rewrite.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Reproduce and correct the two bounds

First add regressions and demonstrate old behavior fails, then implement
bounded download plus exact serialized-page sizing with retained behavior.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Correct active runbook and prepare coordinator body

Change only current guidance. Update KB index/log for durable qualification.
Keep earlier activation and gate evidence immutable.

<!-- rpi:phase id=P02 -->
### [ ] P02: Validate, independently review and commit

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Execute local tests/static/browser and rubric contracts

Use explicit constructed data only. Required API discovery command exactly as
requested; package Ruff/format/mypy; infra tests and transport lint/types;
existing local Playwright harness starts/stops a loopback app.
Verify installed distributions and editable paths before application scripts;
actual missing dependency results alone authorize pip restoration.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile evidence and run one independent Review

Review current diff against main plus validation evidence. Preserve outcome;
route later findings without repeating this task's Review.

<!-- rpi:task id=P02-T03 -->
#### [ ] P02-T03: Commit and run final complete local gate

Resolve gh account and repository-local privacy email; required trailer.
Run full gate on clean committed candidate with external output; verify
receipt against fetched main. No push. A gate failure stays unmet.
Write final HEAD/tree/base/receipt/log status to a task-owned external
handoff, not the committed proposed body or changes record after the gate.
Any later tracked correction requires a new commit and fresh gate.
At this committed snapshot P02-T03 is intentionally not checked: the final
candidate/evidence commit and actual gate attempt execute afterward.
The authoritative post-commit result is the external final handoff.

## Test Ownership and Locked Coverage

Canonical tests: infra/tests/test_staff_azure.py. No removals. At most ten new
test methods in existing codec/controller classes; update fake download
signature and one failure override as needed. No generated targets.
Semantic checks: exact measured wrappers, preserving complete results and
cleanup. Regression checks: reviewer counterexamples and replacement race.
Current runbook may receive one focused static assertion in existing tests.
No duplicate browser tooling: existing checks/design_system_browser_check.py.
Gate-runner and rubric implementation stay unchanged except merge results.

## Dependencies and Risks

Available tools include Python, Ruff, mypy, Docker, Trivy, actionlint and
ShellCheck; imports/browser prerequisites still need actual verification.
Global heavy lock admission may block. Do not bypass it or inspect foreign
output. All heavy commands use flock -w 600 /tmp/ama-rpi-heavy.lock; runner
already owns that same lock internally and must not be double-wrapped.
Repository ignored generated inputs can invalidate gate; use external
cache/output paths and retention-policy-backed finite cleanup only.

## Critique Disposition

One independent critique executed, original verdict Revise retained at the
critique path. No second critique.

| Finding | Disposition | Resolving change |
| --- | --- | --- |
| PC-001 Medium | Applied directly | P02-T01 now requires interpreter/distribution/editable-path preflight before source-assisted execution |
| PC-002 Medium | Applied directly | P01-T03/P02-T03 distinguish committed pre-gate body from final external HEAD/tree/base-bound supplement |

## Follow-Up Items

* Coordinator must apply replacement PR body and obtain final hosted score,
  human assessment and publication authority. No remote write here.
* Coordinator must reconcile later main f168d079 (or its successor), then
  obtain a fresh exact-head complete gate. The original requested d986c4c4
  integration and its local evidence must not be relabelled as that later base.
* Live private Blob routing, real job/role behavior and signed attestation
  remain operational follow-up, not inferred from offline results.

Original independent Review: Complete / Residual work. No implementation
defect identified; RV-001 High routes newer-main/full-gate dependency,
RV-002 Medium routes remote body/fresh hosted scoring, RV-003 Low routes live
and human acceptance. No repeat Review or source correction in this task.

## Handoff

Changes path: .copilot-tracking/changes/2026-10-30/pr423-review-corrections-changes.md.
Automatic parent proceeds only after critique dispositions are complete.
