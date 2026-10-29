---
title: Employee chat skills 530 implementation plan
description: Local bounded chat implementation and evidence plan
ms.date: 2026-10-29
---

Task: 530 / employee-chat-skills-530. Status: source implemented; Review ready
with explicit full-suite/SQL/publication blockers, not acceptance complete.

## Executive Summary

Extend the existing read-only ChatPanel with explicit five-skill selection and
general workflow help. Add one native dialog launcher to the employee shell,
reusing the current endpoint and async feedback. No router, tools or domain
writes. Preserve legacy callers and all privacy/authorization gates.

## User Decisions and Requirements

* Full ordered RPI loop and local Conventional Commits; no push, az or closing keywords.
* Use repository capability IDs, existing chat modules, Fluent 2 and async-action.
* Case context only through current role projection; label every answer.
* Audit questions by message reference, skill and outcome without duplicating text.
* Run API/core Ruff, formatting, mypy, units and relevant browser/axe; SQL is separate.
* Use nonblocking shared lock for heavy suites. PR #529 is merged.

## Goals

Make bounded advisory chat available across staff routes with defensible
context, failure handling and evidence.

## Scope and Non-Goals

API/core/web chat and tests/docs only. No router, resident chat change, new
model SDK, deployment, actual inference or approval/sending/record mutation.

## Functional Requirements

Five skill IDs/purposes derive from assistants.REGISTRY. Selecting a skill
adds its bounded purpose and category restrictions, never proposal authority.
General questions receive cited workflow-only knowledge and visibility caveat.
Record facts use existing projected/allowlisted case sources. Validate skill
before storing or inference. Audit outcome by thread/question sequence and
selected skill. Keep the existing case panel intact.

## Non-Functional Requirements

At most one model call per turn. Native modal focus trap/Escape/return focus,
text-only rendering, live updates, narrow viewport and reduced motion.
No unnecessary personal data in audit or diagnostics. Privacy gates unchanged.

## Acceptance Criteria

Tests cover all five skills/general, same-role and cross-role/thread/case
denial, changed scope, citations, missing/invalid model output, refusal and
unchanged case state, minimal audit. Browser covers global navigation,
context changes, keyboard/focus/live/reduced motion and axe. SQL and live
verification are separately recorded, never inferred from SQLite or mocks.

## Phase Checklist

<!-- P01 -->
### P01: Bounded service
* [x] P01-T01 Extend ChatPanel with skill registry/prompt/general context/audit.
* [x] P01-T02 Expose skill metadata and pass validated skill at existing ask route.
<!-- P02 -->
### P02: Employee shell
* [x] P02-T01 Add native dialog/global launcher and route-bound context reset.
* [x] P02-T02 Preserve case panel; reuse AsyncAction and Fluent tokens.
<!-- P03 -->
### P03: Verification and documentation
* [x] P03-T01 Extend existing API/core test ownership; add one browser check.
* [ ] P03-T02 Run required static/unit/browser checks and attempt SQL evidence.
* [x] P03-T03 Update API guide and dated changes; prepare independent Review and local commits.

## Test Ownership and Change Budget

Canonical targets: chat_panel.py, server.py, chat.js, app.js, index.html,
style.css, existing test_chat_panel.py files and one employee chat browser check.
No test removals. At most 12 new unit methods and one browser module.
Implementation amendment: update test_workspace_scripts route-readiness
expectations because chat.js now serves every staff route, and extend the
existing constructed browser server with an opt-in synthetic privacy fixture.
No inherited environment/model configuration is added.
Semantic checks: allowed data/prompt/audit/citations and UI outcomes.
Regression checks: existing legacy case panel/privacy/isolation and workspace.
No generated or pinned scenario files expected to change.

## Critique Disposition

One independent critique executed, original verdict Revise preserved.
PC-001 accepted: dispose on login/session change, denial and navigation;
suppress delayed results with disposed-state checks and abort signal.
PC-002 accepted: omitted skill retains legacy; explicit "general" enables
workflow help; only string registry IDs/general accepted; null/unknown rejected
before persistence/inference. Per-turn selection, no thread task schema change.
PC-003 accepted: new browser scans the open dialog with pinned axe in answer
and fallback states.
PC-004 partially rejected: its claimed /tmp prohibition does not exist in the
parent execution context and conflicts with the user's explicit /tmp/mv and
/tmp lock directions. Preserve those directions. Explicit worktree PYTHONPATH
prevents cross-worktree bindings; further environment mutation is lock-bound.
PC-005 accepted: full publication gate is blocked because it invokes forbidden
az; no invocation, fabricated receipt or publication. Record after local commits.

## Follow-Up Items

Live employee-site and screen-reader/voice-control acceptance remain separate.
Complete publication gate is not permission to push and cannot use forbidden az.
P03-T02 remains partial: permitted static and targeted unit/browser checks
pass; full suites and actual SQL are blocked by occupied shared heavy lock.

## Handoff

Research: .copilot-tracking/research/2026-10-29/employee-chat-skills-530-research.md.
Details: .copilot-tracking/details/2026-10-29/employee-chat-skills-530-phase-details.md.
Changes: .copilot-tracking/changes/2026-10-29/employee-chat-skills-530-changes.md.
Source tasks P01/P02 and P03-T01/T03 are complete. P03-T02 remains blocked
only for full-suite/SQL coverage. Independent Review must preserve that boundary.
