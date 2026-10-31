---
title: Employee identity runner phase details
ms.date: 2026-10-31
---
<!-- markdownlint-disable-file -->

## Metadata

Task 570, employee-identity-check-570.
Plan: .copilot-tracking/plans/2026-10-31/employee-identity-check-570-plan.md.
Research: .copilot-tracking/research/2026-10-31/employee-identity-check-570-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Local repair complete; live blocked | P01-T01, P01-T02 |
| P02 | Pending P01 | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Runner integration

<!-- rpi:task id=P01-T01 -->
### P01-T01: Maintained runner and regression

After critique, reuse BINDING in an already-authenticated Page adapter only;
no sign-in/credential entry point. Validate independent expected IDs before
evaluation; exact all-boolean result shape, authenticated strictly true.
Allow only the authorized live origin or explicit local loopback test origin.
Check before/after probe and every stage, recheck identity after navigation.
Reject debug environment before evaluation. Fixed statuses/boolean/count
observations only, never exception/body capture. Caller owns browser lifecycle,
watchdog, independent ID attestation and authorized sign-in accounting.
CLI runs synthetic Chromium regressions only, never reads private files.
Chat: harmless general-work prompt, current selected-skill response and no alert;
record workflow-only versus actual AI label separately.
Map: explicit overview, offered unselected keyboard filter, matching HTTP 200
with valid total, selected state and non-busy map. Case: actual offered link,
loaded journey and no workspace alert. Any unproven predicate fails/blocks.
Regression tests outside package; six maximum in one new API-owned module,
including real Chromium positive/negative caller integration with constructed
actual /me HTTP response using existing EmployeeIdentityTests fixtures.
Compose the fixture instead of inheriting its seven tests. Six new tests:
expectations, projection, origin/debug, downstream/session loss, Chromium
rosterless, Chromium wrong account. P01-T01 also owns the API README example.
No historical runner modifications or generated output in source.
Completed evidence: maintained adapter, six focused tests and README.
Positive Chromium also exercises actual synthetic local observers; fixed
case navigation uses a visible offered link in the all-case list.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Validation

Use external venv installed with pip after missing src import.
Execute supplied API discovery plus Ruff, mypy; real Chromium CLI must run.
Explicitly format-check formatter-excluded runner with isolated Ruff config.
Include both new Chromium selectors as extra tests in the full gate.
Warm authorized healthz. Independently resolve expected IDs read-only; directory
denial blocks live automation before secret access, not a reason to accept
any role-bearing session. If eligible, execute chat sends, keyboard map filters
and actual case navigation with boolean observations, no record mutation.
Capture separate live-blocked statuses when prerequisite absent.
Completed locally: API 1436 tests/320 opt-in skips, six focused contracts,
two actual Chromium executions, Ruff lint/format including explicit excluded
runner format check and 125-file mypy. Two independent directory resolution
methods denied; live identity/chat/map/case blocked, zero attempts.

<!-- rpi:phase id=P02 -->
## P02: Review and publication

<!-- rpi:task id=P02-T01 -->
### P02-T01: Independent review and gate

One fresh reviewer owns original review artifact; findings routed later.
Resolve gh user id/login email locally; commit implementation and dated RPI
evidence with requested trailer. Full external gate at clean committed head and
current main, followed by receipt verification. Gate failures block push/PR
and remain external evidence, not silent skips. No force/rebase/Azure changes.
Original Review Complete / Not accepted: RV-001 and RV-002 routed to later
implementation, independent identity/live remains blocked. No repeat Review
or correction in this task. Commit/gate next; push/PR cannot be approved by
local tests while material review defects remain open.
