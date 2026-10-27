<!-- markdownlint-disable-file -->
# RPI Plan: employee-case-workspace

## Task Metadata

* Task ID and slug: employee-case-workspace
* Date: 2026-10-27
* Status: Ready, single critique dispositions applied
* Details: .copilot-tracking/details/2026-10-27/employee-case-workspace-phase-details.md
* Critique: .copilot-tracking/reviews/plans/2026-10-27/employee-case-workspace-plan-critique.md

## Executive Summary

Make a failed employee dependency load actionable instead of exposing an
undefined helper and an ineffective route-only retry. Keep personal briefing
scope explicit and document employee AI configuration and redeploy requirements.
Preserve authorization, Fluent styling, controlled records and manual paths.

### What You May Not Know

The serving image already wires matching ops.js bytes. Local synthetic
ZF-2026-0597 works. The exact original authenticated request/execution failure
is NOT proven; no authenticated browser session is available. Current recovery
is defective when that script is missing. Empty personal assignment is consistent
with Entra identities that have no matching seeded owner code. Employee AI
endpoint configuration is absent in safe deployed environment-name metadata.

## User Decisions and Requirements

* Execute Research, Plan, Implement and Review with dated committed artifacts.
* Diagnose deployed employee case and briefing, not resident-demo behavior.
* Use src packages and synthetic local unittest/Playwright checks; no uv,
  .env, secrets, private data, Azure deployment or resource deletion.
* Use existing topic branch, push normally, one PR with Refs, not Closes.
* Follow /tmp/brief-common.md: no full gate; this small source change uses
  focused local checks rather than the optional large-change scoped gate.

## Goals

* Recover visibly from a missing employee script while preserving deep links.
* Distinguish no assigned work from no programme work.
* Separate source evidence from unavailable authenticated/live acceptance.

## Scope and Non-Goals

In scope: src/api web dependency readiness, HTTP/browser regression checks,
src/core briefing text and corresponding tests, src/api README runbook.
Non-goals: deployment, ownership reassignment, identity grants, model invocation,
CSP/auth weakening, duplicated quality helpers, visual redesign or issue closure.

## Functional Requirements

* Selected-route shared-script absence shows the exact asset path and full-page reload,
  rather than rendering a partial case or raw ReferenceError. Reload preserves
  the original fragment. Generic API errors keep existing route retry.
* Briefing remains restricted to not-closed cases with exact owner_code match.
  Empty copy explicitly describes assignment, not programme-wide absence.
* Documentation names employee AI endpoint, both deployments, model attestations,
  identity/RBAC and activation prerequisites; resident settings are separate.

## Non-Functional Requirements

* Native heading/status/button and existing focus styles; keyboard recovery
  works and changed error view fits 320/390/1280px. No conformance claim.
* Normal case path retains quality controls and script execution order; no
  extra external requests, model calls or changed authorization.
* Tests read constructed public fixtures only, isolated from environment.

## Acceptance Criteria

* AC1: real synthetic API/Chromium case ZF-2026-0597 renders quality panel with
  no pageerrors; required script responses are 200 JavaScript under actual CSP.
* AC2: intercept ops.js as 404, show named failure and reload; remove interception,
  keyboard reload requests ops again and renders same deep-linked case, preserving
  search/fragment and signed-in session. An unrelated specialist-script failure
  must not block ordinary case/list routes. A transient case API error retains
  route-only retry without document or script refetch.
* AC3: HTTP tests cover /app, query-bearing /app and /index.html shell parity,
  script status/content/MIME/no-store/CSP plus protected trusted-proxy behavior.
* AC4: JSON and SQLite synthetic tests prove unbound Entra has no own cases
  while all permitted cases remain; unique tenant+OID binding restores matching
  seeded ownership, not display-email equality. Closed cases excluded.
* AC5: no endpoint means explicit template reason with zero model calls;
  settings documentation covers both model tiers and independent release gate.
* AC6: PR discloses unproven original live HTTP cause/current owner mapping,
  no deployment, settings needed, tests and remaining owner acceptance.

## Sources

