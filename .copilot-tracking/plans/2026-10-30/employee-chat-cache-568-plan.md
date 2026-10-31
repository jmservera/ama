---
title: Employee chat and release cache implementation plan
ms.date: 2026-10-30
---

## Task Metadata

* Task ID: 568
* Task slug: employee-chat-cache-568
* Planning status: Ready; original critique Revise, direct dispositions complete
* Plan date: 2026-10-30
* Phase details: .copilot-tracking/details/2026-10-30/employee-chat-cache-568-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-30/employee-chat-cache-568-plan-critique.md

## Executive Summary

Make release changes visible on the next normal page load on both sites through
content-derived asset versions, non-stored HTML and mandatory asset revalidation.
Retain the existing shared chat fix and strengthen browser evidence using the
ordinary launcher, without resetting or reinstalling the employee widget.

### What You May Not Know

The supplied base already contains shared chat and the employee focus fix.
Historical employee deployed bytes are unavailable; this work must not claim
live acceptance. Existing `no-store` headers alone cannot invalidate a previously
fresh browser entry at the same old URL.

### Unresolved Decisions or Blockers

None for implementation. Publication/full gate and human/live acceptance remain
separate; no push is authorized.

## Sources

* .copilot-tracking/research/2026-10-30/employee-chat-cache-568-research.md: C3-C9 and W1.
* src/api/README.md: shared chat contract and local browser harness.
* src/README.md: test commands and local gate/publication boundaries.

## User Decisions and Requirements

* Complete research, plan, implement, review in that order with dated evidence.
* Ensure employee and resident use shared chat; Return/Send retains the answer.
* Fix stale JS/CSS/library delivery on both sites and add regression tests.
* Work on supplied branch/base; source under src; tests outside package; pip only.
* Preserve Fluent 2, native semantics, WCAG baseline, plain content and reduced motion.
* Run requested full API discovery, Ruff, format, mypy and real local Playwright.
* Serialize heavy work with `flock -w 600 /tmp/ama-rpi-heavy.lock`.
* No Azure, deploy, live sign-in, credential access, push or issue-closing directive.
* Commit locally using the requested coauthor trailer and Refs #568.

## Goals

Deliver coherent, fresh packaged code on both sites and preserve chat focus,
visibility, manual dismissal, consent and authenticated-context boundaries.

## Scope and Non-Goals

Scope: shared static helper, staff server and recovery loader, resident showcase
and loopback preview entry points, HTTP/unit/browser regressions and API guide.
No framework change, visual redesign, live identity/model or deployment work.

## Functional Requirements

* FR1: both sites load byte-identical shared widget assets.
* FR2: Enter and Send keep chat/answers visible; deliberate dismissal never reopens.
* FR3: packaged JS/CSS changes alter initial HTML asset URLs including vendored
  libraries; retry uses the exact initial versioned URL.
* FR4: HTML/API/errors remain no-store; static assets use byte ETags and
  `no-cache, must-revalidate`; matching conditional GET/HEAD returns empty 304.
* FR5: stale versions never receive an immutable promise or stale bytes.
  Keep existing authorization, host restrictions, allowlists, CSP and MIME types.

## Non-Functional Requirements

* Snapshot packaged files once per handler creation, with deterministic SHA-256
  release identity including file names and bytes; no git/build/runtime secrets.
* Preserve startup dependency recovery limits and native focus/keyboard behavior.
* No new dependency or in-package test; no user content or identity in asset hashes.

## Acceptance Criteria

* AC1: real loopback employee/resident Enter and mouse Send retain visible replies,
  launcher expanded state and composer focus, including employee route refresh.
* AC2: every served entry-point JS/CSS URL is versioned; any asset change selects
  a different release URL, including shared widget and vendored Leaflet.
* AC3: actual sockets prove cache headers, body-derived ETags, 200 changed
  validators, empty 304/HEAD, unversioned/old-version revalidation and no-store
  HTML/API/denials on both applications.
* AC4: ordinary dependency recovery preserves initial asset version and remains bounded.
* AC5: requested API checks and local browsers have explicit outcomes; missing
  prerequisites and nonlocal/human acceptance are not reported as passing.

## Implementation Context Record

Research: .copilot-tracking/research/2026-10-30/employee-chat-cache-568-research.md.
Plan/details/critique use this task slug and date. Implementation owns
.copilot-tracking/changes/2026-10-30/employee-chat-cache-568-changes.md.
Parent continues sequentially when critique findings are disposed.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Release-safe delivery and regressions

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Share versioned static delivery

Add one typed shared helper; wire three existing handlers, retaining their
admission checks. Version HTML src/href only for known packaged files.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Preserve recovery identity and prove chat integration

Resolve recovery URL from initial script elements, retaining query versions.
Strengthen current browser check with no-reset ordinary launcher submissions.

<!-- rpi:task id=P01-T03 -->
#### [x] P01-T03: Validate and document

Add socket/content identity tests, run focused then full checks and both-site
browser exercises, update API guide and dated changes evidence.

## Test Ownership and Change Budget

API owns tests in `src/api/tests/` and harnesses in `src/api/checks/`.
Removals: none. Maximum additions: one new unit/HTTP test module and one new
browser harness if release simulation cannot fit the existing check; prefer
extending existing harness. Existing header expectations may be corrected only
where static policy intentionally changes. Canonical code is packaged source;
generated screenshots/results stay external. Semantic coverage: version identity,
conditional HTTP, auth/cache separation. Regression coverage: both chat send
methods, refresh/dismissal, initial/recovered versions and browser warm-cache
navigation across a constructed release change. No test count is an acceptance proxy.

## Dependencies

Existing pip environment `/tmp/mv`, Node, Playwright/Chromium, heavy lock.
Q1-Q3 research is complete. P01-T02 depends on P01-T01; P01-T03 covers both.

## Critique Disposition

One independent critique executed; original verdict Revise is preserved.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Rejected: conflicts with caller direction and this host's actual instructions | User explicitly requires `/tmp/ama-rpi-heavy.lock`; no parent-host prohibition on `/tmp` exists. Use supplied lock and existing `/tmp/mv`, external evidence under session storage. Critique worker restriction does not extend parent authority. |
| PC-002 | Applied | P01-T03 details now require same-origin/context release turnover, legacy fresh cache priming, executed JS/applied CSS and server-observed retry URLs. |
| PC-003 | Applied | P01-T02 details require real local thread/ask happy paths for both employee activations without reset/install or fulfilled responses. Controlled race matrix retained. |

## Follow-Up Items

* None.

## Handoff

Implementation P01 complete; requested local checks and both browser harnesses
passed, with 320 discovery skips explicitly recorded. Ready for one independent
post-implementation Review. Full publication gate, hosted checks, human and
live-site acceptance remain separate; no push is authorized.
