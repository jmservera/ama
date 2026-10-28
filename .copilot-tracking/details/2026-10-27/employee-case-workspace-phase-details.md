<!-- markdownlint-disable-file -->
# RPI Phase Details: employee-case-workspace

## Metadata

Task ID/slug: employee-case-workspace. Plan:
.copilot-tracking/plans/2026-10-27/employee-case-workspace-plan.md.
Research: .copilot-tracking/research/2026-10-27/employee-case-workspace-research.md.

## Phase Index

| Phase | Status | Tasks |
| --- | --- | --- |
| P01 | Complete | P01-T01, P01-T02 |
| P02 | Complete | P02-T01 |

<!-- rpi:phase id=P01 -->
## P01: Implement bounded recovery and honest scope

Keep all source changes surgical. No visual overhaul, dependencies, public
static exemption, change to role capabilities or approved AI release.

<!-- rpi:task id=P01-T01 -->
### P01-T01: Guard shared scripts and support document reload

C1/C2: missing ops.js currently yields ReferenceError, then Try again invokes
route only. Before dispatching a route, test representative exports using safe
typeof checks only for the selected route: staff case requires panels, ops,
assistants and chat; contractor list/capacity require ops; dedicated assistants,
time, finance and specialist destinations require their own module; map
destinations require Leaflet. Ordinary case/list routes do not require specialist
screens or Leaflet. Never evaluate an undefined variable unsafely.
Render a native error screen with named paths and a document reload button.
No automatic repeated retries. Preserve current hash/query and session.
Use existing show/focus/live-status styling. Generic API retry unchanged.
Evidence: healthy case and injected missing ops; verify exact path, no pageerror,
keyboard reload recovery and reflow. Missing specialist module does not block
ordinary case/list; visiting that affected destination shows its named error.

<!-- rpi:task id=P01-T02 -->
### P01-T02: Clarify briefing assignment and AI runbook

C3/C4: select owner_code exact match, exclude closed. Change only the misleading
empty fallback text. Unbound verified staff remain authorized by app roles and
can inspect permitted all-case views; no owner inference by role/email.
C5/W1: document AI_ENDPOINT, AI_DEPLOYMENT (default standard),
AI_DEPLOYMENT_STRONG (default capable), AI_MODEL_VERSION and
AI_MODEL_VERSION_STRONG, AZURE_CLIENT_ID and platform-provided identity transport,
OpenAI User role, network and per-task release/incident gates. ZF_AI off is
intentional workflow-only; resident ZF_DEMO_ASSISTANT_* are not employee settings.
Record exact image observation and remaining authenticated browser gap.
Read existing Fluent/content/WCAG guidance before web edits.

<!-- rpi:phase id=P02 -->
## P02: Verify source behavior and reconcile evidence

Depends on P01. Maximum tests and ownership are locked in the plan.

<!-- rpi:task id=P02-T01 -->
### P02-T01: Add and run focused HTTP/unit/browser checks

Extend existing public fixture suites, not private-data generator runs.
Use JSON/SQLite task mixin for briefing and no-model-call assertions.
Trusted-proxy HTTP uses only test tenant/object IDs in a loopback server, never
a forged principal against Azure. Static shell aliases and protected assets
must preserve CSP/no-store/nosniff and exact installed bytes.
New focused check reuses checks.design_system_browser_check.main:
renamed synthetic case ZF-2026-0597, real src/api server, local password flow,
blocked or intercepted external map tiles. Three scenarios: healthy (including
one transient case API 503, keyboard Try again, no document/script refetch),
404 ops, and 404 specialist script (ordinary routes work; specialist fails
explicitly). Ops scenario starts with nonempty location.search and case hash;
keyboard reload refetches ops, preserves exact search/hash and signed-in session,
then shows quality heading without pageerror.
Run focused suites then required full API discovery, no full rpi-checks gate.
Independent Review is a distinct single later phase, never a self-approval.
Completion evidence belongs in changes and Review, not invented acceptance.

## Completion Evidence

P01/P02 implemented and reconciled. API discovery: 1130 tests, OK with 314
explicit opt-in skips, 411.838s. Focused API suites: 90 tests OK. New browser
three-scenario check and existing eight-role workbench check passed in Chromium
156.0.8078.4. Changed-file Ruff/mypy, Node syntax and diff whitespace passed.
Negative control shows original exact undefined-helper error and no refetch.
No remaining active plan markers. Live/browser mapping, real AI, SQL Server
opt-ins, human/screen-reader and deployment acceptance remain unavailable.