* .copilot-tracking/research/2026-10-27/employee-case-workspace-research.md:
  C1-C5, W1-W3, exact asset and identity observations.
* #73 and #360: broader acceptance remains open; use Refs only.
* docs/prds/zava-forward-retrofit-programme-demonstrator.md: FR-001-007,
  SA-001-010, role/case boundaries.
* docs/brds/agentic-retrofit-programme-brd.md: CON-008, verified tenant+OID,
  no prerequisite staff roster for login.
* docs/adrs/0002-pilot-readiness-architecture.md: service-enforced roles,
  release-controlled AI.
* Web Interface Guidelines fetched 2026-10-27; repository Fluent/content baseline
  takes precedence over generic title-case/Unicode suggestions.

## Phase Checklist

<!-- rpi:phase id=P01 -->
### [x] P01: Implement bounded recovery and honest scope

<!-- rpi:task id=P01-T01 -->
#### [x] P01-T01: Guard shared scripts and support document reload

Detect selected-route file helper availability before route rendering; show named
missing dependencies, native reload control and no partial-workspace success.

<!-- rpi:task id=P01-T02 -->
#### [x] P01-T02: Clarify briefing assignment and AI runbook

Update fallback wording without widening data selection. Document observed
deployment identity/digest and exact redeploy/environment prerequisites.

<!-- rpi:phase id=P02 -->
### [x] P02: Verify source behavior and reconcile evidence

Depends on P01.

<!-- rpi:task id=P02-T01 -->
#### [x] P02-T01: Add and run focused HTTP/unit/browser checks

Extend existing API tests and add an isolated check reusing the existing
real-server synthetic harness. Record exact passes and any unrelated failures.

## Test Ownership and Validation Lock

* Canonical targets: app.js, core/store.py, test_ui_support.py, test_auth.py,
  test_ai_tasks.py, checks/employee_workspace_browser_check.py, API README.
  No generated source targets.
* Tests owned by existing component suites. Removals: none. Maximum additions:
  8 unittest methods and 1 focused browser module, up to 3 browser scenarios.
* Semantic coverage: assignment scope and configuration fallback. Regression:
  actual asset HTTP execution/failure/reload and full existing API unittest
  discovery per README; targeted core tests where relevant.
* Commands: API PYTHONPATH=tests:../core/tests:../agents/tests python3 -m unittest
  test_ui_support test_auth test_ai_tasks -q, then API unittest discovery.
  python3 -m checks.employee_workspace_browser_check; node --check app.js;
  relevant existing lint/type checks and git diff --check.
* No full gate, no Azure/SQL/model integration acceptance. Existing API discovery
  may skip explicit live/SQL opt-ins; report them as skipped, never passed.

## Dependencies

Installed pip distributions in /tmp/ama-emp-ui-20261027 and existing Chromium.
No new dependency manifest changes or tooling.

## Critique Disposition

Single critique executed: Complete / Revise, original unchanged.

| Finding | Disposition | Resolving evidence |
| --- | --- | --- |
| PC-001 | Accepted, direct | P01-T01 guards actual selected-route dependencies only; ordinary case/list negative control for missing specialist script |
| PC-002 | Accepted, direct | AC2 and details require API retry without navigation/refetch, search+fragment preservation, same session and keyboard document reload |
| PC-003 | Rejected, conflicting authority | Critique cites worker-specific filesystem constraints not present in the parent task. Owner explicitly supplied /tmp/brief-common.md and external gate conventions. Isolated /tmp interpreter was installed after actual ModuleNotFoundError; no parent restriction forbids it. Keep current permitted environment and synthetic harness. |

## Follow-Up Items

* Obtain authenticated deployed script status/console and current permitted
  owner mapping from the owner/operator; no private data inferred or read here.
* Owner-authorized redeploy and qualified employee AI activation remain separate.

## Handoff

Implementation changes record:
.copilot-tracking/changes/2026-10-27/employee-case-workspace-changes.md.
Implementation P01/P02 complete; ready for single independent Review.
The full requested live diagnosis remains partial; original authenticated
request and owner mapping require owner/operator evidence.
