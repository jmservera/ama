---
title: Resident chat launcher 520 changes
ms.date: 2026-10-30
---

## Metadata

Task ID: 520. Task slug: resident-chat-launcher-520.
Plan: .copilot-tracking/plans/2026-10-30/resident-chat-launcher-520-plan.md.
Details: .copilot-tracking/details/2026-10-30/resident-chat-launcher-520-phase-details.md.

## Execution Status

Full plan in scope. Complete: P01, P01-T01, P01-T02, P02 and P02-T01.
Approved boundary: resident routing/dispatch, intro text, existing tests/browser
check and API guide; no dependencies, projection, SQL, deployment or AI activation.

## Execution Summary

Research and one independent critique complete; original Revise verdict preserved.
PC-001 concerns a worker-specific /tmp restriction, not the parent environment.
The parent used the caller's exact shared lock successfully; no alternate lock.
Existing implementation baseline: 27 resident chat API tests pass (20.032s).

## Completed Work

### Grounded document questions (P01-T01)

chat.py now accepts bounded complete missing/provision/warning/error variants.
app.py sends typed documents through the existing fixed-topic advisor, keeping
mandatory facts/citations and truthful disabled/failure/suggestion labels.
Other typed generation unchanged. assistant.js adds ordinary question examples
and retains native shared widget/Fluent-derived styling and consent/manual paths.

### Regression and guide reconciliation (P01-T02)

Expanded existing parameter lists, moved ordinary warning wording from refused
to supported, and preserved combined/action refusals. One new API method tests
17 document questions with AI off/success/transport failure/arbitrary prose
rejection, distinct second-resident data, forged header and prompt isolation.
Late-revocation test now exercises typed and topic requests. Existing generated
tests still exercise every non-document record question. Browser latest-reply
cases and API guide updated. No test removals or new files.

## Implementation-Time Plan and Detail Updates

No scope/user decision changes. Baseline system python3 can run API tests, but
has no installed project distributions, Ruff or Playwright. A missing ruff
command stopped the first formatting/test command before tests ran. Existing
/tmp/mv Ruff was used read-only for formatting; it was not modified.
Create a task-owned external pip environment for consistent installed source
and browser/type/lint checks rather than mutate the shared environment.

## Validation Record

| Check | Scope | Status | Evidence |
| --- | --- | --- | --- |
| Pre-change focused API suite | test_resident_chat_api | Passed | 27 tests, 20.032s; exact shared flock and requested PYTHONPATH with python3 |
| Changed focused suite | chat API, agenda, assistant API, Azure advisor fake transport | Passed | 61 tests, 28.855s; system python3, exact shared flock |
| Full API discovery | P02, exact requested PYTHONPATH and python3 command | Passed with skips | 1380 tests, 481.873s, 320 opt-in/integration skips; /tmp/ama-520-20261030-validation/api-unit.log |
| Ruff check | Entire src/api | Passed | /tmp/ama-520-20261030-validation/ruff-check.log |
| Ruff format --check | Entire src/api | Passed | 61 files already formatted; /tmp/ama-520-20261030-validation/ruff-format.log |
| mypy | Entire configured API scope | Passed | 117 source files; /tmp/ama-520-20261030-validation/mypy.log |
| JS syntax and diff | Changed assistant.js; all diff | Passed | node --check and git diff --check |
| Actual loopback Playwright/axe | Existing resident chat, agenda, session and responsive harness with extended document questions | Passed assertions | /tmp/ama-520-20261030-validation/browser/report.json; Chromium 156.0.8078.4; axe 4.10.3 digest verified, 32 scoped scans, zero violations |

Validation used /tmp/ama-520-20261030-venv with current core/agents/api editable
distributions installed via pip and project-pinned dev tools. Full checks held
flock -w 600 /tmp/ama-rpi-heavy.lock. The browser check starts/stops its real
loopback server and proves responsiveness by HTTP/sign-in/view/chat/agenda
requests with constructed credentials/data only; zero external application
requests and zero page errors. No live sign-in or model connection.

The browser scans retain 18 color-contrast and 25 aria-valid-attr-value incomplete
entries. These are not passes or demonstrated violations. They need review
beyond axe's scoped automatic determination; full conformance is not claimed.
The 320px/200% text-resize screenshot was inspected. It is narrow reflow with
wrapped text/controls, not native zoom or human comprehension evidence.

## Pre-Review Reconciliation

Plan/details checked against completed changes; all P01/P02 tasks complete,
no implementation work pending. Ready for the single independent Review.
Validation limitations and follow-ups current; local publication gate remains
after original Review and local commit. No approval checkbox was completed.

## Blockers

None currently. Missing full-gate prerequisites will be recorded, not bypassed.

## Remaining Work

One independent Review, local commit, then complete gate at exact committed head.

## Follow-Up Items

Owner live authenticated acceptance and human/AT acceptance remain pending,
outside local authorization.
