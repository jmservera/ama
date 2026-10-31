<!-- markdownlint-disable-file -->
---
title: Versioned asset cache headers implementation plan
description: Local RV-001 correction with guarded immutable URLs
ms.date: 2026-10-31
---

## Task Metadata

* Task ID: 12a8273a-1cfb-42aa-ae85-97f032ffafbd.
* Task slug: versioned-asset-cache-headers.
* Planning status: Ready; single critique Complete / Revise preserved, PC-001 rejected with evidence.
* Plan date: 2026-10-31.
* Phase details: .copilot-tracking/details/2026-10-31/versioned-asset-cache-headers-phase-details.md.
* Plan critique: .copilot-tracking/reviews/plans/2026-10-31/versioned-asset-cache-headers-plan-critique.md.

## Executive Summary

Give static URLs containing exactly the current release version a one-year public immutable cache policy across the employee app and both resident handlers. Preserve no-store HTML and no-cache bare/obsolete assets, including ETags and conditional GET/HEAD. Extend actual-handler tests and existing browser checks, then perform one independent Review and commit locally.

### User Decisions and Requirements Highlights

* Refs #568 only; no issue closure, Azure, secrets, push or workflow edits.
* Run the exact requested API unittest, Ruff lint and formatting commands.

### What You May Not Know

* Old version URLs serve current snapshot bytes; they must not gain immutable policy merely because `v` exists.
* Fresh immutable browser cache reuse should not require 304; validate reuse and explicit conditional HTTP separately.
* This source correction does not change the original redeploy Review or prove live deployed acceptance.

### Unresolved Decisions or Blockers

* None preventing implementation. Publication and human/live acceptance remain outside this local-only task.

## User Decisions and Requirements

* Execute research, plan, implement, review in that order with dated tracking artifacts.
* Address RV-001 High from PR #596 using its original remote Review.
* Serve content-version static URLs with `public, max-age=31536000, immutable` on employee and resident apps.
* Keep HTML and unversioned assets no-store/no-cache; source stays in src and tests outside packages.
* Add focused unit tests and keep browser checks passing.
* From src/api run supplied PYTHONPATH unittest discovery, ruff check and ruff format --check.
* Do not edit .github/workflows; no Azure, secrets or push.
* Commit locally with Refs #568 and Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>.

## Goals

* Prevent stale-library recurrence on new page loads while allowing safe reuse of content-versioned dependencies.
* Keep one shared header contract across all serving paths.

## Scope and Non-Goals

* In scope: shared Asset/StaticAssets, three HTTP callers, test_static_assets, existing test_ui_support header assertion, asset-cache/workspace browser checks, API README and dated evidence.
* Non-goals: auth redesign, UI changes, deployment, private data, workflow edits, cloud or publication.

## Functional Requirements

* FR1: Non-HTML assets with exactly one decoded current `v` receive the exact immutable header.
* FR2: HTML always no-store and never 304, regardless of query or validator.
* FR3: Absent, blank, obsolete, duplicate or unrelated version queries retain no-cache/must-revalidate and byte ETags; current bytes remain compatible.
* FR4: GET, HEAD and 304 use the same query-aware policy; guard ordering and no-store error/API paths stay intact.

## Non-Functional Requirements

* One centralized query classification, no new dependency or workflow.
* No mutable serving snapshot or historical version store introduced.
* Preserve exact source/test ownership and existing validators.

## Acceptance Criteria

* AC1: Actual employee, resident demo and resident preview requests show exact immutable policy on every rendered versioned dependency.
* AC2: Same endpoints prove HTML no-store even with a current version and matching wildcard validator, and bare/stale/blank/duplicate assets no-cache on GET/HEAD/304.
* AC3: Focused tests cover release identity, shared/vendored assets, unrelated queries, encoded current version and changed-release old URLs.
* AC4: Existing local browser checks prove legacy cache turnover, fresh versioned reuse, failure recovery, exact policy, explicit ETag 304 and ordinary chat submission.
* AC5: Requested API unittest discovery, ruff check and ruff format --check pass, with actual results recorded.
* AC6: One independent critique and one post-implementation Review recorded, reconciled plan/details/changes, local Refs-only commit with trailer; no remote/cloud changes.

## Implementation Context Record

| Context item | Record |
| --- | --- |
| Research | .copilot-tracking/research/2026-10-31/versioned-asset-cache-headers-research.md; executed, Ready, C1-C9 |
| Changes | .copilot-tracking/changes/2026-10-31/versioned-asset-cache-headers-changes.md; implementation-owned |
| Review | .copilot-tracking/reviews/logs/2026-10-31/versioned-asset-cache-headers-review.md; one independent assessment |
| Continuation | Explicit automatic full loop; no routine confirmation |

## Sources

* Owner 2026-10-31 instruction and original remote PR #596 Review RV-001.
* Research C1-C9 establishes snapshot, caller and regression contracts.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement shared cache policy and regressions

