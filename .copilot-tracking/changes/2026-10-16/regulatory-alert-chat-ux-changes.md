---
title: Issue 215 implementation changes
description: Evidence and remaining acceptance boundaries
ms.date: 2026-10-16
---

## Scope and starting state

Full plan P01/P02. Existing topic feat/regulatory-alert-chat-ux-215 was clean,
has no open PR and contains merged dependency commits. No branch move needed.
Research completed; one critique reconciled in plan/details.
Source writes limited to src/api, related READMEs, KB index/log and requested
RPI artifacts. No private data or Azure use. First boundary P01-T01.

## Validation intent

Local SQL-backed browser fixture, automated axe and keyboard interaction,
targeted API/core regressions, ruff/mypy. Initial system Python lacked Playwright;
pip rejected global installation under externally-managed-environment policy.
Use isolated session virtualenv rather than bypass policy.

## Acceptance boundary

Staff comprehension Not run/unmet. Full WCAG conformance unassessed; automated
and keyboard evidence only. Operational approval and chat-value ship test unmet.

## P01 presentation implemented

Updated API web app/chat/style assets: visible home alerts use existing scoped
GET, all six required fields and retained-risk/current-control metadata. Role
guidance uses existing staff roles; supplier view has contract-gap/contact
guidance without chat/law access. Structured cited chat uses unchanged sections,
source dates and links, explicit no-source and disabled states. Plain-language
mode adds explanations, never rewrites source quotes or changes authority.
Doubt route preserves focus and reports the actual receipt or error.

Local app execution reached alerts, answer, missing-source, persisted inbox,
reload, source-change retained risk, outage and disabled lookup. Axe initially
found invalid list-item ancestry caused by role=log replacing list semantics.
Moved log role to a wrapper around the ordered list, including ordinary chat.
Subsequent executed scans passed those states. API targeted regressions: 86
passed. Browser role-loop fixture needed its cached synthetic staff map updated;
this was test setup, not a runtime authorization change. API mypy now resolves
shared API tests via its explicit tests search path; no typing exemption added.

## P02-T01 and P02-T02 evidence

Browser check completed on the real local app with health/readiness verified by
the shared HTTP fixture. Seventeen axe states: no detected violations, eight
states with unresolved color-contrast incompletes on textareas (axe reports
partially obscured background). Do not promote these incompletes to passes.
Native Enter/Space, sequential Tab/Shift-Tab, visible focus and post-turn/doubt
focus passed; 320/390/1280px and 200% text at 320px passed overflow assertions.
Actual persisted inbox/history, no source, source change retained risk, actual
law-store outage, disabled lookup, seven staff mappings and contractor denial
were exercised. Browser external requests and provider inference were blocked.

API regression command used API tests before core tests in absolute PYTHONPATH
to avoid colliding test names. 86 tests passed. Core regulatory chat/rule engine:
33 passed. API ruff check, ruff format --check (16 files) and strict mypy
(46 source files) passed. JS syntax and git diff --check passed.
Updated API README with exact audience/account crosswalk, reproducible commands,
observed limits and predeclared real-staff trial protocol; updated KB index and
appended log. Staff trial remains Not run. Full WCAG acceptance and chat-value
ship test remain unmet; operational source/owner approval is not claimed.

Ready for one bounded Review; P02-T03 delivery remains outstanding.

## Final assessment and bounded correction

During review preparation, captured the sent regulatory question before awaits
and preserved any newly typed draft instead of logging/clearing changed text.
A delayed actual local render now verifies both original question and next
draft. This necessary source correction during preparation diverged from the
nominal review-only write boundary; no second critique or Review was run.
Final browser exercise again passed 17 states with the same eight contrast
incompletes, and 86 API regressions again passed. Final ruff/format/mypy passed.

