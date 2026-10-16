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
