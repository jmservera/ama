---
title: Employee chat and release cache research
ms.date: 2026-10-30
---
<!-- markdownlint-disable-file -->

## Research Brief

* Topic: Refs #568, employee chat dismissing on Return/Send and stale employee/resident assets.
* Purpose/audience: evidence for the requested sequential research, plan, implement, review loop.
* Scope: shared chat, both web entry points, static serving, dependency recovery and local regressions.
* Non-goals: visual redesign, Azure, deployment, live sign-in, private datasets, credentials, push.
* Criteria: both sites retain submitted chat; release changes select fresh JS/CSS and libraries; tests exercise actual serving and browsers.
* Output mode: convergence, preparing planning.

## Research Parameters

* Questions: Q1 shared employee/resident chat and focus ownership; Q2 cache/release identity including dynamic dependencies; Q3 suitable local test harnesses.
* Posture: focused (bounded named failures and source targets).
* Evidence root: `.copilot-tracking/research/2026-10-30/`.
* Starting areas: `src/api/src/zava_forward/api/`, `src/api/tests/`, `src/api/checks/`, component guides.
* External scope: required Web Interface Guidelines; framework cache behavior if needed.
* Research source edits: none. Explicit limits: local only, pip not uv; heavy commands use `/tmp/ama-rpi-heavy.lock`; no push.

## Extension Registry and Provenance

| Kind | Selection | Provenance and authority |
| --- | --- | --- |
| Instructions | Selected repository instructions | `.github/copilot-instructions.md`, source/tests/web/evidence/publication boundaries |
| Skills | Selected rpi-research, web-design-guidelines | Phase protocol and fetched web rules |
| Skills | Skipped aesthetic redesign skills | App behavior and delivery fix, no redesign |
| Specialist | Inline research | One tightly coupled code-path trace; delegation adds no independent lane |

## User Participation and Research Decisions

User explicitly requests all four phases in order and local commit without push.
No interaction needed; proceed in requested automatic execution, not an open-ended
automatic follow-up session. Owner feedback is a hypothesis to verify.

## Scope and Success Criteria

Verify Q1-Q3 against current branch `fix/employee-chat-cache-568`, base `d986c4c4`.
Preserve Fluent 2, native semantics, WCAG baseline, reduced motion and manual paths.
Do not assume source defects explain previously deployed behavior.

## Direction Controls

Local-only, synthetic-data-only; Refs #568; no issue-closing directive; no push.
Original evidence and human/hosted gates remain separate from local checks.

## Research Questions

| Question | Type | Status |
| --- | --- | --- |
| Q1: Do both sites use shared chat, and why might employee submission dismiss it? | depth | Open |
| Q2: How do HTML, static assets and recovered libraries avoid stale releases? | depth | Open |
| Q3: Which tests prove actual behavior without live access? | straightforward | Open |

## Prior Knowledge Gate

Read original/addendum, reference index and owner memory; no prior session found
by bounded session lookup. API README describes shared chat and an existing
focused submit browser harness. Those claims require source verification.

## Research Cycle Log

### Cycle 1

#### Wave 1: Wider

Both employee and resident showcase HTML load `/chat-widget.js` and
`/chat-widget.css` (C3). Static handlers already send `no-store`, but HTML and
retry loaders use stable unversioned URLs (C4). Prior issue #568 and the current
README describe a source-level focus fix already in this base (C5).
Reflection: do not duplicate or replace that fix; investigate delivery identity
and reproduce current behavior rather than assume employee has a second widget.

#### Wave 2: Deeper

Verified shared `busy()` moves Send focus into the composer before disabling it;
employee `show()` preserves chat focus and equivalent authenticated refreshes
retain session identity (C6). Existing browser harness covers 12 send combinations,
route/session refreshes, deliberate dismissal and resident actual rules answers
(C7). Employee retry loader sets `script.src = path` without retaining the
original asset URL (C8).
Reflection: version initial assets and dependency recovery together. HTML remains
non-stored; static responses can revalidate using byte-derived ETags.

#### Wave 3: Contrarian

Challenged the hypothesis that employee code lacks the resident fix: source
already shares the widget and includes the focus guard (C3/C6). Historical
deployed bytes cannot be reconstructed locally. Rejected a second employee
widget or unconditional refocusing, which would break deliberate dismissal.
Challenged immutable query caching: an old query served by a new process must
not claim immutable old content. Select versioned URLs plus mandatory
revalidation rather than immutable caching. Include welcome/law HTML and the
loopback resident preview so entry-point aliases cannot bypass asset versioning.
Reflection: cache-safe delivery plus production-shaped no-reset browser regression
is the bounded correction. No further research cycle needed; source paths,
test boundaries and alternatives are covered.

## Evidence Log

| ID | Evidence | Location |
| --- | --- | --- |
| C1 | Clean requested branch at supplied base; no existing PR | `git status`, `git log`, `gh pr list` on 2026-10-30 |
| C2 | Guide claims shared chat and focused submit harness | `src/api/README.md:91` |
| W1 | Current Web Interface Guidelines retrieved completely | https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md (2026-10-30) |
| C3 | Both sites load the identical shared widget | `src/api/src/zava_forward/api/web/index.html:49`, `src/api/src/zava_forward/api/resident_demo/web/index.html:58` |
| C4 | Existing responses use no-store but stable URLs | `src/api/src/zava_forward/api/server.py:43`, `src/api/src/zava_forward/api/resident_demo/app.py:62` |
| C5 | Issue records prior source fix, not deployed acceptance | `gh issue view 568` on 2026-10-30; `src/api/README.md:119` |
| C6 | Shared submit and employee render guards already exist | `src/api/src/zava_forward/api/web/chat-widget.js:86`, `src/api/src/zava_forward/api/web/app.js:93` |
| C7 | Constructed loopback browser harness covers both sites | `src/api/checks/chat_submit_browser_check.py:41`, `src/api/checks/chat_submit_browser_check.py:323` |
| C8 | Recovery retries use an unversioned URL | `src/api/src/zava_forward/api/web/app.js:239` |
| C9 | Resident preview has separate strict static allowlist | `src/api/src/zava_forward/api/resident_preview/app.py:18` |

## Findings Mapped to Questions and Evidence

Q1 answered by C3/C6: shared fix already present; deployed mismatch is unverified.
Q2 answered by C4/C8/C9: version every served HTML JS/CSS link from packaged
content, preserve version in retries, add ETag/mandatory revalidation for assets.
Q3 answered by C7: extend actual socket tests and existing local Playwright
harness; use existing `/tmp/mv` tools after system Python missing dependency.

## Alternatives and Decision State

Select a shared immutable-in-process asset snapshot and content-derived release
version for initial URLs; use `no-cache, must-revalidate` and byte ETags for
non-HTML, `no-store` for HTML/API/errors. Select version-preserving recovery.
Reject headers alone: old fresh cache entries under stable URLs may bypass new
headers. Reject build tooling or duplicated bundles: unnecessary for native
scripts. Reject immutable caching without retaining historical bytes.

## Open Questions, Risks, and Residual Uncertainty

Historical deployed asset bytes and live behavior are unavailable and out of scope.

## Current Decisions

Use the supplied branch; preserve existing shared architecture where verified.

## Potential Next Research

Only re-enter if local source or browser evidence contradicts the selected fix.

## Planning Readiness

Ready. Research disposition: executed, complete. Evidence C3-C9 answers Q1-Q3;
W1 and local UX standards guide the bounded web edit. Self-check: all three
waves complete, alternatives challenged, no source changes during research,
historical deployment uncertainty preserved. Parent continuation: Plan.
