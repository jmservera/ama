---
title: Employee briefing manager visibility plan
description: Scoped programme briefing delivery plan
ms.date: 2026-10-28
---

Task ID: employee-briefing-manager-visibility
Status: P01/P02 and P03-T01 complete; publication pending.

## Executive Summary

Managers receive a clearly labelled summary drawn from all permitted open
programme cases. Personal assignments remain unchanged. Reuse existing roles,
case reads, ranking, draft/release controls and role-projected status; isolate
the cache by actor and current permission/scope context. Prove the result on
JSON and SQLite plus a synthetic loopback browser, not Azure.

## Sources

Research: .copilot-tracking/research/2026-10-28/employee-briefing-manager-visibility-research.md
(C1-C10). Owner request and /tmp/brief-common.md. PR #514 is merged at reviewed
base 98b0bb98f2424dd23c00e386378f44892a7a79e0. Refs #73, #104, #360;
no whole-issue acceptance or closure.

## User Decisions and Requirements

* Owner decision 2026-10-28: "Show all programme cases to manager roles on the briefing".
* Use only existing manager role constants and existing permitted-case checks.
* Label manager scope "All programme cases", not "your cases".
* Other briefings stay assignment-only; unbound identities gain no assignments.
* Preserve resident consent, home scope, human approvals and authorization.
* Add src/api unittest coverage on both existing stores and a real browser check.
* Full finite RPI loop, dated evidence, push topic branch and Refs PR requested.
* No Azure deployment, secrets/.env, private datasets or uv. Owner brief forbids
  full --all; this small source change uses planned local unit/browser checks.

## Goals

Populate manager briefings with already-permitted programme work without
misrepresenting assignment or the existing top-eight summary as an exhaustive list.

## Scope and Non-Goals

Scope: Store.briefing, app.js aiBox, directly coupled cache release tests,
API task tests, one focused browser check and API README.
Non-goals: My cases/counts/navigation, new roles, auth changes, AI activation,
priority changes, SQL schema, deployment and whole-epic acceptance.

## Functional Requirements

* FR1: existing MANAGER_ROLES select list_cases(user, "all"); others select mine.
* FR2: only existing briefing-permitted roles can invoke the store briefing.
* FR3: exclude closed/unpermitted cases before ranking and the top-eight cap.
* FR4: return scope, scope_label, case_count and summary_count; render that label
  and explicit counts in Today's briefing, with neutral loading/refresh copy.
* FR5: preserve personal lists/counts; unbound manager programme view is not assignment.
* FR6: use projected status in prompt facts and retain draft/release/citation checks.
* FR7: cache separates current code/email/role/reason visibility/full ordered permitted IDs/mode.

## Non-Functional Requirements

Reuse Store.list_cases and shared inherited briefing for JSON/SQL parity.
Keep existing Fluent semantics, native controls, human review and safe manual
paths. No prompt template/version, dependency manifest or schema change.
No new network/resource calls beyond the existing local test harness.

## Acceptance Criteria

* AC1: both manager roles include another owner's open work and exclude closed work.
* AC2: all other staff roles retain exact owner scoping; unbound non-managers have
  no briefing cases, and unbound managers retain zero personal assignments.
* AC3: selected IDs, model facts and counts respect a restricted permitted read;
  unsupported/contractor/admin-only identities cannot obtain a briefing.
* AC4: role/actor/reason-policy/permitted-set changes cannot reuse another scope's
  cached result; existing continuity/release cache regressions still pass.
* AC5: Programme Support Officer facts omit held private waiting text; controlled
  case data remains unchanged by briefing generation.
* AC6: >8 open programme cases report the full eligible total but summarize only
  ranked top eight, preserving hazard-first order.
* AC7: actual browser sees All programme cases for both managers and My assigned
  cases for other staff; My cases queue remains personal, including empty manager.
* AC8: required API discovery, focused core/release/role checks and browser run
  have recorded outcomes. Missing opt-in/live/human checks remain explicit.

## Test Ownership and Change Budget

Canonical semantic owner: existing TasksMixin in src/api/tests/test_ai_tasks.py,
executed by JsonTasks and SqlTasks. Add at most nine methods for AC1-AC6.
Existing non-manager identity regressions remain, no removals. Adjust at most
two existing cache-internals references in test_assistant_release.py to match
the new key without weakening their stale-release behavior.
Browser owner: one new src/api/checks/employee_briefing_browser_check.py using
the existing synthetic real-server harness. No generated production assets.
Regression coverage: existing API discovery, role/release/task suites and core
sensor prompt guards. No new test framework or dependencies.

## Phase Checklist

<!-- phase:P01 -->
### P01: Implement scoped briefing and visible scope

* [x] P01-T01: select permitted role-dependent briefing cases and isolate cache.
* [x] P01-T02: render scope/counts and neutral loading/refresh wording.
* [x] P01-T03: update API README with programme-vs-assigned semantics and commands.

<!-- phase:P02 -->
### P02: Verify semantic and regression boundaries

* [x] P02-T01: add paired store tests and maintain existing cache release tests.
* [x] P02-T02: add and run synthetic browser check for manager/non-manager labels.
* [x] P02-T03: run API discovery, focused core tests and changed-file lint/type checks.

<!-- phase:P03 -->
### P03: Independent review and publication

* [x] P03-T01: reconcile plan/details/changes and run exactly one independent Review.
* [ ] P03-T02: record original review outcome, commit dated evidence, inspect exact
  candidate and push topic branch with Refs PR.

## Critique Disposition

Execution Complete, original verdict Revise (one High, one Medium). Original:
.copilot-tracking/reviews/plans/2026-10-28/employee-briefing-manager-visibility-plan-critique.md.

| Finding | Disposition | Resolving plan evidence |
| --- | --- | --- |
| PC-001 Medium: selected IDs omit eligible count changes | Applied directly | FR7/P01-T01 include full ordered eligible IDs; P02-T01 covers >8 to >8-minus-one permitted count at unchanged version |
| PC-002 High: missing publication stop | Applied directly | P03-T01/T02 stop publication on unresolved acceptance-blocking findings; only justified nonblocking residuals may defer |

No new user choice, test-budget increase or repeat critique. Executive summary
remains accurate.

## Follow-Up Items

Existing PR #514 live diagnosis/deployment/model activation residuals remain
outside this task. Human/user/accessibility acceptance is not established by
constructed browser checks.

## Handoff

Details: .copilot-tracking/details/2026-10-28/employee-briefing-manager-visibility-phase-details.md
Critique: .copilot-tracking/reviews/plans/2026-10-28/employee-briefing-manager-visibility-plan-critique.md
Changes (implementation-owned):
.copilot-tracking/changes/2026-10-28/employee-briefing-manager-visibility-changes.md
