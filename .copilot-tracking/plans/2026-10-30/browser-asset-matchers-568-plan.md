---
title: Browser asset matcher correction plan
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Task Metadata

* Task ID: pr-594-browser-asset-matchers-568
* Task slug: browser-asset-matchers-568
* Planning status: implementation Complete; Review-ready; one critique disposed
* Plan date: 2026-10-30
* Phase details: `.copilot-tracking/details/2026-10-30/browser-asset-matchers-568-phase-details.md`
* Critique: `.copilot-tracking/reviews/plans/2026-10-30/browser-asset-matchers-568-plan-critique.md`

## Executive Summary

Restored actual browser fault injection, request/response waits and coverage observations after PR #594 introduced versioned assets. One shared anchored URL pattern matches a canonical asset suffix with optional version-directory prefix and query/fragment, and is reused in DOM instrumentation. Existing retry, fallback, original-function coverage and cache behavior assertions are preserved. Original CI commands and all seven affected checks passed; 73 relevant tests, API Ruff and mypy passed.

### What You May Not Know

The exact CI browser sequence already reproduced the case-journey timeout. Additional workspace/loading checks are also affected even though CI does not invoke them. A stale Leaflet cache assertion must now expect revalidation and ETags. The app emits query versions only; synthetic segment tests prove matching, not segment-based HTTP serving. No live-site or publication acceptance is implied.

No unresolved implementation decisions. One original critique returned Revise; PC-001 is rejected as inapplicable to the parent execution context and PC-002 is incorporated below. No second critique.

## User Decisions and Requirements

* Correct open PR #594 on existing `fix/employee-chat-cache-568`, Refs #568 only.
* Research, Plan, Implement and Review in order with dated artifacts.
* Update every asset matcher, selector and coverage comparison in `src/api/checks`.
* Prove versioned and unversioned matching; reproduce the workflow failure locally.
* Use pip and src packages, constructed data and the heavy lock; no Azure, secrets or push.
* Validate Ruff lint/format and relevant tests; commit locally with the requested Copilot trailer.

## Goals

* Browser checks continue to exercise actual asset failure/recovery instead of bypassing versioned downloads.
* Preserve exact canonical asset identity and existing behavioral assertions.
* Provide bounded, reproducible local evidence and an independent original Review.

## Scope and Non-Goals

Included: new `checks/asset_urls.py`; seven asset-instrumenting checks (workspace scripts, loading briefing, employee workspace, chat widget, case journey, case-view UX, asset cache); new `tests/test_browser_asset_urls.py`; related API guide.

Excluded: application asset generation, UI redesign, API route matching, old RPI evidence, cloud operations, remote writes and issue closure. Bare HTTP contract requests and legacy priming deliberately remain bare.

## Functional Requirements

* Anchored matching accepts bare, query-versioned and version-directory-prefixed canonical paths, including `/vendor/leaflet.js` and stylesheet assets.
* Reject lookalike filenames, extra trailing paths and asset names occurring only inside queries.
* Use the same regex for Playwright routes/unroutes and request/response waits and its pattern for DOM selection/observation.
* CDP coverage keeps same-origin filtering and original lexical companion count assertions.
* Matching accepts an optional exact origin for routes/waits/coverage. Bind page asset matchers to the owned origin so off-origin lookalikes fall through to the existing context deny guard. Add that guard to shell context; keep warm-cache fixture unrouted because routing disables cache.
* Leaflet response retains MIME/body-length checks and now verifies `no-cache, must-revalidate` and byte-derived ETag.

## Non-Functional Requirements

* Standard library helper only; no dependency/manifest change.
* Preserve harness typing and conventions; Ruff check/format pass for API and isolated strict checks for new code.
* All heavy browser/test executions hold `flock -w 600 /tmp/ama-rpi-heavy.lock`.
* Browser apps use owned synthetic loopback fixtures and block external application traffic.

## Acceptance Criteria

* AC1: original CI sequence fails at the same case-journey fallback assertion before source edits.
* AC2: one matcher test matrix accepts both version forms and bare URLs, rejects false positives, and checks native Playwright route/wait, DOM and coverage semantics.
* AC3: all seven affected browser checks pass after correction; the original CI three-command sequence passes.
* AC4: relevant static-assets/workspace/chat/UX tests and API Ruff check/format pass; type check passes for new code and affected surfaces or baseline discrepancies are explicitly recorded.
* AC5: original critique and Review artifacts, implementation changes and local commit persist; no push or closing keyword.

