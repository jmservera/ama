---
title: Employee chat and release cache phase details
ms.date: 2026-10-30
---

## Metadata

Task ID 568; slug employee-chat-cache-568. Plan:
.copilot-tracking/plans/2026-10-30/employee-chat-cache-568-plan.md.
Research: .copilot-tracking/research/2026-10-30/employee-chat-cache-568-research.md.

## Phase Index

| Phase | Name | Status |
| --- | --- | --- |
| P01 | Release-safe delivery and regressions | Complete; independent Review next |

<!-- rpi:phase id=P01 -->
## P01: Release-safe delivery and regressions

Scope is static serving and existing shared chat integration, not design or AI
authority. Preserve original evidence and local-only boundaries. Completion is
measured by AC1-AC5, not a deployment claim.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Share versioned static delivery

Context: research C3/C4/C9; HTML has stable URLs despite current no-store.
Targets: new `src/api/src/zava_forward/api/static_assets.py`, `server.py`,
`resident_demo/app.py`, `resident_preview/app.py`.
Use an explicit URL/file map built from existing roots/allowlists and capture
bytes once. Deterministic release digest must account for file names, content,
shared files and vendored code; entry-point aliases use the same rendered HTML.
HTML rewrites only known asset attributes. Keep HTML/API/auth errors no-store,
but let assets revalidate with byte-derived quoted ETags; support weak/list/star
If-None-Match GET/HEAD correctly. Do not send bodies for HEAD/304.
Old version URLs may serve current bytes with mandatory revalidation, never
immutable caching. No auth bypass or cached personalized HTML.

Completion: socket tests verify URLs, cache policy, ETag/body, conditional requests,
HEAD, changed release contents and unchanged CSP/admission. All tests are API-owned.
No unresolved implementation choice requiring owner decision.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Preserve recovery identity and prove chat integration

Depends on P01-T01. Targets: `web/app.js`, existing workspace loader unit tests,
`checks/chat_submit_browser_check.py`.
Recover missing dependency by matching pathname of original script src and using
its complete versioned URL, including shared chat and Leaflet. Retain two-attempt
limits, timeout behavior and session/route guards. Raw source tests may have no
version and must remain usable without DOM-wide assumptions.
Both sites already use shared widget; do not introduce a second composer or
refocus on replies. Add ordinary-open/no-reset browser sends, a real same-context
refresh, deliberate dismissal and shared asset URL/byte assertions.

Completion: browser behavior is measured through actual page event dispatch and
socket-delivered source, not a string-presence assertion alone.
An added employee happy path must use actual local thread/ask replies for both
Enter and mouse Send, without reset/install overrides or ask-route fulfillment.
Assert successful HTTP, added reply, visible panel, expanded launcher and exact
composer focus. Preserve the controlled-delay race matrix separately.

<!-- rpi:task id=P01-T03 -->
### P01-T03: Validate and document

Depends on P01-T01 and P01-T02. Add at most one unit/HTTP module, update existing
intentional header assertions, retain all existing semantic coverage.
Use temporary constructed asset roots for release A/B; browser context stays
warm across normal navigation, no cache-disabling Playwright request routing in
that cache exercise. Verify fresh JS/CSS and dependency retries after initial
failure; block external traffic only in separate chat exercises if needed.
Keep origin/port and browser context unchanged across A/B handler recreation.
First prime legacy unversioned A script/style with a fresh cache lifetime and
demonstrate reuse via server request counts. Switch the server-owned snapshot
to B, navigate normally, assert executed B JavaScript and computed B CSS plus
shared/vendor identity. Also test unchanged-release ETag revalidation and
server-injected first-download failure; record exact versioned retry URL and
bounded counts. Editing snapshot source files alone is not a release turnover.
Run focused tests first, then from src/api:
`PYTHONPATH=src:tests:../core/src:../agents/src:../core/tests:../agents/tests python3 -m unittest discover -s tests -q`,
Ruff check, Ruff format --check and mypy under the heavy lock with existing
pip environment PATH. Start actual loopback apps and use Chromium.
Update `src/api/README.md`; preserve Fluent/native semantics, WCAG and content
baseline. Refresh required web rules before Review. Record actual failures,
skips, browser evidence and acceptance limitations in changes.

Review and publication: one independent Review artifact after implementation;
commit original RPI evidence and code locally. Complete-gate publication evidence
is a separate required boundary, not implied by focused/full API checks.

## Completion Evidence

P01-T01/T02/T03 complete. Final API discovery: 1,384 tests, 487.490s,
OK with 320 skips. Ruff/format and mypy (120 source files) passed. Local chat
and same-origin warm-cache browser checks passed on Chromium 156.0.8078.4.
Original failures, corrections and external output pointers are preserved in
.copilot-tracking/changes/2026-10-30/employee-chat-cache-568-changes.md.