One post-implementation Review completed with outcome Residual work: RV-001
accessibility assessment, RV-002 authorised staff comprehension and RV-003
operational delegates/sources/ADR ship test. No conformant outcome claimed.
The sanitized browser result is persisted beside the review. Implementation
scope complete; P02-T03 commit/push/PR publication still pending.

## P02-T03 delivery completed

Feature commit 82bd6c2 published on feat/regulatory-alert-chat-ux-215.
PR https://github.com/jmservera/ama/pull/354 targets main, uses Refs #215,
audits all five criteria and leaves staff/WCAG acceptance unmet.
Authenticated account resolved to jmservera / 8036360; repo-local privacy-safe
author/committer email and required Copilot trailer used. No force push,
history rewrite, merge, issue-checkbox update or Azure action.
All active plan tasks are complete; remaining work is the three routed
acceptance/evidence follow-ups, not unreported implementation work.

## P03 starting state and validation intent

Owner requested both independent CHANGES findings on d79a737, existing branch
and PR #354. Clean starting worktree verified. Merged origin/main as 91ed90e;
resolved only docs/reference/log.md by retaining both complete append-only
histories. Authenticated privacy-safe local email and Copilot trailer used.
P03 is the only active scope; original critique and Review stay historical.
Next: wire CI, optional hash-pinned axe, all-control bounding boxes and exact
CSS-deletion mutation. Validate actual local SQL-backed app plus targeted unit,
ruff/format/mypy; update PR and push without waiting, as explicitly requested.
Missing local Playwright/ruff/mypy permits pip dependency restoration.

## P03-T02 CI execution and explicit fallback

Added the regulatory harness to the existing src-api browser step and strict
isolated lint/format commands. Absolute test paths resolve installed packages
and shared fixtures. Bounded curl downloads axe 4.10.3; the existing SHA-256
guard remains mandatory for supplied scripts. Download failure warns, omits
only axe and still runs all other assertions. JSON records executed/skipped
status and the workflow uploads it. No blanket continue-on-error.

Executed the exact new workflow shell block locally with genuine download
and deliberately failed curl, each exit 0 after 17 real local app states.
Wrong-hash content fails before app startup (unit-tested). Hosted CI is pending;
owner explicitly says not to wait after pushing. No hosted pass is invented.

## P03-T03 measured targets and CSS mutation

Every scan now measures visible enabled controls, links and summaries in the
changed surfaces, including the outer chat and cited-lookup disclosure.
Require width/height >=24px; retain the existing summary's stronger 44px design
height. The initial real run detected 18px-high citation links; changed only
their regulatory CSS to inline-block/min-height 1.5rem. This directly coupled
runtime fix is within the approved boundary. Static supplier guidance has no
interactive targets and is explicitly distinguished from empty staff surfaces.

Both CI paths measured 142 targets across 17 states; minimum width/height 24px
and summary height 44px. Deleted the exact regulatory summary rule from the
served stylesheet, ran the no-axe browser harness and required nonzero exit.
It failed at cited-answer with:
`Target size below 24px width / 44px height: <summary>Cited regulatory lookup (synthetic-demo)</summary> (1198 x 24)`.
Restored the rule immediately; both exact CI shell paths then passed. The
unstyled 24px summary is already AA-sized; this mutation protects the stronger
shipped design, not a fabricated AA violation. Axe still has eight incomplete
contrast states and zero detected violations; no full conformance claim.

## P03-T04 local evidence and publication preparation

Missing tools restored with pip into an isolated session virtualenv, editable
core/agents/API distributions installed. No private datasets or Azure used.
86 targeted API tests and 33 core tests pass; three new harness tests cover
24px boundaries, 44px design retention, static supplier exemption and corrupt
axe. API ruff, format (17 files), strict mypy (47 files), isolated harness
lint/format and existing design-system browser pass. Updated READMEs, KB
index and appended log; criterion audit still keeps full WCAG/staff testing
unmet. PR body update and ordinary commit/push remain the delivery actions.
