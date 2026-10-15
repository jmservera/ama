---
title: Role workbench IA 152 phase details
description: Marker-addressed implementation context and evidence expectations
ms.date: 2026-10-15
---

Task `152`, slug `role-workbench-ia-152`; plan is the task-wide authority.
P01 and P02 implementation/evidence complete. Publication is the parent
post-Review action, not a prerequisite pretending Review already ran.

<!-- P01 -->
## P01: Shared navigation and recoverable context

<!-- P01-T01 -->
### P01-T01: Server navigation

API-owned typed metadata describes existing routes using projection.allowed
and existing Finance/manager rules. Add metadata to `/api/me`; no permissions
change. Test all eight implemented roles, unknown role default-deny, endpoint
access and contractor minimum projection. Navigation is not authorization.

<!-- P01-T02 -->
### P01-T02: Web IA

Render server links without new client role predicates. Add primary navigation
label, current-page state, skip link and persistent page status. Track last
queue scope for case back links; retain search/filter values until explicit
reset. Reset returns mine and urgent order, clears pending debounce, focuses
the new reset button and announces the refreshed result. Keep status/error
handling explicit. Move existing safety panel ahead of routine forms; do not
collapse controls. CSS uses existing tokens and min-width:0/wrapping.

PC-003: per-route AbortController cancels obsolete async loads. Query state
updates immediately; route/reset clears debounce. Back restores mine/all and
filters, explicitly reloading page one; direct case entry falls back to mine.

<!-- P02 -->
## P02: Evidence and delivery

<!-- P02-T01 -->
### P02-T01: Synthetic manifest and browser evidence

Use the existing dataset fixture and real loopback app; no environment model
credentials inherited. Reuse the existing browser launcher with typed
callables. Versioned JSON declares active shared-IA slice, eight implemented
role checks and all eleven PRD perspectives/nine workflows with explicit
deferred endpoints when not represented. Freeze expected own/default IDs/order
before checking reset. Verify filters/no match/all override, back restoration,
focus/live status, safety markers/panel and unchanged records. Check
320/390/768/1024/1280 and enlarged text. Existing AI endpoints/config are
untouched; offline browser run is not actual inference evidence.

PC-002/004/005/006: API fixture extends the shared data with eight auth roles,
two owners, empty own queue and other-contractor scope. JSON freezes expected
IDs/order/navigation independently, and declares all eleven perspectives/nine
workflows as represented or deferred. Scratch is under ignored `.venv/`,
removed by context manager. Existing CI browser entry point runs both checks.
Check queue/case at five widths, 200% root text at 1280px, long source wrapping,
keyboard skip/case/back/reset, current route, count status, errors and delayed
route cancellation. Do not add staff safety fields to contractor projection.

<!-- P02-T02 -->
### P02-T02: Validation

After missing-dependency failure, create only a worktree-local ignored venv,
install with pip editable src packages and their dev tools. Run five project
suites with documented shared-test PYTHONPATH, existing ruff/mypy configs,
strict checks for new browser code, node syntax, both browser checks and a
Docker build attempt. Record exact commands and outcomes/skips in changes.
Any baseline failure must be distinguished from introduced regressions.

<!-- P02-T03 -->
### P02-T03: Documentation/review/publication

Use existing UX synthesis for durable scope/reset findings, API README for
commands/boundaries, index row and append-only log. Leave owner memory and
original case unchanged. Reconcile task markers, changes and limitations
before invoking one Review. Review findings route to future work, not another
implementation/review loop. Resolve authenticated user before repository-local
email configuration; include required coauthor trailer. Commit artifacts/code,
push only the named topic and open main PR with command/results and unchecked
criteria. CI image evidence is separate from unexecuted SQL/model/Azure checks.
PC-001: introduced failures must be resolved and tested before Review. A
material Review defect blocks readiness, even though the single review has
executed; any resulting PR must disclose not-ready status. Do not merge.

## Implementation Reconciliation

No permission/store/SQL/model changes. New code/test file budget respected.
Root `.gitignore` now excludes the worktree-local venv/scratch. Route lifetime
handling also touches existing Finance/proposal/time catch paths and map draw:
aborted old requests must not replace new views or reject unhandled promises.
These are tightly coupled cancellation fixes, not role-screen expansion.
Generic wrapping initially shrank scrollable tables; final CSS preserves
normal wrapping inside named table-scroll regions while other case content
wraps. Both baseline and IA browser suites pass with original scrolling
assertions retained. Owner devices/full journeys/live/human checks remain open.