* Intent: one policy, all callers and directly related docs.
* Dependencies: Research Ready and single critique disposition.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Make asset headers query-aware across all handlers

* Retain snapshot version on Asset; parse raw query in headers with blank values retained.
* Pass request query from employee and resident routes without moving guards.
* Detail section: P01-T01.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Extend focused unit/browser coverage and README

* Update existing exact-version assertions; add negative version matrix and HTML validator coverage.
* Keep bare Leaflet browser assertion; add versioned counterpart.
* Add browser origin-count assertion for fresh immutable reuse plus explicit conditional GET.
* Detail section: P01-T02.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate and reconcile implementation

* Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Run requested API commands and relevant browser checks

* Exact unittest discovery, ruff check, ruff format --check.
* Existing modules: checks.asset_cache_browser_check, checks.workspace_scripts_browser_check, checks.chat_submit_browser_check.
* External outputs under /home/azureuser/.copilot/session-state/12a8273a-1cfb-42aa-ae85-97f032ffafbd/files/; shared heavy lock.
* Detail section: P02-T01.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Reconcile artifacts and prepare independent Review

* Record actual commands/results, amendments/divergences and remaining gates.
* Detail section: P02-T02.

<!-- rpi:phase id=P03 -->
### [x] P03: Independent Review and local persistence

* Dependencies: P02.

<!-- rpi:task id=P03-T01 -->
#### [x] P03-T01: Perform one independent post-implementation Review

* Read-only source/evidence comparison; write only Review artifact.
* Route findings to distinct follow-up; no repeat Review or in-task repair after Review.
* Detail section: P03-T01.

<!-- rpi:task id=P03-T02 -->
#### [x] P03-T02: Record outcome and commit locally

* Resolve gh api user to privacy-safe repository-local email; no secrets.
* Commit exact local work with Refs #568 and required trailer, verify resulting metadata and clean status.
* No push or publication receipt claim; full publication gate remains required before any later publication.
* Detail section: P03-T02.

## Dependencies

* Existing Python 3.12, source PYTHONPATH, Ruff and Playwright/Chromium; restore dependencies only after missing-dependency failure.
* Original remote review ref is locally available; no Azure or live endpoint needed.

## Test Ownership and Change Budget

* Canonical focused unit owner: src/api/tests/test_static_assets.py; existing src/api/tests/test_ui_support.py changes only its versioned-script header expectation. All package tests stay outside src/zava_forward.
* Exact removals: none.
* Maximum additions: three focused test methods, parameterized rather than duplicated; no new test files or tooling.
* Canonical browser targets: existing asset_cache_browser_check.py and workspace_scripts_browser_check.py; chat-submit check unchanged.
* Semantic coverage: exact version recognition, stale/ambiguous queries and HTML precedence.
* Regression coverage: handler GET/HEAD/304, release turnover, actual browser cache reuse/recovery and existing chat behavior.
* Generated outputs: external session files only; no screenshots/binary evidence in repository.
* Validation evidence: actual commands, exits and summaries in changes; no inferred passes.
* Implementation amendment: full discovery exposed the existing test_ui_support versioned-header expectation and missing runtime/distribution dependencies. Correct only that in-scope assertion; restore distributions in an isolated external venv after the actual missing-dependency failure. No new tests/owners beyond this existing assertion, no tooling or dependency manifest changes.

## Critique Disposition

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 Medium | Rejected: asserted environment restriction is absent from parent instructions | Current host instructions permit /tmp operations; src/README.md local RPI gate explicitly requires shared /tmp/ama-rpi-heavy.lock. Replacing it with a private lock would defeat cross-worktree heavy-run coordination. External result storage follows retention policy; no README lock rewrite or source-tempfile change is authorized. |

* Critique execution: Complete; original verdict Revise remains unchanged.
* Final readiness: Ready after disposition; no remaining applicable critique findings. No second critique.

## Follow-Up Items

* Owner-authorized live cache acceptance remains outside local source scope; requires separate deployment/sign-in authority (original Review C2).

## Handoff

* Ready for implementation after single critique disposition.
* Changes artifact: .copilot-tracking/changes/2026-10-31/versioned-asset-cache-headers-changes.md.
* All P01-P03 tasks complete. Independent Review execution Complete, outcome Conformant with justified divergence, no actionable findings.
* Local implementation/original-evidence commit b516db894c3e7d02e11ccd726a9b1a7ec73f5c83 verified, including privacy-safe author/committer, Refs #568 and exact Copilot trailer. This closeout records completion after the actual commit; no source change or repeat Review.
* Final API discovery passed: 1430 tests, 320 existing skips; Ruff check and format passed; all three selected browsers passed after isolated dependency restoration.
* No unresolved source requirement decision; publication/live/human gates are not established.