## Implementation Context Record

Research: `.copilot-tracking/research/2026-10-30/browser-asset-matchers-568-research.md` (executed / Ready, C1-C7).
Changes: `.copilot-tracking/changes/2026-10-30/browser-asset-matchers-568-changes.md`, owned by Implement.
Review: `.copilot-tracking/reviews/logs/2026-10-30/browser-asset-matchers-568-review.md`, one independent post-implementation assessment.

## Sources

Research C1-C7 and original failed CI run 41144371712. Existing pip environment was unusably bound to another worktree; a task-owned pip environment now installs this worktree's src projects.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Correct asset instrumentation

Dependencies: completed Research and one final-candidate critique.

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Shared matching and all browser surfaces

Implement the anchored pattern and use it consistently in seven affected checks. Preserve canonical vendor suffix, CDP origin, exact retry URLs, counts, DOM observation and cache checks.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Regression tests and related guide

Add matrix and native browser instrumentation tests; document version-independent checks and precise local evidence boundaries in `src/api/README.md`.

<!-- rpi:phase id=P02 -->
### [x] P02: Validate the correction

Dependencies: P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: CI replay and affected browser checks

Repeat design-system, regulatory and case-journey workflow commands, then workspace scripts, loading briefing, employee workspace, chat widget, case-view UX and asset cache. Use pinned axe and fresh external output directories under the heavy lock.

<!-- rpi:task id=P02-T02 -->
#### [x] P02-T02: Unit, lint and typing evidence

Run new matcher tests with `test_static_assets`, `test_workspace_scripts`, `test_chat_widget_focus`, `test_case_journey`, `test_design_system`, `test_accessibility_baseline` and `test_content_standard`; run API Ruff check/format and mypy. Reconcile markers, evidence and handoff before Review.

## Test Ownership and Change Budget

Canonical code: new helper and seven named browser files. Canonical tests: `src/api/tests/test_browser_asset_urls.py` and existing relevant suites. Exact removals: none. Maximum additions: one helper and one test file, at most six independently named test methods. Semantic coverage: direct URL classification plus native routing/waits, JavaScript pattern parity and original CDP counts. Regression coverage: existing real browser checks and original CI replay. Generated outputs: external session files only, not committed. No test deletion, timeout relaxation, retries added to hide failures or cache/coverage assertion removal.

## Dependencies

Task-owned pip environment with installed src projects, Playwright/Chromium and pinned axe 4.10.3; all available and already exercised by baseline. No SQL/cloud prerequisite for these constructed JSON browser checks.

## Critique Disposition

| Finding | Owner / disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Parent / rejected as inapplicable | The critique cites a worker-specific file-location restriction absent from this parent context and contrary to the explicit caller command `/tmp/ama-rpi-heavy.lock` and repository external-output policy. Parent tools permit task-owned session output, demonstrated by original successful lock acquisition and baseline runtime. Retain the actual shared lock, external session pip/output paths and existing sanitized fixture cleanup; no bypass or lock rename. |
| PC-002 | Parent / accepted, directly applied | Functional requirement binds page routes/waits and coverage to the exact owned origin; details specify context guards and test off-origin rejection. Warm-cache fixture remains deliberately unrouted: adding Playwright routing disables browser cache and conflicts with the confirmed requirement to preserve real cache evidence. That fixture has no page route precedence issue and serves constructed local files. |

Execution Complete / original verdict Revise / final readiness Ready after these dispositions. Original critique is preserved unchanged.

## Follow-Up Items

* Hosted rerun, full local publication gate and human/live approval remain later owner-authorized work, outside local correction.
* Optional isolated lint of the whole legacy case-view harness exposes ten pre-existing diagnostics (B023/E501), proven against the original HEAD. API-configured lint passes; new helper/tests pass strict isolated lint with the API source-root setting. Do not expand this correction into legacy lint cleanup.

## Handoff

Full-plan P01/P02 Complete; no active implementation markers remain. Automatic parent continues to one independent Review. Local commit follows original Review preservation; no publication or hosted/human acceptance claim.
